from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageChops
import sys
import json
import math
import uuid
from better_json_tools import load_jsonc
from enum import Enum, auto
from typing import Literal

class SpecialKeys(Enum):
    AUTO = auto()  # Special key used for the "target" property in "_map.py"

DATA_PATH = Path("data")
FILTER_DATA_PATH = Path("data/shapescape_texture_tools")

def print_red(text: str):
    '''Prints text in red.'''
    for t in text.split('\n'):
        print("\033[91m {}\033[00m".format(t))

class TextureManipulationException(Exception):
    '''Base class for exceptions in this module.'''
    pass

class Tile:
    '''
    A wrapper around a PIL image that allows applying operations to the image
    in tiles.
    '''
    def __init__(self, image: Image):
        self.image: Image = image
        self.tiles: tuple[int, int] = (1, 1)

    def set_tiles(self, tiles: tuple[int, int]):
        '''Sets the number of tiles in the image.'''
        if (
                any((i <= 0 or not isinstance(i, int)) for i in tiles)
                or len(tiles) != 2):
            raise TextureManipulationException(
                "The 'tiles' property must be a tuple of two positive integers"
            )
        im_size: tuple[int, int] = self.image.size
        _, reminder = divmod(im_size[0], tiles[0])
        if reminder != 0:
            raise TextureManipulationException(
                f"Image width ({im_size[0]}) is not divisible by the number of "
                f"tiles ({tiles[0]})")
        _, reminder = divmod(im_size[1], tiles[1])
        if reminder != 0:
            raise TextureManipulationException(
                f"Image height ({im_size[1]}) is not divisible by the number of "
                f"tiles ({tiles[1]})")
        self.tiles = tiles

    def get_tile_coordinates(self, tile_index: int) -> tuple[int, int, int, int]:
        '''Gets the position of a tile: (x, y, x+width, y+height)'''
        tile_size: tuple[int, int] = (
            self.image.size[0] // self.tiles[0],
            self.image.size[1] // self.tiles[1])
        tile_pos = (
            (tile_index % self.tiles[0]) * tile_size[0],
            (tile_index // self.tiles[0]) * tile_size[1])
        return tile_pos + tuple(
            pos+size for pos, size in zip(tile_pos, tile_size))

    def _get_tile_indices(self, tile: int) -> list[int]:
        '''
        Returns a list of tile indices for various tile operations. If the tile
        is -1, all tiles are returned.
        '''
        return (
            [tile] if tile != -1 else
            list(range(self.tiles[0] * self.tiles[1]))
        )

    def paste(self, image: Image, position: tuple[int, int], tile: int = -1):
        '''
        Pastes an image into the tile. If the tile is -1, the image is pasted
        into all tiles. The tiles are indexed from left to right, top to
        bottom. The index of the first tile is 0.
        '''
        for tile_index in self._get_tile_indices(tile):
            tile_crds = self.get_tile_coordinates(tile_index)
            # Get the tile as separate image
            tile_image = self.image.crop(tile_crds)
            # Paste the 'image' into the tile
            tile_image.paste(image, position)
            # Paste the tile back into the self.image
            self.image.paste(tile_image, tile_crds[:2])

    def offset(self, offset: tuple[int, int], tile: int = -1):
        '''
        Offsets the tile. If the tile is -1, all tiles are offset by the same
        amount.
        '''
        for tile_index in self._get_tile_indices(tile):
            tile_crds = self.get_tile_coordinates(tile_index)
            # Get the tile as separate image
            tile_image = self.image.crop(tile_crds)
            # Shift the tile
            tile_image = ImageChops.offset(
                tile_image, offset[0], offset[1])
            # Paste the tile back into the self.image
            self.image.paste(tile_image, tile_crds[:2])

    def scale(self, scale: tuple[float, float]):
        '''Scale the image.'''
        width, height = self.image.size
        scaled_width = width * scale[0]
        if scaled_width != int(scaled_width):
            raise TextureManipulationException(
                f"The scaled image width is not an integer "
                f"({width} * {scale[0]} = {scaled_width})")
        scaled_height = height * scale[1]
        if scaled_height != int(scaled_height):
            raise TextureManipulationException(
                f"The scaled image height is not an integer "
                f"({height} * {scale[1]} = {scaled_height})")
        self.image = self.image.resize(
            (int(scaled_width), int(scaled_height)), Image.NEAREST)

class ImageBuilder:
    '''Builds an image from a list of operations.'''
    def __init__(self, size: tuple[int, int], background: str):
        self.tile: Tile = Tile(Image.new("RGBA", size, background))

    def apply_operations(self, operations: list[dict]):
        '''Applies a list of operations to the image.'''
        for i, operation in enumerate(operations):
            if operation["type"] == "paste":
                self.paste(
                    Path(operation["image"]),
                    tuple(operation["source_position"]),
                    tuple(operation["source_size"]),
                    tuple(operation["target_position"]),
                    operation.get('tile', -1)
                )
            elif operation["type"] == "offset":
                self.tile.offset(
                    tuple(operation["offset"]),
                    operation.get('tile', -1)
                )
            elif operation["type"] == "set_tiles":
                self.tile.set_tiles(tuple(operation["tiles"]))
            elif operation["type"] == "scale":
                self.tile.scale(tuple(operation["scale"]))
            else:
                raise TextureManipulationException(
                    f"Unknown operation type (operation {i}): {operation['type']}")

    def paste(
            self,
            source_path: Path,
            source_pos: tuple[int, int],
            source_size: tuple[int, int],
            target_pos: tuple[int, int],
            tile: int):
        '''An operation that pastes an image into the image.'''
        source_image = Image.open(source_path)
        source_image = source_image.crop(
            source_pos +
            tuple(pos+size for pos, size in zip(source_pos, source_size))
        )
        # Paste the image into self.tile.image
        self.tile.paste(source_image, target_pos, tile)

    def save(self, output: Path):
        '''Saves the image of the builder to a file.'''
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.exists():
            raise TextureManipulationException(
                f"Output file already exists: {output}")
        print(f"Creating image: {output}")
        self.tile.image.save(output)

def main():
    # Load the config
    config = {}
    if len(sys.argv) > 1:
        try:
            config = json.loads(sys.argv[1])
        except Exception:
            raise TextureManipulationException([f'Failed load the config data'])
    scope_path = DATA_PATH / config.get(
        'scope_path', 'shapescape_texture_tools/scope.json')

    # Load the scope based on the defaults and the data from the config
    scope = {
        'true': True, 'false': False, 'math': math, 'uuid': uuid,
        "AUTO": SpecialKeys.AUTO}
    scope = scope | load_jsonc(scope_path).data

    for task in (FILTER_DATA_PATH).rglob("*.py"):
        data = eval(task.read_text(), scope)
        try:
            for image in data:
                img_builder = ImageBuilder(image['size'], image['background'])
                img_builder.apply_operations(image['operations'])
                img_builder.save(Path(image['output']))
        except TextureManipulationException as e:
            print_red(f"Failed to finish task: {task.as_posix()}")
            print_red(str(e))
            sys.exit(1)

if __name__ == "__main__":
    main()
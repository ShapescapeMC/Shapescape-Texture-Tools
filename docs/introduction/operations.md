(operations)=
# Operations

Operations are the building blocks of the tasks. They describe how to transform the background image to get the final image. The operations are defined as a list of dictionaries. Each dictionary defines a single operation that should be applied to the background image. The operations are applied in the order they are defined in the list.

## Operation Types

### `paste`
The `paste` operation pastes an image or a selected area of an image on top of the background image.

```json
{
  "type": "paste",
  "image": "data/shapescape_texture_tools/sky.png",
  "source_position": [0, 0],
  "source_size": [1000, 1000],
  "target_position": [0, 0]
}
```
- `image`: Path to the image to paste.
- `source_position`: Position of the top left corner of the area to copy from the source image.
- `source_size`: Size of the area to copy from the source image.
- `target_position`: UV coordinates on the background image to paste the source image to.

### `scale`
The `scale` operation scales the image by a given factor.

```json
{
  "type": "scale",
  "scale": [0.5, 0.5]
}
```
- `scale`: The scale to apply to the image.

### `offset`
The `offset` operation shifts the image by a given number of pixels.

```json
{
  "type": "offset",
  "offset": [1, 0]
}
```
- `offset`: The offset to apply to the image.

### `set_tiles`
The `set_tiles` operation divides the image into a grid of tiles.

```json
{
  "type": "set_tiles",
  "tiles": [3, 2]
}
```
- `tiles`: Number of tiles in the X and Y direction.

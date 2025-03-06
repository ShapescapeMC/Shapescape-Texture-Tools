# 📝 Description
This filter allows you to create textures by transforming other textures.

# 💿 Installation
**1.** Install the filter with command:
```
regolith install github.com/Shapescape-Software/regolith-filters/texture_manipulation
```
You can also set up the Shapescape resolver by once typing this command:
```
regolith config resolvers github.com/Shapescape-Software/private_regolith_resolver/resolver.json
```

After that you can use this command to install this filter:
```
regolith install texture_manipulation
```

**2.** Add the filter to the `filters` list in the `config.json` file of the Regolith project:
```json
                    {
                        "filter": "texture_manipulation",
                        "settings": {
                            "scope_path": "texture_manipulation/scope.json"
                        }
                    },
```

# ⚙️ Configuration settings
- `scope_path: str` - a path to JSON file that diefines the scope of variables provided to the tasks during their evaluation. The `scope_path` is relative to the Regolith's filter data folder.

# ⭐ Usage
The filter is data driven. The input data is a list of Python files that define the way of combining textures. The Python files are structured in a very specific way, one task is a list of dictionaries, each dictionary defines an image that should be created. The syntax of a JSON file is also a valid Python code, so you can write the code as you would write it in JSON. Python enables you to use more complex logic thanks to Python's [comprehensions](https://www.geeksforgeeks.org/comprehensions-in-python/).


### Tasks
Tasks are defined as a list of dictionaries. Each dictionary defines a single image that should be created. The task file is a Python file with a single expression that must evaluate into a list of dictionaries that define task steps. The tasks must be placed in the folder with the data of the filter (in *data/texture_manipulation/* or any subfolder of that path)

*Task file example:*
```py
[
  {
      "output": f"RP/textures/my_image.png",
      "size": [1000, 1000],
      "background": "#00000000",
      "operations": [
        # List of operations...
      ]
  },
  {
    # ...
  },
  # More tasks ...
]
```
- `output` - the path to the output image should start with `RP/textures` if you want to export your file to the texture folder of the resource pack. The output file can use different format than the images used to compose the final image. For example, you can use a `.png` file as a source image and export the final image as a `.tga` file.
- `size` - the size of the image to create.
- `background` - the color of the background image. The operations paste the images on top of the background image to create the final image.
- `operations` - the list of operations to apply to the background image in order to get the final image.

### Operations
Operations are the building blocks of the tasks. They describe how to transform the background image to get the final image. The operations are defined as a list of dictionaries. Each dictionary defines a single operation that should be applied to the background image. The operations are applied in the order they are defined in the list.

There is a few types of operations. Every operation has a `type` field that tells the filter what type of operation it is. The rest of the fields depend on the type of the operation.

*Operation syntax:*
```jsonc
        // ...
        {
          "type": "paste",
          // The properties of operation
        },
        // ...
```
- `type` - the type of the operation to apply.


#### The `pase` operation
The `paste` operation pastes an image or a selected area of an image on top of the background image. 

*Example file that uses the `paste` operation:*
```py
[
  {
      # ...
      "operations": [
        {
          "type": "paste",
          "image": "data/texture_manipulation/sky.png",
          "source_position": [0, 0],
          "source_size": [1000, 1000],
          "target_position": [0, 0],
        }
      ]
  },
  {
    # ...
  },
]
```
- `image` - the path to the image to paste relative to the root of the working director of regolith (it can access the files in `RP`, `BP` and `data` folders).
- `source_position` - the position of the top left corner of the area to copy from the source image. The position is defined in pixels.
- `source_size` - the size of the area to copy from the source image. The size is defined in pixels.
- `target_position` - the UV coordinates on the background image to paste the source image to. The position is defined in pixels.

#### The `scale` operation
The `scale` operation scales the image by a given factor.

```py
[
  {
      # ...
      "operations": [
        {
          "type": "scale",
          "scale": [0.5, 0.5],
        }
      ]
  },
  {
    # ...
  },
]
```
- `scale` - the scale to apply to the image. The scale is defined as a factor, so for example if you want to scale the image by 2 times, you should use `[2, 2]` as the scale. You can scale the width and height of the image independently by using different values for the scale.

#### The `offset` operation
The `offset` operation shifts the image by a given number of pixels. The offset loops around the image, so for example if you offset the image by 1 pixel to the right, the rightmost pixels will be moved to the leftmost position.

*Example file that uses the `offset` operation:*
```py
[
  {
      # ...
      "operations": [
        {
          "type": "offset",
          "offset": [1, 0],
        }
      ]
  },
  {
    # ...
  },
]
```
- `offset` - the offset to apply to the image. The offset is defined in pixels.



#### The `set_tiles` operation
The `set_tiles` operation divides the image that is being processed into a grid of tiles. This operation doesn't do anything on its own, but it affects all of the subsequent operations. After this operation is applied, every operation will be applied to each tile of the image separately.

*Example file that uses the `set_tiles` operation:*
```py
[
  {
      # ...
      "operations": [
        {
          "type": "set_tiles",
          "tiles": [3, 2],
        },
        {
          "type": "offset",
          "offset": [30, 0],

          # This operation is available to any operation tha is applied to the
          # image after dividing it into tiles.
          "tile": 1
        }
      ]
  },
  {
    # ...
  },
]
```
- `tiles` - the number of tiles in the X and Y direction. The number of tiles is defined in pixels. The number of tiles must be a positive integer that evenly divides the size of the image. If the image can't be divided evenly into tiles, the operation will fail.

The example above would divide the image into 6 tiles (3x2) and then apply the `offset` operation to the tile with the index 1.

The `set_tiles` operation lets you apply changes to a specific tile. Every operation which isn't `set_tiles` has a property called `tile`. The `tile` property is an integer that defines the index of the tile to apply the operation to. The indices are defined in left to right, top to bottom order. The first tile has the index 0, the second tile has the index 1, etc. If the `tile` property is not defined it uses the default value of `-1`, which means that the operation is applied to all tiles.

If after applying changes to the tiles of the image, you want to combine the tiles back into a single image, you can use the `set_tiles` operation again with the `tiles` parameter set to `[1, 1]`. The tiles always applies to the entire image not to the tiles that were created by the previous `set_tiles` operation (you can't divide tiles into smaller tiles).

### The scope file
The scope file is a file that defines the scope for the function that evaluates the content of the tasks (the Python's `eval` function). The scope file is a JSON file that you can put anywhere in the Regolith's data folder. A scope file is valid as long as it is a valid JSON file that defines a dictionary. Additionally, the scope file supports using C-style comments which aren't part of the JSON standard. You can define the path to the scope file to be used in the `scope_path` setting of the `texture_manipulation` Regolith filter.

## Example task
Example below shows the configuraiton of a task that creates a cubemap for north, south, east and west directions from a single image. The size of the source image is 4000x1000 px and the side of each cubemap image is 1000x1000 px.

```py
[
    {`
        "size": [1000, 1000],
        "background": "#00000000",
        "output": f"RP/textures/environment/overworld_cubemap/cubemap_{i}.png",
        "operations": [
            {
                "type": "paste",
                "image": "data/texture_manipulation/images/sky.png",
                "source_position": [i*1000, 0],
                "source_size": [1000, 1000],
                "target_position": [0, 0],
            }
        ]
    } for i in range(4)
]
```

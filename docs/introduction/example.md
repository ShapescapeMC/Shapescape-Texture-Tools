(example)=
# Example

Below is an example configuration of a task that creates a cubemap for north, south, east, and west directions from a single image. The size of the source image is 4000x1000 px and the side of each cubemap image is 1000x1000 px.

```py
[
    {
        "size": [1000, 1000],
        "background": "#00000000",
        "output": f"RP/textures/environment/overworld_cubemap/cubemap_{i}.png",
        "operations": [
            {
                "type": "paste",
                "image": "data/shapescape_texture_tools/images/sky.png",
                "source_position": [i*1000, 0],
                "source_size": [1000, 1000],
                "target_position": [0, 0],
            }
        ]
    } for i in range(4)
]
```

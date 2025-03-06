[
    {
        "size": [1000, 1000],
        "background": "#00000000",
        "output": f"RP/textures/environment/overworld_cubemap/cubemap_{i}.png",
        "operations": [
            {
                "type": "paste",
                "image": "data/shapescape_texture_tools/sky/image.png",
                "source_position": [i*1000, 0],
                "source_size": [1000, 1000],
                "target_position": [0, 0],
            }
        ]
    } for i in range(4)
]
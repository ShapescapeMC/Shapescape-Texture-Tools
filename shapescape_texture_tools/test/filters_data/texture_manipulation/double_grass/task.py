[
    {
        "size": [32, 128],
        "background": "#00000000",
        "output": f"RP/textures/blocks/double_plant_grass_{side}.png",
        "operations": [
            {
                "type": "paste",
                "image": "data/shapescape_texture_tools/double_grass/image.png",
                "source_position": [0, frame*64 + variant*32],
                "source_size": [32, 32],
                "target_position": [0, frame*32],
            }
            for frame in range(4)
        ]
    } for variant, side in enumerate(['top', 'bottom'])
]

[
    {
        # Duplicate the height map to duplicate each frame
        "size": [32, 128*2],

        "background": "#00000000",
        "output": f"RP/textures/blocks/leaves_oak.png",
        "operations": [
            # Paste each frame two times stacked on top of each other
            {
                "type": "paste",
                "image": "data/shapescape_texture_tools/leaves_oak/image.png",
                "source_position": [0, j*32],
                "source_size": [32, 32],
                "target_position": [0, 32*i + j*64],
            }
            for i in range(2)  # Each frame duplicated
            for j in range(4)  # There is a total of 4 frames in the source image
        ] + [
            {
                "type": "scale",
                "scale": [2, 2]
            },
            {
                # Original image was 1x4 frames but now it's 2x8 frames
                "type": "set_tiles",
                "tiles": [1, 8]
            },
        ] + [
            {
                "type": "offset",
                "offset": offset,
                "tile": i
            }
            for i, offset in enumerate(
                [
                    (0, 0),
                    (1, 0),
                    (2, 1),
                    (1, 1),
                    (0, 2),
                    (-1, 2),
                    (-2, 1),
                    (-1, 1)
                ]
            )
        ]
    }
]

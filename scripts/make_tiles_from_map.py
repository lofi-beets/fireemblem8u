#!/usr/bin/env python3

import sys
from PIL import Image

with Image.open(sys.argv[1]) as im, open(sys.argv[2], 'rb') as f_map:
    w = int.from_bytes(f_map.read(1), 'little') + 1
    h = int.from_bytes(f_map.read(1), 'little') + 1
    if (8 * w, 8 * h) != im.size:
        print("image size doesn't match")
        sys.exit(1)
    im_tiles = Image.new('P', (8, 8 * w * h))
    im_tiles.putpalette(im.getpalette())
    max_tile = 0
    for r in range(h - 1, -1, -1):
        for c in range(0, w):
            entry = int.from_bytes(f_map.read(2), 'little')
            tile = entry & 1023
            max_tile = max(max_tile, tile)
            flipH = entry & (1 << 10)
            flipV = entry & (1 << 11)
            im_tile = im.crop((8 * c, 8 * r, 8 * c + 8, 8 * r + 8))
            if flipH:
                im_tile = im_tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if flipV:
                im_tile = im_tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            im_tiles.paste(im_tile, (0, 8 * tile))
    im_tiles = im_tiles.crop((0, 0, 8, 8 * max_tile + 8))
    im_tiles.save(sys.argv[3])

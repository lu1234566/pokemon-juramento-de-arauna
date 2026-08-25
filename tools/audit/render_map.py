#!/usr/bin/env python3
"""Render any map's block data to a PNG, exactly as the GBA composes it.

Metatiles are 2x2 tiles of 8x8 pixels drawn in two layers: the bottom layer
always paints, the top layer paints over it with colour index 0 transparent.
Tile ids below NUM_TILES_IN_PRIMARY come from the primary tileset, the rest
from the secondary one; palettes split the same way.
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NUM_TILES_IN_PRIMARY = 512
NUM_METATILES_IN_PRIMARY = 512
NUM_PALS_IN_PRIMARY = 6
TILE_BYTES = 32          # 8x8 at 4bpp
METATILE_ENTRIES = 8     # 4 bottom + 4 top


def tileset_dir(root, symbol):
    # gTileset_General -> data/tilesets/{primary,secondary}/general
    name = symbol.replace("gTileset_", "")
    slug = ""
    for i, ch in enumerate(name):
        if ch.isupper() and i:
            slug += "_"
        slug += ch.lower()
    for kind in ("primary", "secondary"):
        path = os.path.join(root, "data/tilesets", kind, slug)
        if os.path.isdir(path):
            return path
    raise SystemExit("tileset not found: %s" % symbol)


def load_tiles(png_path):
    """Return a list of 8x8 tiles, each a list of 64 palette indices."""
    img = Image.open(png_path)
    if img.mode != "P":
        img = img.convert("P")
    w, h = img.size
    px = img.load()
    tiles = []
    for ty in range(h // 8):
        for tx in range(w // 8):
            tiles.append([px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)])
    return tiles


def load_palettes(pal_dir):
    pals = []
    for i in range(16):
        path = os.path.join(pal_dir, "%02d.pal" % i)
        if not os.path.exists(path):
            pals.append([(0, 0, 0)] * 16)
            continue
        lines = open(path, "r", encoding="utf-8", errors="replace").read().split()
        nums = [int(v) for v in lines if v.isdigit()]
        colors = [tuple(nums[j:j + 3]) for j in range(2, len(nums), 3)][:16]
        while len(colors) < 16:
            colors.append((0, 0, 0))
        pals.append(colors)
    return pals


class Tileset:
    def __init__(self, root, symbol):
        d = tileset_dir(root, symbol)
        self.tiles = load_tiles(os.path.join(d, "tiles.png"))
        self.pals = load_palettes(os.path.join(d, "palettes"))
        self.metatiles = open(os.path.join(d, "metatiles.bin"), "rb").read()


def render(root, layout, out_path, grid_step=0):
    prim = Tileset(root, layout["primary_tileset"])
    sec = Tileset(root, layout["secondary_tileset"])
    palettes = prim.pals[:NUM_PALS_IN_PRIMARY] + sec.pals[NUM_PALS_IN_PRIMARY:]

    def entries(metatile_id):
        if metatile_id < NUM_METATILES_IN_PRIMARY:
            blob, base = prim.metatiles, metatile_id
        else:
            blob, base = sec.metatiles, metatile_id - NUM_METATILES_IN_PRIMARY
        off = base * METATILE_ENTRIES * 2
        return struct.unpack("<8H", blob[off:off + 16])

    def tile_pixels(tile_id):
        if tile_id < NUM_TILES_IN_PRIMARY:
            src = prim.tiles
            idx = tile_id
        else:
            src = sec.tiles
            idx = tile_id - NUM_TILES_IN_PRIMARY
        return src[idx] if idx < len(src) else [0] * 64

    w, h = int(layout["width"]), int(layout["height"])
    raw = open(os.path.join(root, layout["blockdata_filepath"]), "rb").read()
    blocks = struct.unpack("<%dH" % (w * h), raw)

    img = Image.new("RGB", (w * 16, h * 16), (0, 0, 0))
    px = img.load()
    for by in range(h):
        for bx in range(w):
            mid = blocks[by * w + bx] & 0x03FF
            ent = entries(mid)
            for layer in (0, 1):
                for quad in range(4):
                    e = ent[layer * 4 + quad]
                    tile_id = e & 0x03FF
                    xflip = (e >> 10) & 1
                    yflip = (e >> 11) & 1
                    pal = palettes[(e >> 12) & 0x0F]
                    data = tile_pixels(tile_id)
                    ox = bx * 16 + (quad & 1) * 8
                    oy = by * 16 + (quad >> 1) * 8
                    for y in range(8):
                        sy = 7 - y if yflip else y
                        for x in range(8):
                            sx = 7 - x if xflip else x
                            c = data[sy * 8 + sx]
                            if layer and c == 0:
                                continue
                            px[ox + x, oy + y] = pal[c]
    if grid_step:
        for by in range(0, h, grid_step):
            for x in range(w * 16):
                px[x, by * 16] = (255, 0, 0)
        for bx in range(0, w, grid_step):
            for y in range(h * 16):
                px[bx * 16, y] = (255, 0, 0)
    img.save(out_path)
    return img.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("layout_id")
    ap.add_argument("out")
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--grid", type=int, default=0)
    args = ap.parse_args()
    data = json.load(open(os.path.join(args.root, "data/layouts/layouts.json")))
    for layout in data["layouts"]:
        if layout["id"] == args.layout_id:
            print("%s -> %s %dx%d" % (args.layout_id, args.out, *render(args.root, layout, args.out, args.grid)))
            return
    raise SystemExit("unknown layout: %s" % args.layout_id)


if __name__ == "__main__":
    main()

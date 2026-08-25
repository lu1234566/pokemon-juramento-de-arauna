#!/usr/bin/env python3
"""Draw a tileset pair's metatiles as a labelled sheet.

Picking a replacement block by id alone is guesswork; this puts every block a
map can use on one page, in id order, so a substitution can be chosen by
looking at it. Blocks are grouped 16 per row and the row's first id is printed
down the left edge.

    python3 tools/audit/render_metatiles.py gTileset_General gTileset_Petalburg out.png
    python3 tools/audit/render_metatiles.py ... out.png --range 0x200 0x260
"""
from __future__ import annotations

import argparse
import os
import struct
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_map import NUM_METATILES_IN_PRIMARY, Tileset  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COLS = 16
CELL = 16
PAD = 4
GUTTER = 40
BEHAVIOR_MASK = 0x00FF


def attributes(root, symbol):
    name = symbol.replace("gTileset_", "")
    slug = "".join(("_" if c.isupper() and i else "") + c.lower() for i, c in enumerate(name))
    for kind in ("primary", "secondary"):
        p = os.path.join(root, "data/tilesets", kind, slug, "metatile_attributes.bin")
        if os.path.exists(p):
            blob = open(p, "rb").read()
            return list(struct.unpack("<%dH" % (len(blob) // 2), blob))
    raise SystemExit("no attributes for %s" % symbol)


def sheet(root, primary_symbol, secondary_symbol, out_path, first, last, scale):
    prim = Tileset(root, primary_symbol)
    sec = Tileset(root, secondary_symbol)
    pals = prim.pals[:6] + sec.pals[6:]
    attrs = (attributes(root, primary_symbol), attributes(root, secondary_symbol))

    def entries(mid):
        blob, base = (prim.metatiles, mid) if mid < NUM_METATILES_IN_PRIMARY \
            else (sec.metatiles, mid - NUM_METATILES_IN_PRIMARY)
        off = base * 16
        return struct.unpack("<8H", blob[off:off + 16])

    def tile(tid):
        src, i = (prim.tiles, tid) if tid < 512 else (sec.tiles, tid - 512)
        return src[i] if i < len(src) else [0] * 64

    def behavior(mid):
        table, i = (attrs[0], mid) if mid < NUM_METATILES_IN_PRIMARY else (attrs[1], mid - NUM_METATILES_IN_PRIMARY)
        return (table[i] & BEHAVIOR_MASK) if i < len(table) else 0

    available = NUM_METATILES_IN_PRIMARY + len(sec.metatiles) // 16
    ids = list(range(first, min(last, available)))
    rows = (len(ids) + COLS - 1) // COLS
    step = CELL + PAD
    img = Image.new("RGB", (GUTTER + COLS * step, rows * step), (24, 24, 28))
    px = img.load()
    for n, mid in enumerate(ids):
        bx = GUTTER + (n % COLS) * step
        by = (n // COLS) * step
        ent = entries(mid)
        for layer in (0, 1):
            for quad in range(4):
                v = ent[layer * 4 + quad]
                data = tile(v & 0x03FF)
                xflip, yflip = (v >> 10) & 1, (v >> 11) & 1
                pal = pals[(v >> 12) & 0x0F]
                ox, oy = bx + (quad & 1) * 8, by + (quad >> 1) * 8
                for y in range(8):
                    sy = 7 - y if yflip else y
                    for x in range(8):
                        sx = 7 - x if xflip else x
                        c = data[sy * 8 + sx]
                        if layer and c == 0:
                            continue
                        px[ox + x, oy + y] = pal[c]
        if behavior(mid):
            # A non-zero behaviour is gameplay, not decoration: mark it.
            for x in range(3):
                for y in range(3):
                    px[bx + CELL - 1 - x, by + y] = (255, 80, 80)

    img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    draw = ImageDraw.Draw(img)
    for row in range(rows):
        draw.text((3, (row * step + 4) * scale), "%03X" % ids[row * COLS], fill=(210, 210, 210))
    img.save(out_path)
    return img.size, len(ids)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("primary")
    ap.add_argument("secondary")
    ap.add_argument("out")
    ap.add_argument("--range", nargs=2, default=["0", "0x400"])
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--root", default=ROOT)
    args = ap.parse_args()
    first, last = (int(v, 0) for v in args.range)
    size, count = sheet(args.root, args.primary, args.secondary, args.out, first, last, args.scale)
    print("%s + %s: %d blocks -> %s %dx%d" % (args.primary, args.secondary, count, args.out, *size))


if __name__ == "__main__":
    main()

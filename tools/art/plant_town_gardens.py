#!/usr/bin/env python3
"""Plant hand-placed flower beds on town grass.

The block value keeps its collision and elevation bits untouched; only the
metatile id changes, and only to a decorative ground tile the map already uses.
Nothing here can alter where the player may walk, so doors, ledges, NPC wander
ranges and scripted coordinates are unaffected by construction.

Every bed is written out coordinate by coordinate rather than scattered by a
random pass: a bed is a compact shape placed against a building front or as a
patch of meadow, which is what makes it read as landscaping instead of noise.
"""
from __future__ import annotations

import argparse
import json
import os
import struct

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GRASS = 0x001


def rect(x0, y0, x1, y1):
    return [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]


# city -> list of (metatile id, cells). Cells must currently hold plain grass.
GARDENS = {
    "LittlerootTown": [
        # Flower beds flanking the lab door, mirroring the ones already there.
        (0x004, rect(8, 17, 9, 18)),
        # A bed at the front of each house, on the side away from the doorstep.
        (0x004, [(2, 9), (3, 9)]),
        (0x004, [(16, 9), (17, 9)]),
        # Meadow patches breaking up the two empty fields.
        (0x201, rect(16, 11, 17, 12)),
        (0x201, rect(1, 12, 2, 13)),
        (0x201, rect(12, 17, 13, 18)),
    ],
}


def load_layout(layout_id):
    path = os.path.join(ROOT, "data/layouts/layouts.json")
    for entry in json.load(open(path, encoding="utf-8"))["layouts"]:
        if entry["id"] == layout_id:
            return entry
    raise SystemExit("unknown layout: %s" % layout_id)


def plant(city, beds, dry_run):
    map_path = os.path.join(ROOT, "data/maps/%s/map.json" % city)
    layout = load_layout(json.load(open(map_path, encoding="utf-8"))["layout"])
    w, h = int(layout["width"]), int(layout["height"])
    dest = os.path.join(ROOT, layout["blockdata_filepath"])
    blocks = list(struct.unpack("<%dH" % (w * h), open(dest, "rb").read()))

    planted = 0
    for metatile, cells in beds:
        for x, y in cells:
            if not (0 <= x < w and 0 <= y < h):
                raise SystemExit("%s: cell %d,%d is off the map" % (city, x, y))
            i = y * w + x
            if blocks[i] & 0x03FF != GRASS:
                raise SystemExit("%s: cell %d,%d is not plain grass (%03X)"
                                 % (city, x, y, blocks[i] & 0x03FF))
            blocks[i] = (blocks[i] & 0xFC00) | metatile
            planted += 1

    if not dry_run:
        open(dest, "wb").write(struct.pack("<%dH" % len(blocks), *blocks))
    return planted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    for city, beds in GARDENS.items():
        print("%-16s %d blocks planted" % (city, plant(city, beds, args.dry_run)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""What every block in a tileset pair is actually used for, harvested from maps.

A metatile sheet shows what a block looks like but not how it is meant to be
used. Reading every map that shares a tileset pair answers that: whether a
block is laid as walkable ground or as something solid, which blocks sit next
to it, and how common it is. That is the vocabulary a restyle has to speak, and
it is what stops a "nice looking" block being dropped where the game expects
ground.

    python3 tools/audit/tileset_vocabulary.py gTileset_General gTileset_Petalburg
    python3 tools/audit/tileset_vocabulary.py ... --ground   # walkable only
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import struct

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NUM_METATILES_IN_PRIMARY = 512
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


def harvest(root, primary, secondary):
    layouts = json.load(open(os.path.join(root, "data/layouts/layouts.json"), encoding="utf-8"))["layouts"]
    attrs = (attributes(root, primary), attributes(root, secondary))
    usage = collections.defaultdict(lambda: collections.Counter())
    maps = 0
    for layout in layouts:
        if layout.get("primary_tileset") != primary or layout.get("secondary_tileset") != secondary:
            continue
        path = os.path.join(root, layout.get("blockdata_filepath", ""))
        if not os.path.exists(path):
            continue
        maps += 1
        raw = open(path, "rb").read()
        for value in struct.unpack("<%dH" % (len(raw) // 2), raw):
            usage[value & 0x03FF][(value >> 10) & 0x03] += 1
    return usage, attrs, maps


def behavior(attrs, mid):
    table, i = (attrs[0], mid) if mid < NUM_METATILES_IN_PRIMARY else (attrs[1], mid - NUM_METATILES_IN_PRIMARY)
    return (table[i] & BEHAVIOR_MASK) if i < len(table) else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("primary")
    ap.add_argument("secondary")
    ap.add_argument("--ground", action="store_true", help="only blocks laid as walkable ground")
    ap.add_argument("--solid", action="store_true", help="only blocks laid as solid")
    ap.add_argument("--behavior", type=int, help="only blocks with this metatile behaviour")
    ap.add_argument("--root", default=ROOT)
    args = ap.parse_args()

    usage, attrs, maps = harvest(args.root, args.primary, args.secondary)
    print("%d map(s) use %s + %s" % (maps, args.primary, args.secondary))
    rows = []
    for mid, counts in usage.items():
        walk = counts[0]
        solid = sum(v for k, v in counts.items() if k)
        beh = behavior(attrs, mid)
        if args.ground and not walk:
            continue
        if args.solid and not solid:
            continue
        if args.behavior is not None and beh != args.behavior:
            continue
        rows.append((walk + solid, mid, walk, solid, beh))
    rows.sort(reverse=True)
    try:
        print("%-6s %8s %8s %10s" % ("block", "walkable", "solid", "behaviour"))
        for total, mid, walk, solid, beh in rows:
            print("%-6s %8d %8d %10d" % ("%03X" % mid, walk, solid, beh))
        print("%d block(s) listed" % len(rows))
    except BrokenPipeError:
        os.dup2(os.open(os.devnull, os.O_WRONLY), 1)


if __name__ == "__main__":
    main()

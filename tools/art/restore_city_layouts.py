#!/usr/bin/env python3
"""Put the settlements' block data back to a composition that actually reads.

An earlier pass gave every town a different look by shuffling its metatiles
inside collision groups. Collision survived, so the towns stayed walkable, but
the buildings did not: a house is eight specific blocks in eight specific
relative positions, and permuting them scatters roof and wall fragments across
the grass. This restores the authored composition for those maps.

Nothing outside the block grid is touched. Every warp, object event, coord
event and bg event in these maps already sits at its authored coordinate, which
is verified here before a single byte is written, so doors land under doorways
and NPCs stand on the ground they were placed on.
"""
from __future__ import annotations

import argparse
import json
import os
import struct
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CITIES = [
    "LittlerootTown", "OldaleTown", "PetalburgCity", "RustboroCity",
    "DewfordTown", "SlateportCity", "MauvilleCity", "VerdanturfTown",
    "FallarborTown", "LavaridgeTown", "FortreeCity", "LilycoveCity",
    "MossdeepCity", "SootopolisCity", "PacifidlogTown", "EverGrandeCity",
]

EVENT_KINDS = ("warp_events", "object_events", "coord_events", "bg_events")


def layouts(root):
    path = os.path.join(root, "data/layouts/layouts.json")
    return {x["id"]: x for x in json.load(open(path, encoding="utf-8"))["layouts"]}


def event_coords(map_data):
    out = {}
    for kind in EVENT_KINDS:
        out[kind] = [(e.get("x"), e.get("y")) for e in map_data.get(kind, [])]
    return out


def restore(city, source_root, dry_run):
    here = json.load(open(os.path.join(ROOT, "data/maps/%s/map.json" % city), encoding="utf-8"))
    there = json.load(open(os.path.join(source_root, "data/maps/%s/map.json" % city), encoding="utf-8"))

    if here["layout"] != there["layout"]:
        raise SystemExit("%s: layout id differs (%s vs %s)" % (city, here["layout"], there["layout"]))
    if event_coords(here) != event_coords(there):
        raise SystemExit("%s: an event has been moved; restoring the grid could strand it" % city)
    if here.get("connections") != there.get("connections"):
        raise SystemExit("%s: connections differ" % city)

    mine = layouts(ROOT)[here["layout"]]
    theirs = layouts(source_root)[there["layout"]]
    for key in ("width", "height", "primary_tileset", "secondary_tileset"):
        if mine[key] != theirs[key]:
            raise SystemExit("%s: layout %s differs (%s vs %s)" % (city, key, mine[key], theirs[key]))

    dest = os.path.join(ROOT, mine["blockdata_filepath"])
    src = os.path.join(source_root, theirs["blockdata_filepath"])
    old = open(dest, "rb").read()
    new = open(src, "rb").read()
    if len(old) != len(new):
        raise SystemExit("%s: block data size differs" % city)

    count = len(new) // 2
    a = struct.unpack("<%dH" % count, old)
    b = struct.unpack("<%dH" % count, new)
    changed = sum(1 for x, y in zip(a, b) if x != y)
    if changed and not dry_run:
        open(dest, "wb").write(new)
    return {"city": city, "changed": changed, "total": count}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="/home/user/pret/pokeemerald",
                    help="checkout holding the authored block data")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not os.path.isdir(args.source):
        raise SystemExit("source checkout not found: %s" % args.source)
    total = 0
    for city in CITIES:
        r = restore(city, args.source, args.dry_run)
        total += r["changed"]
        print("%-16s %4d/%d blocks restored" % (r["city"], r["changed"], r["total"]))
    print("%d blocks restored across %d settlements" % (total, len(CITIES)))


if __name__ == "__main__":
    main()

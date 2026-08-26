#!/usr/bin/env python3
"""Break up the tree line a town inherited, by planting into it.

Moving buildings is nearly exhausted: Emerald's towns are boxed in, and after
the destination guard only one settlement in ten has an offset left that does
not overwrite a neighbour. But a town's silhouette is not only its buildings.
It is also the shape of the green around them, and Emerald's is a ruler-straight
ring of identical trees with a lawn scraped flat inside it.

Vegetation is scenery, so this is the safest change left. A grove is stamped
from the town's own trees - the same 2x2 the border is built from, read out of
the map rather than named, so it is already wearing the biome's green - and
only onto ground the campaign never touches: not a warp, a trigger, a sign, a
person's wander box or a scripted walk, not the strip a route is drawn against,
and never against a doorway.

Adding something solid can only take walkable ground away, so every stamp is
applied, measured against the whole map, and put back unless everything that
was reachable still is.

    python3 tools/art/replant_towns.py --report
    python3 tools/art/replant_towns.py --all
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audit"))

from map_invariants import NUM_METATILES_IN_PRIMARY, TownMap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# How many groves a town gets, by how much room it has. Enough to break a
# straight edge, not enough to turn a village into a wood.
GROVES_PER_1000_CELLS = 9

# How many of a 2x2's twelve neighbours have to be open ground, somewhere on
# the map, for it to be something that grows there rather than something the
# land is made of.
RING_IN_THE_OPEN = 3


def biome_lawn(city):
    import forge_town_variants
    return forge_town_variants.town_lawn(city)


def foliage(town):
    """Every block in this town that the biome pass found greenery on.

    `forge_town_variants` repainted each block that drew Emerald's grass ramp
    into the biome's own green and recorded the slot it forged, so the manifest
    is a list of this town's leaves - in its own tileset, under its own ids,
    without a single block having to be named here.
    """
    path = os.path.join(ROOT, "data/tilesets/arauna_variants.json")
    if not os.path.exists(path):
        return set()
    manifest = json.load(open(path, encoding="utf-8"))["blocks"]
    secondary = town.layout["secondary_tileset"]
    return {NUM_METATILES_IN_PRIMARY + slot for key, slot in manifest.items()
            if key.split("|")[0] == secondary}


def tree_stamp(town):
    """The 2x2 of tree the town is already planted with, read off the map.

    Naming a block id would be wrong twice over: the id means different things
    in different tilesets, and after the biome pass a town's trees are variants
    with ids that were free slots. So the tree has to be recognised rather than
    named - and "the most repeated solid 2x2" is not enough to recognise it.
    In Sootopolis the most repeated solid 2x2 is the white crater wall, and
    planting it dropped chunks of cliff onto the lawn.

    Two things have to be true of it. It has to have leaves on it, which the
    biome pass already knows: it repainted every block that drew Emerald's
    grass ramp into this town's own green, and wrote down which ones (see
    `foliage`). And it has to stand in the open somewhere on the map, which is
    what tells a tree from a hedge grown along a wall.

    Neither test alone is enough. "The most repeated solid 2x2" on its own
    planted chunks of the white crater wall across Sootopolis' lawn; openness
    on its own promoted the grey stone slabs lying beside them.
    """
    counts, openest = collections.Counter(), collections.defaultdict(int)
    for y in range(town.h - 1):
        for x in range(town.w - 1):
            quad = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if any(town.walkable(*c) or town.behavior(*c) != 0 for c in quad):
                continue
            stamp = tuple(town.blocks[town.index(*c)] for c in quad)
            counts[stamp] += 1
            ring = [(x + dx, y + dy) for dx in (-1, 0, 1, 2) for dy in (-1, 0, 1, 2)
                    if (x + dx, y + dy) not in quad]
            openest[stamp] = max(openest[stamp],
                                 sum(1 for c in ring if town.inside(*c) and town.walkable(*c)))
    leaves = foliage(town)
    standing = [(seen, stamp) for stamp, seen in counts.items()
                if openest[stamp] >= RING_IN_THE_OPEN
                and all((b & 0x03FF) in leaves for b in stamp)]
    if not standing:
        return None
    seen, stamp = max(standing)
    return stamp if seen >= 4 else None


def plantable(town, lawn):
    """Ground a grove may stand on: open, plain, and nobody's business."""
    campaign = town.campaign_cells()
    seams = town.seams()
    warps = {(int(e["x"]), int(e["y"])) for e in town.events("warp_events")}
    doorsteps = {(x, y + dy) for x, y in warps for dy in range(1, 3)}
    out = set()
    for y in range(1, town.h - 1):
        for x in range(1, town.w - 1):
            cell = (x, y)
            if cell in campaign or cell in seams or cell in doorsteps:
                continue
            if not town.walkable(x, y) or town.metatile(x, y) != lawn:
                continue
            out.add(cell)
    return out


def replant(city, dry_run):
    town = TownMap(city, ROOT)
    lawn = biome_lawn(city)
    if lawn is None:
        return None
    stamp = tree_stamp(town)
    if stamp is None:
        return {"city": city, "groves": 0, "why": "no tree it tiles its own border with"}

    open_ground = plantable(town, lawn)
    before = town.reachable(allow_water=False)
    budget = max(2, round(town.w * town.h * GROVES_PER_1000_CELLS / 1000))

    # Deterministic, and biased to the edges: a grove against the border breaks
    # the straight line, while one in the middle of a square just gets in the
    # way.
    def edginess(cell):
        x, y = cell
        return min(x, y, town.w - 1 - x, town.h - 1 - y)

    order = sorted(open_ground, key=lambda c: (edginess(c), c))
    # Keep the edge-first bias for the first third and shuffle the rest, so a
    # town gets a broken border and a few groves inland rather than a neat band.
    tail = order[len(order) // 3:]
    random.Random(sum(ord(ch) for ch in city)).shuffle(tail)
    order = order[:len(order) // 3] + tail

    planted, used = 0, set()
    for x, y in order:
        if planted >= budget:
            break
        quad = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
        if any(c not in open_ground or c in used for c in quad):
            continue
        keep = [town.blocks[town.index(*c)] for c in quad]
        for c, value in zip(quad, stamp):
            town.blocks[town.index(*c)] = value
        # Ground already taken by an earlier grove is not ground this one lost:
        # without subtracting it, every grove after the first is refused for the
        # cells the first one is standing on.
        if before - town.reachable(allow_water=False) - set(quad) - used:
            for c, value in zip(quad, keep):
                town.blocks[town.index(*c)] = value
            continue
        used.update(quad)
        planted += 1

    if planted and not dry_run:
        open(town.path, "wb").write(struct.pack("<%dH" % len(town.blocks), *town.blocks))
    return {"city": city, "groves": planted, "budget": budget, "room": len(open_ground)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("city", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    import retheme_cities
    cities = [c for c in retheme_cities.THEMES if retheme_cities.THEMES[c].get("biome")] \
        if (args.all or args.report) else [args.city]
    total = 0
    for city in cities:
        r = replant(city, args.report)
        if not r:
            continue
        total += r["groves"]
        print("%-16s %3d grove(s)%s" % (city, r["groves"],
              "" if "why" in r else " of a %d budget, %d blocks of open ground"
              % (r["budget"], r["room"])))
    print("%d grove(s) planted" % total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

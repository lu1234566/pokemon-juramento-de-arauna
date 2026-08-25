#!/usr/bin/env python3
"""Give each settlement of Arauna its own look, in Emerald's own blocks.

The campaign is not negotiable, so nothing here moves a wall, a door, a person
or a trigger: every block this tool writes keeps the collision, elevation and
metatile behaviour it already had, and only its appearance changes. What that
still allows is most of what a town looks like - what the ground is made of,
where the streets run, where the squares and gardens are.

Streets are not drawn by hand. Each town's own walkable graph is walked from
every door and every route exit to a hub, and the union of those shortest paths
is the street plan, because a settlement's paths are already implied by where
its buildings stand and where its roads leave. The material is then laid with
an autotile table learned from the Emerald corpus, so the edges and corners are
the ones the artists drew.

    python3 tools/art/retheme_cities.py --list
    python3 tools/art/retheme_cities.py LittlerootTown
    python3 tools/art/retheme_cities.py --all
"""
from __future__ import annotations

import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audit"))

import forge_arauna_tiles as forge  # noqa: E402
import paint_town  # noqa: E402
from map_invariants import TownMap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Materials, as the set of blocks that make one surface. The autotile table for
# each is learned from every Emerald map that lays it.
SAND = {0x118, 0x119, 0x11A, 0x120, 0x121, 0x122, 0x128, 0x129, 0x12A}
GRASS = {0x001, 0x002}

# What counts as bare, paintable floor in a town: the blocks a street may be
# laid over. Anything else the map put down - a doorstep, a flowerbed, a ledge,
# a patch of tall grass - is left where it is.
# Only blocks below 0x200 belong here: those come from the primary tileset and
# mean the same thing in every outdoor map. A block at or above 0x200 is an
# index into whichever secondary tileset the map loads, so the same number is a
# flowerbed in one town and a ledge in the next; those go in a theme's own
# "extra_ground", next to the tileset they were read from.
GRASS_GROUND = SAND | {0x001, 0x002, 0x004,
                       # The speckled field variants Emerald lays to keep a
                       # lawn from looking flat - plain ground, not a shadow.
                       0x1D0, 0x1D1, 0x1D2, 0x1D8, 0x1D9, 0x1DA,
                       0x1E0, 0x1E1, 0x1E2}

# gTileset_Petalburg: its yellow flower patch and its two sand blocks are bare
# ground, and a street runs straight over them.
PETALBURG_GROUND = {0x201, 0x252, 0x253}

# Emerald's lawn, in every block it is laid as. The plain ones all become a
# biome's plain lawn; the two that carry a tree's shadow become that biome's
# own shadowed pair, so a tree line does not sit on a strip of the old green.
LAWN_PLAIN = {0x001, 0x002, 0x1D0, 0x1D1, 0x1D2, 0x1D8, 0x1D9, 0x1DA,
              0x1E0, 0x1E1, 0x1E2}
LAWN_SHADOWED = (0x1CE, 0x1CF)

# Emerald's flowerbed is half lawn by pixel count - the petals are drawn on a
# tile that carries the old green with them - and recolouring it would cost
# four more tiles per biome, which the primary tileset does not have. Against a
# dark or a yellow lawn each bed would read as a pale hole, so in those biomes
# the beds go back to being grass. The pale biome is close enough to the green
# the petals were drawn against that they still sit right.
FLOWERBED = 0x004
FOLD_FLOWERBEDS_IN = {"MATA", "CERRADO"}

# Arauna's settlements are joined by packed earth, not by Hoenn's paving. The
# street plan is drawn from each town's own doors and exits; a paved city gets
# green squares cut into it instead, because it has streets already.
THEMES = {
    # Its pale meadow patches were planted against Emerald's mint; against the
    # forest green they read as holes, so they go back to being lawn.
    "LittlerootTown": {"mode": "street", "biome": "MATA", "lawn_extra": {0x201},
                       "material": SAND, "forged": "TERRA",
                       "ground": GRASS_GROUND | PETALBURG_GROUND,
                       "plaza": 1, "verge": 0x004, "verge_step": 2},
    "OldaleTown": {"mode": "street", "biome": "CERRADO", "material": SAND, "forged": "TERRA",
                       "ground": GRASS_GROUND | PETALBURG_GROUND,
                   "plaza": 1, "lanes": 1, "verge": 0x004, "verge_step": 3},
    "PetalburgCity": {"mode": "street", "biome": "PAMPA", "material": SAND, "forged": "TERRA",
                       "ground": GRASS_GROUND | PETALBURG_GROUND,
                      "plaza": 2, "verge": 0x004, "verge_step": 3},
    "VerdanturfTown": {"mode": "street", "biome": "MATA", "material": SAND, "forged": "TERRA", "ground": GRASS_GROUND,
                       "plaza": 1, "verge": 0x004, "verge_step": 3},
    "LavaridgeTown": {"mode": "street", "biome": "CERRADO", "material": SAND, "forged": "TERRA", "ground": GRASS_GROUND,
                      "plaza": 1, "verge": 0x004, "verge_step": 4},
    "MossdeepCity": {"mode": "street", "biome": "PAMPA", "material": SAND, "forged": "TERRA", "ground": GRASS_GROUND,
                     "plaza": 2, "verge": 0x004, "verge_step": 4},
    "LilycoveCity": {"mode": "street", "biome": "MATA", "material": SAND, "forged": "TERRA", "ground": GRASS_GROUND,
                     "plaza": 2, "verge": 0x004, "verge_step": 4},

    # Already-paved cities: cut squares of green into the stone instead.
    "RustboroCity": {"mode": "park", "biome": "PAMPA", "material": GRASS, "ground": {0x2BB, 0x2C3, 0x309},
                     "squares": 4, "size": 4, "verge": 0x004, "verge_step": 2},
    "SlateportCity": {"mode": "park", "biome": "CERRADO", "material": GRASS,
                      "ground": {0x202, 0x209, 0x210, 0x211, 0x212, 0x219},
                      "squares": 5, "size": 3, "verge": 0x004, "verge_step": 2},
    "MauvilleCity": {"mode": "street", "biome": "CERRADO", "material": SAND, "forged": "TERRA", "ground": GRASS_GROUND,
                     "plaza": 2, "verge": 0x004, "verge_step": 3},
    # These carry an identity of their own already - timber, cliff, ash - so
    # they take the biome's green and nothing else.
    "FortreeCity": {"mode": "lawn", "biome": "MATA", "material": GRASS,
                    "ground": set()},
    "EverGrandeCity": {"mode": "lawn", "biome": "PAMPA", "material": GRASS,
                       "ground": set()},

    "SootopolisCity": {"mode": "park", "biome": "MATA", "material": GRASS, "ground": {0x2D9, 0x244, 0x245},
                       "squares": 5, "size": 2, "verge": 0x004, "verge_step": 2},
}


def biome_lawn(town, biome, keep, extra=()):
    """Relay a town's whole lawn in its biome's green.

    Every block here is plain walkable ground with no behaviour of its own, and
    the forged lawn is the same two tiles of grass pointing at a different ramp
    of the same palette, so this changes the colour of a town and nothing else.
    """
    blocks = forge.MATERIALS[biome]["metatiles"]
    plain, shadow_left, shadow_right = blocks
    swap = {mid: plain for mid in set(LAWN_PLAIN) | set(extra)}
    if biome in FOLD_FLOWERBEDS_IN:
        swap[FLOWERBED] = plain
    swap[LAWN_SHADOWED[0]] = shadow_left
    swap[LAWN_SHADOWED[1]] = shadow_right

    out = {}
    for y in range(town.h):
        for x in range(town.w):
            if (x, y) in keep:
                continue
            block = swap.get(town.metatile(x, y))
            if block is None or town.behavior_of(block) != town.behavior(x, y):
                continue
            out[(x, y)] = (town.blocks[town.index(x, y)] & 0xFC00) | block
    return out


def biome_border(town, biome):
    """The frame drawn beyond the map's edge wears the biome too."""
    path = os.path.join(ROOT, town.layout["border_filepath"])
    raw = open(path, "rb").read()
    values = list(struct.unpack("<%dH" % (len(raw) // 2), raw))
    plain = forge.MATERIALS[biome]["metatiles"][0]
    changed = 0
    for i, value in enumerate(values):
        if (value & 0x03FF) in LAWN_PLAIN:
            values[i] = (value & 0xFC00) | plain
            changed += 1
    if changed:
        open(path, "wb").write(struct.pack("<%dH" % len(values), *values))
    return changed


def anchors(town):
    """Where a street has to reach: every doorstep and every way out of town."""
    out = []
    for e in town.events("warp_events"):
        x, y = int(e["x"]), int(e["y"])
        step = (x, y + 1)
        out.append(step if town.inside(*step) and town.walkable(*step) else (x, y))
    for c in town.map.get("connections") or []:
        d = c.get("direction")
        if d == "up":
            edge = [(x, 0) for x in range(town.w)]
        elif d == "down":
            edge = [(x, town.h - 1) for x in range(town.w)]
        elif d == "left":
            edge = [(0, y) for y in range(town.h)]
        elif d == "right":
            edge = [(town.w - 1, y) for y in range(town.h)]
        else:
            continue
        out.extend(cell for cell in edge if town.walkable(*cell))
    return out


def open_squares(town, count, size, ground):
    """The roomiest patches of bare floor the campaign never walks on."""
    campaign = town.campaign_cells()

    def free(x, y):
        return (town.inside(x, y) and town.walkable(x, y) and (x, y) not in campaign
                and town.metatile(x, y) in ground)

    chosen, taken = [], set()
    for y in range(town.h - size + 1):
        for x in range(town.w - size + 1):
            if len(chosen) >= count:
                break
            cells = [(x + dx, y + dy) for dy in range(size) for dx in range(size)]
            if not all(free(*c) for c in cells):
                continue
            if any(abs(x - cx) < size * 2 and abs(y - cy) < size * 2 for cx, cy in chosen):
                continue
            chosen.append((x, y))
            taken.update(cells)
    return taken


def retheme(city, theme, dry_run=False):
    town = TownMap(city, ROOT)
    table = paint_town.learn_family(theme["material"], primary=town.layout["primary_tileset"])

    if theme["mode"] == "lawn":
        region, hub = set(), (0, 0)
    elif theme["mode"] == "park":
        region = open_squares(town, theme.get("squares", 3), theme.get("size", 4), theme["ground"])
        hub = min(region) if region else (0, 0)
    else:
        spots = anchors(town)
        road = paint_town.avenues(town, spots, lanes=theme.get("lanes", 2))
        # A square where the streets meet, so the town has a centre. It is a
        # rectangle rather than a grown blob, and it keeps clear of the buildings.
        hub = paint_town._hub(town, spots, lambda x, y: town.walkable(x, y))
        r = theme.get("plaza", 0)
        square = {(x, y)
                  for y in range(hub[1] - r, hub[1] + r + 1)
                  for x in range(hub[0] - r, hub[0] + r + 1)
                  if town.inside(x, y) and town.walkable(x, y)
                  and not paint_town._touches_solid(town, (x, y))}
        region = road | square
    # The strip a neighbouring route is drawn against stays exactly as it is,
    # so a street ends in its own rounded cap a couple of blocks inside the
    # town and the join with the route is untouched.
    region -= town.seams()

    keep = set(town.seams())
    keep |= {(int(e["x"]), int(e["y"])) for e in town.events("warp_events")}
    keep |= {(int(e["x"]), int(e["y"])) for e in town.events("bg_events")}

    changed = paint_town.paint(town, region, table, theme["ground"], keep=keep)
    paved = len(changed)
    planted = _verges(town, region, theme, keep, changed)
    changed.update(planted)
    forged = _forge_material(town, theme, keep, changed)
    changed.update(forged)
    greened = 0
    if theme.get("biome"):
        # The lawn is relaid last so it also catches the ground the street plan
        # left alone, and it reaches the route seam: a settlement's biome should
        # stop at the settlement's edge, the way Emerald stops its own ash.
        for cell, value in biome_lawn(town, theme["biome"], keep - town.seams(),
                                      theme.get("lawn_extra", ())).items():
            changed[cell] = value
            greened += 1
    if not dry_run:
        paint_town.commit(town, changed)
        if theme.get("biome"):
            biome_border(town, theme["biome"])
    return {"city": city, "paved": paved,
            "planted": len(planted), "greened": greened,
            "region": len(region), "hub": hub}


def _forge_material(town, theme, keep, changed):
    """Swap a whole material for its forged counterpart, town-wide.

    Doing this only along the new streets would leave a town wearing two
    materials at once - the paths Emerald already laid in sand beside the ones
    laid here in earth. The swap is block for block, so collision, elevation
    and behaviour are carried straight over.
    """
    name = theme.get("forged")
    if not name:
        return {}
    swap = forge.substitution(name)
    out = {}
    for y in range(town.h):
        for x in range(town.w):
            if (x, y) in keep:
                continue
            value = changed.get((x, y), town.blocks[town.index(x, y)])
            block = swap.get(value & 0x03FF)
            if block is not None:
                out[(x, y)] = (value & 0xFC00) | block
    return out


def _verges(town, region, theme, keep, paved):
    """Plant the strip along a street, at a regular spacing so it reads as a verge."""
    block = theme.get("verge")
    if not block or (block == FLOWERBED and theme.get("biome") in FOLD_FLOWERBEDS_IN):
        return {}
    step = theme.get("verge_step", 3)
    out = {}
    if theme["mode"] == "lawn":
        region, hub = set(), (0, 0)
    elif theme["mode"] == "park":
        # A green square is planted inside itself, not along its edge.
        for x, y in sorted(region):
            if (x, y) in keep or (x + y) % step:
                continue
            old = paved.get((x, y), town.blocks[town.index(x, y)])
            out[(x, y)] = (old & 0xFC00) | block
        return out
    for x, y in sorted(region):
        for dx, dy in paint_town.NEIGHBOURS:
            nx, ny = x + dx, y + dy
            cell = (nx, ny)
            if not town.inside(nx, ny) or cell in region or cell in keep or cell in out:
                continue
            if town.metatile(nx, ny) not in (0x001, 0x002):
                continue
            if paint_town._touches_solid(town, cell):
                continue
            if (nx + ny) % step:
                continue
            old = paved.get(cell, town.blocks[town.index(nx, ny)])
            out[cell] = (old & 0xFC00) | block
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("city", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.list:
        for city in THEMES:
            print(city)
        return 0
    cities = list(THEMES) if args.all else [args.city]
    for city in cities:
        if city not in THEMES:
            raise SystemExit("no theme for %s" % city)
        r = retheme(city, THEMES[city], args.dry_run)
        print("%-16s %4d street, %3d planted, %4d lawn relaid in %s"
              % (r["city"], r["paved"], r["planted"], r["greened"],
                 THEMES[r["city"]].get("biome") or "-"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

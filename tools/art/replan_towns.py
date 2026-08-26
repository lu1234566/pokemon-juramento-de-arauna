#!/usr/bin/env python3
"""Redraw a town's plan by hand, moving what the campaign is tied to with it.

The automatic nudge in `move_buildings.py` refuses anything a script's step
count is tied to, which in a starting town is nearly everything. That refusal
is right for a tool that cannot read intent; it is not a law of the map. A
cutscene's step count survives a building moving as long as *everything the
count is measured against* moves the same way - the door, the person who walks
out of it, the truck they walk to, and the coordinates the script names in
plain numbers.

So a plan here is not just an offset. It is a group: the blocks, the events
standing in them, the extra cells that belong to the building without touching
it (its sign), and the literal coordinates in the scripts - including scripts
in *other* maps, because the player's arrival in this town is written inside
the truck they arrive in.

Everything is stated rather than inferred, so a plan can be read and argued
with. What is inferred is only whether it worked: after the move the map is
re-checked for reachability, for warps that still open doors, and for scripted
walks that still land on ground.

    python3 tools/art/replan_towns.py --report
    python3 tools/art/replan_towns.py LittlerootTown
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audit"))

import forge_arauna_tiles as forge  # noqa: E402
from map_invariants import TownMap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EVENT_KINDS = ("warp_events", "object_events", "bg_events", "coord_events")


PLANS = {
    # VILA AMANHECER. Emerald's plan is two houses facing each other across a
    # crossroads with the laboratory square in the bottom-left corner - the
    # most recognisable silhouette in the game. Pull the player's house up
    # against the northern forest and push the laboratory into the middle of
    # the village, and the mirror is gone.
    "LittlerootTown": {
        "groups": [
            {
                "what": "the player's house",
                "rect": (2, 4, 6, 8),
                "extra": [(7, 8)],            # its sign, which stands outside the wall
                "by": (0, -2),
                "also_move": [(2, 10)],       # the moving truck it arrives beside
                "literals": [
                    # The door coordinate the intro hands to `opendoor`.
                    ("data/maps/LittlerootTown/scripts.inc",
                     "\tsetvar VAR_0x8004, 5\n\tsetvar VAR_0x8005, 8\n",
                     "\tsetvar VAR_0x8004, 5\n\tsetvar VAR_0x8005, 6\n"),
                    ("data/maps/LittlerootTown/scripts.inc",
                     "setobjectxyperm LOCALID_LITTLEROOT_MOM, 5, 9",
                     "setobjectxyperm LOCALID_LITTLEROOT_MOM, 5, 7"),
                    ("data/maps/LittlerootTown/scripts.inc",
                     "setobjectxy LOCALID_LITTLEROOT_RIVAL, 6, 10",
                     "setobjectxy LOCALID_LITTLEROOT_RIVAL, 6, 8"),
                    ("data/maps/LittlerootTown/scripts.inc",
                     "setobjectxy LOCALID_LITTLEROOT_BIRCH, 5, 10",
                     "setobjectxy LOCALID_LITTLEROOT_BIRCH, 5, 8"),
                    # Where the player is put down when they climb out. This
                    # one lives in the truck's own map.
                    ("data/maps/InsideOfTruck/scripts.inc",
                     "setdynamicwarp MAP_LITTLEROOT_TOWN, 3, 10",
                     "setdynamicwarp MAP_LITTLEROOT_TOWN, 3, 8"),
                ],
            },
            {
                "what": "the laboratory",
                "rect": (3, 12, 9, 16),
                "extra": [(6, 17)],           # its sign
                "by": (3, 0),
                "also_move": [],
                "literals": [],
            },
        ],
        # People who only wander, standing where a building is going.
        "relocate": [((12, 13), (4, 13))],
    },

    # VALE DO SILENCIO is not here on purpose: it paves its ground from the
    # same secondary tileset it builds with, so a footprint cannot be told
    # apart from the floor around it. It keeps the automatic nudge instead.

    # VILA DA PASSAGEM. Emerald's Oldale is a tidy T: a house on the upper
    # left, the mart on the upper right, the centre below it. Drop the house
    # down into the crossroads it is named for and pull the south-east block
    # up off the map's edge, and the T breaks.
    "OldaleTown": {
        "groups": [
            {
                "what": "the house on the rise",
                # The roof's top row is walkable and sits a row above the
                # walls, so the footprint has to reach up to y4 to be a house.
                "rect": (4, 4, 9, 7),
                "extra": [],
                "by": (0, 2),
                "also_move": [],
                "literals": [],
            },
            {
                "what": "the south-east block",
                "rect": (14, 12, 19, 19),
                "extra": [],
                "by": (0, -1),
                "also_move": [],
                "literals": [],
            },
        ],
        "relocate": [],
    },
}

# VALE DO SILENCIO is deliberately absent: it paves its ground from the same
# secondary tileset it builds with, so a footprint cannot be told apart from
# the floor around it. It keeps the automatic nudge instead.


def biome_lawn(city):
    import retheme_cities
    biome = (retheme_cities.THEMES.get(city) or {}).get("biome")
    return forge.MATERIALS[biome]["metatiles"][0]


def ground_physics(town):
    """The collision and elevation bits of this town's ordinary walkable ground.

    Writing a constant here is how a whole footprint of grass ended up solid:
    the collision bits live at 10 and 11, so 0x0C00 is collision 3 - a wall
    that happens to be drawn as a lawn. Read the map instead.
    """
    counts = collections.Counter(town.blocks[town.index(x, y)] & 0xFC00
                                 for y in range(town.h) for x in range(town.w)
                                 if town.walkable(x, y))
    return counts.most_common(1)[0][0]


def group_cells(group):
    x0, y0, x1, y1 = group["rect"]
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)} | set(group["extra"])


LEDGER = os.path.join(ROOT, "data/maps/arauna_replans.json")


def load_ledger():
    return json.load(open(LEDGER, encoding="utf-8")) if os.path.exists(LEDGER) else {}


def save_ledger(ledger):
    with open(LEDGER, "w", encoding="utf-8") as handle:
        json.dump(ledger, handle, indent=1, sort_keys=True)
        handle.write("\n")


NUM_METATILES_IN_PRIMARY = 512


def cuts_a_building(town, group):
    """Does this footprint slice through a building instead of containing it?

    Emerald draws the top row of a roof on a *walkable* block, so the player
    can pass behind it. A footprint taken from the solid blocks alone therefore
    stops one row short of the building it is supposed to be, and moving it
    leaves a strip of roof floating where the house used to be - which is
    exactly what happened to the house in Vila da Passagem.

    Solid or not, a building is drawn from the town's own secondary tileset
    while the ground around it comes from the shared primary one. So if a block
    of the secondary tileset inside the footprint touches another one outside
    it, the footprint has cut a building in half.
    """
    cells = group_cells(group)
    for x, y in cells:
        if town.metatile(x, y) < NUM_METATILES_IN_PRIMARY:
            continue
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            n = (x + dx, y + dy)
            if n in cells or not town.inside(*n):
                continue
            if town.metatile(*n) >= NUM_METATILES_IN_PRIMARY:
                return "%d,%d is part of the same building and is outside the footprint" % n
    return None


def already_applied(ledger, city, group):
    """Has this group been moved already?

    A plan is a statement about the map, not a diff, so running it twice must
    not move a building twice. Reading that off the map does not work when a
    move overlaps where it started - the doorway is inside both the old
    footprint and the new one - so it is written down instead.
    """
    return group["what"] in (ledger.get(city) or [])


def move_events(town, cells, offset, also):
    dx, dy = offset
    moved = 0
    for kind in EVENT_KINDS:
        for e in town.map.get(kind) or []:
            if "x" not in e:
                continue
            here = (int(e["x"]), int(e["y"]))
            if here in cells or here in also:
                e["x"] = here[0] + dx
                e["y"] = here[1] + dy
                moved += 1
    return moved


def apply_group(town, group, lawn, physics):
    cells = group_cells(group)
    dx, dy = group["by"]
    payload = {c: town.blocks[town.index(*c)] for c in cells}
    for c in cells:
        town.blocks[town.index(*c)] = physics | lawn
    for (x, y), value in payload.items():
        if not town.inside(x + dx, y + dy):
            raise SystemExit("%s: %s would leave the map" % (town.city, group["what"]))
        town.blocks[town.index(x + dx, y + dy)] = value
    for c in cells:
        if not town.walkable(*c) and c not in {(x + dx, y + dy) for x, y in cells}:
            raise SystemExit("%s: %s left ground you cannot walk on at %d,%d"
                             % (town.city, group["what"], *c))
    return move_events(town, cells, group["by"], set(map(tuple, group["also_move"])))


def rewrite_literals(group, dry_run):
    done = []
    for rel, old, new in group["literals"]:
        path = os.path.join(ROOT, rel)
        text = open(path, encoding="utf-8").read()
        if text.count(old) != 1:
            raise SystemExit("%s: expected exactly one %r, found %d"
                             % (rel, old[:48], text.count(old)))
        if not dry_run:
            open(path, "w", encoding="utf-8").write(text.replace(old, new))
        done.append(rel)
    return done


def check(town, before_reach, before_walks, doors):
    problems = []
    lost = before_reach - town.reachable(allow_water=False)
    stranded = [c for c in lost if town.walkable(*c)]
    if stranded:
        problems.append("%d tile(s) walled off, e.g. %s"
                        % (len(stranded), " ".join("%d,%d" % c for c in sorted(stranded)[:4])))
    for kind in EVENT_KINDS:
        for e in town.map.get(kind) or []:
            if "x" in e and (int(e["x"]), int(e["y"])) in lost and not town.walkable(int(e["x"]), int(e["y"])):
                continue
            if "x" in e and (int(e["x"]), int(e["y"])) in lost:
                problems.append("%s at %s,%s cut off" % (kind[:-7], e["x"], e["y"]))
    for e in town.events("warp_events"):
        x, y = int(e["x"]), int(e["y"])
        if town.behavior(x, y) not in doors:
            problems.append("warp at %d,%d no longer sits on a door (behaviour %d)"
                            % (x, y, town.behavior(x, y)))
        if not town.inside(x, y + 1) or not town.walkable(x, y + 1):
            problems.append("the doorstep below the warp at %d,%d is blocked" % (x, y))
    bad = [c for c in town.scripted_paths(include_player=False, include_repositioned=False)
           if town.inside(*c) and not town.walkable(*c) and not town.surfable(*c)]
    if set(bad) - before_walks:
        problems.append("%d scripted step(s) would walk into a wall" % len(set(bad) - before_walks))
    return problems


def replan(city, dry_run):
    plan = PLANS[city]
    town = TownMap(city, ROOT)
    lawn = biome_lawn(city)
    physics = ground_physics(town)
    before_reach = town.reachable(allow_water=False)
    before_walks = {c for c in town.scripted_paths(include_player=False, include_repositioned=False)
                    if town.inside(*c) and not town.walkable(*c)}
    doors = {town.behavior(int(e["x"]), int(e["y"])) for e in town.events("warp_events")}

    ledger = load_ledger()
    moved_events, skipped, done = 0, 0, []
    for group in plan["groups"]:
        if already_applied(ledger, city, group):
            skipped += 1
            continue
        cut = cuts_a_building(town, group)
        if cut:
            raise SystemExit("%s: %s - %s" % (city, group["what"], cut))
        done.append(group["what"])
        moved_events += apply_group(town, group, lawn, physics)
    for old, new in plan.get("relocate", []):
        for e in town.map.get("object_events") or []:
            if (int(e["x"]), int(e["y"])) == tuple(old):
                e["x"], e["y"] = new

    problems = check(town, before_reach, before_walks, doors)
    if problems:
        raise SystemExit("%s: %s" % (city, "; ".join(problems[:5])))

    files = []
    for group in plan["groups"]:
        if group["what"] in done:
            files += rewrite_literals(group, dry_run)
    if not dry_run and done:
        ledger.setdefault(city, [])
        ledger[city] = sorted(set(ledger[city]) | set(done))
        save_ledger(ledger)
    if not dry_run:
        open(town.path, "wb").write(struct.pack("<%dH" % len(town.blocks), *town.blocks))
        path = os.path.join(ROOT, "data/maps/%s/map.json" % city)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(town.map, handle, indent=2)
            handle.write("\n")
    return {"city": city, "groups": len(plan["groups"]) - skipped, "skipped": skipped,
            "events": moved_events, "scripts": sorted(set(files))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("city", nargs="?")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    for city in ([args.city] if args.city else list(PLANS)):
        r = replan(city, args.report)
        print("%-16s %d group(s) moved (%d already in place), %d event(s) carried, scripts: %s"
              % (r["city"], r["groups"], r["skipped"], r["events"],
                 ", ".join(r["scripts"]) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

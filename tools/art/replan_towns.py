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
}


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

    moved_events = 0
    for group in plan["groups"]:
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
        files += rewrite_literals(group, dry_run)
    if not dry_run:
        open(town.path, "wb").write(struct.pack("<%dH" % len(town.blocks), *town.blocks))
        path = os.path.join(ROOT, "data/maps/%s/map.json" % city)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(town.map, handle, indent=2)
            handle.write("\n")
    return {"city": city, "groups": len(plan["groups"]), "events": moved_events,
            "scripts": sorted(set(files))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("city", nargs="?")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    for city in ([args.city] if args.city else list(PLANS)):
        r = replan(city, args.report)
        print("%-16s %d group(s) moved, %d event(s) carried, scripts: %s"
              % (r["city"], r["groups"], r["events"], ", ".join(r["scripts"]) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

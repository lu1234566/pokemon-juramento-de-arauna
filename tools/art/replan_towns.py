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
import move_buildings  # noqa: E402
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
                # Named by its doorway, not by a rectangle. The rectangle used
                # to run two columns wider than the house, and those two empty
                # columns are what put the man who blocks the road to Route 103
                # inside a wall when the house came down on him.
                "door": (5, 7),
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

# ENCRUZILHADA had a plan here and it is gone, because it was wrong. It moved
# "the block along the north side" four columns west, and what came back was a
# Pokemon Center with a dirt street running over its roof. The detector had
# read the town's re-greened trees as architecture and the Center - which the
# shared primary tileset draws, not the town's own - as landscape, so one flood
# swallowed the whole north side and then dropped it on top of the Center. The
# rule that told buildings from scenery is rewritten (see
# `move_buildings.built_metatiles`), and under it the same offset is refused:
# a neighbour is standing at 30,4. Mauville keeps the automatic nudge instead.

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


def group_cells(town, group):
    """The blocks a group is made of.

    A group may name a rectangle, or - better - just its doorway, and let the
    same detector the automatic mover uses grow the building from there. Typing
    a rectangle by hand is how a roof got left behind twice; a doorway cannot
    be mistyped into half a house.
    """
    if "door" in group:
        door = tuple(group["door"])
        for shape in move_buildings.buildings(town):
            if door in shape:
                return set(shape) | set(group.get("extra", ()))
        raise SystemExit("%s: no building found at the doorway %d,%d" % (town.city, *door))
    x0, y0, x1, y1 = group["rect"]
    return {(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)} | set(group.get("extra", ()))


LEDGER = os.path.join(ROOT, "data/maps/arauna_replans.json")


def load_ledger():
    return json.load(open(LEDGER, encoding="utf-8")) if os.path.exists(LEDGER) else {}


def save_ledger(ledger):
    with open(LEDGER, "w", encoding="utf-8") as handle:
        json.dump(ledger, handle, indent=1, sort_keys=True)
        handle.write("\n")


def cuts_a_building(town, group):
    """Does this footprint slice through a building instead of containing it?

    Emerald draws the top row of a roof on a *walkable* block, so the player
    can pass behind it. A footprint taken from the solid blocks alone therefore
    stops one row short of the building it is supposed to be, and moving it
    leaves a strip of roof floating where the house used to be - which is
    exactly what happened to the house in Vila da Passagem.

    So if a block this map built with, inside the footprint, touches another
    one outside it, the footprint has cut a building in half.
    """
    cells = group_cells(town, group)
    rare = move_buildings.built_metatiles(town)
    for cell in cells:
        if not move_buildings.is_built(town, cell, rare):
            continue
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            n = (cell[0] + dx, cell[1] + dy)
            if n in cells or not move_buildings.is_built(town, n, rare):
                continue
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


def destination_is_clear(town, group, exempt=()):
    """Nothing of consequence is standing where the group is going.

    Without this the paste is blind: a neighbouring building, a sign, a person
    would simply be overwritten, and the checks that run afterwards - which ask
    about reachability and doors - would not necessarily notice. Scenery is
    fair game and gets built over; anything this map built with is another
    building, and anything with an event on it belongs to someone - unless the
    plan itself says where that someone is going, which is what `relocate` is.
    """
    cells = group_cells(town, group)
    dx, dy = group["by"]
    rare = move_buildings.built_metatiles(town)
    events = {(int(e["x"]), int(e["y"])) for kind in EVENT_KINDS
              for e in town.map.get(kind) or [] if "x" in e} - set(exempt)
    for x, y in cells:
        target = (x + dx, y + dy)
        if target in cells:
            continue
        if not town.inside(*target):
            return "it would leave the map"
        if target in events and not lands_softly(town, (x, y), target):
            return "an event stands at %d,%d" % target
        if move_buildings.is_built(town, target, rare):
            return "another building stands at %d,%d" % target
    return None


def lands_softly(town, source, target):
    """Would the block moving from `source` bury whoever stands on `target`?

    A person standing where a wall is going has to be dealt with by the plan.
    A person standing where a patch of the same plain lawn is going has not:
    the ground under their feet is being replaced by ground that walks the
    same way and reads the same way, and they never notice.
    """
    if not town.walkable(*source):
        return False
    return town.behavior(*source) == town.behavior(*target)


def apply_group(town, group, lawn, physics):
    cells = group_cells(town, group)
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
    return move_events(town, cells, group["by"], set(map(tuple, group.get("also_move", ()))))


def rewrite_literals(group, dry_run):
    done = []
    for rel, old, new in group.get("literals", ()):
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
        exempt = {tuple(old) for old, _ in plan.get("relocate", [])}
        for why in (cuts_a_building(town, group), destination_is_clear(town, group, exempt)):
            if why:
                raise SystemExit("%s: %s - %s" % (city, group["what"], why))
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

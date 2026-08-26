#!/usr/bin/env python3
"""Move a town's buildings off Emerald's plan, without moving the campaign.

Repainting a town changes what it is made of. Where its buildings stand is
still Hoenn's decision, and a player who knows Emerald recognises the silhouette
before they read a single tile.

A building can be moved. What makes it safe is moving it as one rigid piece -
its walls, its doorway, the sign beside it and anyone standing in it, all
translated by the same offset - so every relationship inside the group survives
even though its coordinates change. What makes it *checkable* is refusing the
move whenever something outside the group depends on where the group is:

  * a trigger inside the footprint, because a coord event fires on a coordinate
    and nothing tells us what that coordinate meant;
  * a scripted actor standing inside the footprint, because it would travel
    with the building and `applymovement` counts steps - the walk still runs,
    but it stops two tiles from where it was written to stop. An actor beside
    the building does not move, so it is allowed, and the whole-map check below
    catches it if the building lands in its way;
  * a destination that holds any event, another building, or anything whose
    metatile behaviour is not plain - a cliff edge, a ledge, water.

Scenery it may push aside. A tree or a fence in the way is cleared to lawn,
because a settlement that grew somewhere else would have cleared it too; that
only ever makes more ground walkable, never less.

After the move the map is re-checked as a whole: every warp, trigger and person
still reachable from the town's entrances, and every scripted walk still landing
on ground it can walk on.

    python3 tools/art/move_buildings.py --report
    python3 tools/art/move_buildings.py --all
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audit"))

from map_invariants import TownMap  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EVENT_KINDS = ("warp_events", "object_events", "bg_events", "coord_events")

# Offsets to try, in order. Small, so a town keeps a sane composition; ordered
# so the first that passes every check is deterministic.
CANDIDATES = [(0, -2), (2, 0), (-2, 0), (0, 2), (2, -2), (-2, -2), (2, 2), (-2, 2),
              (3, 0), (-3, 0), (0, -3), (0, 3), (3, -2), (-3, -2), (3, 2), (-3, 2),
              (0, -1), (1, 0), (-1, 0), (0, 1), (4, 0), (-4, 0)]


def biome_lawn_block(city):
    import forge_town_variants
    return forge_town_variants.town_lawn(city)


def scripted_actors(town):
    """Where every actor a script drives by step count is standing."""
    path = os.path.join(ROOT, "data/maps/%s/scripts.inc" % town.city)
    if not os.path.exists(path):
        return set()
    text = open(path, encoding="utf-8", errors="replace").read()
    driven = {who for who, _ in re.findall(r"applymovement\s+([^,\s]+)\s*,\s*(\w+)", text)}
    out = set()
    for e in town.events("object_events"):
        if str(e.get("local_id")) in driven:
            out.add((int(e["x"]), int(e["y"])))
    return out


# How often a block may be repeated across one map and still count as part of
# a building. A house is drawn from blocks that were cut for that house: its
# roof corners and its window appear once or twice. Landscape is a stamp - the
# same tree, the same fence post, tiled along a border - so it appears dozens
# of times. Three identical houses in one town still leave every block of them
# well under this.
LANDSCAPE_REPEATS = 6


def built_metatiles(town):
    """The blocks this map uses for architecture rather than for landscape.

    The old rule here was "a building is whatever the secondary tileset drew",
    and it was wrong twice over. Emerald draws the Pokemon Center and the Mart
    from the *primary* tileset every outdoor map shares, so a Center read as
    landscape and got built over; and once each town's greenery was reforged
    into its own secondary tileset, every tree read as architecture and a
    single flood swallowed a whole street.

    Rarity separates them without naming a single block, in any tileset.
    """
    counts = collections.Counter(town.metatile(x, y)
                                 for y in range(town.h) for x in range(town.w))
    return {mt for mt, seen in counts.items() if seen < LANDSCAPE_REPEATS}


def is_built(town, cell, rare):
    """Is this cell part of a building?

    Solid and rare is a wall or a closed door. Walkable and rare is only
    architecture if it is standing on top of one: Emerald draws a roof's top
    row and an awning on walkable blocks so the player passes behind them,
    while a one-off corner of street paving is also rare and is not a building.
    """
    x, y = cell
    if not town.inside(x, y) or town.metatile(x, y) not in rare:
        return False
    if not town.walkable(x, y):
        return True
    return (town.behavior(x, y) == 0 and town.inside(x, y + 1)
            and town.metatile(x, y + 1) in rare and not town.walkable(x, y + 1))


def buildings(town):
    """Each building, as the exact set of blocks it is made of.

    Flooding every solid cell returns the map's whole solid mass, because walls
    and the border tree line touch. Climbing from the doorway row by row loses
    any part of the building wider than its doorway - it left the top half of
    Lilycove's contest hall standing where the rest had moved. So flood from
    the doorway through the blocks this map built with (see `built_metatiles`),
    and the building comes back whole, roof row included, and by itself.
    """
    out = []
    claimed = set()
    rare = built_metatiles(town)
    for e in town.events("warp_events"):
        seed = (int(e["x"]), int(e["y"]))
        if seed in claimed or not town.inside(*seed):
            continue
        if not is_built(town, seed, rare):
            continue                     # a doorway cut into the landscape
        mass, stack = set(), [seed]
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in mass:
                continue
            mass.add((cx, cy))
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                nx, ny = cx + dx, cy + dy
                if (nx, ny) in mass or not is_built(town, (nx, ny), rare):
                    continue
                stack.append((nx, ny))
        if len(mass) < 4:
            continue
        claimed |= mass
        out.append(frozenset(mass))
    return out


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


def cells_of(shape):
    return list(shape)


def shift(shape, offset):
    dx, dy = offset
    return frozenset((x + dx, y + dy) for x, y in shape)


def bounds(shape):
    xs = [c[0] for c in shape]
    ys = [c[1] for c in shape]
    return min(xs), min(ys), max(xs), max(ys)


def events_in(town, shape):
    found = collections.defaultdict(list)
    for kind in EVENT_KINDS:
        for e in town.map.get(kind) or []:
            if "x" in e and (int(e["x"]), int(e["y"])) in shape:
                found[kind].append(e)
    return found


def scenery(town, cell, footprints, campaign):
    """A solid block that is only decoration: a tree, a hedge, a fence.

    Anything a building is made of is excluded by footprint, anything with a
    behaviour of its own - a cliff, a ledge, water - by behaviour, and anything
    the campaign stands on or walks through by coordinate.
    """
    x, y = cell
    if town.walkable(x, y) or town.behavior(x, y) != 0:
        return False
    if cell in campaign:
        return False
    if x in (0, town.w - 1) or y in (0, town.h - 1):
        return False
    if is_built(town, cell, built_metatiles(town)):
        return False                     # somebody's wall, not a hedge
    return not any(cell in shape for shape in footprints)


def buriable(town):
    """Walkable ground the campaign needs to stay walkable.

    A building only has to be refused where it would land on something solid,
    or on an event's own coordinate - or so the first version of this thought.
    But a sign is read from the tile in front of it, a person paces a box
    wider than the tile they start on, and a cutscene counts steps across open
    ground. All three are walkable, so all three would be built over in
    silence: it put a wall through the sign outside Lavaridge's gym and buried
    a passer-by in Lilycove.
    """
    marked = town.protected()
    return (marked["bg_events"] | marked["people"] | marked["coord_events"]
            | town.scripted_paths(include_player=False, include_repositioned=False))


def why_not(town, shape, offset, lawn, actors, seams, taken, footprints, campaign):
    dx, dy = offset
    inside = events_in(town, shape)
    if inside["coord_events"]:
        return "a trigger stands in it"
    if actors & shape:
        return "a scripted actor stands inside it"
    moved = shift(shape, offset)
    for cell in moved:
        if not town.inside(*cell):
            return "it would leave the map"
        if cell in seams:
            return "it would reach the route seam"
        if cell in taken:
            return "another move already claimed that ground"
        if cell in shape:
            continue
        if not town.walkable(*cell) and not scenery(town, cell, footprints, campaign):
            return "there is something solid where it would land"
        if cell in town.buriable:
            return "it would build over ground the campaign walks on"
    for kind in EVENT_KINDS:
        for e in town.map.get(kind) or []:
            if "x" not in e:
                continue
            here = (int(e["x"]), int(e["y"]))
            if here in moved and here not in shape:
                return "an event stands where it would land"
    # A footprint that leaves part of the same building behind is not a
    # footprint, and a destination that lands on part of one tears that one in
    # half - which is how a street ended up running over a Pokemon Center's
    # roof. Both are asked of the blocks this map builds with.
    rare = built_metatiles(town)
    for cell in shape:
        if not is_built(town, cell, rare):
            continue
        for dxx, dyy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            n = (cell[0] + dxx, cell[1] + dyy)
            if n not in shape and is_built(town, n, rare):
                return "it would leave part of the same building behind"
    for cell in moved:
        if cell not in shape and is_built(town, cell, rare):
            return "it would land on part of another building"
    # A doorway is only a doorway if you can stand in front of it.
    for e in town.events("warp_events"):
        here = (int(e["x"]), int(e["y"]))
        if here in shape:
            step = (here[0] + dx, here[1] + dy + 1)
            if not town.inside(*step) or step in moved or not town.walkable(*step):
                return "its doorstep would be blocked"
    return None


def apply_move(town, shape, offset, lawn, footprints, campaign, physics):
    dx, dy = offset
    moved = shift(shape, offset)
    # Clear whatever scenery stood where the building is going.
    for cell in moved:
        if cell not in shape and scenery(town, cell, footprints, campaign):
            town.blocks[town.index(*cell)] = physics | lawn
    payload = {cell: town.blocks[town.index(*cell)] for cell in shape}
    # Vacated ground becomes plain walkable lawn, at whatever elevation the
    # walkable cells of the footprint were already using.
    for cell in shape:
        town.blocks[town.index(*cell)] = physics | lawn
    for cell in shape:
        if cell not in moved and not town.walkable(*cell):
            raise SystemExit("vacated ground at %d,%d is not walkable" % cell)
    for (x, y), value in payload.items():
        town.blocks[town.index(x + dx, y + dy)] = value
    for kind, items in events_in(town, shape).items():
        for e in items:
            e["x"] = int(e["x"]) + dx
            e["y"] = int(e["y"]) + dy


def scripted_walks_ok(town):
    """Every step a script takes still lands on ground it can walk on."""
    bad = []
    for (x, y) in town.scripted_paths(include_player=False, include_repositioned=False):
        if town.inside(x, y) and not town.walkable(x, y) and not town.surfable(x, y):
            bad.append((x, y))
    return bad


def move_town(city, dry_run):
    town = TownMap(city, ROOT)
    lawn = biome_lawn_block(city)
    if lawn is None:
        return None
    actors = frozenset(scripted_actors(town))
    seams = town.seams()
    before_reach = town.reachable(allow_water=False)
    before_walks = set(scripted_walks_ok(town))

    def harm():
        """What a move just cost, measured on the whole map rather than locally.

        Losing any ground at all is refused, not just ground an event stands
        on: a building that walls off an empty corner has still walled off a
        corner, and a player who walks into it finds a pocket that goes
        nowhere. The building's own new footprint is not a loss - that ground
        is the building.
        """
        lost = before_reach - town.reachable(allow_water=False) - set(town.solid_now)
        for kind in EVENT_KINDS:
            for e in town.map.get(kind) or []:
                if "x" in e and (int(e["x"]), int(e["y"])) in lost:
                    return "%s at %s,%s would be cut off" % (kind[:-7], e["x"], e["y"])
        if lost:
            cell = sorted(lost)[0]
            return "%d tile(s) would be walled off, from %d,%d" % (len(lost), *cell)
        if set(scripted_walks_ok(town)) - before_walks:
            return "a scripted step would walk into a wall"
        return None

    footprints = buildings(town)
    town.buriable = buriable(town)
    physics = ground_physics(town)
    campaign = town.campaign_cells()
    taken, moved, refused = set(), [], []
    for shape in footprints:
        last = None
        for offset in CANDIDATES:
            last = why_not(town, shape, offset, lawn, actors, seams, taken, footprints, campaign)
            if last:
                continue
            # Local checks pass; try it for real and keep it only if the map as
            # a whole survives. Anything else is put back exactly as it was.
            town.solid_now = shift(shape, offset)
            blocks_before = list(town.blocks)
            events_before = json.loads(json.dumps({k: town.map.get(k) for k in EVENT_KINDS}))
            apply_move(town, shape, offset, lawn, footprints, campaign, physics)
            last = harm()
            if last is None:
                taken |= shift(shape, offset) | shape
                moved.append((shape, offset))
                break
            town.blocks = blocks_before
            for kind, items in events_before.items():
                if items is not None:
                    town.map[kind] = items
        else:
            refused.append((shape, last or "no offset fits"))

    if moved and not dry_run:
        open(town.path, "wb").write(struct.pack("<%dH" % len(town.blocks), *town.blocks))
        json.dump(town.map, open(os.path.join(ROOT, "data/maps/%s/map.json" % city), "w",
                                 encoding="utf-8"), indent=2)
        open(os.path.join(ROOT, "data/maps/%s/map.json" % city), "a", encoding="utf-8").write("\n")
    return {"city": city, "moved": moved, "refused": refused}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("city", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    import retheme_cities
    import replan_towns
    # A town with a plan drawn by hand is not a town for a blind nudge.
    cities = [c for c in retheme_cities.THEMES
              if retheme_cities.THEMES[c].get("biome") and c not in replan_towns.PLANS] \
        if (args.all or args.report) else [args.city]
    for city in cities:
        r = move_town(city, args.report)
        if not r:
            continue
        print("%-16s %d building(s) moved, %d left alone" % (city, len(r["moved"]), len(r["refused"])))
        for shape, offset in r["moved"]:
            print("    %d blocks at %d,%d by %+d,%+d"
                  % (len(shape), bounds(shape)[0], bounds(shape)[1], *offset))
        for shape, reason in r["refused"]:
            print("    %d blocks at %d,%d stay: %s"
                  % (len(shape), bounds(shape)[0], bounds(shape)[1], reason))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

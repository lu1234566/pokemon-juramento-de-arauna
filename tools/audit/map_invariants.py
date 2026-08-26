#!/usr/bin/env python3
"""What a town's block grid may not lose when it is redesigned.

A settlement can be rebuilt as heavily as you like as long as the campaign
still runs through it. That is a smaller promise than "do not change the map",
and it can be stated exactly, per block:

  * physics frozen - collision and elevation stay bit-identical, so every
    step the player, an NPC or a scripted `applymovement` could take is still
    available and still costs the same;
  * behaviour frozen - the metatile behaviour stays identical, so a doorway
    stays a doorway, water stays water, tall grass stays tall grass and no
    patch of decoration quietly becomes an encounter tile;
  * seams accounted for - a connection is defined by the two maps' dimensions
    and its offset, never by what the blocks at the join look like, and their
    physics and behaviour are frozen like everything else. So restyling them
    cannot break a join; it can only make the change visible at the town's
    edge, which is a decision, not an accident. They are counted and reported
    rather than forbidden.

What is left free is the metatile id, which is the entire look of the town:
walls, roofs, ground, vegetation, water surface, cliffs. That is enough to
rebuild a settlement's identity without touching a single thing the campaign
can trip over.

`--free-structure` relaxes the first two rules away from the coordinates the
campaign actually uses, for changes that do intend to move a wall. Everything
the campaign uses stays frozen, and reachability is re-checked.

    python3 tools/audit/map_invariants.py LittlerootTown --report
    python3 tools/audit/map_invariants.py LittlerootTown --verify HEAD
"""
from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BEHAVIOR_MASK = 0x00FF
NUM_METATILES_IN_PRIMARY = 512

DIRECTIONS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
# A connection's seam is the strip the neighbouring map is drawn against. Two
# blocks deep covers the road in and the row it lines up with.
SEAM_DEPTH = 2

CITIES = [
    "LittlerootTown", "OldaleTown", "PetalburgCity", "RustboroCity",
    "DewfordTown", "SlateportCity", "MauvilleCity", "VerdanturfTown",
    "FallarborTown", "LavaridgeTown", "FortreeCity", "LilycoveCity",
    "MossdeepCity", "SootopolisCity", "PacifidlogTown", "EverGrandeCity",
]


def behaviors():
    """MB_* name -> value, read from the enum the game itself compiles."""
    text = open(os.path.join(ROOT, "include/constants/metatile_behaviors.h"), encoding="utf-8").read()
    body = text.split("enum {", 1)[1].split("};", 1)[0]
    out, value = {}, 0
    for token in body.split(","):
        token = re.sub(r"//.*", "", token).strip()
        if not token:
            continue
        if "=" in token:
            name, raw = (part.strip() for part in token.split("=", 1))
            value = int(raw, 0)
        else:
            name = token
        out[name] = value
        value += 1
    return out


MB = behaviors()
LEDGE_JUMPS = {
    MB["MB_JUMP_EAST"]: (1, 0),
    MB["MB_JUMP_WEST"]: (-1, 0),
    MB["MB_JUMP_NORTH"]: (0, -1),
    MB["MB_JUMP_SOUTH"]: (0, 1),
    MB["MB_JUMP_NORTHEAST"]: (1, -1),
    MB["MB_JUMP_NORTHWEST"]: (-1, -1),
    MB["MB_JUMP_SOUTHEAST"]: (1, 1),
    MB["MB_JUMP_SOUTHWEST"]: (-1, 1),
}
WATER = {MB[name] for name in (
    "MB_POND_WATER", "MB_DEEP_WATER", "MB_OCEAN_WATER", "MB_SOOTOPOLIS_DEEP_WATER",
    "MB_INTERIOR_DEEP_WATER", "MB_NO_SURFACING", "MB_SEAWEED", "MB_WATERFALL",
    "MB_UNUSED_SOOTOPOLIS_DEEP_WATER", "MB_UNUSED_SOOTOPOLIS_DEEP_WATER_2",
)}

STEP_DELTAS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}
MOVEMENT_STEP = re.compile(
    r"^\s*(?:walk|slow|fast|jump|ride_water_current)?_?"
    r"(?:in_place_)?(?:walk_)?(?:slow_|fast_|faster_|fastest_|diag_)?"
    r"(left|right|up|down)\b", re.I)


class TownMap:
    def __init__(self, city, root=ROOT, blocks=None, ref=None):
        # `ref` reads the tilesets' attributes from a revision too. Without it
        # a baseline's block ids would be read against today's attribute
        # tables, and any change to a tileset would be reported as if the map
        # had changed under it.
        self.ref = ref
        self.city = city
        self.root = root
        self.map = json.load(open(os.path.join(root, "data/maps/%s/map.json" % city), encoding="utf-8"))
        layouts = json.load(open(os.path.join(root, "data/layouts/layouts.json"), encoding="utf-8"))["layouts"]
        self.layout = next(l for l in layouts if l["id"] == self.map["layout"])
        self.w = int(self.layout["width"])
        self.h = int(self.layout["height"])
        self.path = os.path.join(root, self.layout["blockdata_filepath"])
        raw = blocks if blocks is not None else open(self.path, "rb").read()
        self.blocks = list(struct.unpack("<%dH" % (self.w * self.h), raw))
        self.attrs = self._attributes()

    def _attributes(self):
        def read(symbol):
            name = symbol.replace("gTileset_", "")
            slug = "".join(("_" if c.isupper() and i else "") + c.lower() for i, c in enumerate(name))
            for kind in ("primary", "secondary"):
                rel = "data/tilesets/%s/%s/metatile_attributes.bin" % (kind, slug)
                p = os.path.join(self.root, rel)
                if not os.path.exists(p):
                    continue
                if self.ref:
                    blob = subprocess.check_output(["git", "show", "%s:%s" % (self.ref, rel)],
                                                   cwd=self.root)
                else:
                    blob = open(p, "rb").read()
                return list(struct.unpack("<%dH" % (len(blob) // 2), blob))
            raise SystemExit("no attributes for %s" % symbol)
        return read(self.layout["primary_tileset"]), read(self.layout["secondary_tileset"])

    # -- per-cell reads -----------------------------------------------------
    def index(self, x, y):
        return y * self.w + x

    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def metatile(self, x, y):
        return self.blocks[self.index(x, y)] & 0x03FF

    def physics(self, x, y):
        return self.blocks[self.index(x, y)] & 0xFC00

    def collision(self, x, y):
        return (self.blocks[self.index(x, y)] >> 10) & 0x03

    def elevation(self, x, y):
        return (self.blocks[self.index(x, y)] >> 12) & 0x0F

    def behavior_of(self, metatile_id):
        primary, secondary = self.attrs
        if metatile_id < NUM_METATILES_IN_PRIMARY:
            table, i = primary, metatile_id
        else:
            table, i = secondary, metatile_id - NUM_METATILES_IN_PRIMARY
        return (table[i] & BEHAVIOR_MASK) if i < len(table) else 0

    def behavior(self, x, y):
        return self.behavior_of(self.metatile(x, y))

    def walkable(self, x, y):
        return self.collision(x, y) == 0

    def surfable(self, x, y):
        return self.behavior(x, y) in WATER

    # -- coordinates the campaign depends on --------------------------------
    def events(self, kind):
        for e in self.map.get(kind) or []:
            if "x" in e and "y" in e:
                yield e

    def wander_box(self, e):
        rx, ry = int(e.get("movement_range_x", 0) or 0), int(e.get("movement_range_y", 0) or 0)
        x, y = int(e["x"]), int(e["y"])
        for dy in range(-ry, ry + 1):
            for dx in range(-rx, rx + 1):
                if self.inside(x + dx, y + dy):
                    yield (x + dx, y + dy)

    def seams(self):
        out = set()
        for c in self.map.get("connections") or []:
            d = c.get("direction")
            if d == "up":
                cells = [(x, y) for y in range(SEAM_DEPTH) for x in range(self.w)]
            elif d == "down":
                cells = [(x, y) for y in range(self.h - SEAM_DEPTH, self.h) for x in range(self.w)]
            elif d == "left":
                cells = [(x, y) for x in range(SEAM_DEPTH) for y in range(self.h)]
            elif d == "right":
                cells = [(x, y) for x in range(self.w - SEAM_DEPTH, self.w) for y in range(self.h)]
            else:
                continue
            out.update(cells)
        return out

    def scripted_paths(self, include_player=True, include_repositioned=True):
        """Tiles a scripted walk crosses, replayed from the map's own scripts.

        Each `applymovement` is matched to the object event it names by local
        id and replayed step by step from that object's coordinate; movements
        handed to the player are replayed from every trigger and warp, since
        that is where a cutscene can catch the player standing. What the walk
        actually steps on is claimed - a scripted walk must never find a wall
        in front of it.
        """
        path = os.path.join(self.root, "data/maps/%s/scripts.inc" % self.city)
        if not os.path.exists(path):
            return set()
        text = open(path, encoding="utf-8", errors="replace").read()
        common = os.path.join(self.root, "data/scripts/movement.inc")
        if os.path.exists(common):
            text_moves = text + "\n" + open(common, encoding="utf-8", errors="replace").read()
        else:
            text_moves = text

        moves, label = {}, None
        for line in text_moves.splitlines():
            stripped = line.strip()
            m = re.match(r"^(\w+):\s*(?:@.*)?$", stripped)
            if m:
                label = m.group(1)
                moves.setdefault(label, [])
                continue
            if label is None:
                continue
            if stripped.startswith("step_end"):
                label = None
                continue
            step = MOVEMENT_STEP.match(stripped)
            if step and label in moves:
                moves[label].append(step.group(1).lower())

        # An actor a script teleports with `setobjectxy` does not start its
        # walks where the map put it, so replaying from the map's coordinate
        # invents paths that never happen. Freezing those tiles anyway is
        # harmless; judging a change by them is not, so a caller can leave them
        # out and let the game itself answer for them.
        repositioned = set(re.findall(r"setobjectxy(?:perm)?\s+([^,\s]+)", text))
        by_local_id = {}
        for e in self.events("object_events"):
            if not e.get("local_id"):
                continue
            if not include_repositioned and str(e["local_id"]) in repositioned:
                continue
            by_local_id[str(e["local_id"])] = (int(e["x"]), int(e["y"]))
        everyone = [(int(e["x"]), int(e["y"])) for e in self.events("object_events")]
        player_starts = [(int(e["x"]), int(e["y"])) for e in self.events("coord_events")]
        player_starts += [(int(e["x"]), int(e["y"])) for e in self.events("warp_events")]

        swept = set()
        for who, label in re.findall(r"applymovement\s+([^,\s]+)\s*,\s*(\w+)", text):
            steps = moves.get(label) or []
            if not steps:
                continue
            if who in ("LOCALID_PLAYER", "OBJ_EVENT_ID_PLAYER"):
                # The player's start is wherever the cutscene caught them, so
                # this replays from every trigger and warp - deliberately more
                # than can really happen. That over-approximation is right for
                # deciding what to freeze and wrong for judging a change, so a
                # caller that is asking "did I break a walk" leaves it out and
                # checks the actors whose start is known instead.
                if not include_player:
                    continue
                starts = player_starts
            elif who in by_local_id:
                starts = [by_local_id[who]]
            elif not include_repositioned:
                continue
            else:
                starts = everyone
            for sx, sy in starts:
                x, y = sx, sy
                if self.inside(x, y):
                    swept.add((x, y))
                for step in steps:
                    dx, dy = STEP_DELTAS[step]
                    x, y = x + dx, y + dy
                    if self.inside(x, y):
                        swept.add((x, y))
        return swept

    def campaign_cells(self):
        """Everything the campaign can stand on, walk through or line up with."""
        cells = set(self.seams())
        for kind in ("warp_events", "coord_events", "bg_events"):
            cells |= {(int(e["x"]), int(e["y"])) for e in self.events(kind)}
        for e in self.events("object_events"):
            cells |= set(self.wander_box(e))
        cells |= self.scripted_paths()
        return {c for c in cells if self.inside(*c)}

    def protected(self):
        return {
            "warps": {(int(e["x"]), int(e["y"])) for e in self.events("warp_events")},
            "coord_events": {(int(e["x"]), int(e["y"])) for e in self.events("coord_events")},
            "bg_events": {(int(e["x"]), int(e["y"])) for e in self.events("bg_events")},
            "people": {c for e in self.events("object_events") for c in self.wander_box(e)},
            "seams": self.seams(),
            "scripted": self.scripted_paths(),
        }

    # -- reachability -------------------------------------------------------
    def _seeds(self):
        seeds = {(int(e["x"]), int(e["y"])) for e in self.events("warp_events")}
        for x, y in self.seams():
            if self.walkable(x, y) or self.surfable(x, y):
                seeds.add((x, y))
        return {s for s in seeds if self.inside(*s)}

    def reachable(self, allow_water):
        def open_cell(x, y):
            return self.walkable(x, y) or (allow_water and self.surfable(x, y))

        seen = set()
        stack = [s for s in self._seeds() if open_cell(*s)]
        seen.update(stack)
        while stack:
            x, y = stack.pop()
            here = self.elevation(x, y)
            for dx, dy in DIRECTIONS.values():
                nx, ny = x + dx, y + dy
                if not self.inside(nx, ny):
                    continue
                if (nx, ny) not in seen and open_cell(nx, ny):
                    there = self.elevation(nx, ny)
                    if here == there or here in (0, 15) or there in (0, 15):
                        seen.add((nx, ny))
                        stack.append((nx, ny))
                        continue
                if LEDGE_JUMPS.get(self.behavior(nx, ny)) == (dx, dy):
                    lx, ly = x + dx * 2, y + dy * 2
                    if self.inside(lx, ly) and open_cell(lx, ly) and (lx, ly) not in seen:
                        seen.add((lx, ly))
                        stack.append((lx, ly))
        return seen


def baseline_blocks(city, ref, root=ROOT):
    layouts = json.load(open(os.path.join(root, "data/layouts/layouts.json"), encoding="utf-8"))["layouts"]
    map_data = json.load(open(os.path.join(root, "data/maps/%s/map.json" % city), encoding="utf-8"))
    layout = next(l for l in layouts if l["id"] == map_data["layout"])
    return subprocess.check_output(["git", "show", "%s:%s" % (ref, layout["blockdata_filepath"])], cwd=root)


def verify(city, ref="HEAD", free_structure=False, root=ROOT):
    now = TownMap(city, root)
    was = TownMap(city, root, blocks=baseline_blocks(city, ref, root), ref=ref)
    problems = []
    if len(now.blocks) != len(was.blocks):
        return ["%s: block grid size changed" % city]

    campaign = was.campaign_cells()
    frozen_physics = campaign if free_structure else None
    changed = 0
    seam_restyled = 0

    for y in range(now.h):
        for x in range(now.w):
            if now.blocks[now.index(x, y)] == was.blocks[was.index(x, y)]:
                continue
            changed += 1
            frozen = frozen_physics is None or (x, y) in frozen_physics
            if frozen and now.physics(x, y) != was.physics(x, y):
                problems.append("%d,%d: collision/elevation %d/%d -> %d/%d on a tile the campaign uses"
                                % (x, y, was.collision(x, y), was.elevation(x, y),
                                   now.collision(x, y), now.elevation(x, y)))
            if frozen and now.behavior(x, y) != was.behavior(x, y):
                problems.append("%d,%d: behaviour %d -> %d on a tile the campaign uses"
                                % (x, y, was.behavior(x, y), now.behavior(x, y)))
            if (x, y) in was.seams():
                seam_restyled += 1

    for kind, cells in (("warp", was.protected()["warps"]), ("sign", was.protected()["bg_events"])):
        for x, y in sorted(cells):
            if now.behavior(x, y) != was.behavior(x, y):
                problems.append("%s at %d,%d: behaviour %d -> %d" % (kind, x, y,
                                was.behavior(x, y), now.behavior(x, y)))

    for label, water in (("on foot", False), ("by surf", True)):
        lost = was.reachable(water) - now.reachable(water)
        touching = sorted(lost & campaign)
        if touching:
            problems.append("%s: %d campaign tile(s) cut off, e.g. %s"
                            % (label, len(touching), " ".join("%d,%d" % c for c in touching[:6])))
        elif lost:
            problems.append("%s: %d tile(s) that used to be reachable no longer are, e.g. %s"
                            % (label, len(lost), " ".join("%d,%d" % c for c in sorted(lost)[:6])))

    # Deduplicate while keeping the first mention of each coordinate.
    seen, unique = set(), []
    for p in problems:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique, changed, seam_restyled


def report(city, root=ROOT):
    m = TownMap(city, root)
    prot = m.protected()
    marks = {}
    for label, cells in (("W", prot["warps"]), ("T", prot["coord_events"]),
                         ("S", prot["bg_events"]), ("n", prot["people"]),
                         ("*", prot["scripted"]), (":", prot["seams"])):
        for c in cells:
            marks.setdefault(c, label)
    print("%s %dx%d" % (city, m.w, m.h))
    print("    " + "".join("%d" % (x % 10) for x in range(m.w)))
    for y in range(m.h):
        row = ""
        for x in range(m.w):
            if (x, y) in marks:
                row += marks[(x, y)]
            elif not m.walkable(x, y):
                row += "#"
            elif m.surfable(x, y):
                row += "~"
            else:
                row += "."
        print("%3d %s" % (y, row))
    free = m.w * m.h - len(m.campaign_cells())
    print("W warp  T trigger  S sign  n person  * scripted walk  : route seam  # solid  ~ water  . open")
    print("%d of %d blocks are outside every campaign coordinate" % (free, m.w * m.h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("city", nargs="?", help="one settlement, or every one when --verify is used alone")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--verify", metavar="GIT_REF", help="compare against this revision's block data")
    ap.add_argument("--free-structure", action="store_true",
                    help="allow collision and behaviour to change away from campaign coordinates")
    args = ap.parse_args()

    if args.report:
        report(args.city)
        return 0
    if args.verify:
        cities = [args.city] if args.city else CITIES
        failed = 0
        for city in cities:
            problems, changed, seams = verify(city, args.verify, args.free_structure)
            for p in problems[:12]:
                print("  " + p)
            if len(problems) > 12:
                print("  ... and %d more" % (len(problems) - 12))
            print("%-16s %5d blocks restyled (%3d on a route seam)  %s"
                  % (city, changed, seams,
                     "FAIL (%d)" % len(problems) if problems else "OK"))
            failed += bool(problems)
        return 1 if failed else 0
    report(args.city)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

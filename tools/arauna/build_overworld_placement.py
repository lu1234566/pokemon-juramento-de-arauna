#!/usr/bin/env python3
"""Put the Arauna overworld creatures out in the world.

Forty-three of the forty-six redraws were registered and invisible: reachable
from the dispatcher, standing nowhere. This places them.

Which creature goes where is not guessed. Each candidate map already declares
what lives in it -- its wild encounter table -- so the dominant type of that
table picks the creature, and a water route gets something aquatic because the
route itself says so.

Where exactly it stands is verified, not guessed either. A 64x64 object is four
tiles wide; dropping one into a doorway or a one-tile corridor would be a
progression bug. Every candidate coordinate has to pass:

  * passable in the map's own blockdata (collision bits of the block are 0);
  * not on, and not beside, a warp;
  * not on an existing object event;
  * at least three passable neighbours, so it is not standing in a corridor;
  * and an articulation test -- flood fill the passable area with and without
    the tile blocked, and require the reachable count to drop by exactly one.
    If standing there would cut the map in half, the tile is rejected.

No map script is touched. The selector vars are set from a generated
map -> (channel A, channel B) table, read by SetAraunaOverworldForCurrentMap()
which runs just before a map's own ON_TRANSITION script, so a map that wants to
override still can.

  --check   choose and validate, write nothing
  --write   write the map objects, the map table and the placement CSV
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import struct
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORT = ROOT / "graphics/arauna/arauna_sprites_gba_export.zip"
MAPPING = ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
SELECTION = ROOT / "docs/arauna/ARAUNA_OVERWORLD_46.csv"
PLACEMENT = ROOT / "docs/arauna/ARAUNA_OVERWORLD_PLACEMENT.csv"
LAYOUTS = ROOT / "data/layouts/layouts.json"
ENCOUNTERS = ROOT / "src/data/wild_encounters.json"
MAPS = ROOT / "data/maps"
MAP_TABLE = ROOT / "src/data/object_events/arauna_overworld_maps.h"

# The three that own a dedicated graphics id and are already standing on maps.
ALREADY_PLACED = {"258", "261", "298"}
# The registry's own proving ground; leave it as it is.
SKIP_MAPS = {"AquaHideout_UnusedRubyMap1"}

WARP_CLEARANCE = 2      # tiles to stay away from a door
EDGE_MARGIN = 3         # tiles to stay in from the map border
MIN_NEIGHBOURS = 3      # of the four orthogonal tiles, how many must be open


def arauna():
    with zipfile.ZipFile(EXPORT) as zf:
        mons = {m["id"]: m for m in json.loads(zf.read("pokedex.json"))["pokemon"]}
    slots, by_dex = {}, {}
    for row in csv.DictReader(MAPPING.open(encoding="utf-8")):
        mon = mons[int(row["arauna_dex"])]
        by_dex[int(row["arauna_dex"])] = {"types": mon["types"], "name": mon["name"]}
        slots[row["species_constant"]] = int(row["arauna_dex"])
    return slots, by_dex


def redraws():
    out = []
    for row in csv.DictReader(SELECTION.open(encoding="utf-8")):
        if row["arauna_dex"] in ALREADY_PLACED:
            continue
        out.append(row)
    return out


def blockdata(layout):
    raw = Path(ROOT / layout["blockdata_filepath"]).read_bytes()
    values = struct.unpack(f"<{len(raw) // 2}H", raw)
    width, height = layout["width"], layout["height"]
    return width, height, [((v >> 10) & 3) == 0 for v in values]


def reachable(width, height, passable, start, blocked=None):
    seen = {start}
    stack = [start]
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if (nx, ny) in seen or (nx, ny) == blocked:
                continue
            if passable[ny * width + nx]:
                seen.add((nx, ny))
                stack.append((nx, ny))
    return seen


def pick_spot(layout, occupied, warps, taken):
    width, height, passable = blockdata(layout)
    open_tiles = [(x, y) for y in range(height) for x in range(width)
                  if passable[y * width + x]]
    if not open_tiles:
        return None, "no passable tile"
    start = max(open_tiles, key=lambda t: min(
        (abs(t[0] - w[0]) + abs(t[1] - w[1]) for w in warps), default=99))
    whole = reachable(width, height, passable, start)

    def neighbours(x, y):
        return sum(1 for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                   if 0 <= nx < width and 0 <= ny < height and passable[ny * width + nx])

    candidates = []
    for (x, y) in whole:
        if not (EDGE_MARGIN <= x < width - EDGE_MARGIN and EDGE_MARGIN <= y < height - EDGE_MARGIN):
            continue
        if (x, y) in occupied or (x, y) in taken:
            continue
        if any(abs(x - wx) < WARP_CLEARANCE and abs(y - wy) < WARP_CLEARANCE
               for wx, wy in warps):
            continue
        if neighbours(x, y) < MIN_NEIGHBOURS:
            continue
        candidates.append((x, y))
    if not candidates:
        return None, "no tile with clearance"

    # Spread them out: prefer the candidate furthest from doors and other objects.
    def spacing(t):
        others = list(warps) + list(occupied) + list(taken)
        return min((abs(t[0] - o[0]) + abs(t[1] - o[1]) for o in others), default=99)

    for spot in sorted(candidates, key=spacing, reverse=True):
        if len(reachable(width, height, passable, start, blocked=spot)) == len(whole) - 1:
            return spot, "ok"
    return None, "every candidate is a chokepoint"


def map_flavour(slots, by_dex):
    """map name -> the types that actually live there, by encounter frequency."""
    data = json.loads(ENCOUNTERS.read_text(encoding="utf-8"))
    out = {}
    for group in data["wild_encounter_groups"]:
        for enc in group["encounters"]:
            if "map" not in enc:
                continue
            counter = collections.Counter()
            for table in ("land_mons", "water_mons", "fishing_mons", "rock_smash_mons"):
                for mon in enc.get(table, {}).get("mons", []):
                    dex = slots.get(mon["species"])
                    if dex:
                        for kind in by_dex[dex]["types"]:
                            counter[kind] += 1
            if counter:
                out[enc["base_label"].removeprefix("g")] = counter
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    slots, by_dex = arauna()
    layouts = {l["id"]: l for l in json.loads(LAYOUTS.read_text(encoding="utf-8"))["layouts"] if l}
    flavour = map_flavour(slots, by_dex)

    pool = redraws()
    unplaced = {row["arauna_dex"]: row for row in pool}

    # Only maps that declare wildlife, are not gyms or the harness, and exist.
    candidates = []
    for name, counter in flavour.items():
        folder = MAPS / name
        if not folder.is_dir() or name in SKIP_MAPS or "_Gym" in name:
            continue
        candidates.append((name, counter))
    def priority(item):
        """Routes first, in number order, then towns and cities, then the rest.

        Alphabetical order buried every creature in Abandoned Ship and Cave of
        Origin. The world the player walks through is the routes.
        """
        name = item[0]
        if name.startswith("Route") and name[5:].isdigit():
            return (0, int(name[5:]), name)
        if name.endswith(("Town", "City")):
            return (1, 0, name)
        return (2, 0, name)

    candidates.sort(key=priority)

    placements, report = [], []
    for name, counter in candidates:
        if not unplaced:
            break
        blob = json.loads((MAPS / name / "map.json").read_text(encoding="utf-8"))
        layout = layouts.get(blob["layout"])
        if not layout:
            continue
        occupied = {(o["x"], o["y"]) for o in blob.get("object_events", [])}
        warps = {(w["x"], w["y"]) for w in blob.get("warp_events", [])}
        if len(blob.get("object_events", [])) + 2 > 60:
            continue

        # Only the types this map actually leans on, and only creatures whose
        # own primary type is one of them: a parrot has no business in a cave
        # just because something there happens to share its secondary type.
        wanted = [kind for kind, _ in counter.most_common(3)]
        chosen, taken = [], set()
        for channel in ("A", "B"):
            match = None
            for kind in wanted:
                for dex, row in unplaced.items():
                    if by_dex[int(dex)]["types"][0] == kind:
                        match = row
                        break
                if match:
                    break
            if not match:
                continue
            spot, why = pick_spot(layout, occupied, warps, taken)
            if not spot:
                report.append((name, "-", why))
                break
            taken.add(spot)
            del unplaced[match["arauna_dex"]]
            chosen.append((channel, match, spot))
        for channel, row, spot in chosen:
            placements.append(dict(map=name, channel=channel, arauna_dex=row["arauna_dex"],
                                   name=row["name"], slug=row["slug"], x=spot[0], y=spot[1],
                                   layout=blob["layout"]))

    # Second pass for whatever the primary-type rule could not house: same maps,
    # same safety checks, but any of the creature's types will do.
    if unplaced:
        used = collections.defaultdict(set)
        for p in placements:
            used[p["map"]].add(p["channel"])
        for name, counter in candidates:
            if not unplaced:
                break
            free = [c for c in ("A", "B") if c not in used[name]]
            if not free:
                continue
            blob = json.loads((MAPS / name / "map.json").read_text(encoding="utf-8"))
            layout = layouts.get(blob["layout"])
            if not layout:
                continue
            occupied = {(o["x"], o["y"]) for o in blob.get("object_events", [])}
            warps = {(w["x"], w["y"]) for w in blob.get("warp_events", [])}
            taken = {(p["x"], p["y"]) for p in placements if p["map"] == name}
            for channel in free:
                match = next((row for dex, row in unplaced.items()
                              if any(k in counter for k in by_dex[int(dex)]["types"])), None)
                if not match:
                    break
                spot, _ = pick_spot(layout, occupied, warps, taken)
                if not spot:
                    break
                taken.add(spot)
                del unplaced[match["arauna_dex"]]
                placements.append(dict(map=name, channel=channel, arauna_dex=match["arauna_dex"],
                                       name=match["name"], slug=match["slug"],
                                       x=spot[0], y=spot[1], layout=blob["layout"]))

    print(f"{len(pool)} criaturas para colocar; {len(placements)} colocadas em "
          f"{len({p['map'] for p in placements})} mapas; {len(unplaced)} sem lugar")
    for problem in report[:6]:
        print(f"  rejeitado: {problem[0]} -- {problem[2]}")
    if unplaced:
        print("  sem mapa compatível: " +
              ", ".join(f"#{d} {r['name']}" for d, r in list(unplaced.items())[:8]))
    for p in placements[:12]:
        print(f"  {p['map']:26} canal {p['channel']}  ({p['x']:2},{p['y']:2})  "
              f"#{p['arauna_dex']} {p['name']}")

    if not args.write:
        return 0

    by_map = collections.defaultdict(dict)
    for p in placements:
        by_map[p["map"]][p["channel"]] = p

    for name, channels in by_map.items():
        path = MAPS / name / "map.json"
        blob = json.loads(path.read_text(encoding="utf-8"))
        blob.setdefault("object_events", [])
        # Appended, never inserted: a local id is the index plus one, and scripts
        # address objects by local id.
        blob["object_events"] = [o for o in blob["object_events"]
                                 if not str(o.get("graphics_id", "")).startswith(
                                     "OBJ_EVENT_GFX_ARAUNA_POKEMON")]
        for channel, p in sorted(channels.items()):
            blob["object_events"].append({
                "graphics_id": f"OBJ_EVENT_GFX_ARAUNA_POKEMON_{channel}",
                "x": p["x"], "y": p["y"], "elevation": 3,
                "movement_type": "MOVEMENT_TYPE_LOOK_AROUND",
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": "0x0", "flag": "0",
            })
        path.write_text(json.dumps(blob, indent=2) + "\n", encoding="utf-8")

    lines = [
        "// Generated by tools/arauna/build_overworld_placement.py. Do not edit.",
        "//",
        "// Which creature each dispatcher channel shows, per map. Read by",
        "// SetAraunaOverworldForCurrentMap() just before the map's own ON_TRANSITION",
        "// script runs, so no map script had to be touched and a map that wants to",
        "// override the choice still can.",
        "",
        "struct AraunaOverworldMap",
        "{",
        "    u8 mapGroup;",
        "    u8 mapNum;",
        "    u8 channelA;",
        "    u8 channelB;",
        "};",
        "",
        "static const struct AraunaOverworldMap sAraunaOverworldMaps[] =",
        "{",
    ]
    for name in sorted(by_map):
        channels = by_map[name]
        # Every map.json carries its own constant; deriving it from the folder
        # name got GraniteCave_1F wrong as MAP_GRANITE_CAVE1_F.
        constant = json.loads((MAPS / name / "map.json").read_text(encoding="utf-8"))["id"]
        a = channels.get("A")
        b = channels.get("B")
        lines.append(f"    {{ MAP_GROUP({constant}), MAP_NUM({constant}), "
                     f"{'ARAUNA_OW_' + a['slug'].upper() if a else 'ARAUNA_OW_NONE'}, "
                     f"{'ARAUNA_OW_' + b['slug'].upper() if b else 'ARAUNA_OW_NONE'} }},"
                     f"  // {a['name'] if a else '-'} / {b['name'] if b else '-'}")
    lines += ["};", ""]
    MAP_TABLE.write_text("\n".join(lines), encoding="utf-8")

    with PLACEMENT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["map", "channel", "arauna_dex", "name", "x", "y"])
        for p in placements:
            writer.writerow([p["map"], p["channel"], p["arauna_dex"], p["name"], p["x"], p["y"]])
    print(f"\nwrote {len(by_map)} maps, {MAP_TABLE.relative_to(ROOT)} and "
          f"{PLACEMENT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

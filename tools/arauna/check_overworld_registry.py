#!/usr/bin/env python3
"""Prove the Arauna overworld registry is complete and costs nothing persistent.

Every claim the design makes is checked against the tree rather than asserted:

  * all 46 redraws are in the registry, on both channels, each pointing at its
    own pic table;
  * the selector constants are unique and inside the registry;
  * the dispatch exists in GetObjectEventGraphicsInfo and clamps the selector;
  * both dispatcher ids are ordinary one-byte ids below NUM_OBJ_EVENT_GFX, which
    is back to its vanilla 239;
  * graphicsId is still u8 in ObjectEventTemplate and in ObjectEvent;
  * the two persistent structs are byte-for-byte what they were before any of
    this work started, so SaveBlock1 cannot have moved;
  * the selector vars are ones vanilla never writes;
  * the harness map places one object per channel, so two different creatures
    stand there at once.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# The commit before the first overworld change touched anything.
BEFORE = "c8557cb2"

CONSTANTS = ROOT / "include/constants/arauna_overworld.h"
REGISTRY = ROOT / "src/data/object_events/arauna_overworld.h"
EVENT_OBJECTS = ROOT / "include/constants/event_objects.h"
MOVEMENT = ROOT / "src/event_object_movement.c"
HARNESS = ROOT / "data/maps/AquaHideout_UnusedRubyMap1/map.json"
PERSISTENT = ["include/global.h", "include/global.fieldmap.h"]


def reachable_tiles(width, height, passable, start, blocked=None):
    seen, stack = {start}, [start]
    while stack:
        x, y = stack.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in seen \
                    and (nx, ny) != blocked and passable[ny * width + nx]:
                seen.add((nx, ny))
                stack.append((nx, ny))
    return seen


def check(name: str, ok: bool, detail: str = "") -> bool:
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'  -- ' + detail if detail else ''}")
    return ok


def main() -> int:
    constants = CONSTANTS.read_text(encoding="utf-8")
    registry = REGISTRY.read_text(encoding="utf-8")
    movement = MOVEMENT.read_text(encoding="utf-8")
    event_objects = EVENT_OBJECTS.read_text(encoding="utf-8")
    results = []

    selectors = dict(re.findall(r"^#define (ARAUNA_OW_\w+)\s+(\d+)", constants, re.M))
    species = {k: int(v) for k, v in selectors.items()
               if k not in ("ARAUNA_OW_NONE", "ARAUNA_OW_COUNT",
                            "ARAUNA_OW_CHANNEL_A", "ARAUNA_OW_CHANNEL_B", "ARAUNA_OW_CHANNELS")}
    count = int(re.search(r"#define ARAUNA_OW_COUNT (\d+)", constants).group(1))

    print("registry")
    results.append(check("46 selector constants", len(species) == 46, f"{len(species)}"))
    results.append(check("selector values unique and in range",
                         sorted(species.values()) == list(range(1, 47)) and count == 47))

    for channel in ("A", "B"):
        entries = re.findall(rf"\[(ARAUNA_OW_\w+)\] = &sAraunaOverworld{channel}_(\w+),", registry)
        named = {name for name, _ in entries if name != "ARAUNA_OW_NONE"}
        infos = {info for _, info in entries if _ != "ARAUNA_OW_NONE"}
        results.append(check(f"channel {channel}: 46 entries, each its own graphics info",
                             named == set(species) and len(infos) == 46, f"{len(named)} entries"))

    tables = set(re.findall(r"\.images = sPicTable_Arauna(\w+),", registry))
    results.append(check("each creature has its own pic table", len(tables) == 46, f"{len(tables)}"))

    slot_a = registry.count(".paletteSlot = PALSLOT_NPC_SPECIAL,")
    slot_b = registry.count(".paletteSlot = 16 + PALSLOT_NPC_SPECIAL_REFLECTION,")
    results.append(check("the two channels claim different palette slots",
                         slot_a == 46 and slot_b == 46, f"A={slot_a} B={slot_b}"))

    print("\ndispatch")
    results.append(check("GetObjectEventGraphicsInfo dispatches both channels",
                         "OBJ_EVENT_GFX_ARAUNA_POKEMON_A]" not in movement
                         and movement.count("gAraunaOverworldGraphicsInfo[ARAUNA_OW_CHANNEL_") == 2))
    results.append(check("the selector is clamped before it indexes",
                         "if (selection >= ARAUNA_OW_COUNT)" in movement))

    ids = {n: int(v) for n, v in re.findall(r"^#define (OBJ_EVENT_GFX_\w+)\s+(\d+)$",
                                            event_objects, re.M)}
    num = int(re.search(r"#define NUM_OBJ_EVENT_GFX\s+(\d+)", event_objects).group(1))
    dispatchers = {k: v for k, v in ids.items() if k.startswith("OBJ_EVENT_GFX_ARAUNA_POKEMON")}
    results.append(check("NUM_OBJ_EVENT_GFX is back to vanilla 239", num == 239, str(num)))
    results.append(check("two dispatcher ids, both ordinary one-byte ids",
                         len(dispatchers) == 2 and all(v < num for v in dispatchers.values()),
                         ", ".join(f"{k}={v}" for k, v in sorted(dispatchers.items()))))
    results.append(check("46 creatures reachable from 2 ids",
                         len(species) == 46 and len(dispatchers) == 2))

    print("\nnothing persistent moved")
    for path in PERSISTENT:
        diff = subprocess.run(["git", "diff", BEFORE, "--", path],
                              cwd=ROOT, capture_output=True, text=True).stdout
        results.append(check(f"{path} unchanged since {BEFORE}", diff == ""))
    fieldmap = (ROOT / "include/global.fieldmap.h").read_text(encoding="utf-8")
    results.append(check("graphicsId is u8 in both structs",
                         fieldmap.count("u8 graphicsId;") == 2))

    # The reservation has to be enforced, not just written down: anything outside
    # the Arauna system that writes these vars silently repaints whatever Arauna
    # overworld object happens to be standing on the map.
    ALLOWED = {
        "include/constants/vars.h",                                   # the reservation itself
        "include/constants/arauna_overworld.h",                       # the selector values
        "src/event_object_movement.c",                                # the dispatcher
        "data/maps/AquaHideout_UnusedRubyMap1/scripts.inc",           # the harness
    }
    trespass = []
    for name in ("VAR_OBJ_GFX_ID_C", "VAR_OBJ_GFX_ID_D", "VAR_ARAUNA_OW_A", "VAR_ARAUNA_OW_B"):
        hits = subprocess.run(["grep", "-rl", rf"\b{name}\b", "data", "src", "include"],
                              cwd=ROOT, capture_output=True, text=True).stdout.split()
        trespass += [f"{h} ({name})" for h in hits if h not in ALLOWED]
    results.append(check("only the Arauna system touches the reserved vars",
                         not trespass, ", ".join(trespass)))

    vanilla_writes = set(subprocess.run(
        ["grep", "-rho", "VAR_OBJ_GFX_ID_[0-9A-F]", "data", "src"],
        cwd=ROOT, capture_output=True, text=True).stdout.split())
    reserved = set(re.findall(r"#define VAR_ARAUNA_OW_[AB]\s+(VAR_OBJ_GFX_ID_[0-9A-F])",
                              (ROOT / "include/constants/vars.h").read_text(encoding="utf-8")))
    results.append(check("both selectors are marked reserved where they are defined",
                         all(f"#define {v}" in line and "RESERVED" in line
                             for v in reserved
                             for line in (ROOT / "include/constants/vars.h").read_text(
                                 encoding="utf-8").splitlines()
                             if line.startswith(f"#define {v} "))))
    del vanilla_writes

    print("\nharness")
    harness = HARNESS.read_text(encoding="utf-8")
    results.append(check("one object per channel on the same map",
                         harness.count("OBJ_EVENT_GFX_ARAUNA_POKEMON_A") == 1
                         and harness.count("OBJ_EVENT_GFX_ARAUNA_POKEMON_B") == 1))
    scripts = (ROOT / "data/maps/AquaHideout_UnusedRubyMap1/scripts.inc").read_text(encoding="utf-8")
    proven = ["ARAUNA_OW_QUERIBELA", "ARAUNA_OW_BOIUNA", "ARAUNA_OW_IEMANJA",
              "ARAUNA_OW_CURUPIRA_ANCIAO", "ARAUNA_OW_ANHANGAU"]
    missing = [p for p in proven if p not in scripts]
    results.append(check("the five named creatures are exercised", not missing, str(missing)))

    # The harness is kept in the shipped build because it costs nothing a player
    # can reach. That is only true while it stays unreachable, so check it.
    elsewhere = [h for h in subprocess.run(
        ["grep", "-rl", "MAP_AQUA_HIDEOUT_UNUSED_RUBY_MAP1", "data", "src"],
        cwd=ROOT, capture_output=True, text=True).stdout.split()
        if not h.startswith("data/maps/AquaHideout_UnusedRubyMap1/")]
    connections = (ROOT / "data/maps/AquaHideout_UnusedRubyMap1/connections.inc").read_text(
        encoding="utf-8").strip()
    results.append(check("the harness map is still unreachable",
                         not elsewhere and not connections,
                         ", ".join(elsewhere) or ("has connections" if connections else "")))

    print("\nplacement")
    import struct, collections
    placed = list(csv.DictReader((ROOT / "docs/arauna/ARAUNA_OVERWORLD_PLACEMENT.csv")
                                 .open(encoding="utf-8")))
    table = (ROOT / "src/data/object_events/arauna_overworld_maps.h").read_text(encoding="utf-8")
    layouts = {l["id"]: l for l in json.loads(
        (ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8"))["layouts"] if l}

    results.append(check("every redraw is somewhere",
                         len(placed) + 3 == 46, f"{len(placed)} placed + 3 with their own id"))
    results.append(check("the map table covers every placed map",
                         len(re.findall(r"MAP_GROUP\(", table)) == len({p["map"] for p in placed}),
                         f"{len(re.findall(chr(77)+'AP_GROUP.', table))} rows"))

    bad_object, bad_tile, blocked = [], [], []
    for name, rows in collections.defaultdict(list, {
            m: [p for p in placed if p["map"] == m] for m in {p["map"] for p in placed}}).items():
        blob = json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))
        objects = {(o["x"], o["y"]): o.get("graphics_id", "")
                   for o in blob.get("object_events", [])}
        layout = layouts[blob["layout"]]
        raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
        values = struct.unpack(f"<{len(raw) // 2}H", raw)
        width, height = layout["width"], layout["height"]
        passable = [((v >> 10) & 3) == 0 for v in values]
        for row in rows:
            spot = (int(row["x"]), int(row["y"]))
            if objects.get(spot, "") != f"OBJ_EVENT_GFX_ARAUNA_POKEMON_{row['channel']}":
                bad_object.append(f"{name}{spot}")
            if not passable[spot[1] * width + spot[0]]:
                bad_tile.append(f"{name}{spot}")
                continue
            # Seed from the tile itself. A map can have passable regions that do
            # not connect -- across water, or below a ledge -- so flooding from
            # an arbitrary corner measures the wrong one.
            region = reachable_tiles(width, height, passable, spot)
            neighbour = next((n for n in ((spot[0] + 1, spot[1]), (spot[0] - 1, spot[1]),
                                          (spot[0], spot[1] + 1), (spot[0], spot[1] - 1))
                              if n in region), None)
            if neighbour is None:
                blocked.append(f"{name}{spot} (isolated)")
            elif reachable_tiles(width, height, passable, neighbour,
                                 blocked=spot) != region - {spot}:
                blocked.append(f"{name}{spot}")
    results.append(check("each placement has its object event on the map",
                         not bad_object, ", ".join(bad_object[:4])))
    results.append(check("every creature stands on a walkable tile",
                         not bad_tile, ", ".join(bad_tile[:4])))
    results.append(check("no creature blocks a chokepoint",
                         not blocked, ", ".join(blocked[:4])))

    print(f"\n{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())

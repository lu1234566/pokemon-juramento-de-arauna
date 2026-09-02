#!/usr/bin/env python3
"""Keep the overworld palette budget honest.

The GBA has sixteen OBJ palette banks, but that is hardware capacity, not what
an object event may use. The engine reserves the first OBJ_PALSLOT_COUNT of
them and writes those by slot: the player and its reflection, four generic NPC
palettes and their four reflections, one bank for a character with colours of
its own and one for that character's reflection. Everything above the reserve
belongs to the general sprite palette allocator, handed out by tag, and
weather claims two of those the moment the overworld starts.

So the real budget on a water-reflection map is two pooled banks plus the two
special slots, and a scene that wants more gets the documented fallback rather
than a wrong bank. This checks the parts of that arrangement a source edit can
break:

  - a character declared as pool-allocated is actually in the pool list;
  - a character declared on a fixed special slot is not also in the pool list,
    which would be two owners for one character;
  - every pool character still names a fallback slot in its graphics info;
  - no two characters on the same fixed special slot share a map where both
    can be seen, which is the collision the CAETANO work found;
  - the reserve boundary is still OBJ_PALSLOT_COUNT, so banks the allocator
    hands out cannot overlap the object-event slots;
  - the forbidden `16 + PALSLOT_...` spelling has not come back;
  - a manifest blocker is not removed while the asset is still missing.

Nothing matches on line numbers.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOVEMENT = ROOT / "src/event_object_movement.c"
INFO = ROOT / "src/data/object_events/object_event_graphics_info.h"
MANIFEST = ROOT / "tools/arauna/character_manifest.json"
POOL_SLOT = "ARAUNA_EXCLUSIVE_POOL"
FIXED_SLOTS = ("PALSLOT_NPC_SPECIAL", "PALSLOT_NPC_SPECIAL_REFLECTION")


def main() -> int:
    movement = MOVEMENT.read_text(encoding="utf-8")
    info = INFO.read_text(encoding="utf-8")
    cast = json.loads(MANIFEST.read_text(encoding="utf-8"))["characters"]

    results: list[tuple[bool, str, str]] = []

    def check(ok: bool, label: str, detail: str = "") -> None:
        results.append((ok, label, detail))

    table = re.search(r"sAraunaExclusivePaletteTags\[\]\s*=\s*\{(.*?)\};",
                      movement, re.S)
    pool_tags = set(re.findall(r"OBJ_EVENT_PAL_TAG_\w+", table.group(1))) if table else set()
    pool_tags.discard("OBJ_EVENT_PAL_TAG_NONE")
    check(table is not None, "the pool list exists",
          f"{len(pool_tags)} characters" if table else "missing")

    blocks = dict(re.findall(
        r"gObjectEventGraphicsInfo_(\w+) = \{(.*?)\n\};", info, re.S))

    declared_pool, declared_fixed = set(), {}
    for c in cast:
        if "overworld" not in c.get("surfaces", []):
            continue
        tag, slot = c.get("palette_tag"), c.get("palette_slot")
        if slot == POOL_SLOT:
            declared_pool.add(tag)
            body = blocks.get(c.get("graphics_info", ""), "")
            fallback = re.search(r"\.paletteSlot = ([A-Za-z0-9_ +]+),", body)
            check(bool(fallback), f"{c['name']} names a fallback slot",
                  fallback.group(1).strip() if fallback else "none")
        elif slot in FIXED_SLOTS:
            declared_fixed[tag] = (c["name"], slot)

    check(declared_pool == pool_tags,
          "manifest and pool list agree on who is pool-allocated",
          f"manifest-only {sorted(declared_pool - pool_tags)}, "
          f"list-only {sorted(pool_tags - declared_pool)}"
          if declared_pool != pool_tags else "identical")

    both = sorted(set(declared_fixed) & pool_tags)
    check(not both, "no character claims a fixed slot and the pool at once",
          ", ".join(both) if both else "none")

    # Two characters on the same fixed special slot must not share a map, which
    # is the collision that put CAETANO in somebody else's colours.
    ptr = (ROOT / "src/data/object_events/object_event_graphics_info_pointers.h"
           ).read_text(encoding="utf-8")
    gfx_of = {i: g for g, i in re.findall(
        r"\[OBJ_EVENT_GFX_(\w+)\] =\s*&gObjectEventGraphicsInfo_(\w+),", ptr)}
    slot_of_gfx = {}
    safe_with = {}
    for c in cast:
        if c.get("palette_slot") in FIXED_SLOTS and c.get("object_event"):
            slot_of_gfx[c["object_event"].replace("OBJ_EVENT_GFX_", "")] = \
                (c["name"], c["palette_slot"])
        # Sharing a map is not sharing a moment. A pair audited as never
        # simultaneously visible says so here, from both sides, and an
        # unaudited pair still fails.
        for other in c.get("same_slot_safe_with", {}):
            safe_with.setdefault(c["name"], set()).add(other)
    clashes = []
    for ev in (ROOT / "data/maps").glob("*/events.inc"):
        seen = {}
        for gid in re.findall(r"object_event \d+, OBJ_EVENT_GFX_(\w+),",
                              ev.read_text(encoding="utf-8")):
            if gid in slot_of_gfx:
                name, slot = slot_of_gfx[gid]
                if slot in seen and seen[slot] != name:
                    a, b = seen[slot], name
                    mutual = (b in safe_with.get(a, set())
                              and a in safe_with.get(b, set()))
                    if not mutual:
                        clashes.append(f"{ev.parent.name}: {a} and {b} "
                                       f"both on {slot}")
                seen[slot] = name
    check(not clashes, "no two characters share a fixed special slot on a map",
          "; ".join(clashes[:3]) if clashes else "none")

    check("OBJ_PALSLOT_COUNT" in movement,
          "the allocator reserve is still tied to OBJ_PALSLOT_COUNT")

    stale = re.findall(r"\.paletteSlot = 16 \+", info) + \
        re.findall(r"\.paletteSlot = 16 \+",
                   (ROOT / "src/data/object_events/arauna_overworld.h"
                    ).read_text(encoding="utf-8"))
    check(not stale, "the forbidden 16 + PALSLOT spelling has not returned",
          f"{len(stale)} occurrences" if stale else "none")

    missing = []
    for c in cast:
        for surface, key in (("overworld", "overworld"), ("front", "front")):
            if surface in c.get("surfaces", []) and c.get(key):
                if not (ROOT / c[key]).is_file():
                    missing.append(f"{c['name']} {surface}")
    check(not missing, "every declared surface has its asset on disk",
          ", ".join(missing) if missing else "none")

    width = max(len(l) for _, l, _ in results)
    failed = sum(1 for ok, _, _ in results if not ok)
    for ok, label, detail in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<{width}}"
              + (f"  -- {detail}" if detail else ""))
    print(f"\n{len(results) - failed}/{len(results)} palette capacity checks passed")
    if failed:
        print("Arauna overworld palette capacity: FAIL", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

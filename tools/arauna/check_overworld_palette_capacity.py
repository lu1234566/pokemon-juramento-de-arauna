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
special slots, plus whichever of the four NPC reflection banks no live object
event can reflect into. A scene that wants more than that gets the documented
fallback rather than a wrong bank. This checks the parts of that arrangement a
source edit can break:

  - a character declared as pool-allocated is actually in the pool list;
  - a character declared on a fixed special slot is not also in the pool list,
    which would be two owners for one character;
  - every pool character still names a fallback slot in its graphics info;
  - no two characters on the same fixed special slot share a map where both
    can be seen, which is the collision the CAETANO work found;
  - the reserve boundary is still OBJ_PALSLOT_COUNT, so banks the allocator
    hands out cannot overlap the object-event slots;
  - the forbidden `16 + PALSLOT_...` spelling has not come back;
  - a manifest blocker is not removed while the asset is still missing;
  - a borrowed reflection bank is only ever one of the four NPC ones, is
    decided by measured occupancy rather than by map, is given back on every
    path where a generic NPC arrives, and is released with the pool at map
    load;
  - the widest scene still fits in the budget, counting borrowable banks;
  - the virtual graphics registry is bounded, is reached only through the
    ARAUNA_VIRTUAL_GFX_* constants, and falls back for an id past its end;
  - a character on a virtual id has that id defined and in the table, has a
    map object using the matching OBJ_EVENT_GFX_VAR_x, and has that var
    written before objects spawn on every map that places it;
  - RAUL draws his own art, not the Magma grunt's;
  - the one-byte graphics id and NUM_OBJ_EVENT_GFX have not moved;
  - each Battle Circuit Master still sits on the internal Frontier Brain slot
    it was mapped to, draws its own front and overworld, and shares neither
    with anybody else;
  - the Silver and Gold tiers resolve to the same visible identity, because
    the three functions that answer "who is this" take no symbol input;
  - the streak thresholds that decide when a Master appears are untouched.

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

    # ---- borrowed reflection banks -------------------------------------
    def body_of(name: str) -> str:
        """The definition, not the forward declaration above it."""
        m = re.search(r"\b" + name + r"\([^;]*?\)\s*\n\{.*?\n\}\n",
                      movement, re.S)
        return m.group(0) if m else ""

    claim_body = body_of("AraunaClaimReflectionSlot")
    check(bool(claim_body), "the reflection-bank claim exists")
    named = set(re.findall(r"PALSLOT_\w+", claim_body))
    stray = named - {"PALSLOT_NPC_1_REFLECTION", "PALSLOT_NPC_4_REFLECTION"}
    check(not stray, "only the four NPC reflection banks can be borrowed",
          ", ".join(sorted(stray)) if stray else
          "PALSLOT_NPC_1_REFLECTION..PALSLOT_NPC_4_REFLECTION")

    idle_body = body_of("AraunaReflectionSlotIsIdle")
    check(bool(idle_body), "the idle test exists")
    # Measured per owner, never by map. A map name or the player's location
    # appearing here is the rule this work exists to refuse.
    by_map = re.findall(r"MAP_[A-Z0-9_]+|gSaveBlock1Ptr->location",
                        idle_body + claim_body)
    check(not by_map, "the idle test is measured, not decided by map",
          ", ".join(sorted(set(by_map))) if by_map else
          "reads gSprites and gObjectEvents only")
    check("gSprites[" in idle_body and "gObjectEvents[" in idle_body,
          "the idle test reads both live sprites and live object events")

    releases = len(re.findall(r"AraunaReleaseReflectionSlotForBase\(paletteSlot\)",
                              movement))
    assigns = len(re.findall(
        r"paletteSlot = graphicsInfo->paletteSlot;", movement))
    check(releases == assigns and assigns >= 3,
          "every path that hands out a base slot gives a loan back first",
          f"{releases} handbacks for {assigns} assignments")

    reserve = re.search(r"void FreeAndReserveObjectSpritePalettes\(void\)"
                        r".*?\n\}\n", movement, re.S)
    check(bool(reserve) and "AraunaResetReflectionClaims" in reserve.group(0),
          "loans are released when the palette pool is cleared")

    # ---- the widest scene still fits -----------------------------------
    # Two pool banks after weather, plus the four borrowable reflection banks,
    # plus the two special slots. Counted from the maps rather than assumed.
    pool_gfx = {c["object_event"].replace("OBJ_EVENT_GFX_", ""): c["name"]
                for c in cast
                if c.get("palette_slot") == POOL_SLOT and c.get("object_event")}
    worst, worst_map = 0, ""
    for ev in (ROOT / "data/maps").glob("*/events.inc"):
        here = {pool_gfx[g] for g in re.findall(
            r"object_event \d+, OBJ_EVENT_GFX_(\w+),",
            ev.read_text(encoding="utf-8")) if g in pool_gfx}
        if len(here) > worst:
            worst, worst_map = len(here), ev.parent.name
    budget = (16 - 12) - 2 + 4          # allocator pool less weather, plus loans
    check(worst <= budget,
          "the widest pooled scene fits in the palette budget",
          f"{worst_map} wants {worst}, budget is {budget}")

    # ---- the virtual graphics registry ---------------------------------
    events_h = (ROOT / "include/constants/event_objects.h").read_text(
        encoding="utf-8")
    virt_consts = dict(re.findall(
        r"#define (ARAUNA_VIRTUAL_GFX_\w+)\s+(.+)", events_h))
    declared_count = virt_consts.get("ARAUNA_VIRTUAL_GFX_COUNT", "").strip()
    vtable = re.search(r"sAraunaVirtualGraphicsInfo\[ARAUNA_VIRTUAL_GFX_COUNT\]"
                       r"\s*=\s*\{(.*?)\};", movement, re.S)
    entries = re.findall(r"\[(ARAUNA_VIRTUAL_GFX_\w+) - ARAUNA_VIRTUAL_GFX_START\]"
                         r"\s*=\s*&gObjectEventGraphicsInfo_(\w+),",
                         vtable.group(1) if vtable else "")
    check(vtable is not None, "the virtual graphics registry exists",
          f"{len(entries)} entries, ARAUNA_VIRTUAL_GFX_COUNT = {declared_count}")
    check(declared_count.isdigit() and int(declared_count) == len(entries),
          "the registry's declared size matches its entries",
          f"{declared_count} declared, {len(entries)} present")
    unknown = [c for c, _ in entries if c not in virt_consts]
    check(not unknown, "every registry entry is named by a constant",
          ", ".join(unknown) if unknown else "none")

    getter = re.search(r"AraunaGetVirtualGraphicsInfo\(u16 virtualId\)"
                       r".*?\n\}\n", movement, re.S)
    body = getter.group(0) if getter else ""
    check("ARRAY_COUNT(sAraunaVirtualGraphicsInfo)" in body
          and "OBJ_EVENT_GFX_NINJA_BOY" in body,
          "an id past the end of the registry falls back instead of reading on")

    dispatch = re.search(r"GetObjectEventGraphicsInfo\(u8 graphicsId\)"
                         r".*?\n\}\n", movement, re.S)
    dbody = dispatch.group(0) if dispatch else ""
    check("ARAUNA_VIRTUAL_GFX_START" in dbody
          and "AraunaGetVirtualGraphicsInfo" in dbody,
          "the dispatch reaches the registry by range, not by name")
    named_here = [c for c in virt_consts
                  if c not in ("ARAUNA_VIRTUAL_GFX_START",
                               "ARAUNA_VIRTUAL_GFX_COUNT") and c in dbody]
    check(not named_here, "no character is hardcoded in the dispatch",
          ", ".join(named_here) if named_here else "none")

    # ---- characters on a virtual id ------------------------------------
    scripts_by_map = {p.parent.name: p.read_text(encoding="utf-8")
                      for p in (ROOT / "data/maps").glob("*/scripts.inc")}
    for c in cast:
        vid = c.get("virtual_graphics_id")
        if not vid:
            continue
        check(vid in virt_consts, f"{c['name']}'s virtual id is defined", vid)
        check(vid in [e for e, _ in entries],
              f"{c['name']}'s virtual id is in the registry")
        gfx_var = c.get("object_event", "")
        check(gfx_var.startswith("OBJ_EVENT_GFX_VAR_"),
              f"{c['name']} is placed through an object gfx var", gfx_var)
        var_name = gfx_var.replace("OBJ_EVENT_GFX_VAR_", "VAR_OBJ_GFX_ID_")
        # Every map that places this object must name the character in the var
        # before the map spawns anything -- or be a decoration room, which
        # rewrites the same var from the save on entry.
        unset = []
        for ev in (ROOT / "data/maps").glob("*/events.inc"):
            text = ev.read_text(encoding="utf-8")
            for line in text.splitlines():
                if f"OBJ_EVENT_GFX_VAR_{gfx_var[-1]}," not in line:
                    continue
                if "FLAG_DECORATION_" in line:
                    continue
                script = scripts_by_map.get(ev.parent.name, "")
                if f"setvar {var_name}, {vid}" not in script:
                    unset.append(ev.parent.name)
        check(not unset, f"{c['name']}'s var is set before his maps spawn",
              ", ".join(sorted(set(unset))) if unset else "all three maps")

        body = blocks.get(c.get("graphics_info", ""), "")
        pic = re.search(r"\.images = (\w+),", body)
        want = f"sPicTable_{c.get('graphics_info', '')}"
        check(bool(pic) and pic.group(1) == want,
              f"{c['name']} draws his own art", pic.group(1) if pic else "none")

    # ---- the Battle Circuit Masters -------------------------------------
    #
    # The Masters are a visual layer over the inherited Frontier Brains. The
    # engine keeps seeing TRAINER_ANABEL and OBJ_EVENT_GFX_ANABEL; the player
    # sees MAIRA. What has to stay true is that the internal slot never moves,
    # that the art on it belongs to exactly one Master, and that Silver and
    # Gold cannot end up looking like different people.
    frontier = (ROOT / "src/frontier_util.c").read_text(encoding="utf-8")
    trainers_h = (ROOT / "include/constants/trainers.h").read_text(encoding="utf-8")
    trainer_data = (ROOT / "src/data/trainers.h").read_text(encoding="utf-8")
    front_decl = (ROOT / "src/data/graphics/trainers.h").read_text(encoding="utf-8")

    brain_gfx = dict(re.findall(
        r"\[FRONTIER_FACILITY_(\w+)\]\s*=\s*\{OBJ_EVENT_GFX_(\w+),", frontier))
    brain_ids = dict(re.findall(
        r"\[FRONTIER_FACILITY_(\w+)\]\s*=\s*TRAINER_(\w+),", frontier))
    masters = [c for c in cast if c.get("internal_trainer")]
    for c in masters:
        internal = c["internal_trainer"].replace("TRAINER_", "")
        gfx = c["object_event"].replace("OBJ_EVENT_GFX_", "")
        check(gfx == internal,
              f"{c['name']} still stands on the {internal} object slot", gfx)
        check(internal in brain_ids.values(),
              f"{c['name']}'s internal trainer is still a Frontier Brain",
              c["internal_trainer"])
        check(gfx in brain_gfx.values(),
              f"{c['name']}'s object slot is still the facility's brain graphic")
        # And on the right facility: the Tower's brain has to be the Tower's
        # Master, or Silver and Gold would hand the player somebody else.
        key = c.get("facility", "").replace("Battle ", "").upper()
        check(brain_ids.get(key) == internal
              and brain_gfx.get(key) == gfx,
              f"{c['name']} is the {c.get('facility')}'s Master",
              f"{key} -> {brain_ids.get(key)} / {brain_gfx.get(key)}")
        # The front has to be this Master's and nobody else's.
        pic = c["trainer_pic"]
        users = re.findall(rf"\.trainerPic = {re.escape(pic)}\b", trainer_data)
        check(len(users) == 1, f"{c['name']}'s trainer pic has one owner",
              f"{len(users)} trainers use {pic}")
        # Not just "the file is mentioned somewhere" -- the symbol the ROM
        # links for this trainer pic has to be the one built from it.
        stem = Path(c["front"]).stem
        camel = "".join(part.capitalize() for part in stem.split("_"))
        linked = re.search(rf'gTrainerFrontPic_{camel}\[\]\s*=\s*INCGFX_U32\("([^"]+)"',
                           front_decl)
        check(bool(linked) and linked.group(1) == c["front"],
              f"{c['name']}'s front file is the one the ROM links",
              linked.group(1) if linked else "no gTrainerFrontPic_" + camel)

    if masters:
        pics = [c["trainer_pic"] for c in masters]
        check(len(set(pics)) == len(pics),
              "no two Circuit Masters share a trainer pic")
        fronts = [c["front"] for c in masters]
        check(len(set(fronts)) == len(fronts),
              "no two Circuit Masters share a front file")

    # Silver and Gold pick different parties and different words. They must not
    # pick a different person: these three read sFrontierBrainTrainerIds by
    # facility alone, and a symbol lookup creeping in here is what would make
    # one tier show somebody else.
    for fn in ("GetFrontierBrainTrainerPicIndex", "GetFrontierBrainTrainerClass",
               "CopyFrontierBrainTrainerName"):
        m = re.search(rf"\b{fn}\([^;]*?\)\s*\n\{{.*?\n\}}\n", frontier, re.S)
        body = m.group(0) if m else ""
        check(bool(body) and "sFrontierBrainTrainerIds" in body
              and "GetFronterBrainSymbol" not in body,
              f"{fn} answers the same for Silver and Gold",
              "reads the facility only" if body else "not found")

    # The thresholds that decide when a Master turns up are mechanics, not art.
    streaks = re.search(r"sFrontierBrainStreakAppearances\[NUM_FRONTIER_FACILITIES\]\[4\]"
                        r"\s*=\s*\{(.*?)\};", frontier, re.S)
    rows = re.findall(r"\{\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\}",
                      streaks.group(1) if streaks else "")
    check(rows == [("35","70","35","1"), ("4","9","5","0"), ("21","42","21","1"),
                   ("28","56","28","1"), ("21","42","21","1"), ("28","140","56","1"),
                   ("21","70","35","0")],
          "the Silver and Gold streak thresholds are unchanged",
          f"{len(rows)} rows")

    # ---- the id space itself -------------------------------------------
    check("#define NUM_OBJ_EVENT_GFX                        239" in events_h,
          "NUM_OBJ_EVENT_GFX has not grown")
    field = (ROOT / "include/global.fieldmap.h").read_text(encoding="utf-8")
    check("u8 graphicsId;" in field,
          "an object event still stores a one-byte graphics id")

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

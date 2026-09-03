#!/usr/bin/env python3
"""Keep the two Arauna factions looking like themselves.

CONSORCIO HORIZONTE and the LEMBRANTES are worn by the Emerald Team Aqua and
Team Magma object-event slots. That reuse is deliberate -- it is what makes a
hundred and twelve inherited encounters follow Arauna's factions without
touching a single map script -- and it is also what makes the wiring easy to
break silently: the symbols still say Aqua and Magma, so a graphic or a front
sliding back to vanilla art reads as perfectly normal in a diff.

So this does not look for the words. Internal names are expected to stay. It
checks the visual wiring instead:

  - each of the four slots draws the faction art the manifest names, from the
    graphics info the engine actually indexes for that OBJ_EVENT_GFX;
  - each carries its own palette tag, shared with nobody -- the generic NPC
    ramps those slots used to borrow belong to about sixty other people, and
    quantising a faction into one is how the art was lost before;
  - the two genders of a faction are not the same art or the same palette,
    and neither are the two factions;
  - every battled faction trainer's front is the file the manifest names, and
    those fronts serve faction trainers only;
  - the visible trainer class and trainer names are the Arauna ones;
  - RAUL, who used to wear the Lembrante grunt graphic, does not wear it again.

Nothing matches on line numbers.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tools/arauna/character_manifest.json"
INFO = ROOT / "src/data/object_events/object_event_graphics_info.h"
POINTERS = ROOT / "src/data/object_events/object_event_graphics_info_pointers.h"
GFX_DECL = ROOT / "src/data/object_events/object_event_graphics.h"
PIC_TABLES = ROOT / "src/data/object_events/object_event_pic_tables.h"
TRAINER_GFX = ROOT / "src/data/graphics/trainers.h"
TRAINER_DATA = ROOT / "src/data/trainers.h"
CLASS_NAMES = ROOT / "src/data/text/trainer_class_names.h"

# The mapping the story settled on, and the only one this gate accepts.
CANON = {
    "HORIZONTE_M": ("OBJ_EVENT_GFX_AQUA_MEMBER_M",  "CONSORCIO HORIZONTE"),
    "HORIZONTE_F": ("OBJ_EVENT_GFX_AQUA_MEMBER_F",  "CONSORCIO HORIZONTE"),
    "LEMBRANTE_M": ("OBJ_EVENT_GFX_MAGMA_MEMBER_M", "LEMBRANTES"),
    "LEMBRANTE_F": ("OBJ_EVENT_GFX_MAGMA_MEMBER_F", "LEMBRANTES"),
}
VISIBLE_CLASS = {"TRAINER_CLASS_TEAM_AQUA": "HORIZONTE",
                 "TRAINER_CLASS_TEAM_MAGMA": "LEMBRANTE"}


def main() -> int:
    cast = json.loads(MANIFEST.read_text(encoding="utf-8"))["characters"]
    by_name = {c["name"]: c for c in cast}
    info = INFO.read_text(encoding="utf-8")
    blocks = dict(re.findall(
        r"gObjectEventGraphicsInfo_(\w+) = \{(.*?)\n\};", info, re.S))
    pointers = dict(re.findall(
        r"\[OBJ_EVENT_GFX_(\w+)\] =\s*&gObjectEventGraphicsInfo_(\w+),",
        POINTERS.read_text(encoding="utf-8")))
    gfx_decl = GFX_DECL.read_text(encoding="utf-8")
    pic_tables = PIC_TABLES.read_text(encoding="utf-8")
    trainer_gfx = TRAINER_GFX.read_text(encoding="utf-8")
    trainer_data = TRAINER_DATA.read_text(encoding="utf-8")

    results: list[tuple[bool, str, str]] = []

    def check(ok: bool, label: str, detail: str = "") -> None:
        results.append((ok, label, detail))

    missing = [n for n in CANON if n not in by_name]
    check(not missing, "all four faction archetypes are in the manifest",
          ", ".join(missing) if missing else "HORIZONTE M/F, LEMBRANTE M/F")
    if missing:
        report(results)
        return 1

    art, palettes, fronts = {}, {}, {}
    for name, (gfx_const, faction) in CANON.items():
        entry = by_name[name]
        check(entry.get("object_event") == gfx_const,
              f"{name} is wired to {gfx_const}", str(entry.get("object_event")))
        check(entry.get("faction") == faction,
              f"{name} belongs to {faction}", str(entry.get("faction")))

        # The engine reaches the art through the pointer table, so that is the
        # path this follows rather than trusting the manifest's own name.
        gfx = gfx_const.replace("OBJ_EVENT_GFX_", "")
        linked_info = pointers.get(gfx)
        check(linked_info == entry.get("graphics_info"),
              f"{name}'s graphics id points at the graphics info the manifest names",
              f"{gfx_const} -> {linked_info}")

        body = blocks.get(linked_info or "", "")
        want_tag = entry["palette_tag"]
        tag = re.search(r"\.paletteTag\s*=\s*(\w+)", body)
        check(bool(tag) and tag.group(1) == want_tag,
              f"{name} carries its own palette tag",
              tag.group(1) if tag else "none")
        palettes[name] = tag.group(1) if tag else None

        # A faction palette shared with anybody else is the failure that put
        # this art into the generic NPC ramps in the first place.
        sharers = [other for other, b in blocks.items()
                   if re.search(rf"\.paletteTag\s*=\s*{re.escape(want_tag)}\b", b)]
        check(len(sharers) == 1, f"{name}'s palette belongs to nobody else",
              ", ".join(sorted(sharers)))

        table = re.search(rf"sPicTable_{linked_info}\[\]\s*=\s*\{{(.*?)\}};",
                          pic_tables, re.S)
        pic_sym = re.findall(r"overworld_frame\((\w+),", table.group(1)) if table else []
        check(len(set(pic_sym)) == 1 and len(pic_sym) == 9,
              f"{name} draws nine frames from one sheet",
              f"{len(pic_sym)} frames from {sorted(set(pic_sym))}")
        art[name] = pic_sym[0] if pic_sym else None

        declared = re.search(rf'{art[name]}\[\]\s*=\s*INCGFX_U32\("([^"]+)"', gfx_decl)
        check(bool(declared) and declared.group(1) == entry["overworld"],
              f"{name}'s sheet is the file the ROM links",
              declared.group(1) if declared else "not declared")

        # The front: linked symbol built from the file the manifest names.
        stem = Path(entry["front"]).stem
        camel = "".join(part.capitalize() for part in stem.split("_"))
        linked = re.search(rf'gTrainerFrontPic_{camel}\[\]\s*=\s*INCGFX_U32\("([^"]+)"',
                           trainer_gfx)
        check(bool(linked) and linked.group(1) == entry["front"],
              f"{name}'s front is the file the ROM links",
              linked.group(1) if linked else f"no gTrainerFrontPic_{camel}")
        fronts[name] = entry["front"]

        # And that front serves faction trainers only.
        pic = entry["trainer_pic"]
        users = re.findall(
            rf"\.trainerClass = (\w+),\s*\n\s*\.encounterMusic_gender[^\n]*\n\s*"
            rf"\.trainerPic = {re.escape(pic)}\b", trainer_data)
        stray = sorted({c for c in users} - set(VISIBLE_CLASS))
        check(not stray, f"{name}'s front is only used by faction trainers",
              f"{len(users)} trainers" + (f", also {stray}" if stray else ""))

    # Two genders of one faction, and the two factions, must stay distinct.
    for a, b, what in (("HORIZONTE_M", "HORIZONTE_F", "the two HORIZONTE variants"),
                       ("LEMBRANTE_M", "LEMBRANTE_F", "the two LEMBRANTE variants"),
                       ("HORIZONTE_M", "LEMBRANTE_M", "the two factions")):
        check(art[a] != art[b] and palettes[a] != palettes[b]
              and fronts[a] != fronts[b],
              f"{what} are not the same character",
              f"{art[a]}/{palettes[a]} vs {art[b]}/{palettes[b]}")

    names = CLASS_NAMES.read_text(encoding="utf-8")
    for cls, want in VISIBLE_CLASS.items():
        shown = re.search(rf"\[{cls}\] = _\(\"([^\"]*)\"\)", names)
        check(bool(shown) and want in shown.group(1),
              f"{cls} shows a faction name in battle",
              shown.group(1) if shown else "not found")

    # RAUL wore the Lembrante grunt graphic until the virtual registry gave him
    # his own; this refuses to let him back onto it.
    raul = by_name.get("RAUL")
    if raul:
        check(raul.get("object_event") != "OBJ_EVENT_GFX_MAGMA_MEMBER_M"
              and raul.get("graphics_info") != "MagmaMemberM"
              and raul.get("palette_tag") != palettes["LEMBRANTE_M"],
              "RAUL is not wearing the LEMBRANTE grunt graphic again",
              f"{raul.get('object_event')} / {raul.get('graphics_info')}")

    return report(results)


def report(results: list[tuple[bool, str, str]]) -> int:
    width = max(len(l) for _, l, _ in results)
    failed = sum(1 for ok, _, _ in results if not ok)
    for ok, label, detail in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<{width}}"
              + (f"  -- {detail}" if detail else ""))
    print(f"\n{len(results) - failed}/{len(results)} faction identity checks passed")
    if failed:
        print("Arauna faction visual identity: FAIL", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

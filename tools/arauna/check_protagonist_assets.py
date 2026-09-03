#!/usr/bin/env python3
"""Keep the protagonist's replacement honest while most of it is still unbuilt.

The player is not an NPC with one 144x32 sheet. Each avatar state has its own
frame size, its own pic table and its own animation table, and NORMAL alone
spans two sheets -- walking and running -- that share a single sixteen-colour
bank. Replacing the protagonist therefore happens one state at a time, over
several passes, with most states still wearing inherited Emerald art in
between. That long half-finished stretch is what this guards.

It refuses four things:

  - a state declared READY whose art is not actually installed, the wrong
    size, or drawing from a sheet the engine does not read;
  - a state declared MISSING or PARTIAL that has nevertheless been wired to
    Arauna art -- a half-replaced state, the transition break the plan calls
    worse than waiting;
  - a NORMAL whose two sheets do not share one palette, which renders the
    run cycle in the walk cycle's colours;
  - the player and CIRO ending up on the same art, or one gender's graphics
    info leaking into the other's slot.

Every engine number is read from the source the linker reads -- the graphics
info, the pic table, the INCGFX line, the PNG header -- so the manifest can
never drift from the build. The manifest supplies only asset readiness.
"""
from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tools/arauna/character_manifest.json"
INFO = ROOT / "src/data/object_events/object_event_graphics_info.h"
POINTERS = ROOT / "src/data/object_events/object_event_graphics_info_pointers.h"
PIC_TABLES = ROOT / "src/data/object_events/object_event_pic_tables.h"
GFX_DECL = ROOT / "src/data/object_events/object_event_graphics.h"
AVATAR = ROOT / "src/field_player_avatar.c"

# The player's own banks. The exclusive pool the NPC work built is for NPCs;
# the player is preloaded into slot 0 and its reflection into slot 1, and a
# protagonist that ends up in the pool has lost its reflection and its
# weather handling with it.
PLAYER_SLOTS = {"PALSLOT_PLAYER", "PALSLOT_PLAYER_REFLECTION", "PALSLOT_NPC_SPECIAL"}
VANILLA_DIRS = ("people/brendan/", "people/may/")


def png_header(rel: str):
    data = (ROOT / rel).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{rel} is not a PNG")
    w, h, depth, color = struct.unpack(">IIBB", data[16:26])
    return w, h, depth, color


def png_palette(rel: str) -> list[tuple[int, int, int]]:
    """The PLTE chunk, read without a decoder."""
    data = (ROOT / rel).read_bytes()
    i = 8
    while i < len(data):
        (length,) = struct.unpack(">I", data[i:i + 4])
        kind = data[i + 4:i + 8]
        if kind == b"PLTE":
            raw = data[i + 8:i + 8 + length]
            return [tuple(raw[j:j + 3]) for j in range(0, len(raw), 3)]
        i += 12 + length
    return []


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    states = manifest.get("protagonist_states")
    surfaces = manifest.get("protagonist_battle_surfaces")
    info = INFO.read_text(encoding="utf-8")
    pointers = dict(re.findall(
        r"\[OBJ_EVENT_GFX_(\w+)\] =\s*&gObjectEventGraphicsInfo_(\w+),",
        POINTERS.read_text(encoding="utf-8")))
    blocks = dict(re.findall(
        r"gObjectEventGraphicsInfo_(\w+) = \{(.*?)\n\};", info, re.S))
    pic_src = PIC_TABLES.read_text(encoding="utf-8")
    decl = GFX_DECL.read_text(encoding="utf-8")
    avatar = AVATAR.read_text(encoding="utf-8")

    results: list[tuple[bool, str, str]] = []

    def check(ok, label, detail=""):
        results.append((bool(ok), label, detail))

    check(states is not None, "the manifest declares the player's avatar states",
          f"{len(states)} states" if states else "protagonist_states missing")
    check(surfaces is not None, "the manifest declares the player's battle surfaces",
          f"{len(surfaces)} surfaces" if surfaces else "missing")
    if not states or not surfaces:
        return report(results)

    def field(body, name):
        m = re.search(rf"\.{name}\s*=\s*([^,\n]+),", body)
        return m.group(1).strip() if m else None

    def sheets_of(gfx_const):
        """Every PNG the engine draws this state from, via its pic table."""
        short = gfx_const.replace("OBJ_EVENT_GFX_", "")
        sym = pointers.get(short)
        body = blocks.get(sym or "", "")
        images = field(body, "images")
        m = re.search(rf"{re.escape(images or '')}\[\]\s*=\s*\{{(.*?)\n\}};",
                      pic_src, re.S)
        pics = re.findall(r"overworld_frame\((\w+),", m.group(1)) if m else []
        files = []
        for pic in dict.fromkeys(pics):
            d = re.search(rf"\b{pic}\[\]\s*=\s*INCGFX_U32\(\"([^\"]+)\"", decl)
            if d:
                files.append(d.group(1))
        return sym, body, images, len(pics), files

    # The engine's own gender table is the authority on which id is whose.
    male_ids, female_ids = set(), set()
    table = re.search(r"sPlayerAvatarGfxIds\[\]\[GENDER_COUNT\] =\s*\{(.*?)\n\};",
                      avatar, re.S)
    if table:
        for m, f in re.findall(r"\{(OBJ_EVENT_GFX_\w+),\s*(OBJ_EVENT_GFX_\w+)\}",
                               table.group(1)):
            male_ids.add(m)
            female_ids.add(f)
    check(bool(male_ids) and bool(female_ids),
          "the player avatar gender table was found in the engine",
          f"{len(male_ids)} male ids, {len(female_ids)} female ids")

    seen_art: dict[str, str] = {}
    for entry in states:
        name = entry["state"]
        status = entry["status"]
        check(status in ("READY", "PARTIAL", "MISSING", "REFERENCE_ONLY"),
              f"{name} declares a known status", status)

        for gender, key in (("male", "gfx_male"), ("female", "gfx_female")):
            gfx = entry[key]
            sym, body, images, frames, files = sheets_of(gfx)
            check(sym is not None and bool(body),
                  f"{name} {gender} resolves through the pointer table",
                  f"{gfx} -> {sym}")
            if not body:
                continue

            # The player's palette must stay the player's. DECORATING is drawn
            # by the decoration menu rather than the field, so it sits on the
            # special NPC slot in vanilla too.
            slot = field(body, "paletteSlot")
            check(slot in PLAYER_SLOTS,
                  f"{name} {gender} stays on a player palette slot", str(slot))

            # No state may be half-replaced.
            arauna = [f for f in files
                      if not any(v in f for v in VANILLA_DIRS)]
            vanilla = [f for f in files if any(v in f for v in VANILLA_DIRS)]
            if status == "READY":
                check(files and not vanilla,
                      f"{name} {gender} draws only Arauna art", ", ".join(files))
                for f in files:
                    exists = (ROOT / f).exists()
                    check(exists, f"{name} {gender} sheet {Path(f).name} is on disk", f)
                    if not exists:
                        continue
                    w, h, depth, color = png_header(f)
                    fw = int(field(body, "width") or 0)
                    fh = int(field(body, "height") or 0)
                    check(fw and fh and w % fw == 0 and h % fh == 0,
                          f"{name} {gender} {Path(f).name} tiles into "
                          f"{fw}x{fh} frames", f"{w}x{h}")
                    check(depth == 4 and color == 3,
                          f"{name} {gender} {Path(f).name} is 4bpp indexed",
                          f"depth {depth} colour type {color}")
            else:
                check(not arauna,
                      f"{name} {gender} is not half-replaced while {status}",
                      ", ".join(arauna) if arauna else
                      f"still on {', '.join(Path(f).parent.name for f in files) or 'no sheet'}")

            # A state whose pic table spans several sheets renders all of them
            # through one palette, so those sheets must agree colour for colour.
            on_disk = [f for f in files if (ROOT / f).exists()]
            if len(on_disk) > 1:
                pals = {f: tuple(png_palette(f)[:16]) for f in on_disk}
                same = len(set(pals.values())) == 1
                check(same,
                      f"{name} {gender} sheets share one 16-colour palette",
                      f"{len(on_disk)} sheets, "
                      + ("identical" if same else "palettes differ"))

            # Two genders, two sets of art.
            for f in files:
                other = seen_art.get(f)
                check(other is None or other == gfx,
                      f"{name} {gender} does not wear another slot's sheet",
                      f"{Path(f).name} also used by {other}" if other else Path(f).name)
                seen_art.setdefault(f, gfx)

            if male_ids and female_ids:
                pool = male_ids if gender == "male" else female_ids
                wrong = female_ids if gender == "male" else male_ids
                # DECORATING is not in the avatar table; it is created directly.
                if gfx in pool or gfx in wrong:
                    check(gfx in pool and gfx not in wrong,
                          f"{name} {gender} is on the {gender} side of the "
                          f"engine's gender table", gfx)

    # CIRO wears the RIVAL slots. The player must never reach that art, and
    # CIRO must never reach the player's.
    ciro = {c["name"]: c for c in manifest["characters"]
            if c["name"].startswith("CIRO")}
    ciro_art = {c.get("overworld") for c in ciro.values()}
    ciro_info = {c.get("graphics_info") for c in ciro.values()}
    player_info = set()
    for entry in states:
        for key in ("gfx_male", "gfx_female"):
            sym, _, _, _, files = sheets_of(entry[key])
            player_info.add(sym)
            for f in files:
                check(f not in ciro_art,
                      f"{entry['state']} does not draw CIRO's art", Path(f).name)
    clash = player_info & ciro_info
    check(not clash, "no player state shares CIRO's graphics info",
          ", ".join(sorted(clash)) if clash else
          f"{len(player_info)} player infos, {len(ciro_info)} CIRO infos")

    for surface in surfaces:
        label = surface["surface"]
        if surface["status"] == "READY":
            for gender in ("male", "female"):
                f = surface[gender]
                check((ROOT / f).exists(), f"{label} {gender} art is on disk", f)
        else:
            check(True, f"{label} is declared {surface['status']}",
                  "not claimed as integrated")

    return report(results)


def report(results) -> int:
    width = max(len(l) for _, l, _ in results)
    failed = sum(1 for ok, _, _ in results if not ok)
    for ok, label, detail in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<{width}}"
              + (f"  -- {detail}" if detail else ""))
    print(f"\n{len(results) - failed}/{len(results)} protagonist asset checks passed")
    if failed:
        print("Arauna protagonist asset audit: FAIL", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

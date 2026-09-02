#!/usr/bin/env python3
"""Hold the line on species that inherited a vanilla slot's visual quirks.

Three Emerald species draw themselves differently per individual, and Arauna
put its own creatures in two of those slots.

ESTALAGMITE sits in SPECIES_UNOWN. Unown's twenty-eight letters are an engine
detail of the slot, not something Arauna uses, and the twenty-eight form
folders deliberately hold one identical picture. That is easy to mistake for
missing art, and equally easy to undo by making the Pokedex read the stored
personality again, so both halves are pinned here.

POSTE sits in SPECIES_SPINDA. Spinda's spot overlay stamps four
personality-placed marks into the decompressed front pic on every path that
draws it, and on POSTE it produced cyan speckle down the shaft that differed
from one specimen to the next. The overlay is off; this refuses to let it
come back.

TUIM sits in SPECIES_CASTFORM and is deliberately untouched until its four
weather-form designs exist. The guard here runs the other way: it fails if
Castform's machinery is quietly disabled, because deferring it means leaving
it exactly as it is.

Nothing below matches on line numbers. The checks read structures, symbols
and call relationships, so ordinary edits to these files do not trip them.
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POKEDEX_C = ROOT / "src/pokedex.c"
POKEMON_C = ROOT / "src/pokemon.c"
GLOBAL_H = ROOT / "include/global.h"
BATTLE_UTIL_C = ROOT / "src/battle_util.c"
MAPPING = ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
UNOWN_DIR = ROOT / "graphics/pokemon/unown"

UNOWN_FORMS = list("abcdefghijklmnopqrstuvwxyz") + ["exclamation_mark",
                                                   "question_mark"]
SURFACES = ("front.png", "back.png", "normal.pal", "shiny.pal", "icon.png",
            "anim_front.png")


def body_of(text: str, signature: str) -> str | None:
    """The braces of one function, found by its name rather than its place."""
    m = re.search(rf"\n[\w \*]*\b{re.escape(signature)}\s*\([^)]*\)\s*\{{", text)
    if not m:
        return None
    i = text.index("{", m.start())
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j]
    return None


def main() -> int:
    results: list[tuple[bool, str, str]] = []

    def check(ok: bool, label: str, detail: str = "") -> None:
        results.append((ok, label, detail))

    mapping = {r["species_constant"]: r
               for r in csv.DictReader(MAPPING.open(encoding="utf-8"))}

    # --- ESTALAGMITE -------------------------------------------------------
    row = mapping.get("SPECIES_UNOWN")
    check(row is not None and row["full_name"] == "Estalagmite",
          "Estalagmite still occupies SPECIES_UNOWN",
          row["full_name"] if row else "not mapped")

    digests = {}
    for surface in SURFACES:
        seen = set()
        missing = []
        for form in UNOWN_FORMS:
            p = UNOWN_DIR / form / surface
            if not p.is_file():
                missing.append(form)
                continue
            seen.add(hashlib.sha256(p.read_bytes()).hexdigest())
        digests[surface] = (len(seen), missing)
    single = all(n == 1 and not miss for n, miss in digests.values())
    check(single, "the 28 Unown form folders hold one identical design",
          ", ".join(f"{s}:{n}" for s, (n, _) in digests.items()))

    pokedex = POKEDEX_C.read_text(encoding="utf-8")
    body = body_of(pokedex, "GetPokedexMonPersonality")
    check(body is not None, "GetPokedexMonPersonality is still the only "
                            "place the Pokedex picks a personality")
    if body is not None:
        reads = [f for f in ("unownPersonality", "spindaPersonality")
                 if f in body]
        check(not reads,
              "the Pokedex draws the canonical representation",
              f"still reads {', '.join(reads)}" if reads else "reads nothing")

    # No form selector may appear: vanilla never had one and Estalagmite must
    # not gain one. The Pokedex's A-Z name search is unrelated and stays.
    selector = re.findall(r"SPECIES_UNOWN", pokedex)
    check(not selector, "no Unown form UI in the Pokedex",
          f"{len(selector)} SPECIES_UNOWN references" if selector else "none")

    # --- POSTE -------------------------------------------------------------
    row = mapping.get("SPECIES_SPINDA")
    check(row is not None and row["full_name"] == "Poste",
          "Poste still occupies SPECIES_SPINDA",
          row["full_name"] if row else "not mapped")

    pokemon = POKEMON_C.read_text(encoding="utf-8")
    spots = body_of(pokemon, "DrawSpindaSpots")
    check(spots is not None, "DrawSpindaSpots still exists")
    if spots is not None:
        check("DRAW_SPINDA_SPOTS" not in spots,
              "the Spinda spot overlay does not run for Poste",
              "macro is invoked again" if "DRAW_SPINDA_SPOTS" in spots else "off")

    # --- save compatibility ------------------------------------------------
    glob = GLOBAL_H.read_text(encoding="utf-8")
    fields = [f for f in ("unownPersonality", "spindaPersonality")
              if re.search(rf"\b{f}\b", glob)]
    check(len(fields) == 2, "both personality fields stay in the save",
          ", ".join(fields))
    check("spindaPersonality" in pokemon and "unownPersonality" in pokemon,
          "both are still written when a species is first seen")

    # --- TUIM is deferred, so its machinery must remain ---------------------
    forecast = BATTLE_UTIL_C.read_text(encoding="utf-8")
    check("ABILITY_FORECAST" in forecast and "SPECIES_CASTFORM" in forecast,
          "Tuim's Castform behaviour is left intact (deferred, art pending)")

    width = max(len(label) for _, label, _ in results)
    failed = 0
    for ok, label, detail in results:
        if not ok:
            failed += 1
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<{width}}"
              + (f"  -- {detail}" if detail else ""))
    print(f"\n{len(results) - failed}/{len(results)} special-species checks passed")
    if failed:
        print("Arauna special species: FAIL", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

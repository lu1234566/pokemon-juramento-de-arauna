#!/usr/bin/env python3
"""Apply the Arauna base stats and abilities from the project's pokedex.

Stats are copied straight across: the dex already carries a hand-authored
spread per creature, all inside the u8 the field allows.

Abilities take a deliberately conservative route. Creating new abilities means
new effects in the battle engine, which is where a hack breaks in ways a
playthrough only finds late. Instead each of the 46 Arauna abilities claims one
existing Gen 3 slot whose effect already carries it, and that slot's visible
name and description are rewritten. The player reads Arauna's identity while
the behaviour stays code that shipped and was tested in 2005. The mapping lives
in data/text/arauna/ability_map.json, one line per ability, so any pairing can
be re-judged without touching this script.

Evolutions are deliberately untouched.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
INFO_H = ROOT / "src" / "data" / "pokemon" / "species_info.h"
ABIL_H = ROOT / "src" / "data" / "text" / "abilities.h"
ABIL_MAP = ROOT / "data" / "text" / "arauna" / "ability_map.json"
STAT_FIELD = {"hp": "baseHP", "atk": "baseAttack", "def": "baseDefense",
              "spe": "baseSpeed", "spa": "baseSpAttack", "spd": "baseSpDefense"}
NAME_LIMIT = 12


def dex_to_species() -> dict[int, str]:
    dex = (ROOT / "include" / "constants" / "pokedex.h").read_text(encoding="utf-8")
    order = re.findall(r"^\s*NATIONAL_DEX_([A-Z0-9_]+),", dex[dex.index("enum {"):], re.M)
    known = set(re.findall(r"^#define\s+(SPECIES_[A-Z0-9_]+)\s+\d+",
                           (ROOT / "include" / "constants" / "species.h").read_text(encoding="utf-8"), re.M))
    out: dict[int, str] = {}
    for i, name in enumerate(order):
        if name != "NONE" and f"SPECIES_{name}" in known:
            out.setdefault(i, f"SPECIES_{name}")
    return out


def species_block(text: str, species: str) -> re.Match | None:
    # The final entry closes without a trailing comma, so the comma is optional.
    return re.search(rf"(\[{re.escape(species)}\]\s*=\s*\{{)(.*?)(\n    \}},?)", text, re.S)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pokedex", type=pathlib.Path)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dex = json.loads(args.pokedex.read_text(encoding="utf-8"))["pokemon"]
    abil = json.loads(ABIL_MAP.read_text(encoding="utf-8"))
    slots = dex_to_species()

    info = INFO_H.read_text(encoding="utf-8")
    statted = abilitied = 0
    unknown: set[str] = set()

    for entry in sorted(dex, key=lambda e: e["id"]):
        species = slots.get(entry["id"])
        if species is None:
            continue
        match = species_block(info, species)
        if not match:
            continue
        body = match.group(2)

        for key, field in STAT_FIELD.items():
            value = entry["stats"][key]
            body = re.sub(rf"(\.{field}\s*=\s*)\d+", rf"\g<1>{value}", body, count=1)

        picked = []
        for name in entry["abilities"]:
            if name in abil:
                picked.append(abil[name]["slot"])
            else:
                unknown.add(name)
        if picked:
            # Two distinct slots, or a single one padded with ABILITY_NONE.
            first = picked[0]
            second = picked[1] if len(picked) > 1 and picked[1] != first else "ABILITY_NONE"
            body = re.sub(r"(\.abilities\s*=\s*\{)[^}]*(\})",
                          lambda m: m.group(1) + f"{first}, {second}" + m.group(2), body, count=1)
            abilitied += 1

        info = info[:match.start(2)] + body + info[match.end(2):]
        statted += 1

    names = ABIL_H.read_text(encoding="utf-8")
    renamed = 0
    for pt, spec in abil.items():
        constant = spec["slot"].replace("ABILITY_", "")
        pattern = re.compile(rf'(\[ABILITY_{re.escape(constant)}\]\s*=\s*_\(")([^"]*)("\))')
        if pattern.search(names):
            names = pattern.sub(lambda m: m.group(1) + spec["en"] + m.group(3), names, count=1)
            renamed += 1

    # Rewrite each slot's description too: a renamed ability whose blurb still
    # describes the Emerald one reads as a bug.
    described = 0
    for pt, spec in abil.items():
        constant = spec["slot"].replace("ABILITY_", "")
        pointer = re.search(rf"\[ABILITY_{re.escape(constant)}\]\s*=\s*(s\w+Description)", names)
        if not pointer:
            continue
        symbol = pointer.group(1)
        body = re.compile(rf'(static const u8 {symbol}\[\] = _\(")([^"]*)("\);)')
        if body.search(names):
            names = body.sub(lambda m: m.group(1) + spec["description"] + m.group(3), names, count=1)
            described += 1

    if unknown:
        print("  abilities with no mapping:", sorted(unknown))
    if args.apply:
        INFO_H.write_text(info, encoding="utf-8")
        ABIL_H.write_text(names, encoding="utf-8")

    verb = "applied" if args.apply else "would apply"
    print(f"\n{statted} stat spreads and {abilitied} ability pairs {verb}; "
          f"{renamed} ability names and {described} descriptions rewritten.")
    return 1 if unknown else 0


if __name__ == "__main__":
    raise SystemExit(main())

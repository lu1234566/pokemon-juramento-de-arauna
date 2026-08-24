#!/usr/bin/env python3
"""Give the Emerald species slots Arauna names and types.

Driven by the sprite pack's manifest, keyed by National Dex number, so it
lands on the same slots the art did.

Three things the manifest and the Gen 3 engine disagree on, each resolved
explicitly rather than silently:

names       The charmap has no accented characters at all, and the project
            already writes its Portuguese place names unaccented
            (SERTAO DE DENTRO, VALE DO SILENCIO), so accents are stripped the
            same way.
length      POKEMON_NAME_LENGTH is 10 and 36 names are longer, up to 17. The
            field is part of the save layout, so widening it is not a casual
            change; names are shortened instead. Cutting at the hyphen alone
            collides 16 times -- Curupira-Anciao would become Curupira, which
            already exists -- so shortening keeps going until the result is
            unique, and every choice is written to an override table that can
            be hand-edited and re-applied.
fairy       The type does not exist in Gen 3. All 68 creatures carrying it
            also carry a second type, so the fairy slot collapses onto that
            one and they become mono-typed. Nothing is left typeless and the
            type chart is untouched; revisit if Fairy is ever added.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]
NAMES_H = ROOT / "src" / "data" / "text" / "species_names.h"
INFO_H = ROOT / "src" / "data" / "pokemon" / "species_info.h"
OVERRIDES = ROOT / "data" / "text" / "arauna" / "species_name_overrides.json"
NAME_LIMIT = 10


def unaccent(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text)
                   if unicodedata.category(c) != "Mn")


def dex_to_species() -> dict[int, str]:
    """National Dex number to the SPECIES_ constant holding that slot."""
    dex = (ROOT / "include" / "constants" / "pokedex.h").read_text(encoding="utf-8")
    body = dex[dex.index("enum {"):]
    order = re.findall(r"^\s*NATIONAL_DEX_([A-Z0-9_]+),", body, re.M)
    known = set(re.findall(r"^#define\s+(SPECIES_[A-Z0-9_]+)\s+\d+",
                           (ROOT / "include" / "constants" / "species.h").read_text(encoding="utf-8"), re.M))
    out = {}
    for i, name in enumerate(order):
        if name == "NONE":
            continue
        constant = f"SPECIES_{name}"
        if constant in known:
            out.setdefault(i, constant)
    return out


def shorten(name: str, taken: set[str]) -> str:
    """Fit the name in POKEMON_NAME_LENGTH while staying unique."""
    if len(name) <= NAME_LIMIT and name not in taken:
        return name
    head = name.split("-")[0]
    candidates = [head]
    # Keep the qualifier's first letters so siblings stay distinguishable.
    if "-" in name:
        qualifier = name.split("-", 1)[1]
        for keep in range(1, len(qualifier) + 1):
            candidates.append(f"{head}-{qualifier[:keep]}")
    candidates.append(name)
    for cand in candidates:
        # A truncation that lands on the hyphen reads as an unfinished word.
        cand = cand[:NAME_LIMIT].rstrip("-")
        if cand and cand not in taken:
            return cand
    stem = name[:NAME_LIMIT - 1]
    for n in range(2, 100):
        cand = f"{stem}{n}"[:NAME_LIMIT]
        if cand not in taken:
            return cand
    raise ValueError(f"cannot fit {name!r}")


def build_names(mon: list[dict]) -> dict[int, str]:
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}
    taken: set[str] = set()
    chosen: dict[int, str] = {}
    # Names that already fit claim their spelling first, so a shortened
    # sibling never steals it.
    for entry in sorted(mon, key=lambda e: e["id"]):
        plain = unaccent(entry["name"])
        if str(entry["id"]) in overrides:
            continue
        if len(plain) <= NAME_LIMIT and plain not in taken:
            chosen[entry["id"]] = plain
            taken.add(plain)
    for entry in sorted(mon, key=lambda e: e["id"]):
        if entry["id"] in chosen:
            continue
        forced = overrides.get(str(entry["id"]))
        name = unaccent(forced) if forced else shorten(unaccent(entry["name"]), taken)
        chosen[entry["id"]] = name
        taken.add(name)
    return chosen


def build_types(entry: dict) -> tuple[str, str]:
    kinds = [t.upper() for t in entry["types"]]
    if "FAIRY" in kinds:
        rest = [t for t in kinds if t != "FAIRY"]
        kinds = rest or ["NORMAL"]
    first = f"TYPE_{kinds[0]}"
    second = f"TYPE_{kinds[1]}" if len(kinds) > 1 else first
    return first, second


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", type=pathlib.Path)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    mon = json.loads(args.manifest.read_text(encoding="utf-8"))["pokemon"]
    slots = dex_to_species()
    names = build_names(mon)

    names_text = NAMES_H.read_text(encoding="utf-8")
    info_text = INFO_H.read_text(encoding="utf-8")
    renamed = retyped = missed = 0
    shortened: dict[str, str] = {}

    for entry in sorted(mon, key=lambda e: e["id"]):
        species = slots.get(entry["id"])
        if species is None:
            missed += 1
            continue
        name = names[entry["id"]]
        if name != unaccent(entry["name"]):
            shortened[str(entry["id"])] = name

        pattern = re.compile(rf'(\[{re.escape(species)}\]\s*=\s*_\(")([^"]*)("\))')
        if pattern.search(names_text):
            names_text = pattern.sub(lambda m: m.group(1) + name + m.group(3), names_text, count=1)
            renamed += 1

        first, second = build_types(entry)
        block = re.compile(rf'(\[{re.escape(species)}\]\s*=\s*\{{.*?\.types\s*=\s*\{{\s*)([^}}]*?)(\s*\}})', re.S)
        if block.search(info_text):
            info_text = block.sub(lambda m: m.group(1) + f"{first}, {second}" + m.group(3),
                                  info_text, count=1)
            retyped += 1

    for name, count in ((n, list(names.values()).count(n)) for n in set(names.values())):
        if count > 1:
            print(f"  duplicate name after shortening: {name!r} x{count}")

    if args.apply:
        NAMES_H.write_text(names_text, encoding="utf-8")
        INFO_H.write_text(info_text, encoding="utf-8")
        OVERRIDES.parent.mkdir(parents=True, exist_ok=True)
        if not OVERRIDES.exists():
            OVERRIDES.write_text(json.dumps(shortened, ensure_ascii=False, indent=2,
                                            sort_keys=True) + "\n", encoding="utf-8")
            print(f"  seeded {OVERRIDES.relative_to(ROOT)} with {len(shortened)} shortened names")

    verb = "applied" if args.apply else "would apply"
    print(f"\n{renamed} names and {retyped} type pairs {verb}; "
          f"{missed} dex slots had no species; {len(shortened)} names shortened.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

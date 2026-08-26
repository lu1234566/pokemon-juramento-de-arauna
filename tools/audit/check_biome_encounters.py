#!/usr/bin/env python3
"""Ask whether what lives on a map belongs to the biome the map now wears.

Every route and settlement was given a biome, and the biome is drawn - the
grass, the leaves, the ground. What walks around in it was never touched: the
wild tables are still Hoenn's distribution, mapped onto slots that have since
been renamed and retyped. So a route can be caatinga to look at and hold
nothing that belongs in a caatinga.

This measures that, per map, using each species' own types as this project
wrote them. It is a coherence report and nothing more - it does not say a map
is broken, it says how much of what is in it agrees with what it looks like.

    python3 tools/audit/check_biome_encounters.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/art"))
sys.path.insert(0, str(ROOT / "tools/audit"))

# What each biome reads as, in the type language the species already speak.
# Deliberately generous - three types each - because the question is whether a
# map holds anything of itself, not whether every slot is on the nose.
BELONGS = {
    "MATA": {"GRASS", "BUG", "POISON"},
    "CERRADO": {"FIRE", "GROUND", "NORMAL"},
    "PAMPA": {"NORMAL", "FLYING", "GRASS"},
    "ARAUCARIA": {"ICE", "GRASS", "ROCK"},
    "CAATINGA": {"GROUND", "ROCK", "FIRE"},
    "MANGUE": {"WATER", "POISON", "BUG"},
}


def species_types():
    text = (ROOT / "src/data/pokemon/species_info.h").read_text(encoding="utf-8",
                                                                errors="replace")
    out = {}
    for name, body in re.findall(r"\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\n    \},", text, re.S):
        m = re.search(r"\.types\s*=\s*\{\s*TYPE_(\w+),\s*TYPE_(\w+)\s*\}", body)
        if m:
            out[name] = set(m.groups())
    return out


def encounters():
    data = json.loads((ROOT / "src/data/wild_encounters.json")
                      .read_text(encoding="utf-8", errors="replace"))
    out = {}
    for entry in data["wild_encounter_groups"][0]["encounters"]:
        slots = []
        for key in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
            if entry.get(key):
                slots += [m["species"].replace("SPECIES_", "") for m in entry[key]["mons"]]
        if slots:
            out.setdefault(entry["map"].replace("MAP_", ""), []).extend(slots)
    return out


def main():
    import forge_town_variants as forge
    import retheme_cities

    biomes = dict(forge.COUNTRYSIDE)
    for city, theme in retheme_cities.THEMES.items():
        if theme.get("biome"):
            biomes.setdefault(city, theme["biome"])

    types, wild = species_types(), encounters()
    rows = []
    for name, biome in biomes.items():
        key = next((k for k in (name.upper(),
                                re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()) if k in wild), None)
        if key is None:
            continue
        mons = wild[key]
        fits = sum(1 for s in mons if types.get(s, set()) & BELONGS[biome])
        rows.append((fits / len(mons), name, biome, len(mons), fits))

    rows.sort()
    print("%-18s %-10s %6s %8s" % ("map", "biome", "slots", "belongs"))
    for frac, name, biome, total, fits in rows:
        print("%-18s %-10s %6d %5d  %3.0f%%" % (name, biome, total, fits, 100 * frac))
    total = sum(r[3] for r in rows)
    fits = sum(r[4] for r in rows)
    print("\n%d of %d slots (%.0f%%) hold something that belongs to the map's biome"
          % (fits, total, 100 * fits / total if total else 0))
    empty = [r[1] for r in rows if r[4] == 0]
    if empty:
        print("nothing of itself at all: %s" % ", ".join(sorted(empty)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

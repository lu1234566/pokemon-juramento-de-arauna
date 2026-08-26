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


def map_biomes():
    """Every map that wears a biome, keyed the way wild_encounters.json spells it.

    The map names here are written CamelCase with the odd underscore already in
    them - `SafariZone_North` - and turning that into the JSON's
    `SAFARI_ZONE_NORTH` needs the underscore that is already there not to be
    doubled by the one the capital asks for. It used to be, which is why the six
    Safari Zone maps - 72 land slots, a quarter of everything with a biome -
    were silently outside every count this file ever printed.
    """
    import forge_town_variants as forge
    import retheme_cities

    def snake(name):
        return re.sub(r"_+", "_", re.sub(r"(?<!^)(?=[A-Z])", "_", name)).upper()

    named = dict(forge.COUNTRYSIDE)
    for city, theme in retheme_cities.THEMES.items():
        if theme.get("biome"):
            named.setdefault(city, theme["biome"])
    return {spelling: biome for name, biome in named.items()
            for spelling in (name.upper(), snake(name))}


def species_types():
    text = (ROOT / "src/data/pokemon/species_info.h").read_text(encoding="utf-8",
                                                                errors="replace")
    out = {}
    for name, body in re.findall(r"\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\n    \},", text, re.S):
        m = re.search(r"\.types\s*=\s*\{\s*TYPE_(\w+),\s*TYPE_(\w+)\s*\}", body)
        if m:
            out[name] = set(m.groups())
    return out


# Only the grass can be steered. A surfing or fishing table is water-typed by
# its nature and a rock-smash table is what is inside a rock, so those are
# counted apart rather than folded into one number that means neither.
STEERABLE = ("land_mons",)
FIXED = ("water_mons", "rock_smash_mons", "fishing_mons")


def encounters():
    data = json.loads((ROOT / "src/data/wild_encounters.json")
                      .read_text(encoding="utf-8", errors="replace"))
    out = {}
    for entry in data["wild_encounter_groups"][0]["encounters"]:
        name = entry["map"].replace("MAP_", "")
        for kind, keys in (("land", STEERABLE), ("water", FIXED)):
            slots = [m["species"].replace("SPECIES_", "")
                     for key in keys if entry.get(key)
                     for m in entry[key]["mons"]]
            if slots:
                out.setdefault(name, {}).setdefault(kind, []).extend(slots)
    return out


def main():
    types, wild = species_types(), encounters()
    biomes = map_biomes()
    rows = []
    for key, biome in sorted(biomes.items()):
        if key not in wild:
            continue
        mons = wild[key].get("land")
        if not mons:
            continue                      # a sea route has no grass to steer
        fits = sum(1 for s in mons if types.get(s, set()) & BELONGS[biome])
        rows.append((fits / len(mons), key, biome, len(mons), fits))

    rows.sort()
    print("%-22s %-10s %6s %8s" % ("map", "biome", "grass", "belongs"))
    for frac, name, biome, total, fits in rows:
        print("%-22s %-10s %6d %5d  %3.0f%%" % (name, biome, total, fits, 100 * frac))
    total = sum(r[3] for r in rows)
    fits = sum(r[4] for r in rows)
    print("\n%d of %d grass slots (%.0f%%) hold something that belongs to the "
          "map's biome" % (fits, total, 100 * fits / total if total else 0))
    wet = [(name, mons) for name, kinds in wild.items() for mons in [kinds.get("water")]
           if mons and name in biomes]
    print("%d water, fishing and rock-smash slots on the same maps are left "
          "alone" % sum(len(m) for _, m in wet))
    empty = [r[1] for r in rows if r[4] == 0]
    if empty:
        print("nothing of itself at all: %s" % ", ".join(sorted(empty)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

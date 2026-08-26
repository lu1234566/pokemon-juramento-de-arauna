#!/usr/bin/env python3
"""Put the creatures where the land they live in says they should be.

Every route wears a biome now, drawn into its grass and its leaves. What walks
around in the grass was never touched: the wild tables are still Hoenn's, on
slots that have since been renamed and retyped, so a caatinga can hold nothing
of a caatinga - and five of them hold exactly that.

Choosing new creatures for each route would be the obvious fix and the wrong
one: it makes some species unobtainable, others suddenly common, and it moves
the difficulty of every route it touches. So nothing is chosen. The species
already in the ground are *permuted* between maps, and only within a band of
similar strength, so that:

  * every species still appears exactly as many times as it did - the Pokedex
    stays completable and nothing becomes a rarity by accident;
  * every slot keeps its own levels and its own encounter rate, so a route is
    as hard as it was;
  * and what lives on a map is as much of that map's biome as the permutation
    can manage.

Water is left alone. A sea route is not a caatinga whatever the tileset says,
and surfing tables are water-typed by their nature.

    python3 tools/art/rehome_wilds.py --report
    python3 tools/art/rehome_wilds.py
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/art"))
sys.path.insert(0, str(ROOT / "tools/audit"))

WILDS = ROOT / "src/data/wild_encounters.json"

# What each biome reads as, in the type language the species already speak.
from check_biome_encounters import BELONGS  # noqa: E402

# How wide a band of base-stat total counts as "about as strong". Two species
# inside one band can change places without a route getting harder or easier.
BAND = 60


def species_facts():
    text = (ROOT / "src/data/pokemon/species_info.h").read_text(encoding="utf-8",
                                                                errors="replace")
    types, power = {}, {}
    for name, body in re.findall(r"\[SPECIES_(\w+)\]\s*=\s*\{(.*?)\n    \},", text, re.S):
        m = re.search(r"\.types\s*=\s*\{\s*TYPE_(\w+),\s*TYPE_(\w+)\s*\}", body)
        if m:
            types[name] = set(m.groups())
        total = 0
        for field in ("baseHP", "baseAttack", "baseDefense", "baseSpeed",
                      "baseSpAttack", "baseSpDefense"):
            got = re.search(r"\.%s\s*=\s*(\d+)" % field, body)
            total += int(got.group(1)) if got else 0
        power[name] = total
    return types, power


def biomes():
    import forge_town_variants as forge
    import retheme_cities
    out = dict(forge.COUNTRYSIDE)
    for city, theme in retheme_cities.THEMES.items():
        if theme.get("biome"):
            out.setdefault(city, theme["biome"])
    return {re.sub(r"(?<!^)(?=[A-Z])", "_", k).upper(): v for k, v in out.items()} | \
           {k.upper(): v for k, v in out.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    types, power = species_facts()
    where = biomes()
    data = json.loads(WILDS.read_text(encoding="utf-8", errors="replace"))

    # Every land slot on a map that has a biome, as somewhere a species sits.
    slots = []
    for entry in data["wild_encounter_groups"][0]["encounters"]:
        name = entry["map"].replace("MAP_", "")
        biome = where.get(name)
        if not biome or not entry.get("land_mons"):
            continue
        for i, mon in enumerate(entry["land_mons"]["mons"]):
            slots.append({"entry": entry, "index": i, "biome": biome,
                          "species": mon["species"].replace("SPECIES_", "")})
    if not slots:
        print("no land slots on any map with a biome")
        return 0

    def fits(species, biome):
        return bool(types.get(species, set()) & BELONGS[biome])

    before = sum(1 for s in slots if fits(s["species"], s["biome"]))

    # Band the slots by how strong what is standing in them is, and permute
    # inside each band only.
    bands = collections.defaultdict(list)
    for slot in slots:
        bands[power.get(slot["species"], 0) // BAND].append(slot)

    moved = 0
    for band, members in bands.items():
        pool = collections.Counter(s["species"] for s in members)
        # Hand out the fitting species first, to the maps that have the fewest
        # candidates - otherwise a common biome takes them all and a rare one
        # is left with nothing again.
        order = sorted(members, key=lambda s: sum(
            n for sp, n in pool.items() if fits(sp, s["biome"])))
        assigned = {}
        for slot in order:
            pick = next((sp for sp in sorted(pool)
                         if pool[sp] and fits(sp, slot["biome"])), None)
            if pick is None:
                continue
            pool[pick] -= 1
            assigned[id(slot)] = pick
        leftovers = [sp for sp, n in sorted(pool.items()) for _ in range(n)]
        for slot in order:
            if id(slot) not in assigned:
                assigned[id(slot)] = leftovers.pop()
        for slot in members:
            new = assigned[id(slot)]
            if new != slot["species"]:
                moved += 1
            slot["new"] = new

    after = sum(1 for s in slots if fits(s.get("new", s["species"]), s["biome"]))
    print("%d land slot(s) on %d map(s) with a biome"
          % (len(slots), len({id(s["entry"]) for s in slots})))
    print("  belonged before: %d (%.0f%%)" % (before, 100 * before / len(slots)))
    print("  belongs after:   %d (%.0f%%)" % (after, 100 * after / len(slots)))
    print("  %d slot(s) change hands; every species keeps its exact count" % moved)

    if args.report:
        return 0

    for slot in slots:
        slot["entry"]["land_mons"]["mons"][slot["index"]]["species"] = \
            "SPECIES_" + slot["new"]
    WILDS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

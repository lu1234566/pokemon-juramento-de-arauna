#!/usr/bin/env python3
"""Give every one of the 386 creatures somewhere to be caught.

Emerald ships encounter tables for the roughly two hundred species of the Hoenn
dex; the rest of the National dex came from trading with Fire Red and Leaf
Green. Arauna has 386 species and inherited those same tables, so 143 species
appear in the wild, twenty more are handed out by script, evolution reaches a
few dozen past those -- and 198 creatures cannot be obtained at all. The Pokedex
is impossible to finish, and the missing list is not obscure: Curupira, Boiuna,
Mae-d'Agua, Sucuri, Guaraflama.

Only the roots need planting. A creature whose pre-evolution becomes catchable
becomes catchable itself, so of the 198 missing, 179 are chain roots and the
other 19 follow from them.

There is room without touching a single table's shape. Of the game's 2107
encounter slots, 1412 hold a species that already appears elsewhere in the same
table -- Rusturf Tunnel, Mt. Pyre and Route 130 each fill twelve slots with one
species. Those surplus duplicates are what this pass spends, and it never spends
the last copy of anything, so nothing that was catchable stops being catchable.

Encounter rates, level ranges, table sizes and map assignments are all
untouched. Only which species a slot names changes.

A creature goes where it fits:

  * habitat is a hard rule -- water and fishing tables take only Water types,
    rock smash only Rock and Ground;
  * strength is the soft rule -- among the slots left, the one whose displaced
    species is closest in base stat total, so the creature lands at a level its
    own power suits;
  * a table already leaning on the creature's type wins the tie, which keeps
    the routes reading as habitats rather than lists.

Run it last. build_placement.py rewrites the whole encounter table from its own
baseline, so it undoes this pass; running this one again afterwards puts
everything back. check_availability.py, in the static gate, fails loudly if
anyone forgets.

  --check   report what is unobtainable and what would be planted
  --write   rewrite src/data/wild_encounters.json
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORT = ROOT / "graphics/arauna/arauna_sprites_gba_export.zip"
MAPPING = ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
ENCOUNTERS = ROOT / "src/data/wild_encounters.json"
EVOLUTION = ROOT / "src/data/pokemon/evolution.h"
ROSTER = ROOT / "docs/arauna/ARAUNA_AVAILABILITY.csv"

WATER_TABLES = {"water_mons", "fishing_mons"}
ROCK_TABLES = {"rock_smash_mons"}
SLOTS_PER_SPECIES = 2      # give each newcomer two slots where the budget allows


def committed(path: Path) -> str:
    """The working tree, deliberately, unlike the other passes.

    They permute, so re-running one against its own output moves everything
    twice and they have to read a pinned baseline. This one only fills surplus
    slots for species that have nowhere to live, so a second run finds nothing
    missing and plants nothing: idempotent by construction. Reading the live
    tree is also what lets it compose -- run it after build_placement.py and it
    repairs what that pass overwrote, which a pinned baseline could not do.
    """
    return path.read_text(encoding="utf-8")


def arauna():
    with zipfile.ZipFile(EXPORT) as zf:
        mons = {m["id"]: m for m in json.loads(zf.read("pokedex.json"))["pokemon"]}
    by_slot, by_dex = {}, {}
    for row in csv.DictReader(MAPPING.open(encoding="utf-8")):
        dex = int(row["arauna_dex"])
        mon = mons[dex]
        entry = {"slot": row["species_constant"], "dex": dex, "name": mon["name"],
                 "types": mon["types"], "bst": sum(mon["stats"].values())}
        by_slot[row["species_constant"]] = entry
        by_dex[dex] = entry
    return by_slot, by_dex


def evolution_links(by_slot):
    """dex -> dex it evolves into, and the reverse."""
    forward, backward = {}, {}
    for match in re.finditer(r"\[(SPECIES_\w+)\]\s*= \{\{EVO_LEVEL, \d+, (SPECIES_\w+)\}\}",
                             EVOLUTION.read_text(encoding="utf-8")):
        source = by_slot.get(match.group(1))
        target = by_slot.get(match.group(2))
        if source and target:
            forward.setdefault(source["dex"], []).append(target["dex"])
            backward[target["dex"]] = source["dex"]
    return forward, backward


def scripted(by_slot) -> set[int]:
    """Everything a map script hands out or starts a battle with, plus the starters."""
    found = subprocess.run(
        ["grep", "-rhoE", r"(givemon|setwildbattle|createmon)[^\n]*SPECIES_[A-Z_0-9]+", "data"],
        cwd=ROOT, capture_output=True, text=True).stdout
    out = {by_slot[name]["dex"] for name in re.findall(r"SPECIES_[A-Z_0-9]+", found)
           if name in by_slot}
    for starter in ("SPECIES_TREECKO", "SPECIES_TORCHIC", "SPECIES_MUDKIP"):
        out.add(by_slot[starter]["dex"])
    return out


# The Battle Pyramid and Battle Pike have wild battles you cannot catch in, so
# a species living only there is still unobtainable. Their tables are neither
# counted nor planted into.
CATCHABLE_GROUP = "gWildMonHeaders"


def tables(data):
    """Every encounter table you can actually catch from."""
    for group in data["wild_encounter_groups"]:
        if group.get("label") != CATCHABLE_GROUP:
            continue
        for encounter in group["encounters"]:
            for key, value in encounter.items():
                if isinstance(value, dict) and "mons" in value:
                    yield encounter.get("map", encounter.get("base_label", "?")), key, value["mons"]


def caught_in_the_wild(data, by_slot) -> set[int]:
    return {by_slot[m["species"]]["dex"]
            for _, _, mons in tables(data) for m in mons if m["species"] in by_slot}


def reachable(seeds, forward) -> set[int]:
    seen, stack = set(seeds), list(seeds)
    while stack:
        current = stack.pop()
        for nxt in forward.get(current, []):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    by_slot, by_dex = arauna()
    forward, backward = evolution_links(by_slot)
    data = json.loads(committed(ENCOUNTERS))

    wild = caught_in_the_wild(data, by_slot)
    gifts = scripted(by_slot)
    have = reachable(wild | gifts, forward)
    missing = set(by_dex) - have
    roots = sorted(d for d in missing if backward.get(d) not in missing)

    print(f"wild {len(wild)}, scripted {len(gifts)}, reachable with evolution {len(have)}")
    print(f"unobtainable: {len(missing)} of {len(by_dex)}; {len(roots)} of them chain roots")

    # Surplus duplicates: every occurrence past the first of a species in a table.
    spare = []
    for name, kind, mons in tables(data):
        seen = collections.Counter()
        types_here = collections.Counter()
        for mon in mons:
            entry = by_slot.get(mon["species"])
            if entry:
                for kind_name in entry["types"]:
                    types_here[kind_name] += 1
        for index, mon in enumerate(mons):
            seen[mon["species"]] += 1
            if seen[mon["species"]] > 1:
                entry = by_slot.get(mon["species"])
                spare.append({"map": name, "table": kind, "index": index,
                              "mons": mons, "displaced": mon["species"],
                              "bst": entry["bst"] if entry else 300,
                              "flavour": types_here})
    print(f"surplus duplicate slots available: {len(spare)}")

    def allowed(entry, slot):
        if slot["table"] in WATER_TABLES:
            return "water" in entry["types"]
        if slot["table"] in ROCK_TABLES:
            return bool({"rock", "ground"} & set(entry["types"]))
        return True

    used, plan = set(), []
    for dex in roots:
        entry = by_dex[dex]
        picks = []
        options = [s for i, s in enumerate(spare) if i not in used and allowed(entry, s)]
        options.sort(key=lambda s: (abs(s["bst"] - entry["bst"])
                                    - 40 * sum(s["flavour"][t] > 0 for t in entry["types"])))
        for slot in options[:SLOTS_PER_SPECIES]:
            used.add(spare.index(slot))
            picks.append(slot)
        if not picks:
            print(f"  no home for #{dex:03d} {entry['name']}", file=sys.stderr)
            continue
        for slot in picks:
            plan.append((entry, slot))

    planted = {entry["dex"] for entry, _ in plan}
    print(f"planting {len(planted)} creatures into {len(plan)} slots")

    # Apply to a copy and prove it worked before writing anything.
    for entry, slot in plan:
        slot["mons"][slot["index"]]["species"] = entry["slot"]
    after_wild = caught_in_the_wild(data, by_slot)
    after = reachable(after_wild | gifts, forward)
    still = sorted(set(by_dex) - after)
    print(f"after: wild {len(after_wild)}, obtainable {len(after)} of {len(by_dex)}"
          + (f"; still missing {still}" if still else "; nothing is unobtainable"))

    lost = {d for d in wild if d not in after_wild}
    print(f"species that lost their last wild slot: {len(lost)}"
          + (f" {sorted(lost)}" if lost else ""))

    if not args.write:
        return 0
    if still or lost:
        print("refusing to write: the plan does not fully close the dex", file=sys.stderr)
        return 1

    ENCOUNTERS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["arauna_dex", "name", "types", "bst", "map", "table", "displaced"])
        for entry, slot in sorted(plan, key=lambda p: p[0]["dex"]):
            writer.writerow([f"{entry['dex']:03d}", entry["name"], "/".join(entry["types"]),
                             entry["bst"], slot["map"], slot["table"],
                             slot["displaced"][len("SPECIES_"):]])
    print(f"\nwrote {ENCOUNTERS.relative_to(ROOT)} and {ROSTER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

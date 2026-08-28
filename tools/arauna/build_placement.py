#!/usr/bin/env python3
"""Put the Arauna species where the game's difficulty curve expects them.

Installing the dex moved every creature but not a single encounter table, and
the two orders do not agree. SPECIES_POOCHYENA is Route 101's level-2 filler and
now holds #261 Curupira-Ancião: Route 101 averages a base stat total of 500 at
level 2. Every route, cave and trainer in the game is off by the same kind of
amount.

Nothing about the route design is wrong -- the maps, the encounter rates, the
level ranges and the party sizes are all still right. What is wrong is which
species each slot names. So this tool builds one substitution over engine
species constants and applies it to the encounter tables and the trainer
parties: wherever the vanilla game asked for a creature of a given strength and
type, it now asks for the Arauna creature closest to that.

The substitution is built like this:

  1. rank the 386 vanilla species by base stat total, and the 386 Arauna
     species by theirs;
  2. pair them off by rank, so a vanilla slot is replaced by an Arauna creature
     of the same relative strength;
  3. improve the pairing with swaps that trade up to TYPE_BONUS base stat points
     of accuracy for a better type match, so water routes stay watery and caves
     stay rocky. Route 118's water and fishing slots all come out as Brazilian
     fish -- Traíra, Tucunaré, Aruanã, Peixim -- which is the point.

Some slots are pinned to themselves rather than substituted: the three starter
families, and every species a map script hands out or starts a battle with by
name. Those slots are addressed directly by the story, so the rival keeps a
starter and a scripted gift stays the creature the script says it is.

Levels, encounter rates, map assignments, party sizes, IVs, items and moves are
all untouched. Only species names change.

The floor moves less than it looks. Arauna's weakest creature has a base stat
total of 248 against vanilla's 180, so an early route settles around 300 rather
than 205 no matter how the pairing is drawn. That is the dex's own shape, not
the substitution's.

  --check   report the substitution and what it does to the curve
  --write   apply it and write docs/arauna/ARAUNA_PLACEMENT.csv

The CSV is the record: one line per engine slot saying which Arauna creature now
answers for it. Editing a line and rerunning with --write is how to overrule any
individual choice.
"""
from __future__ import annotations

import argparse
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
PLACEMENT = ROOT / "docs/arauna/ARAUNA_PLACEMENT.csv"
ENCOUNTERS = ROOT / "src/data/wild_encounters.json"
PARTIES = ROOT / "src/data/trainer_parties.h"

# The commit before the species tables landed still has the vanilla stats.
VANILLA_REV = "d4804fcc^"
SWAP_SPAN = 40          # how far along the strength order a swap may reach
SWAP_ROUNDS = 6
TYPE_BONUS = 25         # base stat points a matching primary type is worth trading

# Slots the story addresses by name, left holding whatever the dex mapping gave
# them: the three starter families, and every species named by a map script.
PINNED = {
    "SPECIES_TREECKO", "SPECIES_GROVYLE", "SPECIES_SCEPTILE",
    "SPECIES_TORCHIC", "SPECIES_COMBUSKEN", "SPECIES_BLAZIKEN",
    "SPECIES_MUDKIP", "SPECIES_MARSHTOMP", "SPECIES_SWAMPERT",
    "SPECIES_VOLTORB", "SPECIES_ELECTRODE", "SPECIES_KECLEON",
    "SPECIES_CASTFORM", "SPECIES_BELDUM", "SPECIES_SUDOWOODO",
    "SPECIES_LILEEP", "SPECIES_ANORITH",
    "SPECIES_CHIKORITA", "SPECIES_CYNDAQUIL", "SPECIES_TOTODILE",
    "SPECIES_REGIROCK", "SPECIES_REGICE", "SPECIES_REGISTEEL",
    "SPECIES_KYOGRE", "SPECIES_GROUDON", "SPECIES_RAYQUAZA",
}


def vanilla_species() -> dict[str, dict]:
    """Base stat total and types of every species as the engine had them."""
    text = subprocess.run(["git", "show", f"{VANILLA_REV}:src/data/pokemon/species_info.h"],
                          cwd=ROOT, capture_output=True, text=True, check=True).stdout
    out = {}
    for block in re.finditer(r"^    \[(SPECIES_\w+)\] =\n    \{\n(.*?)\n    \},?$",
                             text, re.S | re.M):
        name, body = block.group(1), block.group(2)
        stats = [int(m) for m in re.findall(
            r"\.base(?:HP|Attack|Defense|Speed|SpAttack|SpDefense)\s*=\s*(\d+)", body)]
        types = re.findall(r"\.types = \{\s*(TYPE_\w+),\s*(TYPE_\w+)", body)
        if len(stats) != 6 or not types:
            continue
        out[name] = {"bst": sum(stats), "types": list(types[0])}
    return out


def arauna_species() -> dict[str, dict]:
    with zipfile.ZipFile(EXPORT) as zf:
        entries = {e["id"]: e for e in json.loads(zf.read("pokedex.json"))["pokemon"]}
    out = {}
    for row in csv.DictReader(MAPPING.open(encoding="utf-8")):
        entry = entries[int(row["arauna_dex"])]
        out[row["species_constant"]] = {
            "bst": sum(entry["stats"].values()),
            "types": ["TYPE_" + t.upper() for t in entry["types"]],
            "dex": int(row["arauna_dex"]),
            "name": entry["name"],
        }
    return out


def type_match(a: list[str], b: list[str]) -> int:
    """2 when the primary types agree, 1 when the types merely overlap."""
    if a[0] == b[0]:
        return 2
    return 1 if set(a) & set(b) else 0


def build(vanilla, arauna) -> dict[str, str]:
    every = set(vanilla) & set(arauna)
    pairing = {slot: slot for slot in every & PINNED}
    # Sort on the name as well as the total: ties broken by set order would make
    # the pairing differ between runs.
    slots = sorted(every - PINNED, key=lambda s: (vanilla[s]["bst"], s))
    by_power = sorted(slots, key=lambda s: (arauna[s]["bst"], s))
    pairing.update(zip(slots, by_power))

    def score(slot, chosen):
        drift = abs(vanilla[slot]["bst"] - arauna[chosen]["bst"])
        return drift - TYPE_BONUS * type_match(vanilla[slot]["types"], arauna[chosen]["types"])

    order = list(slots)
    for _ in range(SWAP_ROUNDS):
        improved = 0
        for i, slot in enumerate(order):
            for j in range(max(0, i - SWAP_SPAN), min(len(order), i + SWAP_SPAN)):
                other = order[j]
                if other == slot:
                    continue
                before = score(slot, pairing[slot]) + score(other, pairing[other])
                after = score(slot, pairing[other]) + score(other, pairing[slot])
                if after < before:
                    pairing[slot], pairing[other] = pairing[other], pairing[slot]
                    improved += 1
        if not improved:
            break
    return pairing


def committed(path: Path) -> str:
    """The file as last committed.

    The substitution is a permutation, so applying it to its own output moves
    everything a second time. Always start from the committed text; then
    --write is idempotent and safe to rerun after editing the CSV.
    """
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def apply_encounters(pairing) -> tuple[str, int]:
    data = json.loads(committed(ENCOUNTERS))
    changed = 0

    def walk(node):
        nonlocal changed
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "species" and isinstance(value, str) and value in pairing:
                    if pairing[value] != value:
                        changed += 1
                    node[key] = pairing[value]
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return json.dumps(data, indent=2) + "\n", changed


def apply_parties(pairing) -> tuple[str, int]:
    text = committed(PARTIES)
    changed = 0

    def swap(match):
        nonlocal changed
        name = match.group(1)
        if name in pairing and pairing[name] != name:
            changed += 1
            return f".species = {pairing[name]},"
        return match.group(0)

    return re.sub(r"\.species = (SPECIES_\w+),", swap, text), changed


def curve(pairing, arauna, source: dict) -> list[tuple[str, int, int]]:
    """Mean base stat total of the land encounters on the earliest maps."""
    rows = []
    for group in source["wild_encounter_groups"]:
        for enc in group["encounters"]:
            table = enc.get("land_mons")
            if not table or "map" not in enc:
                continue
            levels = [m["min_level"] for m in table["mons"]]
            totals = [arauna[pairing.get(m["species"], m["species"])]["bst"]
                      for m in table["mons"] if pairing.get(m["species"], m["species"]) in arauna]
            if totals:
                rows.append((enc["map"], min(levels), round(sum(totals) / len(totals))))
    rows.sort(key=lambda r: r[1])
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    vanilla, arauna = vanilla_species(), arauna_species()
    if PLACEMENT.exists() and not args.check:
        pairing = {r["engine_slot"]: r["now_holds_slot"]
                   for r in csv.DictReader(PLACEMENT.open(encoding="utf-8"))}
        print(f"reusing the placement already in {PLACEMENT.relative_to(ROOT)}")
    else:
        pairing = build(vanilla, arauna)

    matched = sum(1 for s, c in pairing.items()
                  if type_match(vanilla[s]["types"], arauna[c]["types"]) == 2)
    drift = [abs(vanilla[s]["bst"] - arauna[c]["bst"]) for s, c in pairing.items()]
    print(f"{len(pairing)} slots substituted; primary type preserved for {matched} "
          f"({matched * 100 // len(pairing)}%); mean strength drift "
          f"{sum(drift) // len(drift)} base stat points")

    source = json.loads(committed(ENCOUNTERS))
    before = curve({}, arauna, source)
    after = curve(pairing, arauna, source)
    print("\nearliest land encounters, mean base stat total:")
    print(f"  {'map':32} {'level':>5} {'before':>7} {'after':>6}")
    for (name, level, was), (_, _, now) in list(zip(before, after))[:8]:
        print(f"  {name[:32]:32} {level:5} {was:7} {now:6}")

    if not args.write:
        return 0

    encounters, n_enc = apply_encounters(pairing)
    parties, n_party = apply_parties(pairing)
    ENCOUNTERS.write_text(encounters, encoding="utf-8")
    PARTIES.write_text(parties, encoding="utf-8")

    with PLACEMENT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["engine_slot", "vanilla_bst", "now_holds_slot",
                         "arauna_dex", "arauna_name", "arauna_bst"])
        for slot in sorted(pairing, key=lambda s: vanilla[s]["bst"]):
            chosen = pairing[slot]
            writer.writerow([slot, vanilla[slot]["bst"], chosen,
                             f"{arauna[chosen]['dex']:03d}", arauna[chosen]["name"],
                             arauna[chosen]["bst"]])

    print(f"\nrewrote {n_enc} encounter slots and {n_party} trainer party members; "
          f"wrote {PLACEMENT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

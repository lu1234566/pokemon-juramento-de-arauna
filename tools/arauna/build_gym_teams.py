#!/usr/bin/env python3
"""Give the gyms and the Elite Four their themes back.

The placement pass matched every trainer's Pokemon on strength and primary type,
which held up wherever Arauna has creatures to spare and collapsed where it does
not. Wattson's electric gym came out with one electric in four; Tate's psychic
gym the same; Glacia's ice team with nothing at all, because the Arauna dex has
96 water creatures, 14 electric ones and zero ice.

This pass fixes the trainers whose type is the point of the fight. For each
party it keeps the level, the IVs, the items, the moves and the number of
Pokemon, and replaces only the species, choosing from the theme's pool the
creature closest in base stat total to the one being replaced. Ranked by level
inside the party, so a leader's ace stays the strongest thing they own.

Glacia becomes steel. Not because steel is the largest free pool -- it is one of
the smallest at 16 -- but because the right piece already exists: #110 Ogum, the
orixa of iron, 602 base stat total, steel/fire. An ice specialist in a Brazilian
region was always going to be a translation; an iron one is not.

Everything else keeps its vanilla theme. Phoebe stays ghost, Sidney dark, Drake
dragon, and the eight gyms keep the type their badge and their puzzle are built
around.

  --check   report the coverage before and after
  --write   rewrite the parties
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# The tree before the gym-team pass landed; see committed().
BASELINE = "2ca77244"
EXPORT = ROOT / "graphics/arauna/arauna_sprites_gba_export.zip"
MAPPING = ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
PARTIES = ROOT / "src/data/trainer_parties.h"
TRAINERS = ROOT / "src/data/trainers.h"
ROSTER = ROOT / "docs/arauna/ARAUNA_GYM_TEAMS.csv"

# The story's legendaries. Not the export's "legendary" flag -- the orixas are
# not flagged there -- but the engine slots the campaign places by name and the
# roamers. A gym leader fielding Oxala would be fielding the Navel Rock encounter.
STORY_SLOTS = {f"SPECIES_{name}" for name in """
    ARTICUNO ZAPDOS MOLTRES MEWTWO MEW RAIKOU ENTEI SUICUNE LUGIA HO_OH CELEBI
    REGIROCK REGICE REGISTEEL KYOGRE GROUDON RAYQUAZA LATIAS LATIOS JIRACHI DEOXYS
""".split()}

# The eight gyms, by the map their trainers stand in.
GYMS = {
    "RustboroCity_Gym": "rock",
    "DewfordTown_Gym": "fighting",
    "MauvilleCity_Gym": "electric",
    "LavaridgeTown_Gym_1F": "fire",
    "LavaridgeTown_Gym_B1F": "fire",
    "PetalburgCity_Gym": "normal",
    "FortreeCity_Gym": "flying",
    "MossdeepCity_Gym": "psychic",
    "SootopolisCity_Gym_1F": "water",
    "SootopolisCity_Gym_B1F": "water",
}

# Leaders and their rematches, then the Elite Four and the champion. The party
# symbols are prefixes: sParty_Roxanne1 through 5 all match "Roxanne".
LEADERS = {
    "Roxanne": "rock", "Brawly": "fighting", "Wattson": "electric",
    "Flannery": "fire", "Norman": "normal", "Winona": "flying",
    "Tate": "psychic", "Liza": "psychic", "TateAndLiza": "psychic",
    "Juan": "water",
    "Sidney": "dark", "Phoebe": "ghost", "Drake": "dragon", "Wallace": "water",
    # Ice does not exist in this dex. Ogum, the orixa of iron, does.
    "Glacia": "steel",
}


def committed(path: Path) -> str:
    """The file as it stood before this tool first wrote it.

    Not HEAD. This pass is a substitution, so running it against its own output
    moves everything a second time -- and once the output is committed, HEAD is
    the output. Pinning the baseline to the commit before the pass landed is what
    actually makes --write idempotent; reading HEAD only looked idempotent while
    the work was still uncommitted.
    """
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.run(["git", "show", f"{BASELINE}:{rel}"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def arauna():
    with zipfile.ZipFile(EXPORT) as zf:
        mons = {m["id"]: m for m in json.loads(zf.read("pokedex.json"))["pokemon"]}
    by_slot, by_type = {}, {}
    for row in csv.DictReader(MAPPING.open(encoding="utf-8")):
        mon = mons[int(row["arauna_dex"])]
        entry = {"slot": row["species_constant"], "dex": int(row["arauna_dex"]),
                 "name": mon["name"], "bst": sum(mon["stats"].values()),
                 "types": mon["types"]}
        by_slot[row["species_constant"]] = entry
        if row["species_constant"] in STORY_SLOTS:
            continue
        for kind in mon["types"]:
            by_type.setdefault(kind, []).append(entry)
    for kind in by_type:
        by_type[kind].sort(key=lambda e: (e["bst"], e["dex"]))
    return by_slot, by_type


def gym_trainers() -> dict[str, str]:
    """Trainer constant -> theme, for everyone standing inside a gym."""
    known = set(re.findall(r"^\s*\[(TRAINER_\w+)\] =", committed(TRAINERS), re.M))
    themed = {}
    for gym, kind in GYMS.items():
        folder = ROOT / "data/maps" / gym
        if not folder.is_dir():
            continue
        for root, _, files in os.walk(folder):
            for name in files:
                text = (Path(root) / name).read_text(encoding="utf-8", errors="replace")
                for trainer in re.findall(r"TRAINER_[A-Z0-9_]+", text):
                    if trainer in known:
                        themed[trainer] = kind
    return themed


def party_symbols(themed: dict[str, str]) -> dict[str, str]:
    """Party symbol -> theme, following each trainer to the party it fields."""
    text = committed(TRAINERS)
    out = {}
    for block in re.finditer(r"\[(TRAINER_\w+)\] =\s*\{(.*?)\n    \},", text, re.S):
        trainer = block.group(1)
        if trainer not in themed:
            continue
        symbol = re.search(r"sParty_(\w+)", block.group(2))
        if symbol:
            out[symbol.group(1)] = themed[trainer]
    return out


def all_targets() -> dict[str, str]:
    targets = party_symbols(gym_trainers())
    text = committed(PARTIES)
    for symbol in re.findall(r"sParty_(\w+)\[\]", text):
        for leader, kind in LEADERS.items():
            if symbol == leader or re.fullmatch(rf"{leader}\d*", symbol):
                targets[symbol] = kind
    return targets


def choose(pool, wanted_bst, taken):
    """Closest creature in the theme to the strength being replaced."""
    free = [e for e in pool if e["slot"] not in taken] or pool
    return min(free, key=lambda e: (abs(e["bst"] - wanted_bst), e["dex"]))


def rebuild(text: str, targets, by_slot, by_type, report):
    changed = 0

    def fix(match):
        nonlocal changed
        symbol, body = match.group(1), match.group(2)
        kind = targets.get(symbol)
        if not kind:
            return match.group(0)
        pool = by_type.get(kind, [])
        if not pool:
            return match.group(0)

        members = re.findall(r"\.lvl = (\d+),\s*\.species = (SPECIES_\w+),", body)
        if not members:
            return match.group(0)

        # Weakest slot gets the weakest suitable creature: the ace stays the ace.
        order = sorted(range(len(members)), key=lambda i: (int(members[i][0]), i))
        picks, taken = {}, set()
        for rank, index in enumerate(order):
            level, slot = members[index]
            current = by_slot.get(slot, {}).get("bst", 300)
            pick = choose(pool, current, taken)
            taken.add(pick["slot"])
            picks[index] = pick

        seen = 0

        def swap(member):
            nonlocal seen, changed
            pick = picks[seen]
            seen += 1
            if pick["slot"] != member.group(2):
                changed += 1
            return f"{member.group(1)}.species = {pick['slot']},"

        body = re.sub(r"(\.lvl = \d+,\s*)\.species = (SPECIES_\w+),", swap, body)
        report.append((symbol, kind, [picks[i] for i in range(len(members))],
                       [m[0] for m in members]))
        return f"static const struct {match.group(0).split('struct ')[1].split()[0]} " \
               f"sParty_{symbol}[] = {{{body}\n}};"

    return re.sub(r"static const struct \w+ sParty_(\w+)\[\] = \{(.*?)\n\};", fix,
                  text, flags=re.S), changed


def coverage(text, targets, by_slot, by_type):
    rows = []
    for match in re.finditer(r"sParty_(\w+)\[\] = \{(.*?)\n\};", text, re.S):
        symbol, kind = match.group(1), targets.get(match.group(1))
        if not kind:
            continue
        slots = re.findall(r"\.species = (SPECIES_\w+),", match.group(2))
        hit = sum(1 for s in slots if kind in by_slot.get(s, {}).get("types", []))
        rows.append((symbol, kind, hit, len(slots)))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    by_slot, by_type = arauna()
    targets = all_targets()
    print(f"pools exclude {len(STORY_SLOTS)} story legendary slots; "
          + ", ".join(f"{k} {len(v)}" for k, v in sorted(by_type.items())
                      if k in set(GYMS.values()) | set(LEADERS.values())))
    source = committed(PARTIES)

    before = coverage(source, targets, by_slot, by_type)
    rebuilt, changed = rebuild(source, targets, by_slot, by_type, report := [])
    after = coverage(rebuilt, targets, by_slot, by_type)

    hit_before = sum(h for _, _, h, _ in before)
    total = sum(n for _, _, _, n in before)
    hit_after = sum(h for _, _, h, _ in after)
    print(f"{len(targets)} themed trainers, {total} Pokemon")
    print(f"  on theme before: {hit_before}/{total} ({hit_before * 100 // total}%)")
    print(f"  on theme after:  {hit_after}/{total} ({hit_after * 100 // total}%)")
    print(f"  species changed: {changed}")

    print("\nleaders and the Elite Four:")
    for symbol, kind, picks, levels in report:
        if not any(symbol == l or re.fullmatch(rf"{l}\d*", symbol) for l in LEADERS):
            continue
        team = ", ".join(f"{p['name']} {lv}" for p, lv in zip(picks, levels))
        print(f"  {symbol:14} {kind:9} {team}")

    if not args.write:
        return 0

    PARTIES.write_text(rebuilt, encoding="utf-8")
    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["party", "theme", "level", "arauna_dex", "name", "bst", "types"])
        for symbol, kind, picks, levels in report:
            for pick, level in zip(picks, levels):
                writer.writerow([symbol, kind, level, f"{pick['dex']:03d}", pick["name"],
                                 pick["bst"], "/".join(pick["types"])])
    print(f"\nwrote {PARTIES.relative_to(ROOT)} and {ROSTER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Give the sixteen Battle Tower apprentices Brazilian names.

They are the last table of people still called what Emerald called them: the
trainer you mentor in the Battle Tower introduces himself as ALANN or SONNY.

Their table is shaped differently from every other, which is why it was left
for last. One apprentice carries six names, one per language of the original
game, and the engine picks by gGameLanguage. This game ships one language, so
the five Latin slots all get the same Brazilian name -- they are one person --
and the Japanese slot is left exactly as it is, since nothing reads it here and
rewriting kana in a Latin charmap would be a lie rather than a translation.

Gender comes from facilityClass, checked against the engine's own lists in
src/battle_tower.c, and the field is PLAYER_NAME_LENGTH, so the pool is the
same short forms the facility trainers draw from.

  --check   report what would be renamed
  --write   rewrite src/data/battle_frontier/apprentice.h and the roster CSV
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VANILLA = "c210195e"
APPRENTICES = ROOT / "src/data/battle_frontier/apprentice.h"
TOWER = ROOT / "src/battle_tower.c"
ROSTER = ROOT / "docs/arauna/ARAUNA_APPRENTICE_NAMES.csv"

NAME_LIMIT = 7  # PLAYER_NAME_LENGTH

WOMEN = "NEUZA CLEIA IVANI DALILA ROSILDA JANDIRA NILZA TEREZA".split()
MEN = ("ARLINDO CLEBER EDIVAL GENARO IZAIAS JOSIAS MESSIAS NIVALDO ROSALVO "
       "WALDECI DJALMA EURICO").split()

ENTRY = re.compile(r"(?P<head>\{\n\s*\.name = \{)(?P<names>[^}]*)(?P<tail>\},)"
                   r"(?P<body>.*?)\.facilityClass = (?P<klass>FACILITY_CLASS_\w+),",
                   re.S)
LATIN = re.compile(r'_\("([^"]*)"\)')


def tower_genders() -> tuple[set[str], set[str]]:
    body = TOWER.read_text(encoding="utf-8")

    def listed(symbol: str) -> set[str]:
        block = re.search(r"const u8 " + symbol + r"\[\d+\] =\s*\{(.*?)\};", body, re.S)
        return set(re.findall(r"FACILITY_CLASS_\w+", block.group(1)))

    return listed("gTowerMaleFacilityClasses"), listed("gTowerFemaleFacilityClasses")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    male, female = tower_genders()
    original = subprocess.run(["git", "show", f"{VANILLA}:{APPRENTICES.relative_to(ROOT)}"],
                              cwd=ROOT, capture_output=True, text=True, check=True).stdout
    body = APPRENTICES.read_text(encoding="utf-8")

    women, men = iter(WOMEN), iter(MEN)
    rows, short = [], []
    for found in ENTRY.finditer(original):
        klass = found.group("klass")
        is_female = klass in female
        if not is_female and klass not in male:
            raise SystemExit(f"{klass} is in neither tower gender list")
        pick = next(women if is_female else men, None)
        if pick is None:
            short.append(klass)
            continue
        english = LATIN.findall(found.group("names"))[1]
        rows.append({"vanilla_name": english, "gender": "F" if is_female else "M",
                     "arauna_name": pick, "facility_class": klass[len("FACILITY_CLASS_"):]})

    over = [r["arauna_name"] for r in rows if len(r["arauna_name"]) > NAME_LIMIT]
    print(f"{len(rows)} apprentices: "
          f"{sum(1 for r in rows if r['gender'] == 'F')} women, "
          f"{sum(1 for r in rows if r['gender'] == 'M')} men")
    print(f"  ran out of names for: {len(short)} {short}")
    print(f"  over {NAME_LIMIT} characters: {len(over)} {over}")
    for row in rows[:6]:
        print(f"   {row['vanilla_name']:8} -> {row['arauna_name']}")
    if short or over:
        raise SystemExit("refusing: fix the pools first")

    def rename(found, rows=iter(rows)):
        row = next(rows)
        names = LATIN.findall(found.group("names"))
        # Slot 0 is Japanese and nothing here reads it; the five Latin slots
        # are the same person, so they get the same name.
        rebuilt = ", ".join([f'_("{names[0]}")']
                            + [f'_("{row["arauna_name"]}")'] * (len(names) - 1))
        return (found.group("head") + rebuilt + found.group("tail")
                + found.group("body") + f".facilityClass = {found.group('klass')},")

    updated = ENTRY.sub(rename, body) if body == original else body
    if body != original:
        print("  apprentice.h already edited since vanilla; left alone")

    if not args.write:
        return 0
    APPRENTICES.write_text(updated, encoding="utf-8")
    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nwrote {APPRENTICES.relative_to(ROOT)} and {ROSTER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

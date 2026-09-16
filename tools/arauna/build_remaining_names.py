#!/usr/bin/env python3
"""Give an Arauna name to the last people who still answer to Hoenn.

build_character_names.py renames whoever the story work already renamed in
trainers.h, and reports the rest. The rest are the people the project never
named: the bike-shop man, the submarine captain, the old sailor and his gull,
the company president, the meteorite professor, the PC researcher, the family
of four on Route 111, and a signature on a letter.

The names are not decided here. They are the `arauna_name` column of
docs/arauna/ARAUNA_CHARACTER_NAMES.csv, so changing one is editing a cell and
running this again -- not editing code.

Two shapes need care and get it:

  * a title travels with the name. "MR. BRINEY" and a bare "BRINEY" are the
    same man, and both are renamed; the Renamer sorts longest-first, so the
    titled form wins where it appears and the bare form catches the rest.

  * STONE is the exception, and the reason this is not a plain word list. The
    president is MR. STONE and PRESIDENT STONE, but the game also sells MOON
    STONE, WATER STONE, FIRE STONE and LEAF STONE. Only the two titled forms
    are renamed; a bare STONE is left alone.

Lines get longer, so run rewrap_text.py afterwards and then check_text_width.py.

  --check   report what would be renamed
  --write   rewrite the text
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rename import Renamer, count  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ROSTER = ROOT / "docs/arauna/ARAUNA_CHARACTER_NAMES.csv"

# How each roster entry appears in the dialogue. The key is the CSV's
# hoenn_name; the value is every written form, with what the Arauna name looks
# like in that form. "{}" takes the new name.
FORMS = {
    "RYDEL":       [("RYDEL", "{}")],
    "SCOTT":       [("SCOTT", "{}")],
    "CAPT. STERN": [("CAPT. STERN", "CAPT. {}"), ("STERN", "{}")],
    "MR. BRINEY":  [("MR. BRINEY", "MR. {}"), ("BRINEY", "{}")],
    "PEEKO":       [("PEEKO", "{}")],
    # Never a bare STONE: MOON STONE, WATER STONE, FIRE STONE, LEAF STONE.
    "MR. STONE":   [("MR. STONE", "MR. {}"), ("PRESIDENT STONE", "PRESIDENT {}")],
    "COZMO":       [("PROF. COZMO", "PROF. {}"), ("COZMO", "{}")],
    "LANETTE":     [("LANETTE", "{}")],
    "WINSTRATE":   [("WINSTRATE", "{}")],
    "BILL":        [("BILL", "{}")],
}


def roster() -> dict[str, str]:
    with open(ROSTER, encoding="utf-8") as handle:
        return {row["hoenn_name"]: row["arauna_name"].strip()
                for row in csv.DictReader(handle)}


def mapping(names: dict[str, str]) -> dict[str, str]:
    out, missing = {}, []
    for hoenn, forms in FORMS.items():
        new = names.get(hoenn, "")
        if not new:
            missing.append(hoenn)
            continue
        for written, shape in forms:
            out[written] = shape.format(new)
    if missing:
        print("sem nome no CSV, nao renomeados: " + ", ".join(missing))
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.check == args.write:
        parser.error("use --check or --write")

    table = mapping(roster())
    if not table:
        print("nada a fazer")
        return 0

    renamer = Renamer(table)
    changed = renamer.apply()
    renamer.report()

    if args.write:
        for path, body in changed:
            path.write_text(body, encoding="utf-8")
        print(f"{len(changed)} arquivos reescritos")
        left = count(list(table))
        if left:
            print("ainda visivel: "
                  + ", ".join(f"{word} ({n})" for word, n in left.most_common()))
        else:
            print("nenhum nome de Hoenn destes sobrou em texto visivel")
    else:
        print(f"{len(changed)} arquivos mudariam")
    return 0


if __name__ == "__main__":
    sys.exit(main())

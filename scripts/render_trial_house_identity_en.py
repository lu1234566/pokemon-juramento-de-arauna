#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = (
    "data/maps/Route110/scripts.inc",
    "data/maps/Route110_TrickHouseEntrance/scripts.inc",
    "data/maps/Route110_TrickHouseCorridor/scripts.inc",
    "data/maps/Route110_TrickHouseEnd/scripts.inc",
    "data/maps/Route110_TrickHousePuzzle1/scripts.inc",
    "data/maps/Route110_TrickHousePuzzle2/scripts.inc",
    "data/maps/Route110_TrickHousePuzzle3/scripts.inc",
    "data/maps/Route110_TrickHousePuzzle4/scripts.inc",
    "data/maps/Route110_TrickHousePuzzle5/scripts.inc",
    "data/maps/Route110_TrickHousePuzzle6/scripts.inc",
    "data/maps/Route110_TrickHousePuzzle7/scripts.inc",
    "data/maps/Route110_TrickHousePuzzle8/scripts.inc",
    "data/text/trick_house_mechadolls.inc",
    "data/text/trainers.inc",
    "src/landmark.c",
)

REPLACEMENTS = (
    ("TRICK MASTER", "TRIAL KEEPER"),
    ("Trick Master", "Trial Keeper"),
    ("TRICK HOUSE", "TRIAL HOUSE"),
    ("Trick House", "Trial House"),
)


def render_one(source: str) -> tuple[str, int]:
    out = source
    changed = 0
    for old, new in REPLACEMENTS:
        count = out.count(old)
        if count:
            out = out.replace(old, new)
            changed += count
    return out, changed


def validate_tree(texts: dict[str, str]) -> None:
    forbidden = tuple(old for old, _ in REPLACEMENTS)
    for rel, text in texts.items():
        for token in forbidden:
            if token in text:
                raise ValueError(f"{rel}: visible legacy Trial House token survived: {token}")
        # Internal identifiers must remain Emerald-compatible.
        if "TrickHouse" not in text and "trick_house" not in rel and rel != "src/landmark.c" and rel != "data/text/trainers.inc":
            raise ValueError(f"{rel}: expected internal TrickHouse identity disappeared")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")

    rendered: dict[str, str] = {}
    total = 0
    for rel in FILES:
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        source = path.read_text(encoding="utf-8")
        out, count = render_one(source)
        rendered[rel] = out
        total += count

    if total == 0:
        raise ValueError("no visible Trick House identity anchors were found")
    validate_tree(rendered)

    if args.in_place:
        for rel, out in rendered.items():
            path = ROOT / rel
            if out != path.read_text(encoding="utf-8"):
                path.write_text(out, encoding="utf-8")

    print(f"Trial House English identity overlay OK: {total} visible replacements across {len(FILES)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

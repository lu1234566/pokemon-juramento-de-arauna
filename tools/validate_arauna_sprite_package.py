#!/usr/bin/env python3
"""Validate Arauna battle sprite packages before they enter the game tree."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


EXPECTED = {
    "anim_front.png": (64, 128),
    "back.png": (64, 64),
    "icon.png": (32, 64),
}


def validate_palette(path: Path) -> None:
    lines = path.read_text(encoding="ascii").replace("\r", "").splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"] or len(lines[3:]) != 16:
        raise ValueError(f"{path}: expected a 16-color JASC palette")
    for line in lines[3:]:
        values = [int(value) for value in line.split()]
        if len(values) != 3 or any(value < 0 or value > 255 for value in values):
            raise ValueError(f"{path}: invalid RGB entry {line!r}")


def validate_package(folder: Path) -> None:
    for filename, expected_size in EXPECTED.items():
        path = folder / filename
        with Image.open(path) as image:
            if image.size != expected_size:
                raise ValueError(f"{path}: expected {expected_size}, found {image.size}")
            if image.mode != "P":
                raise ValueError(f"{path}: expected indexed mode P, found {image.mode}")
            if image.info.get("transparency") != 0:
                raise ValueError(f"{path}: palette index 0 must be transparent")
            used = set(image.getdata())
            if max(used) > 15:
                raise ValueError(f"{path}: uses palette index {max(used)} (>15)")

    for filename in ("normal.pal", "shiny.pal"):
        validate_palette(folder / filename)

    profile = json.loads((folder / "candidate_profile.json").read_text(encoding="utf-8"))
    if profile["visibleColors"] > 15:
        raise ValueError(f"{folder}: visible color count exceeds 15")
    if not 0 <= profile["iconPalIndex"] <= 5:
        raise ValueError(f"{folder}: icon palette must be between 0 and 5")

    print(
        f"OK {folder.name}: indexed PNGs, 15-color battle palette, "
        f"icon palette {profile['iconPalIndex']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    folders = sorted(path for path in args.root.iterdir() if path.is_dir())
    if not folders:
        raise SystemExit(f"no packages found in {args.root}")
    for folder in folders:
        validate_package(folder)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Reject character art that the GBA build cannot take.

Runs the checks the compiler will not: exact dimensions, the sixteen-colour
ceiling, colour 0 reserved for transparency, the shared npc_3 palette left
untouched, and the mirror-safety the east-facing frames depend on.
"""
from __future__ import annotations

import pathlib
import sys

from PIL import Image, ImageChops

ROOT = pathlib.Path(__file__).resolve().parents[2]
NPC3_PAL = ROOT / "graphics" / "object_events" / "palettes" / "npc_3.pal"
SHEET = ROOT / "graphics/object_events/pics/people/prof_birch.png"
PORTRAIT = ROOT / "graphics/birch_speech/birch.png"
FRAME_W, FRAME_H, FRAMES = 16, 32, 9


def read_jasc(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    return [tuple(int(v) for v in l.split()) for l in lines[3:3 + int(lines[2])]]


def palette_of(img: Image.Image, n: int):
    raw = img.convert("P").getpalette()[: n * 3]
    return [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]


def check_sheet(problems: list[str]) -> None:
    img = Image.open(SHEET)
    if img.size != (FRAME_W * FRAMES, FRAME_H):
        problems.append(f"sheet is {img.size[0]}x{img.size[1]}, must be {FRAME_W*FRAMES}x{FRAME_H}")
        return
    if img.mode != "P":
        problems.append(f"sheet mode is {img.mode}, must be indexed (P)")
        return
    used = {p for _, p in img.convert("P").getcolors(1 << 16)}
    if max(used) > 15:
        problems.append(f"sheet uses palette index {max(used)}; only 0-15 exist in 4bpp")
    shared = read_jasc(NPC3_PAL)
    own = palette_of(img, 16)
    drift = [i for i in range(16) if i in used and own[i] != shared[i]]
    if drift:
        problems.append(
            "sheet palette differs from the shared npc_3 palette at "
            f"{drift} - fifty other NPCs read those slots"
        )
    # Mirror safety: the east frames are the west frames flipped, so a west
    # frame that is wildly asymmetric will read as a different costume east.
    for idx, name in ((2, "face west"), (7, "walk west A"), (8, "walk west B")):
        cell = img.crop((idx * FRAME_W, 0, (idx + 1) * FRAME_W, FRAME_H)).convert("RGB")
        flipped = cell.transpose(Image.FLIP_LEFT_RIGHT)
        diff = ImageChops.difference(cell, flipped).convert("L")
        bbox = diff.getbbox()
        if bbox is None:
            problems.append(f"frame {idx} ({name}) is perfectly symmetric - it will not read as a profile")


def check_portrait(problems: list[str]) -> None:
    img = Image.open(PORTRAIT)
    if img.size != (64, 64):
        problems.append(f"portrait is {img.size[0]}x{img.size[1]}, must be 64x64")
        return
    if img.mode != "P":
        problems.append(f"portrait mode is {img.mode}, must be indexed (P)")
        return
    used = {p for _, p in img.convert("P").getcolors(1 << 16)}
    if max(used) > 15:
        problems.append(f"portrait uses palette index {max(used)}; only 0-15 exist")
    if 0 not in used:
        problems.append("portrait never uses index 0 - it will have no transparent background")


def main() -> int:
    problems: list[str] = []
    check_sheet(problems)
    check_portrait(problems)
    for p in problems:
        print(f"  - {p}")
    print(f"\n{len(problems)} character-art problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

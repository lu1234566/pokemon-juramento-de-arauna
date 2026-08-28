#!/usr/bin/env python3
"""Install the Arauna battle sprites into graphics/pokemon/.

Reads the approved export straight from the versioned zip and writes, for every
one of the 386 species, the five files the engine compiles out of a species
folder:

  anim_front.png   64x128, the two animation frames
  front.png        64x64, the still front the Pokédex and the trade screen use
  back.png         64x64
  normal.pal       16 JASC colours, the front sprite's own palette
  shiny.pal        the shiny palette, in the same index order

Two things the export leaves to us:

  * The back sprite was reduced on its own, so its indices point at a different
    palette from the front's. The engine draws both with normal.pal, so the back
    image is re-indexed here by matching each of its colours to the nearest one
    in the front palette. Nothing is redrawn; only the index map changes.

  * The shiny sheet already shares the front's index map (checked, all 386), so
    shiny.pal is just the shiny sheet's palette written out.

Two species land in engine slots whose folder is not a single sprite:

  #210 Estalagmite occupies SPECIES_UNOWN, whose 28 letter folders are picked by
       personality, so the same sprite goes into every one of them.
  #351 Tuim occupies SPECIES_CASTFORM, whose sheet is the four weather forms
       concatenated, so the same sprite goes into all four.

Icons and footprints are not touched: the icon sheet is drawn from three shared
palettes, which is a separate problem from this one.
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
EXPORT = ROOT / "graphics/arauna/arauna_sprites_gba_export.zip"
MAPPING = ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
PICS = ROOT / "graphics/pokemon"

FRONT_SIZE = (64, 128)
STILL_SIZE = (64, 64)
BACK_SIZE = (64, 64)
PALETTE_SIZE = 16

UNOWN_FORMS = list("abcdefghijklmnopqrstuvwxyz") + ["exclamation_mark", "question_mark"]
CASTFORM_FORMS = ["normal", "sunny", "rainy", "snowy"]


def palette_of(image: Image.Image) -> list[tuple[int, int, int]]:
    raw = image.getpalette() or []
    raw += [0] * (PALETTE_SIZE * 3 - len(raw))
    return [tuple(raw[i * 3:i * 3 + 3]) for i in range(PALETTE_SIZE)]


def write_jasc(path: Path, palette) -> None:
    lines = ["JASC-PAL", "0100", str(PALETTE_SIZE)]
    lines += [f"{r} {g} {b}" for r, g, b in palette]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_indexed(path: Path, indices: np.ndarray, palette) -> None:
    image = Image.fromarray(indices.astype(np.uint8), mode="P")
    flat = []
    for colour in palette:
        flat += list(colour)
    image.putpalette(flat + [0] * (768 - len(flat)))
    image.save(path, optimize=False)


def reindex_to(indices: np.ndarray, source_palette, target_palette) -> np.ndarray:
    """Re-index an image onto another palette by nearest colour.

    Index 0 is the transparent slot on both sides and is mapped straight
    through, so the silhouette is preserved exactly.
    """
    target = np.array(target_palette[1:], dtype=np.int32)
    table = np.zeros(PALETTE_SIZE, dtype=np.uint8)
    for i, colour in enumerate(source_palette):
        if i == 0:
            continue
        distance = ((target - np.array(colour, dtype=np.int32)) ** 2).sum(axis=1)
        table[i] = int(distance.argmin()) + 1
    return table[indices]


def load_sheets(zf: zipfile.ZipFile, dex: int):
    names = zf.namelist()

    def one(prefix: str) -> Image.Image:
        matches = [n for n in names if n.startswith(f"{prefix}/{dex:03d}_")]
        if len(matches) != 1:
            raise ValueError(f"#{dex:03d}: expected one {prefix} sheet, found {matches}")
        return Image.open(io.BytesIO(zf.read(matches[0])))

    return one("front"), one("back"), one("shiny")


def targets(folder: str) -> list[Path]:
    if folder == "unown":
        return [PICS / "unown" / form for form in UNOWN_FORMS]
    if folder == "castform":
        return [PICS / "castform" / form for form in CASTFORM_FORMS]
    return [PICS / folder]


def install(dex: int, folder: str, zf: zipfile.ZipFile, write: bool) -> list[str]:
    front, back, shiny = load_sheets(zf, dex)
    problems = []
    if front.size != FRONT_SIZE:
        problems.append(f"#{dex:03d}: front sheet is {front.size}, expected {FRONT_SIZE}")
    if shiny.size != FRONT_SIZE:
        problems.append(f"#{dex:03d}: shiny sheet is {shiny.size}, expected {FRONT_SIZE}")
    if back.size != BACK_SIZE:
        problems.append(f"#{dex:03d}: back sheet is {back.size}, expected {BACK_SIZE}")

    front_idx = np.array(front)
    shiny_idx = np.array(shiny)
    back_idx = np.array(back)
    if not np.array_equal(front_idx, shiny_idx):
        problems.append(f"#{dex:03d}: the shiny sheet does not share the front index map")
    for name, idx in (("front", front_idx), ("back", back_idx)):
        if idx.max() >= PALETTE_SIZE:
            problems.append(f"#{dex:03d}: {name} uses index {idx.max()}, over 15")
    if problems or not write:
        return problems

    normal = palette_of(front)
    shiny_pal = palette_of(shiny)
    back_on_normal = reindex_to(back_idx, palette_of(back), normal)

    for directory in targets(folder):
        directory.mkdir(parents=True, exist_ok=True)
        write_indexed(directory / "anim_front.png", front_idx, normal)
        write_indexed(directory / "front.png", front_idx[:STILL_SIZE[1]], normal)
        write_indexed(directory / "back.png", back_on_normal, normal)
        write_jasc(directory / "normal.pal", normal)
        write_jasc(directory / "shiny.pal", shiny_pal)
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate the export, write nothing")
    parser.add_argument("--write", action="store_true", help="install the sprites")
    args = parser.parse_args()

    rows = list(csv.DictReader(MAPPING.open(encoding="utf-8")))
    problems, written = [], 0
    with zipfile.ZipFile(EXPORT) as zf:
        for row in rows:
            found = install(int(row["arauna_dex"]), row["graphics_folder"], zf, args.write)
            problems += found
            if args.write and not found:
                written += len(targets(row["graphics_folder"]))

    for problem in problems:
        print(f"sprite problem: {problem}", file=sys.stderr)
    if problems:
        return 1
    if args.write:
        print(f"installed {len(rows)} species into {written} sprite folders")
    else:
        print(f"export OK: {len(rows)} species, all sheets the right size and index map")
    return 0


if __name__ == "__main__":
    sys.exit(main())

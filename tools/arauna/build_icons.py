#!/usr/bin/env python3
"""Build the party/box icons for the Arauna dex.

Every icon in the game is drawn from one of a handful of palettes shared by the
whole dex, so the icons cannot simply be reduced one at a time the way the
battle sprites were. This tool does the whole set at once:

  1. each species' icon is the front sprite scaled down to 32x32;
  2. the 386 species are grouped into six colour families;
  3. each family gets a 15-colour palette fitted to the pixels of its members;
  4. every icon is re-indexed onto its family's palette.

Six rather than three: gMonIconPaletteTable already declares six entries and
LoadMonIconPalettes already loads all six, but only three of them ever pointed
at real data. Filling the other three costs no sprite palette slots, since they
are already reserved. It is a modest win -- mean colour error 31.2 against 33.7
-- because what really limits an icon is its own fifteen colours, not how many
families share a palette.

Outputs:

  graphics/pokemon/<folder>/icon.png            32x64, the two bob frames
  graphics/pokemon/icon_palettes/icon_palette_[0-5].pal
  src/data/pokemon/icon_palette_indices.h       which family each species uses

Footprints are not touched. They are 16x16 two-colour paw prints and nothing in
the export corresponds to them.
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
ICON_PALETTES = PICS / "icon_palettes"
INDICES_H = ROOT / "src/data/pokemon/icon_palette_indices.h"

ICON_SIZE = 32
FAMILIES = 6
COLOURS = 15                       # index 0 is the transparent slot
TRANSPARENT = (98, 156, 131)       # the colour vanilla icon palettes park there
BOB_MARGIN = 1                     # frame two sits a pixel lower, as vanilla does
REFINEMENTS = 4                    # rounds of reassign-and-refit

UNOWN_FORMS = list("abcdefghijklmnopqrstuvwxyz") + ["exclamation_mark", "question_mark"]
CASTFORM_FORMS = ["normal", "sunny", "rainy", "snowy"]


def targets(folder: str) -> list[Path]:
    if folder == "unown":
        return [PICS / "unown" / form for form in UNOWN_FORMS]
    if folder == "castform":
        return [PICS / "castform"]
    return [PICS / folder]


def scaled_icon(sheet: Image.Image) -> tuple[np.ndarray, np.ndarray]:
    """Front sheet -> a 32x32 RGB array plus its opacity mask."""
    palette = sheet.getpalette() or []
    indices = np.array(sheet)[:64]
    rgb = np.zeros((64, 64, 4), dtype=np.uint8)
    for value in np.unique(indices):
        base = int(value) * 3
        colour = palette[base:base + 3] if base + 2 < len(palette) else [0, 0, 0]
        mask = indices == value
        rgb[mask, 0], rgb[mask, 1], rgb[mask, 2] = colour
        rgb[mask, 3] = 0 if value == 0 else 255
    small = Image.fromarray(rgb, "RGBA").resize((ICON_SIZE, ICON_SIZE), Image.LANCZOS)
    array = np.array(small)
    opaque = array[:, :, 3] >= 128
    return array[:, :, :3], opaque


def kmeans(points: np.ndarray, k: int, iterations: int = 40, seed: int = 20260828) -> np.ndarray:
    """Plain k-means, seeded so a rerun produces the same palettes."""
    rng = np.random.default_rng(seed)
    centres = points[rng.choice(len(points), size=min(k, len(points)), replace=False)].astype(float)
    for _ in range(iterations):
        distance = ((points[:, None, :].astype(float) - centres[None, :, :]) ** 2).sum(axis=2)
        labels = distance.argmin(axis=1)
        for i in range(len(centres)):
            member = points[labels == i]
            if len(member):
                centres[i] = member.mean(axis=0)
    return labels


def fit_palette(pixels: np.ndarray) -> list[tuple[int, int, int]]:
    """Median-cut a family's pixels down to the fifteen colours it may use."""
    side = int(np.ceil(np.sqrt(len(pixels))))
    canvas = np.zeros((side * side, 3), dtype=np.uint8)
    canvas[:len(pixels)] = pixels
    canvas[len(pixels):] = pixels[-1] if len(pixels) else 0
    image = Image.fromarray(canvas.reshape(side, side, 3), "RGB")
    reduced = image.quantize(colors=COLOURS, method=Image.MEDIANCUT, dither=Image.NONE)
    raw = reduced.getpalette()[:COLOURS * 3]
    return [tuple(raw[i * 3:i * 3 + 3]) for i in range(COLOURS)]


def reindex(rgb: np.ndarray, opaque: np.ndarray, palette) -> np.ndarray:
    colours = np.array(palette, dtype=np.int32)
    flat = rgb.reshape(-1, 3).astype(np.int32)
    distance = ((flat[:, None, :] - colours[None, :, :]) ** 2).sum(axis=2)
    indices = (distance.argmin(axis=1) + 1).reshape(rgb.shape[:2]).astype(np.uint8)
    indices[~opaque] = 0
    return indices


def write_jasc(path: Path, palette) -> None:
    lines = ["JASC-PAL", "0100", "16"] + [f"{r} {g} {b}" for r, g, b in palette]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def write_icon(path: Path, indices: np.ndarray, palette) -> None:
    second = np.zeros_like(indices)
    if not indices[-BOB_MARGIN:, :].any():
        second[BOB_MARGIN:, :] = indices[:-BOB_MARGIN, :]
    else:
        second = indices
    sheet = np.vstack([indices, second])
    image = Image.fromarray(sheet, mode="P")
    flat = []
    for colour in palette:
        flat += list(colour)
    image.putpalette(flat + [0] * (768 - len(flat)))
    image.save(path, optimize=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    rows = list(csv.DictReader(MAPPING.open(encoding="utf-8")))
    icons = {}
    with zipfile.ZipFile(EXPORT) as zf:
        names = zf.namelist()
        for row in rows:
            dex = int(row["arauna_dex"])
            match = [n for n in names if n.startswith(f"front/{dex:03d}_")][0]
            icons[dex] = scaled_icon(Image.open(io.BytesIO(zf.read(match))))

    means = np.array([icons[int(r["arauna_dex"])][0][icons[int(r["arauna_dex"])][1]].mean(axis=0)
                      for r in rows])
    labels = kmeans(means, FAMILIES)

    dexes = [int(r["arauna_dex"]) for r in rows]
    assignment = {dex: int(label) for dex, label in zip(dexes, labels)}

    def fit(assign):
        out = []
        for family in range(FAMILIES):
            members = [d for d in dexes if assign[d] == family]
            pixels = np.concatenate([icons[d][0][icons[d][1]] for d in members]) if members else \
                np.array([[0, 0, 0]], dtype=np.uint8)
            out.append([TRANSPARENT] + fit_palette(pixels))
        return out

    def cost(dex, palette):
        rgb, opaque = icons[dex]
        colours = np.array(palette[1:], dtype=np.int32)
        flat = rgb[opaque].astype(np.int32)
        distance = ((flat[:, None, :] - colours[None, :, :]) ** 2).sum(axis=2)
        return float(np.sqrt(distance.min(axis=1)).mean())

    # The mean colour is only a starting guess. Refit the palettes, move every
    # species to whichever palette actually renders it best, and repeat; the
    # error settles after a couple of rounds.
    palettes = fit(assignment)
    for _ in range(REFINEMENTS):
        moved = 0
        for dex in dexes:
            best = min(range(FAMILIES), key=lambda f: cost(dex, palettes[f]))
            if best != assignment[dex]:
                assignment[dex] = best
                moved += 1
        palettes = fit(assignment)
        if not moved:
            break

    error = [cost(dex, palettes[assignment[dex]]) for dex in dexes]
    print(f"{FAMILIES} families, mean colour error {np.mean(error):.1f} of 255 "
          f"(worst species {np.max(error):.1f})")
    for family in range(FAMILIES):
        print(f"  family {family}: {sum(1 for v in assignment.values() if v == family)} species")

    if not args.write:
        return 0

    ICON_PALETTES.mkdir(parents=True, exist_ok=True)
    for family, palette in enumerate(palettes):
        write_jasc(ICON_PALETTES / f"icon_palette_{family}.pal", palette)

    for row in rows:
        dex = int(row["arauna_dex"])
        rgb, opaque = icons[dex]
        palette = palettes[assignment[dex]]
        indices = reindex(rgb, opaque, palette[1:])
        for directory in targets(row["graphics_folder"]):
            directory.mkdir(parents=True, exist_ok=True)
            write_icon(directory / "icon.png", indices, palette)

    lines = ["// Generated by tools/arauna/build_icons.py from the approved Arauna dex.",
             "// Edit nothing here; rerun the tool instead.", ""]
    for row in rows:
        dex = int(row["arauna_dex"])
        lines.append(f"    [{row['species_constant']}] = {assignment[dex]}, "
                     f"// #{dex:03d} {row['full_name']}")
    source = (ROOT / "src/pokemon_icon.c").read_text(encoding="utf-8")
    used = {r["species_constant"] for r in rows}
    for name in ("SPECIES_NONE", "SPECIES_EGG"):
        if name not in used:
            lines.append(f"    [{name}] = 0,")
    for match in sorted(set(m for m in __import__("re").findall(r"\[(SPECIES_\w+)\] = \d,", source))):
        if match not in used and match not in ("SPECIES_NONE", "SPECIES_EGG"):
            lines.append(f"    [{match}] = 0,")
    INDICES_H.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {len(rows)} icons, {FAMILIES} palettes and "
          f"{INDICES_H.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

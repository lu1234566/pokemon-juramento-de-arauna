#!/usr/bin/env python3
"""Integrate the high-art back sprites into the fakemon graphics header.

The Arauna dex (species 217..386) ships its battle back sprites from a separate,
higher-resolution art export than the one that produced the front sprites. Each
back is delivered as a 1254x1254 RGBA image with the creature on a transparent
(black-keyed) field; it is downscaled to 64x64 with a premultiplied-alpha box
before it reaches this tool, so transparent pixels never bleed their colour into
the edge (a plain resize leaves a black fringe, since the key colour is black).

The catch is the palette. In pokeemerald a species has ONE 16-colour palette,
shared by its front and back battle sprites, so a back sprite cannot simply be
recoloured freely -- whatever palette it uses, the front must use too. This tool
resolves that per species with the smallest change that keeps both faithful:

  keep        the back already lands within MAX_ERROR of the existing
              gAraunaPalette_NNN. Re-encode the back; front/palette untouched.

  rebuild     it does not. Build a fresh 15-colour palette by median-cut over
              BOTH sprites' pixels, weighting the back up until it holds a fair
              share of the colour budget, and search weightings for the lightest
              one that lands BOTH front and back within MAX_ERROR. Re-index and
              re-encode front and back against it, rewrite the palette, and
              regenerate the shiny palette by inheriting each new colour's
              nearest old-colour recolour.

  residual    no shared 16-colour palette holds the back within tolerance
              without pushing the front past it. Leave front/palette/shiny
              untouched, emit the best-effort back against the existing palette,
              and report the species rather than damage the front for a back
              that still would not pass.

  undersized  the downscaled back creature is far shorter than its own front
              (check_sprite_health's rule); the engine would draw a tiny back
              sprite. Revert the species entirely and report it.

Only species 217..386 are considered; 1..216 are left byte-for-byte identical.
The result is guarded by the same checks CI runs: check_sprite_health.py,
fix_sprite_transparency.py --check and validate_packed_arauna_dex.py.

    python3 tools/arauna/integrate_back_sprites.py \
        --art graphics/arauna/back_highart_64x64 --report docs/arauna/BACK_SPRITE_INTEGRATION.csv

Requires Pillow and numpy (an authoring-time dependency, like the PIL the packer
already uses); it never runs in CI.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/arauna"))
from pack_arauna_graphics_header import lz77_compress, lz77_decompress, c_array
import check_sprite_health as H

HEADER = ROOT / "src/data/graphics/arauna_fakemon_graphics.h"
FIRST, LAST = 217, 386
MAX_ERROR = 25.0            # mean opaque-pixel RGB error gate (0..441), matches convert tool
TRANSPARENT = 0x7C1F        # magenta, transparent slot at index 0
ALPHA_THRESH = 128          # hard alpha cut, matches convert_back_sprites_to_4bit
WEIGHTS = (1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0)  # back:front mass ratios to search


def expand(c):  # RGB555 word -> displayed 8-bit RGB (project formula, max 248)
    return ((c & 31) * 8, ((c >> 5) & 31) * 8, ((c >> 10) & 31) * 8)


def to555(r, g, b):
    return (r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10)


def pack_4bpp(grid, width, height):
    """Indices grid -> GBA 4bpp tile bytes (inverse of check_sprite_health.to_grid)."""
    out = bytearray()
    for ty in range(0, height, 8):
        for tx in range(0, width, 8):
            for row in range(8):
                for byte in range(4):
                    lo = grid[ty + row][tx + byte * 2] & 0xF
                    hi = grid[ty + row][tx + byte * 2 + 1] & 0xF
                    out.append(lo | (hi << 4))
    return bytes(out)


def nearest(colours, palette):
    """colours (N,3), palette (K,3) -> (index into palette, euclidean distance)."""
    c = colours.astype(np.int32)[:, None, :]
    p = palette.astype(np.int32)[None, :, :]
    d2 = ((c - p) ** 2).sum(axis=2)
    idx = d2.argmin(axis=1)
    return idx, np.sqrt(d2[np.arange(len(idx)), idx])


def median_cut(pixels, k=15):
    """Median-cut `pixels` (N,3) into up to k representative RGB tuples."""
    boxes = [pixels]
    while len(boxes) < k:
        best_i, best_rng = -1, -1
        for i, bx in enumerate(boxes):
            if len(bx) < 2:
                continue
            rng = int((bx.max(axis=0) - bx.min(axis=0)).max())
            if rng > best_rng:
                best_rng, best_i = rng, i
        if best_rng <= 0:
            break
        bx = boxes[best_i]
        ch = int((bx.max(axis=0) - bx.min(axis=0)).argmax())
        bx = bx[bx[:, ch].argsort()]
        m = len(bx) // 2
        boxes[best_i:best_i + 1] = [bx[:m], bx[m:]]
    return [tuple(int(v) for v in bx.mean(axis=0).round()) for bx in boxes if len(bx)]


def load_palette(text, name):
    m = re.search(r"const u16 %s\[\][^=]*=\s*\{([^}]*)\}" % re.escape(name), text)
    vals = [int(v.strip(), 16) for v in m.group(1).replace("\n", "").split(",") if v.strip()]
    assert len(vals) == 16, (name, len(vals))
    return vals


def replace_array(text, decl):
    name = re.match(r"const u\d+ (\w+)\[\]", decl).group(1)
    pat = re.compile(r"const u\d+ %s\[\][^=]*=\s*\{[^}]*\};\n?" % re.escape(name))
    new = decl if decl.endswith("\n") else decl + "\n"
    text, n = pat.subn(lambda _: new, text, count=1)
    assert n == 1, f"could not locate array {name}"
    return text


def encode_back(grid):
    raw = pack_4bpp(grid, 64, 64)
    lz = lz77_compress(raw)
    assert lz77_decompress(lz) == raw
    return lz


def integrate(art_dir, verbose=False):
    text = HEADER.read_text(encoding="ascii")
    arrays = H.load()
    report = []  # (num, action, back_error, front_after_error)

    for num in range(FIRST, LAST + 1):
        slot = f"{num:03d}"
        png = Path(art_dir) / f"{num:03d}.png"
        if not png.exists():
            report.append((num, "missing", None, None)); continue

        pal = load_palette(text, f"gAraunaPalette_{slot}")
        shiny = load_palette(text, f"gAraunaShinyPalette_{slot}")
        pal_rgb = np.array([expand(c) for c in pal])
        opaque_idx = np.arange(1, 16)

        img = np.array(Image.open(png).convert("RGBA"))
        mask = img[:, :, 3] >= ALPHA_THRESH
        back_rgb = img[:, :, :3][mask]
        if len(back_rgb) == 0:
            report.append((num, "empty", None, None)); continue

        # Undersized guard (mirrors check_sprite_health) -- depends only on the
        # alpha mask, so decide before any recolour and revert if it trips.
        front0 = H.to_grid(H.pixels_of(arrays, f"gAraunaFrontPic_{slot}"))[:64]
        frows = [y for y in range(64) if any(front0[y])]
        front_tall = (frows[-1] - frows[0] + 1) if frows else 0
        brows = np.where(mask.any(axis=1))[0]
        back_tall = int(brows[-1] - brows[0] + 1) if len(brows) else 0
        if back_tall * 1.7 < front_tall:
            report.append((num, "undersized", None, None)); continue

        ys, xs = np.where(mask)
        idx, dist = nearest(back_rgb, pal_rgb[1:])
        back_err = float(dist.mean())

        if back_err <= MAX_ERROR:
            grid = [[0] * 64 for _ in range(64)]
            for y, x, v in zip(ys, xs, opaque_idx[idx]):
                grid[y][x] = int(v)
            text = replace_array(text, c_array(f"gAraunaBackPic_{slot}", "u32", encode_back(grid), 4))
            report.append((num, "keep", back_err, 0.0))
            continue

        # ---- combined-palette rebuild ----
        front_arr = np.array(H.to_grid(H.pixels_of(arrays, f"gAraunaFrontPic_{slot}")))
        fh = len(front_arr)
        fmask = front_arr != 0
        fys, fxs = np.where(fmask)
        front_rgb = pal_rgb[front_arr[fmask]]

        def build(ratio):
            n = max(1, int(round(ratio * len(front_rgb) / max(1, len(back_rgb)))))
            reps = median_cut(np.vstack([front_rgb] + [back_rgb] * n), 15)
            r555 = [to555(*c) for c in reps]
            npal = [TRANSPARENT] + r555
            while len(npal) < 16:
                npal.append(r555[-1])
            npal = npal[:16]
            nrgb = np.array([expand(c) for c in npal])
            be = float(nearest(back_rgb, nrgb[1:])[1].mean())
            fe = float(nearest(front_rgb, nrgb[1:])[1].mean())
            return npal, nrgb, be, fe

        trials = [(r,) + build(r) for r in WEIGHTS]
        feasible = [t for t in trials if t[3] <= MAX_ERROR and t[4] <= MAX_ERROR]
        if not feasible:
            grid = [[0] * 64 for _ in range(64)]
            for y, x, v in zip(ys, xs, opaque_idx[idx]):
                grid[y][x] = int(v)
            text = replace_array(text, c_array(f"gAraunaBackPic_{slot}", "u32", encode_back(grid), 4))
            report.append((num, "residual", back_err, 0.0))
            if verbose:
                best = min(trials, key=lambda t: t[3])
                print(f"  #{slot} residual: back {back_err:.1f} "
                      f"(best rebuild back={best[3]:.1f} front={best[4]:.1f})")
            continue

        _, new_pal, new_rgb, new_back_err, front_after = min(feasible, key=lambda t: t[4])
        new_opaque = new_rgb[1:]

        new_front = [[0] * 64 for _ in range(fh)]
        for y, x, v in zip(fys, fxs, nearest(front_rgb, new_opaque)[0] + 1):
            new_front[y][x] = int(v)
        new_back = [[0] * 64 for _ in range(64)]
        for y, x, v in zip(ys, xs, nearest(back_rgb, new_opaque)[0] + 1):
            new_back[y][x] = int(v)

        new_shiny = [shiny[0]]
        for j in range(1, 16):
            new_shiny.append(shiny[int(((pal_rgb - new_rgb[j]) ** 2).sum(axis=1).argmin())])

        front_raw = pack_4bpp(new_front, 64, fh)
        front_lz = lz77_compress(front_raw)
        assert lz77_decompress(front_lz) == front_raw
        text = replace_array(text, c_array(f"gAraunaFrontPic_{slot}", "u32", front_lz, 4))
        text = replace_array(text, c_array(f"gAraunaBackPic_{slot}", "u32", encode_back(new_back), 4))
        text = replace_array(text, c_array(f"gAraunaPalette_{slot}", "u16", new_pal, 2))
        text = replace_array(text, c_array(f"gAraunaShinyPalette_{slot}", "u16", new_shiny, 2))
        report.append((num, "rebuild", new_back_err, front_after))
        if verbose:
            print(f"  #{slot} rebuild: back {back_err:.1f}->{new_back_err:.1f} front 0->{front_after:.1f}")

    return text, report


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--art", type=Path, default=ROOT / "graphics/arauna/back_highart_64x64",
                    help="directory of 64x64 RGBA back sprites named NNN.png")
    ap.add_argument("--report", type=Path, help="write a per-species outcome CSV here")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not args.art.is_dir():
        ap.error(f"art directory not found: {args.art}")

    text, report = integrate(args.art, verbose=args.verbose)
    HEADER.write_text(text, encoding="ascii")

    from collections import Counter
    counts = Counter(a for _, a, _, _ in report)
    order = ["keep", "rebuild", "residual", "undersized", "missing", "empty"]
    summary = ", ".join(f"{k}={counts[k]}" for k in order if counts.get(k))
    faithful = counts["keep"] + counts["rebuild"]
    print(f"integrated back sprites for species {FIRST}..{LAST}: {summary}")
    print(f"  {faithful}/{LAST - FIRST + 1} within {MAX_ERROR:g} colour error")
    residual = [n for n, a, _, _ in report if a in ("residual", "undersized")]
    if residual:
        print(f"  reported (not faithfully deliverable): {residual}")

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["species", "action", "back_error", "front_after_error"])
            for n, a, b, fr in report:
                w.writerow([n, a, f"{b:.1f}" if b is not None else "",
                            f"{fr:.1f}" if fr is not None else ""])
        print(f"  wrote report {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

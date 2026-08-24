#!/usr/bin/env python3
"""Import Arauna creature art over the Emerald species slots, by dex number.

Each species folder carries one `normal.pal` that the front, the animated
front and the back sprite all read from, so the three cannot be quantized
independently: a back reduced on its own gets a palette the front does not
share, and the creature changes colour when the battle flips to your side.
This importer therefore builds a single sixteen-colour palette per species
from every source image at once, then maps all of them onto it.

Source files are named by dex number, e.g. `001_caramelo.png` for the front
and `001_caramelo_back.png` for the back. The dex number selects the Emerald
species occupying that slot, so `001` lands in graphics/pokemon/bulbasaur/.

Nothing is written unless every target for that species converts cleanly.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
SPECIES_H = ROOT / "include" / "constants" / "species.h"
GRAPHICS_H = ROOT / "src" / "data" / "graphics" / "pokemon.h"
SPRITE_SIZE = (64, 64)
MAX_COLORS = 16          # index 0 is the transparency key
KEY = (152, 208, 160)    # the green pokeemerald uses for transparent pixels


def dex_to_folder() -> dict[int, str]:
    """Map a National Dex number to the graphics folder for that creature.

    Emerald's internal species ids only match the National Dex up to 251; the
    Hoenn block is stored in a different order, so SPECIES_TREECKO is 277 while
    its dex number is 252. The NATIONAL_DEX_* enum is declared in dex order
    starting at NATIONAL_DEX_NONE, so its position gives the real number.
    """
    dex_text = (ROOT / "include" / "constants" / "pokedex.h").read_text(encoding="utf-8")
    body = dex_text[dex_text.index("enum {"):]
    names = re.findall(r"^\s*NATIONAL_DEX_([A-Z0-9_]+),", body, re.M)
    dex_by_name = {}
    for i, name in enumerate(names):
        if name == "NONE":
            continue
        dex_by_name.setdefault(name, i)

    folders = {}
    for m in re.finditer(
        r'gMonBackPic_(\w+)\[\]\s*=\s*INCGFX_U32\("graphics/pokemon/([^/]+)/back\.png"',
        GRAPHICS_H.read_text(encoding="utf-8"),
    ):
        folders[m.group(1)] = m.group(2)

    out = {}
    for symbol, folder in folders.items():
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", symbol).upper()
        if name in dex_by_name:
            out[dex_by_name[name]] = folder
    return out


def load(path: pathlib.Path) -> Image.Image:
    img = Image.open(path).convert("RGBA")
    return trim(img)


def trim(img: Image.Image) -> Image.Image:
    bbox = img.getchannel("A").getbbox()
    return img.crop(bbox) if bbox else img


def fit(img: Image.Image) -> Image.Image:
    """Scale to fit the 64x64 cell, anchored to the bottom like the originals."""
    tw, th = SPRITE_SIZE
    w, h = img.size
    scale = min(tw / w, th / h)
    small = img.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    cell = Image.new("RGBA", SPRITE_SIZE, (0, 0, 0, 0))
    cell.paste(small, ((tw - small.width) // 2, th - small.height), small)
    return cell


def joint_palette(images: list[Image.Image]) -> list[tuple[int, int, int]]:
    """One palette for every sprite of a species, so they stay consistent."""
    strip = Image.new("RGB", (SPRITE_SIZE[0] * len(images), SPRITE_SIZE[1]), KEY)
    for i, img in enumerate(images):
        strip.paste(img.convert("RGB"), (i * SPRITE_SIZE[0], 0), img)
    reduced = strip.quantize(colors=MAX_COLORS - 1, method=Image.MEDIANCUT)
    raw = reduced.getpalette()[: (MAX_COLORS - 1) * 3]
    return [KEY] + [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]


def nearest(color, palette) -> int:
    r1, g1, b1 = color
    best, best_d = 1, None
    for i in range(1, len(palette)):
        r2, g2, b2 = palette[i]
        rm = (r1 + r2) / 2
        d = ((2 + rm / 256) * (r1 - r2) ** 2 + 4 * (g1 - g2) ** 2
             + (2 + (255 - rm) / 256) * (b1 - b2) ** 2)
        if best_d is None or d < best_d:
            best, best_d = i, d
    return best


def to_indexed(img: Image.Image, palette) -> Image.Image:
    out = Image.new("P", img.size)
    flat = [c for rgb in palette for c in rgb]
    out.putpalette(flat + [0, 0, 0] * (256 - len(palette)))
    src, dst = img.convert("RGB").load(), out.load()
    alpha = img.getchannel("A").load()
    cache: dict = {}
    for y in range(img.height):
        for x in range(img.width):
            if alpha[x, y] < 128:
                dst[x, y] = 0
                continue
            c = src[x, y]
            if c not in cache:
                cache[c] = nearest(c, palette)
            dst[x, y] = cache[c]
    return out


def write_pal(path: pathlib.Path, palette) -> None:
    lines = ["JASC-PAL", "0100", str(len(palette))]
    lines += [f"{r} {g} {b}" for r, g, b in palette]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=pathlib.Path, help="directory of NNN_slug[_back].png files")
    ap.add_argument("--apply", action="store_true", help="write the files (default is a dry run)")
    ap.add_argument("--only", type=int, nargs="*", help="restrict to these dex numbers")
    ap.add_argument("--allow-partial", action="store_true",
                    help="import a species even when only one view is supplied")
    args = ap.parse_args()

    mapping = dex_to_folder()
    by_dex: dict[int, dict[str, pathlib.Path]] = {}
    for path in sorted(args.source.glob("*.png")):
        m = re.match(r"^(\d{1,3})_(.+?)(_back)?\.png$", path.name)
        if not m:
            print(f"  skipped (name not NNN_slug[_back].png): {path.name}")
            continue
        dex = int(m.group(1))
        by_dex.setdefault(dex, {})["back" if m.group(3) else "front"] = path

    ok = failed = 0
    for dex in sorted(by_dex):
        if args.only and dex not in args.only:
            continue
        folder = mapping.get(dex)
        if folder is None:
            print(f"  {dex:03d}: no Emerald species occupies that dex slot")
            failed += 1
            continue
        parts = by_dex[dex]
        # normal.pal is shared, so importing one view alone would rewrite the
        # palette around it and recolour the view left behind.
        if not args.allow_partial and set(parts) != {"front", "back"}:
            have = ", ".join(sorted(parts))
            print(f"  {dex:03d}: only {have} supplied; front and back share normal.pal "
                  f"(pass --allow-partial to override)")
            failed += 1
            continue
        images, kinds = [], []
        for kind in ("front", "back"):
            if kind in parts:
                images.append(fit(load(parts[kind])))
                kinds.append(kind)
        if not images:
            continue
        palette = joint_palette(images)
        target = ROOT / "graphics" / "pokemon" / folder
        if not target.is_dir():
            print(f"  {dex:03d}: target folder missing: {target}")
            failed += 1
            continue
        names = ", ".join(kinds)
        if args.apply:
            for kind, img in zip(kinds, images):
                to_indexed(img, palette).save(target / f"{kind}.png")
            write_pal(target / "normal.pal", palette)
            print(f"  {dex:03d} -> {folder:14} wrote {names} + normal.pal")
        else:
            print(f"  {dex:03d} -> {folder:14} would write {names} + normal.pal")
        ok += 1

    mode = "applied" if args.apply else "dry run"
    print(f"\n{ok} species {mode}, {failed} problem(s).")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Install a GBA-native Arauna species pack over the Emerald species slots.

The pack ships one folder per creature named by National Dex number, e.g.
`001_caramelo/`, holding art already exported to the sizes and the 4bpp
indexed format the build wants. This installs it into graphics/pokemon/,
resolving each dex number to the Emerald species occupying that slot.

Two details the pack and the repository disagree on:

  front.png     The repository builds a still front sprite from front.png and
                the animated one from anim_front.png, whose first frame is the
                same drawing. The pack only ships anim_front.png, so front.png
                is cut from its top 64x64 -- which is exactly the relationship
                vanilla already has.
  shiny sprites The pack ships back_shiny/icon_shiny/anim_front_shiny, but the
                engine stores one index matrix per sprite and swaps only the
                palette. Those files are redundant (verified: all 386 carry
                indices identical to the normal art) and are not installed.

footprint.png is left alone: the pack does not cover it and the build needs
one per species.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import struct
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "graphics" / "pokemon"
COPY = ("anim_front.png", "back.png", "icon.png", "normal.pal", "shiny.pal")
SIZES = {"anim_front.png": (64, 128), "back.png": (64, 64), "icon.png": (32, 64)}


def dex_to_folder() -> dict[int, str]:
    """Resolve a National Dex number to its graphics folder.

    Internal species ids only track the dex to 251; the Hoenn block is stored
    in another order, so this walks the dex-ordered NATIONAL_DEX_* enum.
    """
    dex_text = (ROOT / "include" / "constants" / "pokedex.h").read_text(encoding="utf-8")
    body = dex_text[dex_text.index("enum {"):]
    names = re.findall(r"^\s*NATIONAL_DEX_([A-Z0-9_]+),", body, re.M)
    dex_by_name: dict[str, int] = {}
    for i, name in enumerate(names):
        if name != "NONE":
            dex_by_name.setdefault(name, i)

    graphics = (ROOT / "src" / "data" / "graphics" / "pokemon.h").read_text(encoding="utf-8")
    out: dict[int, str] = {}
    for m in re.finditer(
        r'gMonBackPic_(\w+)\[\]\s*=\s*INCGFX_U32\("graphics/pokemon/([^/]+)/back\.png"', graphics
    ):
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", m.group(1)).upper()
        if name in dex_by_name:
            out[dex_by_name[name]] = m.group(2)
    return out


def png_header(path: pathlib.Path) -> tuple[int, int, int, int]:
    b = path.read_bytes()[16:26]
    return struct.unpack(">IIBB", b)  # width, height, bit depth, colour type


def check(folder: pathlib.Path) -> list[str]:
    """Reject a species whose art would not survive the build."""
    bad = []
    for name in COPY:
        p = folder / name
        if not p.exists():
            bad.append(f"missing {name}")
            continue
        if name.endswith(".png"):
            w, h, depth, ctype = png_header(p)
            if (w, h) != SIZES[name]:
                bad.append(f"{name} is {w}x{h}, expected {SIZES[name][0]}x{SIZES[name][1]}")
            if ctype != 3 or depth != 4:
                bad.append(f"{name} is not 4bpp indexed (colour type {ctype}, depth {depth})")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pack", type=pathlib.Path, help="extracted pack directory")
    ap.add_argument("--apply", action="store_true", help="write the files (default is a dry run)")
    args = ap.parse_args()

    mapping = dex_to_folder()
    folders = sorted(d for d in args.pack.iterdir() if d.is_dir() and re.match(r"^\d{3}_", d.name))
    if not folders:
        print(f"no NNN_slug folders under {args.pack}")
        return 2

    installed = skipped = 0
    for folder in folders:
        dex = int(folder.name[:3])
        target_name = mapping.get(dex)
        if target_name is None:
            print(f"  {folder.name}: no Emerald species holds dex slot {dex}")
            skipped += 1
            continue
        target = DEST / target_name
        if not target.is_dir():
            print(f"  {folder.name}: target folder missing: {target}")
            skipped += 1
            continue
        bad = check(folder)
        if bad:
            print(f"  {folder.name}: " + "; ".join(bad))
            skipped += 1
            continue
        if args.apply:
            for name in COPY:
                shutil.copy2(folder / name, target / name)
            # The still front is the animated front's first frame.
            anim = Image.open(folder / "anim_front.png")
            anim.crop((0, 0, 64, 64)).save(target / "front.png")
        installed += 1

    verb = "installed" if args.apply else "would install"
    print(f"\n{installed} species {verb}, {skipped} skipped.")
    return 1 if skipped else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Install the two multi-form species from the Arauna pack.

import_species_pack.py resolves a dex number to a graphics folder by matching

    gMonBackPic_X[] = INCGFX_U32("graphics/pokemon/<folder>/back.png", ...)

which finds neither of the two species whose art is split across form
folders, so both were left carrying Emerald's drawings:

    201  Unown     28 folders (a-z, exclamation_mark, question_mark), each
                   with its own front/back/icon; one palette pair shared by
                   all of them at graphics/pokemon/unown/.
    351  Castform  4 folders (normal, sunny, rainy, snowy), each with its own
                   front/anim_front/back and its own palette pair; the build
                   concatenates the four into the files the engine reads, so
                   every form must be written for any of them to be right.

The pack has one drawing per creature, not one per form, so every form of a
species gets the same drawing -- which is what these two are now: a single
creature that does not change shape. Castform's forms keep working as
separate palette blocks, they just all hold the same colours.

Two size differences from the flat species folders are handled here:

    Castform anim_front.png is 64x64, a single frame, where every other
    species uses 64x128; it is cut from the top of the pack's sheet.
    Unown has no animated front at all -- graphics.h references only
    gMonStillFrontPic_* -- but anim_front.png is tracked in each form folder,
    so it is written to keep the folders consistent.

    python3 tools/art/import_species_forms.py <pack> [--apply]
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "graphics" / "pokemon"

UNOWN_FORMS = ([chr(c) for c in range(ord("a"), ord("z") + 1)]
               + ["exclamation_mark", "question_mark"])
CASTFORM_FORMS = ["normal", "sunny", "rainy", "snowy"]


def find(pack: pathlib.Path, dex: int) -> pathlib.Path | None:
    for d in sorted(pack.iterdir()):
        if d.is_dir() and d.name.startswith("%03d_" % dex):
            return d
    return None


def install_unown(src: pathlib.Path, apply: bool) -> list[str]:
    base = DEST / "unown"
    anim = Image.open(src / "anim_front.png")
    wrote = []
    for name in ("normal.pal", "shiny.pal"):          # shared by every letter
        wrote.append(str((base / name).relative_to(ROOT)))
        if apply:
            shutil.copy2(src / name, base / name)
    for form in UNOWN_FORMS:
        d = base / form
        if not d.is_dir():
            raise SystemExit("missing form folder %s" % d)
        wrote += [str((d / n).relative_to(ROOT))
                  for n in ("front.png", "back.png", "icon.png", "anim_front.png")]
        if apply:
            anim.crop((0, 0, 64, 64)).save(d / "front.png")
            shutil.copy2(src / "back.png", d / "back.png")
            shutil.copy2(src / "icon.png", d / "icon.png")
            shutil.copy2(src / "anim_front.png", d / "anim_front.png")
    return wrote


def install_castform(src: pathlib.Path, apply: bool) -> list[str]:
    base = DEST / "castform"
    anim = Image.open(src / "anim_front.png")
    wrote = [str((base / "icon.png").relative_to(ROOT))]
    if apply:
        shutil.copy2(src / "icon.png", base / "icon.png")   # one icon, all forms
    for form in CASTFORM_FORMS:
        d = base / form
        if not d.is_dir():
            raise SystemExit("missing form folder %s" % d)
        wrote += [str((d / n).relative_to(ROOT)) for n in
                  ("front.png", "anim_front.png", "back.png", "normal.pal", "shiny.pal")]
        if apply:
            top = anim.crop((0, 0, 64, 64))
            top.save(d / "front.png")
            top.save(d / "anim_front.png")                  # 64x64 here, not 64x128
            shutil.copy2(src / "back.png", d / "back.png")
            shutil.copy2(src / "normal.pal", d / "normal.pal")
            shutil.copy2(src / "shiny.pal", d / "shiny.pal")
    return wrote


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pack", type=pathlib.Path)
    ap.add_argument("--apply", action="store_true",
                    help="write the files (default is a dry run)")
    args = ap.parse_args()

    total = 0
    for dex, install in ((201, install_unown), (351, install_castform)):
        src = find(args.pack, dex)
        if src is None:
            print("dex %d: no folder in the pack" % dex)
            return 2
        wrote = install(src, args.apply)
        total += len(wrote)
        print("dex %d from %s: %d files" % (dex, src.name, len(wrote)))
    print("\n%d files %s." % (total, "written" if args.apply else "would be written"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

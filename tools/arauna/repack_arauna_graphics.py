#!/usr/bin/env python3
"""Rebuild Arauna's compact graphics header after editing indexed PNG packages."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from pack_arauna_graphics_header import c_array, gba_4bpp, lz77_compress, lz77_decompress, read_palette


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packages", type=Path, default=Path("graphics/arauna/editable"))
    parser.add_argument("--out", type=Path, default=Path("src/data/graphics/arauna_fakemon_graphics.h"))
    args = parser.parse_args()
    folders = sorted(path for path in args.packages.iterdir() if path.is_dir())
    if len(folders) != 386:
        raise SystemExit(f"expected 386 editable folders in {args.packages}, found {len(folders)}")

    parts = ["// Auto-generated packed Arauna GBA graphics.\n"]
    for number, folder in enumerate(folders, start=1):
        front_raw = gba_4bpp(Image.open(folder / "anim_front.png"))
        back_raw = gba_4bpp(Image.open(folder / "back.png"))
        icon_raw = gba_4bpp(Image.open(folder / "icon.png"))
        front = lz77_compress(front_raw)
        back = lz77_compress(back_raw)
        if lz77_decompress(front) != front_raw or lz77_decompress(back) != back_raw:
            raise ValueError(f"LZ77 round-trip failed for {folder.name}")
        parts.extend((
            c_array(f"gAraunaFrontPic_{number:03d}", "u32", front, 4),
            c_array(f"gAraunaBackPic_{number:03d}", "u32", back, 4),
            c_array(f"gAraunaPalette_{number:03d}", "u16", read_palette(folder / "normal.pal"), 2),
            c_array(f"gAraunaShinyPalette_{number:03d}", "u16", read_palette(folder / "shiny.pal"), 2),
            c_array(f"gAraunaIcon_{number:03d}", "u8", icon_raw, 4),
        ))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(parts), encoding="ascii")
    print(f"rebuilt {args.out} from 386 editable packages")


if __name__ == "__main__":
    main()

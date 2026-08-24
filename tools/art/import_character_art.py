#!/usr/bin/env python3
"""Convert character art into the exact assets the GBA build accepts.

Two targets, two very different sets of rules:

  overworld  A 144x32 sheet of nine 16x32 frames, indexed to the *shared*
             npc_3 palette. Those sixteen colours are used by fifty other
             NPCs, so nothing here may introduce a new one.
  portrait   A 64x64 sprite for the intro speech, which carries its own
             sixteen-colour palette.

In both cases colour 0 is the transparency key and must stay reserved.

The frame order is fixed by sAnimTable_Standard / sPicTable_ProfBirch:

    0 face south   3 walk south A   5 walk north A   7 walk west A
    1 face north   4 walk south B   6 walk north B   8 walk west B
    2 face west

East is not stored: the hardware mirrors the west frames, so any detail that
sits on one side of the body will jump across when the character turns.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
NPC3_PAL = ROOT / "graphics" / "object_events" / "palettes" / "npc_3.pal"
FRAME_W, FRAME_H, FRAME_COUNT = 16, 32, 9
PORTRAIT = (64, 64)
MAX_COLORS = 16

FRAME_NAMES = [
    "face south", "face north", "face west",
    "walk south A", "walk south B",
    "walk north A", "walk north B",
    "walk west A", "walk west B",
]


def read_jasc(path: pathlib.Path) -> list[tuple[int, int, int]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines[0].strip() != "JASC-PAL":
        raise SystemExit(f"{path}: not a JASC palette")
    count = int(lines[2])
    out = []
    for line in lines[3:3 + count]:
        r, g, b = (int(v) for v in line.split())
        out.append((r, g, b))
    return out


def write_jasc(path: pathlib.Path, colors: list[tuple[int, int, int]]) -> None:
    body = ["JASC-PAL", "0100", str(len(colors))]
    body += [f"{r} {g} {b}" for r, g, b in colors]
    path.write_text("\n".join(body) + "\n", encoding="utf-8")


def nearest(color, palette, skip_first=True):
    """Index of the closest palette entry, weighted for human perception."""
    best, best_d = None, None
    start = 1 if skip_first else 0
    r1, g1, b1 = color
    for i in range(start, len(palette)):
        r2, g2, b2 = palette[i]
        rm = (r1 + r2) / 2
        d = (2 + rm / 256) * (r1 - r2) ** 2 + 4 * (g1 - g2) ** 2 + (2 + (255 - rm) / 256) * (b1 - b2) ** 2
        if best_d is None or d < best_d:
            best, best_d = i, d
    return best


def alpha_split(img: Image.Image) -> tuple[Image.Image, Image.Image]:
    img = img.convert("RGBA")
    return img.convert("RGB"), img.getchannel("A")


def quantize_to(img: Image.Image, palette: list[tuple[int, int, int]]) -> tuple[Image.Image, dict]:
    """Map every opaque pixel onto the palette; alpha becomes index 0."""
    rgb, alpha = alpha_split(img)
    w, h = rgb.size
    out = Image.new("P", (w, h))
    flat = []
    for c in palette:
        flat += list(c)
    flat += [0, 0, 0] * (256 - len(palette))
    out.putpalette(flat)

    src, dst = rgb.load(), out.load()
    a = alpha.load()
    cache: dict[tuple[int, int, int], int] = {}
    used = set()
    for y in range(h):
        for x in range(w):
            if a[x, y] < 128:
                dst[x, y] = 0
                continue
            c = src[x, y]
            if c not in cache:
                cache[c] = nearest(c, palette)
            dst[x, y] = cache[c]
            used.add(cache[c])
    return out, {"distinct_source_colors": len(cache), "palette_slots_used": len(used)}


def build_overworld(src_path: pathlib.Path, out_path: pathlib.Path, frames: int) -> None:
    palette = read_jasc(NPC3_PAL)
    sheet = Image.open(src_path)
    w, h = sheet.size
    if w % frames:
        print(f"  note: source width {w} is not divisible by {frames}; "
              f"frames will be cut at fractional boundaries", file=sys.stderr)

    canvas = Image.new("RGBA", (FRAME_W * FRAME_COUNT, FRAME_H), (0, 0, 0, 0))
    step = w / frames
    for i in range(min(frames, FRAME_COUNT)):
        box = (round(i * step), 0, round((i + 1) * step), h)
        cell = sheet.crop(box).convert("RGBA")
        cell = trim_to_content(cell)
        cell = fit_into(cell, FRAME_W, FRAME_H)
        canvas.paste(cell, (i * FRAME_W, 0), cell)

    indexed, stats = quantize_to(canvas, palette)
    indexed.save(out_path)
    print(f"  wrote {out_path.relative_to(ROOT)}  "
          f"({stats['distinct_source_colors']} source colours -> "
          f"{stats['palette_slots_used']} of 15 npc_3 slots)")


def trim_to_content(img: Image.Image) -> Image.Image:
    bbox = img.getchannel("A").getbbox()
    return img.crop(bbox) if bbox else img


def fit_into(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Scale to fit the cell, keeping aspect, anchored to the bottom centre."""
    w, h = img.size
    scale = min(tw / w, th / h)
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    small = img.resize((nw, nh), Image.LANCZOS)
    cell = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    cell.paste(small, ((tw - nw) // 2, th - nh), small)
    return cell


def build_portrait(src_path: pathlib.Path, out_path: pathlib.Path, pal_out: pathlib.Path | None) -> None:
    img = Image.open(src_path).convert("RGBA")
    img = trim_to_content(img)
    img = fit_into(img, *PORTRAIT)

    # The portrait carries its own palette: derive 15 colours plus the key.
    rgb, alpha = alpha_split(img)
    reduced = rgb.quantize(colors=MAX_COLORS - 1, method=Image.MEDIANCUT)
    raw = reduced.getpalette()[: (MAX_COLORS - 1) * 3]
    derived = [tuple(raw[i:i + 3]) for i in range(0, len(raw), 3)]
    palette = [(115, 197, 164)] + derived  # index 0 is the transparency key

    indexed, stats = quantize_to(img, palette)
    indexed.save(out_path)
    print(f"  wrote {out_path.relative_to(ROOT)}  "
          f"({stats['palette_slots_used']} of 15 colours used)")
    if pal_out:
        write_jasc(pal_out, palette)
        print(f"  wrote {pal_out.relative_to(ROOT)}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sheet", type=pathlib.Path, help="source walk sheet (frames left to right)")
    ap.add_argument("--sheet-frames", type=int, default=FRAME_COUNT,
                    help="how many frames the source sheet contains (default 9)")
    ap.add_argument("--portrait", type=pathlib.Path, help="source portrait image")
    ap.add_argument("--out-sheet", type=pathlib.Path,
                    default=ROOT / "graphics/object_events/pics/people/prof_birch.png")
    ap.add_argument("--out-portrait", type=pathlib.Path,
                    default=ROOT / "graphics/birch_speech/birch.png")
    ap.add_argument("--out-portrait-pal", type=pathlib.Path, default=None)
    args = ap.parse_args()

    if not args.sheet and not args.portrait:
        ap.error("give --sheet, --portrait, or both")
    if args.sheet:
        print("overworld sheet:")
        build_overworld(args.sheet, args.out_sheet, args.sheet_frames)
    if args.portrait:
        print("intro portrait:")
        build_portrait(args.portrait, args.out_portrait, args.out_portrait_pal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

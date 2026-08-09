#!/usr/bin/env python3
"""Decode every fakemon sprite and reject the defects that reached play.

Two got through: a solid rectangle behind 86 species, and a back sprite holding
two half-size copies of the creature on 264 of them. Neither is visible to a
text or JSON check -- both live in LZ77-compressed pixel data -- so this
decompresses all 1158 arrays and measures the image itself.

Three tests, each written against a defect that actually shipped:

  canvas      the opaque bounding box is a completely filled rectangle. Real
              art leaves gaps in its own box; a backing canvas does not.
  duplicate   the top half of a back sprite matches the bottom half. That is a
              two-frame strip packed into the single frame the engine draws.
  undersized  the creature is far smaller than its own front sprite, which is
              what the halved back art looked like once split apart.

Pass --sheets DIR to also write contact sheets for eyeballing the whole dex.
"""

from __future__ import annotations

import argparse
import re
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HEADER = ROOT / "src/data/graphics/arauna_fakemon_graphics.h"

ARRAY_RE = re.compile(r"const u(\d+) (gArauna\w+_\d+)\[\][^=]*=\s*\{([^}]*)\}", re.S)


def lz77_decompress(data: bytes) -> bytes:
    size = data[1] | data[2] << 8 | data[3] << 16
    out = bytearray()
    pos = 4
    while len(out) < size:
        flags = data[pos]
        pos += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                first, second = data[pos], data[pos + 1]
                pos += 2
                count = ((first >> 4) & 0xF) + 3
                disp = (((first & 0xF) << 8) | second) + 1
                for _ in range(count):
                    out.append(out[-disp])
            else:
                out.append(data[pos])
                pos += 1
    return bytes(out)


def to_grid(pixels: bytes, width: int = 64) -> list[list[int]]:
    tiles = len(pixels) // 32
    per_row = width // 8
    grid = [[0] * width for _ in range((tiles // per_row) * 8)]
    for tile in range(tiles):
        ox, oy = (tile % per_row) * 8, (tile // per_row) * 8
        for row in range(8):
            for byte in range(4):
                value = pixels[tile * 32 + row * 4 + byte]
                grid[oy + row][ox + byte * 2] = value & 0xF
                grid[oy + row][ox + byte * 2 + 1] = value >> 4
    return grid


def box(frame: list[list[int]]) -> tuple[int, int, int, int] | None:
    rows = [y for y, line in enumerate(frame) if any(line)]
    cols = [x for x in range(len(frame[0])) if any(line[x] for line in frame)]
    if not rows or not cols:
        return None
    return rows[0], rows[-1], cols[0], cols[-1]


def twin_bands(frame: list[list[int]]) -> bool:
    """True when the frame holds two separated blobs of near-equal size."""
    filled = [y for y in range(64) if any(frame[y])]
    if not filled:
        return False
    bands: list[tuple[int, int]] = []
    start = previous = filled[0]
    for y in filled[1:]:
        if y > previous + 1:
            bands.append((start, previous))
            start = y
        previous = y
    bands.append((start, previous))
    if len(bands) != 2:
        return False

    (first_top, first_bottom), (second_top, second_bottom) = bands
    tall = (first_bottom - first_top + 1, second_bottom - second_top + 1)
    if min(tall) < 10 or min(tall) / max(tall) < 0.7:
        return False
    weight = tuple(
        sum(1 for y in range(top, bottom + 1) for x in range(64) if frame[y][x])
        for top, bottom in bands
    )
    return min(weight) / max(weight) > 0.7


def load() -> dict[str, list[int]]:
    text = HEADER.read_text(encoding="ascii")
    return {
        found.group(2): [
            int(v.strip(), 16) for v in found.group(3).replace("\n", "").split(",") if v.strip()
        ]
        for found in ARRAY_RE.finditer(text)
    }


def pixels_of(arrays: dict[str, list[int]], name: str) -> bytes:
    return lz77_decompress(b"".join(struct.pack("<I", w) for w in arrays[name]))


def write_png(path: Path, width: int, height: int, rgb: list[tuple[int, int, int]]) -> None:
    raw = b"".join(
        b"\x00" + bytes(c for x in range(width) for c in rgb[y * width + x])
        for y in range(height)
    )

    def chunk(kind: bytes, payload: bytes) -> bytes:
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def render(grid, palette, top: int, height: int) -> list[tuple[int, int, int]]:
    out = []
    for y in range(top, top + height):
        for x in range(64):
            index = grid[y][x] if y < len(grid) else 0
            out.append((255, 0, 255) if index == 0 else palette[index])
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheets", type=Path, help="write contact sheets to this directory")
    args = parser.parse_args()

    arrays = load()
    problems: list[str] = []
    heights: dict[str, list[int]] = {"front": [], "back": []}

    for number in range(1, 387):
        slot = f"{number:03d}"
        front = to_grid(pixels_of(arrays, f"gAraunaFrontPic_{slot}"))
        back = to_grid(pixels_of(arrays, f"gAraunaBackPic_{slot}"))

        for label, grid, frames in (("front", front, 2), ("back", back, 1)):
            for frame_index in range(frames):
                frame = grid[frame_index * 64 : frame_index * 64 + 64]
                bounds = box(frame)
                if bounds is None:
                    problems.append(f"#{slot} {label} frame {frame_index} is empty")
                    continue
                top, bottom, left, right = bounds
                tall, wide = bottom - top + 1, right - left + 1
                if tall >= 32 and wide >= 32 and all(
                    frame[y][x] for y in range(top, bottom + 1) for x in range(left, right + 1)
                ):
                    problems.append(
                        f"#{slot} {label} frame {frame_index} is a solid "
                        f"{wide}x{tall} canvas, not a sprite"
                    )
                if frame_index == 0:
                    heights[label].append(tall)

        # A two-frame strip squeezed into one frame reads as two separated
        # bands of near-identical size with a blank gap between them. Matching
        # rows exactly does not work -- the copies differ by a pixel or two --
        # and comparing opacity masks flags any creature that simply fills the
        # frame, so measure the bands themselves.
        if twin_bands(back):
            problems.append(
                f"#{slot} back holds two stacked copies of the creature, "
                "not one sprite"
            )

        front_tall, back_tall = heights["front"][-1], heights["back"][-1]
        if back_tall * 1.7 < front_tall:
            problems.append(
                f"#{slot} back is {back_tall}px against a {front_tall}px front"
            )

    if args.sheets:
        args.sheets.mkdir(parents=True, exist_ok=True)
        for label, kind, frame_top in (("front", "FrontPic", 0), ("back", "BackPic", 0)):
            columns, cell = 20, 64
            rows = (386 + columns - 1) // columns
            width, height = columns * cell, rows * cell
            sheet = [(24, 24, 28)] * (width * height)
            for index in range(386):
                slot = f"{index + 1:03d}"
                palette = [
                    ((c & 31) * 8, ((c >> 5) & 31) * 8, ((c >> 10) & 31) * 8)
                    for c in arrays[f"gAraunaPalette_{slot}"]
                ]
                grid = to_grid(pixels_of(arrays, f"gArauna{kind}_{slot}"))
                cellpix = render(grid, palette, frame_top, 64)
                ox, oy = (index % columns) * cell, (index // columns) * cell
                for y in range(cell):
                    for x in range(cell):
                        colour = cellpix[y * 64 + x]
                        if colour != (255, 0, 255):
                            sheet[(oy + y) * width + ox + x] = colour
            write_png(args.sheets / f"arauna_{label}_sheet.png", width, height, sheet)
            print(f"wrote {args.sheets / f'arauna_{label}_sheet.png'}")

    if problems:
        print(f"Sprite health check FAILED: {len(problems)} problem(s)", file=sys.stderr)
        for problem in problems[:25]:
            print(f"  - {problem}", file=sys.stderr)
        if len(problems) > 25:
            print(f"  ... and {len(problems) - 25} more", file=sys.stderr)
        return 1

    median = lambda v: sorted(v)[len(v) // 2]
    print(
        f"Sprite health check passed: 386 species, "
        f"front median {median(heights['front'])}px, back median {median(heights['back'])}px"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

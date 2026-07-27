#!/usr/bin/env python3
"""Restore transparency on Arauna sprites composited onto a solid canvas.

86 of the 386 fakemon shipped with their art drawn over an opaque 58x58
square instead of a transparent one. The GBA treats palette index 0 as
transparent and everything else as paint, so those species render inside a
solid rectangle -- black for Quatim, white for Cigarrinho, whatever colour the
canvas happened to be. The remaining 300 are fine, which is why the defect
reads as "some sprites" rather than a broken pipeline.

The editable art pack in graphics/arauna cannot be used to regenerate them: its
palettes carry a green at index 0 rather than the magenta the committed header
uses, so it is a different pack from the one that produced the shipped data.
This works on the committed arrays instead.

Only background is removed, never paint. The fill walks inward from outside the
frame and crosses two things: pixels that are already transparent, and pixels
holding the canvas colour. It stops at the creature's outline, so a colour that
also appears inside the sprite survives wherever it is not reachable from the
edge.

A frame is only touched when its opaque bounding box is a completely filled
rectangle at least 32x32. A real sprite never fills its own bounding box -- the
healthy ones sit around 36% -- so that test separates a canvas from art without
needing a list of species.
"""

from __future__ import annotations

import re
import struct
import sys
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HEADER = ROOT / "src/data/graphics/arauna_fakemon_graphics.h"

WIDTH = 64
FRAME = 64
# Below this, a filled box is plausibly just a small solid creature.
MIN_CANVAS = 32

ARRAY_RE = re.compile(
    r"(const u32 (gArauna(?:Front|Back)Pic_\d+)\[\][^=]*=\s*\{)([^}]*)(\})", re.S
)


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


def lz77_compress(data: bytes) -> bytes:
    """BIOS-compatible type-0x10 LZ77 with a 4 KiB window."""
    out = bytearray(
        (0x10, len(data) & 0xFF, (len(data) >> 8) & 0xFF, (len(data) >> 16) & 0xFF)
    )
    starts: dict[bytes, list[int]] = {}
    pos = 0
    while pos < len(data):
        flags_at = len(out)
        out.append(0)
        flags = 0
        for bit in range(8):
            if pos >= len(data):
                break
            best_len, best_disp = 0, 0
            if pos + 3 <= len(data):
                key = data[pos : pos + 3]
                for cand in reversed(starts.get(key, ())):
                    disp = pos - cand
                    if disp > 4096:
                        break
                    length = 0
                    limit = min(18, len(data) - pos)
                    while length < limit and data[cand + length] == data[pos + length]:
                        length += 1
                    if length > best_len:
                        best_len, best_disp = length, disp
                        if length == 18:
                            break
            if best_len >= 3:
                flags |= 0x80 >> bit
                out.append(((best_len - 3) << 4) | ((best_disp - 1) >> 8))
                out.append((best_disp - 1) & 0xFF)
                consumed = best_len
            else:
                out.append(data[pos])
                consumed = 1
            for index in range(pos, min(len(data), pos + consumed)):
                if index + 3 <= len(data):
                    starts.setdefault(data[index : index + 3], []).append(index)
            pos += consumed
        out[flags_at] = flags
    return bytes(out)


def to_grid(pixels: bytes) -> list[list[int]]:
    tiles = len(pixels) // 32
    per_row = WIDTH // 8
    grid = [[0] * WIDTH for _ in range((tiles // per_row) * 8)]
    for tile in range(tiles):
        ox, oy = (tile % per_row) * 8, (tile // per_row) * 8
        for row in range(8):
            for byte in range(4):
                value = pixels[tile * 32 + row * 4 + byte]
                grid[oy + row][ox + byte * 2] = value & 0xF
                grid[oy + row][ox + byte * 2 + 1] = value >> 4
    return grid


def to_pixels(grid: list[list[int]]) -> bytes:
    per_row = WIDTH // 8
    tiles = (len(grid) // 8) * per_row
    out = bytearray()
    for tile in range(tiles):
        ox, oy = (tile % per_row) * 8, (tile // per_row) * 8
        for row in range(8):
            for byte in range(4):
                lo = grid[oy + row][ox + byte * 2]
                hi = grid[oy + row][ox + byte * 2 + 1]
                out.append(lo | (hi << 4))
    return bytes(out)


def clear_canvas(frame: list[list[int]]) -> int:
    """Drop a solid backing rectangle. Returns how many pixels became clear."""
    rows = [y for y in range(FRAME) if any(frame[y])]
    cols = [x for x in range(FRAME) if any(frame[y][x] for y in range(FRAME))]
    if not rows or not cols:
        return 0

    top, bottom, left, right = rows[0], rows[-1], cols[0], cols[-1]
    height, width = bottom - top + 1, right - left + 1
    if height < MIN_CANVAS or width < MIN_CANVAS:
        return 0
    # A canvas is filled edge to edge; real art leaves gaps in its own box.
    if any(
        frame[y][x] == 0
        for y in range(top, bottom + 1)
        for x in range(left, right + 1)
    ):
        return 0

    # The box is filled edge to edge, so its outer ring is entirely canvas and
    # every colour on it is a background colour. Several of these canvases are
    # noisy rather than flat -- a dark speckle of four or five near-black
    # indices -- so keying on the single most common colour leaves a halo.
    ring = (
        [frame[top][x] for x in range(left, right + 1)]
        + [frame[bottom][x] for x in range(left, right + 1)]
        + [frame[y][left] for y in range(top, bottom + 1)]
        + [frame[y][right] for y in range(top, bottom + 1)]
    )
    background = {value for value in ring if value != 0}
    if not background:
        return 0

    seen = [[False] * FRAME for _ in range(FRAME)]
    queue = deque()
    for x in range(FRAME):
        for y in (0, FRAME - 1):
            queue.append((x, y))
        for y in range(FRAME):
            if x in (0, FRAME - 1):
                queue.append((x, y))

    cleared = 0
    while queue:
        x, y = queue.popleft()
        if not (0 <= x < FRAME and 0 <= y < FRAME) or seen[y][x]:
            continue
        value = frame[y][x]
        if value != 0 and value not in background:
            continue  # the creature's outline stops the fill
        seen[y][x] = True
        if value in background:
            frame[y][x] = 0
            cleared += 1
        queue.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return cleared


def main() -> int:
    check_only = "--check" in sys.argv
    text = HEADER.read_text(encoding="ascii")
    repaired: list[tuple[str, int]] = []

    def handle(match: re.Match) -> str:
        head, name, body, tail = match.groups()
        words = [int(v.strip(), 16) for v in body.replace("\n", "").split(",") if v.strip()]
        grid = to_grid(lz77_decompress(b"".join(struct.pack("<I", w) for w in words)))

        cleared = 0
        for start in range(0, len(grid), FRAME):
            frame = grid[start : start + FRAME]
            if len(frame) == FRAME:
                cleared += clear_canvas(frame)
        if not cleared:
            return match.group(0)

        repaired.append((name, cleared))
        if check_only:
            return match.group(0)

        raw = to_pixels(grid)
        packed = lz77_compress(raw)
        assert lz77_decompress(packed) == raw, f"{name}: round trip failed"
        # The arrays are u32; the encoder stops on a byte boundary.
        packed += b"\x00" * (-len(packed) % 4)
        values = [
            struct.unpack_from("<I", packed, off)[0] for off in range(0, len(packed), 4)
        ]
        lines = [
            "    " + ", ".join(f"0x{v:08X}" for v in values[i : i + 8])
            for i in range(0, len(values), 8)
        ]
        return head + "\n" + ",\n".join(lines) + ",\n" + tail

    updated = ARRAY_RE.sub(handle, text)

    if check_only:
        if repaired:
            print(f"{len(repaired)} sprite(s) still drawn on a solid canvas:", file=sys.stderr)
            for name, cleared in repaired[:10]:
                print(f"  - {name}: {cleared} background pixels are opaque", file=sys.stderr)
            return 1
        print("Sprite transparency check passed: no sprite sits on a solid canvas")
        return 0

    HEADER.write_text(updated, encoding="ascii")
    print(f"repaired {len(repaired)} sprite arrays")
    for name, cleared in repaired[:8]:
        print(f"  {name}: cleared {cleared} px")
    return 0


if __name__ == "__main__":
    sys.exit(main())

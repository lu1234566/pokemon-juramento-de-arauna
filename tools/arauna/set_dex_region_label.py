#!/usr/bin/env python3
"""Replace the Pokedex counter's HOENN label with ARAUNA.

The dex mode titles are strings and already say ARAUNA DEX, but the word beside
the SEEN and OWN counters is not text -- it is a 32x16 sprite living in
graphics/pokedex/interface.png as tiles 160-167, with NATIONAL at 168-175. No
amount of editing strings reaches it, which is why HOENN survived the rename.

The letters are drawn as a white body at palette index 1 with a grey drop
shadow at index 15, offset one pixel right and one pixel down. Rebuilding that
shadow from the body reproduces the existing HOENN pixel for pixel, so the new
word is drawn in the same hand rather than pasted from another font.

N is lifted from HOENN itself. A, R and U are drawn to match its 4x7 body.
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHEET = ROOT / "graphics/pokedex/interface.png"

BODY, SHADOW, CLEAR = 0x1, 0xF, 0x0
TOP, HEIGHT = 324, 8  # 7 rows of letter plus the shadow row
PITCH = 5

GLYPHS = {
    "A": (".11.", "1..1", "1..1", "1111", "1..1", "1..1", "1..1"),
    "R": ("111.", "1..1", "1..1", "111.", "1.1.", "1..1", "1..1"),
    "U": ("1..1", "1..1", "1..1", "1..1", "1..1", "1..1", ".11."),
    # Taken from the N already in HOENN so the weight matches exactly.
    "N": ("1..1", "11.1", "11.1", "1.11", "1.11", "1..1", "1..1"),
}
WORD = "ARAUNA"


def read_png(path: Path):
    blob = path.read_bytes()
    width, height = struct.unpack(">II", blob[16:24])
    depth, colour = blob[24], blob[25]
    if depth != 4 or colour != 3:
        raise ValueError(f"expected 4-bit indexed PNG, got depth={depth} colour={colour}")

    chunks: list[tuple[bytes, bytes]] = []
    data = b""
    offset = 8
    while offset < len(blob):
        length = struct.unpack(">I", blob[offset : offset + 4])[0]
        kind = blob[offset + 4 : offset + 8]
        payload = blob[offset + 8 : offset + 8 + length]
        if kind == b"IDAT":
            data += payload
        else:
            chunks.append((kind, payload))
        offset += 8 + length + 4

    raw = zlib.decompress(data)
    stride = (width * 4 + 7) // 8
    rows: list[bytearray] = []
    pos = 0
    previous = bytes(stride)
    for _ in range(height):
        kind = raw[pos]
        pos += 1
        line = bytearray(raw[pos : pos + stride])
        pos += stride
        if kind == 1:
            for i in range(1, stride):
                line[i] = (line[i] + line[i - 1]) & 0xFF
        elif kind == 2:
            for i in range(stride):
                line[i] = (line[i] + previous[i]) & 0xFF
        elif kind == 3:
            for i in range(stride):
                left = line[i - 1] if i else 0
                line[i] = (line[i] + (left + previous[i]) // 2) & 0xFF
        elif kind == 4:
            def paeth(a: int, b: int, c: int) -> int:
                guess = a + b - c
                da, db, dc = abs(guess - a), abs(guess - b), abs(guess - c)
                return a if da <= db and da <= dc else (b if db <= dc else c)

            for i in range(stride):
                left = line[i - 1] if i else 0
                upper_left = previous[i - 1] if i else 0
                line[i] = (line[i] + paeth(left, previous[i], upper_left)) & 0xFF
        elif kind != 0:
            raise ValueError(f"unknown PNG filter {kind}")
        rows.append(line)
        previous = line
    return width, height, rows, chunks


def write_png(path: Path, rows, chunks) -> None:
    raw = b"".join(b"\x00" + bytes(line) for line in rows)

    def chunk(kind: bytes, payload: bytes) -> bytes:
        body = kind + payload
        return (
            struct.pack(">I", len(payload))
            + body
            + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
        )

    out = bytearray(b"\x89PNG\r\n\x1a\n")
    for kind, payload in chunks:
        if kind != b"IEND":
            out += chunk(kind, payload)
    out += chunk(b"IDAT", zlib.compress(raw, 9))
    out += chunk(b"IEND", b"")
    path.write_bytes(bytes(out))


def get(rows, x: int, y: int) -> int:
    byte = rows[y][x // 2]
    return (byte >> 4) if x % 2 == 0 else (byte & 0xF)


def put(rows, x: int, y: int, value: int) -> None:
    index = x // 2
    byte = rows[y][index]
    rows[y][index] = ((value << 4) | (byte & 0x0F)) if x % 2 == 0 else ((byte & 0xF0) | value)


def render(width: int) -> list[list[int]]:
    """Draw the word, then grow its shadow the way the sheet already does."""
    cells = [[CLEAR] * width for _ in range(HEIGHT)]
    for position, letter in enumerate(WORD):
        origin = position * PITCH
        for row, line in enumerate(GLYPHS[letter]):
            for column, mark in enumerate(line):
                if mark == "1":
                    cells[row][origin + column] = BODY

    for y in range(HEIGHT - 1, -1, -1):
        for x in range(width - 1, -1, -1):
            if cells[y][x] != CLEAR:
                continue
            neighbours = (
                cells[y][x - 1] if x else CLEAR,
                cells[y - 1][x] if y else CLEAR,
                cells[y - 1][x - 1] if x and y else CLEAR,
            )
            if BODY in neighbours:
                cells[y][x] = SHADOW
    return cells


def main() -> int:
    check_only = "--check" in sys.argv
    width, _, rows, chunks = read_png(SHEET)
    wanted = render(width)

    differs = any(
        get(rows, x, TOP + y) != wanted[y][x]
        for y in range(HEIGHT)
        for x in range(width)
    )

    if check_only:
        if differs:
            print(
                "The Pokedex counter still reads HOENN. Run "
                "tools/arauna/set_dex_region_label.py to redraw it.",
                file=sys.stderr,
            )
            return 1
        print(f"Dex region label check passed: the counter reads {WORD}")
        return 0

    if not differs:
        print(f"already reads {WORD}")
        return 0

    for y in range(HEIGHT):
        for x in range(width):
            put(rows, x, TOP + y, wanted[y][x])
    write_png(SHEET, rows, chunks)
    print(f"redrew the Pokedex counter label as {WORD}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

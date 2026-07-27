#!/usr/bin/env python3
"""Give a-tilde and o-tilde real glyphs instead of aliasing them onto a and o.

charmap.txt mapped 'a-tilde' to 0xD5 and 'o-tilde' to 0xE3 -- the bytes that
already mean plain 'a' and plain 'o'. The tilde was therefore dropped at
assembly time: the source says Capivarao with a tilde and the ROM prints it
without one. It compiles, it passes every check, and it is wrong on 60 of the
386 species names plus any dialogue that uses those letters.

Every other accented pair in charmap.txt is a Latin/Japanese pair sharing a
byte across two character sets, which is by design. These two were the only
Latin-on-Latin collisions, which is what made them a defect rather than a
convention.

There were no unmapped bytes to move into, but there were unused ones. The font
carries German umlauts at 0xF1, 0xF2, 0xF4 and 0xF5, and this project uses none
of them -- u-umlaut at 0xF6 is the only one that appears, in Saguim, so it
stays. The four free cells already hold A, O, a and o with an accent above, at
the right size and on the right rows, so the letters need no redrawing: only
the accent is replaced, copied from the n-tilde glyphs that sit in the same
fonts at the same height.
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FONTS = sorted((ROOT / "graphics/fonts").glob("latin_*.png"))

CELL = 16
PER_ROW = 16

# Byte -> (source of the accent, rows the accent occupies)
LOWER_ROWS = (3, 4)
UPPER_ROWS = (0, 1)
LOWER_TILDE = 0x29  # n with tilde
UPPER_TILDE = 0x14  # N with tilde

# Target cell -> (tilde source, rows to copy)
TARGETS = {
    0xF1: (UPPER_TILDE, UPPER_ROWS),  # A umlaut -> A tilde
    0xF2: (UPPER_TILDE, UPPER_ROWS),  # O umlaut -> O tilde
    0xF4: (LOWER_TILDE, LOWER_ROWS),  # a umlaut -> a tilde
    0xF5: (LOWER_TILDE, LOWER_ROWS),  # o umlaut -> o tilde
}


def read_png(path: Path):
    blob = path.read_bytes()
    width, height = struct.unpack(">II", blob[16:24])
    depth, colour = blob[24], blob[25]
    if depth != 8 or colour != 3:
        raise ValueError(f"{path.name}: expected 8-bit indexed, got {depth}/{colour}")

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
    rows: list[bytearray] = []
    pos = 0
    previous = bytes(width)
    for _ in range(height):
        kind = raw[pos]
        pos += 1
        line = bytearray(raw[pos : pos + width])
        pos += width
        if kind == 1:
            for i in range(1, width):
                line[i] = (line[i] + line[i - 1]) & 0xFF
        elif kind == 2:
            for i in range(width):
                line[i] = (line[i] + previous[i]) & 0xFF
        elif kind == 3:
            for i in range(width):
                left = line[i - 1] if i else 0
                line[i] = (line[i] + (left + previous[i]) // 2) & 0xFF
        elif kind == 4:
            def paeth(a: int, b: int, c: int) -> int:
                guess = a + b - c
                da, db, dc = abs(guess - a), abs(guess - b), abs(guess - c)
                return a if da <= db and da <= dc else (b if db <= dc else c)

            for i in range(width):
                left = line[i - 1] if i else 0
                upper_left = previous[i - 1] if i else 0
                line[i] = (line[i] + paeth(left, previous[i], upper_left)) & 0xFF
        elif kind != 0:
            raise ValueError(f"{path.name}: unknown filter {kind}")
        rows.append(line)
        previous = line
    return width, height, rows, chunks


def write_png(path: Path, width: int, height: int, rows, chunks) -> None:
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
        if kind == b"IEND":
            continue
        out += chunk(kind, payload)
        if kind == b"PLTE" or (kind == b"tRNS"):
            pass
    out += chunk(b"IDAT", zlib.compress(raw, 9))
    out += chunk(b"IEND", b"")
    path.write_bytes(bytes(out))


def cell_origin(index: int) -> tuple[int, int]:
    return (index % PER_ROW) * CELL, (index // PER_ROW) * CELL


def main() -> int:
    check_only = "--check" in sys.argv
    if not FONTS:
        print("no latin font sheets found", file=sys.stderr)
        return 1

    changed: list[str] = []
    for font in FONTS:
        width, height, rows, chunks = read_png(font)
        dirty = False
        for target, (source, accent_rows) in TARGETS.items():
            tx, ty = cell_origin(target)
            sx, sy = cell_origin(source)
            for offset in accent_rows:
                wanted = rows[sy + offset][sx : sx + CELL]
                if rows[ty + offset][tx : tx + CELL] != wanted:
                    rows[ty + offset][tx : tx + CELL] = wanted
                    dirty = True
        if dirty:
            changed.append(font.name)
            if not check_only:
                write_png(font, width, height, rows, chunks)

    if check_only:
        if changed:
            print(
                f"{len(changed)} font sheet(s) still carry an umlaut where a tilde "
                "belongs: " + ", ".join(changed),
                file=sys.stderr,
            )
            return 1
        print(f"Tilde glyph check passed: {len(FONTS)} latin fonts carry a and o tildes")
        return 0

    print(f"updated {len(changed)} of {len(FONTS)} latin font sheets")
    for name in changed:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

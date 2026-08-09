#!/usr/bin/env python3
"""Reject PNGs that libpng will refuse to read.

``gbagfx`` uses libpng, which validates every chunk CRC and aborts the build
with a bare ``libpng error: PLTE: CRC error`` followed by ``Failed to init I/O
for reading``. The message names the failing chunk but not the cause, and no
other check in the suite opens the image files at all, so a byte-level defect
in a single sprite survives every validator and only surfaces after the build
has already spent many minutes compiling other assets.

This walks the PNG chunk chain of every graphic and verifies the stored CRC of
each chunk, which is exactly what libpng does before it will decode anything.
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAGIC = b"\x89PNG\r\n\x1a\n"


def check(path: Path) -> list[str]:
    """Return a list of problems found in one PNG."""
    data = path.read_bytes()
    name = path.relative_to(ROOT)

    if not data.startswith(MAGIC):
        return [f"{name}: not a PNG (bad signature)"]

    problems: list[str] = []
    offset = len(MAGIC)
    seen_end = False

    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        kind = data[offset + 4 : offset + 8]
        end = offset + 8 + length

        if end + 4 > len(data):
            problems.append(f"{name}: chunk {kind!r} runs past the end of the file")
            break

        stored = struct.unpack(">I", data[end : end + 4])[0]
        actual = zlib.crc32(data[offset + 4 : end]) & 0xFFFFFFFF
        if stored != actual:
            label = kind.decode("ascii", "replace")
            problems.append(
                f"{name}: chunk {label!r} at byte {offset} has CRC "
                f"0x{stored:08x}, expected 0x{actual:08x}"
            )
            # The chain cannot be trusted past a bad chunk.
            break

        if kind == b"IEND":
            seen_end = True
            break
        offset = end + 4

    if not problems and not seen_end:
        problems.append(f"{name}: no IEND chunk; the file is truncated")

    return problems


def main() -> int:
    paths = sorted(ROOT.glob("graphics/**/*.png"))
    problems: list[str] = []
    for path in paths:
        problems.extend(check(path))

    if problems:
        for problem in problems[:30]:
            print(problem, file=sys.stderr)
        if len(problems) > 30:
            print(f"... and {len(problems) - 30} more", file=sys.stderr)
        print(
            f"\n{len(problems)} damaged PNG(s): gbagfx would abort the build.",
            file=sys.stderr,
        )
        return 1

    print(f"PNG integrity check passed: {len(paths)} graphics are readable by libpng")
    return 0


if __name__ == "__main__":
    sys.exit(main())

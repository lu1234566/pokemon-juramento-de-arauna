#!/usr/bin/env python3
"""Rebuild the fakemon graphics header from the editable art pack.

The committed header was produced by a conversion that damaged the art. Two
symptoms reached play: 86 species render inside a solid rectangle, and 264 back
sprites show the creature twice, each copy at roughly half the size a back
sprite should be (32 px against 49 px on the ones that survived).

graphics/arauna/arauna_editable_fakemon_assets.zip holds the real art for all
386 species, and it is intact: anim_front.png is 64x128, back.png is 64x64 with
one creature filling the frame, icon.png is 32x64, and index 0 is the
transparent slot everywhere. Repacking from it fixes both defects at their
source rather than repairing pixels after the fact.

On palettes: normal.pal and the PNG's own palette agree on entries 1-15 and
differ only at index 0, where the file says green and the image says black.
Index 0 is the transparent slot and is never drawn, so either is correct; this
writes magenta there, matching the rest of the project and the usual decomp
convention.
"""

from __future__ import annotations

import argparse
import struct
import sys
import zipfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "graphics/arauna/arauna_editable_fakemon_assets.zip"
HEADER = ROOT / "src/data/graphics/arauna_fakemon_graphics.h"

TRANSPARENT = 0x7C1F  # magenta in RGB555
SPECIES = 386


def read_png_indices(blob: bytes) -> tuple[int, int, list[bytes]]:
    """Decode an 8-bit indexed PNG into rows of palette indices."""
    width, height = struct.unpack(">II", blob[16:24])
    depth, colour = blob[24], blob[25]
    if depth != 8 or colour != 3:
        raise ValueError(f"expected 8-bit indexed PNG, got depth={depth} colour={colour}")

    data = b""
    offset = 8
    while offset < len(blob):
        length = struct.unpack(">I", blob[offset : offset + 4])[0]
        kind = blob[offset + 4 : offset + 8]
        if kind == b"IDAT":
            data += blob[offset + 8 : offset + 8 + length]
        offset += 8 + length + 4

    raw = zlib.decompress(data)
    rows: list[bytes] = []
    pos = 0
    previous = bytes(width)
    for _ in range(height):
        filter_type = raw[pos]
        pos += 1
        line = bytearray(raw[pos : pos + width])
        pos += width
        if filter_type == 1:
            for i in range(1, width):
                line[i] = (line[i] + line[i - 1]) & 0xFF
        elif filter_type == 2:
            for i in range(width):
                line[i] = (line[i] + previous[i]) & 0xFF
        elif filter_type == 3:
            for i in range(width):
                left = line[i - 1] if i else 0
                line[i] = (line[i] + (left + previous[i]) // 2) & 0xFF
        elif filter_type == 4:
            def paeth(a: int, b: int, c: int) -> int:
                guess = a + b - c
                da, db, dc = abs(guess - a), abs(guess - b), abs(guess - c)
                return a if da <= db and da <= dc else (b if db <= dc else c)

            for i in range(width):
                left = line[i - 1] if i else 0
                upper_left = previous[i - 1] if i else 0
                line[i] = (line[i] + paeth(left, previous[i], upper_left)) & 0xFF
        elif filter_type != 0:
            raise ValueError(f"unknown PNG filter {filter_type}")
        rows.append(bytes(line))
        previous = line
    return width, height, rows


def to_4bpp(width: int, height: int, rows: list[bytes]) -> bytes:
    if width % 8 or height % 8:
        raise ValueError(f"image is not tile aligned: {width}x{height}")
    out = bytearray()
    for tile_y in range(0, height, 8):
        for tile_x in range(0, width, 8):
            for y in range(8):
                line = rows[tile_y + y]
                for x in range(0, 8, 2):
                    low, high = line[tile_x + x], line[tile_x + x + 1]
                    if low > 15 or high > 15:
                        raise ValueError("palette index above 15 in a 4bpp image")
                    out.append(low | (high << 4))
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
                for candidate in reversed(starts.get(data[pos : pos + 3], ())):
                    disp = pos - candidate
                    if disp > 4096:
                        break
                    length = 0
                    limit = min(18, len(data) - pos)
                    while length < limit and data[candidate + length] == data[pos + length]:
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
    out += b"\x00" * (-len(out) % 4)
    return bytes(out)


def read_jasc(text: str) -> list[int]:
    lines = text.replace("\r", "").splitlines()
    colours = [tuple(map(int, line.split())) for line in lines[3:19]]
    if len(colours) != 16:
        raise ValueError("expected 16 palette entries")
    packed = [((r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10)) for r, g, b in colours]
    packed[0] = TRANSPARENT
    return packed


def emit(name: str, ctype: str, values: list[int], align: int) -> str:
    digits = {"u8": 2, "u16": 4, "u32": 8}[ctype]
    per_line = {"u8": 16, "u16": 8, "u32": 8}[ctype]
    body = ",\n".join(
        "    " + ", ".join(f"0x{v:0{digits}X}" for v in values[i : i + per_line])
        for i in range(0, len(values), per_line)
    )
    return (
        f"const {ctype} {name}[] __attribute__((aligned({align}))) =\n"
        f"{{\n{body},\n}};\n"
    )


def as_words(data: bytes) -> list[int]:
    return [struct.unpack_from("<I", data, i)[0] for i in range(0, len(data), 4)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="report what would change without writing")
    args = parser.parse_args()

    if not PACK.exists():
        print(f"missing art pack: {PACK}", file=sys.stderr)
        return 1

    archive = zipfile.ZipFile(PACK)
    folders = sorted({name.split("/")[0] for name in archive.namelist() if "/" in name})
    if len(folders) != SPECIES:
        print(f"expected {SPECIES} species folders, found {len(folders)}", file=sys.stderr)
        return 1

    parts = ["// Auto-generated packed Arauna GBA graphics (editable art pack).\n"]
    raw_total = packed_total = 0

    for index, folder in enumerate(folders, start=1):
        if int(folder.split("_")[0]) != index:
            print(f"art pack is out of order at {folder}", file=sys.stderr)
            return 1

        front = to_4bpp(*read_png_indices(archive.read(f"{folder}/anim_front.png")))
        back = to_4bpp(*read_png_indices(archive.read(f"{folder}/back.png")))
        icon = to_4bpp(*read_png_indices(archive.read(f"{folder}/icon.png")))
        if (len(front), len(back), len(icon)) != (4096, 2048, 1024):
            print(
                f"{folder}: unexpected sizes "
                f"{len(front)}/{len(back)}/{len(icon)}",
                file=sys.stderr,
            )
            return 1

        front_z, back_z = lz77_compress(front), lz77_compress(back)
        raw_total += len(front) + len(back)
        packed_total += len(front_z) + len(back_z)

        parts.append(emit(f"gAraunaFrontPic_{index:03d}", "u32", as_words(front_z), 4))
        parts.append(emit(f"gAraunaBackPic_{index:03d}", "u32", as_words(back_z), 4))
        parts.append(emit(f"gAraunaPalette_{index:03d}", "u16",
                          read_jasc(archive.read(f"{folder}/normal.pal").decode("ascii")), 2))
        parts.append(emit(f"gAraunaShinyPalette_{index:03d}", "u16",
                          read_jasc(archive.read(f"{folder}/shiny.pal").decode("ascii")), 2))
        parts.append(emit(f"gAraunaIcon_{index:03d}", "u8", list(icon), 4))

    text = "\n".join(parts)
    previous = HEADER.read_text(encoding="ascii") if HEADER.exists() else ""
    if args.check:
        if text == previous:
            print(f"Graphics header matches the art pack ({SPECIES} species)")
            return 0
        print("Graphics header does not match the editable art pack.", file=sys.stderr)
        print("Run tools/arauna/repack_graphics_from_art_pack.py to rebuild it.", file=sys.stderr)
        return 1

    HEADER.write_text(text, encoding="ascii")
    print(f"repacked {SPECIES} species from the art pack")
    print(f"  sprite data: {raw_total} raw -> {packed_total} compressed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

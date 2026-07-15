#!/usr/bin/env python3
"""Validate the Araucaria Village art assets and material palette mapping."""

from __future__ import annotations

import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TILESET = ROOT / "data/tilesets/secondary/araucaria_village"
MATERIAL_PALETTES = tuple(range(6, 14))


def fail(message: str) -> None:
    raise ValueError(message)


def expected_bank(metatile_id: int) -> int:
    if metatile_id <= 0x201:
        return 7
    if metatile_id in {0x202, 0x203, 0x204, 0x206, 0x207, 0x22F}:
        return 6
    if metatile_id == 0x205:
        return 8
    if 0x208 <= metatile_id <= 0x21F:
        return 9
    if 0x220 <= metatile_id <= 0x22E:
        return 10
    if 0x230 <= metatile_id <= 0x249:
        return 8
    if 0x24A <= metatile_id <= 0x24F:
        return 11
    if 0x250 <= metatile_id <= 0x252:
        return 12
    if metatile_id == 0x253:
        return 13
    if 0x254 <= metatile_id <= 0x266:
        return 7
    return 6


def read_palette(bank: int) -> tuple[tuple[int, int, int], ...]:
    path = TILESET / "palettes" / f"{bank:02}.pal"
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"]:
        fail(f"{path.relative_to(ROOT)} must be a 16-color JASC palette")
    try:
        colors = tuple(tuple(map(int, line.split())) for line in lines[3:])
    except ValueError as error:
        fail(f"{path.relative_to(ROOT)} contains a non-numeric color: {error}")
    if len(colors) != 16 or any(len(color) != 3 for color in colors):
        fail(f"{path.relative_to(ROOT)} must contain exactly 16 RGB colors")
    if any(not 0 <= channel <= 255 for color in colors for channel in color):
        fail(f"{path.relative_to(ROOT)} contains a channel outside 0..255")
    return colors


def validate_png() -> None:
    path = TILESET / "tiles.png"
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        fail(f"{path.relative_to(ROOT)} is not a valid PNG header")
    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
    if (width, height, bit_depth, color_type) != (128, 152, 4, 3):
        fail(
            f"{path.relative_to(ROOT)} must remain 128x152, 4-bit indexed; "
            f"got {width}x{height}, depth {bit_depth}, type {color_type}"
        )


def validate_metatile_banks() -> None:
    path = TILESET / "metatiles.bin"
    data = path.read_bytes()
    if len(data) != 2304:
        fail(f"{path.relative_to(ROOT)} must contain 144 eight-tile metatiles")
    entries = struct.unpack(f"<{len(data) // 2}H", data)
    for index in range(0x67):
        metatile_id = 0x200 + index
        expected = expected_bank(metatile_id)
        for entry in entries[index * 8 : index * 8 + 8]:
            if entry & 0x3FF and entry >> 12 != expected:
                fail(
                    f"metatile {metatile_id:#05x} uses palette {entry >> 12}; "
                    f"expected material bank {expected}"
                )


def validate_transition_behaviors() -> None:
    attributes_path = TILESET / "metatile_attributes.bin"
    attributes = attributes_path.read_bytes()
    if len(attributes) != 288:
        fail(f"{attributes_path.relative_to(ROOT)} must contain 144 attributes")
    expected = {0x264: 0x69, 0x265: 0x69, 0x266: 0x62}
    for metatile_id, behavior in expected.items():
        actual = attributes[(metatile_id - 0x200) * 2]
        if actual != behavior:
            fail(
                f"metatile {metatile_id:#05x} behavior is {actual:#04x}; "
                f"expected {behavior:#04x}"
            )


def validate_village_terrain() -> None:
    path = ROOT / "data/layouts/AraunaMapLab/map.bin"
    data = path.read_bytes()
    if len(data) != 800:
        fail(f"{path.relative_to(ROOT)} must remain a 20x20 layout")
    blocks = struct.unpack("<400H", data)
    flat_paths = [index for index, block in enumerate(blocks) if block & 0x3FF in {0x200, 0x201}]
    if flat_paths:
        fail(f"village still uses flat path metatiles at {flat_paths[:8]}")
    expected = {(5, 6): 0x264, (5, 18): 0x265, (18, 10): 0x266}
    for (x, y), metatile_id in expected.items():
        actual = blocks[y * 20 + x] & 0x3FF
        if actual != metatile_id:
            fail(
                f"village transition {(x, y)} uses {actual:#05x}; "
                f"expected {metatile_id:#05x}"
            )


def main() -> int:
    validate_png()
    palettes = [read_palette(bank) for bank in MATERIAL_PALETTES]
    if len(set(palettes)) != len(palettes):
        fail("material palettes 06..13 must remain visually distinct")
    validate_metatile_banks()
    validate_transition_behaviors()
    validate_village_terrain()
    print(
        "Validated the 4bpp Araucaria tilesheet, material palettes, organic "
        "road masks, textured ground, and three functional transition tiles."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Araucaria art validation failed: {error}", file=sys.stderr)
        sys.exit(1)

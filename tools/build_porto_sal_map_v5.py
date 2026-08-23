#!/usr/bin/env python3
"""Build Porto do Sal V5 from the certified Porto do Sal V3 baseline.

V5 keeps the successful patch-based visual language and only strengthens the
south-sector composition: the market stall is shifted west to join the main
market flow, while the engineer-quay apron is extended toward the shipyard.
No random or formula-drawn geometry is used.
"""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_BIN = ROOT / "data/layouts/SlateportCity/map.bin"
MAP_JSON = ROOT / "data/maps/SlateportCity/map.json"

WIDTH, HEIGHT = 40, 60
CELL_COUNT = WIDTH * HEIGHT
MASK_METATILE = 0x03FF
MASK_PHYSICAL = 0xFC00

V3_RAW_SHA1 = "664c661e163661cc3d5f7c4ae4cd552c2297e16c"
V5_RAW_SHA1 = "b6821b5fa6106917761c5e473725e720d10fb893"
EXPECTED_CHANGED_FROM_V3 = 42


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def idx(x: int, y: int) -> int:
    return y * WIDTH + x


def protect_box(out: set[tuple[int, int]], x: int, y: int, rx: int, ry: int) -> None:
    for yy in range(max(0, y - ry), min(HEIGHT, y + ry + 1)):
        for xx in range(max(0, x - rx), min(WIDTH, x + rx + 1)):
            out.add((xx, yy))


def protected_cells(map_data: dict) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for event in map_data.get("object_events", []):
        protect_box(
            out,
            int(event["x"]),
            int(event["y"]),
            int(event.get("movement_range_x", 0)),
            int(event.get("movement_range_y", 0)),
        )
    for event in map_data.get("warp_events", []):
        x, y = int(event["x"]), int(event["y"])
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            protect_box(out, x, y, 1, 1)
    for event in map_data.get("bg_events", []):
        protect_box(out, int(event["x"]), int(event["y"]), 1, 1)
    for event in map_data.get("coord_events", []):
        x, y = int(event["x"]), int(event["y"])
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            out.add((x, y))
    return out


def copy_walkable_patch(
    original: list[int],
    values: list[int],
    protected: set[tuple[int, int]],
    source_xy: tuple[int, int],
    size: tuple[int, int],
    target_xy: tuple[int, int],
    label: str,
) -> None:
    sx, sy = source_xy
    width, height = size
    tx, ty = target_xy
    source_metatiles: list[int] = []

    for yy in range(height):
        for xx in range(width):
            value = original[idx(sx + xx, sy + yy)]
            if (value & MASK_PHYSICAL) != 0x3000:
                raise RuntimeError(f"{label}: source ({sx + xx},{sy + yy}) is not walkable elevation 3")
            source_metatiles.append(value & MASK_METATILE)

    k = 0
    for yy in range(height):
        for xx in range(width):
            x, y = tx + xx, ty + yy
            if (x, y) in protected:
                raise RuntimeError(f"{label}: target ({x},{y}) is gameplay-protected")
            i = idx(x, y)
            old = values[i]
            if (old & MASK_PHYSICAL) != 0x3000:
                raise RuntimeError(f"{label}: target ({x},{y}) is not walkable elevation 3")
            values[i] = (old & MASK_PHYSICAL) | source_metatiles[k]
            k += 1


def build(source: bytes, map_data: dict) -> bytes:
    if len(source) != CELL_COUNT * 2:
        raise RuntimeError(f"map.bin has {len(source)} bytes; expected {CELL_COUNT * 2}")
    if sha1(source) != V3_RAW_SHA1:
        raise RuntimeError(f"V5 requires certified V3 {V3_RAW_SHA1}; got {sha1(source)}")

    original = list(struct.unpack(f"<{CELL_COUNT}H", source))
    values = list(original)
    protected = protected_cells(map_data)

    copy_walkable_patch(
        original, values, protected,
        source_xy=(2, 41), size=(5, 2), target_xy=(13, 53),
        label="Mercado das Marés - ala costeira",
    )

    copy_walkable_patch(
        original, values, protected,
        source_xy=(21, 57), size=(5, 2), target_xy=(15, 55),
        label="Mercado das Marés - pátio de sal",
    )

    copy_walkable_patch(
        original, values, protected,
        source_xy=(28, 51), size=(9, 2), target_xy=(27, 40),
        label="Cais dos Engenheiros - núcleo",
    )

    copy_walkable_patch(
        original, values, protected,
        source_xy=(28, 51), size=(5, 2), target_xy=(22, 40),
        label="Cais dos Engenheiros - ligação ao estaleiro",
    )

    changed = sum(a != b for a, b in zip(original, values))
    if changed != EXPECTED_CHANGED_FROM_V3:
        raise RuntimeError(f"Expected {EXPECTED_CHANGED_FROM_V3} V5 changes from V3; got {changed}")

    for i, (old, new) in enumerate(zip(original, values)):
        if (old & MASK_PHYSICAL) != (new & MASK_PHYSICAL):
            raise RuntimeError(f"Physical bits changed at ({i % WIDTH},{i // WIDTH})")

    output = struct.pack(f"<{CELL_COUNT}H", *values)
    if sha1(output) != V5_RAW_SHA1:
        raise RuntimeError(f"Unexpected V5 output hash: {sha1(output)}")
    return output


def main() -> None:
    map_data = json.loads(MAP_JSON.read_text(encoding="utf-8"))
    output = build(MAP_BIN.read_bytes(), map_data)
    MAP_BIN.write_bytes(output)
    print("Porto do Sal V5: market + engineer-quay stitching applied.")
    print(f"SHA1: {sha1(output)}")


if __name__ == "__main__":
    main()

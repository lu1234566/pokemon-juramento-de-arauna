#!/usr/bin/env python3
"""Build Araucarias Village from the vanilla Emerald General/Petalburg tilesets.

The source map is Littleroot only as a library of valid metatile blocks.  The
result moves the laboratory, removes the mirrored two-house composition, adds
an east-facing village plaza, and preserves independent Arauna map data.
"""

from __future__ import annotations

import argparse
import struct
from pathlib import Path


WIDTH = 20
HEIGHT = 20
GRASS = 0x3001
FLOWER = 0x3004


def read_grid(path: Path) -> list[list[int]]:
    data = path.read_bytes()
    expected = WIDTH * HEIGHT * 2
    if len(data) != expected:
        raise ValueError(f"{path} must contain {expected} bytes, found {len(data)}")
    values = struct.unpack(f"<{WIDTH * HEIGHT}H", data)
    return [list(values[y * WIDTH:(y + 1) * WIDTH]) for y in range(HEIGHT)]


def write_grid(path: Path, grid: list[list[int]]) -> None:
    values = [value for row in grid for value in row]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(struct.pack(f"<{len(values)}H", *values))


def copy_rect(
    source: list[list[int]],
    target: list[list[int]],
    source_x: int,
    source_y: int,
    width: int,
    height: int,
    target_x: int,
    target_y: int,
) -> None:
    snapshot = [row[source_x:source_x + width] for row in source[source_y:source_y + height]]
    for y, row in enumerate(snapshot):
        target[target_y + y][target_x:target_x + width] = row


def fill_rect(grid: list[list[int]], x: int, y: int, width: int, height: int, value: int) -> None:
    for row in range(y, y + height):
        grid[row][x:x + width] = [value] * width


def paint_open_east_plaza(grid: list[list[int]]) -> None:
    # Petalburg's soft path tiles: a five-tile-high plaza open to the east.
    left, right = 3, 19
    top, bottom = 9, 13
    grid[top][left] = 0x31D0
    for x in range(left + 1, right + 1):
        grid[top][x] = 0x31D1
    for y in range(top + 1, bottom):
        grid[y][left] = 0x31D8
        for x in range(left + 1, right + 1):
            grid[y][x] = 0x31D9
    grid[bottom][left] = 0x31E0
    for x in range(left + 1, right + 1):
        grid[bottom][x] = 0x31E1

    # Short branch from the relocated research-center door into the plaza.
    grid[8][13] = 0x31D8
    grid[8][14] = 0x31D9
    grid[8][15] = 0x31DA
    for x in range(13, 16):
        grid[9][x] = 0x31D9


def build(source_path: Path) -> list[list[int]]:
    source = read_grid(source_path)
    grid = [row[:] for row in source]

    # Capture Birch's 7 x 5 laboratory before clearing its original location.
    laboratory = [row[3:10] for row in source[12:17]]

    # Remove the second house and the old southern laboratory footprint.
    fill_rect(grid, 11, 3, 8, 7, GRASS)
    fill_rect(grid, 2, 12, 9, 6, GRASS)

    # Place the research center in the northeast, facing the central plaza.
    for y, row in enumerate(laboratory):
        grid[3 + y][10:17] = row

    paint_open_east_plaza(grid)

    # A small flower garden distinguishes the quieter southern clearing.
    for x, y in ((4, 15), (5, 15), (6, 15), (4, 16), (6, 16), (8, 17), (9, 17)):
        grid[y][x] = FLOWER

    # Required anchors: vanilla animated doors and a walkable route edge.
    anchors = {
        "player_house": (5, 8, 0x0648),
        "research_center": (14, 7, 0x0649),
        "mist_route_edge": (19, 11, 0x31D9),
    }
    for name, (x, y, expected) in anchors.items():
        actual = grid[y][x]
        if actual != expected:
            raise ValueError(f"{name} anchor at {(x, y)} is {actual:#06x}, expected {expected:#06x}")

    if grid == source:
        raise ValueError("Arauna village must not duplicate Littleroot")
    return grid


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("data/layouts/LittlerootTown/map.bin"),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/layouts/AraunaMapLab/map.bin"),
    )
    args = parser.parse_args()
    grid = build(args.source)
    write_grid(args.out, grid)
    print(f"wrote {args.out} ({WIDTH} x {HEIGHT}, General + Petalburg)")


if __name__ == "__main__":
    main()

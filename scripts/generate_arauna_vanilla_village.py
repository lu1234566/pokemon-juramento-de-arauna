#!/usr/bin/env python3
"""Build Vila Amanhecer from the vanilla Emerald General/Petalburg tilesets.

Littleroot is used only as a library of valid metatile blocks (its house and
laboratory, tree border, soft dirt path). The result is an authored village:
the player's house on the west and the research centre on the east frame a
central dirt avenue that reads straight out to the eastern forest trail, a
short southern spur opens a small clearing to explore, and a tree line frames
the whole clearing so the single exit is obvious.
"""

from __future__ import annotations

import argparse
import struct
from collections import deque
from pathlib import Path

WIDTH = 20
HEIGHT = 20

GRASS = 0x3001
FLOWER = 0x3004
# Petalburg soft-dirt path, 9-slice
P_FILL = 0x31D9
P_TOP, P_TL, P_TR = 0x31D1, 0x31D0, 0x31D2
P_L, P_R = 0x31D8, 0x31DA
P_BOT, P_BL, P_BR = 0x31E1, 0x31E0, 0x31E2
# Tree border 2x2 canopy unit
TREE = ((0x05D4, 0x05D5), (0x05DC, 0x05DD))


def read_grid(path: Path) -> list[list[int]]:
    data = path.read_bytes()
    values = struct.unpack(f"<{WIDTH * HEIGHT}H", data)
    return [list(values[y * WIDTH:(y + 1) * WIDTH]) for y in range(HEIGHT)]


def write_grid(path: Path, grid: list[list[int]]) -> None:
    values = [v for row in grid for v in row]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(struct.pack(f"<{len(values)}H", *values))


def blit(dst, block, tx, ty):
    for y, row in enumerate(block):
        dst[ty + y][tx:tx + len(row)] = list(row)


def tree_column(grid, x, y0, y1):
    """Fill a 2-wide tree wall between rows y0..y1 (inclusive) at cols x,x+1."""
    y = y0
    while y <= y1:
        for dy in range(2):
            if y + dy <= y1:
                for dx in range(2):
                    grid[y + dy][x + dx] = TREE[dy][dx]
        y += 2


def path_rect(grid, x0, y0, x1, y1):
    """Lay a soft-dirt path over the rectangle, 9-slicing edges against grass."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            top = y == y0
            bot = y == y1
            left = x == x0
            right = x == x1
            if top and left:      grid[y][x] = P_TL
            elif top and right:   grid[y][x] = P_TR
            elif bot and left:    grid[y][x] = P_BL
            elif bot and right:   grid[y][x] = P_BR
            elif top:             grid[y][x] = P_TOP
            elif bot:             grid[y][x] = P_BOT
            elif left:            grid[y][x] = P_L
            elif right:           grid[y][x] = P_R
            else:                 grid[y][x] = P_FILL


def build(source_path: Path) -> list[list[int]]:
    source = read_grid(source_path)
    house = [row[2:7] for row in source[4:9]]      # player house, door 0x0648 at rel (3,4)
    lab = [row[3:10] for row in source[12:17]]     # Birch lab 7x5, door 0x0649 at rel (4,4)

    grid = [[GRASS] * WIDTH for _ in range(HEIGHT)]

    # Tree frame: top, bottom, left, and right — with a 3-tile exit gap on the
    # east at rows 10-12 leading to the forest trail.
    for x in range(0, WIDTH, 2):
        blit(grid, TREE, x, 0)          # top
        blit(grid, TREE, x, 18)         # bottom
    tree_column(grid, 0, 2, 17)         # west wall
    tree_column(grid, 18, 2, 9)         # east wall (above the exit)
    tree_column(grid, 18, 13, 17)       # east wall (below the exit)

    # Buildings: house on the west, research centre on the east.
    blit(grid, house, 3, 3)             # door -> (6, 7)
    blit(grid, lab, 10, 3)              # door -> (14, 7)

    # Central avenue (rows 10-12) spanning west spur to the east exit.
    path_rect(grid, 4, 10, 19, 12)
    # Front plaza linking both doorsteps along the building fronts.
    path_rect(grid, 6, 9, 14, 9)
    # Door approaches down into the plaza.
    grid[8][6] = P_FILL                 # under the house door
    grid[8][14] = P_FILL                # under the lab door
    # Southern spur into a small clearing to explore
    path_rect(grid, 9, 13, 10, 16)
    # Flower clearing at the end of the spur
    for x, y in ((7, 15), (8, 15), (11, 15), (12, 15), (7, 16), (12, 16), (8, 17), (11, 17)):
        grid[y][x] = FLOWER

    if grid == source:
        raise ValueError("Vila Amanhecer must not duplicate Littleroot")

    # Reachability: house door approach must reach the eastern trail edge.
    def walkable(x, y):
        e = grid[y][x]
        return ((e >> 10) & 0x3) == 0 or (e & 0x3FF) in {0x248, 0x249}
    start = (6, 8)
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in seen and walkable(nx, ny):
                seen.add((nx, ny)); q.append((nx, ny))
    required = {(6, 8), (14, 8), (18, 11), (19, 11), (9, 16)}
    missing = required - seen
    if missing:
        raise ValueError(f"village anchors disconnected: {sorted(missing)}")
    return grid


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=Path("data/layouts/LittlerootTown/map.bin"))
    ap.add_argument("--out", type=Path, default=Path("data/layouts/AraunaMapLab/map.bin"))
    args = ap.parse_args()
    write_grid(args.out, build(args.source))
    print(f"wrote {args.out} ({WIDTH} x {HEIGHT})")


if __name__ == "__main__":
    main()

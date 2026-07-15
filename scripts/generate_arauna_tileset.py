#!/usr/bin/env python3
"""Reproduce the first deterministic Araucarias Village GBA tileset revision.

The committed assets remain editable in Porymap.  This bootstrap generator emits
their original 4-bit indexed PNG, metatiles, attributes, palettes, and 20 x 20
layout without Pillow or any non-standard Python package.
"""

from __future__ import annotations

import argparse
import binascii
import math
import struct
import zlib
from pathlib import Path
from typing import Iterable


TILE_SIZE = 8
SHEET_WIDTH = 128
TILES_PER_ROW = SHEET_WIDTH // TILE_SIZE
METATILE_SIZE = 16
METATILE_COUNT = 144
MAP_WIDTH = 20
MAP_HEIGHT = 20
SECONDARY_METATILE_OFFSET = 0x200
SECONDARY_PALETTE = 6
EXPECTED_TILE_COUNT = 297


def rgb555_channel(value: int) -> int:
    level = round(value * 31 / 255)
    return round(level * 255 / 31)


def rgb555(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(rgb555_channel(value) for value in rgb)


PALETTE = [
    rgb555((0, 0, 0)),       # 0 transparent
    rgb555((16, 24, 27)),    # 1 outline / deep shadow
    rgb555((38, 52, 56)),    # 2 charcoal
    rgb555((70, 88, 90)),    # 3 wet basalt
    rgb555((113, 129, 125)), # 4 light basalt
    rgb555((181, 194, 184)), # 5 mist / plaster
    rgb555((21, 58, 42)),    # 6 deep araucaria green
    rgb555((40, 88, 58)),    # 7 pine green
    rgb555((78, 117, 74)),   # 8 moss
    rgb555((130, 144, 91)),  # 9 lichen
    rgb555((74, 51, 41)),    # 10 dark earth / trunk
    rgb555((117, 81, 58)),   # 11 old timber / earth light
    rgb555((154, 104, 76)),  # 12 weathered roof
    rgb555((177, 135, 85)),  # 13 light timber / rope
    rgb555((210, 165, 93)),  # 14 amber light
    rgb555((113, 51, 58)),   # 15 oath ribbon
]


class Canvas:
    def __init__(self, width: int, height: int, fill: int = 0) -> None:
        self.width = width
        self.height = height
        self.pixels = [[fill for _ in range(width)] for _ in range(height)]

    def set(self, x: int, y: int, color: int) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color

    def rect(self, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
        for y in range(max(0, y0), min(self.height, y1)):
            for x in range(max(0, x0), min(self.width, x1)):
                self.pixels[y][x] = color

    def line(self, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        error = dx + dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            twice = 2 * error
            if twice >= dy:
                error += dy
                x0 += sx
            if twice <= dx:
                error += dx
                y0 += sy

    def paste(self, other: "Canvas", x0: int, y0: int, transparent: int | None = None) -> None:
        for y, row in enumerate(other.pixels):
            for x, color in enumerate(row):
                if transparent is None or color != transparent:
                    self.set(x0 + x, y0 + y, color)

    def crop(self, x0: int, y0: int, width: int, height: int) -> "Canvas":
        result = Canvas(width, height)
        for y in range(height):
            for x in range(width):
                result.set(x, y, self.pixels[y0 + y][x0 + x])
        return result


def textured(width: int, height: int, base: int, accent: int, seed: int, density: int = 23) -> Canvas:
    result = Canvas(width, height, base)
    for y in range(height):
        for x in range(width):
            value = (x * 11 + y * 7 + seed * 13 + (x * y)) % density
            if value in (0, 3):
                result.set(x, y, accent)
    return result


def moss_ground(seed: int = 0) -> Canvas:
    result = textured(16, 16, 8, 7, seed, 29)
    for y in range(2, 16, 6):
        for x in range((seed + y) % 5, 16, 7):
            result.set(x, y, 9)
    return result


def earth_ground(seed: int = 0) -> Canvas:
    result = textured(16, 16, 10, 11, seed, 31)
    for x, y in ((2, 4), (11, 2), (7, 12), (14, 8)):
        result.set((x + seed) % 16, y, 3)
    return result


def basalt_path(seed: int = 0) -> Canvas:
    result = Canvas(16, 16, 2)
    stones = [
        (1, 1, 7, 6, 3), (8, 1, 15, 7, 4),
        (0, 8, 6, 15, 4), (7, 8, 14, 15, 3),
    ]
    for index, (x0, y0, x1, y1, color) in enumerate(stones):
        result.rect(x0, y0, x1, y1, color)
        result.line(x0 + 1, y0 + 1, x1 - 2, y0 + 1, 4 if color == 3 else 5)
        if (index + seed) % 2:
            result.set(x1 - 2, y1 - 2, 8)
    return result


def basalt_steps() -> Canvas:
    result = Canvas(16, 16, 2)
    for y in range(0, 16, 4):
        result.rect(0, y, 16, y + 3, 3 if (y // 4) % 2 else 4)
        result.line(0, y + 3, 15, y + 3, 1)
        result.set((y * 3) % 15, y + 1, 8)
    return result


def forest_wall(seed: int = 0) -> Canvas:
    result = Canvas(16, 16, 6)
    centers = ((2, 4), (7, 2), (13, 4), (4, 10), (10, 9), (14, 13), (2, 15), (8, 15))
    for number, (cx, cy) in enumerate(centers):
        radius = 3 if number % 3 else 4
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radius * radius:
                    noise = ((x // 2) * 37 + (y // 2) * 19 + (x // 4) * (y // 3) * 11 + seed + number * 5) % 11
                    color = 6 if noise < 3 else 7 if noise < 7 else 8 if noise < 10 else 9
                    result.set(x, y, color)
    result.line(0, 15, 15, 15, 1)
    return result


def fern_detail(seed: int = 0) -> Canvas:
    result = moss_ground(seed)
    for stem_x in (5, 10):
        result.line(stem_x, 14, stem_x + (seed & 1), 5, 6)
        for y in range(7, 14, 2):
            x = stem_x + ((y + seed) & 1)
            result.set(x - 2, y, 7)
            result.set(x - 1, y - 1, 8)
            result.set(x + 2, y, 7)
            result.set(x + 1, y - 1, 9)
    return result


def puddle() -> Canvas:
    result = moss_ground(8)
    for y in range(5, 13):
        inset = abs(9 - y) // 2
        result.rect(3 + inset, y, 14 - inset, y + 1, 3)
    result.line(6, 6, 11, 6, 5)
    result.line(5, 10, 8, 10, 4)
    return result


def lantern_path() -> Canvas:
    result = basalt_path(3)
    result.rect(3, 3, 6, 13, 1)
    result.rect(2, 1, 7, 7, 1)
    result.rect(3, 2, 6, 6, 14)
    result.set(4, 3, 5)
    return result


def fence_detail() -> Canvas:
    result = moss_ground(6)
    result.rect(1, 5, 15, 8, 10)
    result.line(1, 5, 14, 5, 13)
    for x in (2, 7, 12):
        result.rect(x, 2, x + 2, 13, 11)
        result.set(x, 2, 13)
    return result


def make_house(variant: int) -> Canvas:
    width, height = 64, 48
    result = Canvas(width, height)
    for y in range(0, height, 16):
        for x in range(0, width, 16):
            result.paste(moss_ground(variant + x // 16 + y // 16), x, y)

    left = 3 + variant
    right = 61 - (variant * 2)
    ridge_x = 31 + variant * 2
    for y in range(3, 22):
        inset = max(0, 10 - y // 2)
        result.rect(left + inset, y, right - inset, y + 1, 12)
        for x in range(left + inset + 2, right - inset, 6):
            result.set(x + (y & 1), y, 15 if (x + y + variant) % 17 == 0 else 11)
    result.line(ridge_x - 2, 2, left, 21, 1)
    result.line(ridge_x + 2, 2, right - 1, 21, 1)
    result.line(left, 21, right - 1, 21, 1)
    result.rect(left + 4, 22, right - 4, 42, 5)
    for y in range(24, 41, 6):
        result.line(left + 5, y, right - 6, y, 4)
    result.rect(left + 3, 40, right - 3, 46, 3)
    result.line(left + 3, 40, right - 4, 40, 1)

    door_x = 29 + variant * 8
    result.rect(door_x, 29, door_x + 8, 46, 1)
    result.rect(door_x + 2, 31, door_x + 6, 46, 10)
    result.set(door_x + 5, 38, 14)
    for window_x in (left + 10, right - 18):
        if door_x - 6 <= window_x <= door_x + 8:
            continue
        result.rect(window_x, 28, window_x + 9, 37, 1)
        result.rect(window_x + 2, 30, window_x + 7, 35, 14)
        result.line(window_x + 4, 30, window_x + 4, 35, 13)
    result.rect(left - 1, 43, right + 1, 46, 10)
    return result


def make_research_house() -> Canvas:
    width, height = 80, 48
    result = Canvas(width, height)
    for y in range(0, height, 16):
        for x in range(0, width, 16):
            result.paste(moss_ground(20 + x // 16 + y // 16), x, y)
    result.rect(3, 12, 77, 22, 12)
    for y in range(3, 13):
        inset = 11 - y
        result.rect(3 + inset, y, 77 - inset, y + 1, 12)
    result.line(13, 2, 67, 2, 1)
    result.line(2, 22, 77, 22, 1)
    for x in range(7, 75, 8):
        result.line(x, 5, x - 5, 20, 15 if x in (31, 55) else 11)
    result.rect(7, 23, 73, 42, 5)
    result.rect(5, 40, 75, 46, 3)
    result.line(5, 40, 74, 40, 1)
    for window_x in (11, 25, 51, 65):
        result.rect(window_x, 28, window_x + 8, 36, 1)
        result.rect(window_x + 2, 30, window_x + 6, 34, 14)
    result.rect(36, 27, 45, 46, 1)
    result.rect(38, 29, 43, 46, 10)
    result.set(42, 37, 14)
    result.rect(31, 18, 50, 24, 10)
    result.rect(33, 19, 48, 22, 13)
    return result


def foliage_blob(canvas: Canvas, cx: int, cy: int, rx: int, ry: int, seed: int) -> None:
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            if ((x - cx) ** 2) * ry * ry + ((y - cy) ** 2) * rx * rx <= rx * rx * ry * ry:
                noise = ((x // 2) * 37 + (y // 2) * 19 + (x // 4) * (y // 3) * 11 + seed * 13) % 11
                color = 6 if noise < 3 else 7 if noise < 7 else 8 if noise < 10 else 9
                canvas.set(x, y, color)


def make_ancient_araucaria() -> Canvas:
    width, height = 64, 80
    result = Canvas(width, height)
    for y in range(0, height, 16):
        for x in range(0, width, 16):
            result.paste(moss_ground(40 + x // 16 + y // 16), x, y)
    result.rect(27, 30, 38, 70, 10)
    result.rect(29, 31, 34, 70, 11)
    for y in range(35, 68, 8):
        result.set(28, y, 13)
        result.set(35, y + 2, 2)
    result.line(22, 72, 31, 66, 10)
    result.line(41, 73, 34, 66, 10)

    for blob in (
        (32, 10, 16, 7, 1),
        (19, 17, 13, 7, 2), (45, 17, 13, 7, 3),
        (32, 25, 24, 8, 4),
        (13, 34, 12, 7, 5), (32, 34, 16, 8, 6), (51, 34, 12, 7, 7),
        (23, 43, 18, 7, 8), (43, 43, 18, 7, 9),
    ):
        foliage_blob(result, *blob)
    result.line(8, 49, 56, 49, 1)
    result.rect(26, 48, 39, 53, 10)
    result.rect(25, 52, 40, 54, 15)
    result.set(24, 53, 14)
    result.set(41, 54, 14)
    return result


def make_small_araucaria(seed: int) -> Canvas:
    result = Canvas(32, 48)
    for y in range(0, 48, 16):
        for x in range(0, 32, 16):
            result.paste(moss_ground(seed + x // 16 + y // 16), x, y)
    result.rect(14, 19, 19, 43, 10)
    result.rect(15, 20, 17, 43, 11)
    foliage_blob(result, 16, 8, 8, 6, seed)
    foliage_blob(result, 9, 16, 8, 6, seed + 1)
    foliage_blob(result, 23, 16, 8, 6, seed + 2)
    foliage_blob(result, 16, 24, 13, 7, seed + 3)
    result.line(3, 31, 29, 31, 1)
    return result


def slice_module(module: Canvas) -> list[Canvas]:
    blocks: list[Canvas] = []
    for y in range(0, module.height, METATILE_SIZE):
        for x in range(0, module.width, METATILE_SIZE):
            blocks.append(module.crop(x, y, METATILE_SIZE, METATILE_SIZE))
    return blocks


def build_metatile_images() -> list[Canvas]:
    definitions: list[Canvas] = [
        earth_ground(0),          # 0 dark earth
        earth_ground(5),          # 1 dark earth variation
        moss_ground(0),           # 2 mossy village ground
        basalt_path(0),           # 3 wet basalt path
        basalt_steps(),           # 4 basalt steps
        forest_wall(0),           # 5 blocked forest border
        fern_detail(0),           # 6 fern detail
        puddle(),                  # 7 puddle detail
    ]
    definitions.extend(slice_module(make_house(0)))               # 8..19
    definitions.extend(slice_module(make_house(1)))               # 20..31
    definitions.extend(slice_module(make_research_house()))       # 32..46
    definitions.append(lantern_path())                             # 47
    definitions.extend(slice_module(make_ancient_araucaria()))    # 48..67
    definitions.extend(slice_module(make_small_araucaria(3)))     # 68..73
    definitions.extend(slice_module(make_small_araucaria(11)))    # 74..79
    definitions.extend([fence_detail(), fern_detail(8), lantern_path(), basalt_path(7)]) # 80..83
    while len(definitions) < METATILE_COUNT:
        definitions.append(moss_ground(0))
    return definitions[:METATILE_COUNT]


Tile = tuple[tuple[int, ...], ...]


def as_tile(canvas: Canvas) -> Tile:
    return tuple(tuple(row) for row in canvas.pixels)


def tile_ref(index: int, palette: int = SECONDARY_PALETTE) -> int:
    return SECONDARY_METATILE_OFFSET + index + (palette << 12)


def compile_tiles(images: list[Canvas]) -> tuple[list[Tile], list[list[int]]]:
    transparent = tuple(tuple(0 for _ in range(8)) for _ in range(8))
    tiles: list[Tile] = [transparent]
    tile_indices: dict[Tile, int] = {transparent: 0}
    definitions: list[list[int]] = []
    for image in images:
        references: list[int] = []
        for y in (0, 8):
            for x in (0, 8):
                pixels = as_tile(image.crop(x, y, 8, 8))
                index = tile_indices.get(pixels)
                if index is None:
                    index = len(tiles)
                    if index >= 512:
                        raise RuntimeError("Secondary tileset exceeded the 512-tile GBA limit")
                    tiles.append(pixels)
                    tile_indices[pixels] = index
                references.append(tile_ref(index))
        definitions.append(references + [0, 0, 0, 0])
    return tiles, definitions


def png_chunk(kind: bytes, data: bytes) -> bytes:
    checksum = binascii.crc32(kind + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", checksum)


def write_indexed_png(path: Path, pixels: list[list[int]]) -> None:
    packed_rows = []
    for row in pixels:
        packed = bytearray([0])
        for x in range(0, len(row), 2):
            packed.append((row[x] << 4) | row[x + 1])
        packed_rows.append(bytes(packed))
    palette_bytes = bytes(channel for color in PALETTE for channel in color)
    ihdr = struct.pack(">IIBBBBB", len(pixels[0]), len(pixels), 4, 3, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n"
    data += png_chunk(b"IHDR", ihdr)
    data += png_chunk(b"PLTE", palette_bytes)
    data += png_chunk(b"IDAT", zlib.compress(b"".join(packed_rows), 9))
    data += png_chunk(b"IEND", b"")
    path.write_bytes(data)


def compose_sheet(tiles: list[Tile]) -> list[list[int]]:
    rows = max(1, math.ceil(len(tiles) / TILES_PER_ROW))
    sheet = [[0 for _ in range(SHEET_WIDTH)] for _ in range(rows * TILE_SIZE)]
    for index, pixels in enumerate(tiles):
        x0 = (index % TILES_PER_ROW) * TILE_SIZE
        y0 = (index // TILES_PER_ROW) * TILE_SIZE
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                sheet[y0 + y][x0 + x] = pixels[y][x]
    return sheet


def write_metatiles(path: Path, definitions: list[list[int]]) -> None:
    values = [value for definition in definitions for value in definition]
    path.write_bytes(struct.pack(f"<{len(values)}H", *values))


def write_attributes(path: Path) -> None:
    # MB_NORMAL + METATILE_LAYER_TYPE_NORMAL. Collision lives in map.bin.
    path.write_bytes(struct.pack(f"<{METATILE_COUNT}H", *([0] * METATILE_COUNT)))


def write_palettes(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    contents = "JASC-PAL\n0100\n16\n" + "\n".join(f"{r} {g} {b}" for r, g, b in PALETTE) + "\n"
    for index in range(16):
        (directory / f"{index:02}.pal").write_text(contents, encoding="ascii")


def map_entry(metatile: int, collision: int = 0, elevation: int = 3) -> int:
    return SECONDARY_METATILE_OFFSET + metatile + (collision << 10) + (elevation << 12)


def place_module(grid: list[list[int]], x0: int, y0: int, start: int, width: int, height: int) -> None:
    for y in range(height):
        for x in range(width):
            grid[y0 + y][x0 + x] = map_entry(start + y * width + x, collision=1, elevation=0)


def build_map() -> list[list[int]]:
    grid = [[map_entry(2) for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    # Impassable forest frame; the eastern opening foreshadows Route 1.
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if x < 2 or x >= MAP_WIDTH - 2 or y < 2 or y >= MAP_HEIGHT - 1:
                grid[y][x] = map_entry(5, collision=3, elevation=3)
    for x in (18, 19):
        grid[10][x] = map_entry(3)

    # Dark-earth paths: east entrance, central clearing, research post and south seal.
    for x in range(7, 20):
        grid[10][x] = map_entry(0 if x % 2 else 1, elevation=3)
    for y in range(9, 19):
        for x in (9, 10, 11):
            grid[y][x] = map_entry(0 if (x + y) % 2 else 1)
    for x in range(5, 17):
        grid[13][x] = map_entry(0 if x % 2 else 1)
    for y in range(5, 10):
        grid[y][5] = map_entry(0 if y % 2 else 1)
        grid[y][15] = map_entry(0 if y % 2 else 1)

    # Houses, community research post, and the ancestral araucaria.
    place_module(grid, 2, 2, 8, 4, 3)
    place_module(grid, 14, 2, 20, 4, 3)
    place_module(grid, 2, 14, 32, 5, 3)
    place_module(grid, 8, 5, 48, 4, 5)

    # Smaller araucarias define the village edge without copying Hoenn trees.
    place_module(grid, 2, 7, 68, 2, 3)
    place_module(grid, 16, 14, 74, 2, 3)

    # Atmosphere and guidance accents.
    for x in (7, 12, 15, 18):
        grid[10][x] = map_entry(3 if x % 2 else 83, collision=1, elevation=0)
    grid[12][7] = map_entry(47, collision=1, elevation=0)
    grid[12][13] = map_entry(47, collision=1, elevation=0)
    grid[16][12] = map_entry(6)
    grid[17][15] = map_entry(7)
    grid[11][15] = map_entry(6)
    for x in (8, 9, 10, 11):
        grid[18][x] = map_entry(80, collision=1, elevation=0)
    return grid


def write_layout(layout_directory: Path, grid: list[list[int]]) -> None:
    layout_directory.mkdir(parents=True, exist_ok=True)
    values = [value for row in grid for value in row]
    (layout_directory / "map.bin").write_bytes(struct.pack(f"<{len(values)}H", *values))
    border = [map_entry(5, collision=3, elevation=3)] * 4
    (layout_directory / "border.bin").write_bytes(struct.pack("<4H", *border))


def rgb_pixels(indexed: Iterable[Iterable[int]]) -> list[list[tuple[int, int, int]]]:
    return [[PALETTE[color] for color in row] for row in indexed]


def write_rgb_png(path: Path, pixels: list[list[tuple[int, int, int]]]) -> None:
    raw_rows = []
    for row in pixels:
        raw_rows.append(bytes([0] + [channel for color in row for channel in color]))
    ihdr = struct.pack(">IIBBBBB", len(pixels[0]), len(pixels), 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n"
    data += png_chunk(b"IHDR", ihdr)
    data += png_chunk(b"IDAT", zlib.compress(b"".join(raw_rows), 9))
    data += png_chunk(b"IEND", b"")
    path.write_bytes(data)


def render_map_preview(path: Path, grid: list[list[int]], metatiles: list[Canvas]) -> None:
    result = Canvas(MAP_WIDTH * 16, MAP_HEIGHT * 16)
    for y, row in enumerate(grid):
        for x, entry in enumerate(row):
            index = (entry & 0x3FF) - SECONDARY_METATILE_OFFSET
            result.paste(metatiles[index], x * 16, y * 16)
    write_rgb_png(path, rgb_pixels(result.pixels))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tileset-output", type=Path, required=True)
    parser.add_argument("--layout-output", type=Path, required=True)
    parser.add_argument("--preview", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.tileset_output.mkdir(parents=True, exist_ok=True)
    metatile_images = build_metatile_images()
    tiles, definitions = compile_tiles(metatile_images)
    if len(tiles) != EXPECTED_TILE_COUNT:
        raise RuntimeError(f"Expected {EXPECTED_TILE_COUNT} unique tiles, generated {len(tiles)}")
    write_indexed_png(args.tileset_output / "tiles.png", compose_sheet(tiles))
    write_metatiles(args.tileset_output / "metatiles.bin", definitions)
    write_attributes(args.tileset_output / "metatile_attributes.bin")
    write_palettes(args.tileset_output / "palettes")
    grid = build_map()
    write_layout(args.layout_output, grid)
    if args.preview:
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        render_map_preview(args.preview, grid, metatile_images)
    print(f"Generated {len(tiles)} unique tiles, {METATILE_COUNT} metatiles, and a {MAP_WIDTH}x{MAP_HEIGHT} layout")


if __name__ == "__main__":
    main()

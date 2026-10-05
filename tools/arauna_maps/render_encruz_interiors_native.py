#!/usr/bin/env python3
"""Render a pokeemerald map.bin from the repository's real tileset assets.

This is intentionally independent from Porymap and the browser Map Studio so
review PNGs can be reproduced in a headless environment.  It follows the
standard Emerald 2-layer, 8-tile metatile layout.
"""
from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
PRIMARY_METATILE_LIMIT = 512
PRIMARY_TILE_LIMIT = 512
INDEX_GRAYS = (255, 238, 222, 205, 189, 172, 156, 139,
               115, 98, 82, 65, 49, 32, 16, 0)


def palette(path: Path) -> list[tuple[int, int, int]]:
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    if lines[:2] != ["JASC-PAL", "0100"] or int(lines[2]) != 16:
        raise ValueError(f"invalid JASC palette: {path}")
    return [tuple(map(int, line.split())) for line in lines[3:19]]


def indexed_tiles(path: Path) -> tuple[Image.Image, int, int]:
    image = Image.open(path).convert("RGB")
    if image.width % 8 or image.height % 8:
        raise ValueError(f"tile sheet must use an 8px grid: {path}")
    pixels = Image.new("L", image.size)
    src = image.load()
    dst = pixels.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue = src[x, y]
            if max(red, green, blue) - min(red, green, blue) > 2:
                raise ValueError(f"tile sheet is not indexed grayscale: {path}")
            dst[x, y] = min(range(16), key=lambda index: abs(red - INDEX_GRAYS[index]))
    return pixels, image.width // 8, image.width * image.height // 64


def words(path: Path) -> list[int]:
    raw = path.read_bytes()
    return list(struct.unpack(f"<{len(raw) // 2}H", raw))


def resolve_tileset(symbol: str) -> Path:
    prefix = "gTileset_"
    if not symbol.startswith(prefix):
        raise ValueError(f"unexpected tileset symbol: {symbol}")
    slug = symbol[len(prefix):]
    slug = "".join(("_" + c.lower()) if c.isupper() and i else c.lower()
                   for i, c in enumerate(slug))
    primary = ROOT / "data" / "tilesets" / "primary" / slug
    path = primary if primary.is_dir() else ROOT / "data" / "tilesets" / "secondary" / slug
    if not path.is_dir():
        raise FileNotFoundError(f"tileset directory not found for {symbol}: {path}")
    return path


class Renderer:
    def __init__(self, primary: Path, secondary: Path):
        self.primary = primary
        self.secondary = secondary
        self.primary_tiles = indexed_tiles(primary / "tiles.png")
        self.secondary_tiles = indexed_tiles(secondary / "tiles.png")
        self.primary_metatiles = words(primary / "metatiles.bin")
        self.secondary_metatiles = words(secondary / "metatiles.bin")
        self.palettes = [palette(primary / "palettes" / f"{i:02}.pal") for i in range(6)]
        self.palettes += [palette(secondary / "palettes" / f"{i:02}.pal") for i in range(6, 16)]

    def _tile(self, tile_id: int) -> Image.Image | None:
        if tile_id < PRIMARY_TILE_LIMIT:
            sheet, per_row, count = self.primary_tiles
            local = tile_id
        else:
            sheet, per_row, count = self.secondary_tiles
            local = tile_id - PRIMARY_TILE_LIMIT
        if not 0 <= local < count:
            # Emerald reserves VRAM-only slots for door/tileset animations.
            # They legitimately appear in metatiles but not in tiles.png.
            return None
        x = local % per_row * 8
        y = local // per_row * 8
        return sheet.crop((x, y, x + 8, y + 8))

    def metatile(self, metatile_id: int) -> Image.Image:
        if metatile_id < PRIMARY_METATILE_LIMIT:
            entries = self.primary_metatiles
            local = metatile_id
        else:
            entries = self.secondary_metatiles
            local = metatile_id - PRIMARY_METATILE_LIMIT
        start = local * 8
        if start + 8 > len(entries):
            raise IndexError(f"metatile {metatile_id} does not exist")
        out = Image.new("RGBA", (16, 16))
        positions = ((0, 0), (8, 0), (0, 8), (8, 8))
        for layer in range(2):
            for quadrant, (dx, dy) in enumerate(positions):
                raw = entries[start + layer * 4 + quadrant]
                tile_id = raw & 0x03FF
                hflip = bool(raw & 0x0400)
                vflip = bool(raw & 0x0800)
                pal_id = raw >> 12
                source = self._tile(tile_id)
                if source is None:
                    source = Image.new("L", (8, 8), 0)
                    # Loud diagnostic marker, matching Map Studio's missing
                    # tile behavior while keeping the render deterministic.
                    rgba = Image.new("RGBA", (8, 8), (255, 0, 255, 255))
                    out.alpha_composite(rgba, (dx, dy))
                    continue
                if hflip:
                    source = source.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                if vflip:
                    source = source.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                rgba = Image.new("RGBA", (8, 8))
                src = source.load()
                dst = rgba.load()
                pal = self.palettes[pal_id]
                for y in range(8):
                    for x in range(8):
                        index = src[x, y]
                        dst[x, y] = (*pal[index], 0 if index == 0 else 255)
                out.alpha_composite(rgba, (dx, dy))
        return out


def render_map(renderer: Renderer, path: Path, width: int, height: int) -> Image.Image:
    cells = words(path)
    if len(cells) != width * height:
        raise ValueError(f"{path}: {len(cells)} cells, expected {width * height}")
    out = Image.new("RGBA", (width * 16, height * 16))
    cache: dict[int, Image.Image] = {}
    for index, raw in enumerate(cells):
        metatile_id = raw & 0x03FF
        tile = cache.get(metatile_id)
        if tile is None:
            tile = renderer.metatile(metatile_id)
            cache[metatile_id] = tile
        out.alpha_composite(tile, ((index % width) * 16, (index // width) * 16))
    return out.convert("RGB")


def add_event_overlay(image: Image.Image, map_json: dict) -> Image.Image:
    out = image.copy()
    draw = ImageDraw.Draw(out)
    colors = {"warp_events": "#22d3ee", "coord_events": "#f97316",
              "object_events": "#e879f9", "bg_events": "#facc15"}
    for category, color in colors.items():
        for event in map_json.get(category, []):
            x, y = int(event["x"]), int(event["y"])
            draw.rectangle((x * 16 + 2, y * 16 + 2, x * 16 + 13, y * 16 + 13),
                           outline=color, width=2)
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("map_name")
    parser.add_argument("output", type=Path)
    parser.add_argument("--events", action="store_true")
    args = parser.parse_args()

    layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"]
    map_json_path = ROOT / "data/maps" / args.map_name / "map.json"
    map_json = json.loads(map_json_path.read_text())
    layout = next(item for item in layouts if item["id"] == map_json["layout"])
    renderer = Renderer(resolve_tileset(layout["primary_tileset"]),
                        resolve_tileset(layout["secondary_tileset"]))
    output = render_map(renderer, ROOT / layout["blockdata_filepath"],
                        int(layout["width"]), int(layout["height"]))
    if args.events:
        output = add_event_overlay(output, map_json)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.output)
    print(args.output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check all fixed/procedural map grids and the IRQ copy allocation."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(relative):
    return (ROOT / relative).read_text()
def number(text, name):
    return int(re.search(r"#define\s+" + name + r"\s+(\d+)", text)[1])
def grid(w, h):
    return (w + 15) * (h + 14)

capacity = number(read("include/fieldmap.h"), "MAX_MAP_DATA_SIZE")
layouts = json.loads(read("data/layouts/layouts.json"))["layouts"]
maximum = max(grid(row["width"], row["height"]) for row in layouts)
assert capacity % 16 == 0, "DMA fill requires a multiple of 32 bytes"
assert maximum <= capacity, (maximum, capacity)
pyramid = [row for row in layouts if row["name"].startswith("BattlePyramidSquare")]
assert len(pyramid) == 16
dimensions = {(row["width"], row["height"]) for row in pyramid}
assert len(dimensions) == 1
width, height = next(iter(dimensions))
constants = read("include/constants/battle_pyramid.h")
assert grid(width * number(constants, "PYRAMID_FLOOR_SQUARES_WIDE"),
            height * number(constants, "PYRAMID_FLOOR_SQUARES_HIGH")) <= capacity
assert "PYRAMID_FLOOR_SQUARES_WIDE" in read("src/battle_pyramid.c")
hill = read("include/constants/trainer_hill.h")
assert grid(number(hill, "HILL_FLOOR_WIDTH"), number(hill, "HILL_FLOOR_HEIGHT_MAIN") + number(hill, "HILL_FLOOR_HEIGHT_MARGIN")) <= capacity
words = int(re.search(r"IntrMain_Buffer\[(0x[0-9a-fA-F]+)\]", read("src/main.c"))[1], 16)
assert words * 4 == 0x200
assert "(IntrMain_End - IntrMain) <= 0x200" in read("ld_script_modern.ld")
print(f"RAM bounds: PASS ({maximum}/{capacity} map cells; {words * 4}-byte IRQ copy)")

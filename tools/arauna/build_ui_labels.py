#!/usr/bin/env python3
"""Render Arauna map labels without changing GBA tile layout or palette indices."""
import argparse
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--write", action="store_true")
args = parser.parse_args()
FONT = {
    "A": ("01110", "10001", "10001", "10001", "11111", "10001", "10001", "10001", "10001"),
    "R": ("11110", "10001", "10001", "10001", "11110", "10100", "10010", "10001", "10001"),
    "U": ("10001",) * 8 + ("01110",),
    "N": ("10001", "11001", "11001", "10101", "10101", "10101", "10011", "10011", "10001"),
    "M": ("10001", "11011", "10101", "10101") + ("10001",) * 5,
    "P": ("11110", "10001", "10001", "10001", "11110") + ("10000",) * 4,
}

def index_for(im, color):
    palette = im.getpalette()
    return min(range(1, 16), key=lambda i: sum((palette[3*i+j] - color[j])**2 for j in range(3)))

def text(im, label, x, y):
    points = []
    for ch in label:
        if ch == " ":
            x += 4
            continue
        for dy, row in enumerate(FONT[ch]):
            points.extend((x + dx, y + dy) for dx, bit in enumerate(row) if bit == "1")
        x += 6
    shadow, white = index_for(im, (82, 82, 74)), index_for(im, (255, 255, 255))
    for px, py in points:
        im.putpixel((px + 1, py + 1), shadow)
    for px, py in points:
        im.putpixel((px, py), white)

def option(im):
    assert im.mode == "P" and im.size == (32, 64)
    view = Image.new("P", (128, 16))
    view.putpalette(im.getpalette())
    for i in range(4):
        view.paste(im.crop((0, i*16, 32, i*16+16)), (i*32, 0))
    for y in range(2, 13):
        background = view.getpixel((126, y))
        for x in range(15, 125):
            view.putpixel((x, y), background)
    text(view, "ARAUNA MAP", 16, 2)
    result = im.copy()
    for i in range(4):
        result.paste(view.crop((i*32, 0, i*32+32, 16)), (0, i*16))
    return result

def header(im):
    assert im.mode == "P" and im.size == (64, 96)
    result = im.copy()
    background = index_for(im, (32, 197, 106))
    for y in range(6, 20):
        for x in range(2, 63):
            result.putpixel((x, y), background)
    text(result, "ARAUNA MAP", 3, 7)
    return result

for relative, render in (("graphics/pokenav/options/hoenn_map.png", option),
                         ("graphics/pokenav/left_headers/hoenn_map.png", header)):
    path = ROOT / relative
    with Image.open(path) as im:
        result = render(im)
        assert result.size == im.size and max(result.tobytes()) < 16
        if args.write:
            result.save(path, bits=4)
        else:
            assert result.tobytes() == im.tobytes(), f"Stale Arauna map label: {relative}"
print("Arauna UI labels: PASS (menu and map header)")

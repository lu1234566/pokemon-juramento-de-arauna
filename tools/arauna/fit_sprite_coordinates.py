#!/usr/bin/env python3
"""Fit engine sprite coordinates to the indexed native Arauna artwork."""
import argparse
import csv
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WRITE = argparse.ArgumentParser()
WRITE.add_argument("--write", action="store_true")
args = WRITE.parse_args()

def coords(path):
    with Image.open(path) as im:
        assert im.mode == "P" and im.size == (64, 64), path
        assert max(im.tobytes()) < 16, path
        bbox = im.point(lambda v: 255 if v else 0).getbbox()
        assert bbox is not None, path
        x0, y0, x1, y1 = bbox
        return ((x1 - x0 + 7) // 8 * 8, (y1 - y0 + 7) // 8 * 8, 64 - y1)

with (ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 386
pattern = re.compile(r"\[(SPECIES_\w+)\]\s*=\s*\{\s*\.size\s*=\s*MON_COORDS_SIZE\(\s*(\d+),\s*(\d+)\),\s*\.y_offset\s*=\s*(\d+)\s*\}")
changed = 0

def fit(path, wanted, regex=pattern):
    global changed
    text = path.read_text()
    seen = set()
    def replace(match):
        global changed
        species = match[1]
        if species not in wanted:
            return match[0]
        seen.add(species)
        w, h, offset = wanted[species]
        if tuple(map(int, match.group(2, 3, 4))) != (w, h, offset):
            changed += 1
        return f"[{species}] = {{ .size = MON_COORDS_SIZE({w}, {h}), .y_offset = {offset} }}"
    result = regex.sub(replace, text)
    assert set(wanted) <= seen, set(wanted) - seen
    if args.write:
        path.write_text(result)
    else:
        # Formatting is not part of the geometry contract.
        for match in regex.finditer(text):
            if match[1] in wanted:
                assert tuple(map(int, match.group(2, 3, 4))) == wanted[match[1]], (path, match[1])

for side in ("front", "back"):
    wanted = {}
    for row in rows:
        folder = ROOT / "graphics/pokemon" / row["graphics_folder"]
        if row["graphics_folder"] == "unown":
            folder /= "a"
        elif row["graphics_folder"] == "castform":
            folder /= "normal"
        wanted[row["species_constant"]] = coords(folder / f"{side}.png")
    variants = [(letter.upper(), letter) for letter in "bcdefghijklmnopqrstuvwxyz"]
    variants += [("EMARK", "exclamation_mark"), ("QMARK", "question_mark")]
    for name, folder in variants:
        wanted[f"SPECIES_UNOWN_{name}"] = coords(ROOT / f"graphics/pokemon/unown/{folder}/{side}.png")
    fit(ROOT / f"src/data/pokemon_graphics/{side}_pic_coordinates.h", wanted)

wanted = {f"CASTFORM_{name}": coords(ROOT / f"graphics/pokemon/castform/{folder}/front.png")
          for name, folder in (("NORMAL", "normal"), ("FIRE", "sunny"), ("WATER", "rainy"), ("ICE", "snowy"))}
cast_pattern = re.compile(pattern.pattern.replace("SPECIES_", "CASTFORM_"))
fit(ROOT / "src/battle_anim_mons.c", wanted, cast_pattern)
print(f"Sprite coordinates: PASS (386 species, {changed} geometry corrections)")

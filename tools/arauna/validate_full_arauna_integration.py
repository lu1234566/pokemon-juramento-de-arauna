#!/usr/bin/env python3
"""Static consistency checks for the complete 386-slot Arauna integration."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

from PIL import Image


def jasc_ok(path: Path) -> bool:
    lines = path.read_text(encoding="ascii").replace("\r", "").splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"] or len(lines) != 19:
        return False
    return all(len(line.split()) == 3 and all(0 <= int(v) <= 255 for v in line.split()) for line in lines[3:])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dex", type=Path, default=Path("arauna_dex_import/pokedex.json"))
    parser.add_argument("--packages", type=Path, default=Path("art_candidates/full_dex/gba"))
    parser.add_argument("--overlay", type=Path, default=Path("full_dex_build/repo_overlay"))
    args = parser.parse_args()

    entries = json.loads(args.dex.read_text(encoding="utf-8"))["pokemon"]
    assert len(entries) == 386 and [e["id"] for e in entries] == list(range(1, 387))
    folders = sorted(path for path in args.packages.iterdir() if path.is_dir())
    assert len(folders) == 386, f"expected 386 packages, got {len(folders)}"

    methods = Counter()
    for folder in folders:
        profile = json.loads((folder / "candidate_profile.json").read_text(encoding="utf-8"))
        methods[profile["productionMethod"]] += 1
        for filename, size in (("anim_front.png", (64, 128)), ("back.png", (64, 64)), ("icon.png", (32, 64))):
            with Image.open(folder / filename) as image:
                assert image.mode == "P" and image.size == size, (folder, filename, image.mode, image.size)
                assert image.info.get("transparency") == 0
                assert max(image.getdata()) <= 15
        assert jasc_ok(folder / "normal.pal") and jasc_ok(folder / "shiny.pal")
    assert methods["hand-prepared-approved"] == 9
    assert methods["reference-front-plus-reconstructed-back"] == 305
    assert methods["procedural-concept-front-and-back"] == 72

    mapping_path = args.overlay / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
    mapping = list(csv.DictReader(mapping_path.open(encoding="utf-8")))
    assert len(mapping) == 386
    assert len({row["species_constant"] for row in mapping}) == 386
    assert len({row["national_slot"] for row in mapping}) == 386
    assert all(len(row["engine_name"]) <= 12 for row in mapping)
    assert mapping[0]["species_constant"] == "SPECIES_TORCHIC"
    assert mapping[3]["species_constant"] == "SPECIES_MUDKIP"
    assert mapping[6]["species_constant"] == "SPECIES_TREECKO"

    header = (args.overlay / "src/data/pokemon/species_info/arauna_dex.h").read_text(encoding="utf-8")
    species_info = (args.overlay / "src/data/pokemon/species_info.h").read_text(encoding="utf-8")
    assert len(re.findall(r"^\s*\[SPECIES_[A-Z0-9_]+\]\s*=", header, re.MULTILINE)) == 386
    assert len(re.findall(r"\.natDexNum\s*=\s*NATIONAL_DEX_", header)) == 386
    expected_evolutions = sum(bool(entry.get("evolvesTo")) for entry in entries)
    assert len(re.findall(r"\.evolutions\s*=\s*EVOLUTION", header)) == expected_evolutions
    assert "—" not in header and "–" not in header
    assert '#include "species_info/arauna_dex.h"' in species_info
    assert '#include "species_info/gen_1_families.h"' not in species_info
    assert '#include "species_info/gen_2_families.h"' not in species_info
    assert '#include "species_info/gen_3_families.h"' not in species_info
    assert header.count("{") == header.count("}")

    graphics = [path for path in (args.overlay / "graphics/pokemon").rglob("*") if path.is_file()]
    assert len(graphics) == 3854, f"expected 3854 resolved engine graphics, got {len(graphics)}"
    for path in graphics:
        if path.suffix == ".png":
            with Image.open(path) as image:
                assert image.mode == "P"
                assert max(image.getdata()) <= 15
        elif path.suffix == ".pal":
            assert jasc_ok(path)

    print("OK Dex: 386 consecutive entries and 386 unique engine/National slots")
    print("OK art: 9 prepared + 305 references + 72 procedural concepts")
    print("OK assets: frontal, rear, icon, shiny palettes and two-frame animation")
    print(f"OK data: 386 species blocks and {expected_evolutions} level evolutions")
    print(f"OK overlay: {len(graphics)} resolved graphics files")


if __name__ == "__main__":
    main()

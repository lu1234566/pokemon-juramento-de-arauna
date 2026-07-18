#!/usr/bin/env python3
"""Inventory the 386 provisional Emerald-slot cries used by Arauna."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEX_SIZE = 386


def family_metadata(entries: list[dict]) -> tuple[dict[int, int], dict[int, int]]:
    parent = {}
    for entry in entries:
        for evolution in entry.get("evolvesTo") or []:
            parent[int(evolution["id"])] = int(entry["id"])
    roots = {}
    stages = {}
    for entry in entries:
        number = int(entry["id"])
        cursor = number
        stage = 0
        seen = set()
        while cursor in parent and cursor not in seen:
            seen.add(cursor)
            cursor = parent[cursor]
            stage += 1
        roots[number] = cursor
        stages[number] = stage
    return roots, stages


def csv_text(rows: list[dict[str, str]]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dex", type=Path, default=ROOT / "docs/arauna/source/pokedex.json")
    parser.add_argument("--profiles", type=Path, default=ROOT / "docs/arauna/ARAUNA_BATTLE_PROFILES.csv")
    parser.add_argument("--species-table", type=Path, default=ROOT / "src/data/pokemon/species_info/arauna_dex.h")
    parser.add_argument("--out", type=Path, default=ROOT / "docs/arauna/ARAUNA_CRY_AUDIT.csv")
    args = parser.parse_args()

    entries = json.loads(args.dex.read_text(encoding="utf-8"))["pokemon"]
    with args.profiles.open(encoding="utf-8", newline="") as source:
        profiles = {int(row["id"]): row for row in csv.DictReader(source)}
    species_text = args.species_table.read_text(encoding="utf-8")
    blocks = re.findall(
        r"^\s*\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)^\s*\},",
        species_text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if len(entries) != DEX_SIZE or len(profiles) != DEX_SIZE or len(blocks) != DEX_SIZE:
        raise ValueError("Dex, profiles and species table must cover IDs 001-386")
    roots, stages = family_metadata(entries)
    rows = []
    for entry, (slot, block) in zip(entries, blocks):
        number = int(entry["id"])
        match = re.search(r"^\s*\.cryId\s*=\s*(CRY_[A-Z0-9_]+),", block, flags=re.MULTILINE)
        if not match:
            raise ValueError(f"species #{number:03d} lacks a valid provisional cry")
        if profiles[number]["engine_species"] != f"SPECIES_{slot}":
            raise ValueError(f"profile/species mapping mismatch at #{number:03d}")
        rows.append({
            "id": f"{number:03d}",
            "name": entry["name"],
            "engine_species": f"SPECIES_{slot}",
            "cry_id": match.group(1),
            "family_root": f"{roots[number]:03d}",
            "family_stage": str(stages[number]),
            "status": "emerald-slot-placeholder",
            "planned_asset": f"sound/arauna/cries/{number:03d}.aif",
        })
    if len({row["cry_id"] for row in rows}) != DEX_SIZE:
        raise ValueError("provisional cry IDs must remain unique across the 386 slots")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(csv_text(rows), encoding="utf-8")
    print("audited 386 unique provisional cries; no sound assets were replaced")


if __name__ == "__main__":
    main()

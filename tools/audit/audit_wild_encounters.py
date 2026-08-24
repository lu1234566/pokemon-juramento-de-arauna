#!/usr/bin/env python3
"""Audit wild encounter tables for anything that breaks catching or crashes.

Checks each encounter field against the engine's expectations: the slot count
the encounter type requires, level ranges that are ordered and legal, species
that actually exist, and encounter rates that leave the table reachable.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]

# Slot counts the engine indexes into; a short table reads out of bounds.
SLOT_COUNTS = {
    "land_mons": 12,
    "water_mons": 5,
    "rock_smash_mons": 5,
    "fishing_mons": 10,
}
MAX_LEVEL = 100


def known_species() -> set[str]:
    text = (ROOT / "include" / "constants" / "species.h").read_text(encoding="utf-8")
    return set(re.findall(r"^#define\s+(SPECIES_[A-Z0-9_]+)", text, re.M))


def known_maps() -> set[str]:
    # map_groups.h declares maps as enum members, not #defines.
    text = (ROOT / "include" / "constants" / "map_groups.h").read_text(encoding="utf-8")
    return set(re.findall(r"\b(MAP_[A-Z0-9_]+)\s*=", text))


def main() -> int:
    data = json.loads((ROOT / "src" / "data" / "wild_encounters.json").read_text(encoding="utf-8"))
    species = known_species()
    maps = known_maps()
    problems: list[str] = []
    tables = 0

    for group in data["wild_encounter_groups"]:
        for entry in group["encounters"]:
            label = entry.get("base_label", "?")
            map_name = entry.get("map", "?")
            if group.get("for_maps", True) and map_name not in maps:
                problems.append(f"{label}: unknown map {map_name}")
            for field, count in SLOT_COUNTS.items():
                table = entry.get(field)
                if table is None:
                    continue
                tables += 1
                mons = table.get("mons", [])
                if len(mons) != count:
                    problems.append(
                        f"{map_name}/{field}: {len(mons)} slots, engine indexes {count}"
                    )
                rate = table.get("encounter_rate", 0)
                if not isinstance(rate, int) or rate <= 0:
                    problems.append(
                        f"{map_name}/{field}: encounter_rate {rate!r} makes the table unreachable"
                    )
                for i, mon in enumerate(mons):
                    lo, hi = mon.get("min_level"), mon.get("max_level")
                    name = mon.get("species", "?")
                    if name not in species:
                        problems.append(f"{map_name}/{field}[{i}]: unknown species {name}")
                    if not isinstance(lo, int) or not isinstance(hi, int):
                        problems.append(f"{map_name}/{field}[{i}]: non-integer level range")
                        continue
                    if lo > hi:
                        problems.append(
                            f"{map_name}/{field}[{i}] {name}: min_level {lo} > max_level {hi}"
                        )
                    if lo < 1 or hi > MAX_LEVEL:
                        problems.append(
                            f"{map_name}/{field}[{i}] {name}: level range {lo}-{hi} out of 1-{MAX_LEVEL}"
                        )

    for line in problems:
        print(f"  - {line}")
    print(f"\n{len(problems)} encounter problem(s) across {tables} tables.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

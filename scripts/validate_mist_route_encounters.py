#!/usr/bin/env python3
"""Validate the Mist Route encounter table and its early-game level curve."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SLOTS = [
    (2, 3, "SPECIES_WURMPLE"),
    (2, 3, "SPECIES_WURMPLE"),
    (3, 4, "SPECIES_SEEDOT"),
    (3, 4, "SPECIES_SEEDOT"),
    (3, 4, "SPECIES_TAILLOW"),
    (3, 4, "SPECIES_TAILLOW"),
    (3, 4, "SPECIES_MARILL"),
    (3, 4, "SPECIES_MARILL"),
    (4, 5, "SPECIES_AIPOM"),
    (4, 5, "SPECIES_AIPOM"),
    (4, 5, "SPECIES_RALTS"),
    (4, 5, "SPECIES_MURKROW"),
]

STARTER_TEXT = {
    "PIMPAU #007: GRASS.",
    "CARAMELO #001: FIRE.",
    "QUERÔ #004: WATER.",
}


def fail(message: str) -> None:
    raise ValueError(message)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    data = json.loads(read("src/data/wild_encounters.json"))
    group = next(
        item for item in data["wild_encounter_groups"]
        if item["label"] == "gWildMonHeaders"
    )
    matches = [
        item for item in group["encounters"]
        if item["map"] == "MAP_ARAUNA_MIST_ROUTE"
    ]
    if len(matches) != 1:
        fail("Mist Route must have exactly one wild-encounter entry")

    encounter = matches[0]
    if encounter.get("base_label") != "gAraunaMistRoute":
        fail("Mist Route must use base label gAraunaMistRoute")
    if set(encounter) != {"map", "base_label", "land_mons"}:
        fail("Mist Route must define land encounters only")

    land = encounter["land_mons"]
    if land.get("encounter_rate") != 20:
        fail("Mist Route encounter rate must be 20")

    actual_slots = [
        (item["min_level"], item["max_level"], item["species"])
        for item in land.get("mons", [])
    ]
    if actual_slots != EXPECTED_SLOTS:
        fail(f"Mist Route slots differ from the approved curve: {actual_slots}")
    if min(slot[0] for slot in actual_slots) != 2:
        fail("the early curve must begin at level 2")
    if max(slot[1] for slot in actual_slots) > 5:
        fail("wild encounters must not exceed the level-5 starter")

    mist_map = (ROOT / "data/layouts/AraunaMistRoute/map.bin").read_bytes()
    route101_map = (ROOT / "data/layouts/Route101/map.bin").read_bytes()
    if mist_map != route101_map:
        fail("Mist Route must retain the approved Route 101 map shell")

    pt = read("data/text/arauna/pt_br/opening.inc")
    en = read("data/text/arauna/en/opening.inc")
    for starter in STARTER_TEXT:
        if starter not in pt or starter not in en:
            fail(f"both languages must identify starter {starter!r}")

    print(
        "Validated Mist Route rate 20, twelve land slots at levels 2-5, "
        "seven official placeholder species, Route 101 shell, and the "
        "Arauna names/numbers of all three starters."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError, KeyError, StopIteration) as error:
        print(f"Mist Route encounter validation failed: {error}", file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""Validate the Mist Route encounter table and its early-game level curve."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# The Mist Route reuses the Route 101 shell as the tutorial route, so its
# encounters must stay on the approved early-game level curve. Specific species
# identities are intentionally not pinned here: the biome-driven Arauna roster is
# audited separately (tools/arauna/audit_arauna_encounters.py enforces the
# no-protected-species-in-wild invariant), and pinning exact slots here had
# drifted into demanding a protected species (#265 Preto-Velho / SPECIES_WURMPLE).
EXPECTED_LEVEL_CURVE = [
    (2, 3),
    (2, 3),
    (3, 4),
    (3, 4),
    (3, 4),
    (3, 4),
    (3, 4),
    (3, 4),
    (4, 5),
    (4, 5),
    (4, 5),
    (4, 5),
]

ENGLISH_STARTER_TEXT = {
    "PIMPAU No. 007: GRASS.",
    "CARAMELO No. 001: FIRE.",
    "QUERO No. 004: WATER.",
}


def trainer_block(source: str, trainer: str) -> str:
    marker = f"=== {trainer} ==="
    start = source.find(marker)
    if start < 0:
        fail(f"missing trainer {trainer}")
    end = source.find("\n=== TRAINER_", start + len(marker))
    return source[start:] if end < 0 else source[start:end]


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

    actual_curve = [
        (item["min_level"], item["max_level"])
        for item in land.get("mons", [])
    ]
    if actual_curve != EXPECTED_LEVEL_CURVE:
        fail(f"Mist Route level curve differs from the approved early curve: {actual_curve}")
    if min(level[0] for level in actual_curve) != 2:
        fail("the early curve must begin at level 2")
    if max(level[1] for level in actual_curve) > 5:
        fail("wild encounters must not exceed the level-5 starter")

    mist_map = (ROOT / "data/layouts/AraunaMistRoute/map.bin").read_bytes()
    route101_map = (ROOT / "data/layouts/Route101/map.bin").read_bytes()
    if mist_map != route101_map:
        fail("Mist Route must retain the approved Route 101 map shell")

    english = read("data/text/arauna/en/opening.inc")
    for starter in ENGLISH_STARTER_TEXT:
        if starter not in english:
            fail(f"English runtime must identify starter {starter!r}")

    trainers = read("src/data/trainers.party")
    agent = trainer_block(trainers, "TRAINER_ARAUNA_TECH_AGENT")
    for token in (
        "Voltorb",
        "- Tackle",
        "- Charge",
        "- Eerie Impulse",
    ):
        if token not in agent:
            fail(f"technical-agent party is missing {token!r}")
    if "- Thunder Shock" in agent or "- MOVE_THUNDER_SHOCK" in agent:
        fail("the first miniboss must not single out the Water starter")

    print(
        "Validated Mist Route rate 20, twelve land slots on the approved "
        "level 2-5 early curve, the Route 101 shell, English starter "
        "names/numbers, and a type-neutral first miniboss."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError, KeyError, StopIteration) as error:
        print(f"Mist Route encounter validation failed: {error}", file=sys.stderr)
        sys.exit(1)

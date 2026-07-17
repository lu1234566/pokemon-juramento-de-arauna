#!/usr/bin/env python3
"""Validate the canonical 386-slot Arauna Pokédex registry."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


EXPECTED_COLUMNS = [
    "slot",
    "family_id",
    "stage",
    "codename",
    "primary_biome",
    "type_1",
    "type_2",
    "battle_role",
    "obtain_phase",
    "batch",
    "concept_status",
    "sprite_status",
    "integration_status",
    "notes",
]

FINAL_STARTER_TYPES = {
    "003": ("Grass", "Rock"),
    "006": ("Fire", "Dragon"),
    "009": ("Water", "Bug"),
}


def fail(message: str) -> None:
    raise SystemExit(f"Pokédex registry validation failed: {message}")


def main() -> None:
    registry = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).with_name("pokedex_registry.csv")
    )

    with registry.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_COLUMNS:
            fail(f"unexpected columns: {reader.fieldnames!r}")
        rows = list(reader)

    if len(rows) != 386:
        fail(f"expected 386 slots, found {len(rows)}")

    expected_slots = [f"{slot:03d}" for slot in range(1, 387)]
    actual_slots = [row["slot"] for row in rows]
    if actual_slots != expected_slots:
        fail("slots must be unique, ordered, and cover 001 through 386")

    indexed = {row["slot"]: row for row in rows}

    for slot in expected_slots[:18]:
        row = indexed[slot]
        if row["codename"] == "RESERVED" or row["concept_status"] == "reserved":
            fail(f"initial ecosystem slot {slot} cannot be reserved")

    for slot in expected_slots[18:]:
        row = indexed[slot]
        if row["codename"] != "RESERVED" or row["concept_status"] != "reserved":
            fail(f"future slot {slot} must remain explicitly reserved")

    for slot, expected_types in FINAL_STARTER_TYPES.items():
        row = indexed[slot]
        actual_types = (row["type_1"], row["type_2"])
        if actual_types != expected_types:
            fail(
                f"starter final form {slot} must be "
                f"{expected_types[0]}/{expected_types[1]}, found {actual_types}"
            )

    if indexed["004"]["sprite_status"] != "silhouette-b-approved":
        fail("slot 004 must preserve approval of Caramelo silhouette B")

    integrated = [row["slot"] for row in rows if row["integration_status"] == "integrated"]
    if integrated:
        fail(f"sprites/data cannot be marked integrated before approval: {integrated}")

    print(
        "Pokédex registry valid: 386 ordered slots, 18 planned entries, "
        "368 reserved entries, and no unapproved integrations."
    )


if __name__ == "__main__":
    main()

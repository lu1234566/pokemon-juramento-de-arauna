#!/usr/bin/env python3
"""Validate the Arauna registry and its save-stable Emerald placeholders."""

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

VISIBLE_ENTRIES = {
    "001": ("Caramelo", "Fire", ""),
    "002": ("Caramelão", "Fire", ""),
    "003": ("Dragauará", "Fire", "Dragon"),
    "004": ("Querô", "Water", ""),
    "005": ("Queribela", "Water", "Bug"),
    "006": ("Terólibra", "Water", "Bug"),
    "007": ("Pimpau", "Grass", ""),
    "008": ("Bicopau", "Grass", ""),
    "009": ("Petronico", "Grass", "Rock"),
    "010": ("Formilim", "Bug", ""),
    "011": ("Saúvarco", "Bug", "Ground"),
    "012": ("Capivim", "Water", "Normal"),
    "013": ("Tucanhão", "Flying", "Grass"),
    "014": ("Sagüim", "Normal", ""),
    "015": ("Micuías", "Normal", "Psychic"),
    "016": ("Boitatá", "Fire", "Ghost"),
    "017": ("Curupim", "Grass", "Fairy"),
    "018": ("Curupira", "Grass", "Fairy"),
    "019": ("Iaraço", "Water", "Fairy"),
    "020": ("Sacizinho", "Dark", "Flying"),
}

STARTER_PLACEHOLDERS = {
    "001": ("Caramelo", "SPECIES_TORCHIC", "255"),
    "002": ("Caramelão", "SPECIES_COMBUSKEN", "256"),
    "003": ("Dragauará", "SPECIES_BLAZIKEN", "257"),
    "004": ("Querô", "SPECIES_MUDKIP", "258"),
    "005": ("Queribela", "SPECIES_MARSHTOMP", "259"),
    "006": ("Terólibra", "SPECIES_SWAMPERT", "260"),
    "007": ("Pimpau", "SPECIES_TREECKO", "252"),
    "008": ("Bicopau", "SPECIES_GROVYLE", "253"),
    "009": ("Petronico", "SPECIES_SCEPTILE", "254"),
}


def fail(message: str) -> None:
    raise SystemExit(f"Pokédex registry validation failed: {message}")


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def main() -> None:
    registry = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("project/design/pokedex/pokedex_registry.csv")
    )
    mapping = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else Path("project/design/pokedex/placeholder_species.csv")
    )

    columns, rows = load_csv(registry)
    if columns != EXPECTED_COLUMNS:
        fail(f"unexpected registry columns: {columns!r}")
    if len(rows) != 386:
        fail(f"expected 386 slots, found {len(rows)}")

    expected_slots = [f"{slot:03d}" for slot in range(1, 387)]
    if [row["slot"] for row in rows] != expected_slots:
        fail("slots must be unique, ordered, and cover 001 through 386")
    indexed = {row["slot"]: row for row in rows}

    for slot, (name, type_1, type_2) in VISIBLE_ENTRIES.items():
        row = indexed[slot]
        actual = (row["codename"], row["type_1"], row["type_2"])
        if actual != (name, type_1, type_2):
            fail(f"visible slot {slot} must be {(name, type_1, type_2)}, got {actual}")
        if row["integration_status"] == "integrated":
            fail(f"visible slot {slot} cannot be integrated from preview art")

    for slot in expected_slots[20:]:
        row = indexed[slot]
        if row["codename"] != "RESERVED" or row["concept_status"] != "reserved":
            fail(f"slot {slot} must stay reserved until structured import")

    map_columns, mapped = load_csv(mapping)
    expected_map_columns = [
        "arauna_slot",
        "arauna_name",
        "placeholder_species",
        "placeholder_national_dex",
        "usage_status",
        "replacement_status",
        "notes",
    ]
    if map_columns != expected_map_columns:
        fail(f"unexpected placeholder columns: {map_columns!r}")
    if len(mapped) != 9:
        fail(f"starter placeholder map must contain 9 rows, found {len(mapped)}")

    slots = [row["arauna_slot"] for row in mapped]
    species = [row["placeholder_species"] for row in mapped]
    national = [row["placeholder_national_dex"] for row in mapped]
    if len(set(slots)) != len(slots) or len(set(species)) != len(species):
        fail("placeholder slots and species must be one-to-one")
    if len(set(national)) != len(national):
        fail("placeholder national numbers must be unique")

    for row in mapped:
        slot = row["arauna_slot"]
        expected = STARTER_PLACEHOLDERS.get(slot)
        actual = (
            row["arauna_name"],
            row["placeholder_species"],
            row["placeholder_national_dex"],
        )
        if expected is None or actual != expected:
            fail(f"invalid starter placeholder mapping for slot {slot}: {actual}")
        if indexed[slot]["codename"] != row["arauna_name"]:
            fail(f"placeholder name for slot {slot} differs from registry")

    integrated = [row["slot"] for row in rows if row["integration_status"] == "integrated"]
    if integrated:
        fail(f"data cannot be marked integrated before approval: {integrated}")

    print(
        "Pokédex registry valid: 386 slots, 20 entries mirrored from the "
        "external preview, 9 unique Emerald starter placeholders, 366 reserved "
        "slots, and no unapproved integrations."
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the canonical Arauna prologue and its real new-game entrypoint."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_VARS = {
    "VAR_ARAUNA_STORY_STAGE": "0x40F7",
    "VAR_ARAUNA_STARTER_CHOICE": "0x40F8",
    "VAR_ARAUNA_BOND_CHOICE": "0x40F9",
    "VAR_ARAUNA_OPTIONAL_MISSION": "0x40FA",
}

EXPECTED_FLAGS = {
    "FLAG_ARAUNA_PROLOGUE_FED_PIMPAU": "0x37",
    "FLAG_ARAUNA_PROLOGUE_FED_CARAMELO": "0x38",
    "FLAG_ARAUNA_PROLOGUE_FED_QUERO": "0x39",
    "FLAG_ARAUNA_CIRO_STARTER_PIMPAU": "0x3A",
    "FLAG_ARAUNA_CIRO_STARTER_CARAMELO": "0x3B",
    "FLAG_ARAUNA_CIRO_STARTER_QUERO": "0x3C",
    "FLAG_ARAUNA_ANAHI_STARTER_PIMPAU": "0x3D",
    "FLAG_ARAUNA_ANAHI_STARTER_CARAMELO": "0x3E",
    "FLAG_ARAUNA_ANAHI_STARTER_QUERO": "0x3F",
}

TEXT_LABEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):{1,2}$", re.MULTILINE)


def fail(message: str) -> None:
    raise ValueError(message)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(source: str, tokens: list[str], name: str) -> None:
    missing = [token for token in tokens if token not in source]
    if missing:
        fail(f"{name} is missing required tokens: {missing}")


def main() -> int:
    vars_h = read("include/constants/vars.h")
    for name, value in EXPECTED_VARS.items():
        if not re.search(rf"^#define\s+{name}\s+{value}\b", vars_h, re.MULTILINE):
            fail(f"{name} must be allocated at {value}")

    flags_h = read("include/constants/flags.h")
    for name, value in EXPECTED_FLAGS.items():
        if not re.search(rf"^#define\s+{name}\s+{value}\b", flags_h, re.MULTILINE):
            fail(f"{name} must be allocated at {value}")

    new_game = read("src/new_game.c")
    require(
        new_game,
        [
            "static void WarpToAraunaOpening(void)",
            "MAP_GROUP(MAP_ARAUNA_PLAYER_HOUSE)",
            "MAP_NUM(MAP_ARAUNA_PLAYER_HOUSE)",
            "WarpToAraunaOpening();",
        ],
        "new-game entrypoint",
    )
    if "WarpToTruck();" in new_game or "MAP_INSIDE_OF_TRUCK" in new_game:
        fail("Emerald new games must not enter the vanilla moving truck")

    house_map = json.loads(read("data/maps/AraunaPlayerHouse/map.json"))
    graphics = [event["graphics_id"] for event in house_map["object_events"]]
    expected_graphics = [
        "OBJ_EVENT_GFX_MOM",
        "OBJ_EVENT_GFX_SCIENTIST_1",
        "OBJ_EVENT_GFX_ITEM_BALL",
        "OBJ_EVENT_GFX_ITEM_BALL",
        "OBJ_EVENT_GFX_ITEM_BALL",
    ]
    if graphics != expected_graphics:
        fail(f"AraunaPlayerHouse object graphics differ: {graphics}")
    if len(house_map["coord_events"]) != 2:
        fail("both house exits must be gated before the starter choice")

    house = read("data/maps/AraunaPlayerHouse/scripts.inc")
    require(
        house,
        [
            "map_script_2 VAR_ARAUNA_STORY_STAGE, 0",
            "setvar VAR_ARAUNA_STORY_STAGE, 1",
            "FLAG_ARAUNA_PROLOGUE_FED_PIMPAU",
            "FLAG_ARAUNA_PROLOGUE_FED_CARAMELO",
            "FLAG_ARAUNA_PROLOGUE_FED_QUERO",
            "givemon SPECIES_TREECKO, 5, ITEM_NONE",
            "givemon SPECIES_TORCHIC, 5, ITEM_NONE",
            "givemon SPECIES_MUDKIP, 5, ITEM_NONE",
            "setflag FLAG_SYS_POKEMON_GET",
            "setflag FLAG_SYS_POKEDEX_GET",
            "special SetUnlockedPokedexFlags",
            "setvar VAR_ARAUNA_STORY_STAGE, 2",
            "call AraunaResearchCenter_EventScript_GiveSecondTestCandies",
            "FLAG_ARAUNA_CIRO_STARTER_CARAMELO",
            "FLAG_ARAUNA_CIRO_STARTER_QUERO",
            "FLAG_ARAUNA_CIRO_STARTER_PIMPAU",
            "FLAG_ARAUNA_ANAHI_STARTER_CARAMELO",
            "FLAG_ARAUNA_ANAHI_STARTER_QUERO",
            "FLAG_ARAUNA_ANAHI_STARTER_PIMPAU",
        ],
        "care-first home selection",
    )

    center = read("data/maps/AraunaResearchCenter/scripts.inc")
    if "givemon " in center:
        fail("the research center must not bypass the care-first home choice")
    require(
        center,
        [
            "AraunaResearchCenter_EventScript_SelectionMovedHome",
            "AraunaResearchCenter_EventScript_GiveSecondTestCandies",
        ],
        "research-center fallback",
    )

    village_map = json.loads(read("data/maps/AraunaMapLab/map.json"))
    if village_map["layout"] != "LAYOUT_ARAUNA_MAP_LAB" or not village_map["show_map_name"]:
        fail("the reused Vila Amanhecer exterior must display its map name")

    map_sections = json.loads(read("src/data/region_map/region_map_sections.json"))
    names = {section["id"]: section["name"] for section in map_sections["map_sections"]}
    if names.get("MAPSEC_LITTLEROOT_TOWN") != "VILA AMANHECER":
        fail("the reused Littleroot map section must be VILA AMANHECER")
    if names.get("MAPSEC_OLDALE_TOWN") != "AMANHECER POST":
        fail("the reused Oldale map section must be AMANHECER POST")

    identity_files = [
        "data/maps/LittlerootTown/scripts.inc",
        "data/maps/OldaleTown/scripts.inc",
        "data/maps/Route101/scripts.inc",
        "data/maps/Route102/scripts.inc",
        "data/maps/Route103/scripts.inc",
    ]
    identity_text = "\n".join(read(path) for path in identity_files)
    for stale in ("LITTLEROOT TOWN", "OLDALE TOWN"):
        if stale in identity_text:
            fail(f"vanilla settlement identity remains visible: {stale}")

    pt = read("data/text/arauna/pt_br/opening.inc")
    en = read("data/text/arauna/en/opening.inc")
    if TEXT_LABEL.findall(pt) != TEXT_LABEL.findall(en):
        fail("Portuguese and English opening labels must match and stay ordered")
    require(
        en,
        [
            "VILA AMANHECER",
            "DONA ZILA",
            "PROF. ANAHI",
            "Feed all three before choosing",
            "CENSUS OF LEGENDS",
        ],
        "English canonical prologue",
    )
    if "386 espécies nativas" not in pt or "386 native species" not in en:
        fail("both languages must describe the integrated 386-species Arauna Dex")
    if "dados e arte estão ligados" not in pt or "data and artwork are linked" not in en:
        fail("both languages must link the chosen partner to its Arauna Dex entry")

    charmap = read("charmap.txt")
    for character in ("ã", "õ"):
        if f"'{character}'" not in charmap:
            fail(f"charmap.txt must define a temporary fallback for {character!r}")

    event_scripts = read("data/event_scripts.s")
    if '#include "data/text/arauna/opening.inc"' not in event_scripts:
        fail("data/event_scripts.s must include the localized opening wrapper")

    print(
        "Validated the real Arauna new-game entrypoint, Vila Amanhecer identity, "
        "care-first starter choice, independent Ciro/Anahi assignments and "
        "one-time test-supply hook."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Arauna opening validation failed: {error}", file=sys.stderr)
        sys.exit(1)

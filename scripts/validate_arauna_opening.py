#!/usr/bin/env python3
"""Validate the canonical English-first Arauna prologue and entrypoint."""

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
    "FLAG_ARAUNA_PROLOGUE_NIGHT_PIMPAU": "0x40",
    "FLAG_ARAUNA_PROLOGUE_NIGHT_CARAMELO": "0x41",
    "FLAG_ARAUNA_PROLOGUE_NIGHT_QUERO": "0x42",
    "FLAG_ARAUNA_PROLOGUE_TALKED_ZILA_AT_NIGHT": "0x43",
    "FLAG_ARAUNA_PROLOGUE_TALKED_ANAHI_AT_NIGHT": "0x44",
    "FLAG_ARAUNA_PROLOGUE_NIGHT_COMPLETE": "0x45",
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(source: str, tokens: tuple[str, ...], name: str) -> None:
    missing = [token for token in tokens if token not in source]
    if missing:
        raise ValueError(f"{name} is missing required tokens: {missing}")


def main() -> int:
    vars_h = read("include/constants/vars.h")
    flags_h = read("include/constants/flags.h")
    for name, value in EXPECTED_VARS.items():
        if not re.search(rf"^#define\s+{name}\s+{value}\b", vars_h, re.MULTILINE):
            raise ValueError(f"{name} must remain allocated at {value}")
    for name, value in EXPECTED_FLAGS.items():
        if not re.search(rf"^#define\s+{name}\s+{value}\b", flags_h, re.MULTILINE):
            raise ValueError(f"{name} must remain allocated at {value}")

    new_game = read("src/new_game.c")
    require(new_game, (
        "static void WarpToAraunaOpening(void)",
        "MAP_GROUP(MAP_ARAUNA_PLAYER_HOUSE)",
        "MAP_NUM(MAP_ARAUNA_PLAYER_HOUSE)",
        "WarpToAraunaOpening();",
    ), "new-game entrypoint")
    if "WarpToTruck();" in new_game or "MAP_INSIDE_OF_TRUCK" in new_game:
        raise ValueError("new games must not enter Emerald's moving truck")

    overworld = read("src/overworld.c")
    callback = re.search(r"void CB2_NewGame\(void\)\s*\{(?P<body>.*?)\n\}", overworld, re.DOTALL)
    if callback is None or "gFieldCallback = FieldCB_WarpExitFadeFromBlack;" not in callback.group("body"):
        raise ValueError("Arauna new games must fade into Dona Zila's house")
    if "ExecuteTruckSequence" in callback.group("body"):
        raise ValueError("Arauna new games must not execute the truck sequence")

    house_map = json.loads(read("data/maps/AraunaPlayerHouse/map.json"))
    expected_graphics = [
        "OBJ_EVENT_GFX_ARAUNA_DONA_ZILA",
        "OBJ_EVENT_GFX_ARAUNA_PROFESSORA_ANAHI",
        "OBJ_EVENT_GFX_ITEM_BALL",
        "OBJ_EVENT_GFX_ITEM_BALL",
        "OBJ_EVENT_GFX_ITEM_BALL",
    ]
    graphics = [event["graphics_id"] for event in house_map["object_events"]]
    if graphics != expected_graphics:
        raise ValueError(f"AraunaPlayerHouse object graphics differ: {graphics}")
    if len(house_map["coord_events"]) != 2:
        raise ValueError("both house exits must remain gated before partner choice")

    house = read("data/maps/AraunaPlayerHouse/scripts.inc")
    require(house, (
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
        "giveitem ITEM_FAME_CHECKER",
        "setvar VAR_ARAUNA_STORY_STAGE, 2",
        "AraunaPlayerHouse_EventScript_CheckNightReady",
        "AraunaPlayerHouse_EventScript_BeginDawn",
        "fadescreen FADE_TO_BLACK",
        "fadescreen FADE_FROM_BLACK",
    ), "care-first playable home selection")

    opening_block = house.split("AraunaPlayerHouse_EventScript_Opening::", 1)[1].split(
        "AraunaPlayerHouse_EventScript_DonaZila::", 1
    )[0]
    if "AraunaPlayerHouse_Text_NightWatch" in opening_block or "AraunaPlayerHouse_Text_Dawn" in opening_block:
        raise ValueError("the playable night must not be compressed into the opening dump")

    center = read("data/maps/AraunaResearchCenter/scripts.inc")
    if "givemon " in center:
        raise ValueError("the research center must not bypass the home choice")

    village_map = json.loads(read("data/maps/AraunaMapLab/map.json"))
    if village_map["layout"] != "LAYOUT_ARAUNA_MAP_LAB" or not village_map["show_map_name"]:
        raise ValueError("Vila Amanhecer must retain its reused layout and name popup")
    east_triggers = {
        (event["x"], event["y"])
        for event in village_map["coord_events"]
        if event["script"] == "AraunaMapLab_EventScript_EnterMistRoute"
    }
    # Three rows of gate, three rows of trigger. Covering only the middle one
    # let the player leave along y=10 or y=12 with nothing firing.
    if east_triggers != {(x, y) for x in (18, 19) for y in (10, 11, 12)}:
        raise ValueError(f"visible east exit is misaligned: {east_triggers}")

    sections = json.loads(read("src/data/region_map/region_map_sections.json"))
    names = {section["id"]: section.get("name") for section in sections["map_sections"]}
    if names.get("MAPSEC_LITTLEROOT_TOWN") != "VILA AMANHECER":
        raise ValueError("Littleroot's reused map section must read VILA AMANHECER")

    en = read("data/text/arauna/en/opening.inc")
    require(en, (
        "VILA AMANHECER",
        "DONA ZILA",
        "PROF. ANAHI",
        "Feed all three before choosing",
        "CENSUS OF LEGENDS",
        "ZILA'S NOTEBOOK",
        "Follow the east path and cross",
    ), "English canonical prologue")

    event_scripts = read("data/event_scripts.s")
    if '#include "data/text/arauna/opening.inc"' not in event_scripts:
        raise ValueError("localized opening wrapper is not included")

    print("Arauna opening validated: English-first prologue, visible east exit and usable notebook reward.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Arauna opening validation failed: {error}", file=sys.stderr)
        sys.exit(1)

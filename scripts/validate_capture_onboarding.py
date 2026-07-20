#!/usr/bin/env python3
"""Validate Arauna's English-first Dex activation and one-time field kit."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise ValueError(message)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(source: str, tokens: tuple[str, ...], name: str) -> None:
    missing = [token for token in tokens if token not in source]
    if missing:
        fail(f"{name} is missing required tokens: {missing}")


def script_block(source: str, label: str, next_label: str) -> str:
    start = source.find(label + "::")
    if start < 0:
        fail(f"missing script label {label}")
    end = source.find(next_label + "::", start)
    if end < 0:
        fail(f"missing following script label {next_label}")
    return source[start:end]


def main() -> int:
    house = read("data/maps/AraunaPlayerHouse/scripts.inc")

    zila_recovery = script_block(
        house,
        "AraunaPlayerHouse_EventScript_ZilaAfterChoice",
        "AraunaPlayerHouse_EventScript_ZilaNotebookBagFull",
    )
    require(
        zila_recovery,
        (
            "checkitem ITEM_FAME_CHECKER, 1",
            "giveitem ITEM_FAME_CHECKER",
            "AraunaPlayerHouse_EventScript_ZilaNotebookBagFull",
            "AraunaPlayerHouse_Text_NotebookReceived",
        ),
        "Dona Zila notebook recovery",
    )
    if zila_recovery.index("checkitem ITEM_FAME_CHECKER, 1") > zila_recovery.index("giveitem ITEM_FAME_CHECKER"):
        fail("Dona Zila must check ownership before retrying the notebook reward")

    choice = script_block(
        house,
        "AraunaPlayerHouse_EventScript_CompleteChoice",
        "AraunaPlayerHouse_EventScript_NotebookBagFull",
    )
    require(
        choice,
        (
            "setflag FLAG_SYS_POKEMON_GET",
            "setflag FLAG_SYS_POKEDEX_GET",
            "special SetUnlockedPokedexFlags",
            "special EnableNationalPokedex",
            "giveitem ITEM_FAME_CHECKER",
            "AraunaResearchCenter_Text_DexActivated",
        ),
        "care-first partner completion",
    )
    if not (
        choice.index("setflag FLAG_SYS_POKEDEX_GET")
        < choice.index("special EnableNationalPokedex")
        < choice.index("AraunaResearchCenter_Text_DexActivated")
    ):
        fail("the full Arauna Dex must unlock before its confirmation message")

    bag_full = script_block(
        house,
        "AraunaPlayerHouse_EventScript_NotebookBagFull",
        "AraunaPlayerHouse_EventScript_AssignRemainingStarters",
    )
    require(
        bag_full,
        ("AraunaPlayerHouse_Text_NotebookBagFull", "AraunaResearchCenter_Text_DexActivated"),
        "notebook bag-full fallback",
    )

    village = read("data/maps/AraunaMapLab/scripts.inc")
    kit = script_block(
        village,
        "AraunaMapLab_EventScript_FieldKit",
        "AraunaMapLab_EventScript_FieldKitLocked",
    )
    require(
        kit,
        (
            "goto_if_lt VAR_ARAUNA_STORY_STAGE, 2",
            "checkitemspace ITEM_POKE_BALL, 5",
            "checkitemspace ITEM_POTION, 3",
            "giveitem ITEM_POKE_BALL, 5",
            "giveitem ITEM_POTION, 3",
            "setflag FLAG_ARAUNA_MAP_LAB_FIELD_KIT_TAKEN",
            "removeobject VAR_LAST_TALKED",
        ),
        "field kit",
    )
    for check in ("checkitemspace ITEM_POKE_BALL, 5", "checkitemspace ITEM_POTION, 3"):
        if kit.index(check) > kit.index("giveitem ITEM_POKE_BALL, 5"):
            fail("both bag-space checks must run before either item is given")

    map_data = json.loads(read("data/maps/AraunaMapLab/map.json"))
    kits = [
        event for event in map_data["object_events"]
        if event["script"] == "AraunaMapLab_EventScript_FieldKit"
    ]
    if len(kits) != 1:
        fail("the village must contain exactly one field-kit object")
    event = kits[0]
    if event["graphics_id"] != "OBJ_EVENT_GFX_ITEM_BALL":
        fail("the field kit must keep the approved official item-ball graphic")
    if event["trainer_sight_or_berry_tree_id"] != "ITEM_POKE_BALL":
        fail("field-kit metadata must identify its primary capture item")
    if event["flag"] != "FLAG_ARAUNA_MAP_LAB_FIELD_KIT_TAKEN":
        fail("the field kit must use its persistent one-time flag")

    flags = read("include/constants/flags.h")
    if "FLAG_ARAUNA_MAP_LAB_FIELD_KIT_TAKEN" not in flags:
        fail("the persistent field-kit flag is missing")

    english_opening = read("data/text/arauna/en/opening.inc")
    require(
        english_opening,
        (
            "The ARAUNA DEX",
            "All 386 native species can now",
            "Observe their habitats",
            "ZILA'S NOTEBOOK",
        ),
        "English-first Dex disclosure",
    )

    english_map = read("data/text/arauna/en/map_lab.inc")
    require(
        english_map,
        (
            "5 POKé BALLS and 3 POTIONS",
            "The FIELD KIT is sealed.",
            "Choose your partner at DONA",
            "ZILA's house first.",
        ),
        "English field-kit text",
    )

    print(
        "Validated care-first full-Dex activation, recoverable Zila notebook, "
        "one-time starter-gated field kit, 5 Poke Balls, 3 Potions, persistent "
        "object removal, and English-first runtime disclosure."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as error:
        print(f"Capture-onboarding validation failed: {error}", file=sys.stderr)
        sys.exit(1)

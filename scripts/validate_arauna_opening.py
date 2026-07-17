#!/usr/bin/env python3
"""Validate the non-art opening flow for the Arauna vertical slice."""

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

EXPECTED_OBJECTS = {
    "AraunaPlayerHouse": ["OBJ_EVENT_GFX_MOM"],
    "AraunaResearchCenter": [
        "OBJ_EVENT_GFX_SCIENTIST_1",
        "OBJ_EVENT_GFX_ITEM_BALL",
        "OBJ_EVENT_GFX_ITEM_BALL",
        "OBJ_EVENT_GFX_ITEM_BALL",
    ],
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

    for map_name, expected_graphics in EXPECTED_OBJECTS.items():
        data = json.loads(read(f"data/maps/{map_name}/map.json"))
        actual_graphics = [event["graphics_id"] for event in data["object_events"]]
        if actual_graphics != expected_graphics:
            fail(f"{map_name} object graphics differ: {actual_graphics}")

    house = read("data/maps/AraunaPlayerHouse/scripts.inc")
    require(
        house,
        [
            "map_script_2 VAR_ARAUNA_STORY_STAGE, 0",
            "setvar VAR_ARAUNA_STORY_STAGE, 1",
            "AraunaPlayerHouse_EventScript_Responsible",
        ],
        "player-house opening",
    )

    center = read("data/maps/AraunaResearchCenter/scripts.inc")
    require(
        center,
        [
            "givemon SPECIES_TREECKO, 5, ITEM_NONE",
            "givemon SPECIES_TORCHIC, 5, ITEM_NONE",
            "givemon SPECIES_MUDKIP, 5, ITEM_NONE",
            "setvar VAR_ARAUNA_STARTER_CHOICE, 1",
            "setvar VAR_ARAUNA_STARTER_CHOICE, 2",
            "setvar VAR_ARAUNA_STARTER_CHOICE, 3",
            "setvar VAR_ARAUNA_STORY_STAGE, 2",
            "AraunaResearchCenter_Text_PlaceholderNotice",
        ],
        "research-center selection",
    )

    village = read("data/maps/AraunaMapLab/scripts.inc")
    require(
        village,
        [
            "goto_if_lt VAR_ARAUNA_STORY_STAGE, 2",
            "setvar VAR_ARAUNA_STORY_STAGE, 3",
            "goto_if_ge VAR_ARAUNA_STORY_STAGE, 3",
            "AraunaMapLab_Text_RouteLocked",
        ],
        "village progression gate",
    )

    route = read("data/maps/AraunaMistRoute/scripts.inc")
    require(
        route,
        [
            "goto_if_eq VAR_ARAUNA_STORY_STAGE, 3",
            "setvar VAR_ARAUNA_STORY_STAGE, 4",
        ],
        "route stage transition",
    )

    pt = read("data/text/arauna/pt_br/opening.inc")
    en = read("data/text/arauna/en/opening.inc")
    pt_labels = TEXT_LABEL.findall(pt)
    en_labels = TEXT_LABEL.findall(en)
    if pt_labels != en_labels:
        fail("Portuguese and English opening labels must match and stay ordered")
    if "placeholder técnico" not in pt or "technical placeholder" not in en:
        fail("both languages must disclose that starter species are placeholders")
    if "Nenhum sprite de ARAUNA" not in pt or "No ARAUNA sprite" not in en:
        fail("both languages must preserve the sprite-approval safeguard")

    charmap = read("charmap.txt")
    for character in ("ã", "õ"):
        if f"'{character}'" not in charmap:
            fail(f"charmap.txt must define a temporary fallback for {character!r}")

    event_scripts = read("data/event_scripts.s")
    if '\t.include "data/text/arauna/opening.inc"' not in event_scripts:
        fail("data/event_scripts.s must include the localized opening bank")

    print(
        "Validated Arauna opening stages 0–4, one-time starter choice, "
        "route gate, bilingual text, vanilla-only NPC graphics, and explicit "
        "placeholder disclosure with Portuguese tilde fallbacks."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Arauna opening validation failed: {error}", file=sys.stderr)
        sys.exit(1)

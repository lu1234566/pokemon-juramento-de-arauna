#!/usr/bin/env python3
"""Validate the Mist Route story gate and optional notebook mission."""

from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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
    flags = read("include/constants/flags.h")
    require(
        flags,
        [
            "FLAG_ARAUNA_MIST_ROUTE_AFFECTED_MON_CLEARED  0x23",
            "FLAG_ARAUNA_MIST_ROUTE_NOTEBOOK_TAKEN        0x24",
        ],
        "Arauna route flags",
    )

    map_data = json.loads(read("data/maps/AraunaMistRoute/map.json"))
    objects = map_data["object_events"]
    expected_graphics = [
        "OBJ_EVENT_GFX_EXPERT_M",
        "OBJ_EVENT_GFX_ITEM_BALL",
        "OBJ_EVENT_GFX_POOCHYENA",
    ]
    if [event["graphics_id"] for event in objects] != expected_graphics:
        fail("Mist Route must use only the three approved vanilla object graphics")

    layout_data = json.loads(read("data/layouts/layouts.json"))
    layout = next(
        item for item in layout_data["layouts"]
        if item["id"] == "LAYOUT_ARAUNA_MIST_ROUTE"
    )
    width = int(layout["width"])
    height = int(layout["height"])
    raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
    entries = struct.unpack(f"<{width * height}H", raw)
    for event in objects:
        x, y = int(event["x"]), int(event["y"])
        if not (0 <= x < width and 0 <= y < height):
            fail(f"route object {(x, y)} is outside the layout")
        if ((entries[y * width + x] >> 10) & 0x3) != 0:
            fail(f"route object {(x, y)} is placed on a solid block")

    route = read("data/maps/AraunaMistRoute/scripts.inc")
    require(
        route,
        [
            "setvar VAR_ARAUNA_OPTIONAL_MISSION, 1",
            "setvar VAR_ARAUNA_OPTIONAL_MISSION, 2",
            "setvar VAR_ARAUNA_OPTIONAL_MISSION, 3",
            "giveitem ITEM_SUPER_POTION",
            "setflag FLAG_ARAUNA_MIST_ROUTE_NOTEBOOK_TAKEN",
            "setflag FLAG_ARAUNA_MIST_ROUTE_AFFECTED_MON_CLEARED",
            "setvar VAR_ARAUNA_STORY_STAGE, 5",
            "goto_if_ge VAR_ARAUNA_STORY_STAGE, 5",
            "AraunaMistRoute_Text_RuinBlocked",
        ],
        "Mist Route scripts",
    )

    pt = read("data/text/arauna/pt_br/route.inc")
    en = read("data/text/arauna/en/route.inc")
    if TEXT_LABEL.findall(pt) != TEXT_LABEL.findall(en):
        fail("Portuguese and English route text labels must match")
    if "placeholder técnico" not in pt or "technical placeholder" not in en:
        fail("the affected Pokémon must be identified as a technical placeholder")

    event_scripts = read("data/event_scripts.s")
    if '\t.include "data/text/arauna/route.inc"' not in event_scripts:
        fail("data/event_scripts.s must include the localized route bank")

    print(
        "Validated Mist Route objects, passable coordinates, notebook states "
        "0–3, affected-Pokemon story stage 5, ruin gate, bilingual text, and "
        "vanilla-only graphics."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError, StopIteration) as error:
        print(f"Mist Route validation failed: {error}", file=sys.stderr)
        sys.exit(1)

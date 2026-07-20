#!/usr/bin/env python3
"""Validate Mist Route evidence, optional mission and coast-road handoff."""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(source: str, tokens: tuple[str, ...], name: str) -> None:
    missing = [token for token in tokens if token not in source]
    if missing:
        raise ValueError(f"{name} is missing required tokens: {missing}")


def main() -> int:
    flags = read("include/constants/flags.h")
    require(flags, (
        "FLAG_ARAUNA_MIST_ROUTE_AFFECTED_MON_CLEARED  0x23",
        "FLAG_ARAUNA_MIST_ROUTE_NOTEBOOK_TAKEN        0x24",
    ), "Arauna route flags")

    map_data = json.loads(read("data/maps/AraunaMistRoute/map.json"))
    objects = map_data["object_events"]
    expected_graphics = ["OBJ_EVENT_GFX_EXPERT_M", "OBJ_EVENT_GFX_ITEM_BALL"]
    if [event["graphics_id"] for event in objects] != expected_graphics:
        raise ValueError("Mist Route must contain only the observer and optional notebook")
    if map_data["warp_events"]:
        raise ValueError("Mist Route must not contain the old hidden bounce warp")

    layout_data = json.loads(read("data/layouts/layouts.json"))
    layout = next(item for item in layout_data["layouts"] if item["id"] == "LAYOUT_ARAUNA_MIST_ROUTE")
    width = int(layout["width"])
    height = int(layout["height"])
    raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
    entries = struct.unpack(f"<{width * height}H", raw)
    for event in objects:
        x, y = int(event["x"]), int(event["y"])
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"route object {(x, y)} is outside the layout")
        if ((entries[y * width + x] >> 10) & 0x3) != 0:
            raise ValueError(f"route object {(x, y)} is placed on a solid block")

    route = read("data/maps/AraunaMistRoute/scripts.inc")
    require(route, (
        "setvar VAR_ARAUNA_OPTIONAL_MISSION, 1",
        "setvar VAR_ARAUNA_OPTIONAL_MISSION, 2",
        "setvar VAR_ARAUNA_OPTIONAL_MISSION, 3",
        "giveitem ITEM_SUPER_POTION",
        "setflag FLAG_ARAUNA_MIST_ROUTE_NOTEBOOK_TAKEN",
        "setflag FLAG_ARAUNA_MIST_ROUTE_AFFECTED_MON_CLEARED",
        "setvar VAR_ARAUNA_STORY_STAGE, 5",
        "setvar VAR_ARAUNA_STORY_STAGE, 6",
        "goto_if_ge VAR_ARAUNA_STORY_STAGE, 8, AraunaMistRoute_EventScript_ContinueToCoastRoad",
        "warp MAP_ROUTE110, 255, 17, 9",
    ), "Mist Route scripts")
    if "setflag FLAG_ARAUNA_PORTO_ARRIVED" in route:
        raise ValueError("Porto arrival must not be recorded before the coast road is crossed")

    en = read("data/text/arauna/en/route.inc")
    require(en, (
        "AraunaMistRoute_Text_AffectedPokemon::",
        "AraunaMistRoute_Text_SurveyComplete::",
        "AraunaMistRoute_Text_CoastRoad::",
        "Route110_Text_CoastRoadArrival::",
        "OLD COAST ROAD",
        "PORTO DAS REDES",
    ), "English Mist Route and coast-road text")

    event_scripts = read("data/event_scripts.s")
    if '#include "data/text/arauna/route.inc"' not in event_scripts:
        raise ValueError("localized route bank is not included")

    print("Mist Route validated: optional notebook, gray-trail evidence and full coast-road handoff.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError, StopIteration) as error:
        print(f"Mist Route validation failed: {error}", file=sys.stderr)
        sys.exit(1)

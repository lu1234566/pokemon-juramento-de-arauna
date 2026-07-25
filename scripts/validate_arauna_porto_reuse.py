#!/usr/bin/env python3
"""Validate Porto das Redes, its coast road and HM-free Tide Board."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def object_at(data: dict, x: int, y: int, graphics: str) -> dict:
    matches = [
        obj for obj in data["object_events"]
        if obj["x"] == x and obj["y"] == y and obj["graphics_id"] == graphics
    ]
    require(len(matches) == 1, f"expected one {graphics} object at ({x}, {y})")
    return matches[0]


def bg_script_at(data: dict, x: int, y: int) -> str:
    matches = [
        event["script"] for event in data["bg_events"]
        if event["x"] == x and event["y"] == y
    ]
    require(len(matches) == 1, f"expected one background event at ({x}, {y})")
    return matches[0]


def main() -> None:
    shoreline = json.loads(read("data/maps/Route109/map.json"))
    coast = json.loads(read("data/maps/Route110/map.json"))
    city = json.loads(read("data/maps/SlateportCity/map.json"))

    require(shoreline["layout"] == "LAYOUT_ROUTE109", "Porto shoreline must reuse Route 109")
    require(coast["layout"] == "LAYOUT_ROUTE110", "coast road must reuse Route 110")
    require(city["layout"] == "LAYOUT_SLATEPORT_CITY", "Porto must reuse Slateport's layout")
    require(city["connections"] == [
        {"map": "MAP_ROUTE110", "offset": 0, "direction": "up"},
        {"map": "MAP_ROUTE109", "offset": 0, "direction": "down"},
    ], "Porto must connect only to the coast road and shoreline in this slice")
    require(coast["connections"] == [
        {"map": "MAP_MAUVILLE_CITY", "offset": 0, "direction": "up"},
        {"map": "MAP_SLATEPORT_CITY", "offset": 0, "direction": "down"},
    ], "coast road connection contract changed")
    require(not city["show_map_name"], "vanilla Slateport popup must be suppressed")
    require(not coast["show_map_name"], "Route 110 popup must be suppressed")
    require(not city["allow_cycling"] and not coast["allow_cycling"], "campaign route must be crossed on foot")

    fisher = object_at(shoreline, 33, 6, "OBJ_EVENT_GFX_OLD_MAN")
    celina = object_at(city, 20, 37, "OBJ_EVENT_GFX_ARAUNA_DONA_CELINA")
    agent = object_at(city, 28, 13, "OBJ_EVENT_GFX_ARAUNA_COMPLIANCE_AGENT")
    dockworker = object_at(city, 37, 41, "OBJ_EVENT_GFX_ARAUNA_DOCKWORKER")
    builder = object_at(city, 26, 40, "OBJ_EVENT_GFX_SAILOR")
    mechanic = object_at(coast, 9, 57, "OBJ_EVENT_GFX_MAN_4")
    require(fisher["script"] == "AraunaPorto_EventScript_FisherWitness", "shoreline witness changed")
    require(celina["script"] == "AraunaPorto_EventScript_DonaCelina", "Dona Celina object changed")
    require(agent["script"] == "AraunaPorto_EventScript_ConsortiumAgent", "Consortium Agent object changed")
    require(dockworker["script"] == "AraunaPorto_EventScript_Dockworker", "dock witness changed")
    require(builder["script"] == "AraunaPorto_EventScript_BoardBuilder", "Tide Board builder is missing")
    require(mechanic["script"] == "Route110_EventScript_Mechanic", "coast-road mechanic changed")
    require(mechanic["elevation"] == 4, "coast-road mechanic must remain on the elevated Route 110 platform")

    forbidden_graphics = {"OBJ_EVENT_GFX_AQUA_MEMBER_M", "OBJ_EVENT_GFX_AQUA_MEMBER_F"}
    require(not any(obj["graphics_id"] in forbidden_graphics for obj in city["object_events"]),
            "vanilla Team Aqua objects remain in Porto")
    require(not any(obj["graphics_id"] in forbidden_graphics for obj in coast["object_events"]),
            "vanilla Team Aqua objects remain on the coast road")

    inactive_doors = {
        (10, 12): "AraunaPorto_EventScript_HouseOfTideDoor",
        (5, 19): "AraunaPorto_EventScript_EvacuatedHouseDoor",
        (4, 26): "AraunaPorto_EventScript_NetGuildDoor",
        (30, 26): "AraunaPorto_EventScript_ConsortiumPostDoor",
        (31, 26): "AraunaPorto_EventScript_ConsortiumPostDoor",
        (28, 12): "AraunaPorto_EventScript_HarborOfficeDoor",
        (40, 7): "AraunaPorto_EventScript_HarborOfficeDoor",
    }
    for coordinates, expected_script in inactive_doors.items():
        require(
            bg_script_at(city, *coordinates) == expected_script,
            f"inactive Porto doorway {coordinates} is not visibly explained",
        )

    for coordinates in ((20, 19), (21, 19)):
        require(
            bg_script_at(city, *coordinates) == "Common_EventScript_ShowPokemonCenterSign",
            f"open Pokemon Center sign is missing at {coordinates}",
        )
    for coordinates in ((14, 26), (15, 26)):
        require(
            bg_script_at(city, *coordinates) == "Common_EventScript_ShowPokemartSign",
            f"open Poke Mart sign is missing at {coordinates}",
        )

    traces = {
        (event["x"], event["y"])
        for event in shoreline["coord_events"]
        if event["script"] == "AraunaPorto_EventScript_IaracoTrace"
    }
    require(traces == {(32, 7), (33, 7)}, "Iaraco trace must cover both shoreline lanes")

    north_blocks = {
        (event["x"], event["y"])
        for event in coast["coord_events"]
        if event["script"] == "Route110_EventScript_BlockNorthRoad"
    }
    require(north_blocks == {(x, 4) for x in range(13, 22)}, "north road blocker has gaps")
    require(any(obj["script"] == "Route110_EventScript_ConsortiumCheckpoint" for obj in coast["object_events"]),
            "north closure lacks a visible checkpoint")
    require(all(
        obj["flag"] == "FLAG_UNUSED_0x04F"
        for obj in coast["object_events"]
        if obj["script"] in {
            "Route110_EventScript_NorthRoadWorker",
            "Route110_EventScript_ConsortiumCheckpoint",
        }
    ), "visible north blockers must use the reserved 0x4F object flag")
    require(coast["warp_events"] == [], "vanilla Route 110 building warps remain accessible")

    village_scripts = read("data/maps/AraunaMapLab/scripts.inc")
    mist_scripts = read("data/maps/AraunaMistRoute/scripts.inc")
    coast_scripts = read("data/maps/Route110/scripts.inc")
    shoreline_scripts = read("data/maps/Route109/scripts.inc")
    city_scripts = read("data/maps/SlateportCity/scripts.inc")
    runtime = read("data/scripts/arauna_porto_runtime.inc")

    require("warp MAP_ROUTE109" not in village_scripts, "Vila still teleports directly to Porto")
    require("warp MAP_ROUTE110, 255, 17, 9" in mist_scripts, "Mist Route does not hand off to the north coast road")
    require("FLAG_ARAUNA_COAST_ROAD_ENTERED" in coast_scripts, "coast-road arrival is not persistent")
    require("FLAG_ARAUNA_PORTO_ARRIVED" in runtime, "Porto arrival is not recorded in the city")
    require("AraunaPorto_EventScript_RoadArrival" in runtime, "custom Porto arrival script is missing")
    for script in set(inactive_doors.values()):
        require(script in runtime, f"closed-door runtime is missing {script}")

    custom_route = shoreline_scripts.split("@ Arauna reuses Route 109", 1)[1]
    require("showmonpic" not in custom_route, "unapproved Iaraco art is forced on the shoreline")
    for token in (
        "FLAG_ARAUNA_PORTO_MEMORIAL_HEARD",
        "FLAG_ARAUNA_PORTO_PERMIT_FOUND",
        "setflag FLAG_ARAUNA_PORTO_IARACO_RESTORED",
        "setflag FLAG_ARAUNA_TESTIMONY_IARA_MAE",
        "setvar VAR_ARAUNA_TESTIMONY_COUNT, 1",
    ):
        require(token in custom_route, f"shoreline story is missing {token}")
    for token in (
        "AraunaPorto_EventScript_DonaCelina",
        "AraunaPorto_EventScript_Dockworker",
        "AraunaPorto_EventScript_ConsortiumAgent",
        "trainerbattle_single TRAINER_ARAUNA_TECH_AGENT",
        "trainerbattle_single TRAINER_ARAUNA_MARE_TRIAL",
        "setflag FLAG_BADGE01_GET",
        "setvar VAR_ARAUNA_BADGE_COUNT, 1",
    ):
        require(token in city_scripts, f"Porto story is missing {token}")

    config = read("include/config/arauna.h")
    item_override = read("src/arauna_item_overrides.c")
    field_tools = read("src/arauna_field_tools.c")
    field_move = read("src/field_move.c")
    surf_script = read("data/scripts/surf.inc")
    for token in (
        "FLAG_ARAUNA_COAST_ROAD_ENTERED",
        "FLAG_ARAUNA_PORTO_IDENTITY_SEEN",
        "FLAG_ARAUNA_BOARD_RECEIVED",
        "FLAG_ARAUNA_BOARD_FIELD_UNLOCKED",
        "FLAG_ARAUNA_NORTH_ROAD_REOPENED",
    ):
        require(token in config, f"missing stable world flag alias: {token}")
    require("ITEM_DEVON_SCOPE" in item_override and "Tide Board" in item_override,
            "Devon Scope slot is not presented as the Tide Board")
    require("ItemUseOutOfBattle_AraunaBoard" in item_override, "Tide Board has no bag behavior")
    require("AraunaPartyHasMonWithSurf" in field_tools, "Tide Board does not satisfy water access")
    require("FLAG_ARAUNA_BOARD_FIELD_UNLOCKED" in field_move, "field move permission ignores the Tide Board")
    require("EventScript_UseTideBoard" in surf_script, "water interaction does not branch to the Tide Board")
    require("giveitem ITEM_DEVON_SCOPE" in runtime, "boatbuilder does not award the Tide Board")

    # The runtime is pulled in as a top-level .include from event_scripts.s so
    # the first preproc pass expands its FLAG_*/VAR_* macros before cpp runs.
    require('data/scripts/arauna_porto_runtime.inc' in read("data/event_scripts.s"),
            "Porto runtime is not included")
    wrapper = read("data/text/arauna/porto_das_redes.inc")
    require('data/text/arauna/en/porto_das_redes.inc' in wrapper, "English Porto text is not included")
    text = read("data/text/arauna/en/porto_das_redes.inc")
    for label in (
        "AraunaPorto_Text_RoadArrival::",
        "AraunaPorto_Text_DonaCelinaIntroduction::",
        "AraunaPorto_Text_ConsortiumAgentConfrontation::",
        "AraunaPorto_Text_IaraMaeTestimony::",
        "AraunaPorto_Text_MareBadgeReceived::",
        "AraunaPorto_Text_BoardReceived::",
        "AraunaPorto_Text_HouseOfTideDoor::",
        "AraunaPorto_Text_EvacuatedHouseDoor::",
        "AraunaPorto_Text_NetGuildDoor::",
        "AraunaPorto_Text_ConsortiumPostDoor::",
        "AraunaPorto_Text_HarborOfficeDoor::",
    ):
        require(label in text, f"missing Porto text label: {label}")
    require("Your dead are cleaned by memory." in text, "approved Iara-Mae line is missing")
    for literal in re.findall(r'\.string "([^"]*)"', text):
        for segment in re.split(r"\\[np]", literal):
            visible = re.sub(r"\\.", "", segment).removesuffix("$")
            require(len(visible) <= 32, f"Porto text exceeds 32 characters: {visible!r}")

    print(
        "Porto validated: full coast road, custom city identity, legible reused "
        "doorways, visible blockers and HM-free Tide Board."
    )


if __name__ == "__main__":
    main()

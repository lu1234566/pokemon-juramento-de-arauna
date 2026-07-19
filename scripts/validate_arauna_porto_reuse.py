#!/usr/bin/env python3
"""Validate Porto das Redes without allowing a new map or layout."""

from __future__ import annotations

import csv
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


def main() -> None:
    route = json.loads(read("data/maps/Route109/map.json"))
    city = json.loads(read("data/maps/SlateportCity/map.json"))

    require(route["layout"] == "LAYOUT_ROUTE109", "Porto shoreline must reuse Route 109")
    require(city["layout"] == "LAYOUT_SLATEPORT_CITY", "Porto city must reuse Slateport")
    require(route["connections"] == [
        {"map": "MAP_SLATEPORT_CITY", "offset": 0, "direction": "up"},
        {"map": "MAP_ROUTE108", "offset": 40, "direction": "left"},
    ], "Route 109 connections changed")
    require(city["connections"] == [
        {"map": "MAP_ROUTE110", "offset": 0, "direction": "up"},
        {"map": "MAP_ROUTE109", "offset": 0, "direction": "down"},
        {"map": "MAP_ROUTE134", "offset": 0, "direction": "right"},
    ], "Slateport connections changed")

    fisher = object_at(route, 33, 6, "OBJ_EVENT_GFX_OLD_MAN")
    celina = object_at(city, 20, 37, "OBJ_EVENT_GFX_OLD_WOMAN")
    agent = object_at(city, 28, 13, "OBJ_EVENT_GFX_SCIENTIST_1")
    dockworker = object_at(city, 37, 41, "OBJ_EVENT_GFX_SAILOR")
    require(fisher["script"] == "AraunaPorto_EventScript_FisherWitness",
            "existing Route 109 fisherman was not reused")
    require(celina["script"] == "AraunaPorto_EventScript_DonaCelina",
            "existing Slateport old-woman object was not reassigned to Dona Celina")
    require(agent["script"] == "AraunaPorto_EventScript_ConsortiumAgent"
            and agent["flag"] == "0",
            "existing Slateport scientist is not the visible Consortium Agent")
    require(dockworker["script"] == "AraunaPorto_EventScript_Dockworker",
            "existing Slateport sailor is not the dock-song witness")
    placeholders = [
        obj for obj in route["object_events"]
        if "Iaraco" in obj.get("script", "")
        or ("ZIGZAGOON" in obj.get("graphics_id", "")
            and "AraunaPorto" in obj.get("script", ""))
    ]
    require(not placeholders, "Iaraco still uses an overworld placeholder")
    traces = {
        (event["x"], event["y"])
        for event in route["coord_events"]
        if event["script"] == "AraunaPorto_EventScript_IaracoTrace"
    }
    require(traces == {(32, 7), (33, 7)},
            "Iaraco trace must cover both Route 109 lanes")

    vars_h = read("include/constants/vars.h")
    flags_h = read("include/constants/flags.h")
    required_vars = (
        "VAR_ARAUNA_ARC_STAGE                            0x40FB",
        "VAR_ARAUNA_BADGE_COUNT                          0x40FC",
        "VAR_ARAUNA_TESTIMONY_COUNT                      0x40FD",
    )
    required_flags = (
        "FLAG_ARAUNA_PORTO_ARRIVED                    0x28",
        "FLAG_ARAUNA_PORTO_CELINA_MET                 0x29",
        "FLAG_ARAUNA_PORTO_IARACO_SEEN                0x2A",
        "FLAG_ARAUNA_PORTO_IARACO_RESTORED            0x2B",
        "FLAG_ARAUNA_TESTIMONY_IARA_MAE               0x2C",
        "FLAG_ARAUNA_BADGE_MARE                       0x2D",
        "FLAG_ARAUNA_PORTO_MEMORIAL_HEARD             0x46",
        "FLAG_ARAUNA_PORTO_PERMIT_FOUND                0x47",
        "FLAG_ARAUNA_PORTO_DOCK_SONG_HEARD             0x48",
        "FLAG_ARAUNA_PORTO_NET_FOUND                   0x49",
        "FLAG_ARAUNA_PORTO_AGENT_DEFEATED              0x4A",
    )
    for token in required_vars:
        require(token in vars_h, f"missing campaign var: {token}")
    for token in required_flags:
        require(token in flags_h, f"missing Porto flag: {token}")

    village_scripts = read("data/maps/AraunaMapLab/scripts.inc")
    route_scripts = read("data/maps/Route109/scripts.inc")
    city_scripts = read("data/maps/SlateportCity/scripts.inc")
    require("warp MAP_ROUTE109, 255, 30, 6" in village_scripts,
            "slice does not use Route 109's dry north-beach landing")
    require("warp MAP_ROUTE109, 255, 20, 28" not in village_scripts,
            "slice still drops the player into Route 109's swimmer zone")
    custom_route = route_scripts.split("@ Arauna reuses Route 109", 1)[1]
    require("showmonpic" not in custom_route,
            "unapproved Iaraco art is forced in Route 109")
    for token in (
        "FLAG_ARAUNA_PORTO_MEMORIAL_HEARD",
        "FLAG_ARAUNA_PORTO_PERMIT_FOUND",
        "AraunaPorto_EventScript_IaracoTrace",
        "setflag FLAG_ARAUNA_PORTO_IARACO_RESTORED",
        "setflag FLAG_ARAUNA_TESTIMONY_IARA_MAE",
        "setvar VAR_ARAUNA_TESTIMONY_COUNT, 1",
        "setvar VAR_ARAUNA_ARC_STAGE, 14",
    ):
        require(token in custom_route, f"Route 109 story is missing {token}")
    for token in (
        "AraunaPorto_EventScript_DonaCelina",
        "AraunaPorto_EventScript_Dockworker",
        "AraunaPorto_EventScript_ConsortiumAgent",
        "FLAG_ARAUNA_PORTO_MEMORIAL_HEARD",
        "FLAG_ARAUNA_PORTO_PERMIT_FOUND",
        "FLAG_ARAUNA_PORTO_DOCK_SONG_HEARD",
        "FLAG_ARAUNA_PORTO_NET_FOUND",
        "FLAG_ARAUNA_PORTO_IARACO_SEEN",
        "special HealPlayerParty",
        "trainerbattle_single TRAINER_ARAUNA_TECH_AGENT",
        "trainerbattle_single TRAINER_ARAUNA_MARE_TRIAL",
        "setflag FLAG_BADGE01_GET",
        "setvar VAR_ARAUNA_BADGE_COUNT, 1",
        "setvar VAR_ARAUNA_ARC_STAGE, 15",
    ):
        require(token in city_scripts, f"Slateport story is missing {token}")

    with (ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        mapping = {int(row["arauna_dex"]): row for row in csv.DictReader(handle)}
    require(mapping[19]["species_constant"] == "SPECIES_CATERPIE",
            "Iaraco engine mapping changed")
    require(mapping[286]["species_constant"] == "SPECIES_BRELOOM",
            "Iara-Mae engine mapping changed")

    wrapper = read("data/text/arauna/porto_das_redes.inc")
    require('data/text/arauna/en/porto_das_redes.inc' in wrapper,
            "Porto text wrapper must select English")
    require("pt_br" not in wrapper and "#if" not in wrapper,
            "first Porto implementation must remain English-only")
    text = read("data/text/arauna/en/porto_das_redes.inc")
    required_labels = (
        "AraunaPorto_Text_DonaCelinaIntroduction::",
        "AraunaPorto_Text_DonaCelinaNetSong::",
        "AraunaPorto_Text_ConsortiumAgentConfrontation::",
        "AraunaPorto_Text_IaraMaeTestimony::",
        "AraunaPorto_Text_MareBadgeReceived::",
    )
    for label in required_labels:
        require(label in text, f"missing English Porto text: {label}")
    require("DONA ZILA" not in text,
            "Dona Zila still replaces Porto's local guardian")
    require("Your dead are cleaned by memory." in text,
            "the approved Iara-Mae Testimony line is missing")

    for literal in re.findall(r'\.string "([^"]*)"', text):
        for segment in re.split(r"\\[np]", literal):
            visible = re.sub(r"\\.", "", segment).removesuffix("$")
            require(len(visible) <= 32, f"Porto text exceeds 32 characters: {visible!r}")

    print(
        "Porto das Redes validated: reused Route 109 and Slateport, "
        "four evidence nodes, prose-only Iaraco trace, Dona Celina, "
        "Agent confrontation, Iara-Mae Testimony and Mare Badge."
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate Serra do Uivo on unmodified Emerald map foundations."""

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


def object_at(data: dict, x: int, y: int) -> dict:
    matches = [obj for obj in data["object_events"] if obj["x"] == x and obj["y"] == y]
    require(len(matches) == 1, f"expected one existing object at ({x}, {y})")
    return matches[0]


def main() -> None:
    town = json.loads(read("data/maps/FallarborTown/map.json"))
    route = json.loads(read("data/maps/Route114/map.json"))
    cave = json.loads(read("data/maps/MeteorFalls_1F_1R/map.json"))

    require(town["layout"] == "LAYOUT_FALLARBOR_TOWN",
            "Serra settlement must reuse Fallarbor")
    require(route["layout"] == "LAYOUT_ROUTE114",
            "Serra ascent must reuse Route 114")
    require(cave["layout"] == "LAYOUT_METEOR_FALLS_1F_1R",
            "Lobisomem scene must reuse Meteor Falls")
    require(town["connections"] == [
        {"map": "MAP_ROUTE114", "offset": 0, "direction": "left"},
        {"map": "MAP_ROUTE113", "offset": 0, "direction": "right"},
    ], "Fallarbor connections changed")
    require(route["connections"] == [
        {"map": "MAP_ROUTE115", "offset": 40, "direction": "left"},
        {"map": "MAP_FALLARBOR_TOWN", "offset": 0, "direction": "right"},
    ], "Route 114 connections changed")

    child = object_at(town, 8, 11)
    hermit = object_at(route, 19, 11)
    companion = object_at(route, 19, 12)
    lobisomem = object_at(cave, 13, 23)
    require(child["graphics_id"] == "OBJ_EVENT_GFX_ARAUNA_SERRA_CHILD"
            and child["script"] == "AraunaSerra_EventScript_LibrasChild",
            "Serra child must use the approved Arauna overworld sprite")
    require(hermit["graphics_id"] == "OBJ_EVENT_GFX_GENTLEMAN"
            and hermit["script"] == "AraunaSerra_EventScript_DeafHermit",
            "existing Route 114 gentleman was not reused")
    require(companion["graphics_id"] == "OBJ_EVENT_GFX_POOCHYENA"
            and companion["script"] == "AraunaSerra_EventScript_HermitCompanion",
            "existing Route 114 companion was not reused")
    require(lobisomem["graphics_id"] == "OBJ_EVENT_GFX_POOCHYENA"
            and lobisomem["script"] == "AraunaSerra_EventScript_Lobisomem"
            and lobisomem["flag"] == "0",
            "existing Meteor Falls object was not relocated to Lobisomem")

    flags_h = read("include/constants/flags.h")
    for token in (
        "FLAG_ARAUNA_SERRA_ARRIVED                     0x2E",
        "FLAG_ARAUNA_LIBRAS_LEARNED                    0x2F",
        "FLAG_ARAUNA_SERRA_HERMIT_UNDERSTOOD           0x30",
        "FLAG_ARAUNA_SERRA_LOBISOMEM_CALMED            0x31",
        "FLAG_ARAUNA_BADGE_UIVO                        0x32",
        "FLAG_ARAUNA_SERRA_CHAPTER_RECEIVED            0x33",
    ):
        require(token in flags_h, f"missing Serra flag: {token}")

    porto = read("data/maps/SlateportCity/scripts.inc")
    town_scripts = read("data/maps/FallarborTown/scripts.inc")
    route_scripts = read("data/maps/Route114/scripts.inc")
    cave_scripts = read("data/maps/MeteorFalls_1F_1R/scripts.inc")
    for token in (
        "warp MAP_FALLARBOR_TOWN, 255, 10, 13",
        "setvar VAR_METEOR_FALLS_STATE, 1",
        "setflag FLAG_HIDE_METEOR_FALLS_TEAM_MAGMA",
        "setflag FLAG_HIDE_METEOR_FALLS_TEAM_AQUA",
    ):
        require(token in porto, f"Porto-to-Serra handoff is missing {token}")
    require("setflag FLAG_ARAUNA_LIBRAS_LEARNED" in town_scripts,
            "Fallarbor does not teach Libras")
    for token in (
        "AraunaSerra_Text_PlayerSigns",
        "setflag FLAG_ARAUNA_SERRA_HERMIT_UNDERSTOOD",
        "setflag FLAG_BADGE02_GET",
        "setvar VAR_ARAUNA_BADGE_COUNT, 2",
        "setvar VAR_ARAUNA_ARC_STAGE, 24",
    ):
        require(token in route_scripts, f"Route 114 story is missing {token}")
    for token in (
        "showmonpic SPECIES_HOUNDOUR",
        "setflag FLAG_ARAUNA_SERRA_LOBISOMEM_CALMED",
        "setvar VAR_ARAUNA_ARC_STAGE, 23",
    ):
        require(token in cave_scripts, f"Meteor Falls story is missing {token}")

    with (ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        mapping = {int(row["arauna_dex"]): row for row in csv.DictReader(handle)}
    require(mapping[237]["species_constant"] == "SPECIES_HOUNDOUR",
            "Lobisomem engine mapping changed")

    wrapper = read("data/text/arauna/serra_do_uivo.inc")
    require('data/text/arauna/en/serra_do_uivo.inc' in wrapper,
            "Serra wrapper must select English")
    require("pt_br" not in wrapper and "#if" not in wrapper,
            "first Serra implementation must remain English-only")
    text = read("data/text/arauna/en/serra_do_uivo.inc")
    for label in (
        "AraunaSerra_Text_LibrasChildIntroduction::",
        "AraunaSerra_Text_LibrasLesson::",
        "AraunaSerra_Text_HermitNoSigns::",
        "AraunaSerra_Text_PlayerSigns::",
        "AraunaSerra_Text_LobisomemDesaturated::",
        "AraunaSerra_Text_UivoBadgeReceived::",
    ):
        require(label in text, f"missing English Serra text: {label}")
    require("Brazilian Sign Language" in text,
            "Libras must be identified accurately")
    require("not the whole language" in text,
            "three signs must not be presented as complete Libras")

    for literal in re.findall(r'\.string "([^"]*)"', text):
        for segment in re.split(r"\\[np]", literal):
            visible = re.sub(r"\\.", "", segment).removesuffix("$")
            require(len(visible) <= 32, f"Serra text exceeds 32 characters: {visible!r}")

    print(
        "Serra do Uivo validated: reused Fallarbor, Route 114 and Meteor Falls; "
        "Libras, deaf hermit, Lobisomem and Uivo Badge are persistent."
    )


if __name__ == "__main__":
    main()

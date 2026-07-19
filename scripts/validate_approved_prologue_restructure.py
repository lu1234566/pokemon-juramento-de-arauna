#!/usr/bin/env python3
"""Validate the first approved Prologue/Porto restructuring checkpoint."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise ValueError(message)


def trainer_block(source: str, trainer: str) -> str:
    marker = f"=== {trainer} ==="
    if marker not in source:
        fail(f"missing trainer party: {trainer}")
    return source.split(marker, 1)[1].split("\n=== ", 1)[0]


def main() -> None:
    village = json.loads(read("data/maps/AraunaMapLab/map.json"))
    route = json.loads(read("data/maps/AraunaMistRoute/map.json"))
    village_scripts = read("data/maps/AraunaMapLab/scripts.inc")
    route_scripts = read("data/maps/AraunaMistRoute/scripts.inc")
    trainers = read("src/data/trainers.party")
    opponents = read("include/constants/opponents.h")
    english = "\n".join(
        read(path)
        for path in (
            "data/text/arauna/en/opening.inc",
            "data/text/arauna/en/map_lab.inc",
            "data/text/arauna/en/porto_das_redes.inc",
        )
    )
    portuguese = read("data/text/arauna/pt_br/opening.inc")

    north_warps = [
        event
        for event in village["warp_events"]
        if (event["x"], event["y"], event["dest_map"]) == (
            14,
            1,
            "MAP_ARAUNA_MIST_ROUTE",
        )
    ]
    if len(north_warps) != 1:
        fail("Vila Amanhecer must use the visible north opening")

    if any(
        (event["x"], event["y"]) == (18, 11)
        for event in village["warp_events"]
    ):
        fail("the hidden route warp behind Ciro still exists")

    north_gates = [
        event
        for event in village["coord_events"]
        if (
            event["x"],
            event["y"],
            event["script"],
        )
        == (14, 2, "AraunaMapLab_EventScript_EnterMistRoute")
    ]
    if len(north_gates) != 1:
        fail("the visible north opening must retain the story gate")

    if "walk_down" not in village_scripts:
        fail("the north gate must return a blocked player toward the village")
    if "warp MAP_ARAUNA_MAP_LAB, 255, 14, 3" not in route_scripts:
        fail("the route must return beside the visible north opening")

    changed_identity = "\n".join(
        (
            json.dumps(village),
            village_scripts,
            english,
            portuguese,
            trainers,
            opponents,
        )
    )
    for stale in ("Nilo", "NILO", "SCOUT_NILO"):
        if stale in changed_identity:
            fail(f"stale Ciro identity remains: {stale}")

    expected_ciro = {
        "TRAINER_ARAUNA_CIRO_PIMPAU": "Treecko",
        "TRAINER_ARAUNA_CIRO_CARAMELO": "Torchic",
        "TRAINER_ARAUNA_CIRO_QUERO": "Mudkip",
    }
    for trainer, species in expected_ciro.items():
        party = trainer_block(trainers, trainer)
        for token in ("Name: CIRO", species, "Level: 7"):
            if token not in party:
                fail(f"{trainer} is missing {token}")
        if "Poochyena" in party:
            fail(f"{trainer} still uses the old Poochyena slot")

    agent = trainer_block(trainers, "TRAINER_ARAUNA_TECH_AGENT")
    if "Poochyena" in agent:
        fail("Ciro and the Agent still share the old Poochyena lead")

    for token in (
        "FLAG_ARAUNA_CIRO_STARTER_PIMPAU",
        "FLAG_ARAUNA_CIRO_STARTER_CARAMELO",
        "TRAINER_ARAUNA_CIRO_PIMPAU",
        "TRAINER_ARAUNA_CIRO_CARAMELO",
        "TRAINER_ARAUNA_CIRO_QUERO",
    ):
        if token not in village_scripts:
            fail(f"conditional Ciro battle is missing {token}")

    if any(
        event.get("graphics_id") == "OBJ_EVENT_GFX_POOCHYENA"
        for event in route["object_events"]
    ):
        fail("the route still displays Poochyena as the faded creature")

    faded_gates = {
        (event["x"], event["y"])
        for event in route["coord_events"]
        if event["script"] == "AraunaMistRoute_EventScript_AffectedPokemon"
    }
    if faded_gates != {(10, 3), (11, 3)}:
        fail("the non-visual faded encounter does not cover both route lanes")

    if "LOCALID_ARAUNA_MIST_ROUTE_AFFECTED_MON" in route_scripts:
        fail("the route script still controls the removed Poochyena object")

    for placeholder in (
        "END OF THE CURRENT",
        "VERTICAL SLICE",
        "FIM DO VERTICAL SLICE",
    ):
        if placeholder in english or placeholder in portuguese:
            fail(f"player-facing development placeholder remains: {placeholder}")

    if "AraunaMapLab_Text_PortoLead" not in village_scripts:
        fail("the prologue must hand off to the Porto das Redes lead")

    plan = read("docs/arauna/APPROVED_PROLOGUE_PORTO_RESTRUCTURE.md")
    for decision in (
        "Visible north exit",
        "First Link ruins deferred",
        "local Tide Storyteller",
    ):
        if decision not in plan:
            fail(f"approved plan is missing decision: {decision}")

    print(
        "Approved restructure checkpoint validated: north exit, Ciro starter "
        "teams, no Poochyena placeholder and Porto handoff"
    )


if __name__ == "__main__":
    main()

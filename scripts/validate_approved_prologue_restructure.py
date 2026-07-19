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
    porto_route = json.loads(read("data/maps/Route109/map.json"))
    porto_city = json.loads(read("data/maps/SlateportCity/map.json"))
    house_scripts = read("data/maps/AraunaPlayerHouse/scripts.inc")
    village_scripts = read("data/maps/AraunaMapLab/scripts.inc")
    route_scripts = read("data/maps/AraunaMistRoute/scripts.inc")
    porto_route_scripts = read("data/maps/Route109/scripts.inc")
    porto_city_scripts = read("data/maps/SlateportCity/scripts.inc")
    trainers = read("src/data/trainers.party")
    opponents = read("include/constants/opponents.h")
    flags = read("include/constants/flags.h")
    vars_source = read("include/constants/vars.h")
    porto_text = read("data/text/arauna/en/porto_das_redes.inc")
    english = "\n".join(
        read(path)
        for path in (
            "data/text/arauna/en/opening.inc",
            "data/text/arauna/en/map_lab.inc",
            "data/text/arauna/en/porto_das_redes.inc",
            "data/text/arauna/en/route.inc",
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

    if any(
        event.get("dest_map") == "MAP_ARAUNA_FIRST_LINK_RUIN"
        for event in route["warp_events"]
    ):
        fail("the First Link ruin is still on the critical route")

    critical_path = "\n".join((village_scripts, route_scripts, english))
    for deferred in (
        "AraunaMapLab_EventScript_CiroMemoryConclusion",
        "AraunaMistRoute_EventScript_EnterRuin",
        "FIRST LINK CHAMBER",
        "CHAMPION's memory",
    ):
        if deferred in critical_path:
            fail(f"deferred First Link material remains in the prologue: {deferred}")

    story_tokens = (
        "AraunaMapLab_EventScript_CiroBeforeRoute",
        "setvar VAR_ARAUNA_STORY_STAGE, 3",
        "setvar VAR_ARAUNA_STORY_STAGE, 4",
        "setvar VAR_ARAUNA_STORY_STAGE, 5",
        "setvar VAR_ARAUNA_STORY_STAGE, 6",
        "goto_if_eq VAR_ARAUNA_STORY_STAGE, 6, AraunaMapLab_EventScript_CiroBattle",
        "setvar VAR_ARAUNA_STORY_STAGE, 8",
    )
    combined_flow = "\n".join((village_scripts, route_scripts))
    for token in story_tokens:
        if token not in combined_flow:
            fail(f"explore-before-Ciro flow is missing {token}")

    playable_night_flags = (
        "FLAG_ARAUNA_PROLOGUE_NIGHT_PIMPAU",
        "FLAG_ARAUNA_PROLOGUE_NIGHT_CARAMELO",
        "FLAG_ARAUNA_PROLOGUE_NIGHT_QUERO",
        "FLAG_ARAUNA_PROLOGUE_TALKED_ZILA_AT_NIGHT",
        "FLAG_ARAUNA_PROLOGUE_TALKED_ANAHI_AT_NIGHT",
        "FLAG_ARAUNA_PROLOGUE_NIGHT_COMPLETE",
    )
    for token in playable_night_flags:
        if token not in flags or token not in house_scripts:
            fail(f"playable night is missing state: {token}")

    opening_block = house_scripts.split(
        "AraunaPlayerHouse_EventScript_Opening::", 1
    )[1].split("AraunaPlayerHouse_EventScript_DonaZila::", 1)[0]
    if (
        "AraunaPlayerHouse_Text_NightWatch" in opening_block
        or "AraunaPlayerHouse_Text_Dawn" in opening_block
    ):
        fail("night watch and dawn still run as an opening text dump")

    for token in (
        "AraunaPlayerHouse_EventScript_CheckNightReady",
        "AraunaPlayerHouse_EventScript_BeginDawn",
        "fadescreen FADE_TO_BLACK",
        "fadescreen FADE_FROM_BLACK",
    ):
        if token not in house_scripts:
            fail(f"playable night transition is missing {token}")

    iaraco_objects = [
        event
        for event in porto_route["object_events"]
        if "Iaraco" in event.get("script", "")
        or (
            "ZIGZAGOON" in event.get("graphics_id", "")
            and "AraunaPorto" in event.get("script", "")
        )
    ]
    if iaraco_objects:
        fail("Route 109 still uses an overworld placeholder for Iaraco")

    iaraco_traces = {
        (event["x"], event["y"])
        for event in porto_route["coord_events"]
        if event["script"] == "AraunaPorto_EventScript_IaracoTrace"
    }
    if iaraco_traces != {(32, 7), (33, 7)}:
        fail("the prose-only Iaraco trace must cover both Route 109 lanes")

    porto_objects = {
        event.get("script"): event
        for event in porto_city["object_events"]
        if event.get("script", "").startswith("AraunaPorto_EventScript_")
    }
    for script in (
        "AraunaPorto_EventScript_DonaCelina",
        "AraunaPorto_EventScript_Dockworker",
        "AraunaPorto_EventScript_ConsortiumAgent",
    ):
        if script not in porto_objects:
            fail(f"Porto exploration is missing its reassigned NPC: {script}")
    if porto_objects["AraunaPorto_EventScript_ConsortiumAgent"]["flag"] != "0":
        fail("the Consortium Agent is still hidden by a vanilla story flag")

    evidence_flags = (
        "FLAG_ARAUNA_PORTO_MEMORIAL_HEARD",
        "FLAG_ARAUNA_PORTO_PERMIT_FOUND",
        "FLAG_ARAUNA_PORTO_DOCK_SONG_HEARD",
        "FLAG_ARAUNA_PORTO_NET_FOUND",
    )
    investigation_requirements = (*evidence_flags, "FLAG_ARAUNA_PORTO_IARACO_SEEN")
    porto_flow = "\n".join((porto_route_scripts, porto_city_scripts))
    for token in (*investigation_requirements, "FLAG_ARAUNA_PORTO_AGENT_DEFEATED"):
        if token not in flags or token not in porto_flow:
            fail(f"Porto investigation is missing save-safe state: {token}")

    evidence_check = porto_city_scripts.split(
        "AraunaPorto_EventScript_CheckEvidence::", 1
    )[1].split("AraunaPorto_EventScript_DonaCelinaAwardBadge::", 1)[0]
    for token in investigation_requirements:
        if f"goto_if_unset {token}" not in evidence_check:
            fail(f"the Agent confrontation does not require {token}")

    agent_scene = porto_city_scripts.split(
        "AraunaPorto_EventScript_ConsortiumAgent::", 1
    )[1].split("AraunaPorto_EventScript_ConsortiumAgentDenial::", 1)[0]
    heal_at = agent_scene.find("special HealPlayerParty")
    battle_at = agent_scene.find("trainerbattle_single TRAINER_ARAUNA_TECH_AGENT")
    if heal_at < 0 or battle_at < 0 or heal_at > battle_at:
        fail("the investigation must heal immediately before the Agent battle")

    custom_route = porto_route_scripts.split(
        "@ Arauna reuses Route 109", 1
    )[1]
    if "showmonpic" in custom_route or "LOCALID_ARAUNA_PORTO_IARACO" in custom_route:
        fail("unapproved Iaraco artwork is still forced into the restoration")
    if "setflag FLAG_ARAUNA_PORTO_IARACO_RESTORED" not in custom_route:
        fail("Iaraco is not marked restored at the field restoration scene")

    porto_identity = "\n".join((porto_city_scripts, porto_text))
    for stale in ("DonaZila", "DONA ZILA"):
        if stale in porto_identity:
            fail(f"Dona Zila still replaces Porto's local guardian: {stale}")
    for token in ("DonaCelina", "DONA CELINA", "I clean the water.",
                  "Your dead are cleaned by memory."):
        if token not in porto_identity:
            fail(f"Dona Celina or the approved Testimony is missing: {token}")

    celina = trainer_block(trainers, "TRAINER_ARAUNA_MARE_TRIAL")
    for token in ("Name: CELINA", "Level: 14", "Level: 15", "Level: 17"):
        if token not in celina:
            fail(f"Dona Celina's Tide Vigil is missing {token}")
    agent = trainer_block(trainers, "TRAINER_ARAUNA_TECH_AGENT")
    if "Level: 12" not in agent:
        fail("the Porto Agent still uses the prologue test level")

    arc_state = "\n".join((village_scripts, porto_flow, vars_source))
    for stage in (10, 11, 12, 13, 14, 15):
        if str(stage) not in arc_state:
            fail(f"Porto's save-safe arc graph is missing stage {stage}")

    for raw in porto_text.splitlines():
        if '.string "' not in raw:
            continue
        visible = raw.split('.string "', 1)[1].rsplit('"', 1)[0]
        for marker in ("\\n", "\\p", "$"):
            visible = visible.replace(marker, "")
        if len(visible) > 32:
            fail(f"Porto GBA text line exceeds 32 characters: {visible}")

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
        "teams, playable night, explore-before-rival flow, four-part Porto "
        "investigation, Dona Celina, Agent confrontation and Tide Vigil"
    )


if __name__ == "__main__":
    main()

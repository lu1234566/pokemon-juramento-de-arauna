#!/usr/bin/env python3
"""Validate Ciro's prologue conclusion and the physical road to Porto."""

from __future__ import annotations

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


def main() -> int:
    script = read("data/maps/AraunaMapLab/scripts.inc")
    require(
        script,
        (
            "goto_if_eq VAR_ARAUNA_STORY_STAGE, 6, AraunaMapLab_EventScript_CiroBattle",
            "TRAINER_ARAUNA_CIRO_PIMPAU",
            "TRAINER_ARAUNA_CIRO_CARAMELO",
            "TRAINER_ARAUNA_CIRO_QUERO",
            "setvar VAR_ARAUNA_STORY_STAGE, 7",
            "AraunaMapLab_Text_CiroPostBattle",
            "AraunaMapLab_Text_CiroDeparture",
            "setvar VAR_ARAUNA_STORY_STAGE, 8",
            "AraunaMapLab_Text_PortoLead",
            "goto_if_ge VAR_ARAUNA_STORY_STAGE, 8, AraunaMapLab_EventScript_ObjectiveSliceComplete",
            "warp MAP_ARAUNA_MIST_ROUTE, 255, 10, 17",
        ),
        "Ciro prologue conclusion",
    )
    for forbidden in (
        "warp MAP_ROUTE109",
        "AraunaMapLab_EventScript_OfferPortoTravel",
        "AraunaMapLab_EventScript_TravelToPorto",
    ):
        if forbidden in script:
            fail(f"prologue conclusion still contains instant travel: {forbidden}")

    map_lab_text = read("data/text/arauna/en/map_lab.inc")
    opening_text = read("data/text/arauna/en/opening.inc")
    require(
        map_lab_text,
        (
            "AraunaMapLab_Text_CiroPostBattle::",
            "You listened before giving",
            "That is harder than winning.",
        ),
        "English Ciro battle conclusion",
    )
    require(
        opening_text,
        (
            "AraunaMapLab_Text_CiroDeparture::",
            "They called me to PORTO.",
            "AraunaMapLab_Text_PortoLead::",
            "PORTO DAS REDES",
            "Follow the east path and cross",
            "the coast road on foot.",
        ),
        "English Porto lead",
    )

    print(
        "Validated Ciro's three rival variants, stage-8 prologue conclusion, "
        "and the required on-foot route toward Porto das Redes."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Prologue conclusion validation failed: {error}", file=sys.stderr)
        sys.exit(1)

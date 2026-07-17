#!/usr/bin/env python3
"""Validate Nilo's Bond reaction and the vertical-slice completion state."""

from __future__ import annotations

import re
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
    script = read("data/maps/AraunaMapLab/scripts.inc")
    require(
        script,
        [
            "goto_if_eq VAR_ARAUNA_STORY_STAGE, 7, AraunaMapLab_EventScript_NiloEpilogue",
            "goto_if_ge VAR_ARAUNA_STORY_STAGE, 8, AraunaMapLab_EventScript_NiloAfterSlice",
            "goto_if_eq VAR_ARAUNA_BOND_CHOICE, 1",
            "goto_if_eq VAR_ARAUNA_BOND_CHOICE, 2",
            "AraunaMapLab_EventScript_NiloCompassionReaction",
            "setvar VAR_ARAUNA_STORY_STAGE, 8",
            "AraunaMapLab_Text_VerticalSliceComplete",
            "goto_if_eq VAR_ARAUNA_STORY_STAGE, 7, AraunaMapLab_EventScript_ObjectiveNiloReturn",
        ],
        "Araucaria village epilogue",
    )

    pt = read("data/text/arauna/pt_br/opening.inc")
    en = read("data/text/arauna/en/opening.inc")
    if TEXT_LABEL.findall(pt) != TEXT_LABEL.findall(en):
        fail("Portuguese and English opening labels must remain identical")
    for value in ("CORAGEM", "SABEDORIA", "COMPAIXAO"):
        if value not in pt:
            fail(f"Portuguese epilogue is missing {value}")
    for value in ("COURAGE", "WISDOM", "COMPASSION"):
        if value not in en:
            fail(f"English epilogue is missing {value}")
    if "CAMPEÃO" not in pt or "CHAMPION" not in en:
        fail("the epilogue must preserve the Champion revelation")

    print(
        "Validated Nilo's three Bond reactions, the Champion conclusion, "
        "guide objectives, and persistent vertical-slice stage 8."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Vertical-slice epilogue validation failed: {error}", file=sys.stderr)
        sys.exit(1)

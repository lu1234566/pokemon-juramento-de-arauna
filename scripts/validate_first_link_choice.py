#!/usr/bin/env python3
"""Validate the first Bond choice and the chamber gate."""

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
    if "FLAG_ARAUNA_FIRST_LINK_RESCUE_COMPLETE  0x25" not in flags:
        fail("the first-link rescue flag must be allocated at 0x25")

    map_data = json.loads(read("data/maps/AraunaFirstLinkRuin/map.json"))
    objects = map_data["object_events"]
    if len(objects) != 1 or objects[0]["graphics_id"] != "OBJ_EVENT_GFX_POOCHYENA":
        fail("the ruin must contain one vanilla Poochyena placeholder")
    triggers = map_data["coord_events"]
    if len(triggers) != 1:
        fail("the ruin must contain exactly one scripted chamber gate")
    gate = triggers[0]
    if (gate["x"], gate["y"], gate["script"]) != (
        15,
        3,
        "AraunaFirstLinkRuin_EventScript_ChamberGate",
    ):
        fail("the chamber gate must remain at (15, 3)")

    layout_data = json.loads(read("data/layouts/layouts.json"))
    layout = next(
        item for item in layout_data["layouts"]
        if item["id"] == "LAYOUT_ARAUNA_FIRST_LINK_RUIN"
    )
    route_map = (ROOT / layout["blockdata_filepath"]).read_bytes()
    source_map = (ROOT / "data/layouts/MirageTower_1F/map.bin").read_bytes()
    if route_map != source_map:
        fail("the current ruin shell is expected to match the vanilla Mirage Tower 1F layout")
    width = int(layout["width"])
    height = int(layout["height"])
    entries = struct.unpack(f"<{width * height}H", route_map)
    for x, y, name in (
        (int(objects[0]["x"]), int(objects[0]["y"]), "affected Pokemon"),
        (int(gate["x"]), int(gate["y"]), "chamber gate"),
    ):
        if ((entries[y * width + x] >> 10) & 0x3) != 0:
            fail(f"{name} at {(x, y)} is placed on a solid block")

    script = read("data/maps/AraunaFirstLinkRuin/scripts.inc")
    require(
        script,
        [
            "setvar VAR_ARAUNA_BOND_CHOICE, 1",
            "setvar VAR_ARAUNA_BOND_CHOICE, 2",
            "setvar VAR_ARAUNA_BOND_CHOICE, 3",
            "setvar VAR_ARAUNA_STORY_STAGE, 6",
            "setflag FLAG_ARAUNA_FIRST_LINK_RESCUE_COMPLETE",
            "goto_if_ge VAR_ARAUNA_STORY_STAGE, 6",
            "AraunaFirstLinkRuin_Text_ChamberBlocked",
        ],
        "first-link scripts",
    )

    pt = read("data/text/arauna/pt_br/ruin.inc")
    en = read("data/text/arauna/en/ruin.inc")
    if TEXT_LABEL.findall(pt) != TEXT_LABEL.findall(en):
        fail("Portuguese and English ruin labels must match")
    # The vanilla Emerald font has no uppercase A-tilde glyph. Keep the
    # all-caps decision label readable without introducing an art change.
    for value in ("CORAGEM", "SABEDORIA", "COMPAIXAO"):
        if value not in pt:
            fail(f"Portuguese choice text is missing {value}")
    for value in ("COURAGE", "WISDOM", "COMPASSION"):
        if value not in en:
            fail(f"English choice text is missing {value}")

    if '\t.include "data/text/arauna/ruin.inc"' not in read("data/event_scripts.s"):
        fail("data/event_scripts.s must include the localized ruin bank")

    print(
        "Validated the first Bond choice values 1–3, story stage 6, the "
        "passable rescue object, chamber gate, bilingual text, and unchanged "
        "vanilla ruin shell."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError, StopIteration) as error:
        print(f"First-link validation failed: {error}", file=sys.stderr)
        sys.exit(1)

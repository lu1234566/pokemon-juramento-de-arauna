#!/usr/bin/env python3
"""Validate Arauna's heal checkpoint, whiteout return, and repeatable healing."""

from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_LABEL = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):{1,2}$", re.MULTILINE)
HEAL_ID = "HEAL_LOCATION_ARAUNA_RESEARCH_CENTER"
RESPAWN = (14, 8)


def fail(message: str) -> None:
    raise ValueError(message)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def block(source: str, label: str, next_label: str) -> str:
    start = source.find(label + "::")
    end = source.find(next_label + "::", start + 1)
    if start < 0 or end < 0:
        fail(f"could not isolate {label}")
    return source[start:end]


def main() -> int:
    heal_data = json.loads(read("src/data/heal_locations.json"))
    matches = [item for item in heal_data["heal_locations"] if item["id"] == HEAL_ID]
    if len(matches) != 1:
        fail("Arauna must define exactly one research-center heal location")
    heal = matches[0]
    if (heal.get("map"), heal.get("x"), heal.get("y")) != (
        "MAP_ARAUNA_MAP_LAB",
        *RESPAWN,
    ):
        fail(f"unexpected Arauna respawn data: {heal}")
    if "respawn_map" in heal or "respawn_npc" in heal:
        fail("Arauna whiteout must return directly to the outdoor checkpoint")

    layouts = json.loads(read("data/layouts/layouts.json"))["layouts"]
    layout = next(item for item in layouts if item["id"] == "LAYOUT_ARAUNA_MAP_LAB")
    width, height = int(layout["width"]), int(layout["height"])
    x, y = RESPAWN
    if not (0 <= x < width and 0 <= y < height):
        fail("Arauna respawn is outside the village layout")
    raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
    entries = struct.unpack(f"<{width * height}H", raw)
    if ((entries[y * width + x] >> 10) & 0x3) != 0:
        fail("Arauna respawn coordinate is blocked")

    center = read("data/maps/AraunaResearchCenter/scripts.inc")
    choice = block(
        center,
        "AraunaResearchCenter_EventScript_CompleteChoice",
        "AraunaResearchCenter_EventScript_SelectionLocked",
    )
    if f"setrespawn {HEAL_ID}" not in choice:
        fail("starter completion must register the Arauna respawn")

    after_choice = block(
        center,
        "AraunaResearchCenter_EventScript_AfterChoice",
        "AraunaResearchCenter_EventScript_RouteOpen",
    )
    route_open = block(
        center,
        "AraunaResearchCenter_EventScript_RouteOpen",
        "AraunaResearchCenter_EventScript_PicaPau",
    )
    for name, script in (("after choice", after_choice), ("route open", route_open)):
        if "special HealPlayerParty" not in script:
            fail(f"Dra. Maia must heal the party during {name}")

    pt = read("data/text/arauna/pt_br/opening.inc")
    en = read("data/text/arauna/en/opening.inc")
    if TEXT_LABEL.findall(pt) != TEXT_LABEL.findall(en):
        fail("opening text labels must match between Portuguese and English")
    if pt.count("equipe foi recuperada") < 2:
        fail("Portuguese text must disclose both repeatable healing states")
    if en.count("party was restored") < 2:
        fail("English text must disclose both repeatable healing states")

    print(
        "Validated Arauna whiteout checkpoint at (14, 8), passable collision, "
        "starter-time respawn registration, repeatable Maia healing, and "
        "bilingual recovery text."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError, KeyError, StopIteration) as error:
        print(f"Safe-recovery validation failed: {error}", file=sys.stderr)
        sys.exit(1)

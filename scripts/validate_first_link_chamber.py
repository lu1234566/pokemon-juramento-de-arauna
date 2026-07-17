#!/usr/bin/env python3
"""Validate the First Link miniboss, memory, rewards, and completion state."""

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
    for name, value in (
        ("FLAG_ARAUNA_FIRST_LINK_MEMORY_SEEN", "0x26"),
        ("FLAG_ARAUNA_FIRST_LINK_CHAMBER_COMPLETE", "0x27"),
    ):
        if not re.search(rf"^#define\s+{name}\s+{value}\b", flags, re.MULTILINE):
            fail(f"{name} must be allocated at {value}")

    opponents = read("include/constants/opponents.h")
    require(
        opponents,
        [
            "#define TRAINER_ARAUNA_TECH_AGENT           856",
            "#define TRAINERS_COUNT_EMERALD     857",
        ],
        "trainer constants",
    )
    trainer_data = read("src/data/trainers.party")
    agent_block = trainer_data.split("=== TRAINER_ARAUNA_TECH_AGENT ===", 1)[-1]
    if agent_block == trainer_data or "=== " in agent_block:
        fail("the Arauna technical agent must be the final trainer block")
    require(agent_block, ["Name: AGENTE", "Poochyena", "Voltorb"], "agent party")

    map_data = json.loads(read("data/maps/AraunaFirstLinkChamber/map.json"))
    objects = map_data["object_events"]
    if len(objects) != 1:
        fail("the chamber must contain exactly one technical-agent object")
    agent = objects[0]
    if (
        agent["local_id"],
        agent["graphics_id"],
        agent["x"],
        agent["y"],
        agent["flag"],
    ) != (
        "LOCALID_ARAUNA_FIRST_LINK_TECH_AGENT",
        "OBJ_EVENT_GFX_SCIENTIST_1",
        10,
        10,
        "FLAG_ARAUNA_FIRST_LINK_CHAMBER_COMPLETE",
    ):
        fail("the technical agent must use the approved vanilla placeholder at (10, 10)")

    layouts = json.loads(read("data/layouts/layouts.json"))["layouts"]
    layout = next(
        item for item in layouts
        if item["id"] == "LAYOUT_ARAUNA_FIRST_LINK_CHAMBER"
    )
    chamber_map = (ROOT / layout["blockdata_filepath"]).read_bytes()
    vanilla_map = (ROOT / "data/layouts/SealedChamber_InnerRoom/map.bin").read_bytes()
    if chamber_map != vanilla_map:
        fail("the chamber shell must remain equal to vanilla Sealed Chamber")
    width = int(layout["width"])
    height = int(layout["height"])
    entries = struct.unpack(f"<{width * height}H", chamber_map)
    x, y = int(agent["x"]), int(agent["y"])
    if ((entries[y * width + x] >> 10) & 0x3) != 0:
        fail("the technical agent is placed on a solid block")

    script = read("data/maps/AraunaFirstLinkChamber/scripts.inc")
    require(
        script,
        [
            "TRAINER_ARAUNA_TECH_AGENT",
            "goto_if_defeated TRAINER_ARAUNA_TECH_AGENT",
            "special HealPlayerParty",
            "playse SE_M_EARTHQUAKE",
            "FLAG_ARAUNA_FIRST_LINK_MEMORY_SEEN",
            "giveitem ITEM_X_ATTACK",
            "giveitem ITEM_X_SP_ATK",
            "giveitem ITEM_GUARD_SPEC",
            "setvar VAR_ARAUNA_STORY_STAGE, 7",
            "FLAG_ARAUNA_FIRST_LINK_CHAMBER_COMPLETE",
        ],
        "chamber script",
    )

    pt = read("data/text/arauna/pt_br/chamber.inc")
    en = read("data/text/arauna/en/chamber.inc")
    if TEXT_LABEL.findall(pt) != TEXT_LABEL.findall(en):
        fail("Portuguese and English chamber labels must match")
    if "CAMPEÃO" not in pt or "CHAMPION" not in en:
        fail("the guardian memory must mention the missing Champion")
    if '\t.include "data/text/arauna/chamber.inc"' not in read("data/event_scripts.s"):
        fail("data/event_scripts.s must include the localized chamber bank")

    print(
        "Validated the vanilla chamber shell, technical-agent miniboss, "
        "guardian memory, three Bond rewards, bag-full retry, and stage 7."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError, StopIteration) as error:
        print(f"First-link chamber validation failed: {error}", file=sys.stderr)
        sys.exit(1)

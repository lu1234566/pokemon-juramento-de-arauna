#!/usr/bin/env python3
"""Validate the integrated Arauna priority-10 NPC v3 assets."""

from __future__ import annotations

import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBJECTS = {
    "data/maps/AraunaPlayerHouse/map.json": {
        "AraunaPlayerHouse_EventScript_DonaZila": "OBJ_EVENT_GFX_ARAUNA_DONA_ZILA",
        "AraunaPlayerHouse_EventScript_Anahi": "OBJ_EVENT_GFX_ARAUNA_PROFESSORA_ANAHI",
    },
    "data/maps/AraunaMapLab/map.json": {
        "AraunaMapLab_EventScript_Ciro": "OBJ_EVENT_GFX_ARAUNA_CIRO_PROLOGUE",
    },
    "data/maps/SlateportCity/map.json": {
        "AraunaPorto_EventScript_CiroPorto": "OBJ_EVENT_GFX_ARAUNA_CIRO_CONSORCIO",
        "AraunaPorto_EventScript_DonaCelina": "OBJ_EVENT_GFX_ARAUNA_DONA_CELINA",
        "AraunaPorto_EventScript_ConsortiumAgent": "OBJ_EVENT_GFX_ARAUNA_COMPLIANCE_AGENT",
        "AraunaPorto_EventScript_Dockworker": "OBJ_EVENT_GFX_ARAUNA_DOCKWORKER",
        "AraunaPorto_EventScript_MemorialKeeper": "OBJ_EVENT_GFX_ARAUNA_MEMORIAL_FISHER",
    },
    "data/maps/FallarborTown/map.json": {
        "AraunaSerra_EventScript_LibrasChild": "OBJ_EVENT_GFX_ARAUNA_SERRA_CHILD",
    },
}

OVERWORLDS = (
    "dona_zila", "professora_anahi", "ciro_prologo", "ciro_consorcio",
    "dona_celina", "agente_conformidade", "trabalhador_cais",
    "pescador_memorial", "crianca_serra",
)
TRAINERS = {
    "salon_maiden_anabel.png": "Professora Anahi",
    "dome_ace_tucker.png": "Ciro prologue",
    "factory_head_noland.png": "Ciro Consortium",
    "arena_tycoon_greta.png": "Dona Celina",
    "pike_queen_lucy.png": "Compliance Agent",
    "palace_maven_spenser.png": "deaf hermit",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def png_info(path: Path) -> tuple[int, int, int, bytes | None]:
    data = path.read_bytes()
    require(data.startswith(b"\x89PNG\r\n\x1a\n"), f"not a PNG: {path}")
    offset = 8
    width = height = colour_type = -1
    transparency = None
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        if kind == b"IHDR":
            width, height, _, colour_type, _, _, _ = struct.unpack(">IIBBBBB", payload)
        elif kind == b"tRNS":
            transparency = payload
        elif kind == b"IEND":
            break
        offset += 12 + length
    return width, height, colour_type, transparency


def main() -> None:
    for name in OVERWORLDS:
        path = ROOT / f"graphics/object_events/pics/people/arauna/{name}.png"
        width, height, colour_type, transparency = png_info(path)
        require((width, height, colour_type) == (48, 128, 3), f"invalid overworld PNG: {path}")
        require(transparency is not None and transparency[:1] == b"\x00", f"missing index-0 transparency: {path}")
    for filename, label in TRAINERS.items():
        path = ROOT / "graphics/trainers/front_pics" / filename
        width, height, colour_type, transparency = png_info(path)
        require((width, height, colour_type) == (64, 64, 3), f"invalid {label} trainer PNG: {path}")
        require(transparency is not None and transparency[:1] == b"\x00", f"missing trainer transparency: {path}")

    for map_path, expected in OBJECTS.items():
        data = json.loads((ROOT / map_path).read_text(encoding="utf-8"))
        by_script = {obj.get("script"): obj for obj in data["object_events"]}
        for script, graphics in expected.items():
            require(script in by_script, f"missing object script {script} in {map_path}")
            require(by_script[script]["graphics_id"] == graphics, f"wrong graphics for {script}")

    event_ids = (ROOT / "include/constants/event_objects.h").read_text(encoding="utf-8")
    graphics = (ROOT / "src/data/object_events/object_event_graphics_info_pointers.h").read_text(encoding="utf-8")
    for graphics_id in {value for values in OBJECTS.values() for value in values.values()}:
        require(graphics_id in event_ids, f"missing object graphics ID {graphics_id}")
        require(f"[{graphics_id}]" in graphics, f"missing object graphics pointer {graphics_id}")

    parties = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
    for token in (
        "Pic: Dome Ace Tucker",
        "Pic: Pike Queen Lucy",
        "Pic: Arena Tycoon Greta",
        "Pic: Palace Maven Spenser",
    ):
        require(token in parties, f"story trainer portrait not wired: {token}")
    agent = parties.split("=== TRAINER_ARAUNA_TECH_AGENT ===", 1)[1].split("\n=== ", 1)[0]
    require("Gender: Female" in agent, "v3 Compliance Agent trainer gender is not female")

    serra = (ROOT / "data/text/arauna/en/serra_do_uivo.inc").read_text(encoding="utf-8")
    require("LOOK. WAIT. SAFE." in serra, "approved text support for Libras changed")
    for forbidden in ("LibrasLookAnimation", "LibrasWaitAnimation", "LibrasSafeAnimation"):
        require(forbidden not in "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in (ROOT / "data").rglob("*.inc")),
                f"unvalidated lexical animation was added: {forbidden}")

    docs = (ROOT / "docs/arauna/NPC_PRIORITY10_V3_INTEGRATION.md").read_text(encoding="utf-8")
    require("v3 is canonical" in docs, "v3 canonical-source contract is missing")
    require("No improvised LOOK / WAIT / SAFE animation" in docs, "Libras gate is missing from integration notes")

    print("Priority-10 NPC v3 validated: nine overworlds, six trainer portraits, story wiring and Libras safety gate.")


if __name__ == "__main__":
    main()

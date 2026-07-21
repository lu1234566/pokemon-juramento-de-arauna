#!/usr/bin/env python3
"""Validate the approved priority-10 NPC pack integration."""

from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OVERWORLD = {
    "graphics/object_events/pics/people/mom.png": (144, 32),
    "graphics/object_events/pics/people/reporter_f.png": (144, 32),
    "graphics/object_events/pics/people/camper.png": (144, 32),
    "graphics/object_events/pics/people/devon_employee.png": (144, 32),
    "graphics/object_events/pics/people/old_woman.png": (144, 32),
    "graphics/object_events/pics/people/scientist_1.png": (144, 32),
    "graphics/object_events/pics/people/sailor.png": (144, 32),
    "graphics/object_events/pics/people/wallace.png": (144, 32),
    "graphics/object_events/pics/people/girl_1.png": (144, 32),
    "graphics/object_events/pics/people/gentleman.png": (144, 32),
}

TRAINERS = {
    "graphics/trainers/front_pics/salon_maiden_anabel.png": (64, 64),
    "graphics/trainers/front_pics/dome_ace_tucker.png": (64, 64),
    "graphics/trainers/front_pics/factory_head_noland.png": (64, 64),
    "graphics/trainers/front_pics/arena_tycoon_greta.png": (64, 64),
    "graphics/trainers/front_pics/pike_queen_lucy.png": (64, 64),
    "graphics/trainers/front_pics/palace_maven_spenser.png": (64, 64),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def read_png(path: Path) -> tuple[int, int, int, int, set[int], bool]:
    data = path.read_bytes()
    require(data[:8] == b"\x89PNG\r\n\x1a\n", f"not a PNG: {path}")
    width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(
        ">IIBBBBB", data[16:29]
    )
    require(compression == 0 and filtering == 0 and interlace == 0, f"unsupported PNG encoding: {path}")
    require(bit_depth == 8 and color_type == 3, f"NPC asset must be 8-bit indexed: {path}")
    pos = 8
    compressed = bytearray()
    transparent_zero = False
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        payload = data[pos + 8:pos + 8 + length]
        if kind == b"IDAT":
            compressed.extend(payload)
        elif kind == b"tRNS":
            transparent_zero = bool(payload) and payload[0] == 0
        pos += 12 + length
        if kind == b"IEND":
            break
    raw = zlib.decompress(bytes(compressed))
    stride = width
    require(len(raw) == height * (stride + 1), f"unexpected PNG scanline size: {path}")
    previous = bytearray(stride)
    used: set[int] = set()
    offset = 0
    for _ in range(height):
        filter_type = raw[offset]
        encoded = raw[offset + 1:offset + 1 + stride]
        decoded = bytearray(stride)
        for x, value in enumerate(encoded):
            left = decoded[x - 1] if x else 0
            up = previous[x]
            upper_left = previous[x - 1] if x else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = up
            elif filter_type == 3:
                predictor = (left + up) // 2
            elif filter_type == 4:
                predictor = paeth(left, up, upper_left)
            else:
                raise ValueError(f"unknown PNG filter {filter_type}: {path}")
            decoded[x] = (value + predictor) & 0xFF
        used.update(decoded)
        previous = decoded
        offset += stride + 1
    return width, height, bit_depth, color_type, used, transparent_zero


def object_for_script(map_data: dict, script: str) -> dict:
    matches = [obj for obj in map_data["object_events"] if obj["script"] == script]
    require(len(matches) == 1, f"expected one object for {script}")
    return matches[0]


def main() -> None:
    for relative, expected_size in {**OVERWORLD, **TRAINERS}.items():
        path = ROOT / relative
        require(path.is_file(), f"missing NPC asset: {relative}")
        width, height, bit_depth, color_type, used_indices, transparent_zero = read_png(path)
        require((width, height) == expected_size, f"wrong dimensions for {relative}: {(width, height)}")
        require(bit_depth == 8 and color_type == 3, f"NPC asset must be indexed: {relative}")
        require(1 <= len(used_indices) <= 16 and max(used_indices) <= 15,
                f"NPC asset exceeds 16 used palette indices: {relative}")
        require(transparent_zero, f"palette index 0 must be transparent: {relative}")
    for relative in OVERWORLD:
        require(read_png(ROOT / relative)[0] // 16 == 9, f"overworld sheet must contain 9 frames: {relative}")

    house = json.loads((ROOT / "data/maps/AraunaPlayerHouse/map.json").read_text())
    village = json.loads((ROOT / "data/maps/AraunaMapLab/map.json").read_text())
    porto = json.loads((ROOT / "data/maps/SlateportCity/map.json").read_text())
    serra = json.loads((ROOT / "data/maps/FallarborTown/map.json").read_text())
    ascent = json.loads((ROOT / "data/maps/Route114/map.json").read_text())

    expected = {
        ("house", "AraunaPlayerHouse_EventScript_DonaZila"): "OBJ_EVENT_GFX_MOM",
        ("house", "AraunaPlayerHouse_EventScript_Anahi"): "OBJ_EVENT_GFX_REPORTER_F",
        ("village", "AraunaMapLab_EventScript_Guide"): "OBJ_EVENT_GFX_MAN_3",
        ("village", "AraunaMapLab_EventScript_Ciro"): "OBJ_EVENT_GFX_CAMPER",
        ("porto", "AraunaPorto_EventScript_CiroPorto"): "OBJ_EVENT_GFX_DEVON_EMPLOYEE",
        ("porto", "AraunaPorto_EventScript_DonaCelina"): "OBJ_EVENT_GFX_OLD_WOMAN",
        ("porto", "AraunaPorto_EventScript_ConsortiumAgent"): "OBJ_EVENT_GFX_SCIENTIST_1",
        ("porto", "AraunaPorto_EventScript_Dockworker"): "OBJ_EVENT_GFX_SAILOR",
        ("porto", "AraunaPorto_EventScript_MemorialKeeper"): "OBJ_EVENT_GFX_WALLACE",
        ("serra", "AraunaSerra_EventScript_LibrasChild"): "OBJ_EVENT_GFX_GIRL_1",
        ("ascent", "AraunaSerra_EventScript_DeafHermit"): "OBJ_EVENT_GFX_GENTLEMAN",
    }
    maps = {"house": house, "village": village, "porto": porto, "serra": serra, "ascent": ascent}
    for map_name, map_data in maps.items():
        for obj in map_data["object_events"]:
            require("movement_trange_x" not in obj and "movement_trange_y" not in obj,
                    f"{map_name} contains a misspelled movement range field")
            require("movement_range_x" in obj and "movement_range_y" in obj,
                    f"{map_name} object is missing movement range fields: {obj.get('script')}")
    for (map_name, script), graphics in expected.items():
        actual = object_for_script(maps[map_name], script)["graphics_id"]
        require(actual == graphics, f"{script} uses {actual}, expected {graphics}")

    doc = (ROOT / "docs/arauna/PRIORITY10_NPC_INTEGRATION.md").read_text(encoding="utf-8")
    require("v3 is canonical" in doc, "NPC integration must identify v3 as canonical")
    require("LOOK / WAIT / SAFE" in doc, "Libras lexical-animation guardrail is missing")
    require("not implemented" in doc, "Libras guardrail must remain explicit")

    integration_dir = ROOT / ".integration/npc_v3"
    require(not integration_dir.exists(), "temporary NPC integration payload was not removed")
    print("Priority-10 NPC pack validated: 10 overworld sheets, 6 portraits and 11 story bindings.")


if __name__ == "__main__":
    main()

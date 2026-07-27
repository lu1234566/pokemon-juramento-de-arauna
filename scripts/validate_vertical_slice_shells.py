#!/usr/bin/env python3
"""Validate the independent map shells used by the Arauna vertical slice."""

from __future__ import annotations

import json
import struct
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_GROUP = "gMapGroup_AraunaPrototype"

EXPECTED_MAPS = {
    "AraunaMapLab": ("MAP_ARAUNA_MAP_LAB", "LAYOUT_ARAUNA_MAP_LAB", 2, 2),
    "AraunaPlayerHouse": ("MAP_ARAUNA_PLAYER_HOUSE", "LAYOUT_ARAUNA_PLAYER_HOUSE", 2, 2),
    "AraunaResearchCenter": ("MAP_ARAUNA_RESEARCH_CENTER", "LAYOUT_ARAUNA_RESEARCH_CENTER", 2, 0),
    "AraunaMistRoute": ("MAP_ARAUNA_MIST_ROUTE", "LAYOUT_ARAUNA_MIST_ROUTE", 0, 6),
    "AraunaFirstLinkRuin": ("MAP_ARAUNA_FIRST_LINK_RUIN", "LAYOUT_ARAUNA_FIRST_LINK_RUIN", 2, 1),
    "AraunaFirstLinkChamber": ("MAP_ARAUNA_FIRST_LINK_CHAMBER", "LAYOUT_ARAUNA_FIRST_LINK_CHAMBER", 1, 0),
}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read valid JSON from {path.relative_to(ROOT)}: {error}")


def read_entries(layout: dict) -> tuple[int, int, tuple[int, ...]]:
    width = int(layout["width"])
    height = int(layout["height"])
    path = ROOT / layout["blockdata_filepath"]
    data = path.read_bytes()
    expected_size = width * height * 2
    if len(data) != expected_size:
        fail(f"{path.relative_to(ROOT)} has {len(data)} bytes; expected {expected_size}")
    return width, height, struct.unpack(f"<{width * height}H", data)


def collision(entry: int) -> int:
    return (entry >> 10) & 0x3


def metatile_id(entry: int) -> int:
    return entry & 0x3FF


def validate_transition_paths(name: str, layout: dict, warps: list[dict], coords: list[dict]) -> None:
    width, height, entries = read_entries(layout)
    coordinates = [(int(event["x"]), int(event["y"])) for event in [*warps, *coords]]
    if len(coordinates) != len(set(coordinates)):
        fail(f"{name} contains duplicate transition coordinates")
    if not coordinates:
        fail(f"{name} must contain at least one transition")

    for x, y in coordinates:
        if not (0 <= x < width and 0 <= y < height):
            fail(f"{name} transition {(x, y)} is outside {width}x{height}")
        entry = entries[y * width + x]
        if collision(entry) != 0 and metatile_id(entry) not in {0x248, 0x249}:
            fail(f"{name} transition {(x, y)} is placed on a solid block")

    start = coordinates[0]
    reached = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if (
                (nx, ny) not in reached
                and 0 <= nx < width
                and 0 <= ny < height
                and (
                    collision(entries[ny * width + nx]) == 0
                    or metatile_id(entries[ny * width + nx]) in {0x248, 0x249}
                )
            ):
                reached.add((nx, ny))
                queue.append((nx, ny))
    unreachable = [coordinate for coordinate in coordinates if coordinate not in reached]
    if unreachable:
        fail(f"{name} has unreachable transition coordinates: {unreachable}")


def main() -> int:
    groups = load_json(ROOT / "data/maps/map_groups.json")
    expected_names = list(EXPECTED_MAPS)
    if groups.get(MAP_GROUP) != expected_names:
        fail(f"{MAP_GROUP} must remain exactly {expected_names}")

    layout_data = load_json(ROOT / "data/layouts/layouts.json")
    layouts = {layout["id"]: layout for layout in layout_data["layouts"]}
    event_index = (ROOT / "data/event_scripts.s").read_text(encoding="utf-8")
    maps: dict[str, dict] = {}
    used_paths: set[str] = set()

    for name, (map_id, layout_id, warp_count, coord_count) in EXPECTED_MAPS.items():
        map_data = load_json(ROOT / "data/maps" / name / "map.json")
        if map_data.get("id") != map_id or map_data.get("layout") != layout_id:
            fail(f"{name} map or layout id changed")
        script_path = ROOT / "data/maps" / name / "scripts.inc"
        script = script_path.read_text(encoding="utf-8")
        if f"{name}_MapScripts::" not in script:
            fail(f"{script_path.relative_to(ROOT)} lacks {name}_MapScripts")
        if f'\t.include "data/maps/{name}/scripts.inc"' not in event_index:
            fail(f"data/event_scripts.s does not include {name}/scripts.inc")

        warps = map_data.get("warp_events") or []
        coords = map_data.get("coord_events") or []
        if len(warps) != warp_count or len(coords) != coord_count:
            fail(f"{name} expected {warp_count} warps/{coord_count} triggers; got {len(warps)}/{len(coords)}")
        if any(event.get("type") != "trigger" or not event.get("script") for event in coords):
            fail(f"{name} contains an invalid coordinate trigger")

        layout = layouts.get(layout_id)
        if layout is None:
            fail(f"missing layout {layout_id}")
        prefix = f"data/layouts/{name}/"
        for key in ("blockdata_filepath", "border_filepath"):
            path = layout.get(key, "")
            if not path.startswith(prefix):
                fail(f"{layout_id} must use files below {prefix}")
            if path in used_paths:
                fail(f"{layout_id} reuses another Arauna layout path")
            used_paths.add(path)
            if not (ROOT / path).is_file():
                fail(f"missing {path}")

        validate_transition_paths(name, layout, warps, coords)
        maps[name] = map_data

    village = maps["AraunaMapLab"]
    village_warps = [(event["x"], event["y"]) for event in village["warp_events"]]
    village_triggers = [(event["x"], event["y"]) for event in village["coord_events"]]
    if village_warps != [(6, 7), (14, 7)]:
        fail(f"village building anchors are misaligned: {village_warps}")
    if village_triggers != [(18, 11), (19, 11)]:
        fail(f"visible east-road triggers are misaligned: {village_triggers}")

    village_layout = layouts["LAYOUT_ARAUNA_MAP_LAB"]
    if village_layout["primary_tileset"] != "gTileset_General":
        fail("AraunaMapLab must use the vanilla General primary tileset")
    if village_layout["secondary_tileset"] != "gTileset_Petalburg":
        fail("AraunaMapLab must use the vanilla Petalburg secondary tileset")

    village_scripts = (ROOT / "data/maps/AraunaMapLab/scripts.inc").read_text(encoding="utf-8")
    mist_scripts = (ROOT / "data/maps/AraunaMistRoute/scripts.inc").read_text(encoding="utf-8")
    if "warp MAP_ARAUNA_MIST_ROUTE, 255, 10, 17" not in village_scripts:
        fail("visible east road does not enter Mist Route")
    if "warp MAP_ARAUNA_MAP_LAB, 255, 17, 11" not in mist_scripts:
        fail("Mist Route does not return to the village")
    if "warp MAP_ROUTE110, 255, 14, 9" not in mist_scripts:
        fail("post-prologue Mist Route does not continue to the coast road")

    print("Validated 6 independent Arauna layouts, visible village exits and scripted route continuity.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"vertical slice shell validation failed: {error}", file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""Validate the independent, navigable map shells used by the vertical slice."""

from __future__ import annotations

import json
import struct
import sys
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAP_GROUP = "gMapGroup_AraunaPrototype"

EXPECTED_MAPS = {
    "AraunaMapLab": ("MAP_ARAUNA_MAP_LAB", "LAYOUT_ARAUNA_MAP_LAB", 3, 3),
    "AraunaPlayerHouse": (
        "MAP_ARAUNA_PLAYER_HOUSE",
        "LAYOUT_ARAUNA_PLAYER_HOUSE",
        2,
        0,
    ),
    "AraunaResearchCenter": (
        "MAP_ARAUNA_RESEARCH_CENTER",
        "LAYOUT_ARAUNA_RESEARCH_CENTER",
        2,
        0,
    ),
    "AraunaMistRoute": (
        "MAP_ARAUNA_MIST_ROUTE",
        "LAYOUT_ARAUNA_MIST_ROUTE",
        2,
        4,
    ),
    "AraunaFirstLinkRuin": (
        "MAP_ARAUNA_FIRST_LINK_RUIN",
        "LAYOUT_ARAUNA_FIRST_LINK_RUIN",
        2,
        0,
    ),
    "AraunaFirstLinkChamber": (
        "MAP_ARAUNA_FIRST_LINK_CHAMBER",
        "LAYOUT_ARAUNA_FIRST_LINK_CHAMBER",
        1,
        0,
    ),
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
    try:
        data = path.read_bytes()
    except OSError as error:
        fail(f"cannot read {path.relative_to(ROOT)}: {error}")
    expected_size = width * height * 2
    if len(data) != expected_size:
        fail(
            f"{path.relative_to(ROOT)} has {len(data)} bytes; "
            f"expected {expected_size} for {width}x{height}"
        )
    entries = struct.unpack(f"<{width * height}H", data)
    return width, height, entries


def collision(entry: int) -> int:
    return (entry >> 10) & 0x3


def validate_transition_paths(
    name: str, layout: dict, warps: list[dict], coord_events: list[dict]
) -> None:
    width, height, entries = read_entries(layout)
    coordinates = [
        (int(event["x"]), int(event["y"])) for event in [*warps, *coord_events]
    ]
    if len(coordinates) != len(set(coordinates)):
        fail(f"{name} contains duplicate warp coordinates")

    for x, y in coordinates:
        if not (0 <= x < width and 0 <= y < height):
            fail(f"{name} warp {(x, y)} is outside its {width}x{height} layout")
        if collision(entries[y * width + x]) != 0:
            fail(f"{name} warp {(x, y)} is placed on a solid block")

    if not coordinates:
        fail(f"{name} must contain at least one transition")

    start = coordinates[0]
    reached = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            nx, ny = neighbor
            if (
                neighbor not in reached
                and 0 <= nx < width
                and 0 <= ny < height
                and collision(entries[ny * width + nx]) == 0
            ):
                reached.add(neighbor)
                queue.append(neighbor)

    unreachable = [coordinate for coordinate in coordinates if coordinate not in reached]
    if unreachable:
        fail(f"{name} has unreachable warp coordinates: {unreachable}")


def main() -> int:
    map_groups = load_json(ROOT / "data/maps/map_groups.json")
    expected_names = list(EXPECTED_MAPS)
    actual_names = map_groups.get(MAP_GROUP)
    if actual_names != expected_names:
        fail(f"{MAP_GROUP} must be exactly {expected_names}; got {actual_names}")

    layout_data = load_json(ROOT / "data/layouts/layouts.json")
    layouts = {layout["id"]: layout for layout in layout_data["layouts"]}
    maps: dict[str, dict] = {}
    map_ids: dict[str, str] = {}
    blockdata_paths: set[str] = set()
    border_paths: set[str] = set()
    try:
        event_script_index = (ROOT / "data/event_scripts.s").read_text(encoding="utf-8")
    except OSError as error:
        fail(f"cannot read data/event_scripts.s: {error}")

    for name, (map_id, layout_id, warp_count, coord_count) in EXPECTED_MAPS.items():
        map_path = ROOT / "data/maps" / name / "map.json"
        script_path = ROOT / "data/maps" / name / "scripts.inc"
        map_data = load_json(map_path)
        if map_data.get("id") != map_id:
            fail(f"{name} must use map id {map_id}")
        if map_data.get("layout") != layout_id:
            fail(f"{name} must use layout {layout_id}")
        if map_id in map_ids:
            fail(f"duplicate map id {map_id}")
        map_ids[map_id] = name

        try:
            script = script_path.read_text(encoding="utf-8")
        except OSError as error:
            fail(f"cannot read {script_path.relative_to(ROOT)}: {error}")
        if f"{name}_MapScripts::" not in script:
            fail(f"{script_path.relative_to(ROOT)} lacks {name}_MapScripts")
        include = f\'\\t.include "data/maps/{name}/scripts.inc"\'
        if include not in event_script_index:
            fail(f"data/event_scripts.s does not include {name}/scripts.inc")

        warps = map_data.get("warp_events") or []
        if len(warps) != warp_count:
            fail(f"{name} must contain {warp_count} warps; got {len(warps)}")
        coord_events = map_data.get("coord_events") or []
        if len(coord_events) != coord_count:
            fail(
                f"{name} must contain {coord_count} coordinate transitions; "
                f"got {len(coord_events)}"
            )
        for event in coord_events:
            if event.get("type") != "trigger" or not event.get("script"):
                fail(f"{name} contains a coordinate event without a trigger script")

        layout = layouts.get(layout_id)
        if layout is None:
            fail(f"missing layout {layout_id}")
        expected_prefix = f"data/layouts/{name}/"
        blockdata = layout.get("blockdata_filepath", "")
        border = layout.get("border_filepath", "")
        if not blockdata.startswith(expected_prefix) or not border.startswith(expected_prefix):
            fail(f"{layout_id} must use independent files below {expected_prefix}")
        if blockdata in blockdata_paths or border in border_paths:
            fail(f"{layout_id} reuses another Arauna layout path")
        blockdata_paths.add(blockdata)
        border_paths.add(border)
        if not (ROOT / border).is_file():
            fail(f"missing {border}")

        validate_transition_paths(name, layout, warps, coord_events)
        maps[name] = map_data

    for source_name, map_data in maps.items():
        for warp_id, warp in enumerate(map_data["warp_events"]):
            destination_name = map_ids.get(warp["dest_map"])
            if destination_name is None:
                fail(f"{source_name} warp {warp_id} targets unknown map {warp['dest_map']}")
            destination_warps = maps[destination_name]["warp_events"]
            try:
                destination_id = int(warp["dest_warp_id"])
                destination = destination_warps[destination_id]
            except (ValueError, IndexError):
                fail(
                    f"{source_name} warp {warp_id} targets invalid warp "
                    f"{warp['dest_warp_id']} in {destination_name}"
                )
            if destination["dest_map"] != map_data["id"]:
                fail(
                    f"{source_name} warp {warp_id} has no reciprocal route "
                    f"from {destination_name}"
                )

    reachable = {"AraunaMapLab"}
    queue = deque(reachable)
    while queue:
        current = queue.popleft()
        for warp in maps[current]["warp_events"]:
            destination = map_ids[warp["dest_map"]]
            if destination not in reachable:
                reachable.add(destination)
                queue.append(destination)
    if reachable != set(EXPECTED_MAPS):
        fail(f"map graph is disconnected; reachable maps: {sorted(reachable)}")

    print(
        "Validated 6 independent Arauna layouts, 12 reciprocal warp anchors, "
        "7 coordinate transitions, passable endpoints, and a connected "
        "vertical-slice map graph."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ValueError as error:
        print(f"vertical slice shell validation failed: {error}", file=sys.stderr)
        sys.exit(1)

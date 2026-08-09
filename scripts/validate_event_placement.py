#!/usr/bin/env python3
"""Reject scripted coordinates that sit inside a wall.

Map data records a coordinate; nothing checks that a player can stand on it.
The Mist Route handed off to Route 110 at (17, 9), which is solid rock, so the
player materialised inside the fence. The two arrival triggers were placed on
the same rock and never fired, and two of the three road workers stood inside
the cliff beside them. Every one of those is a plain integer in a JSON file and
survived every check in this suite.

Collision lives in the layout's map.bin: one u16 per block, bits 10-11 holding
the collision value, where 0 means passable. Reading it is enough to tell a
corridor from a cliff.

Scope is the maps Arauna places events on. Vanilla maps legitimately park
decorative objects on blocked tiles, so auditing all of them would report
hundreds of intentional placements; the point here is to catch coordinates this
project chose.
"""

from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Maps whose Arauna event coordinates must be reachable.
WATCHED = {
    "Route110",
    "Route109",
    "AraunaMapLab",
    "AraunaMistRoute",
    "AraunaPlayerHouse",
    "AraunaFirstLinkRuin",
    "AraunaResearchCenter",
    "SlateportCity",
}

WARP_RE = re.compile(r"^\s*warp\s+(MAP_[A-Z0-9_]+)\s*,\s*\S+\s*,\s*(\d+)\s*,\s*(\d+)", re.M)


def load_layouts() -> dict[str, tuple[int, int, Path]]:
    data = json.loads((ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8"))
    out = {}
    for entry in data["layouts"]:
        if entry:
            out[entry["id"]] = (
                entry["width"],
                entry["height"],
                ROOT / entry["blockdata_filepath"],
            )
    return out


def collision_reader(layout_id: str, layouts):
    if layout_id not in layouts:
        return None
    width, height, path = layouts[layout_id]
    if not path.exists():
        return None
    blob = path.read_bytes()

    def blocked(x: int, y: int) -> bool | None:
        if not (0 <= x < width and 0 <= y < height):
            return None  # off the map entirely
        offset = (y * width + x) * 2
        if offset + 2 > len(blob):
            return None
        return ((struct.unpack_from("<H", blob, offset)[0] >> 10) & 0x3) != 0

    return blocked


def main() -> int:
    layouts = load_layouts()
    problems: list[str] = []
    checked = 0

    map_ids: dict[str, str] = {}
    for map_json in sorted((ROOT / "data/maps").glob("*/map.json")):
        data = json.loads(map_json.read_text(encoding="utf-8"))
        map_ids[data["id"]] = map_json.parent.name

    for name in sorted(WATCHED):
        map_json = ROOT / "data/maps" / name / "map.json"
        if not map_json.exists():
            problems.append(f"{name}: map.json is missing")
            continue
        data = json.loads(map_json.read_text(encoding="utf-8"))
        blocked = collision_reader(data["layout"], layouts)
        if blocked is None:
            continue

        for section in ("coord_events", "object_events"):
            for index, event in enumerate(data.get(section) or []):
                x, y = event.get("x"), event.get("y")
                if not isinstance(x, int) or not isinstance(y, int):
                    continue
                checked += 1
                state = blocked(x, y)
                if state is None:
                    problems.append(f"{name}: {section}[{index}] at ({x}, {y}) is off the map")
                elif state:
                    label = event.get("script") or event.get("graphics_id") or "?"
                    problems.append(
                        f"{name}: {section}[{index}] at ({x}, {y}) is inside a wall "
                        f"-> {label}"
                    )

    # Warp destinations written by hand in Arauna scripts.
    for scripts in sorted((ROOT / "data/maps").glob("*/scripts.inc")):
        if scripts.parent.name not in WATCHED:
            continue
        for found in WARP_RE.finditer(scripts.read_text(encoding="utf-8")):
            target, x, y = found.group(1), int(found.group(2)), int(found.group(3))
            folder = map_ids.get(target)
            if folder is None:
                continue
            dest = json.loads((ROOT / "data/maps" / folder / "map.json").read_text(encoding="utf-8"))
            blocked = collision_reader(dest["layout"], layouts)
            if blocked is None:
                continue
            checked += 1
            state = blocked(x, y)
            if state is None:
                problems.append(
                    f"{scripts.parent.name}: warp to {target} ({x}, {y}) is off the map"
                )
            elif state:
                problems.append(
                    f"{scripts.parent.name}: warp to {target} lands on ({x}, {y}), "
                    "which is inside a wall"
                )

    if problems:
        print("Event placement check FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print(
            f"\n{len(problems)} coordinate(s) a player cannot stand on.",
            file=sys.stderr,
        )
        return 1

    print(f"Event placement check passed: {checked} coordinates are on walkable ground")
    return 0


if __name__ == "__main__":
    sys.exit(main())

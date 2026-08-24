#!/usr/bin/env python3
"""Audit the map graph for warps and connections that can strand the player.

Three failure modes matter before launch:
  * a warp whose destination map does not exist, or whose dest_warp_id has no
    matching warp on that map -- the player lands on an undefined warp;
  * a map connection pointing at a map that does not exist;
  * a connection with no matching return connection, so a route can be entered
    but not left the same way.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MAPS = ROOT / "data" / "maps"

OPPOSITE = {"left": "right", "right": "left", "up": "down", "down": "up"}
# Dive/emerge pairs are vertical transitions, not walkable edges.
VERTICAL = {"dive", "emerge"}


def load_maps() -> dict[str, dict]:
    out = {}
    for path in sorted(MAPS.glob("*/map.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        out[data["id"]] = data
    return out


def main() -> int:
    maps = load_maps()
    by_id = {m: d for m, d in maps.items()}
    problems: list[str] = []
    warp_count = conn_count = 0

    for map_id, data in by_id.items():
        name = data.get("name", map_id)
        warps = data.get("warp_events") or []
        for i, warp in enumerate(warps):
            warp_count += 1
            dest = warp.get("dest_map")
            if dest in ("MAP_NONE", "MAP_DYNAMIC", None):
                continue
            target = by_id.get(dest)
            if target is None:
                problems.append(f"{name} warp[{i}] -> unknown map {dest}")
                continue
            try:
                wid = int(warp.get("dest_warp_id"))
            except (TypeError, ValueError):
                # Some warps use a named constant; skip rather than guess.
                continue
            available = len(target.get("warp_events") or [])
            if wid < 0 or wid >= available:
                problems.append(
                    f"{name} warp[{i}] -> {dest} warp id {wid}, "
                    f"but that map defines {available} warp(s)"
                )

        for conn in data.get("connections") or []:
            conn_count += 1
            direction = conn.get("direction")
            other = conn.get("map")
            if other not in by_id:
                problems.append(f"{name} connection {direction} -> unknown map {other}")
                continue
            if direction in VERTICAL:
                continue
            back = OPPOSITE.get(direction)
            if back is None:
                continue
            returns = [
                c for c in (by_id[other].get("connections") or [])
                if c.get("map") == map_id and c.get("direction") == back
            ]
            if not returns:
                problems.append(
                    f"{name} connects {direction} to {other}, "
                    f"but {other} has no {back} connection back"
                )

    for line in problems:
        print(f"  - {line}")
    print(
        f"\n{len(problems)} map-graph problem(s) "
        f"across {len(by_id)} maps, {warp_count} warps, {conn_count} connections."
    )
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

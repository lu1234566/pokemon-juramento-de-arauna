#!/usr/bin/env python3
"""Reject map-edge openings a player can walk through untriggered.

The Arauna maps leave the world through coordinate triggers rather than warps,
so the trigger has to cover every walkable tile of the opening. It did not.

Vila Amanhecer's east gate is three tiles tall (y=10 to 12) and only y=11 was
covered; the Mist Route's north gate is four tiles wide (x=8 to 11) and only
x=10 and 11 were covered. Leaving along any other row or column crossed the
boundary with nothing to fire, which reads in play as a wide gate where only
one tile works.

This walks the outermost ring of each listed map, groups the walkable tiles
into runs, and requires a coordinate event on every tile of every run.
"""

from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Maps whose exits are coordinate triggers rather than warps.
WATCHED = ("AraunaMapLab", "AraunaMistRoute")


def layouts() -> dict[str, tuple[int, int, Path]]:
    data = json.loads((ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8"))
    return {
        entry["id"]: (entry["width"], entry["height"], ROOT / entry["blockdata_filepath"])
        for entry in data["layouts"]
        if entry
    }


def runs(tiles: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    """Group consecutive edge tiles into openings."""
    out: list[list[tuple[int, int]]] = []
    for tile in tiles:
        if out and (
            abs(tile[0] - out[-1][-1][0]) + abs(tile[1] - out[-1][-1][1]) == 1
        ):
            out[-1].append(tile)
        else:
            out.append([tile])
    return out


def main() -> int:
    table = layouts()
    problems: list[str] = []
    checked = 0

    for name in WATCHED:
        data = json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))
        width, height, path = table[data["layout"]]
        blob = path.read_bytes()

        def blocked(x: int, y: int) -> bool:
            offset = (y * width + x) * 2
            return ((struct.unpack_from("<H", blob, offset)[0] >> 10) & 0x3) != 0

        triggered = {(e["x"], e["y"]) for e in (data.get("coord_events") or [])}
        warped = {(e["x"], e["y"]) for e in (data.get("warp_events") or [])}
        covered = triggered | warped

        edges = {
            "north": [(x, 0) for x in range(width)],
            "south": [(x, height - 1) for x in range(width)],
            "west": [(0, y) for y in range(height)],
            "east": [(width - 1, y) for y in range(height)],
        }
        for side, ring in edges.items():
            walkable = [tile for tile in ring if not blocked(*tile)]
            for opening in runs(walkable):
                checked += 1
                gaps = [tile for tile in opening if tile not in covered]
                if gaps and len(gaps) < len(opening):
                    problems.append(
                        f"{name}: the {side} opening spans {len(opening)} tiles "
                        f"but {len(gaps)} of them fire nothing: {gaps}"
                    )

    if problems:
        print("Edge transition check FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print(
            f"\n{len(problems)} opening(s) a player can leave through untriggered.",
            file=sys.stderr,
        )
        return 1

    print(f"Edge transition check passed: {checked} map-edge openings are fully covered")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Scan the Arauna English text banks for lines that overflow a 32-char box.

The renderers that consume these JSON banks validate width one file at a time
and stop at the first offender. This walks every bank at once. {PLAYER} is
modelled at the widest name the game accepts so a long player name cannot push
a line off the box.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

MAX_VISIBLE_WIDTH = 32
# Widest runtime expansion per placeholder, from include/constants/global.h.
PLACEHOLDER_WIDTHS = {
    "{PLAYER}": 7,     # PLAYER_NAME_LENGTH
    "{RIVAL}": 7,
    # Runtime buffers in these banks hold species names.
    "{STR_VAR_1}": 10, # POKEMON_NAME_LENGTH
    "{STR_VAR_2}": 10,
    "{STR_VAR_3}": 10,
    # Single-glyph control codes occupy one character cell.
    "{UP_ARROW}": 1,
    "{DOWN_ARROW}": 1,
    "{LEFT_ARROW}": 1,
    "{RIGHT_ARROW}": 1,
    "{PKMN}": 2,       # the PK/MN ligature pair
    "{POKEBLOCK}": 10,
}
DEFAULT_PLACEHOLDER_WIDTH = 10
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")
CONTROL_RE = re.compile(r"\\[npl]")
# Banks also carry structural metadata; only dialogue has a box to overflow.
NON_TEXT_KEYS = ("path", "file", "target", "symbol", "label")

BANKS = pathlib.Path(__file__).resolve().parents[2] / "data" / "text" / "arauna" / "en"


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub(
        lambda m: "X" * PLACEHOLDER_WIDTHS.get(m.group(0), DEFAULT_PLACEHOLDER_WIDTH),
        payload.replace("$", ""),
    )
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def walk(node, trail: str):
    if isinstance(node, str):
        yield trail, node
    elif isinstance(node, list):
        for i, item in enumerate(node):
            yield from walk(item, f"{trail}[{i}]")
    elif isinstance(node, dict):
        for key, item in node.items():
            if key in NON_TEXT_KEYS:
                continue
            yield from walk(item, f"{trail}.{key}")


def main() -> int:
    total = 0
    banks = sorted(BANKS.glob("*.json"))
    for bank in banks:
        try:
            data = json.loads(bank.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"{bank.name}: invalid JSON: {exc}", file=sys.stderr)
            total += 1
            continue
        for trail, payload in walk(data, bank.name):
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    total += 1
                    print(f"{trail}: {len(segment)} chars: {segment!r}")
    print(f"\n{total} oversized line(s) across {len(banks)} banks.")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())

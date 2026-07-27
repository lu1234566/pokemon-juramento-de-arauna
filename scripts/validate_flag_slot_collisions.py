#!/usr/bin/env python3
"""Reject two names that claim the same flag or var slot.

Arauna keeps flag aliases in two places: the main table in
``include/constants/flags.h`` and the project block in
``include/config/arauna.h``. Both compile into the same build, so a slot
claimed in one file and reused in the other produces two names for one bit of
save data. Nothing complains -- not the compiler, not the linker, not any other
check here -- and the damage only shows up in play, as two unrelated events
switching each other on.

That is exactly what happened to 0x4B-0x4F: the prologue story flags landed on
top of the Porto and coast-road aliases, so hearing Dona Zila's founding story
also told the game the player had already reached the coast road, and picking
the "I will listen first" departure promise reopened the blockaded north road
before the player held a single badge.

Only literal numeric defines are compared. Derived entries (``FLAG_TEMP_1`` and
friends, written as ``BASE + 0x1``) are anchored to a base that this repository
does not move, and resolving them would mean evaluating arbitrary C expressions.
The FireRed tables are skipped: they are a parallel namespace that never
compiles alongside the Emerald ones.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Headers whose defines all reach the same build.
HEADERS = (
    "include/constants/flags.h",
    "include/constants/vars.h",
    "include/config/arauna.h",
)

DEFINE_RE = re.compile(
    r"^\s*#define\s+((?:FLAG|VAR)_[A-Za-z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)\s*(?://.*)?$"
)

# Vanilla parks a large block of inapplicable names on 0; that is deliberate.
SENTINEL = 0


def main() -> int:
    slots: dict[tuple[str, int], list[tuple[str, str]]] = defaultdict(list)

    for header in HEADERS:
        path = ROOT / header
        if not path.exists():
            print(f"missing header: {header}", file=sys.stderr)
            return 1
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            found = DEFINE_RE.match(line)
            if found:
                name, value = found.group(1), int(found.group(2), 0)
                slots[(name.split("_")[0], value)].append((name, f"{header}:{number}"))

    problems = []
    for (kind, value), claims in sorted(slots.items()):
        if value == SENTINEL:
            continue
        if len({name for name, _ in claims}) > 1:
            where = "; ".join(f"{name} ({at})" for name, at in claims)
            problems.append(f"{kind} slot 0x{value:X} is claimed twice: {where}")

    if problems:
        print("Flag/var slot collision check FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print(
            f"\n{len(problems)} colliding slot(s). Two names for one bit means two "
            "unrelated events share state; move one of them to a free slot.",
            file=sys.stderr,
        )
        return 1

    literals = sum(len(v) for v in slots.values())
    print(f"Flag/var slot check passed: {literals} literal defines, no slot claimed twice")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Fail if any of the 386 creatures cannot be obtained.

Reads the encounter tables, the scripted gifts and the evolution table as they
stand and works out what a player can actually end up holding. A species that
lives only in the Battle Pyramid or the Battle Pike does not count: those are
wild battles you cannot catch in.

This guards a bug that is invisible until someone tries to finish the Pokedex:
Emerald's tables cover the Hoenn dex, Arauna has 386 species, and for a while
196 of them existed only in the data.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("build", ROOT / "tools/arauna/build_availability.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


PLAN = ROOT / "docs/arauna/ESPECIAIS_ESTATICOS.csv"


def planned() -> dict[int, str]:
    """The legendaries and mythicals that are deliberately out of the random
    tables, each with the placement it is waiting for.

    They are not a loophole: a special still has to be reachable OR be named
    here, so the hole stays exactly the size the file says it is, and closing
    one means deleting its line.
    """
    import csv
    if not PLAN.exists():
        return {}
    return {int(row["dex"]): row["placement"]
            for row in csv.DictReader(PLAN.open(encoding="utf-8"))}


def main() -> int:
    by_slot, by_dex = build.arauna()
    forward, _ = build.evolution_links(by_slot)
    data = json.loads(build.ENCOUNTERS.read_text(encoding="utf-8"))

    wild = build.caught_in_the_wild(data, by_slot)
    obtainable = build.reachable(wild | build.scripted(by_slot), forward)
    missing = sorted(set(by_dex) - obtainable)

    plan = planned()
    awaiting = [d for d in missing if d in plan]
    broken = [d for d in missing if d not in plan]

    if broken:
        names = ", ".join(f"#{d:03d} {by_dex[d]['name']}" for d in broken[:10])
        print(f"Arauna availability FAILED: {len(broken)} unobtainable -- {names}",
              file=sys.stderr)
        return 1
    print(f"Arauna availability: OK ({len(wild)} species catchable in the wild, "
          f"{len(obtainable)} of {len(by_dex)} obtainable counting evolution and gifts).")
    if awaiting:
        print(f"  {len(awaiting)} legendaries/mythicals are held back for a static "
              f"placement that does not exist yet, all named in {PLAN.name}:")
        for d in awaiting:
            print(f"    #{d:03d} {by_dex[d]['name']:14s} -> {plan[d]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

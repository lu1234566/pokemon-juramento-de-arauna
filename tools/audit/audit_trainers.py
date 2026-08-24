#!/usr/bin/env python3
"""Audit trainer parties for data that crashes or breaks a battle.

Looks for the failure modes that survive compilation: a party size that does
not match the declared mon list, levels outside 1-100, unknown species or
moves, duplicate/empty moveslots, and trainer names that overflow the name
buffer the game copies them into.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TRAINERS = ROOT / "src" / "data" / "trainers.h"
PARTIES = ROOT / "src" / "data" / "trainer_parties.h"
# Trainer names are copied into a fixed buffer; longer names truncate or spill.
TRAINER_NAME_LENGTH = 10


def constants(path: pathlib.Path, prefix: str) -> set[str]:
    text = (ROOT / path).read_text(encoding="utf-8")
    found = set(re.findall(rf"^#define\s+({prefix}[A-Z0-9_]+)", text, re.M))
    found |= set(re.findall(rf"\b({prefix}[A-Z0-9_]+)\s*=", text))
    return found


def main() -> int:
    text = TRAINERS.read_text(encoding="utf-8")
    species = constants(pathlib.Path("include/constants/species.h"), "SPECIES_")
    moves = constants(pathlib.Path("include/constants/moves.h"), "MOVE_")

    problems: list[str] = []
    blocks = re.findall(r"\[(TRAINER_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},", text, re.S)
    # Parties live in their own header and use several TrainerMon* structs.
    party_text = PARTIES.read_text(encoding="utf-8")
    parties = re.findall(
        r"static const struct TrainerMon\w* (\w+)\[\]\s*=\s*\{(.*?)\n\};", party_text, re.S
    )
    party_by_name = {name: body for name, body in parties}

    for name, body in party_by_name.items():
        mons = re.findall(r"\{(.*?)\n    \}", body, re.S)
        for i, mon in enumerate(mons):
            lvl = re.search(r"\.lvl\s*=\s*(\d+)", mon)
            if lvl and not (1 <= int(lvl.group(1)) <= 100):
                problems.append(f"{name}[{i}]: level {lvl.group(1)} outside 1-100")
            sp = re.search(r"\.species\s*=\s*(SPECIES_[A-Z0-9_]+)", mon)
            if sp and sp.group(1) not in species:
                problems.append(f"{name}[{i}]: unknown species {sp.group(1)}")
            if sp and sp.group(1) == "SPECIES_NONE":
                problems.append(f"{name}[{i}]: SPECIES_NONE in a party slot")
            listed = re.search(r"\.moves\s*=\s*\{(.*?)\}", mon, re.S)
            if listed:
                names = [m.strip() for m in listed.group(1).split(",") if m.strip()]
                unknown = [m for m in names if m not in moves]
                for m in unknown:
                    problems.append(f"{name}[{i}]: unknown move {m}")
                real = [m for m in names if m != "MOVE_NONE"]
                if not real:
                    problems.append(f"{name}[{i}]: no usable moves (Struggle-only)")
                if len(real) != len(set(real)):
                    problems.append(f"{name}[{i}]: duplicate moves {real}")

    for trainer, body in blocks:
        count = re.search(r"\.partySize\s*=\s*(\d+)", body)
        # .party = NO_ITEM_DEFAULT_MOVES(sParty_Foo) and friends.
        party = re.search(r"\.party\s*=\s*(?:\w+\()?(sParty_\w+)", body)
        if count and party and party.group(1) in party_by_name:
            declared = int(count.group(1))
            actual = len(re.findall(r"\{(.*?)\n    \}", party_by_name[party.group(1)], re.S))
            if declared != actual:
                problems.append(
                    f"{trainer}: partySize {declared} but {party.group(1)} has {actual} mon(s)"
                )
        tname = re.search(r'\.trainerName\s*=\s*_\("([^"]*)"\)', body)
        if tname and len(tname.group(1)) > TRAINER_NAME_LENGTH:
            problems.append(
                f"{trainer}: name {tname.group(1)!r} is {len(tname.group(1))} chars, "
                f"buffer holds {TRAINER_NAME_LENGTH}"
            )

    for line in problems:
        print(f"  - {line}")
    print(f"\n{len(problems)} trainer problem(s) across {len(blocks)} trainers, {len(party_by_name)} parties.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

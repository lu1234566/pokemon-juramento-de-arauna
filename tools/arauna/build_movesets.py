#!/usr/bin/env python3
"""Give every Arauna creature a moveset that suits it.

The move tables were never touched by the dex port, so each species still
learns whatever the Pokémon that used to occupy its engine slot learned.
#261 Curupira-Ancião, a folkloric grass creature, sits in SPECIES_POOCHYENA and
comes up through the game learning Bite, Howl and Crunch.

The fix reuses a table that already exists. docs/arauna/ARAUNA_PLACEMENT.csv was
built by pairing every vanilla species with the Arauna creature closest to it in
strength and type -- that is exactly the question "which vanilla Pokémon does
this creature resemble?", asked from the other end. Reading it backwards gives,
for each engine slot, the vanilla species whose moves fit the creature now
living there, and the four move tables are repointed accordingly:

  gLevelUpLearnsets     the level-up progression
  gTMHMLearnsets        which TMs and HMs it can be taught
  gTutorLearnsets       which move tutors will teach it
  gEggMoves             what it passes down

No move is invented and no learnset is edited; only which species points at
which existing list changes. Levels inside a learnset are left alone, so the
progression stays paced the way the vanilla game paced it.

The starter families and the script-named species are pinned in the placement,
so they keep their own movesets.

  --check   report what would change
  --write   repoint the four tables
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# The tree before the moveset pass landed; see committed().
BASELINE = "25bf1442"
PLACEMENT = ROOT / "docs/arauna/ARAUNA_PLACEMENT.csv"
LEVEL_UP = ROOT / "src/data/pokemon/level_up_learnset_pointers.h"
TMHM = ROOT / "src/data/pokemon/tmhm_learnsets.h"
TUTOR = ROOT / "src/data/pokemon/tutor_learnsets.h"
EGG = ROOT / "src/data/pokemon/egg_moves.h"


def committed(path: Path) -> str:
    """The file as it stood before this tool first wrote it.

    Not HEAD. This pass is a substitution, so running it against its own output
    moves everything a second time -- and once the output is committed, HEAD is
    the output. Pinning the baseline to the commit before the pass landed is what
    actually makes --write idempotent; reading HEAD only looked idempotent while
    the work was still uncommitted.
    """
    rel = path.relative_to(ROOT).as_posix()
    return subprocess.run(["git", "show", f"{BASELINE}:{rel}"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def resembles() -> dict[str, str]:
    """slot -> the vanilla species the creature in that slot resembles."""
    inverse = {}
    for row in csv.DictReader(PLACEMENT.open(encoding="utf-8")):
        inverse[row["now_holds_slot"]] = row["engine_slot"]
    return inverse


def repoint_pointers(text: str, inverse) -> tuple[str, int]:
    """gLevelUpLearnsets[SLOT] = <the resembled species' list>."""
    original = dict(re.findall(r"\[(SPECIES_\w+)\] = (\w+),", text))
    changed = 0

    def swap(match):
        nonlocal changed
        slot, current = match.group(1), match.group(2)
        like = inverse.get(slot)
        if like and like in original and original[like] != current:
            changed += 1
            return f"[{slot}] = {original[like]},"
        return match.group(0)

    return re.sub(r"\[(SPECIES_\w+)\] = (\w+),", swap, text), changed


def repoint_blocks(text: str, inverse, pattern: str) -> tuple[str, int]:
    """Move whole per-species initialisers around, keeping the slot label."""
    blocks = {m.group(1): m.group(2) for m in re.finditer(pattern, text, re.S)}
    changed = 0

    def swap(match):
        nonlocal changed
        slot = match.group(1)
        like = inverse.get(slot)
        if like and like in blocks and blocks[like] != match.group(2):
            changed += 1
            return match.group(0).replace(match.group(2), blocks[like], 1)
        return match.group(0)

    return re.sub(pattern, swap, text, flags=re.S), changed


def repoint_eggs(text: str, inverse) -> tuple[str, int]:
    """Rebuild gEggMoves so a slot carries the egg moves of what it resembles.

    Repointing in place is not enough here: a slot whose resembled species has
    no egg moves would otherwise keep the ones it inherited from the Pokémon
    that used to live there. The array is rebuilt instead, so a creature either
    has the right egg moves or none.
    """
    pattern = r"    egg_moves\((\w+),\n(.*?)\),\n"
    blocks = {f"SPECIES_{m.group(1)}": m.group(2) for m in re.finditer(pattern, text, re.S)}
    head = text[:text.index("const u16 gEggMoves[] = {")]

    emitted = []
    for slot, like in inverse.items():
        if like in blocks:
            emitted.append(f"    egg_moves({slot[len('SPECIES_'):]},\n{blocks[like]}),\n")
    body = "\n".join(emitted)
    return (f"{head}const u16 gEggMoves[] = {{\n{body}\n    EGG_MOVES_TERMINATOR\n}};\n",
            len(emitted))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    inverse = resembles()
    moved = sum(1 for slot, like in inverse.items() if slot != like)
    print(f"{len(inverse)} slots in the placement, {moved} of them holding a creature "
          f"that resembles a different species")

    level_up, n_level = repoint_pointers(committed(LEVEL_UP), inverse)
    tmhm, n_tm = repoint_blocks(committed(TMHM), inverse,
                                r"\[(SPECIES_\w+)\] = \{ \.learnset = \{(.*?)\}\s*\},")
    tutor, n_tutor = repoint_blocks(committed(TUTOR), inverse,
                                    r"\[(SPECIES_\w+)\]\s*= (\(TUTOR.*?\)),\n")
    eggs, n_egg = repoint_eggs(committed(EGG), inverse)

    print(f"  level-up progressions repointed: {n_level}")
    print(f"  TM/HM sets repointed:            {n_tm}")
    print(f"  tutor sets repointed:            {n_tutor}")
    print(f"  egg move lists rebuilt:          {n_egg}")

    if not args.write:
        return 0
    LEVEL_UP.write_text(level_up, encoding="utf-8")
    TMHM.write_text(tmhm, encoding="utf-8")
    TUTOR.write_text(tutor, encoding="utf-8")
    EGG.write_text(eggs, encoding="utf-8")
    print("wrote the four move tables")
    return 0


if __name__ == "__main__":
    sys.exit(main())

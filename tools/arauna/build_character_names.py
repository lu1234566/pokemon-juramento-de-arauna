#!/usr/bin/env python3
"""Make the dialogue call people what the battle calls them.

The story cast was renamed early on: the gym leader you fight in Pampa da
Espera is ELIAS, the one in Serra do Uivo is DALVA, the champion is AMALIA. The
dialogue around them was never told. An NPC says "the GYM LEADER, ROXANNE" and
three seconds later the battle nameplate reads DALVA -- the same contradiction
the place names had, on the same surfaces, and 408 times.

The mapping is not written here either. It is read out of src/data/trainers.h:
the name each TRAINER_ entry had in the reset-to-vanilla tree against the name
the story work gave it. That is measured at the commit *before* the bulk route
rename, so it catches the twenty names the project chose deliberately and not
the four hundred a generator handed out -- which matters, because those four
hundred include RED, LEAF and HOPE, and RED SHARD and LEAF STONE are not people.

Two adjustments, both visible in the CSV rather than buried:

  * a tag pair is one entry with one ten-character name, so TATE&LIZA became
    CEC&CAET; split in half and expanded to CECILIA and CAETANO, which is what
    the project's own writing already says;
  * GRUNT is skipped. It became AGENTE for one faction and ATIVISTA for the
    other, and which one a line means depends on who is speaking -- that is
    reading, not a table.

People the project never named are left alone and reported: RYDEL, LANETTE,
PROF. COZMO, CAPT. STERN, MR. BRINEY and the rest have no Arauna name to use.

Lines get longer, so run rewrap_text.py afterwards.

  --check   report what would be renamed
  --write   rewrite the text and the roster CSV
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rename import Renamer, count  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
VANILLA = "c210195e"
# The tree just before the bulk route rename: everything different from vanilla
# here was renamed on purpose, by hand, as part of the story.
STORY = "90491073^"
TRAINERS = "src/data/trainers.h"
ROSTER = ROOT / "docs/arauna/ARAUNA_CHARACTER_NAMES.csv"

# A pair shares one ten-character nameplate; the prose does not have to.
PROSE = {"CEC": "CECILIA", "CAET": "CAETANO"}

# One name means two different people depending on which faction is talking.
SKIP = {"GRUNT"}

# Named in the dialogue, never given an Arauna name. Reported, not renamed.
UNNAMED = ["RYDEL", "SCOTT", "CAPT. STERN", "MR. BRINEY", "PEEKO", "MR. STONE",
           "LANETTE", "COZMO", "WINSTRATE", "BILL", "SIDNEY", "PHOEBE",
           "GLACIA", "DRAKE"]

ENTRY = re.compile(r'\[(TRAINER_\w+)\] =\s*\{(.*?)\n    \},', re.S)
NAME = re.compile(r'\.trainerName = _\("([^"]*)"\)')


def at(revision: str) -> dict[str, str]:
    body = subprocess.run(["git", "show", f"{revision}:{TRAINERS}"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout
    out = {}
    for block in ENTRY.finditer(body):
        found = NAME.search(block.group(2))
        if found:
            out[block.group(1)] = found.group(1)
    return out


def cast() -> dict[str, str]:
    """Hoenn name -> Arauna name, from what the story work actually changed."""
    vanilla, story = at(VANILLA), at(STORY)
    mapping = {}
    for key, old in vanilla.items():
        new = story.get(key)
        if not old or not new or old == new:
            continue
        # "TATE&LIZA" -> "CEC&CAET" is two people sharing one nameplate.
        olds, news = old.split("&"), new.split("&")
        if len(olds) != len(news):
            continue
        for one_old, one_new in zip(olds, news):
            one_old, one_new = one_old.strip(), one_new.strip()
            if one_old and one_old not in SKIP:
                mapping[one_old] = PROSE.get(one_new, one_new)
    return mapping


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    mapping = cast()
    renamer = Renamer(mapping)
    changed = renamer.apply()
    renamer.report()
    print(f"  {len(changed)} files")

    left = count(UNNAMED)
    print("still Hoenn because the project never named them: "
          + ", ".join(f"{word} ({n})" for word, n in left.most_common()))

    if not args.write:
        return 0
    for path, updated in changed:
        path.write_text(updated, encoding="utf-8")
    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["hoenn_name", "arauna_name", "mentions", "source"])
        for hoenn, arauna in sorted(mapping.items()):
            writer.writerow([hoenn, arauna, renamer.hits.get(hoenn, 0),
                             "renamed in trainers.h by the story work"])
        for word in UNNAMED:
            writer.writerow([word, "", left.get(word, 0), "not named yet"])
    print(f"\nwrote {len(changed)} files and {ROSTER.relative_to(ROOT)}"
          "\nnow run rewrap_text.py --write: these lines are longer than they were")
    return 0


if __name__ == "__main__":
    sys.exit(main())

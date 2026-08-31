#!/usr/bin/env python3
"""Make the dialogue name the creature that is actually in the slot.

The dex was replaced species by species: the engine's SPECIES_SEEDOT now holds
an Arauna creature, and the Pokedex, the party screen and the battle all say so.
The text around them did not move. A boy in Aguas de M'Boi still measures his
LOTAD, the Trick House quiz still asks about a WAILMER, and the whole of Trainer
Hill fields Pokemon nicknamed MUK and UNOWN -- names of creatures that are not
in this game.

The mapping is the dex port's own: for each SPECIES_ constant, the name it had
before the port against the name it has now, read out of species_names.h. So it
renames a mention to whatever creature really occupies that slot, and it stays
right if the dex is regenerated.

Two things are deliberately left alone.

EGG is a species constant in the engine but never a creature in the text -- "an
EGG is asleep" is an egg.

The dolls are not renamed. There are thirty-five doll decorations, plus the
shops that sell them and the Dodrio berry-picking minigame, and all of that art
is still the vanilla Pokemon: the doll on the shelf is a Pikachu. Renaming the
label to an Arauna creature would make the mismatch worse, not better, because
you can see the doll. That one is waiting on art, not on a table.

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
from rename import Renamer  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
# The tree just before the Arauna dex landed, where the names are still Hoenn's.
VANILLA = "d4804fcc^"
SPECIES_NAMES = "src/data/text/species_names.h"
ROSTER = ROOT / "docs/arauna/ARAUNA_SPECIES_MENTIONS.csv"

NAMED = re.compile(r'\[(SPECIES_\w+)\]\s*=\s*_\("([^"]+)"\)')

# A species constant that is never a creature when the player reads it.
SKIP = {"SPECIES_NONE", "SPECIES_EGG"}

# Surfaces where the vanilla Pokemon is still drawn, so its name has to stay.
SHOWN_AS_VANILLA_ART = re.compile(r"DOLL|BERRY-PICKING")
DOLL_FILES = ("src/data/decoration/",
              "data/maps/BattleFrontier_ExchangeServiceCorner/")


def named(text: str) -> dict[str, str]:
    return {found.group(1): found.group(2) for found in NAMED.finditer(text)
            if found.group(1) not in SKIP and len(found.group(2)) > 2}


def slots() -> dict[str, str]:
    """Old name -> the name of whatever lives in that slot now."""
    before = named(subprocess.run(["git", "show", f"{VANILLA}:{SPECIES_NAMES}"],
                                  cwd=ROOT, capture_output=True, text=True,
                                  check=True).stdout)
    after = named((ROOT / SPECIES_NAMES).read_text(encoding="utf-8"))
    return {old: after[key] for key, old in before.items()
            if key in after and after[key] != old and "?" not in after[key]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    mapping = slots()
    renamer = Renamer(mapping,
                      keep=lambda text: not SHOWN_AS_VANILLA_ART.search(text))
    changed = [(path, body) for path, body in renamer.apply()
               if not str(path.relative_to(ROOT)).startswith(DOLL_FILES)]
    renamer.report()
    print(f"  {len(changed)} files, dolls and the berry-picking minigame left "
          f"to their vanilla art")

    if not args.write:
        return 0
    for path, updated in changed:
        path.write_text(updated, encoding="utf-8")
    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["hoenn_name", "arauna_name", "mentions"])
        for old, new in sorted(mapping.items()):
            if renamer.hits.get(old):
                writer.writerow([old, new, renamer.hits[old]])
    print(f"\nwrote {len(changed)} files and {ROSTER.relative_to(ROOT)}"
          "\nnow run rewrap_text.py --write: these lines are longer than they were")
    return 0


if __name__ == "__main__":
    sys.exit(main())

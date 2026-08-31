#!/usr/bin/env python3
"""Make the dialogue call places what the map calls them.

The region map was renamed a while ago: MAPSEC_SLATEPORT_CITY reads PORTO DO
SAL, MAPSEC_LILYCOVE_CITY reads BAIA DAS LUZES, and the story text the project
wrote uses those names throughout. The dialogue Emerald shipped did not follow.
A sailor still says he came from SLATEPORT while the town sign, the PokeNav and
the map all say PORTO DO SAL.

The mapping is not invented here. It is the difference between
region_map_sections.json now and at the reset-to-vanilla commit: whatever the
project decided a place is called, in the project's own file. Two adjustments
sit on top, both recorded in the CSV rather than hidden in code:

  * where prose already uses a longer form than the fourteen characters the map
    label allows -- MEMORIAL DOS NOMES against the map's MEMORIAL NOMES -- the
    prose wins, because it is what the rest of the writing already says;
  * HOENN is the region, which has no map section, and the project already
    calls it ARAUNA in the text it wrote.

Anything with a map section is named there and read from there, so the map and
the dialogue cannot drift apart; EXTRA below is only for named things that have
no section of their own, like the company and the ferry. What is left in
UNDECIDED is left on purpose: the BATTLE FRONTIER is already BATTLE CIRCUIT in
the English renderers and renaming it belongs with them, and the event islands
are never spoken of.

Generic descriptors are not names and are not touched. UNDERWATER, SECRET BASE
and INSIDE OF TRUCK stay as they are, the way a real map keeps "Rio de Janeiro"
and "the harbour" in different languages.

Replacement happens only inside strings the player reads, and CITY and TOWN go
with the name they belong to: "SLATEPORT CITY" is one place, not a place and a
word. Lines get longer, so run rewrap_text.py afterwards -- check_text_width.py
fails loudly if anyone forgets, for the message box and for the much narrower
description box in the bag.

  --check   report what would change
  --write   rewrite the scripts and the CSV
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rename import STRING, Renamer, count  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
VANILLA = "c210195e"
REGION_MAP = "src/data/region_map/region_map_sections.json"
ROSTER = ROOT / "docs/arauna/ARAUNA_PLACE_NAMES.csv"

# The map label is capped at fourteen characters; prose is not. Where the
# project's own writing already says something longer, that is the real name.
PROSE = {"MEMORIAL NOMES": "MEMORIAL DOS NOMES"}

# Named things with no map section of their own. Everything that has one is
# named there instead, so the map and the dialogue cannot drift apart.
#
# DEVON is the awkward one. The company was already CONSORCIO HORIZONTE in
# three lines and DEVON everywhere else; the short form the writing uses for it
# is HORIZONTE. Its two items cannot carry that -- an item name is thirteen
# characters -- so they are named for what they are: the package the plot is
# about, and the lens that shows what is hiding.
EXTRA = {
    "HOENN": "ARAUNA",              # the region; the text already says ARAUNA
    "DEVON GOODS": "ENCOMENDA",
    "DEVON SCOPE": "VISOR VERDADE",
    "DEVON CORPORATION": "CONSORCIO HORIZONTE",
    "DEVON CORP": "CONSORCIO HORIZONTE",
    "DEVON": "HORIZONTE",
    "TRICK HOUSE": "CASA DOS TRUQUES",
    "S.S. TIDAL": "MARE ALTA",      # the vessel; the service is the LINE FERRY
    "SAFARI ZONE ENTRANCE": "ENTRADA DA RESERVA",
    # Two half-renames from the pass that named the towns: PETALBURG WOODS and
    # NEW MAUVILLE had no name of their own then, so only the town inside them
    # changed and they came out as a town's name with an English word stuck to
    # it. Now that they are named, these are the forms to repair.
    "PAMPA DA ESPERA WOODS": "MATA DA ESPERA",
    "NEW ENCRUZILHADA": "USINA VELHA",
}

# Hoenn names the project has not decided on. Left alone, and reported.
UNDECIDED = ["BATTLE FRONTIER", "TRAINER HILL", "NAVEL ROCK", "BIRTH ISLAND",
             "FARAWAY ISLAND", "ALTERING CAVE"]

def at_vanilla(path: str) -> str:
    return subprocess.run(["git", "show", f"{VANILLA}:{path}"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def renames() -> dict[str, str]:
    """Hoenn name -> Arauna name, from the project's own region map."""
    def sections(text):
        return {s["id"]: s["name"] for s in json.loads(text)["map_sections"]}

    before = sections(at_vanilla(REGION_MAP))
    after = sections((ROOT / REGION_MAP).read_text(encoding="utf-8"))
    out = dict(EXTRA)
    for key, new in after.items():
        old = before.get(key)
        if old and new and old != new and old.isascii() and "{" not in old:
            out[old] = PROSE.get(new, new)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    mapping = renames()
    # "SLATEPORT CITY" is one place. Without this the CITY would survive the
    # rename and the line would read "PORTO DO SAL CITY".
    for hoenn, arauna in list(mapping.items()):
        for suffix in (" CITY", " TOWN"):
            if hoenn.endswith(suffix):
                mapping[hoenn[:-len(suffix)]] = arauna
    renamer = Renamer(mapping)
    changed = renamer.apply()
    renamer.report()
    print(f"  {len(changed)} files")

    left = count(UNDECIDED)
    print("still Hoenn because the project has not named them: "
          + ", ".join(f"{word} ({n})" for word, n in left.most_common()))

    if not args.write:
        return 0

    for path, updated in changed:
        path.write_text(updated, encoding="utf-8")
    hits = renamer.hits
    with ROSTER.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["hoenn_name", "arauna_name", "mentions", "source"])
        for hoenn, arauna in sorted(mapping.items()):
            source = ("region map" if hoenn not in EXTRA else "already used in the text")
            writer.writerow([hoenn, arauna, hits.get(hoenn, 0), source])
        for word in UNDECIDED:
            writer.writerow([word, "", left.get(word, 0), "not named yet"])
    print(f"\nwrote {len(changed)} files and {ROSTER.relative_to(ROOT)}"
          "\nnow run rewrap_text.py --write: these lines are longer than they were")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate that Arauna's English-first runtime has no Portuguese fallback text."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PORTUGUESE_RUNTIME_WORDS = re.compile(
    r"\b(?:uma|para|com|sem|não|você|ainda|agora|depois|vive|espírito|"
    r"região|filhote|guardião|treinador|lendas|floresta|serra)\b",
    re.IGNORECASE,
)

OBSOLETE_PLACEHOLDERS = re.compile(
    r"\b(?:technical placeholder|official POKéMON placeholders|temporary TREECKO|"
    r"the POOCHYENA)\b",
    re.IGNORECASE,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("docs/arauna/source/pokedex.json"))
    parser.add_argument("--localization", type=Path, default=Path("docs/arauna/source/pokedex.en.json"))
    parser.add_argument("--header", type=Path, default=Path("src/data/pokemon/species_info/arauna_dex.h"))
    parser.add_argument("--text-dir", type=Path, default=Path("data/text/arauna/en"))
    parser.add_argument("--event-scripts", type=Path, default=Path("data/event_scripts.s"))
    parser.add_argument("--story-roles", type=Path, default=Path("docs/arauna/source/story_roles.json"))
    args = parser.parse_args()

    source = json.loads(args.source.read_text(encoding="utf-8"))["pokemon"]
    localized_data = json.loads(args.localization.read_text(encoding="utf-8"))
    localized = localized_data["pokemon"]
    if localized_data.get("language") != "en":
        raise ValueError("runtime localization is not marked as English")
    if len(source) != 386 or len(localized) != 386:
        raise ValueError("source and English localization must both contain 386 entries")
    if [entry["id"] for entry in localized] != list(range(1, 387)):
        raise ValueError("English localization IDs are not consecutive")

    source_names = {int(entry["id"]): entry["name"] for entry in source}
    for entry in localized:
        if not entry["category"] or len(entry["category"]) > 12:
            raise ValueError(f"invalid category for #{entry['id']:03d}")
        player_text = f"{entry['category']} {entry['region']} {entry['dex']}"
        player_text = player_text.replace(source_names[int(entry["id"])], "")
        if PORTUGUESE_RUNTIME_WORDS.search(player_text):
            raise ValueError(f"Portuguese runtime text remains in #{entry['id']:03d}: {player_text}")

    header = args.header.read_text(encoding="utf-8")
    if header.count('.categoryName = _("') != 386:
        raise ValueError("generated header does not contain 386 categories")
    if header.count(".description = COMPOUND_STRING(") != 386:
        raise ValueError("generated header does not contain 386 descriptions")
    for entry in localized:
        if f'.categoryName = _("{entry["category"]}"),' not in header:
            raise ValueError(f"generated category missing for #{entry['id']:03d}")

    roles = json.loads(args.story_roles.read_text(encoding="utf-8"))
    non_capturable = {int(entry["id"]) for entry in roles["nonCapturable"]}
    _, *blocks = re.split(r"(?=    \[SPECIES_)", header)
    for species_id in non_capturable:
        if ".catchRate = 0," not in blocks[species_id - 1]:
            raise ValueError(f"non-capturable Census entry #{species_id:03d} has a usable catch rate")

    required_story_files = ("birch_speech.inc", "map_lab.inc", "opening.inc", "route.inc", "ruin.inc", "chamber.inc")
    story = "\n".join((args.text_dir / name).read_text(encoding="utf-8") for name in required_story_files)
    if OBSOLETE_PLACEHOLDERS.search(story):
        raise ValueError("obsolete placeholder text remains in the English story")
    if PORTUGUESE_RUNTIME_WORDS.search(story):
        raise ValueError("Portuguese prose remains in the English story")

    event_scripts = args.event_scripts.read_text(encoding="utf-8")
    wrappers = ("birch_speech", "arauna/map_lab", "arauna/opening", "arauna/route", "arauna/ruin", "arauna/chamber")
    for wrapper in wrappers:
        directive = f'#include "data/text/{wrapper}.inc"'
        if directive not in event_scripts:
            raise ValueError(f"language wrapper must be selected by CPP: {directive}")

    print("English runtime validated: 386 Dex entries and 6 story packs")


if __name__ == "__main__":
    main()

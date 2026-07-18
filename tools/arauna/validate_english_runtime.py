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

    required_story_files = ("birch_speech.inc", "map_lab.inc", "opening.inc", "route.inc", "ruin.inc", "chamber.inc", "porto_das_redes.inc", "serra_do_uivo.inc", "second_rom_test.inc")
    story = "\n".join((args.text_dir / name).read_text(encoding="utf-8") for name in required_story_files)
    if OBSOLETE_PLACEHOLDERS.search(story):
        raise ValueError("obsolete placeholder text remains in the English story")
    story_prose = story.replace("SERRA DO UIVO", "")
    portuguese_match = PORTUGUESE_RUNTIME_WORDS.search(story_prose)
    if portuguese_match:
        raise ValueError(
            f"Portuguese prose remains in the English story: {portuguese_match.group(0)}"
        )
    unsupported_story_chars = sorted({char for char in story if ord(char) > 127 and char != "é"})
    if unsupported_story_chars:
        rendered = " ".join(f"U+{ord(char):04X}" for char in unsupported_story_chars)
        raise ValueError(f"unsupported non-ASCII characters remain in the English story: {rendered}")

    makefile = Path("Makefile").read_text(encoding="utf-8")
    required_build_contract = (
        "ARAUNA_LANGUAGE ?= ENGLISH",
        "supports only ARAUNA_LANGUAGE=ENGLISH",
        "ARAUNA_LANGUAGE_ID := 0",
        "ARAUNA_LANGUAGE_SUFFIX := en",
        "BUILD_NAME := $(BUILD_NAME)-$(ARAUNA_LANGUAGE_SUFFIX)",
        "-DARAUNA_LANGUAGE=$(ARAUNA_LANGUAGE_ID)",
    )
    for token in required_build_contract:
        if token not in makefile:
            raise ValueError(f"English-only build contract is missing: {token}")

    event_scripts = args.event_scripts.read_text(encoding="utf-8")
    wrappers = ("birch_speech", "arauna/map_lab", "arauna/opening", "arauna/route", "arauna/ruin", "arauna/chamber", "arauna/porto_das_redes", "arauna/serra_do_uivo", "arauna/second_rom_test")
    for wrapper in wrappers:
        directive = f'#include "data/text/{wrapper}.inc"'
        if directive not in event_scripts:
            raise ValueError(f"language wrapper must be selected by CPP: {directive}")

    print("English runtime validated: fixed -en build, 386 Dex entries and 9 story packs")


if __name__ == "__main__":
    main()

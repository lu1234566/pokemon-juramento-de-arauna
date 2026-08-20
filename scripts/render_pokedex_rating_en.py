#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "text" / "pokedex_rating.inc"
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")

BLOCKS: dict[str, tuple[str, ...]] = {
    "gBirchDexRatingText_AreYouCurious": (
        "ANAHI: {PLAYER}, want to check\\n", "your POKéDEX progress?$"),
    "gBirchDexRatingText_Cancel": (
        "Not enough records yet\\n", "for a full evaluation.$"),
    "gBirchDexRatingText_SoYouveSeenAndCaught": (
        "Let's see...\\p", "You saw {STR_VAR_1} POKéMON and\\n", "caught {STR_VAR_2} POKéMON.$"),
    "gBirchDexRatingText_LessThan10": (
        "Explore more grassy areas.\\n", "Watch closely.$"),
    "gBirchDexRatingText_LessThan20": (
        "You're getting the hang of it.\\n", "Now it gets harder.$"),
    "gBirchDexRatingText_LessThan30": (
        "Some POKéMON appear only\\n", "in certain places.\\l", "Keep looking.$"),
    "gBirchDexRatingText_LessThan40": (
        "Many records are still missing,\\n", "but your POKéDEX takes shape.$"),
    "gBirchDexRatingText_LessThan50": (
        "The work is moving well.\\n", "Keep this pace.$"),
    "gBirchDexRatingText_LessThan60": (
        "Have you tried fishing RODS?\\n", "Many POKéMON live in water.$"),
    "gBirchDexRatingText_LessThan70": (
        "Do not focus only on catching.\\n", "Some POKéMON can evolve.$"),
    "gBirchDexRatingText_LessThan80": (
        "This POKéDEX could become\\n", "a fine record of ARAUNA.$"),
    "gBirchDexRatingText_LessThan90": (
        "You gathered many records.\\n", "Your work is impressive!$"),
    "gBirchDexRatingText_LessThan100": (
        "Visited the SAFARI ZONE?\\p", "Some POKéMON are found\\n", "only there.$"),
    "gBirchDexRatingText_LessThan110": (
        "You passed one hundred records.\\p", "That is an impressive POKéDEX!$"),
    "gBirchDexRatingText_LessThan120": (
        "Some POKéMON may appear\\n", "when you use ROCK SMASH.$"),
    "gBirchDexRatingText_LessThan130": (
        "Trading with other people\\n", "can expand your records.$"),
    "gBirchDexRatingText_LessThan140": (
        "Some POKéMON evolve after\\n", "forming a strong BOND\\l", "with their TRAINER.$"),
    "gBirchDexRatingText_LessThan150": (
        "ARAUNA holds more species\\n", "than I first imagined.$"),
    "gBirchDexRatingText_LessThan160": (
        "Some species appear in groups.\\p", "Do not miss those chances.$"),
    "gBirchDexRatingText_LessThan170": (
        "Your POKéDEX now shows\\n", "ARAUNA's diversity well.$"),
    "gBirchDexRatingText_LessThan180": (
        "Your work has reached\\n", "a researcher's level.$"),
    "gBirchDexRatingText_LessThan190": (
        "This POKéDEX needs method,\\n", "patience and experience.$"),
    "gBirchDexRatingText_LessThan200": (
        "Very little remains.\\n", "Keep going!$"),
    "gBirchDexRatingText_DexCompleted": (
        "Congratulations!\\n", "ARAUNA POKéDEX complete!$"),
    "gBirchDexRatingText_OnANationwideBasis": (
        "Now, looking at all the data...\\p", "You saw {STR_VAR_1} POKéMON and\\n", "caught {STR_VAR_2} POKéMON.$"),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::\n(?P<body>.*?)(?=^[A-Za-z0-9_]+::(?:\n|$)|\Z)"
    )


def validate_widths() -> None:
    for label, lines in BLOCKS.items():
        for line in lines:
            clean = PH.sub("PLAYER", line.replace("$", ""))
            for segment in CTRL.split(clean):
                segment = segment.strip()
                if len(segment) > MAX:
                    raise ValueError(f"{label}: {len(segment)} chars: {segment!r}")


def mask(text: str) -> str:
    out = text
    for label in BLOCKS:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing rating block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render(source: str) -> str:
    out = source
    for label, lines in BLOCKS.items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected 1 block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        out = out[:start] + body + out[end:]
    if mask(source) != mask(out):
        raise ValueError("non-rating structure changed")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")
    validate_widths()
    source = TARGET.read_text(encoding="utf-8")
    output = render(source)
    if args.in_place and output != source:
        TARGET.write_text(output, encoding="utf-8")
    print(f"Anahi Pokedex rating English overlay OK: {len(BLOCKS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

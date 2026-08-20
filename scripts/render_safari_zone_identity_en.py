#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "scripts" / "safari_zone.inc"
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")

BLOCKS: dict[str, tuple[str, ...]] = {
    "Route121_SafariZoneEntrance_Text_WelcomeToSafariZone": (
        "Welcome to the SAFARI ZONE!\\p",
        "Here you may see POKéMON\\n",
        "rarely found in ARAUNA.\\p",
        "They live in open habitats\\n",
        "with little interference.\\p",
        "TRAINERS may enter and catch\\n",
        "POKéMON during the SAFARI Game.\\p",
        "Come in and explore!$",
    ),
    "Route121_SafariZoneEntrance_Text_YouNeedPokeblockCase": (
        "Excuse me!\\p",
        "You don't have a {POKEBLOCK} CASE.\\p",
        "Your SAFARI Game works better\\n",
        "if you can use {POKEBLOCK}S.\\p",
        "You can get a {POKEBLOCK} CASE\\n",
        "in BAIA DAS LUZES.$",
    ),
    "SafariZone_North_Text_Fisherman": (
        "I'm looking for WATER POKéMON\\n",
        "rarely seen elsewhere in ARAUNA.\\p",
        "Do you know where the lake is?$",
    ),
    "SafariZone_Southeast_Text_RichBoy": (
        "The POKéMON in this area seem\\n",
        "to come from beyond ARAUNA.$",
    ),
}

PRESERVED = (
    "VAR_SAFARI_ZONE_STATE",
    "MAP_ROUTE121_SAFARI_ZONE_ENTRANCE",
    "ITEM_POKEBLOCK_CASE",
    "FLAG_SYS_SAFARI_MODE",
    "SafariZone_EventScript_Exit",
)


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def validate_widths() -> None:
    for label, lines in BLOCKS.items():
        for line in lines:
            visible = PH.sub("POKEBLOCK", line.replace("$", ""))
            for segment in CTRL.split(visible):
                if len(segment.strip()) > MAX:
                    raise ValueError(f"{label}: over-width segment: {segment.strip()!r}")


def mask(text: str) -> str:
    out = text
    for label in BLOCKS:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing Safari Zone block: {label}")
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
        raise ValueError("Safari Zone non-dialogue structure changed")
    for token in PRESERVED:
        if token not in out:
            raise ValueError(f"missing preserved Safari Zone token: {token}")
    for forbidden in ("HOENN", "LILYCOVE CONTEST HALL"):
        for label in BLOCKS:
            match = pattern(label).search(out)
            if match and forbidden in match.group("body"):
                raise ValueError(f"legacy Safari Zone identity survived: {forbidden}")
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
    print(f"Safari Zone Arauna identity OK: {len(BLOCKS)} visible blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

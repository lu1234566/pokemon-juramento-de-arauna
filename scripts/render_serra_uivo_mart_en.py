#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "RustboroCity_Mart" / "scripts.inc"
MAX = 32
CTRL = re.compile(r"\\[npl]")

BLOCKS: dict[str, tuple[str, ...]] = {
    "RustboroCity_Mart_Text_BuyingHealsInCaseOfShroomish": (
        "I'm taking PARLYZ HEAL and\\n",
        "ANTIDOTE.\\p",
        "The nearby woods have POKéMON\\n",
        "that can cause trouble.$",
    ),
    "RustboroCity_Mart_Text_ShouldBuySuperPotionsInstead": (
        "My POKéMON evolved.\\n",
        "Now it has much more HP.\\p",
        "I'll buy SUPER POTIONS\\n",
        "instead of regular POTIONS.$",
    ),
    "RustboroCity_Mart_Text_GettingEscapeRopeJustInCase": (
        "I'll take an ESCAPE ROPE\\n",
        "in case I get lost in a cave.\\p",
        "It can take me back to the\\n",
        "entrance when I need it.$",
    ),
}

PRESERVED = (
    "FLAG_MET_DEVON_EMPLOYEE",
    "RustboroCity_Mart_Pokemart_Basic",
    "RustboroCity_Mart_Pokemart_Expanded",
    "ITEM_TIMER_BALL",
    "ITEM_REPEAT_BALL",
)


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def validate_widths() -> None:
    for label, lines in BLOCKS.items():
        for line in lines:
            for segment in CTRL.split(line.replace("$", "")):
                if len(segment.strip()) > MAX:
                    raise ValueError(f"{label}: over-width segment: {segment.strip()!r}")


def mask(text: str) -> str:
    out = text
    for label in BLOCKS:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing Mart block: {label}")
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
        raise ValueError("Mart non-dialogue structure changed")
    for token in PRESERVED:
        if token not in out:
            raise ValueError(f"missing preserved Mart token: {token}")
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
    print(f"Serra do Uivo Mart English overlay OK: {len(BLOCKS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

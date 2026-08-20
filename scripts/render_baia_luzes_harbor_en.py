#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "LilycoveCity_Harbor" / "scripts.inc"
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")

BLOCKS: dict[str, tuple[str, ...]] = {
    "LilycoveCity_Harbor_Text_FerryUnavailable": (
        "ATTENDANT: Looking for a ship?\\p",
        "Sorry, the LINE FERRY is not\\n",
        "operating yet.$",
    ),
    "LilycoveCity_Harbor_Text_MayISeeYourTicket": (
        "ATTENDANT: May I see your\\n",
        "TICKET?$",
    ),
    "LilycoveCity_Harbor_Text_NoTicket": (
        "{PLAYER} doesn't have a TICKET.\\p",
        "ATTENDANT: You need one\\n",
        "before you can board.$",
    ),
    "LilycoveCity_Harbor_Text_FlashTicketWhereTo": (
        "{PLAYER} showed the TICKET.\\p",
        "ATTENDANT: Perfect.\\n",
        "Where would you like to go?$",
    ),
    "LilycoveCity_Harbor_Text_SailAnotherTime": (
        "ATTENDANT: Travel with us\\n",
        "anytime.$",
    ),
    "LilycoveCity_Harbor_Text_SlateportItIs": (
        "ATTENDANT: PORTO DO SAL,\\n",
        "right?$",
    ),
    "LilycoveCity_Harbor_Text_BattleFrontierItIs": (
        "ATTENDANT: CIRCUITO DE\\n",
        "BATALHA, right?$",
    ),
    "LilycoveCity_Harbor_Text_PleaseBoard": (
        "ATTENDANT: Board the LINE FERRY\\n",
        "and wait for departure.$",
    ),
    "LilycoveCity_Harbor_Text_WhereWouldYouLikeToGo": (
        "ATTENDANT: Where would you like\\n",
        "to go?$",
    ),
    "LilycoveCity_Harbor_Text_SailorFerryUnavailable": (
        "SAILOR: The LINE FERRY is still\\n",
        "being finished in PORTO DO SAL.\\p",
        "Until then, there isn't much\\n",
        "work for us here.$",
    ),
    "LilycoveCity_Harbor_Text_SailorFerryAvailable": (
        "SAILOR: The LINE FERRY is finally\\n",
        "running.\\p",
        "The PORTO DO SAL SHIPYARD worked\\n",
        "hard to finish it.\\p",
        "Now it's our turn to work.$",
    ),
}

PRESERVED = (
    "VAR_SS_TIDAL_STATE",
    "MAP_BATTLE_FRONTIER_OUTSIDE_WEST",
    "FLAG_SYS_GAME_CLEAR",
    "LOCALID_LILYCOVE_HARBOR_SS_TIDAL",
    "LilycoveCity_Harbor_EventScript_GoToBattleFrontier",
)


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
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
            raise ValueError(f"missing harbor block: {label}")
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
        raise ValueError("Baia das Luzes harbor non-dialogue structure changed")
    for token in PRESERVED:
        if token not in out:
            raise ValueError(f"missing preserved harbor token: {token}")
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
    print(f"Baia das Luzes harbor English overlay OK: {len(BLOCKS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

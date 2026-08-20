#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")
TARGETS: dict[str, dict[str, tuple[str, ...]]] = {
    "data/maps/FallarborTown_BattleTentLobby/scripts.inc": {
        "FallarborTown_BattleTentLobby_Text_FallarborTentMyFavorite": (
            "You know how BATTLE TENTS offer\\n",
            "different events in each town?\\p",
            "My favorite is the one in\\n",
            "CAMPO DAS CINZAS.\\p",
            "TRAINERS there put real faith\\n",
            "in their POKéMON.$",
        ),
        "FallarborTown_BattleTentLobby_Text_ScottLookingForSomeone": (
            "SEU BENTO: {PLAYER}, I thought\\n",
            "you might stop here.\\p",
            "People in CAMPO DAS CINZAS\\n",
            "battle at their own pace.\\p",
            "I like seeing how TRAINERS\\n",
            "adapt under pressure.$",
        ),
        "FallarborTown_BattleTentLobby_Text_ScottMakeChallenge": (
            "SEU BENTO: Don't spend the day\\n",
            "talking to me.\\p",
            "Try the challenge.\\n",
            "See what your habits reveal.$",
        ),
    },
    "data/maps/VerdanturfTown_BattleTentLobby/scripts.inc": {
        "VerdanturfTown_BattleTentLobby_Text_ScottCanMeetToughTrainers": (
            "SEU BENTO: {PLAYER}, here too?\\p",
            "This BATTLE TENT draws TRAINERS\\n",
            "who trust their POKéMON's nature.\\p",
            "Watch what they do without\\n",
            "direct commands.$",
        ),
        "VerdanturfTown_BattleTentLobby_Text_ScottVisitRegularly": (
            "SEU BENTO: I return often.\\p",
            "Different rules reveal different\\n",
            "parts of a TRAINER.\\p",
            "That's worth observing.$",
        ),
    },
}

PRESERVED = {
    "data/maps/FallarborTown_BattleTentLobby/scripts.inc": (
        "FLAG_MET_SCOTT_IN_FALLARBOR",
        "VAR_SCOTT_STATE",
        "FRONTIER_FACILITY_ARENA",
        "fallarbortent_save",
    ),
    "data/maps/VerdanturfTown_BattleTentLobby/scripts.inc": (
        "FLAG_MET_SCOTT_IN_VERDANTURF",
        "VAR_SCOTT_STATE",
        "FRONTIER_FACILITY_PALACE",
        "verdanturftent_save",
    ),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def validate_widths() -> None:
    for rel, blocks in TARGETS.items():
        for label, lines in blocks.items():
            for line in lines:
                clean = PH.sub("PLAYER", line.replace("$", ""))
                for segment in CTRL.split(clean):
                    segment = segment.strip()
                    if len(segment) > MAX:
                        raise ValueError(
                            f"{rel}: {label}: {len(segment)} chars: {segment!r}"
                        )


def mask(text: str, labels: tuple[str, ...]) -> str:
    out = text
    for label in labels:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing Battle Tent block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render(rel: str, source: str) -> str:
    out = source
    labels = tuple(TARGETS[rel])
    for label, lines in TARGETS[rel].items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{rel}: {label}: expected one block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        out = out[:start] + body + out[end:]

    if mask(source, labels) != mask(out, labels):
        raise ValueError(f"{rel}: non-text structure changed")
    for token in PRESERVED[rel]:
        if token not in out:
            raise ValueError(f"{rel}: preserved Battle Tent token disappeared: {token}")

    for forbidden in ("SCOTT:", "FALLARBOR TOWN", "VERDANTURF TOWN"):
        for label in labels:
            match = pattern(label).search(out)
            if match and forbidden in match.group("body"):
                raise ValueError(f"{rel}: legacy Battle Tent identity survived: {forbidden}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")

    validate_widths()
    changed = 0
    total = sum(len(v) for v in TARGETS.values())
    for rel in TARGETS:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        output = render(rel, source)
        if output != source:
            changed += 1
            if args.in_place:
                path.write_text(output, encoding="utf-8")

    print(
        f"Battle Tent Arauna identity OK: {total} blocks across "
        f"{len(TARGETS)} lobbies; {changed} changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
    "data/maps/Route115/scripts.inc": {
        "Route115_Text_RouteSignRustboro": (
            "ROUTE 115\\n",
            "{DOWN_ARROW} SERRA DO UIVO$",
        ),
        "Route115_Text_MeteorFallsSign": (
            "RUINAS DA QUEDA\\n",
            "CAMPO DAS CINZAS THIS WAY$",
        ),
    },
    "data/maps/SlateportCity_House/scripts.inc": {
        "SlateportCity_House_Text_MustBeGoingToBattleTent": (
            "You're a TRAINER, aren't you?\\p",
            "Since you came to PORTO DO SAL,\\n",
            "you must be visiting the\\n",
            "BATTLE TENT.$",
        ),
    },
    "data/maps/Route110_TrickHousePuzzle5/scripts.inc": {
        "Route110_TrickHousePuzzle5_Text_Mechadoll4Quiz2": (
            "MECHADOLL 4 QUIZ.\\p",
            "In SERTAO DE DENTRO, were\\n",
            "there more elderly men or\\n",
            "elderly women?$",
        ),
        "Route110_TrickHousePuzzle5_Text_Mechadoll5Quiz1": (
            "MECHADOLL 5 QUIZ.\\p",
            "In PORTO DO SAL's POKéMON\\n",
            "FAN CLUB, how many POKéMON\\n",
            "were there?$",
        ),
        "Route110_TrickHousePuzzle5_Text_Mechadoll5Quiz2": (
            "MECHADOLL 5 QUIZ.\\p",
            "In MATA DO MEIO, how many\\n",
            "tree houses were there?$",
        ),
    },
}

PRESERVED = {
    "data/maps/Route115/scripts.inc": (
        "VAR_ABNORMAL_WEATHER_LOCATION",
        "TRAINER_TIMOTHY_1",
        "Route115_EventScript_MeteorFallsSign",
    ),
    "data/maps/SlateportCity_House/scripts.inc": (
        "SlateportCity_House_EventScript_PokefanM",
        "SlateportCity_House_EventScript_Girl",
    ),
    "data/maps/Route110_TrickHousePuzzle5/scripts.inc": (
        "VAR_TRICK_HOUSE_PUZZLE_5_STATE",
        "MULTI_MECHADOLL4_Q2",
        "MULTI_MECHADOLL5_Q1",
        "MULTI_MECHADOLL5_Q2",
        "Route110_TrickHousePuzzle5_EventScript_Mechadoll4Quiz2",
    ),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(line: str) -> list[str]:
    clean = PH.sub("PLAYER", line.replace("$", ""))
    return [part.strip() for part in CTRL.split(clean)]


def validate_widths() -> None:
    for rel, blocks in TARGETS.items():
        for label, lines in blocks.items():
            for line in lines:
                for segment in visible_segments(line):
                    if len(segment) > MAX:
                        raise ValueError(
                            f"{rel}: {label}: {len(segment)} chars: {segment!r}"
                        )


def mask(text: str, labels: tuple[str, ...]) -> str:
    out = text
    for label in labels:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing visible block: {label}")
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
            raise ValueError(f"{rel}: preserved token disappeared: {token}")
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
        f"Route/service residue English overlay OK: {total} blocks across "
        f"{len(TARGETS)} files; {changed} changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

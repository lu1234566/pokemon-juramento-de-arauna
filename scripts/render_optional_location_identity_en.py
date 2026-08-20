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
    "data/maps/SootopolisCity_House7/scripts.inc": {
        "SootopolisCity_House7_Text_CityFromEruptedVolcano": (
            "An underwater volcano erupted\\n",
            "and rose from the depths.\\p",
            "Its crater broke the sea surface\\n",
            "and filled with rainwater.\\p",
            "That's how AGUAS DE M'BOI\\n",
            "came into being.$",
        ),
        "SootopolisCity_House7_Text_CaveMadeToKeepSomething": (
            "The cave linking AGUAS DE M'BOI\\n",
            "to the outside world...\\p",
            "It feels as if it was made to\\n",
            "keep something from getting out.\\p",
            "Or am I imagining things?$",
        ),
    },
    "data/maps/PacifidlogTown_PokemonCenter_1F/scripts.inc": {
        "PacifidlogTown_PokemonCenter_1F_Text_OnColonyOfCorsola": (
            "CASA DA FOGUEIRA floats over\\n",
            "a colony of CORSOLA.\\p",
            "If I told you that, would you\\n",
            "believe me?$",
        ),
        "PacifidlogTown_PokemonCenter_1F_Text_AncestorsLivedOnBoats": (
            "The ancestors of the people in\\n",
            "CASA DA FOGUEIRA were said\\n",
            "to be born on boats.\\p",
            "They lived and died aboard them,\\n",
            "searching for something.$",
        ),
    },
    "data/maps/VerdanturfTown_House/scripts.inc": {
        "VerdanturfTown_House_Text_TrainersGatherAtPokemonLeague": (
            "Far away, beyond the eastern sea,\\n",
            "is ESTRADA DO JURAMENTO.\\p",
            "The TRAINERS who gather there\\n",
            "are frighteningly skilled.$",
        ),
    },
    "data/scripts/gift_trainer.inc": {
        "sText_MysteryGiftVisitingTrainerInstructions": (
            "Thank you for using the MYSTERY\\n",
            "GIFT System.\\p",
            "By holding this WONDER CARD, you\\n",
            "may take part in a survey at a\\n",
            "POKéMON MART.\\p",
            "Use these surveys to invite\\n",
            "TRAINERS to AGUAS DE M'BOI.\\p",
            "Let me give you a secret\\n",
            "password for a survey:\\p",
            "“GIVE ME\\n",
            "AWESOME TRAINER”\\p",
            "Write that in on a survey and\\n",
            "send it through the WIRELESS\\n",
            "COMMUNICATION SYSTEM.$",
        ),
        "sText_MysteryGiftVisitingTrainerArrived": (
            "Thank you for using the MYSTERY\\n",
            "GIFT System.\\p",
            "A TRAINER has arrived in\\n",
            "AGUAS DE M'BOI looking for you.\\p",
            "We hope you enjoy battling\\n",
            "the visiting TRAINER.\\p",
            "You may invite other TRAINERS\\n",
            "with other passwords.$",
        ),
    },
}

PRESERVED = {
    "data/maps/SootopolisCity_House7/scripts.inc": (
        "SootopolisCity_House7_EventScript_OldMan",
        "SootopolisCity_House7_EventScript_PokefanF",
    ),
    "data/maps/PacifidlogTown_PokemonCenter_1F/scripts.inc": (
        "HEAL_LOCATION_PACIFIDLOG_TOWN",
        "LOCALID_PACIFIDLOG_NURSE",
        "Common_EventScript_PkmnCenterNurse",
    ),
    "data/maps/VerdanturfTown_House/scripts.inc": (
        "VerdanturfTown_House_EventScript_Woman1",
        "VerdanturfTown_House_EventScript_Woman2",
    ),
    "data/scripts/gift_trainer.inc": (
        "MysteryGiftScript_VisitingTrainer",
        "ValidateEReaderTrainer",
        "MysteryGiftScript_VisitingTrainerArrived",
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
            raise ValueError(f"missing optional location block: {label}")
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

    target_text = "\n".join(
        pattern(label).search(out).group("body") for label in labels
    )
    for forbidden in ("SOOTOPOLIS CITY", "PACIFIDLOG TOWN", "PACIFIDLOG", "EVER GRANDE CITY"):
        if forbidden in target_text:
            raise ValueError(f"{rel}: legacy location survived target blocks: {forbidden}")
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
        f"Optional location identity OK: {total} blocks across "
        f"{len(TARGETS)} files; {changed} changed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

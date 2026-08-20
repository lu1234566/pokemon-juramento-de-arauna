#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")
TARGETS: dict[str, dict[str, tuple[str, ...]]] = {}


def add(path: str, label: str, *lines: str) -> None:
    TARGETS.setdefault(path, {})[label] = lines


R109 = "data/maps/Route109/scripts.inc"
add(R109, "DewfordTown_Text_BrineyLandedInSlateportDeliverGoods",
    "SAILOR: PORTO DO SAL!\\p",
    "Take the RESEARCH CASE to the\\n",
    "SHIPYARD as promised.\\p",
    "I'll wait for your next route.$")
add(R109, "Route109_Text_BrineySailToDewfordQuestion",
    "SAILOR: You still have the\\n",
    "RESEARCH CASE.\\p",
    "Sail back to PORTO DAS REDES?$" )
add(R109, "Route109_Text_BrineyDewfordItIs",
    "SAILOR: PORTO DAS REDES it is!\\p",
    "We're casting off.$")
add(R109, "Route109_Text_BrineyDeliverDevonGoods",
    "SAILOR: Deliver the RESEARCH CASE.\\p",
    "I'll wait here.$")
add(R109, "DewfordTown_Text_BrineyLandedInSlateport",
    "SAILOR: PORTO DO SAL!\\p",
    "Tell me when you need the sea\\n",
    "route again.$")
add(R109, "Route109_Text_BrineyWhereAreWeBound",
    "SAILOR: The sea route is open.\\p",
    "Where are we bound?$" )
add(R109, "Route109_Text_BrineyTellMeWhenYouNeedToSail",
    "SAILOR: Tell me when you need\\n",
    "the sea route again.$")

UNDER = "data/maps/Underwater_SeafloorCavern/scripts.inc"
add(UNDER, "Underwater_SeafloorCavern_Text_SubExplorer1",
    "“SUBMARINE EXPLORER 1” is painted\\n",
    "on the hull.\\p",
    "HORIZON took this vessel from\\n",
    "PORTO DO SAL.\\p",
    "Their team entered M'BOI here.$")

PRESERVED = {
    R109: (
        "FLAG_DELIVERED_DEVON_GOODS",
        "MULTI_BRINEY_OFF_DEWFORD",
        "VAR_BRINEY_LOCATION",
        "MAP_DEWFORD_TOWN",
        "LOCALID_ROUTE109_BRINEY",
    ),
    UNDER: (
        "FLAG_LANDMARK_SEAFLOOR_CAVERN",
        "FLAG_HIDE_UNDERWATER_SEA_FLOOR_CAVERN_STOLEN_SUBMARINE",
        "MAP_SEAFLOOR_CAVERN_ENTRANCE",
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
                        raise ValueError(f"{rel}: {label}: {len(segment)} chars: {segment!r}")


def mask(text: str, labels: tuple[str, ...]) -> str:
    out = text
    for label in labels:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render(rel: str, source: str) -> str:
    out = source
    labels = tuple(TARGETS[rel])
    for label, lines in TARGETS[rel].items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{rel}: {label}: expected 1 block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        out = out[:start] + body + out[end:]
    if mask(source, labels) != mask(out, labels):
        raise ValueError(f"{rel}: non-dialogue structure changed")
    for token in PRESERVED[rel]:
        if token not in out:
            raise ValueError(f"{rel}: missing preserved token {token}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")
    validate_widths()
    total = sum(len(v) for v in TARGETS.values())
    changed = 0
    for rel in TARGETS:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        output = render(rel, source)
        if output != source:
            changed += 1
            if args.in_place:
                path.write_text(output, encoding="utf-8")
    print(f"Early sea route English identity OK: {total} blocks across {len(TARGETS)} files; {changed} changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

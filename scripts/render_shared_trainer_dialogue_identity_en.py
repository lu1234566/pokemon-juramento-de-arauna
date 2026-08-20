#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "text" / "trainers.inc"
MAX = 32
CTRL = re.compile(r"\\[npl]")

BLOCKS: dict[str, tuple[str, ...]] = {
    "Route116_Text_JerryPostBattle": (
        "I'll have to redo some courses at\\n",
        "the TRAINER'S SCHOOL.\\l",
        "If I don't, DALVA will be steamed.$",
    ),
    "Route116_Text_JerryPostRematch": (
        "I'll have to redo some courses at\\n",
        "the TRAINER'S SCHOOL.\\l",
        "If I don't, DALVA will be steamed.$",
    ),
    "Route116_Text_KarenPostBattle": (
        "Awww, I'll never become an elegant\\n",
        "TRAINER like DALVA this way!$",
    ),
    "Route116_Text_KarenPostRematch": (
        "You've beaten DALVA?\\n",
        "I can't beat you, then. Not yet.$",
    ),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+:(?:\n|$)|\Z)"
    )


def validate_widths() -> None:
    for label, lines in BLOCKS.items():
        for line in lines:
            for segment in CTRL.split(line.replace("$", "")):
                segment = segment.strip()
                if len(segment) > MAX:
                    raise ValueError(f"{label}: {len(segment)} chars: {segment!r}")


def mask(text: str) -> str:
    out = text
    for label in BLOCKS:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing shared trainer block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render(source: str) -> str:
    out = source
    for label, lines in BLOCKS.items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        out = out[:start] + body + out[end:]

    if mask(source) != mask(out):
        raise ValueError("shared trainer dialogue changed outside target blocks")
    for label in BLOCKS:
        body = pattern(label).search(out).group("body")
        if "ROXANNE" in body or "DALVA" not in body:
            raise ValueError(f"{label}: Dalva identity was not rendered cleanly")
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
    print(f"Shared trainer dialogue identity OK: {len(BLOCKS)} Route 116 blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

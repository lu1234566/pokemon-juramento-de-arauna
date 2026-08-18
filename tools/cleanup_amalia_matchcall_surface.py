#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/text/match_call.inc"
LABEL = "MatchCall_Text_Wallace"
LINES = (
    r"AMALIA: Ola, {PLAYER}.\p",
    r"Voce ja encontrou BENTO?\p",
    r"Ele enxerga caminhos que pouca\n",
    r"gente percebe.\p",
    r"Continue ouvindo o que ARAUNA\n",
    r"tem para mostrar.$",
)
FORBIDDEN = ("WALLACE", "STEVEN", "HOENN")


def marker_for(text: str) -> str:
    for suffix in ("::\n", ":\n"):
        marker = LABEL + suffix
        if marker in text:
            return marker
    raise RuntimeError(f"Missing Match Call block: {LABEL}")


def bounds(text: str) -> tuple[int, int, str]:
    marker = marker_for(text)
    start = text.find(marker)
    end = text.find("\n\n", start)
    if end < 0:
        end = len(text)
    else:
        end += 1
    return start, end, marker


def render(marker: str) -> str:
    return marker + "".join(f'\t.string "{line}"\n' for line in LINES)


def validate(text: str) -> list[str]:
    start, end, marker = bounds(text)
    block = text[start:end]
    failures: list[str] = []
    if block != render(marker):
        failures.append("Amalia Match Call block differs from canonical text")
    for token in FORBIDDEN:
        if token in block:
            failures.append(f"legacy visible token remains: {token}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    start, end, marker = bounds(text)
    replacement = render(marker)
    changed = text[start:end] != replacement
    text = text[:start] + replacement + text[end:]
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Amalia Match Call cleanup: {'changed' if changed else 'already canonical'}.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Amalia Match Call check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Amalia Match Call PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

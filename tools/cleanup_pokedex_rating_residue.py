#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "text" / "pokedex_rating.inc"

REQUIRED = (
    "ANAHI: {PLAYER}",
    "registro excelente de ARAUNA",
    "ARAUNA abriga mais especies",
    "a diversidade de ARAUNA",
    "POKéDEX de ARAUNA completa!",
)

FORBIDDEN = (
    "HOENN",
    "You've",
    "you haven't",
    "I guess",
    "SAFARI ZONE",
    "nationwide basis",
    "POKéMON PROFESSOR",
)

STRING_RE = re.compile(r'^\s*\.string\s+"(.*)"\s*$')
CONTROL_RE = re.compile(r"\\[npl]|\{[^}]+\}")
MAX_VISIBLE_CHARS = 32


def visible_segments(raw: str) -> list[str]:
    parts = re.split(r"\\[npl]", raw)
    return [CONTROL_RE.sub("", part).replace("$", "") for part in parts]


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for token in REQUIRED:
        if token not in text:
            failures.append(f"missing canonical Arauna rating token: {token}")
    for token in FORBIDDEN:
        if token.lower() in text.lower():
            failures.append(f"legacy visible rating token remains: {token}")

    for line_no, line in enumerate(text.splitlines(), 1):
        match = STRING_RE.match(line)
        if not match:
            continue
        for segment in visible_segments(match.group(1)):
            if len(segment) > MAX_VISIBLE_CHARS:
                failures.append(
                    f"line {line_no} exceeds {MAX_VISIBLE_CHARS} visible chars: {segment!r}"
                )
    return failures


def run() -> int:
    text = TARGET.read_text(encoding="utf-8")
    failures = validate(text)
    if failures:
        print("Pokedex rating Arauna cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Pokedex rating Arauna cleanup PASS: identity, language residue and width verified.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    return run()


if __name__ == "__main__":
    raise SystemExit(main())

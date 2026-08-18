#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/RustboroCity_Mart/scripts.inc"
MAX_VISIBLE = 32
REQUIRED = (
    "Estou levando PARLYZ HEAL e",
    "Meu POKéMON evoluiu.",
    "Vou levar uma ESCAPE ROPE",
)
FORBIDDEN = (
    "I'm buying",
    "My POKéMON evolved",
    "I'm getting an ESCAPE ROPE",
    "PETALBURG WOODS",
)
STRING_RE = re.compile(r'\.string "(.*)"')


def validate() -> list[str]:
    text = TARGET.read_text(encoding="utf-8")
    failures: list[str] = []
    for required in REQUIRED:
        if required not in text:
            failures.append(f"missing localized Mart text: {required!r}")
    for legacy in FORBIDDEN:
        if legacy in text:
            failures.append(f"legacy visible Mart text remains: {legacy!r}")
    for raw in STRING_RE.findall(text):
        for segment in re.split(r"\\[npl]", raw):
            visible = segment.replace("$", "")
            if len(visible) > MAX_VISIBLE:
                failures.append(f"over-width Mart segment: {visible!r}")
    return failures


def check() -> int:
    failures = validate()
    if failures:
        print("Serra do Uivo Mart surface check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Serra do Uivo Mart surface PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    return check()


if __name__ == "__main__":
    raise SystemExit(main())

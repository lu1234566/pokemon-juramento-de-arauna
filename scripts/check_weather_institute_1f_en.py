#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "Route119_WeatherInstitute_1F" / "scripts.inc"
MAX_WIDTH = 32

REQUIRED = (
    "DISENCHANTMENT",
    "BOND arrays",
    "HORIZON wants the servers",
    "LIVING ARCHIVE safety claims",
    "Something under Arauna",
)

FORBIDDEN = (
    "Os pesquisadores",
    "O HORIZONTE",
    "DESENCANTO",
    "VINCULO",
    "ARQUIVO VIVO",
    "perda de memoria",
    "chuva, temperatura",
)

CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")
STRING_RE = re.compile(r'^\s*\.string "(.*)"$', re.MULTILINE)


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def main() -> int:
    source = TARGET.read_text(encoding="utf-8")

    for text in REQUIRED:
        if text not in source:
            raise SystemExit(f"missing required English Weather Institute text: {text}")
    for text in FORBIDDEN:
        if text in source:
            raise SystemExit(f"Portuguese Weather Institute residue survived: {text}")

    for match in STRING_RE.finditer(source):
        for segment in visible_segments(match.group(1)):
            if len(segment) > MAX_WIDTH:
                raise SystemExit(
                    f"Weather Institute 1F visible segment is {len(segment)} chars: {segment!r}"
                )

    print("Weather Institute 1F English surface OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

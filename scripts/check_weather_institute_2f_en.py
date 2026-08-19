#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "Route119_WeatherInstitute_2F" / "scripts.inc"
MAX_WIDTH = 32

REQUIRED = (
    "HORIZON seizure order",
    "Remembrancer scouts",
    "They have a RECORD-MATRIX",
    "CASTFORM changes with weather",
    "near {STR_VAR_1}",
    "deep BOND signature",
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

PRESERVED = (
    "TRAINER_SHELLY_WEATHER_INSTITUTE",
    "SPECIES_CASTFORM",
    "ITEM_MYSTIC_WATER",
    "FLAG_RECEIVED_CASTFORM",
    "VAR_WEATHER_INSTITUTE_STATE",
    "CreateAbnormalWeatherEvent",
    "GetAbnormalWeatherMapNameAndType",
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
            raise SystemExit(f"missing required Weather Institute 2F English text: {text}")
    for text in FORBIDDEN:
        if text in source:
            raise SystemExit(f"Portuguese Weather Institute 2F residue survived: {text}")
    for token in PRESERVED:
        if token not in source:
            raise SystemExit(f"preserved gameplay token missing: {token}")

    for match in STRING_RE.finditer(source):
        for segment in visible_segments(match.group(1)):
            if len(segment) > MAX_WIDTH:
                raise SystemExit(
                    f"Weather Institute 2F visible segment is {len(segment)} chars: {segment!r}"
                )

    print("Weather Institute 2F English narrative surface OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

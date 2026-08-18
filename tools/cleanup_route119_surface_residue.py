#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "Route119" / "scripts.inc"

TARGETS = {
    "Route119_Text_ScottWayToGoBeSeeingYou": (
        r"VIAJANTE: Ei, {PLAYER}!\p",
        r"Cruzei com CIRO subindo a trilha.\n",
        r"Ele parecia com pressa demais.\p",
        r"Se vai para a MATA DO MEIO,\n",
        r"continue atento ao caminho.$",
    ),
    "Route119_Text_ScottYouWonAtFortreeGym": (
        r"... ... ... ... ... ...\n",
        r"... ... ... ... ... Bip!\p",
        r"VIAJANTE: {PLAYER}, sou eu!\p",
        r"Ouvi que venceu o desafio\n",
        r"de LIDIA na MATA DO MEIO.\p",
        r"Continue assim. Arauna anda\n",
        r"precisando de gente atenta.\p",
        r"... ... ... ... ... Clique!$",
    ),
    "Route119_Text_StayAwayFromWeatherInstitute": (
        r"HORIZONTE: Estamos isolando\n",
        r"o INSTITUTO DAS AGUAS.\p",
        r"Nao se aproxime enquanto a\n",
        r"operacao estiver em andamento.$",
    ),
    "Route119_Text_DontGoNearWeatherInstitute": (
        r"HORIZONTE: Vigiar esta ponte\n",
        r"e mais tedioso do que parece.\p",
        r"Mesmo assim, nao chegue perto\n",
        r"do INSTITUTO DAS AGUAS.$",
    ),
    "Route119_Text_RouteSignFortree": (
        r"ROTA 119\n",
        r"{RIGHT_ARROW} MATA DO MEIO$",
    ),
    "Route119_Text_WeatherInstitute": (
        r"INSTITUTO DAS AGUAS$",
    ),
}

FORBIDDEN = ("SCOTT:", "FORTREE", "WEATHER INSTITUTE")


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?m)^{re.escape(label)}:\n(?:\t\.string \"[^\n]*\"\n)+")


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def extract(text: str, label: str) -> str:
    match = block_pattern(label).search(text)
    if not match:
        raise RuntimeError(f"Missing text block: {label}")
    return match.group(0)


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for label, lines in TARGETS.items():
        block = extract(text, label)
        for line in lines:
            if f'\t.string "{line}"' not in block:
                failures.append(f"{label} missing expected line: {line}")
        for token in FORBIDDEN:
            if token in block:
                failures.append(f"{label} still contains legacy token: {token}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for label, lines in TARGETS.items():
        updated, count = block_pattern(label).subn(lambda _m: render(label, lines), text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not uniquely replace {label} (matches={count})")
        if updated != text:
            changed += 1
        text = updated
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Route 119 visible-surface cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Route 119 visible-surface cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Route 119 visible-surface cleanup check PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

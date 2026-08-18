#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data/maps/PetalburgCity_Gym/scripts.inc"

# Badge naming/art is intentionally handled by the dedicated badge integration lot.
# These two blocks are excluded so this preparation can merge independently later.
BADGE_HANDOFF_LABELS = {
    "PetalburgCity_Gym_Text_ReceivedBalanceBadge",
    "PetalburgCity_Gym_Text_ExplainBalanceBadgeTakeThis",
}

VISIBLE_REPLACEMENTS = {
    "NORMAN": "ELIAS",
    "DAD:": "ELIAS:",
    "PETALBURG CITY": "PAMPA DA ESPERA",
    "PETALBURG GYM": "GINASIO PAMPA",
    "RUSTBORO CITY": "SERRA DO UIVO",
    "ROXANNE": "DALVA",
    "DEWFORD": "PORTO DAS REDES",
}

LEGACY_VISIBLE = tuple(VISIBLE_REPLACEMENTS)
STRING_RE = re.compile(r'^(?P<prefix>\s*\.string\s+")(?P<body>.*)(?P<suffix>"\s*)$')
LABEL_RE = re.compile(r'^([A-Za-z0-9_]+):\s*$')


def transform(text: str) -> tuple[str, int]:
    current_label: str | None = None
    changed = 0
    out: list[str] = []

    for raw in text.splitlines(keepends=True):
        line = raw.rstrip("\n")
        newline = "\n" if raw.endswith("\n") else ""

        label_match = LABEL_RE.match(line)
        if label_match:
            current_label = label_match.group(1)
            out.append(raw)
            continue

        string_match = STRING_RE.match(line)
        if string_match and current_label not in BADGE_HANDOFF_LABELS:
            body = string_match.group("body")
            new_body = body
            for old, new in VISIBLE_REPLACEMENTS.items():
                new_body = new_body.replace(old, new)
            if new_body != body:
                changed += 1
                line = f'{string_match.group("prefix")}{new_body}{string_match.group("suffix")}'

        out.append(line + newline)

    return "".join(out), changed


def validate(text: str) -> list[str]:
    failures: list[str] = []
    current_label: str | None = None

    for lineno, raw in enumerate(text.splitlines(), start=1):
        label_match = LABEL_RE.match(raw)
        if label_match:
            current_label = label_match.group(1)
            continue
        string_match = STRING_RE.match(raw)
        if not string_match or current_label in BADGE_HANDOFF_LABELS:
            continue
        body = string_match.group("body")
        for legacy in LEGACY_VISIBLE:
            if legacy in body:
                failures.append(f"line {lineno}: legacy visible identity {legacy!r} remains")

    return failures


def apply() -> int:
    original = TARGET.read_text(encoding="utf-8")
    updated, changed = transform(original)
    failures = validate(updated)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(updated, encoding="utf-8")
    print(f"Pampa da Espera / Elias gym identity cleanup: {changed} string lines changed.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Pampa da Espera / Elias gym identity check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Pampa da Espera / Elias gym identity check PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

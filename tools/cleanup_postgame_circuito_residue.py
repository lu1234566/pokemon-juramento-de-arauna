#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from postgame_circuito_targets import TARGETS

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "BattleFrontier_ScottsHouse" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_WIDTHS = {"{PLAYER}": 7, "{KUN}": 0, "{STR_VAR_1}": 10}
FORBIDDEN_VISIBLE = (
    "SCOTT:", "BATTLE FRONTIER", "FRONTIER PASS", "FRONTIER BRAINS",
    "Battle Point(s)", "TRAINERS", "You've", "I'm ", "I want",
)
REQUIRED_INTERNAL = (
    "FLAG_SCOTT_GIVES_BATTLE_POINTS", "VAR_SCOTT_STATE",
    "LOCALID_SCOTTS_HOUSE_SCOTT", "GiveFrontierBattlePoints",
    "FLAG_SYS_TOWER_SILVER", "FLAG_SYS_TOWER_GOLD",
    "DECOR_SILVER_SHIELD", "DECOR_GOLD_SHIELD",
    "ITEM_LANSAT_BERRY", "ITEM_STARF_BERRY",
)


def render(label: str, lines: tuple[str, ...]) -> str:
    return label + ":\n" + "".join(f'\t.string "{line}"\n' for line in lines)


def bounds(text: str, label: str) -> tuple[int, int]:
    start = text.find(label + ":\n")
    if start < 0:
        raise RuntimeError(f"Missing block: {label}")
    end = text.find("\n\n", start)
    return start, len(text) if end < 0 else end + 1


def extract(text: str, label: str) -> str:
    start, end = bounds(text, label)
    return text[start:end]


def visible_width(segment: str) -> int:
    visible = segment
    for token, width in PLACEHOLDER_WIDTHS.items():
        visible = visible.replace(token, "X" * width)
    visible = re.sub(r"\{[^}]+\}", "", visible)
    return len(visible.replace("$", ""))


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for token in REQUIRED_INTERNAL:
        if token not in text:
            failures.append(f"missing inherited internal sentinel: {token}")
    for label, lines in TARGETS.items():
        block = extract(text, label)
        if block != render(label, lines):
            failures.append(f"non-canonical block: {label}")
        for token in FORBIDDEN_VISIBLE:
            if token in block:
                failures.append(f"legacy visible token in {label}: {token}")
        for segment in re.split(r"\\[npl]", "".join(lines)):
            if segment and visible_width(segment) > MAX_VISIBLE_WIDTH:
                failures.append(f"line wider than 32 in {label}: {segment!r}")
    joined = "\n".join(extract(text, label) for label in TARGETS)
    for token in (
        "SEU BENTO", "CIRCUITO DE BATALHA", "PASSE DO CIRCUITO",
        "MESTRE DO CIRCUITO", "SIMBOLOS PRATEADOS", "SIMBOLOS DOURADOS",
    ):
        if token not in joined:
            failures.append(f"missing canonical visible term: {token}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for label, lines in TARGETS.items():
        start, end = bounds(text, label)
        replacement = render(label, lines)
        if text[start:end] != replacement:
            text = text[:start] + replacement + text[end:]
            changed += 1
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Post-game Circuito cleanup: {changed} changed; {len(TARGETS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Post-game Circuito cleanup check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Post-game Circuito cleanup check PASS: {len(TARGETS)} blocks.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return check() if parser.parse_args().check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

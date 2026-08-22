#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "battle_circuit_ui.json"
TARGET_PATH = ROOT / "src" / "strings.c"
EXPECTED = {
    "gText_CheckFrontierMap",
    "gText_PutAwayFrontierPass",
    "gText_BattleFrontier",
}
LEGACY_VALUES = {
    "gText_CheckFrontierMap": "Check BATTLE FRONTIER MAP.",
    "gText_PutAwayFrontierPass": "Put away the FRONTIER PASS.",
    "gText_BattleFrontier": "BATTLE FRONTIER",
}
DECL_RE = re.compile(
    r'(?m)^const u8 (?P<name>gText_[A-Za-z0-9_]+)\[\] = _\("(?P<value>(?:[^"\\]|\\.)*)"\);(?P<suffix>[^\n]*)$'
)


def load_bank() -> dict[str, str]:
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(bank) != EXPECTED:
        raise ValueError(
            f"label contract mismatch; missing={sorted(EXPECTED - set(bank))}, "
            f"extra={sorted(set(bank) - EXPECTED)}"
        )
    for name, value in bank.items():
        if not isinstance(value, str) or not value:
            raise ValueError(f"{name}: UI value must be a non-empty string")
        if '"' in value or "\n" in value or "\r" in value:
            raise ValueError(f"{name}: UI value is not C-string safe")
    return bank


def locate(source: str, name: str) -> re.Match[str]:
    matches = [m for m in DECL_RE.finditer(source) if m.group("name") == name]
    if len(matches) != 1:
        raise ValueError(f"{name}: expected one declaration, found {len(matches)}")
    return matches[0]


def render(source: str, bank: dict[str, str]) -> str:
    replacements: list[tuple[int, int, str]] = []
    for name, new_value in bank.items():
        match = locate(source, name)
        current = match.group("value")
        legacy = LEGACY_VALUES[name]
        if current not in (legacy, new_value):
            raise ValueError(f"{name}: unexpected source value: {current!r}")
        new_decl = f'const u8 {name}[] = _("{new_value}");{match.group("suffix")}'
        replacements.append((match.start(), match.end(), new_decl))

    result = source
    for start, end, replacement in sorted(replacements, reverse=True):
        result = result[:start] + replacement + result[end:]
    return result


def mask(source: str) -> str:
    spans: list[tuple[int, int, str]] = []
    for name in EXPECTED:
        match = locate(source, name)
        spans.append((match.start(), match.end(), f'const u8 {name}[] = _("<ARAUNA_CIRCUIT_UI>");{match.group("suffix")}'))
    result = source
    for start, end, replacement in sorted(spans, reverse=True):
        result = result[:start] + replacement + result[end:]
    return result


def validate(source: str, rendered: str, bank: dict[str, str]) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("src/strings.c changed outside the three owned declarations")

    for name, new_value in bank.items():
        match = locate(rendered, name)
        if match.group("value") != new_value:
            raise ValueError(f"{name}: rendered value mismatch")

    owned = "\n".join(locate(rendered, name).group("value") for name in sorted(EXPECTED))
    for stale in ("BATTLE FRONTIER", "FRONTIER PASS"):
        if stale in owned:
            raise ValueError(f"stale visible UI token survived: {stale}")
    for required in ("BATTLE CIRCUIT", "CIRCUIT PASS"):
        if required not in owned:
            raise ValueError(f"Battle Circuit UI identity missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the English Battle Circuit text UI in src/strings.c.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    source = TARGET_PATH.read_text(encoding="utf-8")
    rendered = render(source, bank)
    validate(source, rendered, bank)

    if args.check:
        print("Battle Circuit UI renderer OK: 3 declarations validated.")
        return 0
    if args.in_place:
        TARGET_PATH.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

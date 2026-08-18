#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src/strings.c"

REPLACEMENTS = {
    'const u8 gText_MainMenuNewGame[] = _("NEW GAME");':
        'const u8 gText_MainMenuNewGame[] = _("NOVO JOGO");',
    'const u8 gText_MainMenuContinue[] = _("CONTINUE");':
        'const u8 gText_MainMenuContinue[] = _("CONTINUAR");',
    'const u8 gText_MainMenuOption[] = _("OPTION");':
        'const u8 gText_MainMenuOption[] = _("OPCOES");',
    'const u8 gText_BirchBoy[] = _("BOY");':
        'const u8 gText_BirchBoy[] = _("MENINO");',
    'const u8 gText_BirchGirl[] = _("GIRL");':
        'const u8 gText_BirchGirl[] = _("MENINA");',
    'const u8 gText_ThisIsAPokemon[] = _("This is what we call a “POKéMON.”{PAUSE 96}\\p");':
        'const u8 gText_ThisIsAPokemon[] = _("Chamamos isso de “POKéMON.”{PAUSE 96}\\p");',
    'const u8 gText_ConfirmStarterChoice[] = _("Do you choose this POKéMON?");':
        'const u8 gText_ConfirmStarterChoice[] = _("Escolher este POKéMON?");',
}


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for old, new in REPLACEMENTS.items():
        if old in text:
            failures.append(f"legacy new-game UI remains: {old}")
        if new not in text:
            failures.append(f"missing localized new-game UI: {new}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        if new in text and old not in text:
            continue
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one new-game UI string {old!r}, found {count}")
        text = text.replace(old, new, 1)
        changed += 1
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"New-game core UI cleanup: {changed} changed; {len(REPLACEMENTS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("New-game core UI check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"New-game core UI PASS: {len(REPLACEMENTS)} strings.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

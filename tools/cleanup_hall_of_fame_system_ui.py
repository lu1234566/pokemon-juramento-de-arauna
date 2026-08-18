#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src/strings.c"

REPLACEMENTS = {
    'const u8 gText_WelcomeToHOF[] = _("Welcome to the HALL OF FAME!");':
        'const u8 gText_WelcomeToHOF[] = _("SALA DA FAMA DE ARAUNA!");',
    'const u8 gText_HOFDexSaving[] = _("SAVING…\\nDON\'T TURN OFF THE POWER.");':
        'const u8 gText_HOFDexSaving[] = _("SALVANDO…\\nNAO DESLIGUE.");',
    'const u8 gText_HOFCorrupted[] = _("The HALL OF FAME data is corrupted.");':
        'const u8 gText_HOFCorrupted[] = _("Dados da SALA DA FAMA\\nestao corrompidos.");',
    'const u8 gText_HOFNumber[] = _("HALL OF FAME No. {STR_VAR_1}");':
        'const u8 gText_HOFNumber[] = _("SALA DA FAMA No. {STR_VAR_1}");',
    'const u8 gText_LeagueChamp[] = _("LEAGUE CHAMPION!\\nCONGRATULATIONS!");':
        'const u8 gText_LeagueChamp[] = _("LIGA CONQUISTADA!\\nPARABENS!");',
}


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for old, new in REPLACEMENTS.items():
        if old in text:
            failures.append(f"legacy Hall of Fame UI remains: {old}")
        if new not in text:
            failures.append(f"missing Arauna Hall of Fame UI: {new}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        if new in text and old not in text:
            continue
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one Hall of Fame UI string {old!r}, found {count}")
        text = text.replace(old, new, 1)
        changed += 1
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Hall of Fame system UI cleanup: {changed} changed; {len(REPLACEMENTS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Hall of Fame system UI check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Hall of Fame system UI PASS: {len(REPLACEMENTS)} strings.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

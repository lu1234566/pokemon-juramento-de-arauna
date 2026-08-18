#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src/strings.c"

# Elias is intentionally excluded here: his dedicated Match Call preparation owns
# both gText_NormanMatchCallDesc and gText_NormanMatchCallName.
REPLACEMENTS = {
    'const u8 gText_RoxanneMatchCallDesc[] = _("ROCKIN\' WHIZ");':
        'const u8 gText_RoxanneMatchCallDesc[] = _("PEDRA VIVA");',
    'const u8 gText_BrawlyMatchCallDesc[] = _("THE BIG HIT");':
        'const u8 gText_BrawlyMatchCallDesc[] = _("MARE FORTE");',
    'const u8 gText_WattsonMatchCallDesc[] = _("SWELL SHOCK");':
        'const u8 gText_WattsonMatchCallDesc[] = _("REDE VIVA");',
    'const u8 gText_FlanneryMatchCallDesc[] = _("PASSION BURN");':
        'const u8 gText_FlanneryMatchCallDesc[] = _("BRASA VIVA");',
    'const u8 gText_WinonaMatchCallDesc[] = _("SKY TAMER");':
        'const u8 gText_WinonaMatchCallDesc[] = _("VOO DA MATA");',
    'const u8 gText_TateLizaMatchCallDesc[] = _("MYSTIC DUO");':
        'const u8 gText_TateLizaMatchCallDesc[] = _("DUPLA DO CEU");',
    'const u8 gText_JuanMatchCallDesc[] = _("DANDY CHARM");':
        'const u8 gText_JuanMatchCallDesc[] = _("AGUA ANTIGA");',
}


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for old, new in REPLACEMENTS.items():
        if new not in text:
            failures.append(f"missing Arauna contact string: {new}")
        if old in text:
            failures.append(f"legacy contact string remains: {old}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        if new in text and old not in text:
            continue
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one source string {old!r}, found {count}")
        text = text.replace(old, new, 1)
        changed += 1
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Arauna PokéNav contact descriptions: {changed} changed; {len(REPLACEMENTS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Arauna PokéNav contact description check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Arauna PokéNav contact description PASS: {len(REPLACEMENTS)} strings.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

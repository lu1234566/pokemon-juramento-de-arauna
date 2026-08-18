#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "strings.c"

REPLACEMENTS = {
    'const u8 gText_ExpandedPlaceholder_Brendan[] = _("BRENDAN");': 'const u8 gText_ExpandedPlaceholder_Brendan[] = _("CIRO");',
    'const u8 gText_ExpandedPlaceholder_May[] = _("MAY");': 'const u8 gText_ExpandedPlaceholder_May[] = _("CIRO");',
    'const u8 gText_ExpandedPlaceholder_Aqua[] = _("AQUA");': 'const u8 gText_ExpandedPlaceholder_Aqua[] = _("HORIZONTE");',
    'const u8 gText_ExpandedPlaceholder_Magma[] = _("MAGMA");': 'const u8 gText_ExpandedPlaceholder_Magma[] = _("LEMBRANTES");',
    'const u8 gText_ExpandedPlaceholder_Archie[] = _("ARCHIE");': 'const u8 gText_ExpandedPlaceholder_Archie[] = _("OTACILIO");',
    'const u8 gText_ExpandedPlaceholder_Maxie[] = _("MAXIE");': 'const u8 gText_ExpandedPlaceholder_Maxie[] = _("LUZIA");',
    'const u8 gText_DexHoennTitle[] = _("HOENN DEX");': 'const u8 gText_DexHoennTitle[] = _("ARAUNA DEX");',
    'const u8 gText_DexHoennDescription[] = _("HOENN region\'s POKéDEX");': 'const u8 gText_DexHoennDescription[] = _("ARAUNA region\'s POKéDEX");',
    'const u8 gText_DexHoenn[] = _("HOENN");': 'const u8 gText_DexHoenn[] = _("ARAUNA");',
}


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for old, new in REPLACEMENTS.items():
        if new not in text:
            failures.append(f"missing expected Arauna string: {new}")
        if old in text:
            failures.append(f"legacy visible string remains: {old}")
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
    print(f"System/UI Arauna identity cleanup: {changed} changed; {len(REPLACEMENTS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("System/UI Arauna identity check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"System/UI Arauna identity check PASS: {len(REPLACEMENTS)} strings.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

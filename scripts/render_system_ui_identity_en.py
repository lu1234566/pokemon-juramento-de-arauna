#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "strings.c"

REPLACEMENTS = {
    'const u8 gText_ExpandedPlaceholder_Brendan[] = _("BRENDAN");':
        'const u8 gText_ExpandedPlaceholder_Brendan[] = _("CIRO");',
    'const u8 gText_ExpandedPlaceholder_May[] = _("MAY");':
        'const u8 gText_ExpandedPlaceholder_May[] = _("CIRO");',
    'const u8 gText_DexHoennTitle[] = _("HOENN DEX");':
        'const u8 gText_DexHoennTitle[] = _("ARAUNA DEX");',
    'const u8 gText_DexHoennDescription[] = _("HOENN region\'s POKéDEX");':
        'const u8 gText_DexHoennDescription[] = _("ARAUNA region\'s POKéDEX");',
    'const u8 gText_DexHoenn[] = _("HOENN");':
        'const u8 gText_DexHoenn[] = _("ARAUNA");',
}


def render(source: str) -> str:
    out = source
    for old, new in REPLACEMENTS.items():
        if new in out and old not in out:
            continue
        count = out.count(old)
        if count != 1:
            raise ValueError(f"expected one system UI anchor, found {count}: {old}")
        out = out.replace(old, new, 1)
    return out


def validate(out: str) -> None:
    for old, new in REPLACEMENTS.items():
        if old in out:
            raise ValueError(f"legacy system identity survived: {old}")
        if new not in out:
            raise ValueError(f"missing Arauna system identity: {new}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")
    source = TARGET.read_text(encoding="utf-8")
    out = render(source)
    validate(out)
    if args.in_place and out != source:
        TARGET.write_text(out, encoding="utf-8")
    print(f"Arauna system UI identity overlay OK: {len(REPLACEMENTS)} anchors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

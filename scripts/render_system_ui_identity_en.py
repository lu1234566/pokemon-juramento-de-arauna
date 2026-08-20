#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
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

MENU_VALUES = {
    "gText_Petalburg": "PAMPA DA ESPERA",
    "gText_Slateport": "PORTO DO SAL",
    "gText_Dewford": "PORTO DAS REDES",
}

# These symbols feed a runtime pool of famous trainer names. Keep the symbol
# identities and selection logic intact while replacing only the visible names.
FAMOUS_TRAINER_VALUES = {
    "gText_Wallace": "AMALIA",
    "gText_Steven": "SEU BENTO",
    "gText_Brawly": "ADEMAR",
    "gText_Winona": "LIDIA",
}


def declaration_pattern(symbol: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?m)^const u8 {re.escape(symbol)}\[\] = _\("(?:\\.|[^"\\])*"\);$'
    )


def render_symbol_values(source: str, values: dict[str, str]) -> str:
    out = source
    for symbol, value in values.items():
        rx = declaration_pattern(symbol)
        matches = list(rx.finditer(out))
        if len(matches) != 1:
            raise ValueError(f"expected one declaration for {symbol}, found {len(matches)}")
        replacement = f'const u8 {symbol}[] = _("{value}");'
        out = rx.sub(lambda _: replacement, out, count=1)
    return out


def render(source: str) -> str:
    out = source
    for old, new in REPLACEMENTS.items():
        if new in out and old not in out:
            continue
        count = out.count(old)
        if count != 1:
            raise ValueError(f"expected one system UI anchor, found {count}: {old}")
        out = out.replace(old, new, 1)

    out = render_symbol_values(out, MENU_VALUES)
    out = render_symbol_values(out, FAMOUS_TRAINER_VALUES)
    return out


def validate_symbol_values(out: str, values: dict[str, str], category: str) -> None:
    for symbol, value in values.items():
        expected = f'const u8 {symbol}[] = _("{value}");'
        if expected not in out:
            raise ValueError(f"missing Arauna {category}: {symbol}")


def validate(out: str) -> None:
    for old, new in REPLACEMENTS.items():
        if old in out:
            raise ValueError(f"legacy system identity survived: {old}")
        if new not in out:
            raise ValueError(f"missing Arauna system identity: {new}")

    validate_symbol_values(out, MENU_VALUES, "shared menu label")
    validate_symbol_values(out, FAMOUS_TRAINER_VALUES, "famous trainer name")


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
    print(
        "Arauna system UI identity overlay OK: "
        f"{len(REPLACEMENTS)} identity anchors + {len(MENU_VALUES)} shared menu labels + "
        f"{len(FAMOUS_TRAINER_VALUES)} famous trainer names."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

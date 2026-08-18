#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "strings.c"

# High-confidence player-facing menu/map constants. Symbol names stay untouched
# because Emerald is intentionally retained as the implementation skeleton.
REPLACEMENTS = {
    'const u8 gText_Petalburg[] = _("PETALBURG");': 'const u8 gText_Petalburg[] = _("PAMPA DA ESPERA");',
    'const u8 gText_Slateport[] = _("SLATEPORT");': 'const u8 gText_Slateport[] = _("PORTO DO SAL");',
    'const u8 gText_Dewford[] = _("DEWFORD");': 'const u8 gText_Dewford[] = _("PORTO DAS REDES");',
    'const u8 gText_LilycoveCity[] = _("LILYCOVE CITY");': 'const u8 gText_LilycoveCity[] = _("BAIA DAS LUZES");',
    'const u8 gText_SlateportCity[] = _("SLATEPORT CITY");': 'const u8 gText_SlateportCity[] = _("PORTO DO SAL");',
    'const u8 gText_CheckMapOfHoenn[] = _("Check the map of the HOENN region.");': 'const u8 gText_CheckMapOfHoenn[] = _("Veja o mapa de ARAUNA.");',
    'const u8 gText_Hoenn[] = _("HOENN");': 'const u8 gText_Hoenn[] = _("ARAUNA");',
}


def validate(text: str) -> list[str]:
    failures: list[str] = []
    for old, new in REPLACEMENTS.items():
        if new not in text:
            failures.append(f"missing Arauna menu identity: {new}")
        if old in text:
            failures.append(f"legacy menu identity remains: {old}")
    return failures


def apply() -> int:
    text = TARGET.read_text(encoding="utf-8")
    changed = 0
    for old, new in REPLACEMENTS.items():
        if new in text and old not in text:
            continue
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one source constant {old!r}, found {count}")
        text = text.replace(old, new, 1)
        changed += 1
    failures = validate(text)
    if failures:
        raise RuntimeError("; ".join(failures))
    TARGET.write_text(text, encoding="utf-8")
    print(f"Global Arauna menu identity cleanup: {changed} changed; {len(REPLACEMENTS)} verified.")
    return 0


def check() -> int:
    failures = validate(TARGET.read_text(encoding="utf-8"))
    if failures:
        print("Global Arauna menu identity check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"Global Arauna menu identity check PASS: {len(REPLACEMENTS)} strings.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

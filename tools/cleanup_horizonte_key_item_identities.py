#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "src/data/items.h"
DESCRIPTIONS = ROOT / "src/data/text/item_descriptions.h"
ITEM_NAME_LENGTH = 14

ITEM_REPLACEMENTS = {
    '.name = _("DEVON GOODS"),': '.name = _("CARGA HORIZ."),',
    '.name = _("DEVON SCOPE"),': '.name = _("LENTE HORIZ."),',
}

DESC_REPLACEMENTS = {
    'static const u8 sDevonGoodsDesc[] = _(\n    "A package that\\n"\n    "contains DEVON\'s\\n"\n    "machine parts.");':
        'static const u8 sDevonGoodsDesc[] = _(\n    "Pacote selado do\\n"\n    "CONSORCIO\\n"\n    "HORIZONTE.");',
    'static const u8 sDevonScopeDesc[] = _(\n    "A device by DEVON\\n"\n    "that signals any\\n"\n    "unseeable POKéMON.");':
        'static const u8 sDevonScopeDesc[] = _(\n    "Um visor criado\\n"\n    "pelo HORIZONTE\\n"\n    "revela o oculto.");',
}


def validate(items: str, desc: str) -> list[str]:
    failures: list[str] = []
    for old, new in ITEM_REPLACEMENTS.items():
        if old in items:
            failures.append(f"legacy key-item name remains: {old}")
        if new not in items:
            failures.append(f"missing Arauna key-item name: {new}")
        visible = new.split('_("', 1)[1].split('")', 1)[0]
        if len(visible) > ITEM_NAME_LENGTH:
            failures.append(f"key-item name exceeds {ITEM_NAME_LENGTH}: {visible!r}")
    for old, new in DESC_REPLACEMENTS.items():
        if old in desc:
            failures.append("legacy Devon key-item description remains")
        if new not in desc:
            failures.append("missing Arauna key-item description")
    return failures


def apply() -> int:
    items = ITEMS.read_text(encoding="utf-8")
    desc = DESCRIPTIONS.read_text(encoding="utf-8")
    changed = 0
    for old, new in ITEM_REPLACEMENTS.items():
        if new in items and old not in items:
            continue
        count = items.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one item name {old!r}, found {count}")
        items = items.replace(old, new, 1)
        changed += 1
    for old, new in DESC_REPLACEMENTS.items():
        if new in desc and old not in desc:
            continue
        count = desc.count(old)
        if count != 1:
            raise RuntimeError(f"Expected exactly one item description block, found {count}")
        desc = desc.replace(old, new, 1)
        changed += 1
    failures = validate(items, desc)
    if failures:
        raise RuntimeError("; ".join(failures))
    ITEMS.write_text(items, encoding="utf-8")
    DESCRIPTIONS.write_text(desc, encoding="utf-8")
    print(f"Horizonte key-item identity cleanup: {changed} replacements applied.")
    return 0


def check() -> int:
    failures = validate(
        ITEMS.read_text(encoding="utf-8"),
        DESCRIPTIONS.read_text(encoding="utf-8"),
    )
    if failures:
        print("Horizonte key-item identity check FAILED:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Horizonte key-item identity PASS.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    return check() if args.check else apply()


if __name__ == "__main__":
    raise SystemExit(main())

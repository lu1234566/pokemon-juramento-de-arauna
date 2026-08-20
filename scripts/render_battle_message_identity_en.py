#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "src" / "battle_message.c"
OLD = 'static const u8 sText_DontLeaveBirch[] = _("ANAHI: Nao me deixe aqui!\\p");'
NEW = 'static const u8 sText_DontLeaveBirch[] = _("ANAHI: Don\'t leave me here!\\p");'
VANILLA = 'static const u8 sText_DontLeaveBirch[] = _("PROF. BIRCH: Don\'t leave me like this!\\p");'


def render(source: str) -> str:
    if NEW in source and OLD not in source and VANILLA not in source:
        return source
    candidates = [(OLD, source.count(OLD)), (VANILLA, source.count(VANILLA))]
    present = [(old, count) for old, count in candidates if count]
    if len(present) != 1 or present[0][1] != 1:
        raise ValueError(f"expected one rescue-message anchor, found {present}")
    return source.replace(present[0][0], NEW, 1)


def validate(source: str, rendered: str) -> None:
    if NEW not in rendered:
        raise ValueError("English Anahi rescue message is missing")
    if OLD in rendered or VANILLA in rendered:
        raise ValueError("legacy rescue battle message survived")
    if source.replace(OLD, NEW, 1).replace(VANILLA, NEW, 1) != rendered:
        raise ValueError("battle_message.c changed outside the rescue string")
    if "STRINGID_DONTLEAVEBIRCH" not in rendered:
        raise ValueError("inherited battle string ID disappeared")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")
    source = TARGET.read_text(encoding="utf-8")
    rendered = render(source)
    validate(source, rendered)
    if args.in_place and rendered != source:
        TARGET.write_text(rendered, encoding="utf-8")
    print("Anahi rescue battle-message English overlay OK: 1 exact visible string.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

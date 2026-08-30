#!/usr/bin/env python3
"""Render the 386 Pokedex entries in English for the English build.

Base data stays Portuguese, like the rest of the project; this swaps the surface
before the English ROM is built, the same shape as every other renderer in
scripts/english_renderers.txt. The translations live in
docs/arauna/ARAUNA_DEX_TEXT.csv, one row per creature, so the prose is editable
without touching generated C.

An entry with no English yet keeps its Portuguese, so the chain is safe to run
while the table is still being filled in.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = ROOT / "src/data/pokemon/pokedex_text.h"
TABLE = ROOT / "docs/arauna/ARAUNA_DEX_TEXT.csv"


def charmap_chars() -> set[str]:
    """The characters this ROM can actually encode.

    Not ASCII: the charmap has a, e, i, o, u with acutes and circumflexes and a
    cedilla, which the creature names use. It has no tilde, which is why the
    project writes Portuguese without one.
    """
    chars = {" "}
    for line in (ROOT / "charmap.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("@")[0].strip()
        if "=" not in line:
            continue
        key = line.split("=")[0].strip()
        if key.startswith("'") and key.endswith("'"):
            # The charmap escapes the apostrophe as '\''; unescape or every
            # string containing one looks unencodable.
            key = key[1:-1].replace("\\'", "'").replace('\\\\', '\\')
        chars.add(key)
    return chars


LINE_WIDTH = 44
LINES = 4
CHARS = charmap_chars()

# Named groups shift the numbered ones, so every piece is named: mixing the two
# once had this splicing the new body in front of the old and dropping the `);`.
ENTRY = re.compile(r'(?P<head>const u8 g(?P<sym>\w+?)(?P<dex>\d{3})PokedexText\[\] = _\(\n)'
                   r'(?P<body>(?:    "[^"]*"\n?)+)'
                   r'(?P<tail>\);)')


def wrap(text: str) -> list[str]:
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if len(candidate) <= LINE_WIDTH:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render(source: str, english: dict[str, str]) -> tuple[str, int]:
    rendered = 0

    def swap(match):
        nonlocal rendered
        text = english.get(match.group("dex"), "").strip()
        if not text:
            return match.group(0)
        lines = wrap(text)
        if len(lines) > LINES or any(len(l) > LINE_WIDTH for l in lines):
            raise ValueError(f"#{match.group('dex')} does not fit the dex page: {text!r}")
        bad = sorted(set(text) - CHARS)
        if bad:
            raise ValueError(f"#{match.group('dex')} uses {bad}, which the charmap lacks")
        rendered += 1
        body = "".join(
            '    "' + line.replace('"', '\\"') + ("\\n" if i < len(lines) - 1 else "") + '"\n'
            for i, line in enumerate(lines))
        return match.group("head") + body + match.group("tail")

    return ENTRY.sub(swap, source), rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    english = {row["arauna_dex"]: row["en"]
               for row in csv.DictReader(TABLE.open(encoding="utf-8"))}
    source = TEXT.read_text(encoding="utf-8")
    rendered, count = render(source, english)

    if args.check:
        print(f"Arauna Pokedex English surface OK: {count} of 386 entries rendered.")
        return 0
    if args.in_place:
        TEXT.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered[:2000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

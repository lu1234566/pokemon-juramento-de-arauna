#!/usr/bin/env python3
"""Keep the Pokedex prose in step between the Portuguese base and the English build.

The 386 dex entries are written in Portuguese, like the rest of the project's
base data, and the English build has been showing them untranslated. The rest of
the project solves this with renderers: base data stays Portuguese, and a script
in scripts/english_renderers.txt swaps the surface before the English ROM is
built. This is the dex's half of that -- the table, and the check that the table
stays complete.

  --extract   refresh docs/arauna/ARAUNA_DEX_TEXT.csv from pokedex_text.h,
              keeping every English line already written
  --check     report how much is translated and whether it fits the dex page
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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

ENTRY = re.compile(r'const u8 g(?P<sym>\w+?)(?P<dex>\d{3})PokedexText\[\] = _\(\n'
                   r'(?P<body>(?:    "[^"]*"\n?)+)\);')


def flatten(body: str) -> str:
    return re.sub(r"\s+", " ",
                  " ".join(re.findall(r'"([^"]*)"', body)).replace("\\n", " ")).strip()


def source_entries():
    text = TEXT.read_text(encoding="utf-8")
    return [(m.group("dex"), m.group("sym"), flatten(m.group("body")))
            for m in ENTRY.finditer(text)]


def existing() -> dict[str, str]:
    if not TABLE.exists():
        return {}
    return {row["arauna_dex"]: row.get("en", "")
            for row in csv.DictReader(TABLE.open(encoding="utf-8"))}


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--extract", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    entries = source_entries()
    have = existing()

    if args.extract:
        with TABLE.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["arauna_dex", "symbol", "pt", "en"])
            for dex, sym, pt in entries:
                writer.writerow([dex, sym, pt, have.get(dex, "")])
        print(f"wrote {TABLE.relative_to(ROOT)}: {len(entries)} entries, "
              f"{sum(1 for d, _, _ in entries if have.get(d))} already translated")
        return 0

    done = [(d, have[d]) for d, _, _ in entries if have.get(d)]
    long_lines = [(d, line) for d, en in done for line in wrap(en) if len(line) > LINE_WIDTH]
    too_many = [d for d, en in done if len(wrap(en)) > LINES]
    CHARS = charmap_chars()
    non_ascii = [d for d, en in done if set(en) - CHARS]

    print(f"{len(done)}/{len(entries)} translated")
    print(f"  lines over {LINE_WIDTH} chars: {len(long_lines)}")
    print(f"  entries over {LINES} lines:    {len(too_many)} {too_many[:6]}")
    print(f"  unencodable entries:          {len(non_ascii)} {non_ascii[:6]}")
    return 0 if not (long_lines or too_many or non_ascii) else 1


if __name__ == "__main__":
    sys.exit(main())

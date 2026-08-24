#!/usr/bin/env python3
"""Apply the Arauna Pokedex entries: category, height, weight and description.

The project's pokedex.json carries the entries in Portuguese, but the build is
English-only, so the English text lives beside it in
data/text/arauna/pokedex_en.json and is edited there rather than here.

Everything else is taken from pokedex.json directly. Height and weight are
converted to the units the struct stores: decimetres and hectograms, the same
scale vanilla uses (Bulbasaur's 0.7 m and 6.9 kg are 7 and 69).

Descriptions are wrapped here rather than written pre-broken, so the text can
be edited as flowing prose. Vanilla entries run to four lines and reach 46
characters; this keeps to 40 over at most four lines and refuses anything that
will not fit, which is the failure a player would otherwise meet as text
spilling out of the box.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import textwrap

ROOT = pathlib.Path(__file__).resolve().parents[2]
ENTRIES_H = ROOT / "src" / "data" / "pokemon" / "pokedex_entries.h"
TEXT_H = ROOT / "src" / "data" / "pokemon" / "pokedex_text.h"
EN = ROOT / "data" / "text" / "arauna" / "pokedex_en.json"
LINE_WIDTH = 40
MAX_LINES = 4
CATEGORY_LIMIT = 11


def dex_constants() -> dict[int, str]:
    """National Dex number to its NATIONAL_DEX_* constant."""
    text = (ROOT / "include" / "constants" / "pokedex.h").read_text(encoding="utf-8")
    order = re.findall(r"^\s*NATIONAL_DEX_([A-Z0-9_]+),", text[text.index("enum {"):], re.M)
    return {i: f"NATIONAL_DEX_{n}" for i, n in enumerate(order) if n != "NONE"}


def wrap(text: str) -> list[str]:
    lines = textwrap.wrap(" ".join(text.split()), width=LINE_WIDTH)
    if len(lines) > MAX_LINES:
        raise ValueError(f"needs {len(lines)} lines at {LINE_WIDTH} chars: {text!r}")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pokedex", type=pathlib.Path)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    dex = {e["id"]: e for e in json.loads(args.pokedex.read_text(encoding="utf-8"))["pokemon"]}
    english = json.loads(EN.read_text(encoding="utf-8")) if EN.exists() else {}
    constants = dex_constants()

    entries = ENTRIES_H.read_text(encoding="utf-8")
    texts = TEXT_H.read_text(encoding="utf-8")
    done = skipped = 0
    problems: list[str] = []

    for number in sorted(dex):
        constant = constants.get(number)
        source = english.get(str(number))
        if constant is None or source is None:
            skipped += 1
            continue
        entry = dex[number]

        category = source["category"].upper()
        if len(category) > CATEGORY_LIMIT:
            problems.append(f"{number:03d} category {category!r} is {len(category)} chars, max {CATEGORY_LIMIT}")
            continue
        try:
            lines = wrap(source["text"])
        except ValueError as exc:
            problems.append(f"{number:03d} {exc}")
            continue

        block = re.search(rf"(\[{constant}\]\s*=\s*\{{)(.*?)(\n    \}},?)", entries, re.S)
        if not block:
            problems.append(f"{number:03d}: no entry block for {constant}")
            continue
        body = block.group(2)
        body = re.sub(r'(\.categoryName\s*=\s*_\(")[^"]*("\))', lambda m: m.group(1) + category + m.group(2), body, count=1)
        body = re.sub(r"(\.height\s*=\s*)\d+", rf"\g<1>{round(entry['height'] * 10)}", body, count=1)
        body = re.sub(r"(\.weight\s*=\s*)\d+", rf"\g<1>{round(entry['weight'] * 10)}", body, count=1)
        entries = entries[:block.start(2)] + body + entries[block.end(2):]

        symbol = re.search(r"\.description\s*=\s*(g\w+PokedexText)", body)
        if symbol:
            payload = "\n".join(f'    "{line}\\n"' for line in lines[:-1] + [""])[:-len('    ""')].rstrip("\n")
            payload = "\n".join(f'    "{line}\\n"' for line in lines[:-1]) + ("\n" if len(lines) > 1 else "") + f'    "{lines[-1]}");'
            pattern = re.compile(rf"(const u8 {symbol.group(1)}\[\] = _\(\n)(?:\s*\"[^\"]*\"\n?)+\);")
            if pattern.search(texts):
                texts = pattern.sub(lambda m: m.group(1) + payload, texts, count=1)
        done += 1

    for line in problems:
        print(f"  {line}")
    if args.apply and not problems:
        ENTRIES_H.write_text(entries, encoding="utf-8")
        TEXT_H.write_text(texts, encoding="utf-8")

    verb = "applied" if (args.apply and not problems) else "would apply"
    print(f"\n{done} entries {verb}; {skipped} without English text; {len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

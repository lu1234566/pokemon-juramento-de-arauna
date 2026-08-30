#!/usr/bin/env python3
"""Re-wrap the dialogue that a rename made too wide to render.

Renaming TEAM AQUA and DEVON CORP to CONSORCIO HORIZONTE added ten characters
to lines that were already close to the edge of the message box, and the line
breaks were left where they were. Twenty-seven lines now run past the widest
line Emerald itself renders, which on screen means the end of the line is
simply not drawn. Three of them also read "CONSORCIO HORIZONTEORATION",
because "DEVON CORP" was replaced inside "DEVON CORPORATION".

This pass touches only the strings that are actually too wide. For each one it
keeps the pages -- \\p stays exactly where the writer put it, so the pacing of
the dialogue does not move -- and re-flows the words inside a page, breaking at
\\n for the second line and \\l for each line after that, which is the same
convention the rest of the game uses. Wrapping is greedy against the measured
ceiling, so a line ends when the next word would not fit.

Strings holding a laid-out table ({CLEAR_TO}) are left alone: their line breaks
are the layout, not prose.

  --check   report what would change
  --write   rewrite the scripts
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from textwidth import Ruler  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
VANILLA = "c210195e"

# One text is a run of consecutive .string lines; the last ends in $ or \p.
BLOCK = re.compile(r'(?P<block>(?:\t\.string "(?:[^"\\]|\\.)*"\n)+)')
STRING_LINE = re.compile(r'\t\.string "((?:[^"\\]|\\.)*)"\n')

# "DEVON CORP" was replaced inside "DEVON CORPORATION" and left the tail behind.
LEFTOVERS = {"CONSORCIO HORIZONTEORATION": "CONSORCIO HORIZONTE"}

REGION_MAP = ROOT / "src/data/region_map/region_map_sections.json"
PLACE_NAMES = ROOT / "docs/arauna/ARAUNA_PLACE_NAMES.csv"


def unbreakable() -> list[str]:
    """Names that must not be split across a line break.

    Two reasons, and they agree. A place reads badly with its name cut in half,
    and the English renderers find their text by searching for a phrase -- so
    putting a newline inside CONSORCIO HORIZONTE would leave a renderer looking
    for something that is no longer there.

    The list is generated: the names build_place_names.py settled on, which
    includes the prose forms the map label is too short to hold (MEMORIAL DOS
    NOMES against the map's MEMORIAL NOMES), plus the region map's own names
    and the company.
    """
    import csv
    import json
    names = {section["name"] for section
             in json.loads(REGION_MAP.read_text(encoding="utf-8"))["map_sections"]}
    if PLACE_NAMES.exists():
        names |= {row["arauna_name"] for row
                  in csv.DictReader(PLACE_NAMES.open(encoding="utf-8"))
                  if row["arauna_name"]}
    return sorted((n for n in names | {"CONSORCIO HORIZONTE"} if " " in n),
                  key=len, reverse=True)


def renderer_anchors() -> set[str]:
    r"""Phrases an English renderer searches the base text for.

    A renderer locates the block it rewrites by a fragment quoted out of the
    dialogue -- "rated for the number of collisions", "S.S. TIDAL" -- so a line
    break dropped inside one leaves it searching for text that no longer exists
    as a contiguous string. Every literal in those scripts that could be such a
    fragment is treated as one word here. What a renderer *writes* is not: those
    carry \n, \p or a terminating $, which is how they are told apart.
    """
    found = set()
    for name in subprocess.run(["git", "ls-files", "scripts"], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.split():
        if not name.endswith(".py"):
            continue
        for double, single in re.findall(r'"([^"\n]*)"|\'([^\'\n]*)\'',
                                         (ROOT / name).read_text(encoding="utf-8")):
            literal = double or single
            if " " not in literal or "\\" in literal or "{" in literal or "$" in literal:
                continue
            found.add(literal)
    return found


def ceiling(ruler: Ruler, files: list[str]) -> int:
    """The widest placeholder-free line the original game renders."""
    best = 0
    for name in files:
        original = subprocess.run(["git", "show", f"{VANILLA}:{name}"], cwd=ROOT,
                                  capture_output=True, text=True).stdout
        for found in re.finditer(r'\.string "((?:[^"\\]|\\.)*)"', original):
            for line in ruler.lines(found.group(1)):
                if "{" not in line:
                    best = max(best, ruler.width(line))
    return best


GLUE = "\x01"  # stands in for the space inside a name while wrapping


def rewrap(ruler: Ruler, text: str, limit: int, whole: list[str]) -> str:
    r"""Re-flow the words of each page, keeping \p where it is."""
    out_pages = []
    for page in re.split(r"(\\p)", text):
        if page == "\\p" or not page:
            out_pages.append(page)
            continue
        end = ""
        if page.endswith("$"):
            page, end = page[:-1], "$"
        for name in whole:
            page = page.replace(name, name.replace(" ", GLUE))
        words = [w.replace(GLUE, " ")
                 for w in re.split(r"\\n|\\l|\s+", page) if w]
        lines, current = [], ""
        for word in words:
            candidate = f"{current} {word}" if current else word
            if current and ruler.width(candidate) > limit:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        # \n opens the second line of a page; \l scrolls for every line after.
        joined = lines[0] if lines else ""
        if len(lines) > 1:
            joined += "\\n" + "\\l".join(lines[1:])
        out_pages.append(joined + end)
    return "".join(out_pages)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    ruler = Ruler()
    files = [f for f in subprocess.run(["git", "ls-files", "data"], cwd=ROOT,
                                       capture_output=True, text=True,
                                       check=True).stdout.split() if f.endswith(".inc")]
    limit = ceiling(ruler, files)
    # A phrase too wide to fit on a line of its own cannot be kept whole; it
    # would make the string unwrappable.
    def fits(phrase: str) -> bool:
        return ruler.width(phrase) <= limit

    places = [n for n in unbreakable() if fits(n)]
    anchors = sorted((a for a in renderer_anchors() if fits(a)), key=len, reverse=True)
    print(f"wrapping to {limit}px, the widest line vanilla renders; "
          f"{len(places)} names kept whole, {len(anchors)} renderer anchors watched")

    touched = 0
    for name in files:
        path = ROOT / name
        original = path.read_text(encoding="utf-8", errors="replace")
        body = original
        for stale, fixed in LEFTOVERS.items():
            if stale in body:
                print(f"  {name}: {stale} -> {fixed}")
                body = body.replace(stale, fixed)

        def one(found):
            nonlocal touched
            block = found.group("block")
            parts = STRING_LINE.findall(block)
            text = "".join(parts)
            if "{CLEAR_TO" in text or "{FONT" in text:
                return block
            if all("{" in line or ruler.width(line) <= limit
                   for line in ruler.lines(text)):
                return block
            # An anchor a renderer searches for lives inside one .string line;
            # if the re-flow drops a break into the middle of one, the renderer
            # stops finding it. Glue only the anchors that actually broke, and
            # try again, so wrapping stays as free as it can be.
            glue = list(places)
            for _ in range(8):
                wrapped = rewrap(ruler, text, limit, glue)
                after = set(re.split(r"\\[nlp]", wrapped))
                broke = [a for a in anchors
                         if any(a in line for line in parts)
                         and not any(a in line for line in after)
                         and a not in glue]
                if not broke:
                    break
                glue = broke + glue
            if wrapped == text:
                return block
            touched += 1
            print(f"  {name}\n    - {text}\n    + {wrapped}")
            indent = "\t.string "
            pieces = re.findall(r'.*?(?:\\[nlp]|\$)|.+', wrapped)
            return "".join(f'{indent}"{piece}"\n' for piece in pieces)

        updated = BLOCK.sub(one, body)
        if args.write and updated != original:
            path.write_text(updated, encoding="utf-8")

    print(f"{touched} strings re-wrapped")
    return 0


if __name__ == "__main__":
    sys.exit(main())

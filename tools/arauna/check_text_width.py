#!/usr/bin/env python3
"""No line of dialogue may be wider than the widest line vanilla ships.

Emerald's message box has a fixed width and nothing warns you when a line runs
past it -- the text is simply cut off on screen, and the .inc file looks fine.
That is easy to do by accident: renaming TEAM AQUA to CONSORCIO HORIZONTE adds
ten characters to a line that was already near the edge.

The ceiling is not a number chosen here. It is measured from the reset-to-
vanilla tree: the widest placeholder-free line the original game itself
renders. Anything the project writes that goes past it is wider than the game
was ever built to show.

Lines containing a runtime placeholder are reported separately and not failed,
because {PLAYER} and {STR_VAR_1} are whatever the player made them and vanilla
already gambles on that.

  (no arguments)  fail if any line is too wide
  --ceiling       just print the measured ceiling and the widest lines
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
STRING = re.compile(r'\.string "((?:[^"\\]|\\.)*)"')


# A description in the bag is drawn in a much narrower window than a message
# box, so it gets its own ceiling measured from its own file. The literals are
# adjacent strings the compiler joins, not one _("").
DESCRIPTIONS = ["src/data/text/item_descriptions.h"]
DESCRIPTION_BLOCK = re.compile(r'_\(\n((?:\s*"(?:[^"\\]|\\.)*"\n?)+)\);')

# Files drawn in a window narrower than the message box, which the global
# ceiling is therefore far too generous for. These are not files that merely
# happen to have no long line: contest_strings.inc holds 226 measurable lines
# and not one of them passes 144px, where the next narrowest file in the game
# reaches 184px and the rest sit at 196-202px. That is a window, not a
# coincidence, and a line written to the 208px ceiling is cut off inside it.
NARROW = ["data/text/contest_strings.inc"]


def scripts() -> list[str]:
    return [f for f in subprocess.run(["git", "ls-files", "data"], cwd=ROOT,
                                      capture_output=True, text=True,
                                      check=True).stdout.split() if f.endswith(".inc")]


def described(ruler: Ruler, text: str):
    for block in DESCRIPTION_BLOCK.finditer(text):
        for literal in re.findall(r'"((?:[^"\\]|\\.)*)"', block.group(1)):
            for line in ruler.lines(literal):
                if line and "{" not in line:
                    yield ruler.width(line), line


def measure(ruler: Ruler, text: str):
    """Every rendered line and its width, skipping ones with a placeholder."""
    for found in STRING.finditer(text):
        for line in ruler.lines(found.group(1)):
            if "{" not in line:
                yield ruler.width(line), line


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ceiling", action="store_true")
    args = parser.parse_args()

    ruler = Ruler()
    files = scripts()

    ceiling, widest = 0, ""
    for name in files:
        original = subprocess.run(["git", "show", f"{VANILLA}:{name}"], cwd=ROOT,
                                  capture_output=True, text=True).stdout
        for width, line in measure(ruler, original):
            if width > ceiling:
                ceiling, widest = width, line

    over = []
    for name in files:
        cap = ceiling
        if name in NARROW:
            original = subprocess.run(["git", "show", f"{VANILLA}:{name}"], cwd=ROOT,
                                      capture_output=True, text=True).stdout
            cap = max(width for width, _ in measure(ruler, original))
            print(f"widest {Path(name).name} line vanilla renders: {cap}px")
        for width, line in measure(ruler, (ROOT / name).read_text(encoding="utf-8",
                                                                  errors="replace")):
            if width > cap:
                over.append((width, name, line))
    over.sort(reverse=True)

    for name in DESCRIPTIONS:
        original = subprocess.run(["git", "show", f"{VANILLA}:{name}"], cwd=ROOT,
                                  capture_output=True, text=True).stdout
        cap = max(width for width, _ in described(ruler, original))
        for width, line in described(ruler, (ROOT / name).read_text(encoding="utf-8")):
            if width > cap:
                over.append((width, name, line))
        print(f"widest {Path(name).name} line vanilla renders: {cap}px")

    print(f"widest line vanilla renders: {ceiling}px  \"{widest}\"")
    if args.ceiling:
        return 0
    if not over:
        print(f"text width: OK ({len(files)} script files, nothing past {ceiling}px)")
        return 0
    print(f"text width: {len(over)} lines are wider than the game ever renders",
          file=sys.stderr)
    for width, name, line in over:
        print(f"  {width:4}px  {name}\n            {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

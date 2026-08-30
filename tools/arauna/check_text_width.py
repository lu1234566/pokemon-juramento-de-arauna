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


def scripts() -> list[str]:
    return [f for f in subprocess.run(["git", "ls-files", "data"], cwd=ROOT,
                                      capture_output=True, text=True,
                                      check=True).stdout.split() if f.endswith(".inc")]


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
        for width, line in measure(ruler, (ROOT / name).read_text(encoding="utf-8",
                                                                  errors="replace")):
            if width > ceiling:
                over.append((width, name, line))
    over.sort(reverse=True)

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

#!/usr/bin/env python3
"""Check every overworld sprite sheet against the frames the game asks it for.

An overworld sprite is a sheet of frames and a table that names them by index.
Nothing checks that the sheet is long enough: replace a nine-frame sheet with a
six-frame one and the build succeeds, the sprite stands still correctly, and
the walk cycle reads whatever bytes come after the image. That is what a broken
animation looks like, and it looks like it only in motion, which is why it
survives a static check and a screenshot both.

So: read the sheets out of `object_event_graphics.h`, read the frame tables out
of `object_event_pic_tables.h`, and say whether every index a table names is a
frame the sheet actually has.

    python3 tools/audit/check_overworld_sprites.py
"""
from __future__ import annotations

import pathlib
import re
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
GRAPHICS = ROOT / "src/data/object_events/object_event_graphics.h"
TABLES = ROOT / "src/data/object_events/object_event_pic_tables.h"


def sheets():
    """symbol -> (path, frame width in tiles, frame height in tiles)."""
    out = {}
    text = GRAPHICS.read_text(encoding="utf-8", errors="replace")
    for symbol, path, args in re.findall(
            r"(gObjectEvent\w+)\[\]\s*=\s*INCGFX_U32\(\s*\"([^\"]+)\"[^)]*?"
            r"(\"-mwidth \d+ -mheight \d+\")?\s*\)", text):
        m = re.search(r"-mwidth (\d+) -mheight (\d+)", args or "")
        out[symbol] = (path, int(m.group(1)) if m else None, int(m.group(2)) if m else None)
    return out


def tables():
    """table name -> list of (sheet symbol, width, height, frame index)."""
    out = {}
    text = TABLES.read_text(encoding="utf-8", errors="replace")
    for name, body in re.findall(r"(sPicTable_\w+)\[\]\s*=\s*\{(.*?)\n\};", text, re.S):
        frames = re.findall(r"overworld_frame\(\s*(\w+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
                            body)
        if frames:
            out[name] = [(s, int(w), int(h), int(i)) for s, w, h, i in frames]
    return out


def main():
    known = sheets()
    problems = []
    checked = 0
    for name, frames in sorted(tables().items()):
        for symbol, w, h, index in frames:
            entry = known.get(symbol)
            if entry is None:
                problems.append("%s names %s, which no sheet defines" % (name, symbol))
                continue
            path = ROOT / entry[0]
            if not path.is_file():
                problems.append("%s: %s is missing" % (name, entry[0]))
                continue
            try:
                width, height = Image.open(path).size
            except Exception as why:                        # noqa: BLE001
                problems.append("%s: %s will not open (%s)" % (name, entry[0], why))
                continue
            per_frame = (w * 8) * (h * 8)
            available = (width * height) // per_frame
            checked += 1
            if index >= available:
                problems.append(
                    "%s asks %s for frame %d, but %s is %dx%d - %d frame(s) of %dx%d"
                    % (name, symbol, index, entry[0], width, height,
                       available, w * 8, h * 8))
    print("%d frame reference(s) checked across %d table(s)" % (checked, len(tables())))
    for line in problems:
        print("  " + line)
    print("%d problem(s)" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())

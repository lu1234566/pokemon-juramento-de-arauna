#!/usr/bin/env python3
"""Reject characters that the GBA charmap cannot encode.

``preproc`` fails the build on any character inside a ``.string`` that has no
entry in ``charmap.txt``. Nothing else in the safety suite catches this: the
localization check only reads the Arauna text packs, and the map scripts are
never parsed for encodability. A stray typographic dash or a character pasted
from another keyboard layout therefore survives every Python validator and only
explodes at build time, which is exactly when the toolchain is hardest to reach.

This check reads the real charmap and validates every ``.string`` literal under
``data/``, so the failure surfaces here instead.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHARMAP = ROOT / "charmap.txt"

# Escapes and placeholders that preproc resolves before encoding.
CONTROL_RE = re.compile(r"\\[a-zA-Z0-9_]+|\{[^}]*\}|\\\\|\\\"")
STRING_RE = re.compile(r'\.string\s+"((?:[^"\\]|\\.)*)"')
# charmap entries look like:  'X' = AB   or   ESCAPE_NAME = AB
CHARMAP_SINGLE_RE = re.compile(r"^'(.+?)'\s*=", re.MULTILINE)


def supported_characters() -> set[str]:
    text = CHARMAP.read_text(encoding="utf-8")
    chars = set(CHARMAP_SINGLE_RE.findall(text))
    # Multi-byte entries are written as the literal character too.
    chars.discard("\\'")
    chars.add("'")
    return chars


def scan(paths: list[Path], allowed: set[str]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        try:
            source = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{path.relative_to(ROOT)}: file is not valid UTF-8")
            continue
        for number, line in enumerate(source.splitlines(), 1):
            for literal in STRING_RE.findall(line):
                visible = CONTROL_RE.sub("", literal)
                bad = sorted({c for c in visible if c not in allowed})
                if bad:
                    rendered = " ".join(f"U+{ord(c):04X} {c!r}" for c in bad)
                    errors.append(
                        f"{path.relative_to(ROOT)}:{number}: "
                        f"character not in charmap.txt: {rendered}"
                    )
    return errors


def main() -> int:
    allowed = supported_characters()
    if len(allowed) < 100:
        print("charmap.txt could not be parsed", file=sys.stderr)
        return 1

    paths = sorted(ROOT.glob("data/**/*.inc"))
    errors = scan(paths, allowed)
    if errors:
        for error in errors[:40]:
            print(error, file=sys.stderr)
        if len(errors) > 40:
            print(f"... and {len(errors) - 40} more", file=sys.stderr)
        print(
            f"\n{len(errors)} unencodable string(s): the build would fail in preproc.",
            file=sys.stderr,
        )
        return 1

    print(f"Charmap check passed: every .string in {len(paths)} files is encodable")
    return 0


if __name__ == "__main__":
    sys.exit(main())

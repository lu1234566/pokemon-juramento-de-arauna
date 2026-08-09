#!/usr/bin/env python3
"""Reject assembler directives that `as` will not recognise.

A malformed directive fails the build with ``Error: unknown pseudo-op``, which
names a line number but not the file the reader is actually looking at, and it
only appears after the toolchain has already compiled most of the project. The
usual cause is a generated or hand-edited text block where the leading dot got
separated from its directive (``.<tab>string`` instead of ``.string``) or lost
entirely (``string "..."``), which still looks plausible to the eye and still
parses as a normal line to every other check in this suite.

The allowlist below is the set of directives this repository actually uses;
anything outside it is far more likely to be a typo than a new construct, and
adding a genuinely new directive here is a one-line change.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

KNOWN_DIRECTIVES = {
    "align", "braille", "byte", "else", "endif", "endm", "equ", "global",
    "if", "ifndef", "include", "macro", "set", "string",
    # Common assembler forms that are valid even if unused today.
    "2byte", "4byte", "ascii", "asciz", "endr", "fill", "hword", "incbin",
    "int", "long", "rept", "section", "short", "space", "word",
}

DIRECTIVE_RE = re.compile(r"^\s*\.\s*([A-Za-z_][A-Za-z0-9_]*)")
# A lone dot, or a dot separated from its directive by whitespace.
LONE_DOT_RE = re.compile(r"^\s*\.(\s|$)")
# A directive that lost its leading dot entirely.
MISSING_DOT_RE = re.compile(r"^\s+(string|byte|align|incbin|include|set|equ)\s")


def check(path: Path) -> list[str]:
    problems: list[str] = []
    name = path.relative_to(ROOT)

    for number, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = raw.split("@", 1)[0]
        if not line.strip():
            continue

        if LONE_DOT_RE.match(line):
            problems.append(
                f"{name}:{number}: a dot stands alone; the directive is "
                f"detached or missing -> {raw.strip()[:60]!r}"
            )
            continue

        if MISSING_DOT_RE.match(line):
            problems.append(
                f"{name}:{number}: directive is missing its leading dot "
                f"-> {raw.strip()[:60]!r}"
            )
            continue

        found = DIRECTIVE_RE.match(line)
        if found and found.group(1) not in KNOWN_DIRECTIVES:
            problems.append(
                f"{name}:{number}: unknown directive '.{found.group(1)}' "
                f"-> {raw.strip()[:60]!r}"
            )

    return problems


def main() -> int:
    paths = sorted(ROOT.glob("data/**/*.inc"))
    problems: list[str] = []
    for path in paths:
        problems.extend(check(path))

    if problems:
        for problem in problems[:30]:
            print(problem, file=sys.stderr)
        if len(problems) > 30:
            print(f"... and {len(problems) - 30} more", file=sys.stderr)
        print(
            f"\n{len(problems)} malformed directive(s): "
            "the assembler would fail with 'unknown pseudo-op'.",
            file=sys.stderr,
        )
        return 1

    print(f"Directive check passed: {len(paths)} .inc files assemble cleanly")
    return 0


if __name__ == "__main__":
    sys.exit(main())

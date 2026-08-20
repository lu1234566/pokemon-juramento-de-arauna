#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRA_FILES = (
    ROOT / "data" / "text" / "apprentice.inc",
    ROOT / "data" / "text" / "tv.inc",
)

# Keep inherited engine identifiers untouched. This renderer edits only the
# payload of `.string` directives in Battle Frontier runtime text.
REPLACEMENTS = (
    ("FRONTIER BRAINS", "CIRCUIT MASTERS"),
    ("Frontier Brains", "Circuit Masters"),
    ("FRONTIER BRAIN", "CIRCUIT MASTER"),
    ("Frontier Brain", "Circuit Master"),
    ("FRONTIER PASS", "CIRCUIT PASS"),
    ("Frontier Pass", "Circuit Pass"),
    ("BATTLE FRONTIER", "CIRCUITO"),
    ("Battle Frontier", "CIRCUITO"),
    ("MR. SCOTT", "SEU BENTO"),
    ("Mr. Scott", "Seu Bento"),
    ("SCOTT", "SEU BENTO"),
    ("Scott", "Seu Bento"),
)

STRING_LINE = re.compile(r'^(?P<prefix>\s*\.string\s+")(?P<body>(?:\\.|[^"\\])*)(?P<suffix>".*)$')


def target_files() -> list[Path]:
    files = sorted((ROOT / "data" / "maps").glob("BattleFrontier_*/scripts.inc"))
    files.extend(path for path in EXTRA_FILES if path.is_file())
    return files


def replace_visible_line(line: str) -> tuple[str, int]:
    match = STRING_LINE.match(line)
    if not match:
        return line, 0
    body = match.group("body")
    changed = 0
    for old, new in REPLACEMENTS:
        count = body.count(old)
        if count:
            body = body.replace(old, new)
            changed += count
    return f'{match.group("prefix")}{body}{match.group("suffix")}', changed


def render(source: str) -> tuple[str, int]:
    lines = source.splitlines(keepends=True)
    out: list[str] = []
    total = 0
    for raw in lines:
        newline = "\n" if raw.endswith("\n") else ""
        core = raw[:-1] if newline else raw
        rendered, count = replace_visible_line(core)
        out.append(rendered + newline)
        total += count
    return "".join(out), total


def validate(rel: str, source: str, rendered: str) -> None:
    # Strip every visible string payload and prove the surrounding script is
    # byte-for-byte equivalent. This catches accidental label/logic changes.
    def mask(text: str) -> str:
        result: list[str] = []
        for raw in text.splitlines(keepends=True):
            newline = "\n" if raw.endswith("\n") else ""
            core = raw[:-1] if newline else raw
            match = STRING_LINE.match(core)
            if match:
                core = f'{match.group("prefix")}<VISIBLE>{match.group("suffix")}'
            result.append(core + newline)
        return "".join(result)

    if mask(source) != mask(rendered):
        raise ValueError(f"{rel}: non-string structure changed")

    for line in rendered.splitlines():
        match = STRING_LINE.match(line)
        if not match:
            continue
        body = match.group("body")
        for old, _ in REPLACEMENTS:
            if old in body:
                raise ValueError(f"{rel}: legacy visible term survived: {old}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize visible Battle Circuit terminology in English runtime text.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")

    files = target_files()
    if not files:
        raise ValueError("no Battle Frontier runtime text files found")

    total_replacements = 0
    changed_files = 0
    rendered_files: list[tuple[Path, str]] = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        source = path.read_text(encoding="utf-8")
        output, count = render(source)
        validate(rel, source, output)
        total_replacements += count
        if output != source:
            changed_files += 1
            rendered_files.append((path, output))

    if total_replacements == 0:
        raise ValueError("no visible Battle Circuit legacy terminology found")

    if args.in_place:
        for path, output in rendered_files:
            path.write_text(output, encoding="utf-8")

    print(
        "Battle Circuit terminology overlay OK: "
        f"{total_replacements} visible replacements across {changed_files}/{len(files)} files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

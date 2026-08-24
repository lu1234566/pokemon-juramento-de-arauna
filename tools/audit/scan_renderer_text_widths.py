#!/usr/bin/env python3
"""Scan every English renderer for text payloads whose visible segments exceed
the 32-character box width the renderers themselves enforce.

The per-renderer validators raise on the *first* violation they meet, which
makes the official build fail one message at a time. This scanner applies the
same rule to every payload in every renderer at once so the whole backlog is
visible in a single pass.
"""
from __future__ import annotations

import ast
import pathlib
import re
import sys

MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")
CONTROL_RE = re.compile(r"\\[npl]")
# Payload strings are the ones carrying script text control codes.
PAYLOAD_RE = re.compile(r"\\[npl]|\$$")
# Renderers also hold regexes and C snippets that happen to contain those
# sequences; they are code, not dialogue, and must not be width-checked.
CODE_MARKERS = ("(?", "[^", "\\\\", "(?P<", ".*?", "_(", "[] =")
# Validator failure messages are f-string fragments, not dialogue.
MESSAGE_PREFIXES = (": ", "bank ", "must ")


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    # Widest expansion the renderers use for the player placeholder.
    cleaned = cleaned.replace("{PLAYER}", "PLAYERX")
    cleaned = cleaned.replace("{UP_ARROW}", "^")
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def scan(path: pathlib.Path) -> list[tuple[int, str, str]]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        print(f"{path}: unparsable: {exc}", file=sys.stderr)
        return []
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        payload = node.value
        if not PAYLOAD_RE.search(payload):
            continue
        if any(marker in payload for marker in CODE_MARKERS):
            continue
        if payload.startswith(MESSAGE_PREFIXES):
            continue
        for segment in visible_segments(payload):
            if len(segment) > MAX_VISIBLE_WIDTH:
                findings.append((node.lineno, segment, payload))
    return findings


def main() -> int:
    root = pathlib.Path(__file__).resolve().parents[2]
    manifest = (root / "scripts" / "english_renderers.txt").read_text(encoding="utf-8")
    names = [
        line.strip()
        for line in manifest.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    # A manifest renderer usually delegates to an unchecked base module holding
    # the payloads, so audit both halves of each pair.
    renderers = []
    for name in names:
        for candidate in (name, name.replace("_checked.py", ".py")):
            path = root / "scripts" / candidate
            if path.exists() and path not in renderers:
                renderers.append(path)
    total = 0
    for renderer in renderers:
        for lineno, segment, _payload in scan(renderer):
            total += 1
            print(f"{renderer.relative_to(root)}:{lineno}: {len(segment)} chars: {segment!r}")
    print(f"\n{total} oversized visible segment(s) across {len(renderers)} renderers.")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())

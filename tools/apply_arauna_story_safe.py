#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import apply_arauna_story as base


def safe_escape_asm(text: str) -> str:
    """Keep Emerald control codes intact and sanitize generated prose for its charset."""
    return text.replace("_", " ").replace('"', '\\"')


def safe_process_script(path: Path) -> tuple[int, int]:
    map_name = path.parent.name
    if not map_name.startswith(base.TARGET_PREFIXES):
        return 0, 0

    original = path.read_text(encoding="utf-8")
    changed_blocks = 0
    total_blocks = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changed_blocks, total_blocks
        total_blocks += 1
        label = match.group("label")
        body = match.group("body")
        msg = base.story_message(label, body, map_name)

        if msg is None:
            # Entity replacements are allowed only inside text bodies.
            body2 = base.apply_term_replacements(body)
            if body2 != body:
                changed_blocks += 1
            return f"{label}:\n{body2}"

        changed_blocks += 1
        return f"{label}:\n{base.emit_message(msg)}"

    # Critical safety rule: only replace matched dialogue blocks. Never run
    # AQUA/MAGMA substitutions over event code, labels, flags, LOCALIDs, etc.
    replaced = base.TEXT_BLOCK_RE.sub(repl, original)

    # Defensive invariant: outside dialogue bodies the script must be identical.
    marker = "\t.string \"<ARAUANA_TEXT_BLOCK>\"\n"
    before_structure = base.TEXT_BLOCK_RE.sub(
        lambda m: f"{m.group('label')}:\n{marker}", original
    )
    after_structure = base.TEXT_BLOCK_RE.sub(
        lambda m: f"{m.group('label')}:\n{marker}", replaced
    )
    if before_structure != after_structure:
        raise RuntimeError(f"Non-dialogue script structure changed: {path}")

    if replaced != original:
        path.write_text(replaced, encoding="utf-8")
    return changed_blocks, total_blocks


def main() -> None:
    # base.emit_message resolves base.escape_asm at runtime, so patch both unsafe
    # hooks before delegating to the canonical story implementation.
    base.escape_asm = safe_escape_asm
    base.process_script = safe_process_script
    base.main()


if __name__ == "__main__":
    main()

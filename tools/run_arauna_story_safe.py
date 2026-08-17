#!/usr/bin/env python3
from __future__ import annotations

import re

import apply_arauna_story_safe as safe


def token_safe_escape_asm(text: str) -> str:
    """Sanitize prose without corrupting Emerald placeholders such as {STR_VAR_1}."""
    parts = re.split(r"(\{[^}]+\})", text)
    cleaned: list[str] = []
    for part in parts:
        if part.startswith("{") and part.endswith("}"):
            cleaned.append(part)
        else:
            cleaned.append(part.replace("_", " "))
    return "".join(cleaned).replace('"', '\\"')


def main() -> None:
    safe.safe_escape_asm = token_safe_escape_asm
    safe.main()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import re

import render_serra_uivo_story_en as base


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?m)^{re.escape(label)}:\n(?P<body>(?:\t\.string .*\n)+)"
    )


def render_text(source: str, file_key: str) -> str:
    rendered = source
    for label, payloads in base.TARGETS[file_key].items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{file_key}:{label}: expected one string-only text block, found {len(matches)}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_target_bodies(text: str, file_key: str) -> str:
    masked = text
    for label in base.TARGETS[file_key]:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{file_key}: cannot mask missing string-only block {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<SERRA_UIVO_EN>"\n' + masked[end:]
    return masked


# Tighten the base renderer without duplicating its 153-entry authored table.
base.block_pattern = block_pattern
base.render_text = render_text
base.mask_target_bodies = mask_target_bodies


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())

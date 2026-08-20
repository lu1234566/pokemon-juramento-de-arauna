#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import render_shared_trainer_dialogue_identity_en as dialogue

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "src" / "data" / "trainers.h"

REPLACEMENTS = {
    '.trainerName = _("AGENTE"),': ('.trainerName = _("AGENT"),', 26),
    '.trainerName = _("ATIVISTA"),': ('.trainerName = _("ACTIVIST"),', 27),
}


def render(source: str) -> str:
    rendered = source
    for old, (new, expected_count) in REPLACEMENTS.items():
        count = rendered.count(old)
        if count != expected_count:
            raise ValueError(f"expected {expected_count} occurrences of {old!r}, found {count}")
        rendered = rendered.replace(old, new)
    return rendered


def validate(rendered: str) -> None:
    for old, (new, expected_count) in REPLACEMENTS.items():
        if old in rendered:
            raise ValueError(f"Portuguese trainer surface survived: {old}")
        if rendered.count(new) != expected_count:
            raise ValueError(f"expected {expected_count} rendered occurrences of {new!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render shared Arauna trainer names and referenced trainer dialogue in English.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.output and args.in_place:
        parser.error("use either --output or --in-place, not both")

    source = args.input.read_text(encoding="utf-8")
    rendered = render(source)
    validate(rendered)

    dialogue.validate_widths()
    dialogue_source = dialogue.TARGET.read_text(encoding="utf-8")
    dialogue_rendered = dialogue.render(dialogue_source)

    if args.check:
        print(
            "Shared trainer English overlay OK: 53 faction trainer names + "
            f"{len(dialogue.BLOCKS)} Route 116 dialogue blocks validated."
        )
        return 0
    if args.in_place:
        args.input.write_text(rendered, encoding="utf-8")
        if dialogue_rendered != dialogue_source:
            dialogue.TARGET.write_text(dialogue_rendered, encoding="utf-8")
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

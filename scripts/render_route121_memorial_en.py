#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE121 = ROOT / "data" / "maps" / "Route121" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "Route121_Text_OkayMoveOutToMtPyre": (
        ("Okay!", "MEMORIAL DOS NOMES"),
        (
            "HORIZON: Move to the MEMORIAL.\\p",
            "Secure the RECORD-MATRIX first.$",
        ),
    ),
    "Route121_Text_AheadLoomsMtPyre": (
        ("Ahead looms MEMORIAL DOS NOMES", "departed POKéMON"),
        (
            "A boy named CIRO passed here.\\p",
            "He asked if M'BOI's names were\\n",
            "people or just records.\\p",
            "Then he went on alone.$",
        ),
    ),
    "Route121_Text_MtPyrePierSign": (
        ("MEMORIAL DOS NOMES PIER", "old and worn out"),
        (
            "MEMORIAL DOS NOMES PIER\\p",
            "Old names, newer flowers.\\n",
            "The path continues east.$",
        ),
    ),
    "Route121_Text_SafariZoneSign": (
        ("rare POKéMON", "SAFARI ZONE"),
        (
            "ARAUNA WILDLIFE PRESERVE\\n",
            "Observe. Do not disturb.$",
        ),
    ),
}

CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^(?P<label>{re.escape(label)}:)\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render(source: str) -> str:
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target body contains no .string data")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: expected source marker not found: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(source: str) -> str:
    masked = source
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_ROUTE121>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask_targets(source) != mask_targets(rendered):
        raise ValueError("non-dialogue Route 121 structure changed")

    forbidden = (
        "MT. PYRE",
        "SAFARI ZONE",
        "rare POKéMON",
    )
    for label, (_, payloads) in TARGETS.items():
        match = block_pattern(label).search(rendered)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: legacy visible token survived: {token}")

    preserved = (
        "Route121_EventScript_AquaGruntsMoveOut::",
        "LOCALID_ROUTE121_GRUNT_1",
        "LOCALID_ROUTE121_GRUNT_2",
        "LOCALID_ROUTE121_GRUNT_3",
        "VAR_ROUTE121_STATE",
        "Route121_Movement_Grunt1Exit",
        "Route121_Movement_Grunt2Exit",
        "Route121_Movement_Grunt3Exit",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved Route 121 gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 121 HORIZON / Ciro bridge into the Memorial in English."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate_widths()
    source = ROUTE121.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.check:
        print(f"Route 121 Memorial English renderer OK: {len(TARGETS)} text blocks validated.")
        return 0
    if args.in_place:
        ROUTE121.write_text(rendered, encoding="utf-8")
        return 0

    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

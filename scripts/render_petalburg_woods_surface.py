#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "maps" / "PetalburgWoods" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "PetalburgWoods_Text_NotAOneToBeFound": (
        ("Not a one to be found",),
        ("Nothing...\\n", "Still nothing out here.$"),
    ),
    "PetalburgWoods_Text_HaveYouSeenShroomish": (
        ("Boitapuro", "I really love that POKéMON"),
        (
            "Hey. Have you seen anything\\n",
            "unusual in these woods?\\p",
            "I'm tracking changes in the\\n",
            "local POKéMON population.$",
        ),
    ),
    "PetalburgWoods_Text_IWasGoingToAmbushYou": (
        ("ambush you", "MATA DA ESPERA"),
        (
            "I was supposed to wait for you.\\p",
            "You took too long.\\n",
            "So I came to collect.$",
        ),
    ),
    "PetalburgWoods_Text_HandOverThosePapers": (
        ("HORIZONTE RESEARCHER", "Hand over those papers"),
        ("You. RESEARCHER.\\p", "Hand over the field reports!$"),
    ),
    "PetalburgWoods_Text_YouHaveToHelpMe": (
        ("POKéMON TRAINER", "help me"),
        ("Wait! You're a TRAINER, right?\\p", "I need your help!$"),
    ),
    "PetalburgWoods_Text_NoOneCrossesTeamAqua": (
        ("CONSORCIO HORIZONTE", "battle me"),
        (
            "Planning to protect him?\\p",
            "HORIZON leaves no loose ends.\\p",
            "Stand aside or battle me.$",
        ),
    ),
    "PetalburgWoods_Text_YoureKiddingMe": (
        ("You're kidding me",),
        ("No way... You're good!$",),
    ),
    "PetalburgWoods_Text_YouveGotSomeNerve": (
        ("CONSORCIO HORIZONTE", "SERRA DO UIVO"),
        (
            "You've got nerve...\\p",
            "HORIZON is already moving on\\n",
            "SERRA DO UIVO.\\p",
            "This isn't over.$",
        ),
    ),
    "PetalburgWoods_Text_ThatWasAwfullyClose": (
        ("awfully close", "GREAT BALL"),
        (
            "That was close.\\p",
            "These reports are field records\\n",
            "from the sensor network.\\p",
            "Please take this.$",
        ),
    ),
    "PetalburgWoods_Text_TeamAquaAfterSomethingInRustboro": (
        ("CONSORCIO HORIZONTE", "SERRA DO UIVO"),
        (
            "He said HORIZON is moving on\\n",
            "SERRA DO UIVO, right?$",
        ),
    ),
    "PetalburgWoods_Text_ICantBeWastingTime": (
        ("crisis", "wasting time"),
        ("Then I need to get there.\\n", "Now.$"),
    ),
    "PetalburgWoods_Text_YoureLoadedWithItems": (
        ("loaded with items", "GREAT BALL"),
        ("Your BAG is full.\\n", "Can't hand over this GREAT BALL.$"),
    ),
}

BLOCK_RE_TEMPLATE = r'(?m)^{label}:\n(?P<body>(?:\t\.string "[^\n]*"\n)+)'
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


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
    for label, (expected_markers, payloads) in TARGETS.items():
        pattern = re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one .string block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in expected_markers:
            if marker not in body:
                raise ValueError(f"{label}: expected source marker not found: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def validate_rendered(rendered: str) -> None:
    forbidden = (
        "PETALBURG WOODS",
        "DEVON RESEARCHER",
        "RUSTBORO",
        "TEAM AQUA",
        "CONSORCIO HORIZONTE",
        "HORIZONTE",
    )
    for label, (_, payloads) in TARGETS.items():
        pattern = re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        match = pattern.search(rendered)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for payload in payloads:
            line = f'\t.string "{payload}"'
            if line not in body:
                raise ValueError(f"{label}: rendered line missing: {line}")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: legacy visible token survived: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Arauna's first HORIZON forest encounter in English without changing event wiring."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.output and args.in_place:
        parser.error("use either --output or --in-place, not both")

    validate_widths()
    source = args.input.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(rendered)

    if args.check:
        print(f"Horizon forest English renderer OK: {len(TARGETS)} dialogue blocks validated.")
        return 0

    if args.in_place:
        args.input.write_text(rendered, encoding="utf-8")
    elif args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

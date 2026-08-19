#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "maps" / "Route119" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

INTRO = (
    "CIRO: You read every scar\\n",
    "like it owes you an answer.\\p",
    "I want to know what comes\\n",
    "after it.$",
)
DEFEAT = (
    "CIRO: Moving on isn't forgetting\\p",
    "I remember enough to know\\n",
    "loss won't decide everything.$",
)
GIFT = (
    "CIRO: Take this HM.\\p",
    "If you're going to follow me,\\n",
    "stop letting roads slow you.$",
)
EXPLAIN_FLY = (
    "FLY returns you to places\\n",
    "you've already reached.\\p",
    "HORIZON calls that efficiency.\\p",
    "I call it refusing to stay put.$",
)

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "Route119_Text_MayIntro": (("CIRO:", "Voce continua"), INTRO),
    "Route119_Text_MayDefeat": (("CIRO:", "Nao confunda"), DEFEAT),
    "Route119_Text_MayPresentForYou": (("CIRO:", "Voce continua"), GIFT),
    "Route119_Text_MayExplainFly": (("CIRO:", "Voce continua"), EXPLAIN_FLY),
    "Route119_Text_BrendanIntro": (("CIRO:", "Nao confunda"), INTRO),
    "Route119_Text_BrendanDefeat": (("CIRO:", "O HORIZONTE"), DEFEAT),
    "Route119_Text_BrendanIllGiveYouThis": (("CIRO:", "Nao confunda"), GIFT),
    "Route119_Text_BrendanExplainFly": (("CIRO:", "O HORIZONTE"), EXPLAIN_FLY),
    "Route119_Text_ScottWayToGoBeSeeingYou": (
        ("VIAJANTE:", "MATA DO MEIO"),
        (
            "SEU BENTO: {PLAYER}!\\p",
            "I crossed paths with CIRO on the\\n",
            "ridge. He was moving too fast.\\p",
            "Fast is useful. So is knowing\\n",
            "what you're running toward.\\p",
            "Keep your eyes open ahead.$",
        ),
    ),
    "Route119_Text_ScottYouWonAtFortreeGym": (
        ("VIAJANTE:", "LIDIA", "MATA DO MEIO"),
        (
            "... ... ... ... ... ...\\n",
            "... ... ... ... ... Beep!\\p",
            "SEU BENTO: {PLAYER}, it's me!\\p",
            "I heard you cleared LIDIA's\\n",
            "challenge in MATA DO MEIO.\\p",
            "Keep going. Arauna needs people\\n",
            "who notice what others miss.\\p",
            "... ... ... ... ... Click!$",
        ),
    ),
    "Route119_Text_RouteSignFortree": (
        ("ROTA 119", "MATA DO MEIO"),
        ("ROUTE 119\\n", "{RIGHT_ARROW} MATA DO MEIO$"),
    ),
    "Route119_Text_WeatherInstitute": (
        ("INSTITUTO DAS AGUAS",),
        ("WEATHER INSTITUTE$",),
    ),
}

CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def block_pattern(label: str) -> re.Pattern[str]:
    # Some legacy Arauna strings use physical backslash-newline continuations.
    # Replace the whole text-label body up to the next label instead of assuming
    # each .string directive is contained on one physical source line.
    return re.compile(
        rf"(?ms)^(?P<label>{re.escape(label)}:)\n(?P<body>.*?)(?=^[A-Za-z0-9_]+:)",
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
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: expected source marker not found: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def validate_rendered(rendered: str) -> None:
    forbidden = (
        "Voce",
        "Nao confunda",
        "O HORIZONTE",
        "VIAJANTE:",
        "ROTA 119",
        "INSTITUTO DAS AGUAS",
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
                raise ValueError(f"{label}: Portuguese/legacy visible token survived: {token}")

    preserved = (
        "TRAINER_MAY_ROUTE_119_TREECKO",
        "TRAINER_BRENDAN_ROUTE_119_TREECKO",
        "giveitem ITEM_HM_FLY",
        "setflag FLAG_RECEIVED_HM_FLY",
        "VAR_SCOTT_STATE",
        "LOCALID_ROUTE119_SCOTT",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved Route 119 gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 119 Ciro / Seu Bento sequence in English without changing event logic."
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
        print(f"Route 119 Ciro English renderer OK: {len(TARGETS)} text blocks validated.")
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

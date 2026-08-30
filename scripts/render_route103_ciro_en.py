#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "Route103" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

OBSERVE = (
    "CIRO: HORIZON marked this route\\n",
    "as low DESECHANTMENT activity.\\p",
    "Let's see if the field agrees.$",
)
CHALLENGE = (
    "CIRO: ANAHI sent you after me?\\p",
    "Good. I want a clean comparison.\\p",
    "Data or instinct. Let's battle.$",
)
DEFEAT = (
    "CIRO: Hm...\\p",
    "The sensors missed something.\\p",
    "Or I did.$",
)
RETURN = (
    "CIRO: ANAHI will want this.\\p",
    "Don't look pleased.\\p",
    "One battle won't erase the data.$",
)

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "Route103_Text_MayRoute103Pokemon": (("CIRO:", "DESENCANTO"), OBSERVE),
    "Route103_Text_MayLetsBattle": (("CIRO:", "Nao confunda"), CHALLENGE),
    "Route103_Text_MayDefeated": (("CIRO:", "memoria"), DEFEAT),
    "Route103_Text_MayTimeToHeadBack": (("CIRO:", "cicatriz"), RETURN),
    "Route103_Text_BrendanRoute103Pokemon": (("CIRO:", "memoria"), OBSERVE),
    "Route103_Text_BrendanLetsBattle": (("CIRO:", "Nao confunda"), CHALLENGE),
    "Route103_Text_BrendanDefeated": (("CIRO:", "cicatriz"), DEFEAT),
    "Route103_Text_BrendanTimeToHeadBack": (("CIRO:", "memoria"), RETURN),
    "Route103_Text_ShouldHaveBroughtPotion": (("staggeringly tired", "POTION"), (
        "My POKéMON is exhausted...\\p",
        "I should have brought a POTION.$",
    )),
    "Route103_Text_ShortcutToOldale": (("shortcut", "VILA DA PASSAGEM"), (
        "Across the water is a shortcut\\n",
        "back to ENCRUZILHADA CENTRAL.\\p",
        "Useful if you can cross the sea.$",
    )),
    "Route103_Text_RouteSign": (("ROUTE 103", "VILA DA PASSAGEM"), (
        "ROUTE 103\\n",
        "{DOWN_ARROW} ENCRUZILHADA CENTRAL$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "").replace("{DOWN_ARROW}", "v")
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
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
    validate_widths()
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(text: str) -> str:
    masked = text
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing Route 103 block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_ROUTE103_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask_targets(source) != mask_targets(rendered):
        raise ValueError("non-dialogue Route 103 structure changed")

    forbidden = (
        "DESENCANTO", "Nao confunda", "Voce ", "voce ", "cicatriz",
        "memoria", "sofrimento", "OLDALE TOWN",
    )
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: stale Route 103 visible token survived: {token}")

    preserved = (
        "TRAINER_MAY_ROUTE_103_TREECKO",
        "TRAINER_BRENDAN_ROUTE_103_TREECKO",
        "VAR_STARTER_MON",
        "FLAG_DEFEATED_RIVAL_ROUTE103",
        "VAR_BIRCH_LAB_STATE",
        "VAR_OLDALE_RIVAL_STATE",
        "FLAG_HIDE_OLDALE_TOWN_RIVAL",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved Route 103 gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the first CIRO rival battle and Route 103 visible surface in English without changing event wiring."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TARGET.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.check:
        print(f"Route 103 Ciro English renderer OK: {len(TARGETS)} text blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

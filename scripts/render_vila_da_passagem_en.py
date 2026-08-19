#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "OldaleTown" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "OldaleTown_Text_SavingMyProgress": (("saving my", "progress"), (
        "I need a break, so I'm saving\\n",
        "my progress first.$",
    )),
    "OldaleTown_Text_IWorkAtPokemonMart": (("POKéMON MART", "come with me"), (
        "MART STAFF: I work at the\\n",
        "POKéMON MART.\\p",
        "Come with me. I'll show you.$",
    )),
    "OldaleTown_Text_ThisIsAPokemonMart": (("POKéMON MART", "promotional item"), (
        "MART STAFF: This is our shop.\\p",
        "Blue roof. Easy to spot.\\p",
        "We sell POKé BALLS and supplies.\\p",
        "Here, take this POTION.\\p",
        "It's a free sample.$",
    )),
    "OldaleTown_Text_PotionExplanation": (("POTION", "POKéMON CENTER"), (
        "MART STAFF: POTIONS work\\n",
        "outside a POKéMON CENTER.\\p",
        "Keep one for the road.$",
    )),
    "OldaleTown_Text_WaitDontComeInHere": (("footprints", "sketching"), (
        "Hold on! Don't step here.\\p",
        "I found tracks I can't identify.\\p",
        "Let me finish sketching them.$",
    )),
    "OldaleTown_Text_DiscoveredFootprints": (("footprints", "sketching"), (
        "I found tracks I can't identify.\\p",
        "Let me finish sketching them.$",
    )),
    "OldaleTown_Text_FinishedSketchingFootprints": (("own footprints",), (
        "Done. I finished the sketch.\\p",
        "They were my own footprints...\\p",
        "I need more field practice.$",
    )),
    "OldaleTown_Text_MayLetsGoBack": (("CIRO:", "memoria"), (
        "CIRO: I'm going back to ANAHI.\\p",
        "She'll want both readings.\\p",
        "Don't make one win a theory.$",
    )),
    "OldaleTown_Text_BrendanLetsGoBack": (("CIRO:", "HORIZONTE"), (
        "CIRO: I'm going back to ANAHI.\\p",
        "She'll want both readings.\\p",
        "Don't make one win a theory.$",
    )),
    "OldaleTown_Text_TownSign": (("VILA DA PASSAGEM", "DESENCANTO"), (
        "VILA DA PASSAGEM\\p",
        "A local POKéMON stopped\\n",
        "responding to its own name.\\p",
        "People here call it\\n",
        "DESECHANTMENT.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload.replace("$", ""))
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
            raise ValueError(f"cannot mask missing Vila da Passagem block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_PASSAGEM_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask_targets(source) != mask_targets(rendered):
        raise ValueError("non-dialogue Vila da Passagem structure changed")

    forbidden = (
        "OLDALE TOWN", "HORIZONTE", "DESENCANTO", "Nao confunda",
        "Voce ", "voce ", "memoria", "sofrimento",
    )
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: stale visible token survived: {token}")

    preserved = (
        "FLAG_VISITED_OLDALE_TOWN",
        "FLAG_RECEIVED_POTION_OLDALE",
        "ITEM_POTION",
        "FLAG_ADVENTURE_STARTED",
        "VAR_OLDALE_RIVAL_STATE",
        "FLAG_HIDE_OLDALE_TOWN_RIVAL",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved Vila da Passagem gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Vila da Passagem's tutorial and CIRO return surface in English without changing Oldale event wiring."
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
        print(f"Vila da Passagem English renderer OK: {len(TARGETS)} text blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

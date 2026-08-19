#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "PetalburgCity_WallysHouse" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "PetalburgCity_WallysHouse_Text_ThanksForPlayingWithWally": (("Obrigado por ter ajudado VAL",), (
        "MAN: Thank you for helping VAL.\\p",
        "He talks about how patient you\\n",
        "were with him.\\p",
        "That mattered more than you know.$",
    )),
    "PetalburgCity_WallysHouse_Text_WonderHowWallyIsDoing": (("VAL nao manda noticias",), (
        "MAN: VAL hasn't sent news for\\n",
        "a few days.\\p",
        "When he chooses a road, he tends\\n",
        "to forget everything else.\\p",
        "I hope he's doing well.$",
    )),
    "PetalburgCity_WallysHouse_Text_PleaseExcuseUs": (("Desculpe trazer voce", "VALE DO SILENCIO"), (
        "MAN: {PLAYER}, sorry to bring you\\n",
        "here so suddenly.\\p",
        "VAL has changed since leaving for\\n",
        "VALE DO SILENCIO.\\p",
        "You helped when he was afraid\\n",
        "to travel alone.\\p",
        "As his father, I remember that.\\p",
        "Please take this.$",
    )),
    "PetalburgCity_WallysHouse_Text_SurfGoAllSortsOfPlaces": (("Com SURF",), (
        "With SURF, your POKéMON can\\n",
        "cross water and reach new paths.$",
    )),
    "PetalburgCity_WallysHouse_Text_WallyIsComingHomeSoon": (("VAL disse que pretende",), (
        "MAN: VAL says he'll visit soon.\\p",
        "Now he travels because he wants\\n",
        "to, not to prove he can.$",
    )),
    "PetalburgCity_WallysHouse_Text_YouMetWallyInEverGrandeCity": (("ESTRADA DO JURAMENTO",), (
        "MAN: You met VAL on\\n",
        "ESTRADA DO JURAMENTO?\\p",
        "He came back more certain,\\n",
        "but still himself.\\p",
        "Thank you for walking beside him.$",
    )),
    "PetalburgCity_WallysHouse_Text_WallyWasReallyHappy": (("VAL ficou muito feliz",), (
        "WOMAN: VAL was so happy after\\n",
        "meeting you.\\p",
        "I hadn't heard him talk about a\\n",
        "journey like that in years.$",
    )),
    "PetalburgCity_WallysHouse_Text_WallyLeftWithoutTelling": (("VAL saiu sem avisar",), (
        "WOMAN: VAL left in a hurry.\\p",
        "I worry, of course.\\p",
        "But choosing his own road is part\\n",
        "of what he needed.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "").replace("{PLAYER}", "PLAYERX")
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
            raise ValueError(f"cannot mask missing Val-house block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_VAL_HOUSE_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask_targets(source) != mask_targets(rendered):
        raise ValueError("non-dialogue Val-house structure changed")

    forbidden = ("Obrigado", "voce", "nao ", "proprio", "saiu sem", "ficou muito feliz")
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: Portuguese Val-house token survived: {token}")

    preserved = (
        "ITEM_HM_SURF",
        "FLAG_RECEIVED_HM_SURF",
        "VAR_PETALBURG_CITY_STATE",
        "FLAG_DEFEATED_WALLY_VICTORY_ROAD",
        "FLAG_THANKED_FOR_PLAYING_WITH_WALLY",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved Val-house gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render VAL's family house in English without changing the HM SURF or inherited Wally state flow."
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
        print(f"Val house English renderer OK: {len(TARGETS)} text blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

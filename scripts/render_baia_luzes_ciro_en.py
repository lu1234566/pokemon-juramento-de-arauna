#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "maps" / "LilycoveCity" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

ASK = (
    "CIRO: I came here for answers.\\p",
    "HORIZON gave me a summary.\\n",
    "No names. No signatures.\\p",
    "Battle me.$",
)
DECLINE = (
    "CIRO: Fine.\\p",
    "I've had enough people deciding\\n",
    "what I'm ready to hear.$",
)
AGAIN = (
    "CIRO: Still here?\\p",
    "I need to know if doubt made me\\n",
    "weaker. Battle me?$",
)
PRE_BATTLE = (
    "CIRO: Don't expect me to break\\n",
    "because HORIZON hid things.\\p",
    "I'm still me.$",
)
DEFEAT = ("CIRO: Anger isn't a direction.$",)
LEAVE = (
    "CIRO: I kept saying the past\\n",
    "shouldn't govern us.\\p",
    "That's still true.\\p",
    "But no one gets to edit it and\\n",
    "call that treatment.$",
)
BADGES = (
    "CIRO: Keep moving.\\p",
    "I'm reading every side of M'BOI\\n",
    "now, not just HORIZON's.$",
)
LEAGUE = (
    "CIRO: You have your LEAGUE.\\p",
    "I have questions with names\\n",
    "attached to them now.$",
)
FRONTIER = (
    "CIRO: The crisis ended.\\p",
    "That doesn't make the records\\n",
    "complete. I'll keep looking.$",
)

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "LilycoveCity_Text_MayShoppingLetsBattle": (("CIRO:", "DESENCANTO"), ASK),
    "LilycoveCity_Text_MayNotRaisingPokemon": (("CIRO:", "HORIZONTE"), DECLINE),
    "LilycoveCity_Text_MayBattleMe": (("CIRO:", "cicatriz"), AGAIN),
    "LilycoveCity_Text_MayWontBeBeaten": (("CIRO:", "DESENCANTO"), PRE_BATTLE),
    "LilycoveCity_Text_MayDefeat": (("CIRO:", "Nao confunda"), DEFEAT),
    "LilycoveCity_Text_MayGoingBackToLittleroot": (("CIRO:", "Nao confunda"), LEAVE),
    "LilycoveCity_Text_MayYouGoingToCollectBadges": (("GYM BADGES", "POKéDEX"), BADGES),
    "LilycoveCity_Text_MayYouGoingToPokemonLeague": (("CIRO:", "Nao confunda"), LEAGUE),
    "LilycoveCity_Text_MayYouGoingToBattleFrontier": (("CIRO:", "cicatriz"), FRONTIER),
    "LilycoveCity_Text_BrendanShoppingLetsBattle": (("CIRO:", "DESENCANTO"), ASK),
    "LilycoveCity_Text_BrendanNoConfidence": (("CIRO:", "HORIZONTE"), DECLINE),
    "LilycoveCity_Text_BrendanBattleMe": (("CIRO:", "cicatriz"), AGAIN),
    "LilycoveCity_Text_BrendanWontBeBeaten": (("CIRO:", "HORIZONTE"), PRE_BATTLE),
    "LilycoveCity_Text_BrendanDefeat": (("CIRO:", "DESENCANTO"), DEFEAT),
    "LilycoveCity_Text_BrendanGoingBackToLittleroot": (("CIRO:", "DESENCANTO"), LEAVE),
    "LilycoveCity_Text_BrendanYouGoingToCollectBadges": (("GYM BADGES", "POKéMON LEAGUE"), BADGES),
    "LilycoveCity_Text_BrendanYouGoingToPokemonLeague": (("CIRO:", "cicatriz"), LEAGUE),
    "LilycoveCity_Text_BrendanYouGoingToBattleFrontier": (("CIRO:", "Nao confunda"), FRONTIER),
    "LilycoveCity_Text_CitySign": (
        ("BAIA DAS LUZES", "ARQUIVO VIVO"),
        (
            "BAIA DAS LUZES\\p",
            "Behind the modern waterfront\\n",
            "stands HORIZON's operations hub.$",
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
        masked = masked[:start] + '\t.string "<ARAUNA_CIRO_LILY>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask_targets(source) != mask_targets(rendered):
        raise ValueError("non-dialogue Lilycove structure changed")

    forbidden = ("HORIZONTE", "DESENCANTO", "Nao confunda", "sofrimento em tradicao")
    for label, (_, payloads) in TARGETS.items():
        body = block_pattern(label).search(rendered).group("body")
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: Portuguese rival residue survived: {token}")

    preserved = (
        "TRAINER_MAY_LILYCOVE_TREECKO",
        "TRAINER_BRENDAN_LILYCOVE_TREECKO",
        "FLAG_DECLINED_RIVAL_BATTLE_LILYCOVE",
        "FLAG_MET_RIVAL_LILYCOVE",
        "VAR_STARTER_MON",
        "FLDEFF_NPCFLY_OUT",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved Ciro gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Ciro's Baia das Luzes rival encounter in English without changing event wiring."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate_widths()
    source = PATH.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.check:
        print(f"Baia das Luzes Ciro renderer OK: {len(TARGETS)} text blocks validated.")
        return 0
    if args.in_place:
        PATH.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

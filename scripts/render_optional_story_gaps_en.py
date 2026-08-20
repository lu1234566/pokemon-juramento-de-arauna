#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX = 32
CTRL = re.compile(r"\\[npl]")
PH = re.compile(r"\{[^}]+\}")
TARGETS: dict[str, dict[str, tuple[str, ...]]] = {}


def add(path: str, label: str, *lines: str) -> None:
    TARGETS.setdefault(path, {})[label] = lines


BENTO = "data/maps/MossdeepCity_StevensHouse/scripts.inc"
add(BENTO, "MossdeepCity_StevensHouse_Text_YouveEarnedHMDive",
    "SEU BENTO: {PLAYER}, good timing.\\p",
    "The M'BOI records point to\\n",
    "something beneath the water.\\p",
    "Take this DIVE technique.\\n",
    "You'll need it.$")
add(BENTO, "MossdeepCity_StevensHouse_Text_ExplainDive",
    "SEU BENTO: When a name fades\\n",
    "from ordinary speech, I write.\\p",
    "Not to replace those who recall.\\n",
    "To leave a trail.$")
add(BENTO, "MossdeepCity_StevensHouse_Text_UnderwateCavernBetweenMossdeepSootopolis",
    "SEU BENTO: The sea between\\n",
    "MISSOES DO CEU and M'BOI hides\\n",
    "a deep route.\\p",
    "DIVE will let you follow it.$")
add(BENTO, "MossdeepCity_StevensHouse_Text_LetterFromSteven",
    "SEU BENTO: If you found this note,\\n",
    "I am probably traveling again.\\p",
    "A record should leave a trail,\\n",
    "not replace a living witness.$")
add(BENTO, "MossdeepCity_StevensHouse_Text_CollectionOfRareRocks",
    "Stones, labels and notebooks.\\p",
    "Each piece has a date, place\\n",
    "and a name written by SEU BENTO.$")

FAN = "data/maps/LilycoveCity_PokemonTrainerFanClub/scripts.inc"
for label in (
    "LilycoveCity_PokemonTrainerFanClub_Text_BrawlyNoImYourFan",
    "LilycoveCity_PokemonTrainerFanClub_Text_ICantHelpLikingBrawly",
    "LilycoveCity_PokemonTrainerFanClub_Text_NobodyUnderstandsBrawly",
    "LilycoveCity_PokemonTrainerFanClub_Text_MyFavoriteTrainerIsBrawly",
):
    add(FAN, label,
        "ADEMAR says the sea returns\\n",
        "things when it chooses.\\p",
        "Nobody owns the water's memory.\\p",
        "That's why I admire him.$")
for label in (
    "LilycoveCity_PokemonTrainerFanClub_Text_LongWayToGoComparedToNorman",
    "LilycoveCity_PokemonTrainerFanClub_Text_YouAndNormanAreDifferent",
):
    add(FAN, label,
        "ELIAS says being a father never\\n",
        "gave him the right to choose\\n",
        "which truths you could bear.\\p",
        "He took too long to learn that.$")

PRESERVED = {
    BENTO: (
        "VAR_STEVENS_HOUSE_STATE",
        "ITEM_HM_DIVE",
        "FLAG_RECEIVED_HM_DIVE",
        "SPECIES_BELDUM",
    ),
    FAN: (
        "VAR_LILYCOVE_FAN_CLUB_STATE",
        "FANCLUB_MEMBER1",
        "NUM_TRAINER_FAN_CLUB_MEMBERS",
        "FLAG_FAN_CLUB_STRENGTH_SHARED",
    ),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def validate_widths() -> None:
    for rel, blocks in TARGETS.items():
        for label, lines in blocks.items():
            for line in lines:
                clean = PH.sub("PLAYER", line.replace("$", ""))
                for segment in CTRL.split(clean):
                    segment = segment.strip()
                    if len(segment) > MAX:
                        raise ValueError(f"{rel}: {label}: {len(segment)} chars: {segment!r}")


def mask(text: str, labels: tuple[str, ...]) -> str:
    out = text
    for label in labels:
        match = pattern(label).search(out)
        if not match:
            raise ValueError(f"missing block: {label}")
        start, end = match.span("body")
        out = out[:start] + '\t.string "<ARAUNA_EN>"\n\n' + out[end:]
    return out


def render(rel: str, source: str) -> str:
    out = source
    labels = tuple(TARGETS[rel])
    for label, lines in TARGETS[rel].items():
        matches = list(pattern(label).finditer(out))
        if len(matches) != 1:
            raise ValueError(f"{rel}: {label}: expected 1 block, found {len(matches)}")
        body = "".join(f'\t.string "{line}"\n' for line in lines) + "\n"
        start, end = matches[0].span("body")
        out = out[:start] + body + out[end:]
    if mask(source, labels) != mask(out, labels):
        raise ValueError(f"{rel}: non-dialogue structure changed")
    for token in PRESERVED[rel]:
        if token not in out:
            raise ValueError(f"{rel}: missing preserved token {token}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("choose --check or --in-place")
    validate_widths()
    total = sum(len(v) for v in TARGETS.values())
    changed = 0
    for rel in TARGETS:
        path = ROOT / rel
        source = path.read_text(encoding="utf-8")
        output = render(rel, source)
        if output != source:
            changed += 1
            if args.in_place:
                path.write_text(output, encoding="utf-8")
    print(f"Optional story English gaps OK: {total} blocks across {len(TARGETS)} files; {changed} changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

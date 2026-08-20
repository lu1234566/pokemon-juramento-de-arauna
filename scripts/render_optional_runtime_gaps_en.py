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


FORTREE = "data/maps/FortreeCity_House3/scripts.inc"
add(FORTREE, "FortreeCity_House3_Text_MetStevenHadAmazingPokemon",
    "SEU BENTO says a name can fade\\n",
    "from ordinary speech.\\p",
    "He writes it down as a trail,\\n",
    "not as a replacement for memory.$")

HOUSE3 = "data/maps/SootopolisCity_House3/scripts.inc"
add(HOUSE3, "SootopolisCity_House3_Text_JuanHasManyFansDoYou",
    "DONA CELINA has many admirers.\\p",
    "Do people follow your battles too?$")
add(HOUSE3, "SootopolisCity_House3_Text_TrainerFanClubWasWild",
    "Dedicated fans come from outside\\n",
    "ARAUNA too.\\p",
    "It was wild when I visited the\\n",
    "TRAINER FAN CLUB in BAIA DAS LUZES.$")

HOUSE5 = "data/maps/SootopolisCity_House5/scripts.inc"
add(HOUSE5, "SootopolisCity_House5_Text_SootopolisMtPyreConnection",
    "The water carries memories that\\n",
    "do not belong to the receiver.\\p",
    "People recognize unknown names\\n",
    "and forget faces they love.$")

BENTO_CAVE = "data/maps/MeteorFalls_StevensCave/scripts.inc"
add(BENTO_CAVE, "MeteorFalls_StevensCave_Text_ShouldKnowHowGoodIAmExpectWorst",
    "SEU BENTO: We compared notes\\n",
    "for long enough.\\p",
    "Now I want to see what your road\\n",
    "changed in battle.\\p",
    "Don't hold back.$")
add(BENTO_CAVE, "MeteorFalls_StevensCave_Text_StevenDefeat",
    "SEU BENTO: Good.\\p",
    "You kept your own rhythm.$")
add(BENTO_CAVE, "MeteorFalls_StevensCave_Text_MyPredictionCameTrue",
    "SEU BENTO: A record can say\\n",
    "who won.\\p",
    "It cannot hold everything that\\n",
    "happened between us.\\p",
    "That part stays with us.$")

COZMO = "data/maps/FallarborTown_CozmosHouse/scripts.inc"
add(COZMO, "FallarborTown_CozmosHouse_Text_MeteoriteWillNeverBeMineNow",
    "PROF. COZMO: I should never have\\n",
    "told the REMEMBRANCERS where\\n",
    "METEORITES could be found.\\p",
    "The one from RUINAS DA QUEDA\\n",
    "is probably gone now.$")
add(COZMO, "FallarborTown_CozmosHouse_Text_IsThatMeteoriteMayIHaveIt",
    "PROF. COZMO: Wait...\\p",
    "Is that the METEORITE taken\\n",
    "from RUINAS DA QUEDA?\\p",
    "May I have it?\\p",
    "I'll trade this TM for it.$")
add(COZMO, "FallarborTown_CozmosHouse_Text_MayIHaveMeteorite",
    "PROF. COZMO: May I have the\\n",
    "METEORITE?\\p",
    "I can trade this TM for it.$")
add(COZMO, "FallarborTown_CozmosHouse_Text_CozmoWentToMeteorFalls",
    "PROF. COZMO went to\\n",
    "RUINAS DA QUEDA on ROUTE 114\\n",
    "with some REMEMBRANCERS.$")

PRESERVED = {
    FORTREE: ("FortreeCity_House3_EventScript_Maniac",),
    HOUSE3: ("SootopolisCity_House3_EventScript_HaveFans", "VAR_RESULT"),
    HOUSE5: ("SootopolisCity_House5_EventScript_Maniac",),
    BENTO_CAVE: ("TRAINER_STEVEN", "FLAG_DEFEATED_METEOR_FALLS_STEVEN"),
    COZMO: ("ITEM_METEORITE", "ITEM_TM_RETURN", "FLAG_RECEIVED_TM_RETURN"),
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
    print(f"Optional runtime English gaps OK: {total} blocks across {len(TARGETS)} files; {changed} changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

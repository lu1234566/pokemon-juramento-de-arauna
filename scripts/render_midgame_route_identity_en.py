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


R111 = "data/maps/Route111/scripts.inc"
add(R111, "Route111_Text_RouteSignMauville",
    "ROUTE 111\\n", "{DOWN_ARROW} ENCRUZILHADA$")

R112 = "data/maps/Route112/scripts.inc"
add(R112, "Route112_Text_LeaderGoingToAwakenThing",
    "REMEMBRANCER: Is LUZIA really\\n",
    "going to activate the amplifier?$" )
add(R112, "Route112_Text_YeahWeNeedMeteorite",
    "REMEMBRANCER: That's the plan.\\p",
    "The device needs a METEORITE\\n",
    "before it can react.$")
add(R112, "Route112_Text_OhThatsWhyCrewWentToFallarbor",
    "REMEMBRANCER: So that's why the\\n",
    "others went to CAMPO DAS CINZAS.$")
add(R112, "Route112_Text_CantLetAnyonePassUntilTheyreBack",
    "REMEMBRANCER: Until they return,\\n",
    "nobody passes this route.$")
add(R112, "Route112_Text_NotEasyToGetBackToLavaridge",
    "I'd like to reach ENCRUZILHADA.\\p",
    "But once I drop these ledges,\\n",
    "getting back toward SERTAO DE\\n",
    "DENTRO is a long climb.$")
add(R112, "Route112_Text_MtChimneyCableCarSign",
    "SERRA DA CINZA CABLE CAR\\n",
    "“A short walk {UP_ARROW} way!”$")
add(R112, "Route112_Text_MtChimneySign",
    "SERRA DA CINZA\\p",
    "For SERTAO DE DENTRO or the\\n",
    "summit, take the CABLE CAR.$")
add(R112, "Route112_Text_RouteSignLavaridge",
    "ROUTE 112\\n", "{LEFT_ARROW} SERTAO DE DENTRO$")

JAG = "data/maps/JaggedPass/scripts.inc"
add(JAG, "JaggedPass_Text_EricIntro",
    "SERRA DA CINZA's lower pass!\\p",
    "This rough stone is exactly\\n",
    "what I want from a mountain.$")
add(JAG, "JaggedPass_Text_EthanIntro",
    "PASSO DA CINZA is hard to walk.\\p",
    "That makes it good training.$")
add(JAG, "JaggedPass_Text_EthanPostRematch",
    "I should get an ACRO BIKE\\n",
    "in ENCRUZILHADA.$")
add(JAG, "JaggedPass_Text_GruntIntro",
    "REMEMBRANCER: You're not meant\\n",
    "to find this entrance.\\p",
    "Turn around.$")
add(JAG, "JaggedPass_Text_GruntDefeat",
    "REMEMBRANCER: I should have\\n",
    "gone inside sooner.$")
add(JAG, "JaggedPass_Text_GoWhereverYouWant",
    "REMEMBRANCER: Fine. You're strong.\\p",
    "I won't stop you again.$")
add(JAG, "JaggedPass_Text_BoulderShakingInResponseToEmblem",
    "The boulder is reacting to\\n",
    "the REMEM. EMBLEM!$")

R118 = "data/maps/Route118/scripts.inc"
add(R118, "Route118_Text_StevenQuestions",
    "SEU BENTO: When a name fades\\n",
    "from ordinary speech, I write.\\p",
    "Not to replace a witness.\\n",
    "To leave a trail.$")
add(R118, "Route118_Text_RouteSignMauville",
    "ROUTE 118\\n", "{LEFT_ARROW} ENCRUZILHADA$")

PRESERVED = {
    R111: ("VAR_MIRAGE_TOWER_STATE", "ITEM_GO_GOGGLES", "TRAINER_VICKY"),
    R112: ("VAR_JAGGED_PASS_ASH_WEATHER", "LOCALID_ROUTE112_GRUNT_1", "LOCALID_ROUTE112_GRUNT_2"),
    JAG: ("ITEM_MAGMA_EMBLEM", "VAR_JAGGED_PASS_STATE", "TRAINER_GRUNT_JAGGED_PASS", "FLAG_BEAT_MAGMA_GRUNT_JAGGED_PASS"),
    R118: ("VAR_ROUTE118_STATE", "LOCALID_ROUTE118_STEVEN", "ITEM_GOOD_ROD"),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def validate_widths() -> None:
    for rel, blocks in TARGETS.items():
        for label, lines in blocks.items():
            for line in lines:
                visible = PH.sub("PLAYER", line.replace("$", ""))
                for segment in CTRL.split(visible):
                    if len(segment.strip()) > MAX:
                        raise ValueError(f"{rel}: {label}: over-width segment: {segment.strip()!r}")


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
    print(f"Midgame route identity OK: {total} blocks across {len(TARGETS)} files; {changed} changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

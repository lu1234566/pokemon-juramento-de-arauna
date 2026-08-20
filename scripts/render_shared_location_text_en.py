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


QUESTION = "data/text/questionnaire.inc"
add(QUESTION, "MysteryGift_Text_TryUsingItAtLilycovePort",
    "It appears to be for use at\\n",
    "the BAIA DAS LUZES port.\\p",
    "Why not try it and see\\n",
    "where it leads?$" )

for rel, label in (
    ("data/scripts/gift_old_sea_map.inc", "sText_MysteryGiftOldSeaMapUseAtPort"),
    ("data/scripts/gift_aurora_ticket.inc", "sText_AuroraTicketUseAtPort"),
    ("data/scripts/gift_mystic_ticket.inc", "sText_MysticTicketUseAtPort"),
):
    add(rel, label,
        "It appears to be for use at\\n",
        "the BAIA DAS LUZES port.\\p",
        "Why not try it and see\\n",
        "where it leads?$" )

NEWS = "data/text/pokemon_news.inc"
add(NEWS, "gPokeNewsTextSlateport_Upcoming",
    "Greetings! It's POKéMON NEWS.\\p",
    "PORTO DO SAL's ENERGY GURU\\n",
    "has announced another sale.\\p",
    "It starts in {STR_VAR_1} day(s).\\p",
    "Save some money if you want\\n",
    "to take advantage.$")
add(NEWS, "gPokeNewsTextSlateport_Ongoing",
    "Greetings! It's POKéMON NEWS.\\p",
    "The ENERGY GURU in PORTO DO SAL\\n",
    "is holding a major sale today!\\p",
    "CALCIUM and PROTEIN are among\\n",
    "the discounted goods.$")
add(NEWS, "gPokeNewsTextSlateport_Ending",
    "Greetings! It's POKéMON NEWS.\\p",
    "PORTO DO SAL's ENERGY GURU\\n",
    "sale is almost over.\\p",
    "There is still stock left,\\n",
    "but not much time.$")
add(NEWS, "gPokeNewsTextGameCorner_Ongoing",
    "Greetings! It's POKéMON NEWS.\\p",
    "The GAME CORNER service day\\n",
    "is happening now.\\p",
    "The location is ENCRUZILHADA.$")
add(NEWS, "gPokeNewsTextGameCorner_Ending",
    "Greetings! It's POKéMON NEWS.\\p",
    "The GAME CORNER service day\\n",
    "is almost over.\\p",
    "Visit ENCRUZILHADA soon\\n",
    "if you still want to play.$")
add(NEWS, "gPokeNewsTextLilycove_Upcoming",
    "Greetings! It's POKéMON NEWS.\\p",
    "BAIA DAS LUZES DEPT. STORE\\n",
    "will hold a clear-out sale\\n",
    "in {STR_VAR_1} day(s).$")
add(NEWS, "gPokeNewsTextLilycove_Ongoing",
    "Greetings! It's POKéMON NEWS.\\p",
    "The clear-out sale at the\\n",
    "BAIA DAS LUZES DEPT. STORE\\n",
    "has begun. Don't miss it!$")
add(NEWS, "gPokeNewsTextLilycove_Ending",
    "Greetings! It's POKéMON NEWS.\\p",
    "The BAIA DAS LUZES DEPT. STORE\\n",
    "clear-out sale ends soon.$")
add(NEWS, "gPokeNewsTextBlendMaster_Upcoming",
    "Greetings! It's POKéMON NEWS.\\p",
    "The legendary BLEND MASTER\\n",
    "will visit BAIA DAS LUZES\\n",
    "in {STR_VAR_1} day(s).\\p",
    "BERRY BLENDER fans should\\n",
    "save their best BERRIES.$")
add(NEWS, "gPokeNewsTextBlendMaster_Ongoing",
    "Greetings! It's POKéMON NEWS.\\p",
    "The BLEND MASTER is now\\n",
    "in BAIA DAS LUZES.\\p",
    "Visit the CONTEST HALL to see\\n",
    "the BERRY BLENDER in action.$")
add(NEWS, "gPokeNewsTextBlendMaster_Ending",
    "Greetings! It's POKéMON NEWS.\\p",
    "The BLEND MASTER will soon\\n",
    "leave BAIA DAS LUZES.\\p",
    "Visit the CONTEST HALL now\\n",
    "if you want to see the show.$")

TIDAL = "data/maps/SSTidalRooms/scripts.inc"
add(TIDAL, "SSTidalRooms_Text_ColtonIntro",
    "I often sail to BAIA DAS LUZES.\\p",
    "I enjoy attending CONTESTS\\n",
    "there.$")
add(TIDAL, "SSTidalRooms_Text_NaomiPostBattle",
    "A world cruise has its charms.\\p",
    "Still, touring ARAUNA by ferry\\n",
    "has an appeal of its own.$")

PRESERVED = {
    QUESTION: ("Questionnaire_Text_FillOut", "MysteryGift_Text_TheresATicketForYou"),
    "data/scripts/gift_old_sea_map.inc": ("ITEM_OLD_SEA_MAP", "FLAG_ENABLE_SHIP_FARAWAY_ISLAND"),
    "data/scripts/gift_aurora_ticket.inc": ("ITEM_AURORA_TICKET", "FLAG_ENABLE_SHIP_BIRTH_ISLAND"),
    "data/scripts/gift_mystic_ticket.inc": ("ITEM_MYSTIC_TICKET", "FLAG_ENABLE_SHIP_NAVEL_ROCK"),
    NEWS: ("gPokeNewsTextSlateport_Upcoming", "gPokeNewsTextBlendMaster_Ending"),
    TIDAL: ("TRAINER_COLTON", "TRAINER_NAOMI", "ITEM_TM_SNATCH"),
}


def pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?ms)^{re.escape(label)}(?:::|:)(?:\n)(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")


def validate_widths() -> None:
    for rel, blocks in TARGETS.items():
        for label, lines in blocks.items():
            for line in lines:
                visible = PH.sub("VALUE", line.replace("$", ""))
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
        raise ValueError(f"{rel}: non-text structure changed")
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
    print(f"Shared location text OK: {total} blocks across {len(TARGETS)} files; {changed} changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

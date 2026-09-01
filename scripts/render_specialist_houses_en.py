#!/usr/bin/env python3
"""Four people who will each do one thing for a POKéMON, and nothing else.

LANETTE reads the Storage System. The NAME RATER reads a nickname. The MOVE
TUTOR reads a move list. The rater in VALE DO SILENCIO reads how a POKéMON
feels about the person carrying it.

The last of those is a seven-rung ladder, from a POKéMON that detests its
TRAINER to one that could not love them more, and it is the only reading of
affection the game offers. A player judges their own by remembering the
reading they got last time, so the seven have to be tellable apart and have
to run in order. They are generated here from one ordered table.

LANETTE's notebook holds the numbers that describe the whole PC system --
thirty to a BOX, four hundred and twenty in all, and the rule that a stored
POKéMON goes to whichever BOX was last opened. That last one changes what a
careful player does, and nothing else in the game states it.

LANETTE and BILL keep their names.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

LANETTE = ROOT / "data" / "maps" / "Route114_LanettesHouse" / "scripts.inc"
NAME_RATER = ROOT / "data" / "maps" / "SlateportCity_NameRatersHouse" / "scripts.inc"
RELEARNER = ROOT / "data" / "maps" / "FallarborTown_MoveRelearnersHouse" / "scripts.inc"
FRIENDSHIP = ROOT / "data" / "maps" / "VerdanturfTown_FriendshipRatersHouse" / "scripts.inc"
ITEMS_TABLE = ROOT / "src" / "data" / "items.h"
SPECIES_TABLE = ROOT / "src" / "data" / "text" / "species_names.h"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 12, "{KUN}": 0}, width=34)

WHOLE = ("NAME RATER", "MOVE TUTOR", "HEART SCALE", "Storage System",
         "POKéMON Storage System", "LANETTE", "BILL")

# How a POKéMON feels about the person carrying it, worst first. This is the
# only reading of affection in the game, and a player ranks their own by
# remembering the last one they were given.
AFFECTION: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("DetestsYou", (
        "This is a little hard to say...",
        "Your POKéMON simply detests you.|Does that not trouble you?")),
    ("VeryWary", (
        "It is very wary of you.|There is something vicious in its eye.|It "
        "does not like you at all.",)),
    ("NotUsedToYou", (
        "It is not used to you yet.|It neither loves you nor hates you.",)),
    ("GettingUsedToYou", (
        "It is getting used to you.|It seems to believe in you.",)),
    ("LikesYouQuiteALot", (
        "It likes you a good deal.|It looks as though it would enjoy being "
        "made a fuss of.",)),
    ("VeryHappy", (
        "It seems very happy.|It plainly likes you a great deal.",)),
    ("AdoresYou", (
        "It adores you.|It could not possibly love you more.|Seeing it makes "
        "me happy myself.",)),
)

LANETTE_BLOCKS: dict[str, tuple[str, ...]] = {
    "EverythingClutteredKeepThis": (
        "LANETTE: Oh! {PLAYER}{KUN}!",
        "I am sorry about the mess...|When the research takes hold of me "
        "this is what happens...",
        "It is embarrassing. Keep it to yourself and take this for your "
        "trouble.",
    ),
    "OrganizeYourBoxes": (
        "May I offer some advice about my POKéMON Storage System?",
        "Organise your BOXES so that you can tell at a glance what is in "
        "each of them.",
    ),
    "ResearchNotesPage1": (
        "LANETTE's research notes. There is a section on BOXES.",
        "BOXES to be designed to hold thirty POKéMON each.",
        "Every TRAINER to be able to store 420 POKéMON on the PC system.",
        "Keep reading?",
    ),
    "ResearchNotesPage2": (
        "A system of marks to be added, so that POKéMON are easier to sort.",
        "The name and the wallpaper of each BOX to be made changeable, to "
        "suit the POKéMON kept in it.",
        "Keep reading?",
    ),
    "ResearchNotesPage3": (
        "A POKéMON being stored to go to whichever BOX was opened last.",
        "If that BOX is full, it goes to the next one.",
        "Which is to say: opening a BOX makes it the one POKéMON are sent "
        "to.",
    ),
    "ClosedTheNotebook": (
        "{PLAYER} closed the notebook.",
    ),
    "EmailFromBill": (
        "There is an e-mail on the PC.",
        "“... ... ... ... ... ... ...",
        "“Your Storage System is a good deal more convenient than mine ever "
        "was.",
        "“It has a great many touches that make it pleasant to use as well "
        "as useful.",
        "“I am proud to have had a hand in how it started.",
        "“Here is hoping you carry on with the work.",
        "“From BILL|... ... ... ... ... ... ... ...”",
    ),
}

NAME_RATER_BLOCKS: dict[str, tuple[str, ...]] = {
    "PleasedToRateMonNickname": (
        "Hi, hi! I am the NAME RATER!|The fortune-teller of names!",
        "I should be delighted to rate the nickname of a POKéMON of yours.",
    ),
    "CritiqueWhichMonNickname": (
        "Whose nickname shall I pass judgement on?",
    ),
    "FineNameSuggestBetterOne": (
        "Hmmm... {STR_VAR_1}, is it?|That is a fine name you have bestowed.",
        "But! What would you say if I were to suggest a slightly better one?",
    ),
    "WhatShallNewNameBe": (
        "Ah, good.|And what shall the new nickname be?",
    ),
    "MonShallBeKnownAsName": (
        "Done. From this moment this POKéMON is known as {STR_VAR_1}.",
        "A better name than before.|How fortunate you are.",
    ),
    "NameNoDifferentYetSuperior": (
        "Done. From this moment this POKéMON is known as {STR_VAR_1}.",
        "It looks no different from before, and yet it is vastly superior.",
        "How fortunate you are.",
    ),
    "MagnificentName": (
        "Hmmm... {STR_VAR_1}, is it?",
        "A magnificent nickname.|Impeccable. Beyond reproach.",
        "You would do well to cherish your {STR_VAR_1}, now and hereafter.",
    ),
    "DoVisitAgain": (
        "I see.|Do come and see me again.",
    ),
    "ThatIsMerelyAnEgg": (
        "Now, now.|That is merely an EGG.",
    ),
}

RELEARNER_BLOCKS: dict[str, tuple[str, ...]] = {
    "ImTheMoveTutor": (
        "I am the MOVE TUTOR.",
        "I know every move a POKéMON can learn -- every one of them -- and I "
        "can put any of them back.",
        "I will do it for one of yours, if you like.",
        "My price is a HEART SCALE. I am collecting them at present.",
    ),
    "ThatsAHeartScaleWantMeToTeachMove": (
        "Oh! That is it! An honest-to-goodness HEART SCALE!",
        "And you will be wanting a move taught, I imagine?",
    ),
    "TutorWhichMon": (
        "Which POKéMON wants tutoring?",
    ),
    "TeachWhichMove": (
        "And which move shall I teach it?",
    ),
    "DontHaveMoveToTeachPokemon": (
        "Sorry...",
        "There does not appear to be a single move I can put back for that "
        "one.",
    ),
    "HandedOverHeartScale": (
        "{PLAYER} handed over one HEART SCALE in exchange.",
    ),
    "ComeBackWithHeartScale": (
        "If one of your POKéMON needs a move back, come to me with a "
        "HEART SCALE.",
    ),
    "CantTeachEgg": (
        "Hm? There is not a single move I can teach an EGG.",
    ),
}

FRIENDSHIP_BLOCKS: dict[str, tuple[str, ...]] = {
    "SeeHowMuchPokemonLikesYou": (
        "Let me see your POKéMON.|I shall tell you how much it likes you.",
        "Oh.|Your POKéMON...",
    ),
    "Pikachu": (
        "Jacarim: Pika pika!",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    friendship = {f"VerdanturfTown_FriendshipRatersHouse_Text_{label}": body
                  for label, body in FRIENDSHIP_BLOCKS.items()}
    for label, body in AFFECTION:
        friendship[f"VerdanturfTown_FriendshipRatersHouse_Text_{label}"] = body
    return {
        "lanette": {f"Route114_LanettesHouse_Text_{k}": v
                    for k, v in LANETTE_BLOCKS.items()},
        "namerater": {f"SlateportCity_NameRatersHouse_Text_{k}": v
                      for k, v in NAME_RATER_BLOCKS.items()},
        "relearner": {f"FallarborTown_MoveRelearnersHouse_Text_{k}": v
                      for k, v in RELEARNER_BLOCKS.items()},
        "friendship": friendship,
    }


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"lanette": LANETTE, "namerater": NAME_RATER,
         "relearner": RELEARNER, "friendship": FRIENDSHIP}


def which(label: str) -> str:
    for name, group in GROUPS.items():
        if label in group:
            return name
    raise KeyError(label)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, paragraphs in TARGETS.items():
        glued_paragraphs = []
        for paragraph in paragraphs:
            for name in WHOLE:
                paragraph = paragraph.replace(name, glued(name))
            glued_paragraphs.append(paragraph)
        composed[label] = BOX.compose(tuple(glued_paragraphs))
    return composed


def render(sources: dict[str, str]) -> dict[str, str]:
    composed = payloads()
    rendered = dict(sources)
    for label in TARGETS:
        group = which(label)
        matches = list(block_pattern(label).finditer(rendered[group]))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered[group] = rendered[group][:start] + new_body + rendered[group][end:]
    return rendered


def mask(texts: dict[str, str]) -> dict[str, str]:
    masked = dict(texts)
    for label in TARGETS:
        group = which(label)
        match = block_pattern(label).search(masked[group])
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked[group] = (masked[group][:start]
                         + '\t.string "<ARAUNA_SPECIALISTS_EN>"\n\n'
                         + masked[group][end:])
    return masked


def validate_slots(sources: dict[str, str]) -> None:
    composed = payloads()
    for label in TARGETS:
        body = block_pattern(label).search(sources[which(label)]).group("body")
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}", body))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(sources: dict[str, str], rendered: dict[str, str]) -> None:
    if mask(sources) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()
    items = ITEMS_TABLE.read_text(encoding="utf-8")
    species = SPECIES_TABLE.read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # Seven rungs of affection, and no other reading of it in the game.
    rungs = [flat(f"VerdanturfTown_FriendshipRatersHouse_Text_{label}")
             for label, _b in AFFECTION]
    if len(set(rungs)) != len(rungs):
        raise ValueError(
            "two of the seven affection readings are the same, so a player "
            "cannot tell a POKéMON that is warming to them from one that is "
            "not")

    # LANETTE's notebook carries the numbers that describe the PC system,
    # and the storage rule a careful player acts on.
    page1 = flat("Route114_LanettesHouse_Text_ResearchNotesPage1")
    for number in ("thirty", "420"):
        if number not in page1:
            raise ValueError(
                f"ResearchNotesPage1: dropped {number!r}, and nothing else "
                f"describes the size of the system")
    page3 = flat("Route114_LanettesHouse_Text_ResearchNotesPage3")
    if "opened last" not in page3 and "last" not in page3:
        raise ValueError(
            "ResearchNotesPage3: no longer says a stored POKéMON goes to the "
            "BOX opened last, which is the one rule here that changes what a "
            "player does")

    # The TUTOR's price appears twice and is the whole of his terms.
    if '.name = _("HEART SCALE")' not in items:
        raise ValueError(
            "the TUTOR asks for a HEART SCALE, which is not a name in "
            "src/data/items.h")
    for label in ("ImTheMoveTutor", "ComeBackWithHeartScale"):
        if "HEART SCALE" not in flat(
                f"FallarborTown_MoveRelearnersHouse_Text_{label}"):
            raise ValueError(f"{label}: no longer states the price")

    # The two renaming confirmations differ only in whether the name changed,
    # and both have to say what the POKéMON is called now.
    for label in ("MonShallBeKnownAsName", "NameNoDifferentYetSuperior"):
        if "{STR_VAR_1}" not in flat(f"SlateportCity_NameRatersHouse_Text_{label}"):
            raise ValueError(f"{label}: no longer says what the new name is")

    # The cry line names a live animal.
    if 'SPECIES_PIKACHU] = _("Jacarim")' not in species:
        raise ValueError(
            "the cry line calls the POKéMON Jacarim, which is no longer what "
            "species_names.h calls SPECIES_PIKACHU")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the four specialist houses in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    sources = {name: path.read_text(encoding="utf-8")
               for name, path in FILES.items()}
    validate_slots(sources)
    rendered = render(sources)
    validate_rendered(sources, rendered)

    if args.in_place:
        for name, path in FILES.items():
            path.write_text(rendered[name], encoding="utf-8")
    print(f"Specialist houses English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""The field moves, the berry patch, the CENTER desk, and the survey forms.

These are the surfaces a player meets over and over, in every town and on
every route, so they are where a small inconsistency does the most damage.

The field moves have the worst of it in Emerald. Each obstacle is described
twice -- once when the player has no move for it, once when they do -- and
the two descriptions do not match. The same rock is "rugged" in one and
"breakable" in the other; the same waterfall is "a wall of water crashing
down with a mighty roar" and also "a large waterfall". A player who reads
both is being told about two different things. Here each obstacle has one
description, written once, and the prompt is that description plus the
question. The renderer checks the prompt still opens on it, and that every
prompt still names the move it is offering.

The berry patch grades how well a plant was tended in three words dropped
into one sentence. Three rungs, generated and checked for order, since a
player reads them across days and ranks their care by comparing.

The CENTER nurse says the same four things at every desk in ARAUNA, which is
exactly why they are written once here.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

NURSE = ROOT / "data" / "text" / "pkmn_center_nurse.inc"
FIELD = ROOT / "data" / "scripts" / "field_move_scripts.inc"
BERRIES = ROOT / "data" / "scripts" / "berry_tree.inc"
SECRET_TM = ROOT / "data" / "scripts" / "secret_power_tm.inc"
QUESTIONNAIRE = ROOT / "data" / "text" / "questionnaire.inc"
GIFT_TRAINER = ROOT / "data" / "scripts" / "gift_trainer.inc"
ITEMS_TABLE = ROOT / "src" / "data" / "items.h"
MOVE_NAMES = ROOT / "src" / "data" / "text" / "move_names.h"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 12, "{STR_VAR_2}": 12},
              width=34)

WHOLE = ("POKéMON CENTER", "GOLD CARD", "SILVER CARD", "ROCK SMASH",
         "SECRET POWER", "SECRET BASE", "Pilhoso PAIL", "BERRIES POCKET",
         "MYSTERY GIFT", "MYSTERY EVENT", "WONDER CARD", "POKéMON MART",
         "AGUAS DE M'BOI", "BAIA DAS LUZES", "WIRELESS COMMUNICATION SYSTEM",
         "WATERFALL", "STRENGTH", "DIVE", "BAG")

# One description per obstacle, written once. The prompt is that description
# plus the offer, so the two cannot disagree about what the player is
# looking at.
#   label stem -> (move as move_names.h spells it, the description, the
#                  offer)
OBSTACLES: dict[str, tuple[str, str, str]] = {
    "Cut": (
        "CUT",
        "This tree looks as though it could be CUT down.",
        "Use CUT on it?",
    ),
    "Smash": (
        "ROCK SMASH",
        "It is a rugged rock, but a POKéMON might well break it.",
        "Use ROCK SMASH on it?",
    ),
    "Strength": (
        "STRENGTH",
        "It is a big boulder, but a POKéMON might well shift it.",
        "Use STRENGTH?",
    ),
    "Waterfall": (
        "WATERFALL",
        "A wall of water coming down with a roar.",
        "Use WATERFALL?",
    ),
    "Dive": (
        "DIVE",
        "The sea is deep here. A POKéMON could go down.",
        "Use DIVE?",
    ),
    "Surface": (
        "DIVE",
        "Light is coming down from above. A POKéMON could go up.",
        "Use DIVE?",
    ),
}

# How well a berry plant was tended, worst first. The word drops into the
# flowering sentence, and a player ranks their care by comparing days.
CARE: tuple[tuple[str, str], ...] = (
    ("CareAdverbPoor", "cutely"),
    ("CareAdverbGood", "prettily"),
    ("CareAdverbGreat", "very beautifully"),
)

FIELD_BLOCKS: dict[str, tuple[str, ...]] = {
    "Text_MonUsedFieldMove": (
        "{STR_VAR_1} used {STR_VAR_2}!",
    ),
    "Text_MonUsedStrength": (
        "{STR_VAR_1} used STRENGTH!",
        "{STR_VAR_1}'s STRENGTH makes it possible to push boulders around.",
    ),
    "Text_StrengthActivated": (
        "STRENGTH makes it possible to push boulders around.",
    ),
    "Text_MonUsedWaterfall": (
        "{STR_VAR_1} used WATERFALL.",
    ),
    "Text_MonUsedDive": (
        "{STR_VAR_1} used DIVE.",
    ),
    "Text_FailSweetScent": (
        "Nothing came. There seems to be nothing here...",
    ),
}

NURSE_BLOCKS: dict[str, tuple[str, ...]] = {
    "gText_WouldYouLikeToRestYourPkmn": (
        "Hello, and welcome to the POKéMON CENTER.",
        "We put tired POKéMON back to full health here.",
        "Would you like yours rested?",
    ),
    "gText_WelcomeCutShort": (
        "Hello, and welcome to the POKéMON CENTER.",
        "We put tired POKéMON back to full health here.",
        "Would you like...",
    ),
    "gText_IllTakeYourPkmn": (
        "Of course. I shall take them for a few seconds.",
    ),
    "gText_IllTakeYourPkmn2": (
        "Of course. I shall take them for a few seconds.",
    ),
    "gText_RestoredPkmnToFullHealth": (
        "Thank you for waiting.",
        "Your POKéMON are back to full health.",
    ),
    "gText_ThankYouForWaiting": (
        "Thank you for waiting.",
    ),
    "gText_WeHopeToSeeYouAgain": (
        "We hope to see you again.",
    ),
    "gText_WeHopeToSeeYouAgain2": (
        "We hope to see you again.",
    ),
    "gText_YouWantTheUsual": (
        "How lovely to see you, {PLAYER}.|The usual, I take it?",
    ),
    "gText_NoticesGoldCard": (
        "Th-that card...|Surely that is not the GOLD CARD?",
        "Oh, the gold of it! And the four stars fairly sparkle!",
        "I have seen a SILVER CARD once or twice, but you, {PLAYER}, are the "
        "first TRAINER I have ever seen carrying a GOLD CARD.",
        "Well then, {PLAYER}. Allow me the honour of resting your POKéMON.",
    ),
}

BERRY_BLOCKS: dict[str, tuple[str, ...]] = {
    "BerryTree_Text_ItsSoftLoamySoil": (
        "Soft, loamy soil.",
    ),
    "BerryTree_Text_WantToPlant": (
        "Soft, loamy soil.|Plant a BERRY here?",
    ),
    "BerryTree_Text_PlantedOneBerry": (
        "{PLAYER} planted one {STR_VAR_1} in the soft, loamy soil.",
    ),
    "BerryTree_Text_BerryGrowthStage1": (
        "One {STR_VAR_1} was planted here.",
    ),
    "BerryTree_Text_BerryGrowthStage2": (
        "The {STR_VAR_1} has sprouted.",
    ),
    "BerryTree_Text_BerryGrowthStage3": (
        "This {STR_VAR_1} plant is growing taller.",
    ),
    "BerryTree_Text_BerryGrowthStage4": (
        "These {STR_VAR_1} flowers are blooming {STR_VAR_2}.",
    ),
    "BerryTree_Text_WantToPick": (
        "You found {STR_VAR_2} {STR_VAR_1}!",
        "Pick the {STR_VAR_1}?",
    ),
    "BerryTree_Text_PickedTheBerry": (
        "{PLAYER} picked the {STR_VAR_2} {STR_VAR_1}.",
    ),
    "BerryTree_Text_PutAwayBerry": (
        "{PLAYER} put the {STR_VAR_1} away in the BAG's BERRIES POCKET.",
        "The soil went back to being soft and loamy.",
    ),
    "BerryTree_Text_BerryPocketFull": (
        "The BAG's BERRIES POCKET is full.",
        "The {STR_VAR_1} could not be taken.",
    ),
    "BerryTree_Text_BerryLeftUnpicked": (
        "{PLAYER} left the {STR_VAR_1} where it was.",
    ),
    "BerryTree_Text_WantToWater": (
        "Water the {STR_VAR_1} with the Pilhoso PAIL?",
    ),
    "BerryTree_Text_WateredTheBerry": (
        "{PLAYER} watered the {STR_VAR_1}.",
    ),
    "BerryTree_Text_PlantIsDelighted": (
        "The plant looks delighted with it.",
    ),
    "BerryTree_Text_ExclamationPoint": (
        "!",
    ),
}

SECRET_TM_BLOCKS: dict[str, tuple[str, ...]] = {
    "Route111_Text_MakingRoomUseTMToMakeYourOwn": (
        "What is it?|What am I doing?",
        "I am working out how to make myself a room out here, using a "
        "POKéMON move.",
        "I know. Have this TM.|Will you use it to make a room of your own?",
    ),
    "Route111_Text_ExplainSecretPower": (
        "Find a big tree that looks as though vines might come down off it.",
        "Use SECRET POWER standing in front of it. Some vines should work "
        "loose and drop, and then you can climb.",
        "Inside there is a great deal of room for whatever you want to put "
        "in it.",
        "Your own room, hidden away.|A SECRET BASE.",
        "You should make one.",
        "And it does not have to be a tree, either.",
        "Try SECRET POWER on a rock wall with a small indent in it.",
        "I am off to look for other places myself. Goodbye!",
    ),
    "Route111_Text_DontWantThis": (
        "Oh -- you do not want it?|Tell me if you change your mind.",
    ),
    "Route111_Text_DontHaveAnyRoom": (
        "Oh, you have no room for it.",
        "I shall keep hold of it. Come back for it another time.",
    ),
}

FORM_BLOCKS: dict[str, tuple[str, ...]] = {
    "Questionnaire_Text_FillOut": (
        "There is a questionnaire here.|Fill it out?",
    ),
    "Questionnaire_Text_ThankYou": (
        "Thank you for taking the time to fill out our questionnaire.",
        "What you have told us will be put to use.",
    ),
    "Questionnaire_Text_YouKnowThoseWordsGift": (
        "Oh, hello.|You know those words?",
        "Then you must know about the MYSTERY GIFT.",
        "From now on you should be receiving them.",
    ),
    "Questionnaire_Text_YouCanAccessMysteryGift": (
        "Save your game and the MYSTERY GIFT will be open to you.",
    ),
    "Questionnaire_Text_YouKnowThoseWordsEvent": (
        "Oh, hello.|You know those words?",
        "Then you must know about the MYSTERY EVENT.",
    ),
    "Questionnaire_Text_YouCanAccessMysteryEvent": (
        "Save your game and the MYSTERY EVENT will be open to you.",
    ),
    "MysteryGift_Text_TheresATicketForYou": (
        "Thank you for using the MYSTERY EVENT System.",
        "You must be {PLAYER}.|There is a ticket here for you.",
    ),
    "MysteryGift_Text_TryUsingItAtLilycovePort": (
        "It appears to be for use at the BAIA DAS LUZES port.",
        "Take it down there and find out what it does.",
    ),
    "sText_MysteryGiftVisitingTrainerInstructions": (
        "Thank you for using the MYSTERY GIFT System.",
        "Holding this WONDER CARD lets you take part in a survey at any "
        "POKéMON MART.",
        "Those surveys are how you invite TRAINERS to AGUAS DE M'BOI.",
        "...Here is a password for one of them:",
        "“GIVE ME|AWESOME TRAINER”",
        "Write that on a survey and send it to the WIRELESS COMMUNICATION "
        "SYSTEM.",
    ),
    "sText_MysteryGiftVisitingTrainerArrived": (
        "Thank you for using the MYSTERY GIFT System.",
        "A TRAINER has arrived in AGUAS DE M'BOI, looking for you.",
        "We hope the battle goes well.",
        "Other passwords will bring other TRAINERS.",
        "It is worth going looking for them.",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    field = dict(FIELD_BLOCKS)
    for stem, (_move, description, offer) in OBSTACLES.items():
        field[f"Text_Cant{stem}"] = (description,)
        field[f"Text_WantTo{stem}"] = (description, offer)
    berries = dict(BERRY_BLOCKS)
    for label, word in CARE:
        berries[f"BerryTree_Text_{label}"] = (word,)
    return {
        "nurse": dict(NURSE_BLOCKS),
        "field": field,
        "berries": berries,
        "secret_tm": dict(SECRET_TM_BLOCKS),
        "questionnaire": {k: v for k, v in FORM_BLOCKS.items()
                          if not k.startswith("sText_")},
        "gift": {k: v for k, v in FORM_BLOCKS.items()
                 if k.startswith("sText_")},
    }


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"nurse": NURSE, "field": FIELD, "berries": BERRIES,
         "secret_tm": SECRET_TM, "questionnaire": QUESTIONNAIRE,
         "gift": GIFT_TRAINER}


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
                         + '\t.string "<ARAUNA_FIELD_SERVICES_EN>"\n\n'
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
    move_names = MOVE_NAMES.read_text(encoding="utf-8")
    items = ITEMS_TABLE.read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # One obstacle, one description. The prompt is that description plus the
    # offer, so what a player is told before they have the move and after
    # they have it cannot disagree.
    for stem, (move, _description, _offer) in OBSTACLES.items():
        if f'_("{move}")' not in move_names:
            raise ValueError(
                f"{stem}: offers {move!r}, which is not a name in "
                f"move_names.h")
        plain = flat(f"Text_Cant{stem}")
        prompt = flat(f"Text_WantTo{stem}")
        if not prompt.startswith(plain):
            raise ValueError(
                f"WantTo{stem}: no longer opens on the same description "
                f"Cant{stem} gives, so the obstacle is described two ways")
        if move not in prompt:
            raise ValueError(f"WantTo{stem}: no longer names {move}")

    # Three rungs of care, read across days and ranked by comparing.
    words = [flat(f"BerryTree_Text_{label}") for label, _w in CARE]
    if len(set(words)) != len(words):
        raise ValueError(
            "two of the three care grades read alike, so a player cannot tell "
            "a well-tended plant from a neglected one")
    if "{STR_VAR_2}" not in flat("BerryTree_Text_BerryGrowthStage4"):
        raise ValueError(
            "BerryGrowthStage4: no longer takes the care word, so the grade "
            "is never shown at all")

    # The watering can goes by the name the BAG prints.
    if '.name = _("Pilhoso PAIL")' not in items:
        raise ValueError(
            "the berry patch calls the can a Pilhoso PAIL, which is no "
            "longer a name in src/data/items.h")
    if "Pilhoso PAIL" not in flat("BerryTree_Text_WantToWater"):
        raise ValueError("WantToWater: no longer names the watering can")

    # The nurse says the same thing at every desk in ARAUNA, so the two
    # copies of each line have to stay copies.
    for a, b in (("gText_IllTakeYourPkmn", "gText_IllTakeYourPkmn2"),
                 ("gText_WeHopeToSeeYouAgain", "gText_WeHopeToSeeYouAgain2")):
        if flat(a) != flat(b):
            raise ValueError(
                f"{a} and {b} have drifted apart, and they are the same line "
                f"said at the same desk")
    if not flat("gText_WelcomeCutShort").startswith(
            flat("gText_WouldYouLikeToRestYourPkmn").rsplit("Would", 1)[0].strip()):
        raise ValueError(
            "WelcomeCutShort: no longer opens the way the full greeting "
            "does, and it is the same greeting interrupted")

    # SECRET POWER is explained once, and both places it works are named.
    explanation = flat("Route111_Text_ExplainSecretPower")
    for fact in ("SECRET POWER", "tree", "SECRET BASE", "indent"):
        if fact not in explanation:
            raise ValueError(
                f"ExplainSecretPower: dropped {fact!r}, and this is the only "
                f"explanation of the move in the game")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the field moves, berry patch and service desks.")
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
    print(f"Field and services English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

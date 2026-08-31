#!/usr/bin/env python3
"""The BATTLE PYRAMID lobby, and the fortune teller who works the door.

The pyramid is the facility that takes things away from you. You go in with
three POKéMON holding nothing, you are handed a BATTLE BAG, and whatever you
put in it is lost if you fail. That is the bargain, and it is the part of the
explanation a player must understand before entering, so it is stated once,
plainly, and repeated in the rules where the bag is described.

The fortune teller by the door reads twenty-one omens, one per hazard the
floors above can hold. They are all the same sentence: here is what I see,
and here is what it does to you. Written out by hand that is twenty-one
chances to warn about paralysis and describe poison, so they are a table of
(what she sees, what it does) and the sentence is written once.

Her omens have to stay useful. A player who reads one should know what to
pack, so each keeps the type or status it is about, and the renderer refuses
two omens that read alike.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

LOBBY = ROOT / "data" / "maps" / "BattleFrontier_BattlePyramidLobby" / "scripts.inc"
PREFIX = "BattleFrontier_BattlePyramidLobby_Text_"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 14}, width=34)

WHOLE = ("BATTLE PYRAMID", "BATTLE BAG", "BATTLE BAGS", "Battle Quest",
         "Open Level", "Battle Point", "Battle Points", "RAIN DANCE",
         "SUNNY DAY", "SANDSTORM", "Power Points")

# suffix -> (what she sees, what it does to you)
OMENS: dict[str, tuple[str, str]] = {
    "Paralysis": ("a shower of sparks",
                  "your POKéMON unable to move for them"),
    "Poison": ("poison", "your POKéMON worn down by it, turn after turn"),
    "Burn": ("red flames", "your POKéMON burned, and weakening as it strikes"),
    "PPWaste": ("a pressure of anger that was never answered",
                "your POKéMON emptied of Power Points, with nothing left but "
                "STRUGGLE"),
    "Levitate": ("POKéMON that do not touch the ground",
                 "your GROUND-type moves passing beneath them"),
    "TrapAbility": ("something rising out of the floor to hold you",
                    "your POKéMON unable to flee"),
    "Ice": ("ICE-type POKéMON", "your POKéMON slowed and frozen by them"),
    "Explosion": ("moves that destroy the one who uses them",
                  "your POKéMON going down with them"),
    "Psychic": ("PSYCHIC-type POKéMON",
                "your POKéMON in torment from what they do"),
    "Rock": ("ROCK-type POKéMON", "your POKéMON battered by them"),
    "Fighting": ("FIGHTING-type POKéMON", "your POKéMON beaten down by them"),
    "Weather": ("POKéMON that grow stronger as the sky changes",
                "your POKéMON caught out by moves it did not expect"),
    "Bug": ("BUG-type POKéMON",
            "your POKéMON worn away by attacks of every kind"),
    "Dark": ("DARK-type POKéMON", "your POKéMON suffering under them"),
    "Water": ("WATER-type POKéMON", "your POKéMON swept away by them"),
    "Ghost": ("GHOST-type POKéMON", "your POKéMON reached where it cannot "
                                    "answer"),
    "Steel": ("STEEL-type POKéMON",
              "your POKéMON unable to make an impression on them"),
    "FlyingDragon": ("POKéMON that fly",
                     "your POKéMON struck by something enormous"),
    "StoneEvolve": ("those that were changed by the power of stones",
                    "your POKéMON caught between fire, water and lightning"),
    "Normal": ("NORMAL-type POKéMON",
               "your POKéMON overwhelmed by nothing but force"),
}

# Weather is the one omen that has to name the four it means, because the
# answer to it depends on which.
WEATHER_MOVES = "RAIN DANCE... SUNNY DAY... SANDSTORM... HAIL..."


def omen(sees: str, does: str, preface: str | None = None) -> tuple[str, ...]:
    lines = [f"I see {sees}..."]
    if preface:
        lines.insert(0, preface)
    lines.append(f"...And I see {does}...")
    return tuple(lines)


TARGETS: dict[str, tuple[str, ...]] = {
    "WelcomeToBattlePyramid": (
        "Where a TRAINER's nerve is put to the question!",
        "Welcome to the BATTLE PYRAMID!",
        "I am your guide to the Battle Quest.",
    ),
    "EmbarkOnChallenge": (
        "Have you the nerve to take the Battle Quest?",
    ),
    "AwaitFutureChallenge": (
        "We shall await your challenge another day!",
    ),
    "ExplainBattlePyramid": (
        "The Battle Quest is a climb. You go into the PYRAMID and try to "
        "reach the top.",
        "Seven floors of maze, and on them skilled TRAINERS and wild POKéMON "
        "both.",
        "You enter with three POKéMON, and none of them may be holding "
        "anything.",
        "We give you a BATTLE BAG instead, to carry what you find.",
        "And understand this before you go up: if you fail, everything in "
        "that BATTLE BAG is gone.",
        "If you must stop part way, choose “REST” and save the game. If you "
        "do not save, the challenge is forfeit.",
    ),
    "WhichLevelMode": (
        "The PYRAMID runs two courses: Level 50 and Open Level.",
        "Which will you enter?",
    ),
    "SelectThreeMons": (
        "Very good. Now select the three POKéMON to go with you.",
    ),
    "NotEnoughValidMonsLvOpen": (
        "A small difficulty, adventurer.",
        "You do not have three POKéMON that qualify.",
        "And remember to take every item off them before you come to me.",
        "EGGS{STR_VAR_1} ineligible.",
        "Have a word with me when you're ready.",
    ),
    "NotEnoughValidMonsLv50": (
        "A small difficulty, adventurer.",
        "You do not have three POKéMON that qualify.",
        "They must be three different kinds, none above Level 50.",
        "And remember to take every item off them before you come to me.",
        "EGGS{STR_VAR_1} ineligible.",
        "Have a word with me when you're ready.",
    ),
    "OkayToSaveBeforeChallenge": (
        "Before you go into the BATTLE PYRAMID the game must be saved. Is "
        "that all right?",
    ),
    "ShowYouIntoPyramid": (
        "Very good. I'll show you into the BATTLE PYRAMID.",
    ),
    "WeWillHoldBagForSafekeeping": (
        "We'll keep your BAG safe, {PLAYER}, while you're up there.",
    ),
    "PleaseTakePreviousBattleBag": (
        "And here is your BATTLE BAG -- the one you had last time.",
    ),
    "PleaseTakeThisBattleBag": (
        "And here is your BATTLE BAG.",
    ),
    "ExchangedBagForBattleBag": (
        "{PLAYER} exchanged the BAG for the BATTLE BAG.",
    ),
    "StepOnFloorPanel": (
        "Step on this panel and it will carry you up into the PYRAMID.",
        "I hope, for your sake, that it goes well up there.",
    ),
    "DidntSaveBeforeQuittingTakeBag": (
        "A large difficulty, explorer.",
        "You did not save before ending your challenge last time.",
        "It is forfeit. I am sorry to have to say so.",
        "Here is the BAG we were holding for you.",
        "{PLAYER} got the BAG back.",
    ),
    "YouveConqueredPyramid": (
        "You're back!|And you took the PYRAMID! Splendid!",
    ),
    "MonHoldingItemCannotTake": (
        "Ah. A small difficulty.",
        "One of your POKéMON is holding something.",
        "What is found in the PYRAMID stays in the PYRAMID, I'm afraid.",
    ),
    "HeldItemsMovedToBag": (
        "Everything your POKéMON are holding goes into the BATTLE BAG, "
        "{PLAYER}.",
    ),
    "BagCannotHoldPickItemsToKeep": (
        "The BATTLE BAG will not hold all of it, I'm afraid.",
        "Choose what stays in the BATTLE BAG and what stays with your "
        "POKéMON.",
    ),
    "LeastOneMonHoldingItem": (
        "One of your POKéMON is still holding something.",
    ),
    "PickItemsToKeep": (
        "Choose what stays in the BATTLE BAG and what stays with your "
        "POKéMON.",
    ),
    "ReturnedEverythingMonsHeld": (
        "{PLAYER} returned everything the POKéMON were holding.",
    ),
    "UsedBattleBagWillBeKept": (
        "The BATTLE BAG you used will be kept ready for your next climb.",
        "{PLAYER} handed the BATTLE BAG back and took the BAG.",
    ),
    "RecordResultsWait": (
        "I must record your result. One moment.",
    ),
    "ForConqueringPyramidTakeThis": (
        "For taking the BATTLE PYRAMID, please have this.",
    ),
    "ReceivedPrizeItem": (
        "{PLAYER} received the prize {STR_VAR_1}.",
    ),
    "BagIsFull": (
        "...Ah.|Your BAG appears to be full.",
        "Come back when you have put it in order.",
    ),
    "DisappointingHereIsBag": (
        "A disappointment for you...",
        "Here is the BAG we were holding.",
        "{PLAYER} got the BAG back.",
    ),
    "LookForwardToNextChallenge": (
        "We look forward to your next climb!",
    ),
    "HereIsPrize": (
        "We have been waiting for you!",
        "Here is your prize for taking the PYRAMID.",
    ),
    "YouveDefeatedPyramidKing": (
        "You're back!|And you have done the thing nobody does!",
        "You beat the MASTER and took the BATTLE PYRAMID!",
    ),
    "GiveYouTheseBattlePoints": (
        "Young explorer! For nerve of that order, we give you these Battle "
        "Point(s)!",
    ),

    # -- the fortune teller ---------------------------------------------------
    "TellYouWhatMisfortunesAwait": (
        "Welcome...",
        "I shall be glad to tell you what waits for you up there...",
    ),
    "Aah": (
        "... ... ... ... ...|... ... ... ... ...",
        "... ... ... ... ...|Aah!",
    ),
    "BelieveMyFortunesOrNot": (
        "Believe me or don't. That is yours to decide...",
        "What is coming can be changed at any hour...|Go safely...",
    ),

    # -- the people standing about --------------------------------------------
    "TrainersNoticeRunning": (
        "Did you know?",
        "Run, and a TRAINER will hear you and come after you.",
        "So if you would rather not battle, keep out of their eye and go "
        "quietly past.",
    ),
    "LostLotOfItems": (
        "Awaaaaaaarrrrgh!",
        "I had an armful of things up there, and lost every one of them when "
        "I lost!",
        "Awaaaaaaarrrrgh!",
    ),

    # -- the rules ------------------------------------------------------------
    "RulesAreListed": (
        "The Battle Quest rules are set out here.",
    ),
    "ReadWhichHeading": (
        "Which heading will you read?",
    ),
    "ExplainMonRules": (
        "Take the PYRAMID once and the wild POKéMON inside it change to "
        "other kinds.",
        "Climb, watch, and learn what you are likely to meet.",
    ),
    "ExplainTrainerRules": (
        "TRAINERS are waiting for you inside.",
        "Up to eight on every floor.",
        "Beat one and you are given a hint worth having.",
    ),
    "ExplainMazeRules": (
        "The mazes are laid out afresh every time you enter.",
        "And they are dark. Go carefully.",
        "Every wild POKéMON and every TRAINER you beat brings the light up a "
        "little.",
    ),
    "ExplainBagRules": (
        "The BATTLE BAG is your BAG while you are inside.",
        "There are two of them, one for the Level 50 climb and one for Open "
        "Level.",
        "Each holds up to ninety-nine of each of ten kinds of item.",
        "And if you fail the climb, everything in it is lost.",
    ),
}

for suffix, (sees, does) in OMENS.items():
    TARGETS[f"Hint{suffix}"] = omen(
        sees, does, WEATHER_MOVES if suffix == "Weather" else None)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(PREFIX + label)}::?\n(?P<body>.*?)"
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


def render(source: str) -> str:
    composed = payloads()
    rendered = source
    for label in TARGETS:
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask(text: str) -> str:
    masked = text
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_BATTLE_PYRAMID_LOBBY_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    composed = payloads()
    for label in TARGETS:
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}",
                                   block_pattern(label).search(source).group("body")))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()

    def flat(label: str) -> str:
        return re.sub(r"\\[npl]", " ", "".join(composed[label]))

    # An omen a player cannot act on is decoration. Each has to keep the type
    # or the status it is warning about.
    for suffix, (sees, _) in OMENS.items():
        text = flat(f"Hint{suffix}")
        marker = sees.split()[1] if sees.startswith("a ") else sees.split()[0]
        if marker not in text:
            raise ValueError(f"Hint{suffix}: the omen no longer names {marker}")

    # And no two may read alike, or the fortune teller is telling one fortune
    # twenty-one times.
    omens = [flat(f"Hint{suffix}") for suffix in OMENS]
    if len(set(omens)) != len(omens):
        raise ValueError("two of the omens read identically")

    # The weather omen covers four different skies, and which one it is
    # decides what answers it.
    weather = flat("HintWeather")
    for move in ("RAIN DANCE", "SUNNY DAY", "SANDSTORM", "HAIL"):
        if move not in weather:
            raise ValueError(f"HintWeather: no longer names {move}")

    # The bargain of the facility: nothing held on the way in, and everything
    # in the BATTLE BAG lost on a failure. Both, in both places.
    entry = flat("ExplainBattlePyramid")
    if "none of them may be holding" not in entry:
        raise ValueError("ExplainBattlePyramid: no longer says you enter empty-handed")
    for label in ("ExplainBattlePyramid", "ExplainBagRules"):
        if "lost" not in flat(label) and "gone" not in flat(label):
            raise ValueError(
                f"{label}: no longer warns the BATTLE BAG is lost on a failure")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BATTLE PYRAMID lobby in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = LOBBY.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        LOBBY.write_text(rendered, encoding="utf-8")
    print(f"Battle Pyramid lobby English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

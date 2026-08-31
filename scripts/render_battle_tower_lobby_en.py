#!/usr/bin/env python3
"""The BATTLE TOWER lobby, and its four guides.

The tower runs four kinds of challenge -- single, double, multi, and multi
with a friend on a cable -- and staffs a separate desk for each. The four
guides say the same six things in the same order, differing only in the
format and the number of POKéMON it wants, which is why they are generated
here from one function: four hand-maintained copies of one explanation is how
one of them ends up telling a player to bring three when the room wants four.

The eight refusals are the same shape again: a level cap or none, crossed
with a count. Eight copies of one sentence, and the count is the part a
player has to act on.

Two facts about this facility are true nowhere else in the building, and
Emerald puts both in passing: once you enter a room you cannot leave until
you lose or win seven, and the linked challenge cannot be interrupted at all,
not even by saving. Both are stated plainly here, and the renderer keeps them.

ReceivedPrize and RecordLastMatch are not here. They belong to renderers
further down the manifest that write those lines for every facility at once.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

LOBBY = ROOT / "data" / "maps" / "BattleFrontier_BattleTowerLobby" / "scripts.inc"
PREFIX = "BattleFrontier_BattleTowerLobby_Text_"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 14, "{STR_VAR_2}": 6}, width=34)

WHOLE = ("BATTLE TOWER", "BATTLE ROOM", "BATTLE ROOMS", "BATTLE SALON",
         "SINGLE BATTLE", "SINGLE BATTLES", "DOUBLE BATTLE",
         "DOUBLE BATTLES", "MULTI BATTLE", "MULTI BATTLES", "LINK MULTI",
         "Open Level", "Battle Point", "Battle Points", "Wireless Adapters",
         "Game Link")

# The counts each room wants, and the word its refusal uses.
ROOMS = {
    "Singles": "three",
    "Doubles": "four",
    "Multis": "two",
}


def welcome(rooms: str) -> tuple[str, ...]:
    return (
        "Where a TRAINER's ability is put to the question!",
        "Welcome to the BATTLE TOWER!",
        f"I am your guide to the {rooms}.",
    )


def refusal(count: str, capped: bool) -> tuple[str, ...]:
    """One refusal, crossed eight ways by count and level cap."""
    requirement = (
        f"You need {count} different POKéMON, all of them Level 50 or lower."
        if capped else
        f"You need {count} different POKéMON.")
    return (
        "Excuse me!",
        f"You don't have {count} eligible POKéMON.",
        requirement,
        "No two of them may hold the same kind of item.",
        "EGGS{STR_VAR_1} ineligible.",
        "Come and see me when you're ready.",
    )


TARGETS: dict[str, tuple[str, ...]] = {
    # -- the four desks -------------------------------------------------------
    "WelcomSingleBattle": welcome("SINGLE BATTLE ROOMS"),
    "TakeSinglesChallenge": (
        "Would you like to take the SINGLE BATTLE ROOM challenge?",
    ),
    "ExplainSinglesChallenge": (
        "The SINGLE BATTLE ROOMS are for SINGLE BATTLES fought with three "
        "POKéMON.",
        "There are a great many of them in the tower.",
        "In each, seven TRAINERS are waiting.",
        "Beat all seven and you earn Battle Points.",
        "If you must stop part way, save the game. If you do not save, the "
        "challenge is forfeit.",
    ),
    "SelectThreeMons": (
        "Now select the three POKéMON to be entered.",
    ),
    "WelcomeDoubleBattle": welcome("DOUBLE BATTLE ROOMS"),
    "TakeDoublesChallenge": (
        "Would you like to take the DOUBLE BATTLE ROOM challenge?",
    ),
    "ExplainDoublesChallenge": (
        "The DOUBLE BATTLE ROOMS are for DOUBLE BATTLES fought with four "
        "POKéMON.",
        "There are a great many of them in the tower.",
        "In each, seven TRAINERS are waiting.",
        "Beat all seven and you earn Battle Points.",
        "If you must stop part way, save the game. If you do not save, the "
        "challenge is forfeit.",
    ),
    "PleaseSelectFourMons": (
        "Now select the four POKéMON to be entered.",
    ),
    "WelcomeMultiBattle": welcome("MULTI BATTLE ROOMS"),
    "TakeMultisChallenge": (
        "Would you like to take the MULTI BATTLE ROOM challenge?",
    ),
    "ExplainMultisChallenge": (
        "The MULTI BATTLE ROOMS are for MULTI BATTLES, which you fight "
        "beside somebody.",
        "You and your partner enter two POKéMON each.",
        "Upstairs there is a room called the BATTLE SALON, where TRAINERS "
        "wait to be asked.",
        "Find one there who suits you, and we shall show the pair of you in.",
        "Seven tag teams are waiting in the room.",
        "Beat all seven and you earn Battle Points.",
        "If you must stop part way, save the game. If you do not save, the "
        "challenge is forfeit.",
    ),
    "PleaseSelectTwoMons": (
        "Now select the two POKéMON to be entered.",
    ),
    "WelcomeLinkMultiBattle": welcome("LINK MULTI BATTLE ROOMS"),
    "TakeLinkMultisChallenge": (
        "Would you like to take the LINK MULTI BATTLE ROOM challenge?",
    ),
    "ExplainLinkMultisChallenge": (
        "The LINK MULTI BATTLE ROOMS are for MULTI BATTLES fought beside a "
        "friend of your own.",
        "You will need to be linked, by Wireless Adapters or by a Game Link "
        "cable.",
        "You enter two POKéMON each, and they must be different kinds from "
        "your friend's.",
        "Seven tag teams are waiting in the room.",
        "Beat all seven and you earn Battle Points.",
        "And be warned: this challenge alone cannot be interrupted.",
        "Once you begin, the seven battles are fought one after another, "
        "without a break.",
    ),
    "PleaseSelectTwoMons2": (
        "Now select the two POKéMON to be entered.",
    ),

    # -- the eight refusals ---------------------------------------------------
    "NotEnoughValidMonsLv50": refusal("{STR_VAR_2}", True),
    "NotEnoughValidMonsLvOpen": refusal("{STR_VAR_2}", False),
    "NotEnoughValidMonsLv50Singles": refusal(ROOMS["Singles"], True),
    "NotEnoughValidMonsLvOpenSingles": refusal(ROOMS["Singles"], False),
    "NotEnoughValidMonsLv50Doubles": refusal(ROOMS["Doubles"], True),
    "NotEnoughValidMonsLvOpenDoubles": refusal(ROOMS["Doubles"], False),
    "NotEnoughValidMonsLv50Multis": refusal(ROOMS["Multis"], True),
    "NotEnoughValidMonsLvOpenMultis": refusal(ROOMS["Multis"], False),

    # -- the desk ------------------------------------------------------------
    "WhichLevelMode": (
        "The BATTLE ROOM runs at two levels: Level 50 and Open Level.",
        "Which will you take?",
    ),
    "PleaseSelectMons": (
        "Select the POKéMON you wish to enter.",
    ),
    "OkayToSaveBeforeEntering": (
        "Before you go in, your progress must be saved. Is that all right?",
    ),
    "ProgressWillBeSaved": (
        "Before you go in, your progress will be saved. One moment.",
    ),
    "SaveGameBeforeShowingIn": (
        "I'll save the game before showing you in. One moment.",
    ),
    "ShowYouToBattleRoom": (
        "I'll show you to the {STR_VAR_1} BATTLE ROOM.",
    ),
    "DirectYouToBattleRoom": (
        "I'll take you to your BATTLE ROOM.",
    ),
    "DidntSaveBeforeQuitting": (
        "Excuse me!",
        "You didn't save before you stopped last time.",
        "I'm afraid that forfeits the challenge you were on. Sorry!",
    ),
    "WeveBeenWaitingForYou": (
        "We've been waiting for you!",
    ),
    "LookForwardToAnotherChallenge": (
        "We look forward to seeing you on another challenge!",
    ),
    "CongratsBeatenSeven": (
        "Congratulations!|All seven TRAINERS.",
    ),
    "EarnedFabulousPrize": (
        "For seven in a row, you have earned this.",
    ),
    "BagFullMakeRoom": (
        "Oh -- your BAG appears to be full.",
        "Make a little room and come back to me.",
    ),
    "ThankYouForPlaying": (
        "Thank you for playing!",
    ),
    "RecordWillBeSaved": (
        "Your record will be saved. One moment.",
    ),
    "AboutToFace50thTrainer": (
        "You are about to face the fiftieth TRAINER.",
        "From here on, every seven you beat in a row earns your POKéMON a "
        "RIBBON to mark it.",
        "Good luck.",
    ),
    "HereAreSomeRibbons": (
        "RIBBONS, for seven hard TRAINERS in a row.",
        "{PLAYER} received some RIBBONS!",
    ),
    "PutRibbonOnMons": (
        "{PLAYER} put the RIBBONS on the POKéMON that earned them.",
    ),
    "CongratsDefeatedMaiden": (
        "Congratulations!|You have beaten the MASTER, and swept seven "
        "TRAINERS besides!",
    ),
    "AwardYouTheseBattlePoints": (
        "In recognition of an ability that appears to have no ceiling, we "
        "award you these Battle Point(s).",
    ),

    # -- the linked challenge's own refusals ----------------------------------
    "ChoseSameMonAsFriend": (
        "You have chosen the same kind of POKéMON as your friend.",
        "Pick two that differ from theirs, agree on the level, and register "
        "again.",
    ),
    "ChooseDifferentMonsMatchLvlMode": (
        "Pick two that differ from your friend's, agree on the level, and "
        "register again.",
    ),
    "LinkMultiOnlyForTwoPlayers": (
        "The LINK MULTI BATTLE ROOM challenge is for two linked players and "
        "no other number.",
    ),
    "FriendAlsoSelectedMon": (
        "Your friend has also chosen {STR_VAR_1}.",
    ),
    "FriendAlsoSelectedMons": (
        "Your friend has also chosen {STR_VAR_1} and {STR_VAR_2}.",
    ),
    "FriendChoseDifferentLvlMode": (
        "Your friend has chosen a different level.",
    ),
    "FriendChoseDifferentLvlModeSameMon": (
        "Your friend has chosen a different level.",
        "And has also chosen {STR_VAR_1}.",
    ),
    "FriendChoseDifferentLvlModeSameMons": (
        "Your friend has chosen a different level.",
        "And has also chosen {STR_VAR_1} and {STR_VAR_2}.",
    ),

    # -- the rooms that were never finished -----------------------------------
    "DoubleBattleRoomConstruction": (
        "Welcome to the BATTLE TOWER DOUBLE BATTLE CORNER!",
        "The BATTLE ROOMS here are still being built, I'm afraid.",
        "Do come back when the work is done.",
    ),
    "MultiBattleRoomConstruction": (
        "Welcome to the BATTLE TOWER MULTI BATTLE CORNER!",
        "The BATTLE ROOMS here are still being built, I'm afraid.",
        "Do come back when the work is done.",
    ),

    # -- the people standing about --------------------------------------------
    "DescribeFeelingsAboutBattleTower": (
        "Excuse me -- have you a moment?",
        "Could you tell me how it feels going into a BATTLE TOWER match? Or "
        "coming out of one, won or lost?",
    ),
    "FeelWhatWhenYouBegin": (
        "Right. What do you feel just before a match?",
    ),
    "FeelWhatWhenYouveWon": (
        "And what do you feel when you've won one?",
    ),
    "FeelWhatWhenYouveLost": (
        "And when you've lost?",
    ),
    "DontThinkMuchAboutIt": (
        "Oh -- you don't think about it much? You're a cool one.",
    ),
    "ChangedYourMind": (
        "Hm? You've changed your mind?|Fickle, aren't you.",
    ),
    "ThatsHowYouFeel": (
        "So that's how it is for you?|Nobody has said that before.",
        "Thank you!",
    ),
    "WinsInRowRecorded": (
        "They keep a record of how many you win in a row.",
        "I'd better not lose in a way anyone remembers.",
    ),
    "CanLeaveUntilLossOrSevenWins": (
        "Once you're in the BATTLE TOWER you can't come out until you lose "
        "or you've beaten seven.",
        "So be sure you want it before you go up.",
    ),

    # -- the rules ------------------------------------------------------------
    "RulesAreListed": (
        "The BATTLE TOWER rules are set out here.",
    ),
    "ReadWhichHeading": (
        "Which heading will you read?",
    ),
    "ExplainTowerRules": (
        "The tower runs four kinds of battle: SINGLE, DOUBLE, MULTI, and "
        "LINK MULTI.",
        "Each has its own BATTLE ROOMS and its own desk.",
        "Speak to the guide for the kind you want.",
    ),
    "ExplainMonRules": (
        "How many POKéMON you bring depends on the room.",
        "SINGLE wants three. DOUBLE wants four. Both MULTI modes want two.",
    ),
    "ExplainSalonRules": (
        "The BATTLE SALON is where you find somebody to fight the MULTI "
        "BATTLE ROOMS beside you.",
        "Look at what the TRAINERS there are carrying and what their moves "
        "do before you ask.",
        "After seven straight wins you may change partner.",
    ),
    "ExplainMultiLinkRules": (
        "LINK MULTI is for two friends taking the tower together.",
        "You must be linked, by Wireless Adapters or by a Game Link cable.",
        "Each of you registers two POKéMON at the counter, and they must "
        "differ from your friend's.",
        "And unlike every other mode, this one cannot be interrupted once "
        "begun.",
    ),
}


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
        masked = masked[:start] + '\t.string "<ARAUNA_BATTLE_TOWER_LOBBY_EN>"\n\n' + masked[end:]
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

    # The count is the part of a refusal a player has to act on, so each of
    # the six fixed ones has to state its own.
    for room, count in ROOMS.items():
        for level in ("Lv50", "LvOpen"):
            text = flat(f"NotEnoughValidMons{level}{room}")
            if count not in text:
                raise ValueError(
                    f"NotEnoughValidMons{level}{room}: no longer says {count}")
            if (level == "Lv50") != ("Level 50" in text):
                raise ValueError(
                    f"NotEnoughValidMons{level}{room}: states the wrong level "
                    f"condition")

    # And the counts must agree with what the rules page and the desks say.
    rules = flat("ExplainMonRules")
    for count in ROOMS.values():
        if count not in rules:
            raise ValueError(f"ExplainMonRules: no longer says {count}")

    # Two facts hold in this facility and nowhere else in the building.
    if "can't come out" not in flat("CanLeaveUntilLossOrSevenWins"):
        raise ValueError(
            "CanLeaveUntilLossOrSevenWins: no longer says you are committed "
            "once you enter")
    for label in ("ExplainLinkMultisChallenge", "ExplainMultiLinkRules"):
        if "cannot be interrupted" not in flat(label):
            raise ValueError(
                f"{label}: no longer warns the linked challenge cannot be "
                f"interrupted")

    # The four guides are one explanation with the format swapped in, so no
    # two of them may come out identical either.
    explanations = [flat(f"Explain{kind}Challenge")
                    for kind in ("Singles", "Doubles", "Multis", "LinkMultis")]
    if len(set(explanations)) != len(explanations):
        raise ValueError("two of the four guides give the same explanation")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BATTLE TOWER lobby in English.")
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
    print(f"Battle Tower lobby English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

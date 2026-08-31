#!/usr/bin/env python3
"""The BATTLE PALACE lobby, where the trainer is not allowed to give orders.

This is the strangest facility in the building and the one whose rules matter
most, because a player who misreads them brings the wrong team and loses
seven times before working out why. You may switch a POKéMON in or out. You
may do nothing else. What your POKéMON does with its turn is decided by its
nature and by which of its moves that nature is willing to use.

Emerald states all of that and buries the operative half: that a POKéMON is
bad at moves its nature dislikes, so a team assembled the usual way -- best
moves, best stats -- can be helpless here. The five headings are reordered so
the consequence comes first and the taxonomy after, and the renderer holds
the rules to naming nature, the switching-only restriction, and the fact that
a mismatched move is a weak one.

Its guide is the most formal person in the frontier and the only one who
never says "okay". That is deliberate: the palace treats a battle as
something to be witnessed rather than run.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

LOBBY = ROOT / "data" / "maps" / "BattleFrontier_BattlePalaceLobby" / "scripts.inc"
PREFIX = "BattleFrontier_BattlePalaceLobby_Text_"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 14}, width=34)

WHOLE = ("BATTLE PALACE", "BATTLE HALL", "BATTLE HALLS", "CIRCUIT PASS",
         "SINGLE BATTLE", "SINGLE BATTLES", "DOUBLE BATTLE",
         "DOUBLE BATTLES", "Open Level", "Battle Point", "Battle Points")


def challenge(kind: str, halls: str) -> tuple[str, ...]:
    """The two hall explanations differ only where the format does."""
    return (
        f"The BATTLE PALACE holds several auditoriums for {kind}S. They are "
        f"called the {halls}.",
        "The battles are as anywhere else, but for one rule that governs "
        "everything.",
        "A TRAINER here may switch a POKéMON in or out. A TRAINER may do "
        "nothing else.",
        "Your POKéMON choose their own moves, according to their nature.",
        "You are to trust them and to watch.",
        "Beat seven TRAINERS one after another and we shall present you with "
        "Battle Points.",
        "If you must stop part way, you must save the game. If you do not "
        "save, the challenge is forfeit.",
    )


TARGETS: dict[str, tuple[str, ...]] = {
    "WelcomeForSingleBattle": (
        "Where the heart of a TRAINER is put to the question.",
        "I welcome you to the BATTLE PALACE.",
        "I take challenges to the SINGLE BATTLE HALLS.",
    ),
    "TakeSingleBattleChallenge": (
        "Do you wish to take the SINGLE BATTLE HALL challenge?",
    ),
    "ExplainSingleBattleChallenge": challenge("SINGLE BATTLE",
                                              "SINGLE BATTLE HALLS"),
    "WelcomeForDoubleBattle": (
        "Where the heart of a TRAINER is put to the question.",
        "I welcome you to the BATTLE PALACE.",
        "I take challenges to the DOUBLE BATTLE HALLS.",
    ),
    "TakeDoubleBattleChallenge": (
        "Do you wish to take the DOUBLE BATTLE HALL challenge?",
    ),
    "ExplainDoubleBattleChallenge": challenge("DOUBLE BATTLE",
                                              "DOUBLE BATTLE HALLS"),
    "ReturnWhenFortified": (
        "Return when your heart and your POKéMON are ready.",
    ),
    "WhichChallenge": (
        "There are two BATTLE HALLS: Level 50 and Open Level.",
        "Which will you take?",
    ),
    "NotEnoughValidMonsLv50": (
        "Sigh...",
        "You do not have the three POKéMON the challenge requires.",
        "They must be three different kinds, all Level 50 or lower, and no "
        "two may hold the same kind of item.",
        "EGGS{STR_VAR_1} ineligible.",
        "Come back when you are prepared.",
    ),
    "NotEnoughValidMonsLvOpen": (
        "Sigh...",
        "You do not have the three POKéMON the challenge requires.",
        "They must be three different kinds, and no two may hold the same "
        "kind of item.",
        "EGGS{STR_VAR_1} ineligible.",
        "Come back when you are prepared.",
    ),
    "NowSelectThreeMons": (
        "Good. Now select your three POKéMON.",
    ),
    "MustSaveBeforeChallenge2": (
        "I must save before I show you to the BATTLE HALL. Is that "
        "acceptable?",
    ),
    "MustSaveBeforeChallenge": (
        "I must save before I show you to the BATTLE HALL. Is that "
        "acceptable?",
    ),
    "FollowMe": (
        "Good.|Follow me.",
    ),
    "ResultsWillBeRecorded": (
        "I count it a privilege to have watched your POKéMON.",
        "The result will be recorded. I must ask you to wait a moment.",
    ),
    "FirmTrueBondsFor7WinStreak": (
        "Seven in a row...",
        "What binds you to your POKéMON is evidently firm, and evidently "
        "true.",
    ),
    "FeatWillBeRecorded": (
        "It will be recorded. I must ask you to wait a moment.",
    ),
    "BattlePointsFor7WinStreak": (
        "For seven wins in a row, we present you with Battle Point(s).",
    ),
    "NoSpaceForPrize": (
        "You appear to have no room for what we would give you.",
        "Return when your BAG is in order.",
    ),
    "WeHaveBeenWaiting": (
        "We have been waiting for you...",
    ),
    "FailedToSaveBeforeEndingChallenge": (
        "Sigh...",
        "You did not save before you ended your challenge last time.",
        "It is forfeit. That is most unfortunate.",
    ),
    "ReceivedPrize": (
        "{PLAYER} received the prize {STR_VAR_1}.",
    ),
    "LadyCanTellWhatMonsThink": (
        "For a hardy man, hardy POKéMON. That's my view.",
        "Attack is the best defence!|Keep swinging and never stop!",
        "But that isn't what I wanted to talk about.",
        "There's a lady comes by here now and then.",
        "She says she can tell what a POKéMON is thinking.",
        "I couldn't say about that. She is very pretty, though.",
        "What?|Why are you looking at me like that?",
    ),
    "NatureAndMovesKeyHere": (
        "Hmm...",
        "It comes down to a POKéMON's nature, and to the moves it has been "
        "taught.",
        "More exactly: to how well those moves suit that nature.",
        "If one of yours is in difficulty and cannot seem to do what it "
        "should, look at whether its moves are ones it likes using.",
    ),
    "MonDocileButTransforms": (
        "Mine is a mild thing, normally.",
        "But in a BATTLE HALL it turns into something else entirely.",
        "Frightening, honestly. I hardly know it.",
    ),
    "WhatNatureFavorsChippingAway": (
        "I wonder what nature a POKéMON has if it likes wearing an opponent "
        "down rather than hitting it.",
        "I'd be surprised if that were a LAX one.",
        "No. That can't be right.",
    ),
    "ToDefeatMavenAnd7Trainers": (
        "To beat the MASTER, and seven TRAINERS before that...",
    ),
    "PresentYouWithBattlePoints": (
        "In honour of what you and your POKéMON evidently are to one "
        "another, we present you with these Battle Point(s).",
    ),
    "LikeToRecordMatch": (
        "Shall I put your last BATTLE PALACE match on your CIRCUIT PASS?",
    ),
    "RulesAreListed": (
        "The BATTLE HALL rules are set out here.",
    ),
    "ReadWhichHeading": (
        "Which heading will you read?",
    ),
    "ExplainRulesBasics": (
        "Here, a POKéMON decides for itself. You may switch it out and "
        "nothing more.",
        "What it decides depends on its nature -- and a POKéMON raised among "
        "people has more nature in it than a wild one, not less.",
    ),
    "ExplainRulesUnderpowered": (
        "This is the part that decides a challenge.",
        "A POKéMON is poor at any move its nature dislikes, and here nobody "
        "is telling it otherwise.",
        "Bring one whose moves it has no wish to use, and it will not come "
        "near what it is capable of.",
    ),
    "ExplainRulesNature": (
        "One nature would rather attack, whatever the situation.",
        "Another would rather keep itself from harm.",
        "Another enjoys confusing and vexing a foe.",
        "Each nature has moves it is happy with and moves it is not.",
    ),
    "ExplainRulesMoves": (
        "A POKéMON weighs its moves in three kinds.",
        "Those that damage a foe directly.",
        "Those that guard, or prepare, or restore HP.",
        "And the odder sort, that leave a foe poisoned or paralysed or "
        "otherwise the worse for it.",
    ),
    "ExplainRulesWhenInDanger": (
        "Some natures change their minds when things go badly, and reach for "
        "moves they would not normally touch.",
        "If one of yours starts behaving unlike itself in a tight place, "
        "watch it closely.",
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
        masked = masked[:start] + '\t.string "<ARAUNA_BATTLE_PALACE_LOBBY_EN>"\n\n' + masked[end:]
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

    # The two halls are one explanation with the format swapped in.
    singles = flat("ExplainSingleBattleChallenge")
    doubles = flat("ExplainDoubleBattleChallenge")
    if (singles.replace("SINGLE", "X") != doubles.replace("DOUBLE", "X")):
        raise ValueError(
            "the single and double hall explanations differ somewhere other "
            "than the format")

    # A player who misreads this facility brings the wrong team and loses
    # seven times before finding out why. These three facts prevent that.
    both = " ".join(flat(label) for label in (
        "ExplainRulesBasics", "ExplainRulesUnderpowered", "ExplainRulesNature",
        "ExplainRulesMoves", "ExplainRulesWhenInDanger"))
    if "nature" not in both:
        raise ValueError("the rules no longer mention nature at all")
    if "switch" not in both:
        raise ValueError("the rules no longer say switching is all you may do")
    if "dislikes" not in both:
        raise ValueError(
            "the rules no longer say a POKéMON is poor at moves its nature "
            "dislikes -- which is the fact that decides a challenge here")

    # And the challenge text itself has to say the trainer gives no orders.
    for label in ("ExplainSingleBattleChallenge", "ExplainDoubleBattleChallenge"):
        if "switch" not in flat(label):
            raise ValueError(f"{label}: no longer states the switching rule")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BATTLE PALACE lobby in English.")
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
    print(f"Battle Palace lobby English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""The BATTLE FACTORY lobby, where nobody brings their own POKéMON.

Everything here is rented. You are handed three, you battle with them, and
after every win you may take one thing off the trainer you just beat. That
single rule is what the facility is, and it is the rule Emerald buries: its
explanation lists the swap conditions in four separate headings without ever
saying plainly that you cannot see what you are swapping for.

So the swap rules are reordered to put that first. A player who reads these
should be able to say, before entering, what they may swap, with whom, how
often, and what they will not be told.

The singles and doubles guides say the same thing twice, once for each
tournament, and the renderer holds them to it: the two explanations must
differ only where the format does.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

LOBBY = ROOT / "data" / "maps" / "BattleFrontier_BattleFactoryLobby" / "scripts.inc"
PREFIX = "BattleFrontier_BattleFactoryLobby_Text_"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 14}, width=34)

WHOLE = ("BATTLE FACTORY", "Battle Swap", "CIRCUIT PASS",
         "SINGLE BATTLE", "DOUBLE BATTLE", "Open Level", "Level 100",
         "Battle Point", "Battle Points")


def challenge(format_name: str, kind: str) -> tuple[str, ...]:
    """The two tournament explanations differ only where the format does."""
    return (
        f"The Battle Swap {format_name} Tournament is a {kind} competition, "
        f"fought entirely with rented POKéMON.",
        "You are loaned three of them for the event.",
        f"With those three you fight a {kind}.",
        "Win, and you may take one POKéMON off the TRAINER you beat, in "
        "exchange for one of yours.",
        "Battle, swap, battle again. Seven wins in a row and you earn "
        "Battle Points.",
        "If you must stop part way, save the game. If you do not save, the "
        "challenge is forfeit.",
    )


TARGETS: dict[str, tuple[str, ...]] = {
    "WelcomeForSingleBattle": (
        "Where a TRAINER's judgement is put to the question!",
        "Welcome to the BATTLE FACTORY!",
        "I am your guide to the Battle Swap Single Tournament.",
    ),
    "TakeSinglesChallenge": (
        "Would you like to take the Battle Swap Single challenge?",
    ),
    "ExplainSinglesChallenge": challenge("Single", "SINGLE BATTLE"),
    "WelcomeForDoubleBattle": (
        "Where a TRAINER's judgement is put to the question!",
        "Welcome to the BATTLE FACTORY!",
        "I am your guide to the Battle Swap Double Tournament.",
    ),
    "TakeDoublesChallenge": (
        "Would you like to take the Battle Swap Double challenge?",
    ),
    "ExplainDoublesChallenge": challenge("Double", "DOUBLE BATTLE"),
    "LookForwardToNextVisit": (
        "We shall look forward to your next visit.",
    ),
    "WhichLevelMode": (
        "Which level will you take?|Level 50, or Open Level?",
    ),
    "OkayToSaveBeforeChallenge": (
        "Before you begin, I must save the game. Is that all right?",
    ),
    "WillHoldMonsForSafekeeping": (
        "Then I'll keep your own POKéMON safe while you compete.",
    ),
    "StepThisWay": (
        "Step this way, please.",
    ),
    "ReturnMonsSaveResults": (
        "Thank you for taking part.",
        "I'll give you your own POKéMON back and take our rentals.",
        "I must save the results as well. One moment.",
    ),
    "ReturnMons": (
        "I'll give you your own POKéMON back and take our rentals.",
    ),
    "CongratsSevenWins": (
        "Congratulations! Seven straight Battle Swap matches!",
    ),
    "AwardBattlePointsForStreak": (
        "In recognition of seven wins in a row, we award you these Battle "
        "Point(s).",
    ),
    "MaxBattlePoints": (
        "Oh -- oh dear.",
        "Your Battle Points are at their limit.",
        "Do come back once you have spent some.",
    ),
    "WaitingForYouToResume": (
        "We've been waiting for you.",
        "Before we take up where you left off, I must save the game.",
    ),
    "DidntSaveBeforeQuitting": (
        "I'm sorry to say it, but you didn't save before you stopped "
        "playing last time.",
        "That forfeits the challenge you were on.",
    ),
    "WellReturnMons": (
        "We'll give you your own POKéMON back.",
    ),
    "ReceivedPrizeItem": (
        "{PLAYER} received the prize {STR_VAR_1}.",
    ),
    "CongratsForDefeatingHead": (
        "Congratulations on beating the MASTER, and on seven matches in a "
        "row!",
    ),
    "AwardBattlePoints": (
        "In recognition of what you clearly know about POKéMON, we award you "
        "these Battle Point(s).",
    ),
    "ExchangeMonsAndSave": (
        "Let me trade your POKéMON back for our rentals.",
        "I must save the battle data. Please wait.",
    ),
    "RecordLastMatch": (
        "Shall I put your last BATTLE FACTORY match on your CIRCUIT PASS?",
    ),
    "NeedKnowledgeOfMonsMoves": (
        "Hello! You there!",
        "Thinking this place is easy, since you don't need a team of your "
        "own?",
        "I shouldn't be too sure of that.",
        "Without knowing POKéMON and what their moves do, you won't keep "
        "winning here for long.",
    ),
    "SwappedForWeakMon": (
        "I swapped for a weak one...|I was sure it was a good kind...",
        "They went straight through us...",
    ),
    "NeedToCheckOpponentsMons": (
        "Nothing has gone my way at all.",
        "You have to watch what the other side is using during the battle, "
        "and decide whether it's worth taking.",
    ),
    "CantFigureOutStaffHints": (
        "You know the staff here drop you a hint about who's next?",
        "Well. I'm a grown man, and half the time I can't work out what they "
        "mean.",
    ),
    "RentalMonsAreVaried": (
        "I'm good at this, but I bore easily, so I just kept swapping and "
        "battling and swapping again.",
        "And doing that often enough, I noticed the rentals aren't always "
        "the same ones.",
    ),
    "RulesAreListed": (
        "The Battle Swap rules are set out here.",
    ),
    "ReadWhichHeading": (
        "Which heading will you read?",
    ),
    "ExplainBasicRules": (
        "In a Battle Swap event you use three POKéMON and no more.",
        "Rented or swapped, you may never hold two of the same kind at once.",
    ),
    "ExplainSwapPartnerRules": (
        "You may only swap with the TRAINER you have just beaten, and only "
        "for a POKéMON that TRAINER actually used.",
    ),
    "ExplainSwapNumberRules": (
        "One swap after every win.",
        "There is no swap after the seventh TRAINER -- that one is the last.",
    ),
    "ExplainSwapNotesRules": (
        "Two things to know before you swap.",
        "You cannot see the stats of what you are taking. You are choosing "
        "on what you saw it do in the battle.",
        "And your three stay in the order you rented them. A swap changes "
        "the POKéMON, never the position.",
    ),
    "ExplainOpenLvRules": (
        "At Open Level, every rented POKéMON and every POKéMON you face is "
        "Level 100.",
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
        masked = masked[:start] + '\t.string "<ARAUNA_BATTLE_FACTORY_LOBBY_EN>"\n\n' + masked[end:]
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

    # The two tournaments are one explanation with the format swapped in. If
    # they have drifted apart anywhere else, one of them is now wrong.
    singles = flat("ExplainSinglesChallenge")
    doubles = flat("ExplainDoublesChallenge")
    normalised = (singles.replace("SINGLE BATTLE", "X").replace("Single", "Y"),
                  doubles.replace("DOUBLE BATTLE", "X").replace("Double", "Y"))
    if normalised[0] != normalised[1]:
        raise ValueError(
            "the singles and doubles explanations differ somewhere other than "
            "the format")

    # A player must be able to answer, before entering: what may I swap, with
    # whom, how often, and what am I not told?
    swapping = " ".join(flat(label) for label in (
        "ExplainSwapPartnerRules", "ExplainSwapNumberRules",
        "ExplainSwapNotesRules"))
    for fact in ("just beaten", "after every win", "seventh", "cannot see"):
        if fact not in swapping:
            raise ValueError(f"the swap rules no longer say: {fact!r}")
    if "order" not in swapping:
        raise ValueError("the swap rules no longer say the order is fixed")

    # Everything here is rented, and that is the facility. Both welcomes and
    # both explanations have to say so.
    for label in ("ExplainSinglesChallenge", "ExplainDoublesChallenge"):
        if "rented" not in flat(label):
            raise ValueError(f"{label}: no longer says the POKéMON are rented")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BATTLE FACTORY lobby in English.")
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
    print(f"Battle Factory lobby English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

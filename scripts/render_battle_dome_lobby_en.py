#!/usr/bin/env python3
"""The BATTLE DOME lobby, where you enter three and only two of them battle.

The dome runs a four-round knockout. You register three POKéMON, and before
each match you see the other trainer's three and pick two of your own to send.
That choosing is the whole facility, and it is the one thing Emerald's
explanation states last, after the format, the count and the prize.

So it goes first here. A player who reads this should leave the desk knowing
that the team they register is not the team they fight with, and that they
get to look before they decide.

The two tournament explanations are one text with the format swapped in, and
the four "previous results" lines are one sentence with two variables in it,
so both are generated rather than kept as hand-maintained copies.

The offer to record a match on the CIRCUIT PASS is not here: it belongs to
render_circuit_pass_facilities_en_checked.py, further down the manifest,
which writes that offer for every facility at once. Writing it here as well
would only mean writing it into a block the later renderer overwrites.
"""
from __future__ import annotations

import argparse
import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

LOBBY = ROOT / "data" / "maps" / "BattleFrontier_BattleDomeLobby" / "scripts.inc"
PREFIX = "BattleFrontier_BattleDomeLobby_Text_"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 14}, width=34)

WHOLE = ("BATTLE DOME", "CIRCUIT PASS", "SINGLE BATTLE",
         "SINGLE BATTLES", "DOUBLE BATTLE", "DOUBLE BATTLES", "Open Level",
         "Battle Point", "Battle Points", "Battle Tournament", "Waiting Room")


def challenge(kind: str) -> tuple[str, ...]:
    """The two tournaments differ only where the format does."""
    return (
        f"The {kind} Tournament is what it sounds like: a knockout of "
        f"{kind}S.",
        "Every TRAINER registers three POKéMON.",
        "But only two of them fight any given match. The third waits out.",
        "And you choose which two after you have seen the other TRAINER's "
        "three. That choosing is the tournament.",
        "Beat four TRAINERS and it is yours.",
        "Battle Points go to the winner.",
        "If you must stop part way, save the game. If you do not save, you "
        "are out.",
    )


def previous(level: str, kind: str) -> tuple[str, ...]:
    return (f"Those are the results of the last {level} {kind} Tournament.",)


TARGETS: dict[str, tuple[str, ...]] = {
    "WelcomeSingleBattle": (
        "Where a TRAINER's planning is put to the question!",
        "Welcome to the BATTLE DOME!",
        "I am your guide to the SINGLE BATTLE Tournament.",
    ),
    "TakeSinglesChallenge": (
        "Would you like to enter the SINGLE BATTLE Tournament?",
    ),
    "ExplainSinglesChallenge": challenge("SINGLE BATTLE"),
    "WelcomeDoubleBattle": (
        "Where a TRAINER's planning is put to the question!",
        "Welcome to the BATTLE DOME!",
        "I am your guide to the DOUBLE BATTLE Tournament.",
    ),
    "TakeDoublesChallenge": (
        "Would you like to enter the DOUBLE BATTLE Tournament?",
    ),
    "ExplainDoublesChallenge": challenge("DOUBLE BATTLE"),
    "HopeToSeeYouAgain": (
        "We hope to see you again.",
    ),
    "OkayToSaveBeforeChallenge": (
        "Before I show you through, I must save the data. Is that all right?",
    ),
    "OkayToSaveBeforeChallenge2": (
        "Before I show you through, I must save the data. Is that all right?",
    ),
    "WhichLevelMode": (
        "The tournament runs at two levels: Level 50 and Open Level.",
        "Which will you enter?",
    ),
    "SelectThreeMons": (
        "Now select the three POKéMON you wish to register, please.",
    ),
    "NotEnoughValidMonsLvOpen": (
        "Excuse me!",
        "You don't have three eligible POKéMON.",
        "They must also be holding different kinds of items.",
        "EGGS{STR_VAR_1} ineligible.",
        "Come and see me when you're ready.",
    ),
    "NotEnoughValidMonsLv50": (
        "Excuse me!",
        "You don't have three eligible POKéMON.",
        "You need three different POKéMON, Level 50 or under, to enter.",
        "They must also be holding different kinds of items.",
        "EGGS{STR_VAR_1} ineligible.",
        "Come and see me when you're ready.",
    ),
    "ShowYouToBattleDome": (
        "I'll show you through to the BATTLE DOME.",
    ),
    "DidntSaveBeforeQuitting": (
        "Excuse me!",
        "You didn't save before you stopped last time.",
        "I'm afraid that puts you out of the tournament you were in. Sorry!",
    ),
    "CongratsForWinningTourney": (
        "Congratulations on winning your Battle Tournament!",
    ),
    "HereIsYourPrize": (
        "Here is your prize for taking the tournament.",
    ),
    "ReceivedPrize": (
        "{PLAYER} received the prize {STR_VAR_1}.",
    ),
    "BagFullMakeRoom": (
        "Oh -- your BAG appears to be full.",
        "Make a little room and come back to me.",
    ),
    "ThankYouForPlaying": (
        "Thank you for entering!",
    ),
    "RecordWillBeSaved": (
        "Your record will be saved. One moment.",
    ),
    "WeveBeenWaitingForYou": (
        "We've been waiting for you!",
    ),
    "PrevTourneyResultsSinglesLv50": previous("Level 50", "SINGLE BATTLE"),
    "PrevTourneyResultsDoublesLv50": previous("Level 50", "DOUBLE BATTLE"),
    "PrevTourneyResultsSinglesLvOpen": previous("Open Level", "SINGLE BATTLE"),
    "PrevTourneyResultsDoublesLvOpen": previous("Open Level", "DOUBLE BATTLE"),
    "LastWinnerWasTough": (
        "Did you see it? The last tournament?",
        "The winner, {STR_VAR_1}, was something to watch.",
        "Have a look at the results on the monitor by the PC.",
    ),
    "WinnersGainReputation": (
        "A TRAINER who takes tournament after tournament here gets a name "
        "for it.",
        "And a name draws the hard ones in. They come to see for themselves.",
        "Which is why keeping the run going is the difficult part, not "
        "starting it.",
    ),
    "TrashedInFirstRound": (
        "I drew one of the favourites in the first round.",
        "You can imagine how that went...",
    ),
    "NeedToCheckOpponentCarefully": (
        "I'd have won if I'd kept this one back.",
        "Look properly at what the other side has registered before you "
        "choose your two. That's the whole thing.",
    ),
    "CongratsDefeatedTucker": (
        "Congratulations!",
        "You beat the MASTER and took the tournament!",
    ),
    "AwardTheseBattlePoints": (
        "In recognition of a plan that was a pleasure to watch, we award you "
        "these Battle Point(s)!",
    ),
    "RulesAreListed": (
        "The tournament rules are set out here.",
    ),
    "ReadWhichHeading": (
        "Which heading will you read?",
    ),
    "ExplainMatchupRules": (
        "The draw is made on how strong the entered POKéMON are.",
        "It is arranged so the strongest TRAINERS do not meet in the first "
        "round.",
    ),
    "ExplainTourneyTree": (
        "The draw -- we call it the Tree -- can be seen in the Waiting Room. "
        "Ask any guide.",
        "It shows more than who plays whom.",
        "You get the last tournament's results, what each TRAINER has "
        "entered, and how each of them tends to battle.",
    ),
    "ExplainDoubleKORules": (
        "If both sides faint on the same turn, the REFEREES review the match "
        "and name the winner.",
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
        masked = masked[:start] + '\t.string "<ARAUNA_BATTLE_DOME_LOBBY_EN>"\n\n' + masked[end:]
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

    # The two tournaments are one text with the format swapped in.
    singles = flat("ExplainSinglesChallenge").replace("SINGLE", "X")
    doubles = flat("ExplainDoublesChallenge").replace("DOUBLE", "X")
    if singles != doubles:
        raise ValueError(
            "the two tournament explanations differ somewhere other than the "
            "format")

    # The four results lines are one sentence with two variables. Any two of
    # them reading identically means a player is told the wrong tournament.
    results = [flat(f"PrevTourneyResults{a}{b}")
               for a, b in itertools.product(("Singles", "Doubles"),
                                             ("Lv50", "LvOpen"))]
    if len(set(results)) != len(results):
        raise ValueError("two of the previous-results lines are identical")

    # The dome is the facility where the team you register is not the team you
    # fight with, and where you get to look first. Both must survive.
    for label in ("ExplainSinglesChallenge", "ExplainDoublesChallenge"):
        text = flat(label)
        if "three" not in text or "two" not in text:
            raise ValueError(f"{label}: no longer says three are entered and two fight")
        if "seen" not in text:
            raise ValueError(
                f"{label}: no longer says you choose after seeing the other "
                f"TRAINER's team")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BATTLE DOME lobby in English.")
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
    print(f"Battle Dome lobby English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

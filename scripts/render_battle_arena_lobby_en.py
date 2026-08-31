#!/usr/bin/env python3
"""The BATTLE ARENA lobby, and the guide who runs the Set KO Tourney.

The arena is the facility where a battle is only three turns long and a
REFEREE decides the rest, so most of what its guide says is rules. Rules
prose has one job: a player who reads it must come away able to predict what
happens. Emerald's version is accurate and shapeless -- eleven separate
sentences about judging with no indication which of them matters -- so it is
reordered here to put the consequence first and the mechanism after.

The three judging factors keep their names. Mind, Skill and Body are printed
in the arena's own results screen, so a player who reads "aggression" here and
sees "Mind" there has been told two different things; the renderer checks all
three survive.

This guide addresses the player as "my dear challenger" and does not drop it
under pressure. That formality is the only thing distinguishing this
receptionist from the other five, who are all doing the same job in the same
building.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

LOBBY = ROOT / "data" / "maps" / "BattleFrontier_BattleArenaLobby" / "scripts.inc"
PREFIX = "BattleFrontier_BattleArenaLobby_Text_"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 14}, width=34)

# Names the arena prints elsewhere and cannot contradict here.
WHOLE = ("BATTLE ARENA", "Set KO Tourney", "CIRCUIT PASS",
         "Open Level", "Battle Point", "Battle Points")
FACTORS = ("Mind", "Skill", "Body")

TARGETS: dict[str, tuple[str, ...]] = {
    "WelcomeToBattleArena": (
        "Where a TRAINER's will to fight is put to the question!",
        "I welcome you to the BATTLE ARENA!",
        "I am your guide to the Set KO Tourney.",
    ),
    "WishToTakeChallenge": (
        "Now -- do you wish to take the BATTLE ARENA challenge?",
    ),
    "AwaitAnotherChallenge": (
        "We shall await your challenge on another occasion.",
    ),
    "ExplainChallenge": (
        "The BATTLE ARENA runs the Set KO Tourney.",
        "You enter with three POKéMON, in the order you want them to appear.",
        "They come out one at a time, in that order, and a POKéMON that has "
        "come out stays out until its battle is decided.",
        "A battle lasts three turns. If nothing is settled by then, the "
        "REFEREE decides it.",
        "If you must stop part way, save the game. If you do not save, you "
        "cannot come back to the challenge.",
        "And if you take seven TRAINERS one after another, we shall present "
        "you with Battle Points.",
    ),
    "OkayToSave": (
        "Before I show you in, the game must be saved. Is that acceptable?",
    ),
    "WhichLevelMode": (
        "The BATTLE ARENA offers two levels: Level 50 and Open Level.",
        "Which will you have?",
    ),
    "SelectThreeMons": (
        "Very well. Select your three POKéMON, if you please.",
    ),
    "NotEnoughValidMonsLvOpen": (
        "My dear challenger.",
        "You do not have the three POKéMON entry requires.",
        "They must be three different kinds, and no two may hold the same "
        "kind of item.",
        "EGGS{STR_VAR_1} ineligible.",
        "Do return when you are ready.",
    ),
    "NotEnoughValidMonsLv50": (
        "My dear challenger.",
        "You do not have the three POKéMON entry requires.",
        "They must be three different kinds, all of them Level 50 or lower, "
        "and no two may hold the same kind of item.",
        "EGGS{STR_VAR_1} ineligible.",
        "Do return when you are ready.",
    ),
    "GuideYouToArena": (
        "I shall show you to the BATTLE ARENA.",
    ),
    "DidntSaveBeforeShuttingDown": (
        "My dear challenger.",
        "You did not save the game before shutting down.",
        "I am afraid that disqualifies the challenge you were on.",
        "You may of course begin a fresh one.",
    ),
    "CongratsOnSevenWins": (
        "Seven TRAINERS, one after another.|Our congratulations.",
    ),
    "RecordAchievement": (
        "It will go on the record.|Please wait while I save the game.",
    ),
    "PresentYouWithPrize": (
        "In recognition of seven straight wins, we present you with this.",
    ),
    "ReceivedPrize": (
        "{PLAYER} received the prize {STR_VAR_1}.",
    ),
    "BagFullReturnForPrize": (
        "Oh?|Your BAG appears to be full.",
        "Clear a little space and come back for it.",
    ),
    "ThankYouWaitWhileSave": (
        "Thank you for taking part.",
        "Please wait while I save the game.",
    ),
    "AwaitAnotherChallenge2": (
        "We shall await your challenge on another occasion.",
    ),
    "LookingForwardToArrivalSaveGame": (
        "We have been expecting you.",
        "Before I show you in, I must save the game. One moment.",
    ),
    "RecordLastMatch": (
        "Shall I put your last BATTLE ARENA match on your CIRCUIT PASS?",
    ),
    "BadIdeaToNotAttack": (
        "I lost on the REFEREE's decision...",
        "Defending for three turns and never once attacking was, I now see, "
        "a poor plan...",
    ),
    "LandingHitsWorked": (
        "I won it in the judging!",
        "Landing hits, over and over, is what did it!",
    ),
    "MatchWasDeclaredDraw": (
        "Mine was called a draw.",
        "When the turns ran out, both sides had much the same HP left.",
    ),
    "OrderOfMonsImportant": (
        "In the BATTLE ARENA the order of your POKéMON is everything.",
        "If your first one has a type that is easily answered, make your "
        "second one the answer to that answer.",
        "Build the three so each covers the one in front. That is the whole "
        "trick of it.",
    ),
    "RulesAreListed": (
        "The rules of the Set KO Tourney are set out here.",
    ),
    "ReadWhichHeading": (
        "Which heading will you read?",
    ),
    "ExplainBattleRules": (
        "A battle here lasts three turns and no longer.",
        "If nothing has been settled by the end of the third, the REFEREE "
        "decides who won.",
        "A POKéMON that has come out cannot be switched away until its "
        "battle is over.",
        "The REFEREE weighs three things: Mind, Skill and Body.",
    ),
    "ExplainMindRules": (
        "Mind is aggression.",
        "It rises with every turn you spend attacking, and does not rise on "
        "the turns you spend doing anything else.",
    ),
    "ExplainSkillRules": (
        "Skill is whether your moves did what they were meant to.",
        "A move that lands raises it. A move that fails lowers it.",
        "An attack that is super effective raises it further; one that is "
        "not very effective lowers it.",
        "Moves like PROTECT and DETECT do not raise Skill.",
        "And if the other side used PROTECT or DETECT, a move of yours that "
        "failed against it does not lower your Skill.",
    ),
    "ExplainBodyRules": (
        "Body is the HP you have left at the end.",
        "It weighs what a POKéMON had when it came out against what it has "
        "when the turns run out.",
    ),
    "CongratsOnDefeatingTycoon": (
        "A win taken off the MASTER, and seven TRAINERS besides.",
        "Our congratulations on a most splendid challenge.",
    ),
    "PleaseAcceptBattlePoints": (
        "My dear challenger -- in recognition of a spirit that would not "
        "tire, please accept these Battle Point(s).",
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
        masked = masked[:start] + '\t.string "<ARAUNA_BATTLE_ARENA_LOBBY_EN>"\n\n' + masked[end:]
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

    # The results screen prints these three words. Explaining the same thing
    # under different names tells the player two stories.
    for factor in FACTORS:
        heading = flat(f"Explain{factor}Rules")
        if factor not in heading:
            raise ValueError(f"Explain{factor}Rules: no longer names {factor}")
    overview = flat("ExplainBattleRules")
    for factor in FACTORS:
        if factor not in overview:
            raise ValueError(f"ExplainBattleRules: does not name {factor}")

    # The rules must still state the two facts a player has to know before
    # entering: three turns, and no switching once a POKéMON is out.
    if "three turns" not in overview and "third" not in overview:
        raise ValueError("ExplainBattleRules: no longer says how long a battle is")
    if "switched" not in overview:
        raise ValueError("ExplainBattleRules: no longer says switching is barred")

    # The entry conditions are refusals a player has to be able to act on.
    for label in ("NotEnoughValidMonsLv50", "NotEnoughValidMonsLvOpen"):
        text = flat(label)
        for requirement in ("three different kinds", "same kind of item", "EGGS"):
            if requirement not in text:
                raise ValueError(f"{label}: dropped a condition: {requirement!r}")
    if "Level 50 or lower" not in flat("NotEnoughValidMonsLv50"):
        raise ValueError("NotEnoughValidMonsLv50: no longer states the level cap")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BATTLE ARENA lobby in English.")
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
    print(f"Battle Arena lobby English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

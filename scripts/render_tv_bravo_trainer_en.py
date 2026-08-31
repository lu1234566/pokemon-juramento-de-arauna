#!/usr/bin/env python3
"""BRAVO TRAINER, and the reporters who feed it.

Two interviewers -- one in the contest lobby, one in the BATTLE TOWER lobby --
stop the player, ask three questions, and the answers come back that evening
as a television segment. The segments are assembled from these blocks in the
order the engine picks, so they have to read as one continuous broadcast no
matter which branch fires.

Emerald's presenter shouted. This one still enjoys himself, but he is a local
man on a local channel, and the show is about a trainer from around here.

The slots are not interchangeable and are not a choice: the engine fills them
per block, and an easy-chat phrase, a nickname, a category and a placing all
land in different ones. The paragraphs below keep each slot in the role
src/tv.c gives it.

The four Text_None blocks are sentinels the engine compares against, not
prose, and are deliberately untouched.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox  # noqa: E402

TV = ROOT / "data" / "text" / "tv.inc"

# An easy-chat phrase is the widest thing any of these slots can hold.
BOX = TextBox({"{STR_VAR_1}": 12, "{STR_VAR_2}": 12, "{STR_VAR_3}": 12}, width=34)

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- the reporter in the contest lobby -----------------------------------
    "LilycoveCity_ContestLobby_Text_InterviewRequest": (
        ("I'm a reporter", "a few questions"), (
            "Oh, hello! You were in a POKéMON CONTEST just now, weren't you?"
            "|I can tell from your POKéMON.",
            "I'm a reporter. I'm putting together a piece on the CONTESTS.",
            "Would you answer a few questions for me?",
        )),
    "LilycoveCity_ContestLobby_Text_DescribeContest": (
        ("Oh, you will?", "describe the"), (
            "Oh, you will?|Thank you.",
            "In a few words, how would you describe the CONTEST you just came out of?",
        )),
    "LilycoveCity_ContestLobby_Text_WhatImageWhenYouHearX": (
        ("edifying comment", "what image do you get"), (
            "Ah. I see.|That's worth printing, that is.",
            "It gives a person a good idea of what the CONTEST was like.",
            "One last question.",
            "When you hear the word “{STR_VAR_2},” what do you picture?",
        )),
    "LilycoveCity_ContestLobby_Text_ThatsAllForInterview": (
        ("that's how you imagine", "look forward to it"), (
            "I see!",
            "So that is what “{STR_VAR_2}” looks like to you.",
            "Thank you!|You've given me a great deal.",
            "I can write something worth reading about the CONTESTS now.",
            "And who knows -- it might even reach the television.|Watch for it!",
        )),
    "LilycoveCity_ContestLobby_Text_PleaseDoShareStoryWithMe": (
        ("too bad", "share it with me"), (
            "Oh, that's a pity...",
            "Well -- if you ever come across a story, bring it to me.",
        )),
    "LilycoveCity_ContestLobby_Text_LookingForwardToNextContest": (
        ("looking forward",), (
            "I'll be watching for your next POKéMON CONTEST.",
        )),

    # -- the show itself -----------------------------------------------------
    "gTVBravoTrainerText00": (("BRAVO TRAINER time", "boasts a"), (
        "Yeah!|It's BRAVO TRAINER time!",
        "Tonight we look at a POKéMON belonging to {STR_VAR_1}.",
        "And this one carries a {STR_VAR_3} Rank in the {STR_VAR_2} Category.",
    )),
    "gTVBravoTrainerText01": (("Introducing", "Even the nickname"), (
        "Introducing {STR_VAR_2}, the {STR_VAR_1}!",
        "{STR_VAR_2}...",
        "Even the name it answers to says “{STR_VAR_3}” out loud!",
    )),
    "gTVBravoTrainerText02": (("impassioned", "trusty partner"), (
        "Now, when {STR_VAR_1} entered this POKéMON in a CONTEST, we got a few "
        "warm words out of the pair of them.",
    )),
    "gTVBravoTrainerText03": (("huge", "perfectly suits"), (
        "Asked about the CONTEST afterwards, {STR_VAR_1} grinned and said, "
        "“{STR_VAR_2}!”",
        "And why not -- {STR_VAR_1}'s POKéMON came in at number {STR_VAR_3}.",
        "That line fits {STR_VAR_1} tonight, I'd say!",
    )),
    "gTVBravoTrainerText04": (("tinge of", "comes across"), (
        "Asked about the CONTEST afterwards, {STR_VAR_1} said, with something "
        "sour in it, “{STR_VAR_2}.”",
        "And why not -- {STR_VAR_1}'s POKéMON came in at number {STR_VAR_3}.",
        "You can hear exactly how {STR_VAR_1} feels about that!",
    )),
    "gTVBravoTrainerText05": (("also like to know", "condensed"), (
        "And wouldn't you like to know what {STR_VAR_1} makes of {STR_VAR_2}?",
        "So would we!|So we asked!",
        "And it all came down to this:|“{STR_VAR_3}!”",
        "That is what {STR_VAR_2} means to {STR_VAR_1}!",
    )),
    "gTVBravoTrainerText06": (("last move", "entirely about"), (
        "That last {STR_VAR_2} from the {STR_VAR_1} was “{STR_VAR_3}” from "
        "start to finish!",
    )),
    "gTVBravoTrainerText07": (("Bravo", "all the time we have"), (
        "Bravo, {STR_VAR_1}!|Bravo, {STR_VAR_2}!",
        "May the pair of them climb higher still!",
        "That's all the time we have.|Until next week -- good night!",
    )),
    "gTVBravoTrainerText08": (("Introducing the TRAINER",), (
        "And here is the TRAINER's {STR_VAR_1}!",
    )),

    # -- the reporter in the tower lobby -------------------------------------
    "BattleFrontier_BattleTowerLobby_Text_InterviewRequest": (
        ("gathering interviews", "impressions on battling"), (
            "Hello! You're the TRAINER who just came out of a battle, aren't you?",
            "I'm collecting interviews with TRAINERS wherever I can find them.",
            "Might I have a few words about how it went?",
        )),
    "BattleFrontier_BattleTowerLobby_Text_HowDidBattleTowerTurnOut": (
        ("You will? Really?", "satisfied with the battle"), (
            "You will? Really?|Thank you!|Then, er...",
            "How did it go in the BATTLE TOWER today?",
            "Are you satisfied with it? Or not?",
        )),
    "BattleFrontier_BattleTowerLobby_Text_SorryWeDisturbedYou": (
        ("Sorry we disturbed", "next"), (
            "Oh...|Sorry to have troubled you.",
            "Give me an interview the next time you're at the BATTLE TOWER.",
        )),
    "BattleFrontier_BattleTowerLobby_Text_ObviousYouHadGreatBattle": (
        ("of course", "great"), (
            "Well, of course you are!",
            "That look on your face gives it away entirely...",
            "You've had a fine battle. Anyone could see it.",
        )),
    "BattleFrontier_BattleTowerLobby_Text_DifficultToMakeBattleTurnOutAsPlanned": (
        ("difficult", "as planned"), (
            "Oh. I see...",
            "It is a hard thing, making a battle come out the way you meant it to.",
        )),
    "BattleFrontier_BattleTowerLobby_Text_DescribeYourBattle": (
        ("one more question", "one saying"), (
            "Oh -- may I ask one more thing?",
            "If you had to put this battle into a single saying, what would it be?",
        )),
    "BattleFrontier_BattleTowerLobby_Text_ThatsGreatLine": (
        ("stunningly cool", "see you again"), (
            "Oh, that is a fine thing to say!",
            "What a line!|May the next one go as well.",
            "I hope I catch you again!",
        )),
    "BattleFrontier_BattleTowerLobby_Text_SilentType": (
        ("silent type", "share your thoughts"), (
            "Oh. I see...",
            "Still -- there's something to be said for keeping it to yourself.",
            "I hope you'll let me ask again another time!",
        )),
    "BattleFrontier_BattleTowerLobby_Text_LookingForwardToNextBattle": (
        ("looking forward",), (
            "I'll be watching for your next battle!",
        )),

    # -- the same show, reporting on the tower --------------------------------
    "BravoTrainerBattleTower_Text_Intro": (("BRAVO TRAINER time", "wicked"), (
        "Yeah!|It's BRAVO TRAINER time!",
        "Tonight, {STR_VAR_1}, who went and took on the BATTLE TOWER!",
        "And went in with one fearsome {STR_VAR_2}.",
    )),
    "BravoTrainerBattleTower_Text_NewRecord": (("new record", "Bravo"), (
        "The pair set a new mark of {STR_VAR_2} straight wins in {STR_VAR_1}!"
        "|Bravo, TRAINER!",
    )),
    "BravoTrainerBattleTower_Text_Lost": (("succumbed", "bad luck"), (
        "The two of them came undone against {STR_VAR_1} in match {STR_VAR_2}."
        "|Well fought, TRAINER!",
        "And hard luck, too -- to meet {STR_VAR_1} that early is nobody's fault.",
        "We asked the TRAINER about that match with {STR_VAR_1}.",
    )),
    "BravoTrainerBattleTower_Text_Won": (("won it all", "moment of glory"), (
        "The two of them took the lot, going through {STR_VAR_1}'s {STR_VAR_2} "
        "cleanly.|Bravo, TRAINER!",
        "Putting away {STR_VAR_1}...|You wouldn't credit it!",
        "We asked the TRAINER about the moment it happened.",
    )),
    "BravoTrainerBattleTower_Text_LostFinal": (("final hurdle", "celebrity pair"), (
        "After a long run of wins, the pair came undone at the last, against "
        "{STR_VAR_1}'s {STR_VAR_2}.",
        "Well fought, TRAINER!",
        "And give them their due -- you don't often see a pairing as known as "
        "{STR_VAR_1} and {STR_VAR_2}.",
        "We asked the TRAINER what it was like.",
    )),
    "BravoTrainerBattleTower_Text_Satisfied": (("refreshing reply", "full satisfaction"), (
        "Here is what the TRAINER told us:|“I'm satisfied!”",
        "Isn't that a clean answer?|Bravo, TRAINER!",
        "And isn't it a fine thing, to come out of a battle satisfied?",
        "I found out just how satisfied when I heard this:",
    )),
    "BravoTrainerBattleTower_Text_Unsatisfied": (("not satisfied", "dissatisfied"), (
        "Here is what the TRAINER told us:|“I'm not satisfied...”",
        "And you could see it, too, when it was said.",
        "Still -- coming out of a battle content is no small thing, is it?",
        "I found out just how far from it when I heard this:",
    )),
    "BravoTrainerBattleTower_Text_Response": (("{STR_VAR_1}",), (
        "“{STR_VAR_1}.”",
    )),
    "BravoTrainerBattleTower_Text_ResponseSatisfied": (("isn't that great", "joy"), (
        "“{STR_VAR_1}.”|Now isn't that something?",
        "It has all of {STR_VAR_2}'s joy in it, I'd say.",
        "That last battle, against {STR_VAR_3}... it really was "
        "“{STR_VAR_1}” and nothing else!",
    )),
    "BravoTrainerBattleTower_Text_ResponseUnsatisfied": (("fitting", "comes across"), (
        "“{STR_VAR_1}.”|Now isn't that the word for it?",
        "That last battle, against {STR_VAR_3}... there's no other way to put "
        "it but “{STR_VAR_1}”!",
        "You can hear exactly how {STR_VAR_2} feels about that!",
    )),
    "BravoTrainerBattleTower_Text_Outro": (("Bravo", "all the time we have"), (
        "Bravo, {STR_VAR_1}!|Bravo, {STR_VAR_2}!",
        "May the pair of them climb higher still!",
        "That's all the time we have.|Until next week -- good night!",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    return {label: BOX.compose(paragraphs)
            for label, (_, paragraphs) in TARGETS.items()}


def render(source: str) -> str:
    composed = payloads()
    rendered = source
    for label, (markers, _) in TARGETS.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target contains no .string payload")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
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
        masked = masked[:start] + '\t.string "<ARAUNA_TV_BRAVO_TRAINER_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    """A slot the engine does not fill for a block prints the previous one."""
    composed = payloads()
    for label in TARGETS:
        available = set(re.findall(r"\{STR_VAR_\d\}",
                                   block_pattern(label).search(source).group("body")))
        used = set(re.findall(r"\{STR_VAR_\d\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    # The sentinels the engine compares against, not prose.
    for label in ("BravoTrainerBattleTower_Text_None1", "BravoTrainerBattleTower_Text_None2",
                  "BravoTrainerBattleTower_Text_None3", "BravoTrainerBattleTower_Text_None4"):
        if block_pattern(label).search(rendered).group("body").strip() != '.string "None$"':
            raise ValueError(f"{label}: sentinel must stay exactly \"None\"")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the BRAVO TRAINER broadcasts.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TV.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        TV.write_text(rendered, encoding="utf-8")
    print(f"TV Bravo Trainer English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

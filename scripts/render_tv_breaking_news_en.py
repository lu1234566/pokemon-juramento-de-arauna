#!/usr/bin/env python3
"""BREAKING NEWS, the rival bulletin, the trend watcher and two letter shows.

BREAKING NEWS treats one trainer catching one POKéMON as a live outside
broadcast, and the joke only lands if the reporter never once admits how small
the story is. So the reporter here is entirely sincere, right through to
envying the trainer for getting to shout.

TREND-WATCHER is the opposite kind of failure: a presenter chasing what is
current, and a guest who only knows what used to be. Neither of them wins,
which is the point, so the interview is left going nowhere.

TODAY'S RIVAL TRAINER reports on somebody the viewer has never met, in the
tone of a league table. TREASURE INVESTIGATORS and FIND THAT GAMER read out
other people's letters.

Two things here are the project's own and not Emerald's: the ARAUNA TREASURE
INVESTIGATORS, and the BATTLE CIRCUIT, which is what this region calls the
place where symbols are won. The renderer refuses a payload that renames
either back.
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

# The slots hold map names here as often as they hold anything else.
BOX = TextBox({"{STR_VAR_1}": 14, "{STR_VAR_2}": 14, "{STR_VAR_3}": 14}, width=34)

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- the rival bulletin ---------------------------------------------------
    "gTVTodaysRivalTrainerText00": (("TODAY'S RIVAL TRAINER", "one of our rivals"), (
        "TODAY'S RIVAL TRAINER!",
        "Good evening, fellow TRAINERS.|How are we all keeping?",
        "Tonight, as every night, we take the measure of one of our rivals.",
    )),
    "gTVTodaysRivalTrainerText01": (("how many BADGES",), (
        "And how many BADGES has our rival? The count is {STR_VAR_1}!",
    )),
    "gTVTodaysRivalTrainerText02": (("single BADGE",), (
        "Though our rival has yet to take a single BADGE!",
    )),
    "gTVTodaysRivalTrainerText03": (("BATTLE CIRCUIT Symbol",), (
        "Our rival has yet to take a single BATTLE CIRCUIT Symbol.",
    )),
    "gTVTodaysRivalTrainerText04": (("Gold Symbols", "Silver Symbols"), (
        "Let's see how our rival stands for BATTLE CIRCUIT Symbols.",
        "Gold: {STR_VAR_1}!|Silver: {STR_VAR_2}!",
    )),
    "gTVTodaysRivalTrainerText05": (("Battle\\n", "Point(s)"), (
        "Our rival has taken {STR_VAR_1} Battle Point(s) at the BATTLE "
        "CIRCUIT.",
    )),
    "gTVTodaysRivalTrainerText06": (("measure up", "keep moving forward"), (
        "So -- how do you stand beside {STR_VAR_1}?",
        "The road goes on!",
        "Fellow TRAINERS!",
        "Let us all keep walking, and keep a step ahead of our rivals!",
    )),
    "gTVTodaysRivalTrainerText07": (("around", "registered"), (
        "Tonight's rival TRAINER is {STR_VAR_1}, who is around {STR_VAR_3} "
        "at present.",
        "{STR_VAR_1} has {STR_VAR_2} POKéMON entered in the POKéDEX so far.",
    )),
    "gTVTodaysRivalTrainerText08": (("SECRET BASE", "registered"), (
        "Tonight's rival TRAINER is {STR_VAR_1}, who is in a SECRET BASE at "
        "present.",
        "{STR_VAR_1} has {STR_VAR_2} POKéMON entered in the POKéDEX so far.",
    )),
    "gTVTodaysRivalTrainerText09": (("So far", "registered"), (
        "Tonight's rival TRAINER is {STR_VAR_1}.",
        "So far, {STR_VAR_1} has {STR_VAR_2} POKéMON entered in the POKéDEX.",
    )),
    "gTVTodaysRivalTrainerText10": (("ferry", "registered"), (
        "Tonight's rival TRAINER is {STR_VAR_1}, who is aboard a ferry at "
        "present.",
        "{STR_VAR_1} has {STR_VAR_2} POKéMON entered in the POKéDEX so far.",
    )),

    # -- the trend watcher ----------------------------------------------------
    "TrendWatcher_Text_Intro": (("TREND-WATCHER", "in thing of the moment"), (
        "PORTO DAS REDES TREND-WATCHER NETWORK!",
        "MC: All right! We keep it straight from the street: what is moving "
        "in PORTO DAS REDES tonight.",
        "Our guest is a gentleman whose claim to fame is knowing everything "
        "there is to know about PORTO DAS REDES.",
        "Old man: Pleased to be here.",
        "MC: So let's get right to it.",
        "What is it that has the good people of PORTO DAS REDES talking?",
        "Old man: {STR_VAR_1} {STR_VAR_2}.",
        "MC: {STR_VAR_1} {STR_VAR_2}, you say?",
        "Old man: No.",
        "{STR_VAR_1} {STR_VAR_2} never caught on at all.",
        "Would you like to hear about it?",
        "MC: Er -- no. What we want is what's happening now...",
    )),
    "TrendWatcher_Text_MaleTaughtMePhrase": (("taught me as being trendy",), (
        "Old man: {STR_VAR_1} {STR_VAR_2} was what {STR_VAR_3} of VILA "
        "AMANHECER told me everyone was saying...",
    )),
    "TrendWatcher_Text_FemaleTaughtMePhrase": (("taught me as being trendy",), (
        "Old man: {STR_VAR_1} {STR_VAR_2} was what {STR_VAR_3} of VILA "
        "AMANHECER told me everyone was saying...",
    )),
    "TrendWatcher_Text_PhraseWasHopeless": (("utterly hopeless", "what's in now"), (
        "And it was hopeless. Utterly.",
        "{STR_VAR_1} {STR_VAR_2} festival!",
        "{STR_VAR_1} {STR_VAR_2} contest!",
        "I taught it to everyone I could, and still...",
        "Perhaps the {STR_VAR_1} part was simply wrong...",
        "MC: Er -- forgive me, my friend, but I need what's current...",
    )),
    "TrendWatcher_Text_MaleTellMeBigger": (("something bigger",), (
        "Old man: {STR_VAR_3}!|Please -- tell me something bigger than that "
        "{STR_VAR_1} {STR_VAR_2}!",
    )),
    "TrendWatcher_Text_FemaleTellMeBigger": (("something bigger",), (
        "Old man: {STR_VAR_3}!|Please -- tell me something bigger than that "
        "{STR_VAR_1} {STR_VAR_2}!",
    )),
    "TrendWatcher_Text_Outro": (("there you have it", "Catch you"), (
        "MC: ...Er... Well. There you have it, everybody.",
        "{STR_VAR_1} {STR_VAR_2}... er... never did catch on in PORTO DAS "
        "REDES.",
        "That's my time. Catch you next week!",
        "Old man: {STR_VAR_1} {STR_VAR_2}!",
    )),

    # -- the letters about buried things --------------------------------------
    "gTVHoennTreasureInvestigatorsText00": (("TREASURE INVESTIGATORS", "letter"), (
        "ARAUNA TREASURE INVESTIGATORS!",
        "Hello, everyone!|Turned anything up lately?",
        "As ever, we go through what people have seen out there.",
        "We start with a letter.|It says: “{STR_VAR_1} discovered!”",
    )),
    "gTVHoennTreasureInvestigatorsText01": (("Dear INVESTIGATORS", "ITEMFINDERS"), (
        "Well, we had better read that one out. Here it is.",
        "...Dear INVESTIGATORS,|I hope this finds you well.",
        "I saw {STR_VAR_2} not long ago, somewhere around {STR_VAR_3}.",
        "And that TRAINER turned up {STR_VAR_1}. I was envious.",
        "...Well done indeed, {STR_VAR_2}!",
        "Viewers -- let that get your ITEMFINDERS out of the bag!",
        "I shall be waiting to hear what you find!",
    )),
    "gTVHoennTreasureInvestigatorsText02": (("on a ferry", "ITEMFINDERS"), (
        "Well, we had better read that one out. Here it is.",
        "...Dear INVESTIGATORS,|I hope this finds you well.",
        "I saw {STR_VAR_2} not long ago, aboard a ferry.",
        "And that TRAINER turned up {STR_VAR_1}. I was envious.",
        "...Well done indeed, {STR_VAR_2}!",
        "Viewers -- let that get your ITEMFINDERS out of the bag!",
        "I shall be waiting to hear what you find!",
    )),

    # -- the one about the game corner ----------------------------------------
    "gTVFindThatGamerText00": (("FIND THAT GAMER", "no. 1 gamer"), (
        "FIND THAT GAMER!",
        "Hello, players!|How is your {STR_VAR_2} turning tonight?",
        "As ever, we put the light on one uncommon TRAINER who has been in "
        "at the GAME CORNER.",
        "And tonight's finest is...|{STR_VAR_1}!",
    )),
    "gTVFindThatGamerText01": (("won a rare", "feel the excitement"), (
        "{STR_VAR_1} played the {STR_VAR_2} game and took {STR_VAR_3} COINS "
        "off it.",
        "“When {STR_VAR_1} walks in, we make sure the COINS are stocked.”",
        "That is what they say behind the counter when our player is at the "
        "machine!",
        "Viewers -- keep an eye on your COINS the way {STR_VAR_1} does, if you "
        "go in for the {STR_VAR_2} game.",
        "Live from the GAME CORNER, where you can feel it in the air!",
        "That's all for tonight!",
    )),
    "gTVFindThatGamerText02": (("lost", "sales seem to increase"), (
        "{STR_VAR_1} played the {STR_VAR_2} game and dropped {STR_VAR_3} "
        "COINS on it.",
        "“When {STR_VAR_1} walks in, our COIN sales go up.”",
        "That is what they say behind the counter when our player is at the "
        "machine!",
    )),
    "gTVFindThatGamerText03": (("watch your COINS", "That's all for today"), (
        "Viewers -- keep an eye on your COINS the way {STR_VAR_1} does, if you "
        "go in for the {STR_VAR_2} game.",
        "Live from the GAME CORNER, where you can feel it in the air!",
        "That's all for tonight!",
    )),

    # -- the outside broadcast ------------------------------------------------
    "gTVBreakingNewsText00": (("BREAKING NEWS",), (
        "BREAKING NEWS TV!",
    )),
    "gTVBreakingNewsText01": (("Rare", "We're live"), (
        "Rare {STR_VAR_2} taken by {STR_VAR_1}!",
        "We are live, near {STR_VAR_3}!",
        "It was here that {STR_VAR_1} caught a rare {STR_VAR_2} this very "
        "day!",
    )),
    "gTVBreakingNewsText02": (("encountered the rare", "sent out"), (
        "On meeting the rare {STR_VAR_2}, {STR_VAR_1} sent out the POKéMON "
        "{STR_VAR_3}.",
    )),
    "gTVBreakingNewsText03": (("BALLS thrown", "used last"), (
        "Over the course of it, the TRAINER threw {STR_VAR_1} POKé BALLS.",
        "And in the end the rare POKéMON was taken by the last {STR_VAR_2}.",
    )),
    "gTVBreakingNewsText04": (("echoed with", "envious"), (
        "In that moment, {STR_VAR_2} rang with {STR_VAR_1}'s shouting.",
        "And I will admit to envy. I should like to shout like that.",
        "...That is the end of our broadcast from a happy place!",
    )),
    "gTVBreakingNewsText05": (("fails to capture", "We're live"), (
        "{STR_VAR_1} loses a rare {STR_VAR_2}!",
        "We are live, near {STR_VAR_3}!",
        "It was here that {STR_VAR_1} failed to take a rare {STR_VAR_2}!",
    )),
    "gTVBreakingNewsText06": (("encountered the rare", "sent out"), (
        "On meeting the rare {STR_VAR_2}, {STR_VAR_1} sent out the POKéMON "
        "{STR_VAR_3}.",
    )),
    "gTVBreakingNewsText07": (("use the move", "faint"), (
        "The TRAINER had the {STR_VAR_2} use {STR_VAR_1}.",
        "And meaning nothing of the kind, knocked the rare POKéMON out...",
    )),
    "gTVBreakingNewsText08": (("shrieks of", "frustration"), (
        "In that moment, {STR_VAR_2} rang with {STR_VAR_1}'s howling...",
    )),
    "gTVBreakingNewsText09": (("run\\n", "out of POKé BALLS"), (
        "But {STR_VAR_1} appears to have run out of POKé BALLS.",
        "The TRAINER had to leave the rare {STR_VAR_2} where it stood.",
        "In that moment, {STR_VAR_3} rang with {STR_VAR_1}'s howling...",
    )),
    "gTVBreakingNewsText10": (("fled without", "warning"), (
        "But the {STR_VAR_2} turned and went, with no warning at all.",
        "In that moment, {STR_VAR_3} rang with {STR_VAR_1}'s howling...",
    )),
    "gTVBreakingNewsText11": (("feel for", "melancholy scene"), (
        "I will admit to feeling for {STR_VAR_1}. It makes me want to howl "
        "myself.",
        "...That is the end of our broadcast from a sorry place!",
    )),
    "gTVBreakingNewsText12": (("panicked", "faint"), (
        "But {STR_VAR_1} lost their head at the sight of the rare "
        "{STR_VAR_2}.",
        "And in the confusion, told {STR_VAR_3} to attack.",
        "And meaning nothing of the kind, knocked the rare POKéMON out.",
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
        masked = masked[:start] + '\t.string "<ARAUNA_TV_BREAKING_NEWS_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
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

    composed = payloads()

    # Names this region gave itself, which the broadcast is not free to undo.
    owned = {
        "gTVHoennTreasureInvestigatorsText00": "ARAUNA TREASURE INVESTIGATORS",
        "gTVTodaysRivalTrainerText03": "BATTLE CIRCUIT",
        "gTVTodaysRivalTrainerText04": "BATTLE CIRCUIT",
        "gTVTodaysRivalTrainerText05": "BATTLE CIRCUIT",
    }
    for label, name in owned.items():
        flat = re.sub(r"\\[npl]", " ", "".join(composed[label]))
        if name not in flat:
            raise ValueError(f"{label}: lost the name this region gave it: {name}")

    # The trend watcher's phrase is two slots read as one saying, and it is
    # said eight times across the show. It must stay two words, in order.
    phrase = re.compile(r"\{STR_VAR_1\}\s*(?:\\[npl])?\s*\{STR_VAR_2\}")
    for label in TARGETS:
        if not label.startswith("TrendWatcher_"):
            continue
        joined = "".join(composed[label])
        if "{STR_VAR_1}" in joined and not phrase.search(joined):
            raise ValueError(f"{label}: the catchphrase came apart")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render BREAKING NEWS, the rival bulletin and the trend watcher.")
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
    print(f"TV Breaking News English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

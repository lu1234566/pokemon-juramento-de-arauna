#!/usr/bin/env python3
"""The three women who sit in the BAIA DAS LUZES POKéMON CENTER.

They share a room and nothing else. One collects objects of a quality she
happens to be fixed on this week, one runs a quiz and will keep your prize if
you fail it, and one wants a POKéBLOCK for a POKéMON she is convinced is
about to be a CONTEST winner. Each is written to sound like nobody else in
the room, since a player meets all three in the same two square metres.

The slots are the reason this file is delicate. Almost every line is
assembled at runtime out of an adjective the engine picked ("slippery",
"roundish"), an item name, a person's name, or a CONTEST quality, and the
sentence has to still parse whichever one lands in it. The renderer refuses
any slot the engine does not fill in that particular block, and checks that
the three lines a player must be able to act on -- the quiz's warning that a
wrong answer loses the prize, the refusal for a full BAG, and the refusal for
a missing {POKEBLOCK} CASE -- still say so.

The five cry lines at the end are left alone. They are the noise a species
makes, not something anybody says.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SOURCE = ROOT / "data" / "scripts" / "lilycove_lady.inc"
PREFIX = "LilycoveCity_PokemonCenter_1F_Text_"

# {STR_VAR_1} can be an item name, a person's name or an adjective, so it is
# budgeted at the longest of those; {POKEBLOCK} is a fixed glyph.
BOX = TextBox({"{STR_VAR_1}": 12, "{STR_VAR_2}": 12, "{STR_VAR_3}": 10,
               "{POKEBLOCK}": 9}, width=34)

WHOLE = ("FAVOR LADY", "QUIZ LADY", "CONTEST LADY", "{POKEBLOCK} CASE",
         "CONTESTS", "BAG")

FAVOR: dict[str, tuple[str, ...]] = {
    "ImTheFavorLady": (
        "I am the FAVOR LADY...",
    ),
    "ObsessedWithThing": (
        "Lately I have not been able to stop thinking about things that are "
        "{STR_VAR_1}...",
    ),
    "ThankYouForLastTime": (
        "Oh...|Thank you for the last one...",
    ),
    "PlayerGaveMeBadThing": (
        "There was somebody before. {STR_VAR_3}, I think it was...",
        "{STR_VAR_3} gave me one {STR_VAR_2} and told me it was "
        "{STR_VAR_1}.",
        "It was not {STR_VAR_1}.|Not in the smallest degree.",
    ),
    "PlayerGaveMeGreatThing": (
        "There was somebody before. {STR_VAR_3} gave me a {STR_VAR_2} that "
        "was very {STR_VAR_1}.",
        "I have kept it close ever since.",
    ),
    "WillYouShareThing": (
        "Listen. If you are carrying anything at all that is {STR_VAR_1}, "
        "would you let me have it?",
    ),
    "WhatWillYouGiveMe": (
        "...Truly?|And what will you give me?",
    ),
    "IsThatSoGoodbye": (
        "Is that so?|Then it is good-bye...",
    ),
    "NotWillingToShare": (
        "Oh...|You would rather keep it?",
    ),
    "IllTryToCherishIt": (
        "Oh?|That {STR_VAR_2} is {STR_VAR_1}?",
        "...Is it. Is it really.",
        "Well. I owe you thanks all the same.|I shall try to keep it close...",
    ),
    "IWillCherishThis": (
        "Oh...",
        "That is a quite {STR_VAR_1} {STR_VAR_2}...",
        "Is it not lovely?|It is like something out of a dream...",
        "Thank you...|I shall keep this close...",
    ),
    "IWillTreasureThis": (
        "...Oh. Oh. Oh...",
        "But this is extraordinary!|This truly is {STR_VAR_1}!",
        "I never knew a single {STR_VAR_2} could be this {STR_VAR_1}!",
        "Thank you!",
        "I shall treasure this for the rest of my life!",
    ),
    "IllGiveYouThisInReturn": (
        "For a gift like that you must have something in return. Take this.",
        "I hope you will keep it close...",
    ),
    "YouDontHaveSpaceForIt": (
        "Oh -- you cannot take it. There is no room in your BAG.",
        "Come and see me once you have made some space...",
    ),
}

QUIZ: dict[str, tuple[str, ...]] = {
    "ImTheQuizLady": (
        "I am the QUIZ LADY!|I do love a quiz!",
    ),
    "WaitingToTakeYourQuiz": (
        "Oh?",
        "I am still waiting for somebody to come and answer the quiz you "
        "wrote.",
        "We shall talk another time, all right?",
    ),
    "WaitingForChallenger": (
        "I am waiting for somebody brave enough to take on the quiz "
        "{STR_VAR_1} thought up!",
    ),
    "TakeQuizChallenge": (
        "Answer it correctly and the prize is yours!",
        "Would you like to take the quiz challenge?",
    ),
    "WaitForAnswer": (
        "... ... ... ... ... ...|... ... ... ... ... ...",
    ),
    "HowBoringBye": (
        "Oh, how dull of you!|Bye-bye!",
    ),
    "YoureGoingToQuit": (
        "Awww!|You are giving up?",
    ),
    "TakeTheQuizAnotherTime": (
        "Do come and take the quiz challenge another time!",
    ),
    "YouGotItRight": (
        "Astonishing! You have got it right!",
        "You are a sharp one, you are!",
    ),
    "YouGotItRightYouveWonPersonsPrize": (
        "Congratulations!|You have got the quiz right!",
        "The prize {STR_VAR_1} put up is yours!",
    ),
    "XReceivedOneY": (
        "{STR_VAR_1} received one {STR_VAR_2}!",
    ),
    "YourBagIsFilledUp": (
        "Oh? Your BAG is full to the brim!",
        "Come and see me when you have room.",
    ),
    "WrongTheCorrectAnswerIs": (
        "Hmm... wrong!|The answer was “{STR_VAR_3}”!",
    ),
    "IGetToKeepPrize": (
        "What a shame!",
        "That means the prize, the {STR_VAR_1}, stays with me!",
    ),
    "MakeYourOwnQuiz": (
        "Listen, listen!|Would you like to write a quiz of your own?",
    ),
    "MaybeNextTime": (
        "Oh, I see...|Another time, then!",
    ),
    "PickYourPrize": (
        "The first thing you do is choose the prize for whoever answers your "
        "quiz correctly.",
        "But be warned. If nobody can answer it, the prize stays with me!",
    ),
    "QuitChoosingPrize": (
        "Without a prize there is no quiz.",
        "Are you giving up on writing one?",
    ),
    "WriteYourQuiz": (
        "Oh, how nice!|That is a splendid prize!",
        "Now you need the question, and the answer to go with it.",
    ),
    "QuitWritingQuizQuestion": (
        "Are you giving up on writing your question?",
    ),
    "QuitWritingQuizAnswer": (
        "Are you giving up on choosing your answer?",
    ),
    "IllLookForAChallenger": (
        "Thank you!|That is a fine quiz you have put together.",
        "I shall go and find somebody to take it on this instant.",
    ),
}

CONTEST: dict[str, tuple[str, ...]] = {
    "ImTheContestLady": (
        "I am the CONTEST LADY!|I do love a CONTEST!",
    ),
    "ThankForPokeblock": (
        "Thank you for that {POKEBLOCK} before!",
    ),
    "MyFriendDisplaysQuality": (
        "This is my friend {STR_VAR_1}!|The very picture of {STR_VAR_2}!",
        "And there is more {STR_VAR_2} in there yet, I am certain of it!",
    ),
    "DontHaveAPokeblockCase": (
        "So I need your help!",
        "Might I have one {POKEBLOCK}?|One is all I am asking for!",
        "...Oh. But...|You have no {POKEBLOCK} CASE.|That will not do. "
        "Another time, then!",
    ),
    "AskingForOnePokeblock": (
        "So I need your help!",
        "Might I have one {POKEBLOCK}?|One is all I am asking for!",
    ),
    "ICantHaveOnePokeblock": (
        "Awww!|Not even one {POKEBLOCK}?!",
    ),
    "WhatACheapskate": (
        "Well!|What a miser you are!",
    ),
    "IllUseYourPokeblock": (
        "Yay!|Thank you!",
        "I shall give my POKéMON your {POKEBLOCK} at once.",
    ),
    "NoChangeThanks": (
        "...It does not seem to have changed in the slightest...",
        "Hmm...",
        "Oh, never mind!|Thank you all the same!",
    ),
    "ReallyImprovedThanks": (
        "Oh, yay!|Look how pleased it is!",
        "And I do think that has brought on {STR_VAR_1}'s {STR_VAR_2} as "
        "well.",
        "Thank you so very much!",
    ),
    "ReadyToEnterContests": (
        "Hmm...",
        "I rather think the two of us are ready for some CONTESTS.",
        "If you see us at one, I hope you will cheer.",
    ),
}

TARGETS: dict[str, tuple[str, ...]] = {**FAVOR, **QUIZ, **CONTEST}

# The five cry lines are deliberately not here. "{STR_VAR_1}: Pikka!" is the
# sound the animal makes; there is no voice in it to rewrite.


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
        masked = masked[:start] + '\t.string "<ARAUNA_LILYCOVE_LADIES_EN>"\n\n' + masked[end:]
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
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip()

    # Three women in one room. Each has to name herself once, or a player who
    # walks between them has no idea which of the three they just spoke to.
    for label, title in (("ImTheFavorLady", "FAVOR LADY"),
                         ("ImTheQuizLady", "QUIZ LADY"),
                         ("ImTheContestLady", "CONTEST LADY")):
        if title not in flat(label):
            raise ValueError(f"{label}: no longer names the {title}")

    # The quiz costs something. A player who writes one and is never told
    # the prize can be lost has been misled by omission.
    warning = flat("PickYourPrize").lower()
    if "prize" not in warning or "stays with me" not in warning:
        raise ValueError(
            "PickYourPrize: no longer warns that an unanswered quiz costs the "
            "player the prize")

    # Two refusals a player has to be able to act on.
    if "BAG" not in flat("YourBagIsFilledUp"):
        raise ValueError("YourBagIsFilledUp: no longer says the BAG is full")
    if "{POKEBLOCK}" not in flat("DontHaveAPokeblockCase"):
        raise ValueError(
            "DontHaveAPokeblockCase: no longer says what is missing")

    # The favor lady's whole exchange turns on the adjective the engine
    # picked. Every line that is about the object has to carry it.
    for label in ("ObsessedWithThing", "WillYouShareThing",
                  "PlayerGaveMeBadThing", "PlayerGaveMeGreatThing",
                  "IWillCherishThis", "IWillTreasureThis"):
        if "{STR_VAR_1}" not in flat(label):
            raise ValueError(
                f"{label}: dropped the quality the FAVOR LADY is fixed on, "
                f"which is the only thing telling the player what to bring")

    # Three voices, and nothing but the words to tell them apart.
    for name, group in (("favor", FAVOR), ("quiz", QUIZ), ("contest", CONTEST)):
        said = [flat(label) for label in group]
        if len(set(said)) != len(said):
            raise ValueError(f"the {name} lady repeats herself word for word")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the three BAIA DAS LUZES ladies in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = SOURCE.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        SOURCE.write_text(rendered, encoding="utf-8")
    print(f"Lilycove ladies English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

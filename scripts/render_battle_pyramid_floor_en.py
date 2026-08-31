#!/usr/bin/env python3
"""The hints the PYRAMID gives you for beating somebody on a floor.

A hundred and twenty-six blocks, and every one of them is a count. Where the
exit is -- four directions, six people who might tell you. How many items are
still lying about -- nine answers, six people. How many TRAINERS are left --
eight answers, six people.

Which makes a hundred and twenty-six hand-written near-copies of eighteen
sentences, and the number is the only part that matters. Get one wrong and a
player searches a floor for an item that was never there. So the eighteen
speakers are written once and the counts are filled in, including the
awkward ones: one item is not "one items", and none of them is not a number
at all.

The arrows are engine glyphs, not words. {UP_ARROW} draws an arrow and
nothing else, so a hint that loses it points nowhere; the renderer checks
every one of the twenty-four still has its direction.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

FLOOR = (ROOT / "data" / "maps" / "BattleFrontier_BattlePyramidFloor"
         / "scripts.inc")
PREFIX = "BattlePyramid_Text_"

# The arrows are single glyphs; nothing else here takes a slot.
BOX = TextBox({"{UP_ARROW}": 1, "{DOWN_ARROW}": 1,
               "{LEFT_ARROW}": 1, "{RIGHT_ARROW}": 1}, width=34)

DIRECTIONS = ("Up", "Down", "Left", "Right")
COUNTS = ("Eight", "Seven", "Six", "Five", "Four", "Three", "Two", "One", "Zero")
WORDS = {"Eight": "eight", "Seven": "seven", "Six": "six", "Five": "five",
         "Four": "four", "Three": "three", "Two": "two"}

# Six ways of pointing at the exit. {arrow} is the glyph for the direction.
EXITS: tuple[str, ...] = (
    "This floor's exit is that way: {arrow}",
    "The exit on this floor lies {arrow}.",
    "The exit is over that {arrow} way.",
    "On this floor the exit is somewhere {arrow}.",
    "The exit?|It's {arrow} of here.",
    "The exit happens to lie {arrow}.",
)

# Six people who will tell you how many items are left. Each is an opening
# remark, then the sentence for several, for one, and for none.
ITEMS: tuple[tuple[str | None, str, str, str], ...] = (
    ("Looking for things?",
     "There are {n} left to be found.",
     "There is one left to be found.",
     "There's nothing left to be found."),
    ("You won, so I'll tell you something.",
     "There are {n} lying about up here.",
     "There is one lying about up here.",
     "There's nothing lying about up here."),
    ("How are you off for supplies?",
     "I reckon there are {n} still on this floor.",
     "I reckon there's one still on this floor.",
     "I reckon there's nothing left on this floor. Take care, now."),
    ("You're strong, so you've earned a hint.",
     "There appear to be {n} more on the ground.",
     "There appears to be one more on the ground.",
     "There appear to be none left on the ground."),
    (None,
     "On this floor of the PYRAMID, I hear there are {n}...",
     "On this floor of the PYRAMID, I hear there is one...",
     "On this floor of the PYRAMID, I hear there is nothing..."),
    ("Have you been picking things up?",
     "I believe there are {n} more on this floor.",
     "I believe there is one more on this floor.",
     "I believe there are none left on this floor."),
)

# Six people who will tell you how many TRAINERS are left.
TRAINERS: tuple[tuple[str | None, str, str, str], ...] = (
    ("You were something!",
     "But there are {n} more hard TRAINERS up here besides me!",
     "But there's one hard TRAINER up here besides me!",
     "And there's nobody left up here who can beat you!"),
    ("This is too upsetting!",
     "But there are {n} TRAINERS left! One of them will humble you!",
     "But there's one TRAINER left! That one will humble you!",
     "But there's nobody left who can take you on!"),
    ("That was impressive.",
     "But there are {n} more TRAINERS on this floor. Can you have them all?",
     "But there's one more TRAINER on this floor. Can you manage it?",
     "And you've gone through every TRAINER on this floor."),
    (None,
     "You might sweep the {n} TRAINERS left on this floor.",
     "You might finish the sweep with the one TRAINER left on this floor.",
     "There isn't a single person left here who could beat you..."),
    (None,
     "You may have what it takes to beat the {n} who remain.",
     "You may have what it takes to beat the one who remains.",
     "Your skill is past arguing with. Nobody here has a chance against "
     "you."),
    (None,
     "Can you keep winning against the {n} remaining TRAINERS?",
     "Can you keep winning against the last one?",
     "There aren't any TRAINERS left who can take you on now..."),
)


def sentences(speaker: tuple[str | None, str, str, str], count: str,
              noun: str) -> tuple[str, ...]:
    opener, many, one, none = speaker
    if count == "Zero":
        body = none
    elif count == "One":
        body = one
    else:
        body = many.format(n=f"{WORDS[count]} {noun}")
    return ((opener, body) if opener else (body,))


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = {}
    for index, phrasing in enumerate(EXITS, start=1):
        for direction in DIRECTIONS:
            arrow = f"{{{direction.upper()}_ARROW}}"
            blocks[f"ExitHint{direction}{index}"] = (
                phrasing.replace("{arrow}", arrow),)
    for index, speaker in enumerate(ITEMS, start=1):
        for count in COUNTS:
            name = "OneItem" if count == "One" else f"{count}Items"
            blocks[f"{name}Remaining{index}"] = sentences(speaker, count, "items")
    for index, speaker in enumerate(TRAINERS, start=1):
        for count in COUNTS[1:]:  # a floor holds seven TRAINERS, not eight
            blocks[f"{count}TrainersRemaining{index}"] = sentences(
                speaker, count, "TRAINERS")
    return blocks


PARAGRAPHS = build()
TARGETS = tuple(PARAGRAPHS)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(PREFIX + label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    return {label: BOX.compose(
                tuple(p.replace("BATTLE PYRAMID", glued("BATTLE PYRAMID"))
                      for p in paragraphs))
            for label, paragraphs in PARAGRAPHS.items()}


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
        masked = masked[:start] + '\t.string "<ARAUNA_PYRAMID_FLOOR_EN>"\n\n' + masked[end:]
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

    # An arrow is a glyph, not a word. A hint that lost it points nowhere.
    for index in range(1, len(EXITS) + 1):
        for direction in DIRECTIONS:
            label = f"ExitHint{direction}{index}"
            arrow = f"{{{direction.upper()}_ARROW}}"
            if arrow not in flat(label):
                raise ValueError(f"{label}: lost its {arrow}")

    # The count is the only part of these that a player uses. Every one has
    # to state its own, and none may claim a different number.
    for index in range(1, len(ITEMS) + 1):
        for count in COUNTS:
            if count in ("One", "Zero"):
                continue
            name = f"{count}Items"
            text = flat(f"{name}Remaining{index}")
            if WORDS[count] not in text:
                raise ValueError(f"{name}Remaining{index}: no longer says "
                                 f"{WORDS[count]}")
            for other, word in WORDS.items():
                if other != count and re.search(rf"\b{word}\b", text):
                    raise ValueError(
                        f"{name}Remaining{index}: also says {word}, which is "
                        f"a different number of items")

    # Singular and none are the two the templates get wrong, so they are
    # checked for what they must not say.
    for family, total in (("Items", len(ITEMS)), ("Trainers", len(TRAINERS))):
        for index in range(1, total + 1):
            singular = "OneItem" if family == "Items" else "OneTrainers"
            text = flat(f"{singular}Remaining{index}")
            if re.search(rf"\bone (?:items|TRAINERS)\b", text):
                raise ValueError(
                    f"{singular}Remaining{index}: says 'one' with a plural")
            none = flat(f"Zero{family}Remaining{index}")
            if re.search(r"\b(?:zero|0)\b", none):
                raise ValueError(
                    f"Zero{family}Remaining{index}: counts nothing as a number")

    # Six speakers, and no two of them may say a thing the same way, or the
    # floor has fewer voices on it than it appears to.
    for family, total in (("Items", len(ITEMS)), ("Trainers", len(TRAINERS))):
        first = "Eight" if family == "Items" else "Seven"
        said = [flat(f"{first}{family}Remaining{index}")
                for index in range(1, total + 1)]
        if len(set(said)) != len(said):
            raise ValueError(f"two of the {family.lower()} speakers say the same thing")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BATTLE PYRAMID floor hints in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = FLOOR.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        FLOOR.write_text(rendered, encoding="utf-8")
    print(f"Battle Pyramid floor English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

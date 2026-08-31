#!/usr/bin/env python3
"""The people who will spin a BERRY BLENDER with you.

Three of them stand in POKéMON CENTERS across ARAUNA -- an old-timer alone,
a cheerful pair, and a lady who says "oh, dear" at everything -- and the
engine gives each the same six texts: do you know how, then let us start,
then the explanation, then one refusal each for no BERRIES, a full
{POKEBLOCK} CASE and no CASE at all.

Six shapes written out three times by hand is where a rules text goes wrong:
one of the three ends up explaining the A Button and the other two do not,
and which explanation a player gets depends on which POKéMON CENTER they
happened to walk into. So the three are composed from one table here, and
the renderer checks that all three explanations still name the A Button and
the marker, and that all three of each refusal still say what is missing.

What differs between them is manner, which is the only thing that should.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SOURCE = ROOT / "data" / "scripts" / "berry_blender.inc"
PREFIX = "BerryBlender_Text_"

BOX = TextBox({"{POKEBLOCK}": 9, "{STR_VAR_1}": 8, "{STR_VAR_2}": 8,
               "{STR_VAR_3}": 8}, width=34)

WHOLE = ("BERRY BLENDER", "{POKEBLOCK} CASE", "A Button", "B Button")

# The three hosts, keyed by the suffix the engine gives their labels.
SHAPES = ("KnowHowToMakePokeblocks", "LetsBerryBlender",
          "ExplainBerryBlending", "DontHaveAnyBerries",
          "PokeblockCaseIsFull", "DontHavePokeblockCase")

HOSTS: dict[str, dict[str, tuple[str, ...]]] = {
    "": {  # the old-timer, slow and kindly
        "KnowHowToMakePokeblocks": (
            "Do you know how a {POKEBLOCK} is made?",
        ),
        "LetsBerryBlender": (
            "Then let us begin!",
            "Let us BERRY BLENDER!",
        ),
        "ExplainBerryBlending": (
            "A word of explanation, then.",
            "Do not fret. There is very little to it.",
            "When the BLENDER's arrow comes round to your marker, press the "
            "A Button.",
            "That is the whole of it. You will see how easy once you have "
            "done it once.",
        ),
        "DontHaveAnyBerries": (
            "Oh?|You have no BERRIES at all?",
            "Without BERRIES there is nothing to blend, and no {POKEBLOCK}S "
            "to be had.",
        ),
        "PokeblockCaseIsFull": (
            "But your {POKEBLOCK} CASE is full.",
            "Use a few of them up and come and see me again.",
        ),
        "DontHavePokeblockCase": (
            "But you have no {POKEBLOCK} CASE.",
            "Get yourself one and then come and see me.",
        ),
    },
    "2": {  # the pair, brisk and friendly
        "KnowHowToMakePokeblocks": (
            "You do know how to blend a {POKEBLOCK}, though? Of course you "
            "do.",
        ),
        "LetsBerryBlender": (
            "Right, off we go!",
            "Let us BERRY BLENDER!",
        ),
        "ExplainBerryBlending": (
            "Right!|Here is how it goes!",
            "The BLENDER's arrow comes spinning round. The moment it reaches "
            "your marker, press the A Button.",
            "That is all there is to it.|Easy, is it not?",
        ),
        "DontHaveAnyBerries": (
            "Oh, hold on a moment...|You have no BERRIES.",
            "No BERRIES, no {POKEBLOCK}S. That is the long and the short of "
            "it...",
            "We are always here. Come back with a BERRY or two and we will "
            "blend.",
        ),
        "PokeblockCaseIsFull": (
            "Oh, hold on a moment...|Your {POKEBLOCK} CASE is full.",
            "Use a few of them up and come back to us.",
        ),
        "DontHavePokeblockCase": (
            "Oh, hold on a moment...|You have no {POKEBLOCK} CASE.",
            "Go and get one, then come back to us.",
        ),
    },
    "3": {  # the lady who is startled by everything
        "KnowHowToMakePokeblocks": (
            "Naturally you know how {POKEBLOCK}S are made, dear?",
        ),
        "LetsBerryBlender": (
            "Very good, dear!|Let us begin!",
            "Let us BERRY BLENDER!",
        ),
        "ExplainBerryBlending": (
            "Oh, dear!",
            "Then I shall explain it to you properly.",
            "The BLENDER's arrow spins round to your marker. When it gets "
            "there, press the A Button.",
            "That is all it takes.|Simple, is it not?",
        ),
        "DontHaveAnyBerries": (
            "You have not a single BERRY on you, dear?",
            "And without BERRIES there are no {POKEBLOCK}S to be made.",
            "We shall be blending here for as long as you like. Come back "
            "with a BERRY and we shall do it together.",
        ),
        "PokeblockCaseIsFull": (
            "Your {POKEBLOCK} CASE is quite full, by the look of it.",
            "Use a few of them up and come back, dear.",
        ),
        "DontHavePokeblockCase": (
            "You have not got yourself a {POKEBLOCK} CASE yet, by the look "
            "of it.",
            "You will want one before you come back, dear.",
        ),
    },
}

HANDWRITTEN: dict[str, tuple[str, ...]] = {
    # -- the old-timer ------------------------------------------------------
    "WantToMakePokeblocks": (
        "Oh? Were you after making a few {POKEBLOCK}S with an old-timer?",
    ),
    "Excellent": (
        "Splendid!",
    ),
    "MadeOldTimerSad": (
        "Oh...|You have gone and made an old-timer sad...",
    ),
    "CanHaveOneOfMyBerries": (
        "Well now, that will not do at all, will it?",
        "If you do not mind them being leftovers, you may have one of mine.",
        "Then the two of us can make {POKEBLOCK}S on the BERRY BLENDER "
        "together.",
    ),
    "DontHaveAnyBerriesToSpare": (
        "If I had a BERRY going spare I would hand it over gladly...",
        "But I have none to spare today. Another time, then.",
    ),
    # -- the pair -----------------------------------------------------------
    "WantToBlendPokeblocksWithUs": (
        "Hello there! Were you after blending a few {POKEBLOCK}S with us?",
    ),
    "Okay": (
        "Right!",
    ),
    "ThatsTooBad": (
        "Oh, what a shame...",
        "Still -- we are always about, whenever the urge to blend takes you!",
    ),
    "LetsGetBlendingAlready": (
        "Come on, let us get blending!",
    ),
    "WhatKindOfPokeblockWillIGet": (
        "I do wonder what sort of {POKEBLOCK} I shall come out with.",
        "The waiting is the best part!",
    ),
    # -- the lady -----------------------------------------------------------
    "MakePokeblocksWithOurGroup": (
        "Oh, hello! Were you after making a few {POKEBLOCK}S with our little "
        "circle?",
    ),
    "OhDear": (
        "Oh, dear!",
    ),
    "LeftUsInShock": (
        "Oh, dear me...",
        "You have left us all quite shaken!",
    ),
    "SetNewBlenderRecord": (
        "Right! Today is the day I set a new BLENDER speed record!",
    ),
    "LookGoodAtBlendingJoinUs": (
        "Oh, dear!|You have the look of somebody good at blending.",
        "Would you care to join us?",
    ),
    "MakeDeliciousPokeblocks": (
        "I am going to make {POKEBLOCK}S so good my POKéMON comes out of it "
        "cuter.",
    ),
    "LoveMakingPokeblocks": (
        "I love making {POKEBLOCK}S.",
        "I never go anywhere without a BERRY or two on me.",
    ),
    "MakePokeblocksUsingBerryBlender": (
        "If you like, the two of us could make some {POKEBLOCK}S on the "
        "BERRY BLENDER.",
    ),
    "DontHaveAnyBerriesHaveOne": (
        "Oh?|You have no BERRIES at all?",
        "Well now, that will not do, will it?",
        "If you do not mind them being leftovers, you may have one of mine.",
    ),
    "UseItToMakePokeblocksTogether": (
        "We shall put it in the BERRY BLENDER and make {POKEBLOCK}S with it "
        "together.",
    ),
    "DontHaveAnyBerriesNoneToSpare": (
        "Oh?|You have no BERRIES at all?",
        "If I had one going spare I would hand it over gladly...",
        "But I have none to spare today. My apologies.",
    ),
    # -- the linked blend ---------------------------------------------------
    "SaveGameBeforeBerryBlenderLink": (
        "You and your friends will blend BERRIES into {POKEBLOCK}S on the "
        "BERRY BLENDER.",
        "The game must be saved before you link up. Is that all right?",
    ),
    "SearchingForFriends": (
        "Searching for your friends...|... ... B Button: Cancel",
    ),
    "Player1Arrived": (
        "{STR_VAR_1} arrived.",
    ),
    "Player1And2Arrived": (
        "{STR_VAR_1} and {STR_VAR_2} arrived.",
    ),
    "AllPlayersArrived": (
        "{STR_VAR_1}, {STR_VAR_2} and {STR_VAR_3} arrived.",
    ),
    "NoBerriesLink": (
        "You have no BERRIES.|The BERRY BLENDER cannot be used.",
    ),
    "PokeblockCaseIsFullLink": (
        "Your {POKEBLOCK} CASE is full.|The BERRY BLENDER cannot be used.",
    ),
    "DontHavePokeblockCaseLink": (
        "You have no {POKEBLOCK} CASE.|The BERRY BLENDER cannot be used.",
    ),
}


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = dict(HANDWRITTEN)
    for suffix, host in HOSTS.items():
        for shape in SHAPES:
            blocks[f"{shape}{suffix}"] = host[shape]
    return blocks


TARGETS: dict[str, tuple[str, ...]] = build()


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
        masked = masked[:start] + '\t.string "<ARAUNA_BERRY_BLENDER_EN>"\n\n' + masked[end:]
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

    for suffix in HOSTS:
        # Which of the three a player meets is an accident of which POKéMON
        # CENTER they walked into, so all three have to teach the same thing.
        explanation = flat(f"ExplainBerryBlending{suffix}")
        for required in ("A Button", "marker", "arrow"):
            if required not in explanation:
                raise ValueError(
                    f"ExplainBerryBlending{suffix}: no longer mentions the "
                    f"{required}, so this host teaches less than the others")
        # Three refusals, each naming what is actually missing.
        if "BERRIES" not in flat(f"DontHaveAnyBerries{suffix}"):
            raise ValueError(
                f"DontHaveAnyBerries{suffix}: no longer says BERRIES are "
                f"what is missing")
        full = flat(f"PokeblockCaseIsFull{suffix}")
        if "{POKEBLOCK} CASE" not in full or "full" not in full:
            raise ValueError(
                f"PokeblockCaseIsFull{suffix}: no longer says the CASE is full")
        if "{POKEBLOCK} CASE" not in flat(f"DontHavePokeblockCase{suffix}"):
            raise ValueError(
                f"DontHavePokeblockCase{suffix}: no longer says a CASE is "
                f"what is missing")

    # Manner is the only thing separating the three. If two of them say a
    # shape identically, one of them has stopped being a person.
    for shape in SHAPES:
        said = [flat(f"{shape}{suffix}") for suffix in HOSTS]
        if len(set(said)) != len(said):
            raise ValueError(f"two of the three hosts give an identical {shape}")

    # The three link refusals are the ones a player reads with three friends
    # waiting, so each has to say both what is wrong and that the session
    # cannot go ahead.
    for label in ("NoBerriesLink", "PokeblockCaseIsFullLink",
                  "DontHavePokeblockCaseLink"):
        if "BERRY BLENDER" not in flat(label):
            raise ValueError(
                f"{label}: no longer says the BERRY BLENDER cannot be used")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BERRY BLENDER hosts in English.")
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
    print(f"Berry blender English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

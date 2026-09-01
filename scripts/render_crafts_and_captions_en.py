#!/usr/bin/env python3
"""The glass workshop, the BLEND MASTER, and the captions on CONTEST paintings.

Three small surfaces that each turn something a player did into an object.

The workshop on ROUTE 113 trades volcanic ash for glassware, and everything
about that trade lives in this one room: that the SOOT SACK has to be carried
to collect anything, that ash is gathered by walking through it, and how many
steps short the player still is. All three are held, because a player who
leaves without them will walk the route with nothing in hand and no idea why.

The BLEND MASTER's refusals are the same three the ordinary blenders give --
no BERRIES, no {POKEBLOCK} CASE, a full one -- and he must still say which,
even while being magnificent about it.

The painting captions are fifteen boasts, three for each CONTEST category.
They are the trophy: a player who wins comes back to the hall to read one, so
each has to belong to the category it hangs under and none may repeat another.
Both are checked. The caption box is narrower than a message box -- vanilla
runs to 197px in it -- and that is the ceiling kept.

The twelve caption words (CONTEST, the four ranks, the five conditions, LINK)
are labels painted on the frame, not sentences, and are left in place.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402
from textwidth import Ruler  # noqa: E402

WORKSHOP = ROOT / "data" / "maps" / "Route113_GlassWorkshop" / "scripts.inc"
BLEND_MASTER = ROOT / "data" / "text" / "blend_master.inc"
PAINTING = ROOT / "data" / "text" / "contest_painting.inc"

BOX = TextBox({"{STR_VAR_1}": 12, "{STR_VAR_2}": 6, "{POKEBLOCK}": 9},
              width=34)
# The caption hangs on the painting, in a narrower frame than a message box.
CAPTION_BOX = TextBox({"{STR_VAR_1}": 10}, width=28)
CAPTION_CEILING = 197

WHOLE = ("SOOT SACK", "BLUE FLUTE", "BLEND MASTER", "{POKEBLOCK} CASE",
         "BERRY BLENDER", "A Button", "BAIA DAS LUZES", "POKéMON CENTER",
         "BAG")

CATEGORIES = ("Cool", "Beauty", "Cute", "Smart", "Tough")

# Three boasts per category. The words that make each one belong to its
# category are what the renderer holds.
CAPTIONS: dict[str, tuple[tuple[str, str], ...]] = {
    "Cool": (
        ("cool", "Cool without pause -- the inestimable {STR_VAR_1}"),
        ("Cool", "Well, hello there.|The coolest thing on four legs: "
                 "{STR_VAR_1}"),
        ("cool", "The marvellous, the wonderful, the impossibly cool "
                 "{STR_VAR_1}"),
    ),
    "Beauty": (
        ("beaut", "The last great beauty of the century -- {STR_VAR_1}"),
        ("beaut", "{STR_VAR_1}'s beautiful, glittering smile"),
        ("beaut", "The beauty they cannot stop talking about: {STR_VAR_1}"),
    ),
    "Cute": (
        ("cute", "The sweet and cuter-than-most {STR_VAR_1}"),
        ("cute", "The cute {STR_VAR_1}, caught mid-victory"),
        ("cute", "Give us a wink!|The cutest of them all, {STR_VAR_1}"),
    ),
    "Smart": (
        ("smart", "A maestro of smartness -- the clever {STR_VAR_1}"),
        ("smart", "{STR_VAR_1} -- the smartest in the room, and chosen for "
                  "it"),
        ("smart", "The smart {STR_VAR_1}, in a moment of pure elegance"),
    ),
    "Tough": (
        ("tough", "Tough, quick, and built like a wall: {STR_VAR_1}"),
        ("tough", "The tough, the tougher, and the toughest {STR_VAR_1}"),
        ("tough", "The mightily tough {STR_VAR_1}"),
    ),
}

WORKSHOP_BLOCKS: dict[str, tuple[str, ...]] = {
    "GoCollectAshWithThis": (
        "The whole of this country is under volcanic ash, huff-puff.",
        "And I have a gift for it, huff-puff.",
        "I make glass out of volcanic ash, and things out of the glass, "
        "huff-puff.",
        "Go and gather me some ash with this, huff-puff.",
    ),
    "ExplainSootSack": (
        "Take that SOOT SACK and walk through the piles of ash, huff-puff.",
        "It fills up as you go, huff-puff.",
        "When you think you have a decent amount, come and see me, "
        "huff-puff.",
    ),
    "LetsSeeCollectedAshes": (
        "Been gathering, have you, huff-puff?|Let me see, huff-puff.",
    ),
    "NotEnoughAshNeedX": (
        "Hmmm...|There is not enough here, huff-puff.|I cannot make glass "
        "from this, huff-puff.",
        "Let me see... {STR_VAR_1} more steps through the ash and I could "
        "make you a BLUE FLUTE, huff-puff.",
    ),
    "WhichGlassItemWoudYouLike": (
        "Oh!|That is a great deal of ash, huff-puff!",
        "I shall make you something in glass, huff-puff.|Which will you "
        "have, huff-puff?",
    ),
    "IsThatTheItemForYou": (
        "A {STR_VAR_1}, huff-puff?|Is that the one for you, huff-puff?",
    ),
    "WhichWouldYouLike": (
        "Which will you have, huff-puff?",
    ),
    "IllMakeItemForYou": (
        "A {STR_VAR_1} it is, huff-puff.",
        "Right. I shall make it, huff-puff.|Give me a little while, "
        "huff-puff.",
    ),
    "NotEnoughAshToMakeItem": (
        "A {STR_VAR_1}, huff-puff?",
        "There is not enough ash here for that one, huff-puff.",
        "Let me see... {STR_VAR_2} more steps through the volcanic ash and I "
        "could make it, huff-puff.",
        "What would you rather I made instead, huff-puff?",
    ),
    "AllThatAshButDontWantAnything": (
        "All that ash gathered and you want nothing at all, huff-puff?",
    ),
    "IveFinishedGlassItem": (
        "Ah -- your {STR_VAR_1} is finished.|Take it, huff-puff.",
    ),
    "NoRoomInBag": (
        "Oh?|There is no room in your BAG, huff-puff.",
        "I shall keep hold of it. Come back later, huff-puff.",
    ),
    "NoRoomInPC": (
        "Oh?|There is no room in your PC, huff-puff.",
        "I shall keep hold of it. Come back later, huff-puff.",
    ),
    "HaventGotYourSootSack": (
        "Hah? You have not got your SOOT SACK with you, huff-puff.",
        "You must keep it on you to gather any volcanic ash at all, "
        "huff-puff.",
    ),
    "FunToBlowGlassFlute": (
        "It is good fun blowing a glass flute while the boss is talking.",
        "Huff-huff! Puff-puff!",
    ),
}

BLEND_MASTER_BLOCKS: dict[str, tuple[str, ...]] = {
    "BlendWithTheBlendMaster": (
        "BLEND MASTER: Indeed I am!|The BLEND MASTER am I!",
        "Blend with me and you shall see what mastery looks like.",
    ),
    "SeeMyMasteryInAction": (
        "BLEND MASTER: Hmmm! So you wish to see that mastery for yourself?",
    ),
    "TooBusyNowIsee": (
        "Hmmm!",
        "So you are too busy for it just now, I see.",
        "But fear not.|I shall be here all day.|Hurry back from your "
        "errand.",
    ),
    "BlendMasterNoBerries": (
        "Hmmm!",
        "You have not a single BERRY on you.",
        "I shall be here all day.|Hurry back with some BERRIES.",
    ),
    "BlendMasterKnowHowToMakePokeblocks": (
        "Of course!|Of course!",
        "Incidentally...|You do know how a {POKEBLOCK} is blended out of "
        "BERRIES?",
    ),
    "BlendMasterExplainBerryBlending": (
        "Hmmm!",
        "Ah, but it is a simple business.",
        "When the BLENDER's arrow comes round to your marker, press the "
        "A Button.",
        "That is the whole of it.",
        "Watch the precision with which I press the A Button and you will "
        "understand.",
    ),
    "BlendMasterLetsBerryBlender": (
        "Good!",
        "Then let us begin.",
        "All together with the BLEND MASTER -- let us BERRY BLENDER!",
    ),
    "BlendMasterNoPokeblockCase": (
        "Hmmm!",
        "You appear not to have a {POKEBLOCK} CASE.",
        "I shall be here all day.|Get yourself one and hurry back.",
    ),
    "BlendMasterPokeblockCaseFull": (
        "Hmmm!",
        "Your {POKEBLOCK} CASE appears to be full.",
        "I shall be here all day.|Use a few of them and hurry back.",
    ),
    "WhoaAwesome": (
        "Whoa!|Astonishing!",
    ),
    "WickedlyFast": (
        "Wickedly fast!",
    ),
    "WhatAnExpert": (
        "What an expert!",
    ),
    "MadeAmazingPokeblocksWithMaster": (
        "When I blended alongside the MASTER we came out with quite "
        "remarkable {POKEBLOCK}S.",
    ),
    "QualitiesOfBlendMaster": (
        "Eyes that follow the arrow like a machine...",
        "A hand that taps the A Button like clockwork...",
        "Having both of those is what makes the BLEND MASTER great.",
    ),
    "MasterWorksOnSkillsInMountains": (
        "The BLEND MASTER is meant to be off working at his craft deep in "
        "the mountains.",
        "Now and then he comes down to BAIA DAS LUZES and blends BERRIES all "
        "day.",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    workshop = {f"Route113_GlassWorkshop_Text_{label}": body
                for label, body in WORKSHOP_BLOCKS.items()}
    master = {f"BerryBlender_Text_{label}": body
              for label, body in BLEND_MASTER_BLOCKS.items()}
    painting: dict[str, tuple[str, ...]] = {}
    for category, boasts in CAPTIONS.items():
        for index, (_word, caption) in enumerate(boasts, start=1):
            painting[f"gContestPainting{category}{index}"] = (caption,)
    return {"workshop": workshop, "master": master, "painting": painting}


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"workshop": WORKSHOP, "master": BLEND_MASTER, "painting": PAINTING}
CAPTION_LABELS = frozenset(GROUPS["painting"])


def which(label: str) -> str:
    for name, group in GROUPS.items():
        if label in group:
            return name
    raise KeyError(label)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)"
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
        box = CAPTION_BOX if label in CAPTION_LABELS else BOX
        composed[label] = box.compose(tuple(glued_paragraphs))
    return composed


def render(sources: dict[str, str]) -> dict[str, str]:
    composed = payloads()
    rendered = dict(sources)
    for label in TARGETS:
        group = which(label)
        matches = list(block_pattern(label).finditer(rendered[group]))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered[group] = rendered[group][:start] + new_body + rendered[group][end:]
    return rendered


def mask(texts: dict[str, str]) -> dict[str, str]:
    masked = dict(texts)
    for label in TARGETS:
        group = which(label)
        match = block_pattern(label).search(masked[group])
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked[group] = (masked[group][:start]
                         + '\t.string "<ARAUNA_CRAFTS_EN>"\n\n'
                         + masked[group][end:])
    return masked


def validate_slots(sources: dict[str, str]) -> None:
    composed = payloads()
    for label in TARGETS:
        body = block_pattern(label).search(sources[which(label)]).group("body")
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}", body))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(sources: dict[str, str], rendered: dict[str, str]) -> None:
    if mask(sources) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()
    ruler = Ruler()

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # Everything a player needs to work the ash trade is in this one room.
    if "SOOT SACK" not in flat("Route113_GlassWorkshop_Text_ExplainSootSack"):
        raise ValueError("ExplainSootSack: no longer names the SOOT SACK")
    if "walk" not in flat("Route113_GlassWorkshop_Text_ExplainSootSack"):
        raise ValueError(
            "ExplainSootSack: no longer says ash is gathered by walking "
            "through it, and nothing else in the game says so")
    if "SOOT SACK" not in flat("Route113_GlassWorkshop_Text_HaventGotYourSootSack"):
        raise ValueError(
            "HaventGotYourSootSack: no longer says what is missing")
    for label, slot in (("NotEnoughAshNeedX", "{STR_VAR_1}"),
                        ("NotEnoughAshToMakeItem", "{STR_VAR_2}")):
        if slot not in flat(f"Route113_GlassWorkshop_Text_{label}"):
            raise ValueError(
                f"{label}: dropped the step count, which is the only measure "
                f"of how far short the player is")

    # The MASTER is magnificent, and still has to say which thing is wrong.
    for label, wanted in (("BlendMasterNoBerries", "BERRIES"),
                          ("BlendMasterNoPokeblockCase", "{POKEBLOCK} CASE"),
                          ("BlendMasterPokeblockCaseFull", "full")):
        if wanted not in flat(f"BerryBlender_Text_{label}"):
            raise ValueError(f"{label}: no longer says what is in the way")
    explanation = flat("BerryBlender_Text_BlendMasterExplainBerryBlending")
    for required in ("A Button", "marker", "arrow"):
        if required not in explanation:
            raise ValueError(
                f"BlendMasterExplainBerryBlending: no longer mentions the "
                f"{required}, so he teaches less than the ordinary blenders")

    # Fifteen trophies. Each belongs to its category, and none repeats.
    captions = []
    for category, boasts in CAPTIONS.items():
        for index, (word, _caption) in enumerate(boasts, start=1):
            label = f"gContestPainting{category}{index}"
            text = flat(label)
            if word.lower() not in text.lower():
                raise ValueError(
                    f"{label}: no longer says anything about being "
                    f"{word}, so the caption does not belong to the "
                    f"{category.upper()} category it hangs under")
            if "{STR_VAR_1}" not in text:
                raise ValueError(
                    f"{label}: no longer names the POKéMON in the picture")
            captions.append(text)
    if len(set(captions)) != len(captions):
        raise ValueError("two painting captions read alike")

    # The frame is narrower than a message box.
    for label in CAPTION_LABELS:
        for payload in composed[label]:
            width = ruler.widest(payload)
            if width > CAPTION_CEILING:
                raise ValueError(
                    f"{label}: {width}px, past the {CAPTION_CEILING}px the "
                    f"painting's frame can show")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the glass workshop, BLEND MASTER and captions.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    sources = {name: path.read_text(encoding="utf-8")
               for name, path in FILES.items()}
    validate_slots(sources)
    rendered = render(sources)
    validate_rendered(sources, rendered)

    if args.in_place:
        for name, path in FILES.items():
            path.write_text(rendered[name], encoding="utf-8")
    print(f"Crafts and captions English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

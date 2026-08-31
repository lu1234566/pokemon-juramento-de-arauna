#!/usr/bin/env python3
"""SECRET BASE SECRETS, and WHAT'S NO. 1 IN ARAUNA TODAY.

SECRET BASE SECRETS is surveillance footage narrated live. A commentator
watches somebody else's visitor wander around a stranger's hideout, sit on the
furniture and burst the balloons, and calls it the way another man would call
a horse race. That is the joke, and it only works if the commentator never
drops the register -- so every one of these lines is breathless about
something trivial, and none of them ever admits it.

The furniture the visitor touches is named in capitals because those are
decorations the player can actually own, so each line has to keep the name of
the thing it is about; the renderer checks all twenty-four of them.

WHAT'S NO. 1 IN ARAUNA TODAY hands out a title nobody asked for, once a day,
for whatever the player did most of.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

TV = ROOT / "data" / "text" / "tv.inc"

BOX = TextBox({"{STR_VAR_1}": 14, "{STR_VAR_2}": 14, "{STR_VAR_3}": 14}, width=34)

# Every decoration the commentator names, and the block that names it.
FURNITURE = {
    "TVSecretBaseSecrets_Text_UsedGoldShield": "GOLD SHIELD",
    "TVSecretBaseSecrets_Text_UsedSilverShield": "SILVER SHIELD",
    "TVSecretBaseSecrets_Text_UsedGlassOrnament": "GLASS ORNAMENT",
    "TVSecretBaseSecrets_Text_UsedMudBall": "MUD BALL",
    "TVSecretBaseSecrets_Text_UsedNoteMat": "NOTE MAT",
    "TVSecretBaseSecrets_Text_UsedSpinMat": "SPIN MAT",
    "TVSecretBaseSecrets_Text_UsedSandOrnament": "SAND ORNAMENT",
    "TVSecretBaseSecrets_Text_UsedBrick": "BRICK",
    "TVSecretBaseSecrets_Text_UsedSolidBoard": "SOLID BOARD",
    "TVSecretBaseSecrets_Text_UsedFence": "FENCE",
    "TVSecretBaseSecrets_Text_UsedGlitterMat": "GLITTER MAT",
    "TVSecretBaseSecrets_Text_UsedTire": "TIRE",
    "TVSecretBaseSecrets_Text_UsedStand": "STAND",
    "TVSecretBaseSecrets_Text_BrokeDoor": "BREAKABLE DOOR",
    "TVSecretBaseSecrets_Text_UsedDoll": "DOLL",
    "TVSecretBaseSecrets_Text_UsedSlide": "SLIDE",
    "TVSecretBaseSecrets_Text_UsedSlideButDidntGoDown": "SLIDE",
    "TVSecretBaseSecrets_Text_UsedJumpMat": "JUMP MAT",
    "TVSecretBaseSecrets_Text_UsedTent": "TENT",
}

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- the title nobody asked for -------------------------------------------
    "gTVWhatsNo1InHoennTodayText00": (("NO. 1 IN ARAUNA", "none other"), (
        "WHAT'S NO. 1 IN ARAUNA TODAY?|Yes -- it is that time again!",
        "Hello, viewers. Are you giving it everything, whatever it is you do?",
        "Let us see who gave it the most today.",
        "Tonight's number one is none other than {STR_VAR_1}!",
    )),
    "gTVWhatsNo1InHoennTodayText01": (("SLOTS", "reels don't"), (
        "In one day, {STR_VAR_1} played the SLOTS at the GAME CORNER "
        "{STR_VAR_2} times.",
        "And was overheard muttering: “For me, the reels don't even turn...”",
        "Isn't that a thing to hear?",
    )),
    "gTVWhatsNo1InHoennTodayText02": (("ROULETTE", "balls decide"), (
        "In one day, {STR_VAR_1} played the ROULETTE at the GAME CORNER "
        "{STR_VAR_2} times.",
        "And was heard to shout: “Let the balls decide!”",
        "The eyes were steady and the face gave nothing away.",
    )),
    "gTVWhatsNo1InHoennTodayText03": (("battled", "anytime"), (
        "In one day, {STR_VAR_1} took on wild POKéMON {STR_VAR_2} times!",
        "Those POKéMON must be far beyond what they were.",
        "They look ready to battle anywhere, at any hour, on any excuse!",
    )),
    "gTVWhatsNo1InHoennTodayText04": (("BERRY BLENDER", "Poste"), (
        "In one day, {STR_VAR_1} turned the BERRY BLENDER {STR_VAR_2} times!",
        "And by the end, even {STR_VAR_1} had gone rather green.",
        "The TRAINER was seen tottering about like a Poste!",
    )),
    "gTVWhatsNo1InHoennTodayText05": (("planted", "soothe"), (
        "In one day, {STR_VAR_1} planted {STR_VAR_2} BERRIES!",
        "And came away filthy to the elbows for it.",
        "Where the TRAINER planted, flowers have come up past counting.",
        "They are said to settle the nerves of anyone who passes.",
    )),
    "gTVWhatsNo1InHoennTodayText06": (("picked", "trouble"), (
        "In one day, {STR_VAR_1} picked {STR_VAR_2} BERRIES!",
        "The BAG was so full of them afterwards that the TRAINER had trouble "
        "walking!",
    )),
    "gTVWhatsNo1InHoennTodayText07": (("Battle Points", "grinning"), (
        "In one day, {STR_VAR_1} took {STR_VAR_2} Battle Points!",
        "And was later seen unable to choose between spending them on "
        "something useful and something for the wall.",
        "Grinning the whole while, by all accounts.",
    )),
    "gTVWhatsNo1InHoennTodayText08": (("isn't that something", "no. 1"), (
        "Well, isn't that something!",
        "{STR_VAR_1}!|You are today's number one!",
        "Viewers -- take heart from {STR_VAR_1}!|Any one of you could be "
        "number one tomorrow!",
    )),

    # -- the surveillance programme -------------------------------------------
    "TVSecretBaseSecrets_Text_Intro": (("SECRET BASE SECRETS", "have a peek"), (
        "SECRET BASE SECRETS!",
        "What do TRAINERS get up to behind a closed SECRET BASE?",
        "Tonight we look in on {STR_VAR_1}'s.",
        "Oh? It seems {STR_VAR_2} has called round.",
        "Let's watch!",
        "What will {STR_VAR_2} do?",
    )),
    "TVSecretBaseSecrets_Text_WhatWillPlayerDoNext1": (("do next",), (
        "And now what will {STR_VAR_2} do?",
    )),
    "TVSecretBaseSecrets_Text_WhatWillPlayerDoNext2": (("what will",), (
        "And after that -- what will {STR_VAR_2} do?",
    )),
    "TVSecretBaseSecrets_Text_TookXStepsBeforeLeaving": (("steps", "leaving"), (
        "In the end, {STR_VAR_2} took {STR_VAR_3} steps about {STR_VAR_1}'s "
        "SECRET BASE before going.",
    )),
    "TVSecretBaseSecrets_Text_BaseFailedToInterestPlayer": (("failed to interest",), (
        "Hmm...",
        "It would appear {STR_VAR_1}'s SECRET BASE did nothing for "
        "{STR_VAR_2}...",
    )),
    "TVSecretBaseSecrets_Text_PlayerEnjoyedBase": (("enjoyed",), (
        "{STR_VAR_2} seems to have thoroughly enjoyed {STR_VAR_1}'s SECRET "
        "BASE.",
    )),
    "TVSecretBaseSecrets_Text_PlayerHugeFanOfBase": (("huge fan",), (
        "{STR_VAR_2} appears to have become a devoted admirer of "
        "{STR_VAR_1}'s SECRET BASE.",
    )),
    "TVSecretBaseSecrets_Text_Outro": (("check out", "Tune in next time"), (
        "Viewers may care to call on {STR_VAR_1}'s SECRET BASE themselves.",
        "Join us next time, when we look in on another!|Thank you for "
        "watching!",
    )),
    "TVSecretBaseSecrets_Text_StoppedMoving1": (("stopped", "unimpressive"), (
        "The visitor has stopped!",
        "The visitor is not moving at all!",
        "Was {STR_VAR_1}'s SECRET BASE as dull as that?",
    )),
    "TVSecretBaseSecrets_Text_StoppedMoving2": (("stopped", "fatigue"), (
        "The visitor has stopped!",
        "The visitor is not moving at all!",
        "Is it tiredness?|Has the visitor simply had enough?",
    )),
    "TVSecretBaseSecrets_Text_UsedChair": (("chair", "comfortable"), (
        "The visitor has sat down on a chair!|The visitor is seated!",
        "And look at that face!",
        "That must be a very good chair indeed!",
    )),
    "TVSecretBaseSecrets_Text_UsedBalloon": (("balloon", "startled"), (
        "The visitor has charged a balloon!",
        "It's gone!|Good heavens, it burst!",
        "The visitor looks thoroughly startled by the bang!",
    )),
    "TVSecretBaseSecrets_Text_UsedTent": (("TENT", "size"), (
        "The visitor has gone into a TENT!",
        "The visitor is running about in there!",
        "Oh, my -- the visitor is thoroughly enjoying it!",
        "The visitor seems surprised by how much room a TENT has!",
    )),
    "TVSecretBaseSecrets_Text_UsedPlant": (("potted plant", "mature taste"), (
        "The visitor is inspecting a potted plant!",
        "Rather grown-up taste, for a visitor!",
    )),
    "TVSecretBaseSecrets_Text_UsedGoldShield": (("GOLD SHIELD", "lit up"), (
        "The visitor is inspecting a GOLD SHIELD!",
        "You can see the eyes light up from here!",
    )),
    "TVSecretBaseSecrets_Text_UsedSilverShield": (("SILVER SHIELD", "wide-eyed"), (
        "The visitor is inspecting a SILVER SHIELD!",
        "The visitor has gone quite wide-eyed!",
    )),
    "TVSecretBaseSecrets_Text_UsedGlassOrnament": (("GLASS ORNAMENT", "fingerprints"), (
        "The visitor is inspecting a GLASS ORNAMENT!",
        "Oh, no.",
        "The visitor is touching it!",
        "It is covered in fingerprints...",
    )),
    "TVSecretBaseSecrets_Text_UsedTV": (("television", "big fan of TV"), (
        "The visitor is watching the television!",
        "There's a viewer after our own hearts!",
    )),
    "TVSecretBaseSecrets_Text_UsedMudBall": (("MUD BALL", "delighted"), (
        "The visitor has stamped on a MUD BALL!",
        "The visitor looks delighted with itself!",
    )),
    "TVSecretBaseSecrets_Text_UsedBag": (("rummaging", "commercial"), (
        "...Oh?",
        "The visitor is reaching into their own BAG and rummaging about!",
        "The visitor has brought out one {STR_VAR_2}!",
        "And look at that smile, holding up the {STR_VAR_2}!",
        "It's like an advertisement!",
    )),
    "TVSecretBaseSecrets_Text_UsedCushion": (("cushion",), (
        "The visitor takes hold of a cushion and...",
    )),
    "TVSecretBaseSecrets_Text_HitCushion": (("hitting", "stress"), (
        "...starts hitting it!",
        "Is something weighing on our visitor?",
    )),
    "TVSecretBaseSecrets_Text_HuggedCushion": (("hugs", "happy"), (
        "...holds it tight!",
        "Has something gone well for our visitor today?",
    )),
    "TVSecretBaseSecrets_Text_BattledWon": (("away match", "victory dance"), (
        "The visitor is talking with {STR_VAR_1}!",
        "It looks as though there is going to be a battle!",
        "And...",
        "It's the visitor!|A win away from home!",
        "And there is the dance!",
    )),
    "TVSecretBaseSecrets_Text_BattledLost": (("has lost", "dejected"), (
        "The visitor is talking with {STR_VAR_1}!",
        "It looks as though there is going to be a battle!",
        "And...",
        "It's {STR_VAR_1}!|The visitor is beaten!",
        "And there goes the head.",
    )),
    "TVSecretBaseSecrets_Text_DeclinedBattle": (("refused", "unappealing"), (
        "The visitor is talking with {STR_VAR_1}!",
        "It looks as though there is going to be a battle!",
        "And...",
        "No -- the visitor has declined!",
        "There is to be no battle after all!",
        "Did {STR_VAR_1} not look worth the trouble?",
    )),
    "TVSecretBaseSecrets_Text_UsedPoster": (("poster", "disturbing"), (
        "The visitor is staring hard at a poster!",
        "Does the poster meet with approval?",
        "...Though... there is something in that stare I don't care for.",
    )),
    "TVSecretBaseSecrets_Text_UsedNoteMat": (("NOTE MAT", "funny tune"), (
        "The visitor has stepped on a NOTE MAT!",
        "...Hmm...|The visitor has composed something peculiar!",
    )),
    "TVSecretBaseSecrets_Text_BattledDraw": (("draw", "disappointed"), (
        "The visitor is talking with {STR_VAR_1}!",
        "It looks as though there is going to be a battle!",
        "And...",
        "A draw!|Nothing settled at all!",
        "Neither of them looks pleased about it!",
    )),
    "TVSecretBaseSecrets_Text_UsedSpinMat": (("SPIN MAT", "tottering"), (
        "The visitor has stepped on a SPIN MAT!",
        "The visitor has gone quite dizzy!",
        "The visitor is tottering about!|Mind out!",
    )),
    "TVSecretBaseSecrets_Text_UsedSandOrnament": (("SAND ORNAMENT", "sheepish"), (
        "The visitor is reaching for a SAND ORNAMENT!",
        "Oh!",
        "It's gone!|It has fallen to pieces!",
        "And the visitor looks thoroughly guilty about it!",
    )),
    "TVSecretBaseSecrets_Text_UsedDesk": (("desktop", "neatness"), (
        "The visitor is running a finger along a desktop!",
        "The visitor does not approve of dust!",
        "A surprisingly particular visitor, this one!",
    )),
    "TVSecretBaseSecrets_Text_UsedBrick": (("BRICK", "thinking about"), (
        "The visitor is staring at a BRICK!",
        "Perhaps the visitor is thinking about whatever is standing on it.",
    )),
    "TVSecretBaseSecrets_Text_UsedSolidBoard": (("SOLID BOARD", "timid"), (
        "The visitor is walking across the SOLID BOARD.",
        "The visitor keeps looking down.",
        "A more cautious visitor than we expected!",
    )),
    "TVSecretBaseSecrets_Text_UsedFence": (("FENCE", "trap"), (
        "The visitor is looking hard at a FENCE!",
        "Has an idea for a trap of their own just arrived?",
    )),
    "TVSecretBaseSecrets_Text_UsedGlitterMat": (("GLITTER MAT", "idol"), (
        "The visitor has stepped on a GLITTER MAT!",
        "The visitor is striking one pose after another!",
        "Somebody is imagining an audience!",
    )),
    "TVSecretBaseSecrets_Text_UsedTire": (("TIRE", "car"), (
        "The visitor is staring hard at a TIRE!",
        "Wondering what sort of vehicle it came off, perhaps.",
    )),
    "TVSecretBaseSecrets_Text_UsedStand": (("STAND", "roaring"), (
        "The visitor has climbed a STAND!",
        "The visitor is looking out over {STR_VAR_1}'s BASE from up there!",
        "And...",
        "Lets out a roar!|The visitor is roaring!",
    )),
    "TVSecretBaseSecrets_Text_BrokeDoor": (("BREAKABLE DOOR", "uproariously"), (
        "The visitor has run headlong into a BREAKABLE DOOR!",
        "And is laughing helplessly about it!",
    )),
    "TVSecretBaseSecrets_Text_UsedDoll": (("DOLL", "creepy"), (
        "The visitor is talking to a DOLL!",
        "...That is a little unsettling...",
    )),
    "TVSecretBaseSecrets_Text_UsedSlide": (("SLIDE", "grand old time"), (
        "The visitor is going up the ladder of a SLIDE!",
        "And...",
        "Down the visitor goes!",
        "Somebody is having the time of their life!",
    )),
    "TVSecretBaseSecrets_Text_UsedSlideButDidntGoDown": (("SLIDE", "chicken out"), (
        "The visitor is going up the ladder of a SLIDE!",
        "And...",
        "Back down the ladder the visitor comes!",
        "A late loss of nerve, I fancy.",
    )),
    "TVSecretBaseSecrets_Text_UsedJumpMat": (("JUMP MAT", "solo performance"), (
        "The visitor has stepped on a JUMP MAT!",
        "One jump!",
        "Two!",
        "And a clean landing!",
        "And now the visitor is applauding!|A performance entirely for one!",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, (_, paragraphs) in TARGETS.items():
        name = FURNITURE.get(label)
        if name and " " in name:
            paragraphs = tuple(p.replace(name, glued(name)) for p in paragraphs)
        composed[label] = BOX.compose(paragraphs)
    return composed


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
        masked = masked[:start] + '\t.string "<ARAUNA_TV_BASE_SECRETS_EN>"\n\n' + masked[end:]
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

    # The commentary is about a decoration the player can own. Lose the name
    # and the line is about nothing.
    for label, name in FURNITURE.items():
        if name not in "".join(composed[label]):
            raise ValueError(f"{label}: the line lost the thing it is about: {name}")

    # The commentator never says who the visitor is -- that is the conceit of
    # the programme, and {STR_VAR_2} is not always filled in these blocks.
    for label in FURNITURE:
        if "visitor" not in " ".join(composed[label]).lower():
            raise ValueError(f"{label}: stopped calling them the visitor")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render SECRET BASE SECRETS and WHAT'S NO. 1 IN ARAUNA.")
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
    print(f"TV base secrets English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

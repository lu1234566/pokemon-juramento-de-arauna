#!/usr/bin/env python3
"""ROUTE 111, the PASSO CORTADO, and the DRAGON hall in MeteorFalls.

Three stretches of open country, and two families that fight as units.

The WINSTRATES take you on four in a row, and the order is the point: the
husband, then his wife because you beat him, then the daughter because you
beat her mother, then the grandmother because you made the daughter cry.
Each of the four is written from one table that says who they follow, so the
chain cannot lose a link. If it does, a player fights four strangers instead
of a family closing ranks.

The couple in MeteorFalls are a matched pair -- fifty years married, and
every line one of them has, the other has a mirror of. Both halves are
generated from one table so the mirror holds.

Two signs carry information available nowhere else. The TRAINER TIPS board on
ROUTE 111 is the only place the game expands SP. ATK and SP. DEF into words,
so both expansions are held and both abbreviations are checked against
src/strings.c. And the boy who was told to bring ROCK SMASH is the only
warning that ROUTE 111 needs it.

WINSTRATE keeps its name.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

ROUTE111 = ROOT / "data" / "maps" / "Route111" / "scripts.inc"
JAGGED = ROOT / "data" / "maps" / "JaggedPass" / "scripts.inc"
FALLS = ROOT / "data" / "maps" / "MeteorFalls_1F_2R" / "scripts.inc"
STRINGS = ROOT / "src" / "strings.c"

# The route signs draw an arrow glyph, which takes one character's room.
BOX = TextBox({"{DOWN_ARROW}": 1, "{LEFT_ARROW}": 1, "{RIGHT_ARROW}": 1},
              width=34)

WHOLE = ("TORRE MIRAGEM", "CLAW FOSSIL", "ROOT FOSSIL", "ROCK SMASH",
         "MAGMA EMBLEM", "ACRO BIKE", "POKéNAV", "ELITE FOUR", "GYM LEADER",
         "POKéMON LEAGUE", "TRAINER HILL", "PASSO CORTADO", "SERRA DA CINZA",
         "ENCRUZILHADA", "SP. ATK", "SP. DEF", "ROUTE 111", "ROUTE 112",
         "ROUTE 113", "TRAINER TIPS")

# The four WINSTRATES, in the order the house sends them out, and why each
# one steps forward. The chain is what makes them a family rather than four
# people who happen to share a floor.
WINSTRATES: tuple[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]], ...] = (
    ("Victor",
     ("That is the spirit. I like you.",),
     ("Aiyah!|You are a great deal tougher than I took you for!",),
     ("Everyone! I have found us a strong one!",)),
    ("Victoria",
     ("Oh, my goodness, aren't you young?",
      "Though you must be quite the TRAINER, to have beaten my husband.",
      "My turn."),
     ("Oh, gosh!|I cannot get over how strong you are!",),
     ("There is a strong TRAINER in here!|Really strong!",)),
    ("Vivi",
     ("You are stronger than Mummy? Wow.",
      "But I am strong too.|Really. Honestly."),
     ("Huh? Did I just lose?",),
     ("This is horrible...|...Snivel...|Grandma!",)),
    ("Vicky",
     ("How dare you make my granddaughter cry.",
      "For that I am going to give you a smacking.|Prepare to lose."),
     ("Kwah! You are strong...|The girl was right about you...",),
     ("If you are in no hurry, stop and sit with us a while.",)),
)

# The couple in MeteorFalls. Fifty years married, and every line one has,
# the other has a mirror of.
COUPLE: dict[str, dict[str, tuple[str, ...]]] = {
    "John": {
        "name": ("NEI",),
        "Intro": ("NEI: We have always battled as a pair.|We have some "
                  "confidence in ourselves.",),
        "Defeat": ("NEI: Oh, my.|We have lost, dear wife.",),
        "PostBattle": ("NEI: Fifty years we have been married.",
                       "And now I think of it, I have never once beaten my "
                       "dear wife in a battle."),
        "NotEnoughMons": ("NEI: Well, well. What a young TRAINER.",
                          "Will you battle us? If so you must come back with "
                          "more POKéMON."),
        "RematchIntro": ("NEI: We have always battled as a pair.|We have "
                         "some confidence in ourselves.",),
        "RematchDefeat": ("NEI: Oh, my.|We have lost, dear wife.",),
        "PostRematch": ("NEI: Fifty years married...",
                        "Looking back, the dear wife and I have battled day "
                        "in and day out..."),
        "RematchNotEnoughMons": ("NEI: Well, well. What a young TRAINER.",
                                 "Will you battle us? If so you must come "
                                 "back with more POKéMON."),
    },
    "Jay": {
        "name": ("ADA",),
        "Intro": ("ADA: Fifty years we have been married.",
                  "What holds between the two of us could never be broken."),
        "Defeat": ("ADA: Oh, dear.|We have lost, my dear husband.",),
        "PostBattle": ("ADA: Fifty years of marriage...",
                       "Whenever we quarrelled we settled it with a POKéMON "
                       "battle..."),
        "NotEnoughMons": ("ADA: Well, well. Aren't you a young TRAINER.",
                          "If you care to battle us, you will have to come "
                          "back with more POKéMON."),
        "RematchIntro": ("ADA: Fifty years we have been married.",
                         "We have held each other up the whole of that time. "
                         "It has made us strong."),
        "RematchDefeat": ("ADA: Oh, dear.|We have lost, my dear husband.",),
        "PostRematch": ("ADA: Fifty years of marriage...|A great many things "
                        "have happened.",
                        "I hope we go on making happy memories together."),
        "RematchNotEnoughMons": ("ADA: Well, well. Aren't you a young "
                                 "TRAINER.",
                                 "If you care to battle us, you will have to "
                                 "come back with more POKéMON."),
    },
}
COUPLE_SHAPES = ("Intro", "Defeat", "PostBattle", "NotEnoughMons",
                 "RematchIntro", "RematchDefeat", "PostRematch",
                 "RematchNotEnoughMons")

ROUTE111_BLOCKS: dict[str, tuple[str, ...]] = {
    "BattleOurFamily": (
        "Hello. Travelling through, are you?",
        "Then how would this be? Take on the four of us, one after another.",
    ),
    "IsThatSo": (
        "Is that so?|Look in again if you change your mind.",
    ),
    "ToughToKeepWinningUpTheRanks": (
        "Raise your POKéMON further than that or you will find it hard "
        "going, the further up you get.",
        "They say the POKéMON LEAGUE's ELITE FOUR are far stronger than any "
        "GYM LEADER.",
    ),
    "WinstrateFamilyDestroyedMe": (
        "I took on the WINSTRATE family. Four matches back to back is hard "
        "going...|They took me apart.",
    ),
    "RouteSignMauville": (
        "ROUTE 111|{DOWN_ARROW} ENCRUZILHADA",
    ),
    "WinstrateHouseSign": (
        "“Our hearts beat as one.”|THE WINSTRATE'S HOUSE",
    ),
    "RouteSign112": (
        "ROUTE 111|{LEFT_ARROW} ROUTE 112",
    ),
    "RouteSign113": (
        "ROUTE 111|{LEFT_ARROW} ROUTE 113",
    ),
    "OldLadysRestStopSign": (
        "OLD LADY'S REST STOP|“Come in and rest your tired bones.”",
    ),
    "TrainerTipsSpAtkSpDef": (
        "TRAINER TIPS",
        "One measure of what a POKéMON can do is its SP. ATK. That is short "
        "for SPECIAL ATTACK.",
        "Likewise SP. DEF, which is short for SPECIAL DEFENSE.",
    ),
    "ShouldBeMirageTowerAroundHere": (
        "There is a tower made of sand somewhere hereabouts.",
        "Only for some reason it can be seen on some days and not on "
        "others.",
        "Which is why I call it the TORRE MIRAGEM.",
    ),
    "MirageTowerClearlyVisible": (
        "I see it!|The tower of sand!",
        "The one they call a mirage, plain as anything!",
        "It looks so fragile, though...|It could come apart at any moment...",
        "I want to go inside. I cannot get up the nerve for it...",
    ),
    "ThatWasShockingSandRainedDown": (
        "Whoa...|That gave me a turn.",
        "Sand came down in great lumps, all at once.",
        "What was it like in there?|Sandy ghosts and the like?",
    ),
    "MirageTowerHasntBeenSeenSince": (
        "Not once since I spoke to you has the tower of sand been seen.",
        "Perhaps it really was the TORRE MIRAGEM...",
    ),
    "ClawFossilDisappeared": (
        "The CLAW FOSSIL went down into the sand...",
    ),
    "RootFossilDisappeared": (
        "The ROOT FOSSIL went down into the sand...",
    ),
    "MauvilleUncleToldMeToTakeRockSmash": (
        "Oh, no.",
        "My uncle in ENCRUZILHADA told me to take ROCK SMASH with me if I "
        "was going to ROUTE 111.",
        "My uncle? He lives opposite the cycle shop in ENCRUZILHADA.",
    ),
    "TrainerHillSign": (
        "{RIGHT_ARROW} TRAINER HILL ENTRANCE",
        "“Climb it, if your blood is hot enough.”",
    ),
}

JAGGED_BLOCKS: dict[str, tuple[str, ...]] = {
    "EricIntro": (
        "SERRA DA CINZA's PASSO CORTADO...",
        "This is what I have always wanted from a mountain.",
        "All this jagged, broken ground...|It shakes something in me.",
    ),
    "EricDefeat": (
        "Losing has left me bitter.",
    ),
    "EricPostBattle": (
        "Yes, I lost at POKéMON...",
        "But on loving mountains I have you beaten outright.",
    ),
    "DianaIntro": (
        "This is no casual walk.|It is not the place for a picnic.",
    ),
    "DianaDefeat": (
        "Ohhh, no!|The ground here is far too broken up...",
    ),
    "DianaPostBattle": (
        "Did you know?",
        "There are people who cleverly ride bicycles up this dreadful "
        "broken pass.",
    ),
    "DianaRegister": (
        "Will you ever be back this way?|If you are, I should like another "
        "go.",
    ),
    "DianaRematchIntro": (
        "A picnic is a fine thing wherever you have it.|Rather like "
        "POKéMON.",
    ),
    "DianaRematchDefeat": (
        "I only lost because the ground is so broken up!",
    ),
    "DianaPostRematch": (
        "I shall forget about losing and simply enjoy the walk.",
    ),
    "EthanIntro": (
        "PASSO CORTADO is hard walking.|Which makes it good ground to train "
        "on.",
    ),
    "EthanDefeat": (
        "It was all over while we were still looking for our footing...",
    ),
    "EthanPostBattle": (
        "With an ACRO BIKE I could get over those ledges.",
    ),
    "EthanRegister": (
        "Once I am used to this ground I shall win.",
        "Will you register me in your POKéNAV?",
    ),
    "EthanRematchIntro": (
        "I am used to the ground now.|I sing on the way up.",
    ),
    "EthanRematchDefeat": (
        "It is still no easy thing, battling on ground like this...",
    ),
    "EthanPostRematch": (
        "I really ought to get an ACRO BIKE from RYDEL in ENCRUZILHADA...",
    ),
    "GruntIntro": (
        "Wah!|What are you doing up here?",
        "What am I doing in a place like this?",
        "And what business is that of yours?",
    ),
    "GruntDefeat": (
        "Urrrgh...",
        "I should have gone straight into our HIDEOUT...",
    ),
    "GoWhereverYouWant": (
        "All right, all right!|You are strong, I admit it.",
        "Never mind me.|Go where you like.",
    ),
    "BoulderShakingInResponseToEmblem": (
        "Oh! The boulder is shaking. It is answering the MAGMA EMBLEM.",
    ),
    "JulioIntro": (
        "Aiyeeh! Coming down this mountain in one run is a frightening "
        "business!",
    ),
    "JulioDefeat": (
        "I feel as though I am coming apart...",
    ),
    "JulioPostBattle": (
        "My bicycle bounced about so much my backside will not forgive me...",
    ),
    "AutumnIntro": (
        "I climb this hill every day.|I have confidence in what that has "
        "made me.",
    ),
    "AutumnDefeat": (
        "Hmm...|Where did that go wrong?",
    ),
    "AutumnPostBattle": (
        "What is that odd bit of rock sticking out, a little way up the "
        "hill?",
    ),
}

FALLS_BLOCKS: dict[str, tuple[str, ...]] = {
    "NicolasIntro": (
        "This is where those of us who use DRAGONS come to train.",
        "The CHAMPION comes here.|Do you see now what sort of place this "
        "is?",
    ),
    "NicolasDefeat": (
        "Urgh!|I did not expect you to be that strong.",
    ),
    "NicolasPostBattle": (
        "The road ahead is long, and it is hard.",
        "When will my POKéMON and I be the best there is?",
    ),
    "NicolasRegister": (
        "I want to know more about what you can do.|Let me register you in "
        "my POKéNAV.",
    ),
    "NicolasRematchIntro": (
        "Since we last met we have trained hard, with our eyes on the top.",
        "Show us how much further we have come.",
    ),
    "NicolasRematchDefeat": (
        "Urgh!|I did not expect you to be that strong.",
    ),
    "NicolasPostRematch": (
        "You have clearly not let up on your training.",
        "So long as you stay strong, I can go on getting stronger too.",
    ),
    "JohnRegister": (
        "NEI: Young TRAINER -- if the chance comes round again, will you "
        "battle us?",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    route111 = {f"Route111_Text_{label}": body
                for label, body in ROUTE111_BLOCKS.items()}
    for name, intro, defeat, after in WINSTRATES:
        route111[f"Route111_Text_{name}Intro"] = intro
        route111[f"Route111_Text_{name}Defeat"] = defeat
        route111[f"Route111_Text_{name}PostBattle"] = after

    jagged = {f"JaggedPass_Text_{label}": body
              for label, body in JAGGED_BLOCKS.items()}

    falls = {f"MeteorFalls_1F_2R_Text_{label}": body
             for label, body in FALLS_BLOCKS.items()}
    for who, lines in COUPLE.items():
        for shape in COUPLE_SHAPES:
            falls[f"MeteorFalls_1F_2R_Text_{who}{shape}"] = lines[shape]
    return {"route111": route111, "jagged": jagged, "falls": falls}


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"route111": ROUTE111, "jagged": JAGGED, "falls": FALLS}


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
        composed[label] = BOX.compose(tuple(glued_paragraphs))
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
                         + '\t.string "<ARAUNA_DESERT_PASS_FALLS_EN>"\n\n'
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
    strings = STRINGS.read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # Four in a row, and each one steps forward because of the last. If two
    # of them read alike, the player is fighting strangers.
    for shape in ("Intro", "Defeat", "PostBattle"):
        said = [flat(f"Route111_Text_{name}{shape}")
                for name, _i, _d, _p in WINSTRATES]
        if len(set(said)) != len(said):
            raise ValueError(
                f"two WINSTRATES give an identical {shape}, so the family "
                f"reads as four unconnected people")
    # The chain itself: the wife names her husband, the grandmother names
    # her granddaughter.
    if "husband" not in flat("Route111_Text_VictoriaIntro"):
        raise ValueError(
            "VictoriaIntro: no longer says she is following her husband, and "
            "the four stop being a family")
    if "granddaughter" not in flat("Route111_Text_VickyIntro"):
        raise ValueError(
            "VickyIntro: no longer says why she has stepped forward")

    # The pair in MeteorFalls mirror each other. Both halves, all eight
    # shapes, and each half keeps its own name on the front.
    for who, lines in COUPLE.items():
        speaker = lines["name"][0]
        for shape in COUPLE_SHAPES:
            text = flat(f"MeteorFalls_1F_2R_Text_{who}{shape}")
            if not text.startswith(f"{speaker}:"):
                raise ValueError(
                    f"{who}{shape}: no longer opens with {speaker}, and the "
                    f"player cannot tell which of the two is talking")
    for shape in COUPLE_SHAPES:
        halves = [flat(f"MeteorFalls_1F_2R_Text_{who}{shape}") for who in COUPLE]
        if len(set(halves)) != len(halves):
            raise ValueError(f"both halves of the couple give the same {shape}")

    # The TRAINER TIPS board is the only place the game spells these out.
    tips = flat("Route111_Text_TrainerTipsSpAtkSpDef")
    for short, long, symbol in (("SP. ATK", "SPECIAL ATTACK", "gText_SpAtk"),
                                ("SP. DEF", "SPECIAL DEFENSE", "gText_SpDef")):
        if f'{symbol}[] = _("{short}")' not in strings:
            raise ValueError(
                f"TrainerTips: expands {short!r}, which is not what {symbol} "
                f"in src/strings.c prints")
        if short not in tips or long not in tips:
            raise ValueError(
                f"TrainerTips: no longer expands {short} into {long}, and no "
                f"other sign in the game does")

    # The only warning that ROUTE 111 needs a field move.
    if "ROCK SMASH" not in flat("Route111_Text_MauvilleUncleToldMeToTakeRockSmash"):
        raise ValueError(
            "MauvilleUncleToldMeToTakeRockSmash: no longer names ROCK SMASH, "
            "and nothing else warns a player they will need it")

    # The boulder answers one item and only that item.
    if "MAGMA EMBLEM" not in flat("JaggedPass_Text_BoulderShakingInResponseToEmblem"):
        raise ValueError(
            "BoulderShakingInResponseToEmblem: no longer names what the "
            "boulder is answering")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render ROUTE 111, the PASSO CORTADO and MeteorFalls.")
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
    print(f"Desert, pass and falls English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

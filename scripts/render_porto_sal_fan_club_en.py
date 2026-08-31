#!/usr/bin/env python3
"""The POKéMON FAN CLUB in PORTO DO SAL, and the corridor beside the tent.

The CHAIRMAN examines a POKéMON, decides how well it has been raised, and
hands over a SCARF. The five SCARVES are the point of the room: each one
raises a different CONTEST condition, and this is the only place in the game
that says which. So the five explanations are generated from one table
pairing a colour to a condition, every colour is checked against the item
name the BAG will print, and every condition against the word the CONTEST
itself uses. A GREEN SCARF that the CHAIRMAN says helps with beauty is worse
than no explanation at all.

The three cry lines are left alone -- they are the noise the animals make.

The corridor beside the BATTLE TENT holds fourteen texts Emerald marks as
unused: they are the CONTEST HALL crowd from an earlier draft, and nothing in
the game reaches them any more. They are rewritten anyway, so no stretch of
the script is left in another game's voice, and so that they read correctly
if anything is ever wired back to them. One factual repair goes with that:
the CONTEST PASS line called VALE DO SILENCIO a city, and it is a town.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

FAN_CLUB = ROOT / "data" / "maps" / "SlateportCity_PokemonFanClub" / "scripts.inc"
CORRIDOR = ROOT / "data" / "maps" / "SlateportCity_BattleTentCorridor" / "scripts.inc"
ITEMS_TABLE = ROOT / "src" / "data" / "items.h"

BOX = TextBox({"{STR_VAR_1}": 12, "{POKEBLOCK}": 9}, width=34)

WHOLE = ("POKéMON FAN CLUB", "FAN CLUB", "CONTEST PASS", "CONTEST JUDGE",
         "GYM LEADER", "RED SCARF", "BLUE SCARF", "PINK SCARF",
         "GREEN SCARF", "YELLOW SCARF", "VALE DO SILENCIO", "HYPER RANK",
         "BAG")

# colour -> (item name as the BAG prints it, the CONTEST condition it
# raises, how the CHAIRMAN puts it). One table, five explanations, so a
# SCARF cannot end up credited with the wrong condition.
SCARVES: dict[str, tuple[str, str, str]] = {
    "Red": ("RED SCARF", "coolness",
            "and every eye in the hall will take in its coolness"),
    "Blue": ("BLUE SCARF", "beauty",
             "and its beauty will carry much further than it does now"),
    "Pink": ("PINK SCARF", "cuteness",
             "and it will draw out more of the creature's cuteness"),
    "Green": ("GREEN SCARF", "smartness",
              "and its smartness will show all the more clearly"),
    "Yellow": ("YELLOW SCARF", "toughness",
               "and its toughness will come through far stronger"),
}

FAN_CLUB_BLOCKS: dict[str, tuple[str, ...]] = {
    "MeetChairman": (
        "Er-hem. I am the CHAIRMAN of the POKéMON FAN CLUB.",
        "Being the CHAIRMAN, I am naturally the most important person in "
        "it.",
        "Nobody alive can better me at raising POKéMON. Nobody.",
        "Now. Let me tell you about POKéMON CONTESTS.",
        "They are occasions for showing a POKéMON off to the world.",
        "But they are held in distant towns, and I cannot get to them nearly "
        "often enough.",
        "Which is why we gather here instead, to show one another what we "
        "have raised.",
    ),
    "LikeToSeeEnteredContestPokemon": (
        "A POKéMON belonging to a TRAINER who has actually entered a "
        "CONTEST...|That, I should like to see.",
    ),
    "AllowMeToExamineYourPokemon": (
        "Er-hem. I see you have taken part in a POKéMON CONTEST.",
        "Then allow me to examine how you have raised it.",
        "There is no end to the pleasure I take in POKéMON raised by other "
        "TRAINERS.",
        "The look on a POKéMON that has been properly cared for...",
        "The kindness in the eye of the TRAINER who did the caring...",
        "The thought alone fills me up entirely.",
        "Oh. I do beg your pardon.|Forgive an old man for prattling.",
        "Please. Let me see how far it has come.",
    ),
    "HowIsYourPokemonGrowing": (
        "And how is your POKéMON coming along?|Allow me to examine it.",
    ),
    "HmHmISee": (
        "Hm. Hm...|I see...",
    ),
    "GiveMonMorePokeblocks": (
        "Hmmm. Not bad. But not good either.",
        "You are its TRAINER. More is required of you than this.",
        "Might I suggest, for a start, rather more {POKEBLOCK}S?",
    ),
    "NoSpaceForReward": (
        "Oh dear...",
        "Your POKéMON is coming along handsomely and you have earned "
        "something for it.",
        "Only there is no room in your BAG to put it.",
    ),
    "MonMostImpressiveGiveItThis": (
        "Your {STR_VAR_1} is coming along most impressively.|A fine "
        "specimen. Truly.",
        "But! Give it this, and it will come along better still. It will "
        "indeed.",
    ),
    "NothingElseToGiveYou": (
        "I am sorry, but I have nothing left to give you. Nothing at all.",
        "You are blessed, after all, with the knack of raising POKéMON "
        "without needing any help from an item.",
    ),
    "ShowMePokemonThatLoveYou": (
        "What I most love to see is a POKéMON that loves its TRAINER.",
        "They are very sensitive to how a TRAINER feels about them.",
        "Treat a POKéMON with love and care, and it will love you back.",
        "When yours has come to love you, bring it and show me.",
    ),
    "PokemonAdoresYou": (
        "Your POKéMON truly adores you.",
        "For a TRAINER of such feeling -- a gift, from the FAN CLUB.",
    ),
    "TreatPokemonWithLove": (
        "POKéMON are very sensitive to how a TRAINER feels about them.",
        "Treat one with love and care, and it will love you back.",
    ),
    "PokemonDontLikeFainting": (
        "Keep letting a POKéMON faint in battle and it will come to resent "
        "it.",
        "Before long it trusts its TRAINER less.",
        "Which is to say it will not think much of you at all.",
    ),
    "MonEnjoyedProtein": (
        "Do POKéMON enjoy having things used on them, do you think?",
        "Mine was thoroughly pleased with itself when I gave it PROTEIN.",
    ),
}

CORRIDOR_BLOCKS: dict[str, tuple[str, ...]] = {
    "AdviceForContests": (
        "Would you like a useful little piece of advice about CONTESTS?",
        "Using one move after another particular kind of move sometimes "
        "wins you extra attention.",
        "Know what you are doing with that and you can score enormously in "
        "the appeal.",
        "Though your opponents may well be trying to disrupt your POKéMON "
        "while you do it.",
    ),
    "MyPapaIsContestJudge": (
        "My papa is a CONTEST JUDGE.",
        "I cannot decide what to be when I am grown. A JUDGE, or a GYM "
        "LEADER?",
    ),
    "ImLikeMajorlyCheesed": (
        "Hey, man, I am like majorly cheesed off, you know? Like, I only "
        "wanted to know why my POKéMON never wins, you know?",
        "So, like, I gave the JUDGE my two cents. Free of charge.",
        "And he would not hear me out. Like, hey! Total bummer, man.",
        "Hey. You. Zip it, you know?|Just, you know, take this.",
    ),
    "ExplainTorment": (
        "That is, like, TM41, you know?|TORMENT, you hearing me?",
        "Like, it stops the other guy using the same move twice running, "
        "see?",
        "Hey, now, you listen. I am not laying a torment on you.",
    ),
    "MCStepUpTakePartInContest": (
        "MC: Oh, my, my!|Now is that not a dandy of a POKéMON?",
        "Please! Step right up and take part in our splendid CONTESTS!",
        "You will do well. I am sure of it. My eye has never once failed "
        "me.",
    ),
    "JudgeWouldntDoToMissContest": (
        "JUDGE: Well, hello there.|A TRAINER, I see.",
        "Then it would never do for you to miss a POKéMON CONTEST.",
        "Get yourself a CONTEST PASS in VALE DO SILENCIO and you may enter "
        "whenever you like.",
    ),
    "ItsAppealTime": (
        "It is appeal time!|What do I lead with?",
    ),
    "DidntPayAttentionToAppeal": (
        "They hardly looked at my POKéMON's appeal...",
        "Humph. That JUDGE would not know a good thing if it sat on him.",
    ),
    "RewardWithSageAdvice": (
        "Oh, hello. You must be a serious follower to get this close to the "
        "floor.",
        "I shall reward that with some advice.",
        "When a move goes over really well, the audience gets excited.",
        "And the POKéMON that makes its appeal at the moment everyone is "
        "excited...",
        "Well. You would expect something good to come of that.",
    ),
    "MoreFreakedOutThanMon": (
        "I cannot do this. I am in a worse state than my POKéMON.",
        "I am shaking and my heart will not slow down.",
    ),
    "BattleAndContestAlike": (
        "A battle and a CONTEST are not the same thing, but they are alike.",
        "Both of them ask you to work at it and to believe in what you have "
        "raised.",
    ),
    "MonLooksOnTopOfGame": (
        "That POKéMON looks like it is on top of its game, does it not?",
        "One that does well in the secondary judging always seems more at "
        "ease during the appeals.",
    ),
    "MyMonBetterThanThatLot": (
        "Will you look at that sorry sight.",
        "Heh. Mine is better than that lot without even trying.",
    ),
    "GetUrgeToMoveWithMon": (
        "Do you not get the urge to move along with them, when a POKéMON is "
        "putting on an energetic appeal?",
    ),
    "HyperRankStage": (
        "POKéMON CONTESTS|HYPER RANK STAGE!",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    club = {f"SlateportCity_PokemonFanClub_Text_{label}": body
            for label, body in FAN_CLUB_BLOCKS.items()}
    for colour, (item, _condition, praise) in SCARVES.items():
        club[f"SlateportCity_PokemonFanClub_Text_Explain{colour}Scarf"] = (
            f"Let a POKéMON hold that {item},",
            f"{praise[0].upper()}{praise[1:]}.",
        )
    corridor = {f"SlateportCity_ContestHall_Text_{label}": body
                for label, body in CORRIDOR_BLOCKS.items()}
    return {"club": club, "corridor": corridor}


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"club": FAN_CLUB, "corridor": CORRIDOR}


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
                         + '\t.string "<ARAUNA_FAN_CLUB_EN>"\n\n'
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
    items = ITEMS_TABLE.read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # Five SCARVES, five conditions, and this room is the only place the
    # pairing is ever stated.
    seen = []
    for colour, (item, condition, _praise) in SCARVES.items():
        if f'.name = _("{item}")' not in items:
            raise ValueError(
                f"{colour}: the CHAIRMAN calls it {item!r}, which is not a "
                f"name in src/data/items.h")
        text = flat(f"SlateportCity_PokemonFanClub_Text_Explain{colour}Scarf")
        if item not in text:
            raise ValueError(f"Explain{colour}Scarf: no longer names the {item}")
        if condition not in text.lower():
            raise ValueError(
                f"Explain{colour}Scarf: no longer says it raises {condition}, "
                f"which is the only reason to hold it")
        seen.append(condition)
    if len(set(seen)) != len(seen):
        raise ValueError(
            "two SCARVES are credited with the same condition, so one of the "
            "five is wrong")

    # VALE DO SILENCIO is a town. Emerald's line calls the CONTEST PASS's
    # home a city, and it never was one.
    pass_line = flat("SlateportCity_ContestHall_Text_JudgeWouldntDoToMissContest")
    if "CONTEST PASS" not in pass_line or "VALE DO SILENCIO" not in pass_line:
        raise ValueError(
            "JudgeWouldntDoToMissContest: no longer says where a CONTEST PASS "
            "comes from")
    if "VALE DO SILENCIO CITY" in pass_line:
        raise ValueError("VALE DO SILENCIO is a town, not a city")

    # The CHAIRMAN's advice on affection is given twice, in two states, and
    # both have to carry it.
    for label in ("ShowMePokemonThatLoveYou", "TreatPokemonWithLove"):
        if "love you back" not in flat(f"SlateportCity_PokemonFanClub_Text_{label}"):
            raise ValueError(f"{label}: lost the advice it exists to give")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the PORTO DO SAL FAN CLUB and tent corridor.")
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
    print(f"Porto do Sal fan club English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

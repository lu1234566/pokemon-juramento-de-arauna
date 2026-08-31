#!/usr/bin/env python3
"""RYDEL's cycle shop and the ENCRUZILHADA GAME CORNER.

Two counters on the same street, and both of them are the only place in the
game where something a player needs is explained.

The cycle shop is the more important of the two. Its five handbook pages are
the whole of the game's instruction on how a BIKE is ridden -- the + Control
Pad, the B Button, the wheelie, the bunny hop, the jump, and the fact that a
sandy slope can only be climbed on a MACH BIKE. A player who never opens
those handbooks has been told none of it, and a page that loses its button is
a page that teaches nothing. The renderer holds every control and every
technique into its own page.

The choice between the two BIKES is the other thing that has to survive: what
each is for, and that RYDEL will swap them any time. A player who thinks the
choice is final will pick differently.

At the GAME CORNER the numbers are the content -- the price of COINS, the
three-COIN limit on the SLOTS, the fact that the ROULETTE tables pay at
different rates -- and they are kept.

RYDEL keeps his name.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

BIKE_SHOP = ROOT / "data" / "maps" / "MauvilleCity_BikeShop" / "scripts.inc"
GAME_CORNER = ROOT / "data" / "maps" / "MauvilleCity_GameCorner" / "scripts.inc"
ITEMS_TABLE = ROOT / "src" / "data" / "items.h"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 12, "{STR_VAR_2}": 10},
              width=34)

WHOLE = ("MACH BIKE", "ACRO BIKE", "COIN CASE", "GAME CORNER",
         "ENCRUZILHADA", "VILA AMANHECER", "RUNNING SHOES", "REEL TIME",
         "+ Control Pad", "B Button", "ARAUNA", "ROULETTE", "SLOTS")

# Named in the shop and checked against the table the BAG draws from.
ITEM_NAMES = ("MACH BIKE", "ACRO BIKE", "COIN CASE")

BIKE_BLOCKS: dict[str, tuple[str, ...]] = {
    "RydelGreeting": (
        "Well, well. What have we here?|A customer with some energy about "
        "them!",
        "Me? You may call me RYDEL.|This cycle shop is mine.",
    ),
    "DidYouComeFromFarAway": (
        "RYDEL: Those RUNNING SHOES of yours...|They are filthy.",
        "Have you come a long way?",
    ),
    "GuessYouDontNeedBike": (
        "RYDEL: Is that so?",
        "Then I suppose none of my BIKES would be of use to you.",
    ),
    "ExplainBikesChooseWhichOne": (
        "RYDEL: Hm. Hm... ... ... ...",
        "You are telling me you walked all the way here from VILA AMANHECER?",
        "My word!|That is a ridiculous distance!",
        "With one of my BIKES you could go anywhere you liked, and feel the "
        "wind on you while you did it.",
        "I will tell you what.|I shall give you a BIKE.",
        "Oh -- wait a moment.",
        "I forgot to say. There are two kinds.",
        "The MACH BIKE and the ACRO BIKE.",
        "The MACH BIKE is for the rider who wants the wind in their face.",
        "The ACRO BIKE is for the rider who would rather do something "
        "clever with it.",
        "And I am a soft touch, so you may have whichever you like.",
        "Which is it to be?",
    ),
    "ChoseMachBike": (
        "{PLAYER} chose the MACH BIKE.",
    ),
    "ChoseAcroBike": (
        "{PLAYER} chose the ACRO BIKE.",
    ),
    "ComeBackToSwitchBikes": (
        "RYDEL: And if you ever fancy the other one, come and see me. I "
        "shall swap it over.",
    ),
    "WantToSwitchBikes": (
        "RYDEL: Oh? Were you thinking of swapping BIKES?",
    ),
    "IllSwitchBikes": (
        "RYDEL: Of course, no trouble at all.|I shall swap it over.",
    ),
    "ExchangedMachForAcro": (
        "{PLAYER} exchanged the MACH BIKE for an ACRO BIKE.",
    ),
    "ExchangedAcroForMach": (
        "{PLAYER} exchanged the ACRO BIKE for a MACH BIKE.",
    ),
    "HappyYouLikeIt": (
        "RYDEL: Good, good!|I am glad it suits you!",
    ),
    "OhYourBikeIsInPC": (
        "Oh? And what has become of the BIKE I gave you?",
        "Ah -- I see. You have put it away in your PC.",
        "Take it back out of storage and I shall be glad to exchange it.",
        "May the wind be at your back, wherever you are going.",
    ),
    "HandbooksAreInBack": (
        "I am learning about BIKES while I work here.",
        "If you want to know how to ride yours, there are a couple of "
        "handbooks in the back.",
    ),

    # -- the MACH BIKE handbook --------------------------------------------
    "MachHandbookWhichPage": (
        "This is the handbook for the MACH BIKE.|Which page?",
    ),
    "HowToRideMachBike": (
        "A BIKE goes the way the + Control Pad is pressed.",
        "Once it is rolling it picks up speed on its own.",
        "Let go of the + Control Pad to stop. It slows to a halt.",
        "Another page?",
    ),
    "HowToTurnMachBike": (
        "A MACH BIKE is fast, and it does not stop quickly.",
        "Which makes a corner rather awkward.",
        "Release the + Control Pad a little before the corner and let it "
        "slow.",
        "Another page?",
    ),
    "SandySlopes": (
        "There are small sandy slopes all over ARAUNA.",
        "The sand is loose and gives way, so on foot they cannot be climbed "
        "at all.",
        "On a MACH BIKE you go straight up them.",
        "Another page?",
    ),

    # -- the ACRO BIKE handbook --------------------------------------------
    "AcroHandbookWhichPage": (
        "This is the handbook for the ACRO BIKE.|Which page?",
    ),
    "Wheelies": (
        "Press the B Button while riding and the front wheel comes up.",
        "With it up, you can go on steering with the + Control Pad.",
        "That is what a wheelie is.",
        "Another page?",
    ),
    "BunnyHops": (
        "Hold the B Button down and the BIKE hops on the spot.",
        "That is a bunny hop.",
        "You can ride along hopping, too.",
        "Another page?",
    ),
    "Jumps": (
        "Press the B Button and the + Control Pad together to jump.",
        "Press the + Control Pad sideways to jump sideways.",
        "Press it backwards and the BIKE turns about in the air.",
        "Another page?",
    ),
}

GAME_CORNER_BLOCKS: dict[str, tuple[str, ...]] = {
    "ThisIsMauvilleGameCorner": (
        "This is the ENCRUZILHADA GAME CORNER.",
    ),
    "NeedCoinCaseForCoins": (
        "COINS for the machines, was it?",
        "Only you have no COIN CASE to keep them in.",
    ),
    "WereYouLookingForCoins": (
        "Were you after some COINS?",
        "Fifty of them for ¥1000.|Would you like some?",
    ),
    "ThankYouHereAreYourCoins": (
        "Thank you very much.|Your COINS.",
    ),
    "DontHaveEnoughMoney": (
        "Um... you do not appear to have the money...",
    ),
    "CoinCaseIsFull": (
        "Oh?|Your COIN CASE is full.",
    ),
    "DontNeedCoinsThen": (
        "Oh... no COINS today, then?|Good luck out there.",
    ),
    "ExchangeCoinsForPrizes": (
        "Welcome.",
        "You can turn your COINS into prizes here.",
    ),
    "WhichPrize": (
        "Which prize would you like?",
    ),
    "SoYourChoiceIsTheTMX": (
        "Your choice is the {STR_VAR_1} {STR_VAR_2}?",
    ),
    "SendToYourHomePC": (
        "Thank you.|We will send it to the PC at your house.",
    ),
    "NotEnoughCoins": (
        "You have not the COINS for that.",
    ),
    "NoRoomForPlacingDecor": (
        "There is nowhere left to put a {STR_VAR_1}.",
    ),
    "OhIsThatSo": (
        "Oh, is that so?",
        "You will want to save up some COINS before you come back to me.",
    ),
    "SoYourChoiceIsX": (
        "Your choice is {STR_VAR_1}?",
    ),
    "HereYouGo": (
        "There you are.",
    ),
    "CantCarryAnyMore": (
        "Oh -- you cannot carry any more than that.",
    ),
    "GotTwoOfSameDollWantOne": (
        "I made a mess of it and won two of the same DOLL.",
        "Would you like one of them?",
    ),
    "HereYouGo2": (
        "There you are!",
    ),
    "YouWantItButNotNow": (
        "Hm?|You want it, only not now?",
    ),
    "DontBeNegative": (
        "Oh, do not be like that.|Have it.",
    ),
    "CantWinJackpot": (
        "There is a prize I want and I cannot win the jackpot to save my "
        "life.",
    ),
    "NeedCoinCaseGoNextDoor": (
        "Here, you. If you want to play in here you need a COIN CASE.",
        "I think the young lady next door had one. Go and ask her.",
    ),
    "LuckOnlyLastSoLongTakeCoins": (
        "My luck will not hold for ever. This is more than I know what to "
        "do with.|Here -- take some COINS.",
    ),
    "MauvilleSomethingForEveryone": (
        "There is something in ENCRUZILHADA for everybody.",
        "For me it is the GAME CORNER.",
    ),
    "RouletteTablesDifferentRates": (
        "The ROULETTE tables do not all pay at the same rate.",
        "Count your COINS before you pick one.",
    ),
    "EasyToLoseTrackOfTime": (
        "It is far too easy to lose an afternoon in here.|I ought to be back "
        "at work.",
    ),
    "CoinsAreNeededToPlay": (
        "You need COINS to play anything in the GAME CORNER.",
    ),
    "RouletteOnlyLuck": (
        "This ROULETTE business...|It asks a lot of a person.",
        "And win or lose, it is nothing but luck.",
    ),
    "UpTo3CoinsCanBeUsed": (
        "You may stake up to three COINS on a spin of the SLOTS.",
    ),
    "DifficultToStopOn7": (
        "Stopping it dead on “7” is very hard indeed.",
        "Land a “7” during the REEL TIME bonus and you take extra COINS.",
    ),
    "HeresSomeSlotsInfo": (
        "A word about the SLOTS.",
        "The more lightning bolts you have stocked, the more REEL TIME "
        "chances you get.",
        "In a game with the full five REEL TIME chances...",
        "It is possible to take four regular bonuses and then a big one.",
        "That comes to 660 COINS. It is also very nearly impossible.",
    ),
    "CantPlayWithNoCoinCase": (
        "You cannot play without a COIN CASE.",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    return {
        "bike": {f"MauvilleCity_BikeShop_Text_{label}": body
                 for label, body in BIKE_BLOCKS.items()},
        "games": {f"MauvilleCity_GameCorner_Text_{label}": body
                  for label, body in GAME_CORNER_BLOCKS.items()},
    }


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"bike": BIKE_SHOP, "games": GAME_CORNER}

# Each handbook page and the control it teaches. A page that loses its
# button teaches nothing, and nothing else in the game teaches it.
PAGES: dict[str, tuple[str, ...]] = {
    "HowToRideMachBike": ("+ Control Pad",),
    "HowToTurnMachBike": ("+ Control Pad", "corner"),
    "SandySlopes": ("MACH BIKE", "sandy slope"),
    "Wheelies": ("B Button", "wheelie"),
    "BunnyHops": ("B Button", "bunny hop"),
    "Jumps": ("B Button", "+ Control Pad", "jump"),
}


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
                         + '\t.string "<ARAUNA_AMUSEMENTS_EN>"\n\n'
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

    # The shop hands over items the BAG will list by name.
    for name in ITEM_NAMES:
        if f'.name = _("{name}")' not in items:
            raise ValueError(
                f"the shop calls an item {name!r}, which is not a name in "
                f"src/data/items.h")

    # Every handbook page teaches one thing and is the only place it is
    # taught.
    for page, controls in PAGES.items():
        text = flat(f"MauvilleCity_BikeShop_Text_{page}")
        for control in controls:
            if control.lower() not in text.lower():
                raise ValueError(
                    f"{page}: no longer mentions {control!r}, and nothing "
                    f"else in the game teaches it")

    # The choice of BIKE has to say what each is for, or it is a coin toss.
    offer = flat("MauvilleCity_BikeShop_Text_ExplainBikesChooseWhichOne")
    for bike in ("MACH BIKE", "ACRO BIKE"):
        if bike not in offer:
            raise ValueError(f"ExplainBikesChooseWhichOne: no longer offers the {bike}")
    # And that it is not final.
    swap = flat("MauvilleCity_BikeShop_Text_ComeBackToSwitchBikes")
    if "swap" not in swap.lower() and "switch" not in swap.lower():
        raise ValueError(
            "ComeBackToSwitchBikes: no longer says the choice can be undone, "
            "which changes how a player picks")

    # The GAME CORNER's numbers are its content.
    if "¥1000" not in flat("MauvilleCity_GameCorner_Text_WereYouLookingForCoins"):
        raise ValueError("WereYouLookingForCoins: no longer states the price")
    if "three" not in flat("MauvilleCity_GameCorner_Text_UpTo3CoinsCanBeUsed"):
        raise ValueError("UpTo3CoinsCanBeUsed: no longer states the stake limit")
    if "660" not in flat("MauvilleCity_GameCorner_Text_HeresSomeSlotsInfo"):
        raise ValueError("HeresSomeSlotsInfo: no longer states the maximum")

    # Both refusals for a missing CASE have to name it, since one is given
    # by staff and the other by a stranger and a player may meet either.
    for label in ("NeedCoinCaseForCoins", "NeedCoinCaseGoNextDoor",
                  "CantPlayWithNoCoinCase"):
        if "COIN CASE" not in flat(f"MauvilleCity_GameCorner_Text_{label}"):
            raise ValueError(f"{label}: no longer says a COIN CASE is what is missing")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the ENCRUZILHADA cycle shop and GAME CORNER.")
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
    print(f"Encruzilhada amusements English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

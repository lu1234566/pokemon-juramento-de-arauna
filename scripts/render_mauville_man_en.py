#!/usr/bin/env python3
"""The five men in the ENCRUZILHADA POKéMON CENTER who all want a moment.

Only one of them stands there at a time, and which one is decided by the save
file: the TRADER, the STORYTELLER, GIDDY, the BARD, the HIPSTER. Emerald gave
all five the same line when you refuse them -- "You've left me feeling the
blues" -- which reads like one man in five hats, and is the giveaway that
nobody meant them to be five people. Here each takes a refusal in his own way,
and the renderer refuses to let two of them share one.

The STORYTELLER is thirty-six tales, and a tale is not free prose: it is a
title, an entry in a menu, a sentence with the count in it, and a closing
line about the trainer. The engine draws the title and the action in a list,
where a long one is simply cut off, so both are measured against the widest
the original list draws rather than guessed at.

The tale itself is fixed in shape -- who it is about, what they did and how
many times, and what that says about them -- so the shape is written once and
the thirty-six are a table. Writing them out by hand is thirty-six chances to
tell the same story twice.
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

MAN = ROOT / "data" / "scripts" / "mauville_man.inc"
PREFIX = "MauvilleCity_PokemonCenter_1F_Text_"

BOX = TextBox({"{STR_VAR_1}": 10, "{STR_VAR_2}": 14, "{STR_VAR_3}": 10,
               "{POKEBLOCK}": 9}, width=34)

# Measured from the widest entry the original story list draws. A title or an
# action past this is cut off on screen with nothing to say it was.
TITLE_CEILING = 187
ACTION_CEILING = 176

# key -> (title, menu entry, the sentence with the count, what it says of them)
TALES: dict[str, tuple[str, str, str, str]] = {
    "SavedGame": (
        "The Cautious TRAINER", "Saved the game",
        "This TRAINER saved the game {STR_VAR_1} times!",
        "You will not find a more careful TRAINER than {STR_VAR_3}."),
    "TrendsStarted": (
        "The Trendsetter", "Started trends",
        "This TRAINER started {STR_VAR_1} new sayings!",
        "What ARAUNA is saying this week, {STR_VAR_3} said first."),
    "BerriesPlanted": (
        "The BERRY Planter", "Planted BERRIES",
        "This TRAINER planted BERRIES {STR_VAR_1} times!",
        "There is not a patch of ground {STR_VAR_3} has left bare."),
    "BikeTrades": (
        "The BIKE Swapper", "Traded BIKES",
        "This TRAINER swapped BIKES {STR_VAR_1} times!",
        "{STR_VAR_3} has never been able to settle on one."),
    "Interviews": (
        "The Interviewed TRAINER", "Got interviewed",
        "This TRAINER was interviewed {STR_VAR_1} times!",
        "The television people know where to find {STR_VAR_3}."),
    "TrainerBattles": (
        "The Tireless Battler", "Battled",
        "This TRAINER battled {STR_VAR_1} times!",
        "{STR_VAR_3} has never once turned a challenge down."),
    "PokemonCaught": (
        "The Great Catcher", "Caught POKéMON",
        "This TRAINER caught {STR_VAR_1} POKéMON!",
        "The wild places of ARAUNA know {STR_VAR_3} by now."),
    "FishingPokemonCaught": (
        "The Patient Angler", "Caught POKéMON with a ROD",
        "This TRAINER landed {STR_VAR_1} POKéMON on a ROD!",
        "{STR_VAR_3} can sit by water longer than anyone living."),
    "EggsHatched": (
        "The EGG Warmer", "Hatched EGGS",
        "This TRAINER brought {STR_VAR_1} POKéMON out of EGGS!",
        "{STR_VAR_3} has more patience than most people have years."),
    "PokemonEvolved": (
        "The Evolver", "Evolved POKéMON",
        "This TRAINER saw {STR_VAR_1} POKéMON change!",
        "{STR_VAR_3} has watched more become something else than anyone."),
    "UsedPokemonCenter": (
        "The CENTRE Regular", "Used POKéMON CENTERS",
        "This TRAINER healed a team {STR_VAR_1} times at POKéMON CENTERS!",
        "There is no counter in ARAUNA that does not know {STR_VAR_3}."),
    "RestedAtHome": (
        "The Homebody", "Rested POKéMON at home",
        "This TRAINER healed a team {STR_VAR_1} times at home!",
        "Whatever the road offers, {STR_VAR_3} still goes home to sleep."),
    "SafariGames": (
        "The RESERVA Walker", "Entered the RESERVA ARAUNA",
        "This TRAINER went into the RESERVA ARAUNA {STR_VAR_1} times!",
        "Something in {STR_VAR_3} only settles inside that fence."),
    "UsedCut": (
        "The Cutter", "Used CUT",
        "This TRAINER used CUT {STR_VAR_1} times!",
        "No branch has ever stood between {STR_VAR_3} and anywhere."),
    "UsedRockSmash": (
        "The Rock Breaker", "Smashed rocks",
        "This TRAINER used ROCK SMASH {STR_VAR_1} times!",
        "{STR_VAR_3} cannot walk past a stone and leave it whole."),
    "MovedBases": (
        "The Restless TRAINER", "Moved the SECRET BASE",
        "This TRAINER moved the SECRET BASE {STR_VAR_1} times!",
        "{STR_VAR_3} has never yet found a spot worth staying in."),
    "UsedSplash": (
        "The SPLASH Enthusiast", "Used SPLASH",
        "This TRAINER used SPLASH {STR_VAR_1} times!",
        "Nobody has ever got so much out of so little as {STR_VAR_3}."),
    "UsedStruggle": (
        "The Tenacious TRAINER", "Resorted to STRUGGLE",
        "This TRAINER had to fall back on STRUGGLE {STR_VAR_1} times!",
        "{STR_VAR_3} does not know how to stop, which is a kind of gift."),
    "SlotJackpots": (
        "The SLOTS Champion", "Won the jackpot on the SLOTS",
        "This TRAINER took the jackpot {STR_VAR_1} times.",
        "The reels have been kind to {STR_VAR_3}, and to almost nobody else."),
    "RouletteWins": (
        "The ROULETTE Champion", "Won at ROULETTE in a row",
        "This TRAINER won at ROULETTE {STR_VAR_1} times in a row.",
        "The ball keeps falling where {STR_VAR_3} said it would."),
    "BattleTowerChallenges": (
        "The TOWER Challenger", "Took the BATTLE TOWER challenge",
        "This TRAINER took the BATTLE TOWER challenge {STR_VAR_1} times!",
        "{STR_VAR_3} keeps going back until the TOWER runs out of floors."),
    "MadePokeblocks": (
        "The Blender", "Made {POKEBLOCK}S",
        "This TRAINER made {STR_VAR_1} {POKEBLOCK}S!",
        "Nobody works a BERRY BLENDER like {STR_VAR_3}."),
    "EnteredContests": (
        "The CONTEST Regular", "Entered CONTESTS",
        "This TRAINER entered CONTESTS {STR_VAR_1} times!",
        "{STR_VAR_3} would rather be looked at than left alone."),
    "WonContests": (
        "The CONTEST Master", "Won CONTESTS",
        "This TRAINER won CONTESTS {STR_VAR_1} times!",
        "The halls of ARAUNA have run out of ribbons for {STR_VAR_3}."),
    "TimesShopped": (
        "The Happy Shopper", "Shopped",
        "This TRAINER bought something {STR_VAR_1} times!",
        "{STR_VAR_3} has never once walked past a counter."),
    "UsedItemFinder": (
        "The Ground Searcher", "Used an ITEMFINDER",
        "This TRAINER used an ITEMFINDER {STR_VAR_1} times!",
        "{STR_VAR_3} is certain there is always one more thing buried."),
    "TimesRained": (
        "The Rain-Soaked TRAINER", "Got rained on",
        "This TRAINER was caught in the rain {STR_VAR_1} times!",
        "The weather of ARAUNA appears to follow {STR_VAR_3} about."),
    "CheckedPokedex": (
        "The Avid POKéDEX Reader", "Checked a POKéDEX",
        "This TRAINER opened a POKéDEX {STR_VAR_1} times!",
        "{STR_VAR_3} reads it the way other people read letters from home."),
    "ReceivedRibbons": (
        "The RIBBON Collector", "Received RIBBONS",
        "This TRAINER was given {STR_VAR_1} RIBBONS!",
        "There is no room left on anything {STR_VAR_3} owns."),
    "LedgesJumped": (
        "The Ledge Jumper", "Jumped down ledges",
        "This TRAINER jumped down {STR_VAR_1} ledges!",
        "If there is a ledge, {STR_VAR_3} is going down it."),
    "TVWatched": (
        "The Devoted Viewer", "Watched TV",
        "This TRAINER watched the television {STR_VAR_1} times!",
        "{STR_VAR_3} has seen every programme ARAUNA makes."),
    "CheckedClock": (
        "The Punctual TRAINER", "Checked the time",
        "This TRAINER checked the time {STR_VAR_1} times!",
        "{STR_VAR_3} has never in life been late for anything."),
    "WonLottery": (
        "The LOTTERY Winner", "Won POKéMON LOTTERIES",
        "This TRAINER won the POKéMON LOTTERY {STR_VAR_1} times!",
        "{STR_VAR_3} must know a great many people to trade with."),
    "UsedDaycare": (
        "The DAY CARE Regular", "Left POKéMON at the DAY CARE",
        "This TRAINER left POKéMON at the DAY CARE {STR_VAR_1} times!",
        "{STR_VAR_3} never lets a POKéMON stand still for long."),
    "RodeCableCar": (
        "The CABLE CAR Rider", "Rode the CABLE CAR",
        "This TRAINER rode the CABLE CAR {STR_VAR_1} times!",
        "{STR_VAR_3} is up and down that mountain more than the car is."),
    "HotSprings": (
        "The Hot Spring Bather", "Bathed in hot springs",
        "This TRAINER got into the hot springs {STR_VAR_1} times!",
        "Whatever else is true of {STR_VAR_3}, the skin is remarkable."),
}

# Multi-word names that must not be split across a line.
WHOLE = ("RESERVA ARAUNA", "POKéMON CENTERS", "BATTLE TOWER", "DAY CARE",
         "CABLE CAR", "BERRY BLENDER", "ROCK SMASH", "SECRET BASE",
         "POKéMON LOTTERY", "POKéDEX")

# Each of the five takes a refusal in his own way. Vanilla gave all five the
# same sentence, which is how you end up with one man in five hats.
HANDWRITTEN: dict[str, tuple[str, ...]] = {
    # -- the TRADER -----------------------------------------------------------
    "WantToTradeDecor": (
        "Hello. I'm the TRADER.",
        "Care to swap decorations with me?",
    ),
    "TraderFeelingTheBlues": (
        "Oh...|And I'd been saving the good ones for somebody like you.",
    ),
    "WeveAlreadyTraded": (
        "But you and I have traded already, you know.",
    ),
    "PickADecorItem": (
        "If you see anything of mine you want, say so.",
    ),
    "YouDontWantAnything": (
        "Nothing at all?|And I thought I had good taste.",
    ),
    "OnceBelongedToPlayerDoYouWantIt": (
        "That one belonged to {STR_VAR_1} once.",
        "Do you want it?",
    ),
    "YouDontHaveAnyDecor": (
        "Ah -- hold on. You haven't a single piece of decoration on you!",
    ),
    "PickTheDecorToTrade": (
        "Right. Pick the one you'll trade me.",
    ),
    "YouDontWantToTrade": (
        "You won't trade with me?|And here I am, being reasonable.",
    ),
    "YouveNoRoomForThis": (
        "You've as many {STR_VAR_2}S as can be stored. There's no room for "
        "this one.",
    ),
    "SoWellTradeTheseDecor": (
        "Right, so -- my {STR_VAR_3} for your {STR_VAR_2}?",
    ),
    "ThatDecorIsInUse": (
        "That one's in use. You can't trade a thing you're standing on.",
    ),
    "SendDecorToYourPC": (
        "Then it's a trade!|I'll send mine to your PC.",
    ),
    "CantTradeThatOne": (
        "Oh -- sorry! That one's genuinely rare.|I can't let that go.",
        "Could I interest you in something else?",
    ),

    # -- the STORYTELLER ------------------------------------------------------
    "WillYouHearMyTale": (
        "I'm the STORYTELLER.|I keep the tales of legendary TRAINERS.",
        "Will you hear one?",
    ),
    "StorytellerFeelingTheBlues": (
        "Oh...|Then the tale keeps, and so do I.",
    ),
    "WhichTaleToTell": (
        "These are the legends I hold.|Which will you have?",
    ),
    "IKnowNoTales": (
        "But I know of no legendary TRAINERS, and so I know no tales.",
        "Where does one find a TRAINER worth telling of?",
    ),
    "CouldThereBeOtherLegends": (
        "It sets me wondering. Might there be others out there with better "
        "legends still, waiting to be found?",
    ),
    "HaveYouAnyLegendaryTales": (
        "Are you a TRAINER?",
        "Then tell me -- have you anything about you that is even faintly "
        "legendary?",
    ),
    "HearAnotherLegendaryTale": (
        "Incidentally -- would you care for another?",
    ),
    "NotWorthyOfLegend": (
        "Hmm...|No. That will not do...",
        "Bring me something a person could reasonably call a legend.",
    ),
    "IWishMorePeopleWereInterested": (
        "I do wish more people wanted to hear about legendary TRAINERS.",
    ),
    "YouDidStatXTimes": (
        "What's that?!|You... You...",
        "{STR_VAR_2}|{STR_VAR_1} time(s)?!",
        "That is magnificent!|A legend is born this afternoon!",
    ),

    # -- GIDDY ----------------------------------------------------------------
    "HearMyStory": (
        "I'm GIDDY!|And I have something remarkable to tell you!",
        "Would you like to hear it?",
    ),
    "GiddyFeelingTheBlues": (
        "Oh...|But it was such a good one, too.",
    ),
    "AlsoIWasThinking": (
        "Also -- I was thinking...",
    ),
    "WeShouldChatAgain": (
        "That's about all of it, I think...",
        "We should do this again!|Bye-bye!",
    ),

    # -- the BARD -------------------------------------------------------------
    "WouldYouLikeToHearMySong": (
        "Hello. I'm the BARD.",
        "Would you like to hear my song?",
    ),
    "BardFeelingTheBlues1": (
        "Oh...|Then I shall play it to the room, as usual.",
    ),
    "WishICouldPlaySongForOthers": (
        "Oh, what a song that is...|I wish I could play it for more than "
        "the walls...",
    ),
    "WouldYouLikeToWriteSomeLyrics": (
        "Well?|What did you make of it?",
        "It's the words I'm not happy with.",
        "How would you like to write me some new ones?",
    ),
    "BardFeelingTheBlues2": (
        "Oh...|Then the words stay as they are, and so do I.",
    ),
    "LetMeSingItForYou": (
        "Thank you kindly!|Let me sing it for you.",
    ),
    "ThatHowYouWantedSongToGo": (
        "Was that how you meant it to go?",
    ),
    "IllSingThisSongForAWhile": (
        "Right! That's settled, then.|I'll be singing this one for a while.",
    ),

    # -- the HIPSTER ----------------------------------------------------------
    "TeachWhatsHipAndHappening": (
        "Hey, yo! They call me the HIPSTER.",
        "I'll teach you what's being said this week.",
    ),
    "IAlreadyTaughtYou": (
        "But, hey -- I taught you that already.",
        "I'd rather get the word out to somebody new.",
    ),
    "IveGotNothingNewToTeach": (
        "But, hey -- you already know what's being said.",
        "I've nothing new for you!",
    ),
    "HaveYouHeardOfWord": (
        "Hey -- have you heard about “{STR_VAR_1}”?",
        "What's it mean? Well...|Ask somebody older than me.",
    ),
}


def build() -> dict[str, tuple[str, ...]]:
    blocks = dict(HANDWRITTEN)
    for key, (title, action, middle, coda) in TALES.items():
        blocks[f"{key}Title"] = (title,)
        blocks[f"{key}Action"] = (action,)
        blocks[f"{key}Story"] = (
            "This is a tale of a TRAINER named {STR_VAR_3}.", middle, coda)
    return blocks


PARAGRAPHS = build()
TARGETS = tuple(PARAGRAPHS)
MENU = tuple(f"{key}{kind}" for key in TALES for kind in ("Title", "Action"))


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(PREFIX + label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def _glue(paragraph: str) -> str:
    for name in WHOLE:
        paragraph = paragraph.replace(name, glued(name))
    return paragraph


def payloads() -> dict[str, tuple[str, ...]]:
    composed = {}
    for label, paragraphs in PARAGRAPHS.items():
        if label in MENU:
            # A menu entry is one line and is never wrapped.
            composed[label] = (paragraphs[0] + "$",)
            continue
        composed[label] = BOX.compose(tuple(_glue(p) for p in paragraphs))
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
        masked = masked[:start] + '\t.string "<ARAUNA_MAUVILLE_MAN_EN>"\n\n' + masked[end:]
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
    ruler = Ruler()

    # The list draws these, and a long one is cut off with nothing to say so.
    for key, (title, action, _, _) in TALES.items():
        if ruler.width(title) > TITLE_CEILING:
            raise ValueError(
                f"{key}: the title is {ruler.width(title)}px, past the "
                f"{TITLE_CEILING}px the list can draw: {title!r}")
        if ruler.width(action) > ACTION_CEILING:
            raise ValueError(
                f"{key}: the menu entry is {ruler.width(action)}px, past the "
                f"{ACTION_CEILING}px the list can draw: {action!r}")

    # Thirty-six tales that say the same thing are one tale told badly.
    for field, index in (("title", 0), ("menu entry", 1), ("closing line", 3)):
        values = [tale[index] for tale in TALES.values()]
        if len(set(values)) != len(values):
            raise ValueError(f"two tales share a {field}")

    # A tale has to name whose it is and how many times, or it is not a tale.
    for key in TALES:
        story = "".join(composed[f"{key}Story"])
        for slot in ("{STR_VAR_1}", "{STR_VAR_3}"):
            if slot not in story:
                raise ValueError(f"{key}: the tale dropped {slot}")

    # Five men, five refusals. Emerald gave them one between them.
    blues = ["TraderFeelingTheBlues", "StorytellerFeelingTheBlues",
             "GiddyFeelingTheBlues", "BardFeelingTheBlues1",
             "BardFeelingTheBlues2"]
    said = ["".join(composed[label]) for label in blues]
    if len(set(said)) != len(said):
        raise ValueError("two of the men take a refusal the same way")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the five men in the ENCRUZILHADA POKéMON CENTER.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = MAN.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        MAN.write_text(rendered, encoding="utf-8")
    print(f"Mauville man English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

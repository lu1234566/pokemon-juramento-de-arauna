#!/usr/bin/env python3
"""POKéMON TODAY, TODAY'S SMART SHOPPER, and THE WORLD OF MASTERS.

POKéMON TODAY is presented by two people who are related to each other and
have never agreed about anything on air. BIG SIS runs the programme; BIG BRO
laughs at the wrong moments. Emerald had them both hooting in the same
register; here the joke is that only one of them thinks it is a joke, and the
episode where a POKéMON gets away is unkind in a way she keeps apologising
for.

SMART SHOPPER is an interviewer who cannot stop bringing the conversation back
around to their own shopping. THE WORLD OF MASTERS is the sober one, and reads
its numbers out like a court record.

The item name in SMART SHOPPER is pluralised in the text as "{STR_VAR_2}S", so
the S has to stay welded to the slot -- a break between them prints a lone S
at the start of a line. The renderer checks it.
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

# An item name is the widest thing the second slot holds.
BOX = TextBox({"{STR_VAR_1}": 12, "{STR_VAR_2}": 14, "{STR_VAR_3}": 12}, width=34)

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- the day it went wrong ------------------------------------------------
    "gTVPokemonTodayFailedText00": (("POKéMON TODAY", "peachy"), (
        "Hello!",
        "It's time for POKéMON TODAY!",
        "BIG SIS: Hello! Is everybody well this evening?",
        "Tonight we look at {STR_VAR_1}'s POKéMON {STR_VAR_2}!",
        "BIG BRO: We are! That's exactly what we're doing!",
    )),
    "gTVPokemonTodayFailedText01": (("with my very", "trying to catch"), (
        "Oh!|Speaking of {STR_VAR_1}...",
        "BIG SIS, I saw that TRAINER with my own eyes!",
        "BIG SIS: Did you? Where?",
        "BIG BRO: Well, I had to go over to {STR_VAR_2}.",
        "And there was {STR_VAR_1}, going after a {STR_VAR_3}, and...",
    )),
    "gTVPokemonTodayFailedText02": (("managed to get away", "frustration"), (
        "It got away!",
        "And it cost this many POKé BALLS: {STR_VAR_2}!",
        "You should have seen {STR_VAR_1}'s face when it went.",
    )),
    "gTVPokemonTodayFailedText03": (("goofed", "stunned dismay"), (
        "But {STR_VAR_1} misjudged it and knocked the POKéMON out!",
        "And it cost this many POKé BALLS: {STR_VAR_2}!",
        "You should have seen {STR_VAR_1}'s face when it fainted.",
    )),
    "gTVPokemonTodayFailedText04": (("not nice", "Sorry for laughing"), (
        "BIG SIS: Now, then!|That isn't kind.",
        "We don't laugh at other people's bad days on this programme.",
        "Poor {STR_VAR_1}.|What a shame.",
        "BIG BRO: You're right.|Sorry. I'm sorry.",
    )),
    "gTVPokemonTodayFailedText05": (("Bufufu", "just laughed"), (
        "BIG SIS: Bufufu...",
        "BIG BRO: Hey!|You just laughed as well!",
        "BIG SIS: What?!",
        "I did no such thing!|I did not!",
        "Poor {STR_VAR_1}.|What a shame.",
        "BIG BRO: ...",
    )),
    "gTVPokemonTodayFailedText06": (("enough silliness", "without me"), (
        "BIG SIS: That's quite enough of that.|Now, tonight's POKéMON...",
        "What?|We're out of time already?",
        "Oh, no!|We never got to it at all!",
        "BIG BRO: See you all next week!",
        "BIG SIS: Don't you end my programme without me!",
    )),

    # -- the day it went right ------------------------------------------------
    "gTVPokemonTodaySuccessfulText00": (("POKéMON TODAY", "peachy"), (
        "Hello!",
        "It's time for POKéMON TODAY!",
        "BIG SIS: Hello! Is everybody well this evening?",
        "Tonight we look at {STR_VAR_1}'s POKéMON {STR_VAR_2}!",
        "BIG BRO: We are! That's exactly what we're doing!",
    )),
    "gTVPokemonTodaySuccessfulText01": (("gave the nickname", "loving care"), (
        "BIG SIS: {STR_VAR_1} named the {STR_VAR_2} {STR_VAR_3}!",
        "And by the sound of it, {STR_VAR_3} is well looked after.",
    )),
    "gTVPokemonTodaySuccessfulText02": (("many POKé BALLS", "single"), (
        "BIG BRO: It took this many POKé BALLS to land it: {STR_VAR_3}!",
        "And in the end one {STR_VAR_2} did it!",
    )),
    "gTVPokemonTodaySuccessfulText03": (("that easy to catch", "destiny"), (
        "BIG SIS: If it came that easily, then {STR_VAR_1} and the "
        "{STR_VAR_2} were always going to find each other!",
    )),
    "gTVPokemonTodaySuccessfulText04": (("so neat", "earns the love"), (
        "BIG SIS: My word! What a thing!",
        "But they do say the one that takes the longest to catch is the one "
        "you end up loving best!",
    )),
    "gTVPokemonTodaySuccessfulText05": (("MASTER BALL", "really"), (
        "BIG SIS: {STR_VAR_1}'s {STR_VAR_2} is a POKéMON to remember, because "
        "it took a MASTER BALL to catch!",
        "BIG BRO: A MASTER BALL! Imagine!",
        "BIG SIS: {STR_VAR_1} wanted that {STR_VAR_2} very badly indeed!",
    )),
    "gTVPokemonTodaySuccessfulText06": (("Then to give the nickname", "second that"), (
        "BIG BRO: And then to call that {STR_VAR_2} {STR_VAR_3}...",
        "That tells you something about how {STR_VAR_1} sees a POKéMON.",
        "BIG SIS: It does. I agree.",
    )),
    "gTVPokemonTodaySuccessfulText07": (("If it were me", "something new"), (
        "If it were up to me, I'd have given that name to something like a "
        "{STR_VAR_3}!",
        "BIG BRO: There you go! That could start something!",
    )),
    "gTVPokemonTodaySuccessfulText08": (("sound perfect", "just right"), (
        "{STR_VAR_2} the {STR_VAR_1}?|Doesn't that sit well?",
        "The sounds of it, the shape of it -- it suits a {STR_VAR_1}!",
        "BIG BRO: It does, at that!",
    )),
    "gTVPokemonTodaySuccessfulText09": (("no TRAINER has ever", "great taste"), (
        "As far as I know, nobody has ever named a {STR_VAR_1} {STR_VAR_2} "
        "before!",
        "BIG BRO: Which tells you what an ear that TRAINER has for a name!",
    )),
    "gTVPokemonTodaySuccessfulText10": (("next time I catch", "too"), (
        "The next one I catch, I shall call {STR_VAR_2}.",
        "BIG BRO: What? So shall I!|I'm using {STR_VAR_2} as well!",
    )),
    "gTVPokemonTodaySuccessfulText11": (("Look at the time", "spotlight"), (
        "BIG SIS: Oh, no!|Look at the time!",
        "Well, that's us for tonight.|See you all next week!",
        "BIG BRO: And remember -- it could be your POKéMON up here next time!",
    )),

    # -- the shopping programme -----------------------------------------------
    "SmartShopper_Text_Intro": (("SMART SHOPPER", "hot sellers"), (
        "Hello!",
        "It's time for TODAY'S SMART SHOPPER.",
        "INTERVIEWER: And how are you all this evening?",
        "Tonight we're at a shop in {STR_VAR_2}.",
        "Let's see what's been going out of the door.",
    )),
    "SmartShopper_Text_ClerkNormal": (("interview the clerk", "doing excellent"), (
        "Let's have a word with whoever's behind the counter.",
        "Hello! How's trade?",
        "CLERK: Oh, we can't complain.",
        "Lately it's been {STR_VAR_2} going out more than anything.",
        "Only the other day a TRAINER called {STR_VAR_1} took {STR_VAR_3}.",
    )),
    "SmartShopper_Text_RandomComment1": (("That's a haul", "so"), (
        "INTERVIEWER: {STR_VAR_3} {STR_VAR_2}S? That is a load!",
        "If I may say so, {STR_VAR_1} must be stocking up for somewhere far "
        "off.",
        "And for travelling, you cannot have too many {STR_VAR_2}S!",
    )),
    "SmartShopper_Text_RandomComment2": (("Speaking of the item", "great item"), (
        "INTERVIEWER: Funny you should mention {STR_VAR_2} -- I bought "
        "{STR_VAR_3} of them myself not long ago.",
        "It's a good thing to have about, {STR_VAR_2}.",
    )),
    "SmartShopper_Text_RandomComment3": (("But", "one or"), (
        "INTERVIEWER: {STR_VAR_2}?!|And {STR_VAR_3} of them?!",
        "I didn't think anyone bought that many at once.",
        "Goodness. I manage one or two at a time...",
    )),
    "SmartShopper_Text_RandomComment4": (("too many", "no point talking about me"), (
        "INTERVIEWER: I bought a great pile of {STR_VAR_2} once.",
        "And it was far too many.|I regretted it for months...",
        "I've bought only what I need ever since...",
        "Oops!",
        "Nobody wants to hear about me!",
    )),
    "SmartShopper_Text_SecondItem": (("also bought the item", "very good item"), (
        "CLERK: {STR_VAR_1} took {STR_VAR_3} of the {STR_VAR_2} as well.",
        "INTERVIEWER: Sensible.|{STR_VAR_2} is a good thing to have too.",
    )),
    "SmartShopper_Text_ThirdItem": (("also bought",), (
        "CLERK: And {STR_VAR_3} of the {STR_VAR_2} on top of that.",
    )),
    "SmartShopper_Text_DuringSale": (("big sale", "smart shopping"), (
        "CLERK: And all of it in the sale.|That is shopping well.",
    )),
    "SmartShopper_Text_OutroNormal": (("bargain hunter", "out of time"), (
        "INTERVIEWER: Hmm... {STR_VAR_1} knows the value of a thing!",
        "All told, {STR_VAR_1} spent...",
        "¥{STR_VAR_2}?!|What a sum!",
        "Oops! We're out of time!|Until the next one!",
    )),
    "SmartShopper_Text_IsVIP": (("VIP customer",), (
        "CLERK: {STR_VAR_1} is one of our best customers, no question.",
    )),
    "SmartShopper_Text_ClerkMax": (("unbelievable", "VIP customer"), (
        "Let's have a word with whoever's behind the counter.",
        "Hello! How's trade?",
        "CLERK: Oh, extraordinary. Almost more than we can manage.",
        "Lately a TRAINER called {STR_VAR_1} has been taking {STR_VAR_2} by "
        "the armful.",
        "Very nearly cleared us out of {STR_VAR_2}S.",
        "I never thought anybody would want that many {STR_VAR_2}S. I've "
        "never seen it.",
        "INTERVIEWER: So a hundred? Two hundred?",
        "CLERK: Oh, a good deal more than that.",
        "INTERVIEWER: Good heavens!|{STR_VAR_1} is a shopper apart!",
        "CLERK: {STR_VAR_1} is one of our best customers, no question.",
    )),
    "SmartShopper_Text_OutroMax": (("mystery deepens", "enigma"), (
        "INTERVIEWER: Hmm...|That is a remarkable thing.",
        "But whatever does the TRAINER need them all for?",
        "... ...",
        "The question stands, and our time does not.|Until the next one!",
        "Still. {STR_VAR_1} is a puzzle...",
    )),

    # -- the sober one --------------------------------------------------------
    "gTVWorldOfMastersText00": (("THE WORLD OF MASTERS", "on foot"), (
        "THE WORLD OF MASTERS",
        "Good evening.",
        "You may know of a TRAINER called {STR_VAR_1}.",
        "{STR_VAR_1} is known as a master of catching POKéMON.",
        "And {STR_VAR_1} does it entirely on foot, by looking carefully.",
        "On one day worth recording, the TRAINER walked {STR_VAR_2} steps.",
        "And caught, that day, {STR_VAR_3} POKéMON.",
    )),
    "gTVWorldOfMastersText01": (("remarkable feat", "trust between"), (
        "A day like that is only possible where there is trust between a "
        "TRAINER and {STR_VAR_1}.",
    )),
    "gTVWorldOfMastersText02": (("last", "challenge this fine record"), (
        "The last of them, a {STR_VAR_3}, was caught near {STR_VAR_2}.",
        "That POKéMON now stands in the record.",
        "Any TRAINER who thinks they can better it is welcome to try.",
        "That is all for tonight.|Do join us again.",
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
        masked = masked[:start] + '\t.string "<ARAUNA_TV_POKEMON_TODAY_EN>"\n\n' + masked[end:]
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

    # A plural is made by welding an S to the slot. Break the line between them
    # and a lone S starts the next one.
    for label, payloads_ in payloads().items():
        for payload in payloads_:
            if re.search(r"\{STR_VAR_\d\}\s*\\[npl]\s*$", payload) and payload.endswith(
                    ("S\\n", "S\\l", "S\\p")):
                raise ValueError(f"{label}: a plural S came away from its slot")
        joined = "".join(payloads_)
        if re.search(r"\{STR_VAR_\d\}\\[npl]S\b", joined):
            raise ValueError(f"{label}: a plural S came away from its slot")

    # The two presenters have to stay two people.
    for label in TARGETS:
        if not label.startswith("gTVPokemonToday"):
            continue
        body = block_pattern(label).search(rendered).group("body")
        if "BIG SIS" in body and "BIG SIS:" not in body:
            raise ValueError(f"{label}: BIG SIS is named but never speaks")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render POKéMON TODAY, SMART SHOPPER and WORLD OF MASTERS.")
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
    print(f"TV Pokemon Today English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

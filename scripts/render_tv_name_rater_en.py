#!/usr/bin/env python3
"""The TRAINER FAN CLUB special, THE NAME RATER SHOW, and the fishing programme.

Three shows and the fan who stops you in the club to ask what you make of
somebody. The fan's answers become the special that airs later, so the two
have to sound like the same week of television.

THE NAME RATER SHOW is the delicate one. Its host reads a nickname the way a
fortune teller reads a palm, and the engine hands him the pieces to read: a
whole nickname in one slot, single letters out of it in others, and in four
blocks a nickname assembled by butting two slots together --
{STR_VAR_2}{STR_VAR_3} is one word, not two. Put a space or a line break
between them and the show starts recommending nicknames that do not exist, so
the renderer checks that every such pair is still touching.

The fishing programme has two hosts who disagree about what patience is.
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

BOX = TextBox({"{STR_VAR_1}": 12, "{STR_VAR_2}": 12, "{STR_VAR_3}": 12}, width=34)

# The blocks where two slots are butted together to make one nickname.
GLUED = ("gTVNameRaterText13", "gTVNameRaterText14",
         "gTVNameRaterText15", "gTVNameRaterText16",
         "gTVNameRaterText17")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- the fan in the club --------------------------------------------------
    "LilycoveCity_PokemonTrainerFanClub_Text_WhatsYourOpinionOfTrainer": (
        ("big fan", "opinion"), (
            "Hello there!",
            "I'm a great admirer of {STR_VAR_1}.|What do you make of "
            "{STR_VAR_1}?",
        )),
    "LilycoveCity_PokemonTrainerFanClub_Text_ThatsWhatYouThink": (
        ("That's what you think",), (
            "I see, I see. So that's how you find the TRAINER.",
        )),
    "LilycoveCity_PokemonTrainerFanClub_Text_HaveYouForgottenTrainer": (
        ("forgotten",), (
            "Have you gone and forgotten {STR_VAR_1} entirely?",
        )),
    "LilycoveCity_PokemonTrainerFanClub_Text_WhatsYourOpinionOfTrainer2": (
        ("big fan", "opinion"), (
            "I'm a great admirer of {STR_VAR_1}.|What do you make of "
            "{STR_VAR_1}?",
        )),
    "LilycoveCity_PokemonTrainerFanClub_Text_HowStrongRateTrainer": (
        ("How strong", "one hundred"), (
            "And how strong would you call {STR_VAR_1}, out of a hundred?",
        )),
    "LilycoveCity_PokemonTrainerFanClub_Text_HaveYouForgottenTrainer2": (
        ("forgotten",), (
            "Have you gone and forgotten {STR_VAR_1} entirely?",
        )),
    "LilycoveCity_PokemonTrainerFanClub_Text_YouShouldMeetTrainer": (
        ("You should meet", "become a fan"), (
            "Oh, I see!",
            "You ought to meet {STR_VAR_1} one day.|You'd come away an "
            "admirer as well, I'm sure of it!",
        )),
    "LilycoveCity_PokemonTrainerFanClub_Text_ThankYouIllShareThisInfo": (
        ("useful to know", "fans and discuss"), (
            "I see, I see.",
            "Thank you!|That is worth knowing.",
            "I shall put it to the other {STR_VAR_1} people and see what they "
            "say.",
        )),
    "LilycoveCity_PokemonTrainerFanClub_HopeYouCatchTVSpecial": (
        ("TV special", "catch it"), (
            "There's to be a programme about {STR_VAR_1} shortly.",
            "Do watch it!",
        )),

    # -- the special that comes of it -----------------------------------------
    "gTVTrainerFanClubSpecialText00": (("SPECIAL", "representative"), (
        "TRAINER FAN CLUB|{STR_VAR_1} SPECIAL!",
        "This one is for everyone in ARAUNA who follows {STR_VAR_1}.",
        "Tonight we ask: what do people make of {STR_VAR_1}?",
        "We put it to {STR_VAR_2}, speaking for the TRAINERS.",
        "We asked: “In one word -- what is {STR_VAR_1}?”",
        "The answer: “{STR_VAR_3}.”",
        "Well said, {STR_VAR_2}!|That is seeing clearly!",
        "“{STR_VAR_3} {STR_VAR_1}.”|It has a ring to it, that!",
        "{STR_VAR_2} also put a number on {STR_VAR_1}'s strength, from nought "
        "to a hundred.",
    )),
    "gTVTrainerFanClubSpecialText01": (("very high score", "esteem"), (
        "{STR_VAR_3} points!|That is a very high mark indeed.",
        "{STR_VAR_2} plainly thinks the world of {STR_VAR_1}.",
    )),
    "gTVTrainerFanClubSpecialText02": (("quite a good score", "rival"), (
        "{STR_VAR_3} points!|A respectable mark, that.",
        "{STR_VAR_2} must count {STR_VAR_1} a rival.",
    )),
    "gTVTrainerFanClubSpecialText03": (("weak score", "sidekick"), (
        "{STR_VAR_3} points!|A thin mark, I'm afraid.",
        "{STR_VAR_2} seems to think of {STR_VAR_1} as somebody who tags "
        "along.",
    )),
    "gTVTrainerFanClubSpecialText04": (("terrible score", "underling"), (
        "{STR_VAR_3} point(s)!|A dreadful mark.",
        "{STR_VAR_2} seems to think of {STR_VAR_1} as somebody to be sent on "
        "errands.",
    )),
    "gTVTrainerFanClubSpecialText05": (("There you have it", "In closing"), (
        "There you have it.",
        "I think we all know {STR_VAR_1} a little better tonight.",
        "And I'll leave you with {STR_VAR_2}'s word for it.",
        "{STR_VAR_3} {STR_VAR_1}!",
    )),

    # -- the nickname reading -------------------------------------------------
    "gTVNameRaterText00": (("NAME RATER SHOW", "reading of"), (
        "And now it is time for...|THE NAME RATER SHOW.",
        "I read a POKéMON's fortune out of the name its TRAINER chose for it.",
        "Advice is what I have to offer, and it is good advice.",
        "Tonight I read the name {STR_VAR_3}, given by {STR_VAR_1} to the "
        "POKéMON {STR_VAR_2}.",
        "Hmhm...",
        "Hmm...|This name is...",
    )),
    "gTVNameRaterText01": (("talent in many", "take courage"), (
        "A name that points at more than one gift.",
        "This TRAINER should take heart and take on a great deal.",
    )),
    "gTVNameRaterText02": (("complements", "precise timing"), (
        "A name that sits perfectly beside {STR_VAR_1}, the TRAINER's own.",
        "The two of them will keep time together.",
    )),
    "gTVNameRaterText03": (("unique individual", "bloom"), (
        "A name for a POKéMON that is like no other!",
        "Raised properly, whatever is odd in it will flower.",
    )),
    "gTVNameRaterText04": (("caring", "warmth"), (
        "A name that will bring out the gentler side of a POKéMON.",
        "Raised properly, this one will be warm to be near.",
    )),
    "gTVNameRaterText05": (("greatness to come", "future"), (
        "A very fine name, and one that points forward.",
        "I am curious about what becomes of this POKéMON.",
    )),
    "gTVNameRaterText06": (("hale and hearty", "robust"), (
        "A good name, and a healthy one!",
        "This POKéMON should stay sound for a long time yet.",
    )),
    "gTVNameRaterText07": (("very active", "battles"), (
        "A good name, and a lively one!",
        "I should expect this POKéMON to be a hard one to beat.",
    )),
    "gTVNameRaterText08": (("charming", "CONTESTS"), (
        "An appealing name, and it will make its POKéMON appealing!",
        "I don't doubt this one will charm the CONTESTS.",
    )),
    "gTVNameRaterText09": (("rooted by", "solid sense"), (
        "The name {STR_VAR_1} is rooted in the letter “{STR_VAR_3}.”",
        "And that letter stands on the first letter, “{STR_VAR_2},” which "
        "gives the whole thing its footing.",
    )),
    "gTVNameRaterText10": (("shapely", "remarkably good"), (
        "The name {STR_VAR_1} has a pleasing shape to it.",
        "Having both “{STR_VAR_2}” and “{STR_VAR_3}” in it -- now that is a "
        "fine thing.",
    )),
    "gTVNameRaterText11": (("flowing feel", "especially wonderful"), (
        "The name {STR_VAR_1} -- there is a flow to it.",
        "The run from “{STR_VAR_2}” at the front through to “{STR_VAR_3}” is "
        "the best of it.",
    )),
    "gTVNameRaterText12": (("other examples",), (
        "Shall we look at some other good names?",
    )),
    "gTVNameRaterText13": (("Take a part of the", "fine nickname"), (
        "Try this. Take a piece of the TRAINER's own name, {STR_VAR_1}, and "
        "you arrive at {STR_VAR_2}{STR_VAR_3}.",
    )),
    "gTVNameRaterText14": (("would also work",), (
        "{STR_VAR_2}{STR_VAR_3} would serve just as well.",
    )),
    "gTVNameRaterText15": (("species name", "basis"), (
        "Or take the POKéMON's own kind, {STR_VAR_2}, and build "
        "{STR_VAR_1}{STR_VAR_3} out of that.",
    )),
    "gTVNameRaterText16": (("effective",), (
        "{STR_VAR_1}{STR_VAR_3} would do the job too.",
    )),
    "gTVNameRaterText17": (("always be avoided", "unacceptable"), (
        "What must never be done is to use another POKéMON's kind as a name.",
        "Do not, for instance, take {STR_VAR_2} and make "
        "{STR_VAR_1}{STR_VAR_3} of it.|That will not do.",
    )),
    "gTVNameRaterText18": (("quite", "May we meet again"), (
        "I will say that {STR_VAR_1} is a good name.",
        "I hope the TRAINER goes on treating {STR_VAR_1} kindly.",
        "That is all for tonight.|May we meet again.",
    )),

    # -- the fishing programme ------------------------------------------------
    "gTVPokemonAnglerText00": (("be patient", "good fishing"), (
        "{STR_VAR_2} ANGLER",
        "ANNOUNCER: Good evening! Tonight, how to fish for {STR_VAR_2}.",
        "GURU, what would you tell someone after {STR_VAR_2}?",
        "GURU: Hm? {STR_VAR_2}, is it?|Then I'll tell you: wait. Wait, and "
        "keep waiting. That's the whole of it.",
        "See {STR_VAR_1} over there?|There's your lesson.",
        "That TRAINER has already had {STR_VAR_3} of them get away.",
        "And there {STR_VAR_1} still sits. That is the law of {STR_VAR_2}.",
        "ANNOUNCER: I see...",
        "Oh! {STR_VAR_1} has landed one at last!",
        "The TRAINER looks close to tears with it!",
        "Watching that face, I've a mind to go fishing myself!",
        "Viewers -- why not take this as your cue to go after some "
        "{STR_VAR_2}?",
        "Until next time: good fishing to you all!",
    )),
    "gTVPokemonAnglerText01": (("vigor", "good fishing"), (
        "{STR_VAR_2} ANGLER",
        "ANNOUNCER: Good evening! Tonight, how to fish for {STR_VAR_2}.",
        "GURU, what would you tell someone after {STR_VAR_2}?",
        "GURU: Hm? {STR_VAR_2}, is it?|Then work the ROD, and work it hard!",
        "See {STR_VAR_1} over there?|Watch how that ROD is handled.",
        "That TRAINER has taken {STR_VAR_3} on the trot.",
        "ANNOUNCER: It's extraordinary!|It's like weather coming in...",
        "Watching work of that order, I've a mind to go fishing myself.",
        "Viewers -- why not take this as your cue to go after some "
        "{STR_VAR_2}?",
        "Until next time: good fishing to you all!",
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
        masked = masked[:start] + '\t.string "<ARAUNA_TV_NAME_RATER_EN>"\n\n' + masked[end:]
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

    # A nickname built by butting two slots together is one word. Anything
    # between them -- a space, a line break -- and the show recommends names
    # that do not exist.
    glued = re.compile(r"\{STR_VAR_\d\}\{STR_VAR_\d\}")
    for label in GLUED:
        body = block_pattern(label).search(rendered).group("body")
        if not glued.search(body):
            raise ValueError(f"{label}: the two halves of the nickname came apart")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the fan club special, the name rater and the angler.")
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
    print(f"TV Name Rater English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

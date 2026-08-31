#!/usr/bin/env python3
"""The shouting show, the letters show, and three more that share their studio.

POKéMON FAN CLUB has a presenter who reads other people's feelings out at
volume; RECENT HAPPENINGS has one who treats a trainer's week as literature;
3 CHEERS FOR POKéBLOCKS has one who feeds the results to Latinha and reports
what she thinks of them. Between them sits the reporter in the museum who
collects the stories the first two broadcast.

They were all Emerald's, and Emerald wrote them as one voice with three hats.
They are separated here: the shouter shouts, the storyteller narrates, and the
food presenter is polite about a bad batch in the way food presenters are.

Latinha keeps her name -- she is the hack's own, and the audience knows her.

The slots are the engine's, not a choice. An easy-chat phrase, a nickname, a
species and a map name each land in a particular one per block, so the
renderer reads which slots a block is given and refuses any it is not.
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

BOX = TextBox({"{STR_VAR_1}": 14, "{STR_VAR_2}": 14, "{STR_VAR_3}": 14,
               "{POKEBLOCK}": 9}, width=34)

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- the shouting show ----------------------------------------------------
    "gTVFanClubOpinionsText00": (("WE ARE THE POKéMON FAN CLUB", "Let's shout"), (
        "WE ARE THE POKéMON FAN CLUB!",
        "And we are on the air!",
        "On this programme you give us your feelings, and I give them back at "
        "volume. Is that not a fine idea for a programme?",
        "Tonight, a report from the FAN CLUB itself.",
        "So who is tonight's devoted fan?",
        "... ... ... ... ... ...",
        "{STR_VAR_1}!",
        "Let us hear what {STR_VAR_1} has to say about {STR_VAR_3} the "
        "{STR_VAR_2}.",
        "And I shall shout every word of it!",
        "Hoo-hah!",
        "Let's shout!",
    )),
    "gTVFanClubOpinionsText01": (("first", "initial thought"), (
        "We asked {STR_VAR_1}: “The first time you laid eyes on your "
        "{STR_VAR_2} -- what went through your head?”",
        "“{STR_VAR_3}!”",
        "Yeahah! Now that is a shout!",
        "Doesn't it take you back?",
    )),
    "gTVFanClubOpinionsText02": (("liken your", "original idea"), (
        "We asked {STR_VAR_1}: “If you had to say what your {STR_VAR_2} is "
        "like, you'd say...”",
        "... ... ... ... ... ...",
        "“{STR_VAR_3}!”",
        "Whoah! Nobody has ever said that before!",
        "You can feel what that TRAINER feels for {STR_VAR_2}.",
    )),
    "gTVFanClubOpinionsText03": (("so attracted", "loud and clear"), (
        "And what was it about that {STR_VAR_2} that took hold of {STR_VAR_1} "
        "in the first place?",
        "... ... ... ... ... ...",
        "“{STR_VAR_3}!”",
        "Whoa! Say it again!",
        "That love comes through clear as a bell!",
    )),
    "gTVFanClubOpinionsText04": (("there's still more", "one last shout"), (
        "Hm? There's more.|Let's have it!",
        "Now, let me see...",
        "We asked {STR_VAR_1}: “What do POKéMON mean to you?”",
        "... ... ... ... ...",
        "“{STR_VAR_3}!”",
        "Bravo!",
        "That is the best shout I have had all day!",
        "“{STR_VAR_3}!”",
        "It makes you want to say it over and over!",
        "And on a shout like that, it's time to leave you.",
        "So -- one more, everyone. All together...",
        "“{STR_VAR_3}!”",
    )),

    # -- the letters show -----------------------------------------------------
    "gTVFanClubText00": (("SURVEY CORNER", "beloved"), (
        "WE ARE THE POKéMON FAN CLUB!",
        "And we are on the air!",
        "We begin tonight with the POSTBAG.",
        "Of all the things that pass between POKéMON and TRAINERS, what has "
        "reached us this week?",
        "Let me see...",
        "This one!",
        "We'll start with this letter!",
        "It is from {STR_VAR_1}, and it is about a beloved {STR_VAR_2}.",
        "Let us see how well our writer can say what that {STR_VAR_2} means. "
        "Hmhm...",
    )),
    "gTVFanClubText01": (("amazing letter",), (
        "Whoah!|What a letter!",
    )),
    "gTVFanClubText02": (("here it is again",), (
        "I liked it so much, here it is again!",
    )),
    "gTVFanClubText03": (("over",), (
        "A good letter will stand being read twice!",
    )),
    "gTVFanClubText04": (("accentuates", "heartfelt"), (
        "That bit -- “{STR_VAR_3}” -- that is where it lands!",
        "There is real feeling under this one!",
    )),
    "gTVFanClubText05": (("Especially", "I love how"), (
        "That “{STR_VAR_3}” especially!",
        "What a way to use “{STR_VAR_3}”!",
    )),
    "gTVFanClubText06": (("not important", "conversations"), (
        "And this is neither here nor there, but “{STR_VAR_3}” is a fine "
        "thing to say.",
        "I have been working “{STR_VAR_3}” into conversation all week.",
    )),
    "gTVFanClubText07": (("score this letter", "look at the time"), (
        "If I had to put a number on this letter, I'd give it {STR_VAR_3}.",
        "And next time I shall want a better one, {STR_VAR_1}!",
        "A-whoops -- look at the time!|Until next week, then!",
    )),

    # -- the reporter who collects the stories --------------------------------
    "SlateportCity_OceanicMuseum_1F_Text_InterviewRequest": (
        ("Do you perhaps like", "something about yourself"), (
            "Oh?|Would I be right that you're fond of POKéMON?",
            "I'm here on assignment for the television.",
            "I'm collecting things that have happened lately between POKéMON "
            "and TRAINERS.",
            "If you don't mind -- would you tell me something of yours?",
        )),
    "SlateportCity_OceanicMuseum_1F_Text_InterviewRequestShort": (
        ("gathering stories", "something about yourself"), (
            "I'm collecting things that have happened lately between POKéMON "
            "and TRAINERS.",
            "If you don't mind -- would you tell me something of yours?",
        )),
    "SlateportCity_OceanicMuseum_1F_Text_TellMeExperienceInvolvingPokemon": (
        ("Oh, you will?", "involving POKéMON"), (
            "Oh, you will?|Thank you!",
            "Then tell me anything worth telling that has happened to you "
            "lately with POKéMON in it.",
        )),
    "SlateportCity_OceanicMuseum_1F_Text_LetMeKnowIfYouHaveStory": (
        ("interesting", "let me know"), (
            "Oh. I see...",
            "Well -- if you ever do have something worth telling, come and "
            "find me.",
        )),
    "SlateportCity_OceanicMuseum_1F_Text_ThatsAllForInterview": (
        ("uplifting story", "look forward to it"), (
            "Oh, what a thing to hear!",
            "I'll see this told on the television.",
            "It should go out one of these evenings. Do watch for it.",
        )),
    "SlateportCity_OceanicMuseum_1F_Text_BetterWriteUpStory": (
        ("write it up",), (
            "Hmmm...|Now that is a story for a programme.",
            "I had better write it up before I lose it!",
        )),

    # -- the storyteller ------------------------------------------------------
    "gTVRecentHappeningsText00": (("RECENT HAPPENINGS", "Let's find out"), (
        "Good evening. It's time for RECENT HAPPENINGS.",
        "For a TRAINER, every day has a story in it somewhere.",
        "What we do here is find those stories and hand them to you.",
        "Tonight, the story of the TRAINER {STR_VAR_1}.",
        "What has happened to {STR_VAR_1} lately? Let's find out.",
        "Let's see...",
    )),
    "gTVRecentHappeningsText01": (("enlightening", "witnesses"), (
        "Wasn't that something?",
        "You come away knowing what {STR_VAR_1} has been through this week. "
        "As though we had stood there and watched it.",
    )),
    "gTVRecentHappeningsText02": (("accents the tale",), (
        "“{STR_VAR_3}.” That is the line that gives the thing its weight.",
    )),
    "gTVRecentHappeningsText03": (("sense of place",), (
        "“{STR_VAR_3}.”|That puts you somewhere. You can see where it "
        "happened.",
    )),
    "gTVRecentHappeningsText04": (("expressive",), (
        "The “{STR_VAR_3}” part of it says a great deal.",
    )),
    "gTVRecentHappeningsText05": (("indelibly", "tune in next time"), (
        "{STR_VAR_1} has told us a fine thing about POKéMON.",
        "And now {STR_VAR_1}'s story is in you as well, and will stay there.",
        "That's all for tonight.|Do join us again.",
    )),

    # -- the news bulletin about an outbreak ----------------------------------
    "gTVMassOutbreakText00": (("mass", "rare opportunity"), (
        "Good evening.|It's time for POKéMON NEWS.",
        "Word has just reached us of something out of the ordinary.",
        "There are reports of a great many {STR_VAR_2} around {STR_VAR_1}.",
        "{STR_VAR_2}, as you will know, is not a POKéMON one comes across "
        "often.",
        "It sounds like a chance worth taking, to see so many of them in the "
        "wild at once.",
        "That has been POKéMON NEWS.",
    )),

    # -- the food programme ---------------------------------------------------
    "gTV3CheersForPokeblocksText00": (("3 CHEERS FOR", "gourmet"), (
        "MC: We hope you're in good cheer -- “3 CHEERS FOR {POKEBLOCK}S” is "
        "here!",
        "Tonight we look at the {POKEBLOCK} blended by {STR_VAR_1} and "
        "company.",
        "And without further ado, I shall give it to Latinha, who knows.",
        "... ... ... ... ...|... ... ... ... ...",
    )),
    "gTV3CheersForPokeblocksText01": (("Gubi", "Thank you so much"), (
        "Latinha: Gubi! Gubii!",
        "MC: And the verdict is very {STR_VAR_1}!|Latinha says it tastes "
        "“{STR_VAR_2}!”",
        "Thank you kindly, {STR_VAR_3}!",
    )),
    "gTV3CheersForPokeblocksText02": (("left something to be desired", "tastier"), (
        "{STR_VAR_1}'s work at the blender left a little to be wanted.",
        "With a steadier hand, this {POKEBLOCK} would have been a good deal "
        "better.",
    )),
    "gTV3CheersForPokeblocksText03": (("too", "hurt the blending"), (
        "Latinha: Gubi! Gubii!",
        "MC: Hmm... It's too {STR_VAR_1}.|Latinha says it tastes "
        "“{STR_VAR_2}!”",
        "{STR_VAR_3}'s slips have told on it, I'm afraid...",
    )),
    "gTV3CheersForPokeblocksText04": (("went to waste", "better showing"), (
        "A shame that {STR_VAR_1}'s good work came to nothing.",
        "Let's hope {STR_VAR_2} does better by it next time!",
    )),
    "gTV3CheersForPokeblocksText05": (("Tune in next time", "slogan"), (
        "Join us next time!|Our slogan: “3 CHEERS FOR {POKEBLOCK}S!”",
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
        masked = masked[:start] + '\t.string "<ARAUNA_TV_FAN_CLUB_EN>"\n\n' + masked[end:]
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

    # The presenter's POKéMON is named on air and has to keep the name the
    # rest of the hack gives her.
    for label in ("gTV3CheersForPokeblocksText00", "gTV3CheersForPokeblocksText01",
                  "gTV3CheersForPokeblocksText03"):
        if "Latinha" not in "".join(payloads()[label]):
            raise ValueError(f"{label}: the gourmet POKéMON lost her name")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the FAN CLUB, RECENT HAPPENINGS and POKéBLOCK broadcasts.")
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
    print(f"TV Fan Club English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

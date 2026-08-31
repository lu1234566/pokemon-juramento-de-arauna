#!/usr/bin/env python3
"""SECRET BASE VISIT, the lottery report, the battle seminar and the fan club.

The base visitor is a critic. He arrives at somebody's hideout, reads the
furniture as though it were an exhibition, then challenges the owner and
loses, and says so on air. Emerald gave him one exclamation to cover awe,
alarm and defeat; here his four openings are four different noises, because
which one he makes is the only thing that tells you how the battle went.

THE POKéMON BATTLE SEMINAR is the one to be careful with. Four of its blocks
are not sentences -- the engine prints them end to end, so
"...the TRAINER's {STR_VAR_1} also knew" is finished by whichever of the next
three fires: "the moves A, B and C." Put a full stop on the first, or a
capital on the others, and the seminar starts speaking in fragments. The
renderer checks the seam.

The lottery report is read from the floor of the BAIA DAS LUZES department
store, and the store gets its due -- that broadcast is an advertisement and
knows it.
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

# Decoration and move names both land in these slots.
BOX = TextBox({"{STR_VAR_1}": 14, "{STR_VAR_2}": 14, "{STR_VAR_3}": 14}, width=34)

# The block that stops mid-sentence, and the three that may finish it.
SEAM_OPENER = "gTVThePokemonBattleSeminarText02"
SEAM_CLOSERS = ("gTVThePokemonBattleSeminarText03",
                "gTVThePokemonBattleSeminarText04",
                "gTVThePokemonBattleSeminarText05")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    # -- the visitor ----------------------------------------------------------
    "gTVSecretBaseVisitText00": (("SECRET BASE VISIT", "personalized"), (
        "Hello, everyone!|It is time once again for a SECRET BASE VISIT.",
        "Tonight we call on the SECRET BASE of {STR_VAR_1}.",
        "What has {STR_VAR_1} made of the place?",
        "Let's find out!|... ... ... ... ...",
    )),
    "gTVSecretBaseVisitText01": (("How marvelous", "expect to"), (
        "Oh!|How very fine!",
        "This {STR_VAR_2}...|One does not expect to meet that in here!",
    )),
    "gTVSecretBaseVisitText02": (("isn't a single piece", "My hat's off"), (
        "Oh!|How very daring!",
        "Not one piece of furniture. Not one ornament.",
        "Most of us would not have the nerve to leave a room like this!",
        "It is plain, and it is wild with it!",
        "My hat is off to you, {STR_VAR_1}.|It could only have been you!",
    )),
    "gTVSecretBaseVisitText03": (("With perfect clarity", "effective message"), (
        "Oh! I see it!|I see it perfectly!",
        "This {STR_VAR_2}, standing just here...|It says something, and says "
        "it well!",
    )),
    "gTVSecretBaseVisitText04": (("deliberately", "effective message"), (
        "Oh! I see it!|I see it perfectly!",
        "This corner has been kept clear on purpose!",
        "It says something, and says it well!",
    )),
    "gTVSecretBaseVisitText05": (("pairing", "dream combination"), (
        "Wheeew!",
        "The {STR_VAR_2} set beside the {STR_VAR_3}!",
        "If ever two things belonged together, it is those!",
    )),
    "gTVSecretBaseVisitText06": (("placement", "presence"), (
        "Wheeew!",
        "This {STR_VAR_2}, put exactly there...",
        "You can feel it from every corner of the SECRET BASE!",
    )),
    "gTVSecretBaseVisitText07": (("nothing in place", "empty space"), (
        "Wheeew!",
        "There is nothing here at all.",
        "And the emptiness works on the whole SECRET BASE.",
    )),
    "gTVSecretBaseVisitText08": (("Here comes", "challenge the TRAINER"), (
        "Oh!|Here comes {STR_VAR_1}!|Let's give the TRAINER a battle!",
        "... ... ... ... ...|... ... ... ... ...",
    )),
    "gTVSecretBaseVisitText09": (("CHAMPION's title", "quite a lesson"), (
        "Sigh...|I take my hat off to {STR_VAR_1}.",
        "Those POKéMON would not have shamed a CHAMPION.",
        "They are proof enough of how hard {STR_VAR_1} is to beat.",
        "And that the {STR_VAR_2} knew {STR_VAR_3}...",
        "That tells you the kind of TRAINER {STR_VAR_1} is.",
        "It was a lesson, and I have learned it!",
    )),
    "gTVSecretBaseVisitText10": (("Aiyeeh", "tenacity"), (
        "Aiyeeh!|I take my hat off to {STR_VAR_1}.",
        "Those POKéMON were frightening things!",
        "They are proof enough of how stubborn {STR_VAR_1} is.",
        "And that the {STR_VAR_2} knew {STR_VAR_3}...",
        "That tells you the kind of TRAINER {STR_VAR_1} is.",
        "It was a lesson, and I have learned it!",
    )),
    "gTVSecretBaseVisitText11": (("well-balanced", "thoughtfulness"), (
        "Wheeew!|I take my hat off to {STR_VAR_1}.",
        "Those POKéMON have been brought on evenly, every one of them.",
        "They are proof enough of how carefully {STR_VAR_1} works.",
        "And that the {STR_VAR_2} knew {STR_VAR_3}...",
        "That tells you the kind of TRAINER {STR_VAR_1} is.",
        "It was a lesson, and I have learned it!",
    )),
    "gTVSecretBaseVisitText12": (("Well, well", "hopes and dreams"), (
        "Well, well!|I take my hat off to {STR_VAR_1}.",
        "Those POKéMON have a great deal still to come.",
        "They carry everything {STR_VAR_1} is hoping for.",
        "And that the {STR_VAR_2} knew {STR_VAR_3}...",
        "That tells you the kind of TRAINER {STR_VAR_1} is.",
        "It was a lesson, and I have learned it!",
    )),
    "gTVSecretBaseVisitText13": (("superb SECRET BASE", "adieu"), (
        "What a SECRET BASE that was!",
        "Viewers -- if the chance comes your way, call on {STR_VAR_1}'s "
        "SECRET BASE.",
        "Until next time, I take my leave!",
    )),

    # -- the advertisement that calls itself a report -------------------------
    "gTVPokemonLotteryWinnerFlashReportText00": (
        ("LOTTERY WINNER FLASH", "greatest selection"), (
            "It's exciting! It's dramatic!",
            "It's the POKéMON LOTTERY WINNER FLASH REPORT!",
            "Hello! We are live from the POKéMON LOTTERY CORNER, on the ground "
            "floor of the BAIA DAS LUZES DEPARTMENT STORE!",
            "And as it always does, luck has found somebody today!",
            "That TRAINER's name... {STR_VAR_1}!",
            "{STR_VAR_1} took the {STR_VAR_2} prize, and went home with the "
            "{STR_VAR_3}!",
            "{STR_VAR_1}! Our congratulations!",
            "Viewers -- don't only watch. Come and take a ticket!",
            "All of us at the BAIA DAS LUZES DEPARTMENT STORE will be glad to "
            "see you!",
            "This has been live from the BAIA DAS LUZES DEPARTMENT STORE, "
            "which carries more than anywhere in ARAUNA!",
        )),

    # -- the seminar ----------------------------------------------------------
    "gTVThePokemonBattleSeminarText00": (("BATTLE SEMINAR", "case study"), (
        "THE POKéMON BATTLE SEMINAR!",
        "We take battles apart to see what can be learned from them.",
        "Tonight we look at a battle of {STR_VAR_1}'s.",
        "{STR_VAR_1}'s {STR_VAR_2} was up against a {STR_VAR_3}...",
    )),
    "gTVThePokemonBattleSeminarText01": (("used the move", "wrong thing to do"), (
        "And it was told to use {STR_VAR_3} on the {STR_VAR_2}...",
        "Hmm... {STR_VAR_1}!|That was the wrong call!",
    )),
    SEAM_OPENER: (("In addition", "also knew"), (
        "Besides the move that lost it, the TRAINER's {STR_VAR_1} also knew",
    )),
    "gTVThePokemonBattleSeminarText03": (("the moves", "and"), (
        "the moves {STR_VAR_1}, {STR_VAR_2} and {STR_VAR_3}.",
    )),
    "gTVThePokemonBattleSeminarText04": (("the moves", "and"), (
        "the moves {STR_VAR_1} and {STR_VAR_2}.",
    )),
    "gTVThePokemonBattleSeminarText05": (("the move",), (
        "the move {STR_VAR_2}.",
    )),
    "gTVThePokemonBattleSeminarText06": (("what should", "battle with intelligence"), (
        "So what ought the TRAINER to have used?",
        "... ... ... ... ...|{STR_VAR_1}!",
        "{STR_VAR_1} would have served far better than {STR_VAR_2}.",
        "Viewers -- take the lesson, and battle with your head!",
        "Until next time, good evening!",
    )),

    # -- the fans -------------------------------------------------------------
    "gTVTrainerFanClubText00": (("TRAINER FAN CLUB", "Wrooooooaaaaah"), (
        "All together now!|TRAINER FAN CLUB!",
        "MC: How is everybody tonight?|We have gathered up the followers of "
        "the TRAINER {STR_VAR_1}!",
        "FANS: Wrooooooaaaaah!",
        "FANS: {STR_VAR_1}!",
        "MC: Everyone!|How do we feel about {STR_VAR_1}?!",
        "FANS: We love {STR_VAR_1}!",
        "MC: And what is it you love?!",
    )),
    "gTVTrainerFanClubText01": (("POKé BALLS",), (
        "FANS: The way those POKé BALLS get thrown!",
    )),
    "gTVTrainerFanClubText02": (("running",), (
        "FANS: The way that TRAINER runs!",
    )),
    "gTVTrainerFanClubText03": (("going gets tough",), (
        "FANS: Getting harder the harder it gets!",
    )),
    "gTVTrainerFanClubText04": (("knowledge",), (
        "FANS: Knowing everything there is to know about POKéMON!",
    )),
    "gTVTrainerFanClubText05": (("kindness",), (
        "FANS: Being kind to every POKéMON going!",
    )),
    "gTVTrainerFanClubText06": (("BIKE",), (
        "FANS: What that TRAINER can do on a BIKE!",
    )),
    "gTVTrainerFanClubText07": (("item-buying",), (
        "FANS: The way that TRAINER shops!",
    )),
    "gTVTrainerFanClubText08": (("nicknaming",), (
        "FANS: The names that TRAINER gives!",
    )),
    "gTVTrainerFanClubText09": (("SECRET BASE",), (
        "FANS: What that TRAINER does with a SECRET BASE!",
    )),
    "gTVTrainerFanClubText10": (("TMs",), (
        "FANS: The nerve it takes to use a TM like that!",
    )),
    "gTVTrainerFanClubText11": (("special slogan", "unique ring"), (
        "MC: There you have it -- {STR_VAR_1} is not to be touched tonight!",
        "And among {STR_VAR_1}'s followers there is a call and an answer!",
        "MC: When I say {STR_VAR_1}, you say...",
        "FANS: {STR_VAR_2}!",
        "FANS: {STR_VAR_3}!",
        "FANS: {STR_VAR_2}!",
        "FANS: {STR_VAR_3}!",
        "MC: That's it. When somebody says “{STR_VAR_1}”...",
        "You come back with “{STR_VAR_2} {STR_VAR_3}!”",
        "And doesn't that sound like nothing else!",
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
        masked = masked[:start] + '\t.string "<ARAUNA_TV_SECRET_BASE_EN>"\n\n' + masked[end:]
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

    # The seminar's sentence is split across two blocks the engine prints end
    # to end. The first must not close it and the others must not open one.
    opener = composed[SEAM_OPENER][-1].rstrip("$").rstrip()
    if opener.endswith((".", "!", "?")):
        raise ValueError(
            f"{SEAM_OPENER}: closes a sentence the next block has to finish")
    for label in SEAM_CLOSERS:
        first = composed[label][0]
        if not first.startswith("the move"):
            raise ValueError(
                f"{label}: must continue the previous block, not start a new "
                f"sentence: {first!r}")

    # The visitor's four verdicts are told apart only by the noise he makes,
    # so no two may open the same way.
    verdicts = [composed[f"gTVSecretBaseVisitText{n:02d}"][0] for n in (9, 10, 11, 12)]
    if len(set(verdicts)) != len(verdicts):
        raise ValueError("two of the visitor's verdicts open identically")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render SECRET BASE VISIT, the lottery report and the seminar.")
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
    print(f"TV Secret Base English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

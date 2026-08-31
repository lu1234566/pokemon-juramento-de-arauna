#!/usr/bin/env python3
"""The RESERVA ARAUNA: its gate, its wardens, and the people wandering it.

A player pays ¥500 at the gate, is handed thirty SAFARI BALLS, and is turned
out into the reserve until the balls or five hundred steps run out. Nothing
in there explains itself again, so the gate texts are the only place those
four numbers are ever stated, and the renderer keeps every one of them: the
price, the thirty balls, the five hundred steps, and the two conditions that
end the game.

The rest of the file is people standing about in the grass, and between them
they teach the one mechanic the reserve runs on -- that a {POKEBLOCK} makes
a wild POKéMON less likely to bolt, and that a {POKEBLOCK} left on the FEEDER
draws POKéMON to it. Emerald scatters that across five strangers who each
half-say it. Here each of the five says one whole part of it, so a player who
speaks to any one of them comes away with something they can use.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SOURCE = ROOT / "data" / "scripts" / "safari_zone.inc"

BOX = TextBox({"{POKEBLOCK}": 9, "{STR_VAR_1}": 12, "{PLAYER}": 7}, width=34)

WHOLE = ("RESERVA ARAUNA", "SAFARI BALL", "SAFARI BALLS", "SAFARI Game",
         "{POKEBLOCK} CASE", "{POKEBLOCK} FEEDER", "CONTEST HALL",
         "BAIA DAS LUZES", "REST HOUSE", "PC BOX", "ARAUNA")

TARGETS: dict[str, tuple[str, ...]] = {
    # -- what the engine says while the game is running ---------------------
    "SafariZone_Text_WouldYouLikeToExit": (
        "Would you like to leave the RESERVA ARAUNA now?",
    ),
    "SafariZone_Text_TimesUp": (
        "Ding-dong! Your five hundred steps are up.|The SAFARI Game is over.",
    ),
    "SafariZone_Text_OutOfBalls": (
        "You have used your last SAFARI BALL.|The SAFARI Game is over.",
    ),
    "SafariZone_Text_PlacePokeblockOnFeeder": (
        "Would you like to put a {POKEBLOCK} on the {POKEBLOCK} FEEDER?",
    ),
    "SafariZone_Text_PokeblockStillHere": (
        "The {STR_VAR_1} you left here before is still on the feeder.",
    ),
    "SafariZone_Text_PokeblockWasPlaced": (
        "The {STR_VAR_1} was placed on the {POKEBLOCK} FEEDER.",
    ),

    # -- the gate -----------------------------------------------------------
    "Route121_SafariZoneEntrance_Text_WelcomeToSafariZone": (
        "Welcome to the RESERVA ARAUNA.",
        "Inside you will find POKéMON that are hardly ever seen anywhere "
        "else in ARAUNA.",
        "And you will find them wild, in the country they actually live in. "
        "Nothing here has been arranged for you.",
        "The gates are open to TRAINERS, and what you catch is yours to "
        "keep.",
        "Come in and enjoy the RESERVA ARAUNA.",
    ),
    "Route121_SafariZoneEntrance_Text_WelcomeFirstTime": (
        "Welcome to the RESERVA ARAUNA.|Is this your first visit?",
    ),
    "Route121_SafariZoneEntrance_Text_ComeInAndEnjoy": (
        "Come in and enjoy the RESERVA ARAUNA.",
    ),
    "Route121_SafariZoneEntrance_Text_FirstTimeInfo": (
        "You go in with 30 SAFARI BALLS and nothing else. Those are what you "
        "catch with.",
        "The SAFARI Game ends the moment you throw the last of them, or the "
        "moment you have walked 500 steps -- whichever comes first.",
        "Come in and enjoy the RESERVA ARAUNA.",
    ),
    "Route121_SafariZoneEntrance_Text_WouldYouLikeToPlay": (
        "Welcome to the RESERVA ARAUNA.",
        "Everything you catch, for ¥500.|Would you like a SAFARI Game?",
    ),
    "Route121_SafariZoneEntrance_Text_PlayAnotherTime": (
        "Of course.|Do come another time.",
    ),
    "Route121_SafariZoneEntrance_Text_NotEnoughMoney": (
        "You have not got ¥500 on you.|I am sorry.",
    ),
    "Route121_SafariZoneEntrance_Text_ThatWillBe500Please": (
        "That will be ¥500, please.",
    ),
    "Route121_SafariZoneEntrance_Text_HereAreYourSafariBalls": (
        "And here are your SAFARI BALLS.",
    ),
    "Route121_SafariZoneEntrance_Text_Received30SafariBalls": (
        "{PLAYER} received 30 SAFARI BALLS.",
    ),
    "Route121_SafariZoneEntrance_Text_PleaseEnjoyYourself": (
        "We will call you in when your game is over.",
        "Until then the reserve is yours. Off you go.",
    ),
    "Route121_SafariZoneEntrance_Text_PCIsFull": (
        "One moment!|Your PC BOX is full.",
    ),
    "Route121_SafariZoneEntrance_Text_YouNeedPokeblockCase": (
        "One moment!|You appear to have no {POKEBLOCK} CASE with you.",
        "You will catch a great deal more with {POKEBLOCK}S than without "
        "them.",
        "You can get a {POKEBLOCK} CASE at the BAIA DAS LUZES CONTEST HALL. "
        "Come back with one.",
    ),

    # -- the warden inside --------------------------------------------------
    "SafariZone_South_Text_StillHaveTimeExit": (
        "You have time left. Are you sure you want to leave the RESERVA "
        "ARAUNA now?",
    ),
    "SafariZone_South_Text_EnjoyTheRestOfYourAdventure": (
        "Then enjoy the rest of it out there.",
    ),
    "SafariZone_South_Text_ExitEarlyThankYouForPlaying": (
        "Very well.",
        "I will take back the SAFARI BALLS you have not thrown.",
        "Thank you for coming.|We hope to see you again.",
    ),
    "SafariZone_South_Text_GoodLuck": (
        "Good luck out there.",
        "If you need anything at all, you come and tell me.",
    ),

    # -- the people in the grass. Between them they teach the whole of it. --
    "SafariZone_South_Text_Boy": (
        "Did you know?",
        "Put a {POKEBLOCK} in that square box and POKéMON come and gather "
        "round it.",
    ),
    "SafariZone_South_Text_Man": (
        "I want to get further in, and I have gone and left my BIKE at home.",
        "Something tells me the rarer things live out at the edges.",
    ),
    "SafariZone_Southwest_Text_Woman": (
        "Sometimes I throw a {POKEBLOCK} at a POKéMON and it pays me no "
        "attention at all.",
        "Do they have things they like and things they do not, do you "
        "suppose?",
    ),
    "SafariZone_Northwest_Text_Man": (
        "Haah... haah...|I got out this far... but...",
        "I am spent. I have not the legs left to catch anything...",
    ),
    "SafariZone_North_Text_Fisherman": (
        "I am out here after WATER POKéMON you never see anywhere in ARAUNA.",
        "You would not know where the lake is, would you?",
    ),
    "SafariZone_North_Text_Man": (
        "I am going to catch a great pile of rare ones here and trade them "
        "off to my friends.",
    ),
    "SafariZone_South_Text_Youngster": (
        "I put a {POKEBLOCK} on the {POKEBLOCK} FEEDER and now it has gone.",
        "Something must have come and eaten it while I was not looking.",
    ),
    "Route121_SafariZoneEntrance_Text_TrainerTip": (
        "RESERVA ARAUNA TRAINER TIP.",
        "Throw {POKEBLOCK}S at a wild POKéMON and it will be slower to bolt.",
    ),
    "SafariZone_Southwest_Text_RestHouseSign": (
        "“Rest your legs a while.”|REST HOUSE",
    ),
    "SafariZone_RestHouse_Text_Youngster": (
        "I have no {POKEBLOCK}S on me and I have still caught a fair few.",
        "Get closer before you throw a SAFARI BALL. That is the whole of my "
        "advice, and it works.",
    ),
    "SafariZone_RestHouse_Text_PsychicM": (
        "A POKéMON given a {POKEBLOCK} is slower to run.",
        "Which means there is little sense spending them on the ones that "
        "were never going to run in the first place.",
    ),
    "SafariZone_RestHouse_Text_FatMan": (
        "Put a {POKEBLOCK} on the FEEDER and POKéMON come to it.",
        "And I am fairly sure a particular sort of {POKEBLOCK} draws a "
        "particular sort of nature.",
    ),

    # -- the eastern expansion ----------------------------------------------
    "SafariZone_South_Text_AreaOffLimits1": (
        "This part is still being built.|No entry, I am afraid.",
    ),
    "SafariZone_South_Text_AreaOffLimits2": (
        "This part is still being built.|No entry, I am afraid.",
    ),
    "SafariZone_Southeast_Text_ExpansionIsFinished": (
        "The work on the RESERVA ARAUNA's new ground is finished.",
        "We hope you will make something of it.",
    ),
    "SafariZone_Southeast_Text_LittleGirl": (
        "Wow! I have never seen a single one of these before!",
    ),
    "SafariZone_Southeast_Text_FatMan": (
        "Every POKéMON in this part is new to me.",
        "And I am allowed to catch them. Rare as they are. Marvellous.",
    ),
    "SafariZone_Southeast_Text_RichBoy": (
        "The POKéMON around here do not look as though they come from ARAUNA "
        "at all.",
    ),
    "SafariZone_Northeast_Text_Boy": (
        "I am down to my last couple of SAFARI BALLS.",
        "Now I cannot make up my mind what to spend them on.",
    ),
    "SafariZone_Northeast_Text_Woman": (
        "I heard there are Jacarim in here somewhere.|Where would one be, do "
        "you think?",
    ),
    "SafariZone_Northeast_Text_Girl": (
        "Oh, bother!|I cannot seem to catch a single thing!",
        "I shall have thrown away the admission if I go home empty-handed!",
    ),
}

# The two off-limits signs are the same sign in two places. They are the one
# pair here allowed to read alike.
TWINS = ("SafariZone_South_Text_AreaOffLimits1",
         "SafariZone_South_Text_AreaOffLimits2")


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
        masked = masked[:start] + '\t.string "<ARAUNA_RESERVA_EN>"\n\n' + masked[end:]
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

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # The gate states the rules once and nothing inside repeats them.
    rules = flat("Route121_SafariZoneEntrance_Text_FirstTimeInfo")
    for fact in ("30", "SAFARI BALLS", "500"):
        if fact not in rules:
            raise ValueError(
                f"FirstTimeInfo: dropped {fact!r}, and nothing inside the "
                f"reserve says it again")
    for label in ("Route121_SafariZoneEntrance_Text_WouldYouLikeToPlay",
                  "Route121_SafariZoneEntrance_Text_ThatWillBe500Please",
                  "Route121_SafariZoneEntrance_Text_NotEnoughMoney"):
        if "¥500" not in flat(label):
            raise ValueError(f"{label}: no longer states the price")

    # Both endings have to say which one it was, since the player is put
    # straight back outside either way.
    if "SAFARI BALL" not in flat("SafariZone_Text_OutOfBalls"):
        raise ValueError("OutOfBalls: no longer says the balls ran out")
    if "steps" not in flat("SafariZone_Text_TimesUp"):
        raise ValueError("TimesUp: no longer says the steps ran out")

    # The case refusal has to say where a case comes from, or it is a dead
    # end for a player who has never been to a CONTEST HALL.
    case = flat("Route121_SafariZoneEntrance_Text_YouNeedPokeblockCase")
    if "CONTEST HALL" not in case:
        raise ValueError(
            "YouNeedPokeblockCase: no longer says where a {POKEBLOCK} CASE "
            "comes from")

    # The reserve runs on one mechanic. Five people teach it between them,
    # and each has to carry a usable piece of it.
    teachers = {
        "Route121_SafariZoneEntrance_Text_TrainerTip": ("bolt", "flee", "run"),
        "SafariZone_RestHouse_Text_PsychicM": ("run", "flee", "bolt"),
        "SafariZone_RestHouse_Text_FatMan": ("FEEDER",),
        "SafariZone_South_Text_Boy": ("gather", "round it"),
        "SafariZone_RestHouse_Text_Youngster": ("closer",),
    }
    for label, wanted in teachers.items():
        text = flat(label).lower()
        if not any(word.lower() in text for word in wanted):
            raise ValueError(
                f"{label}: no longer teaches its part of how the reserve is "
                f"played")

    # Everyone else in the grass is distinguished only by what they say.
    said = [flat(label) for label in TARGETS if label not in TWINS]
    if len(set(said)) != len(said):
        raise ValueError("two people in the reserve say exactly the same thing")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the RESERVA ARAUNA in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = SOURCE.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        SOURCE.write_text(rendered, encoding="utf-8")
    print(f"Reserva Arauna English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

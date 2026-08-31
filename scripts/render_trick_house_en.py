#!/usr/bin/env python3
"""The CASA DOS TRUQUES, its owner, and the five MECHADOLLS in room five.

Three surfaces, one man. He hides somewhere in the entrance hall and is
delighted to be found, he waits at the end of each puzzle to concede a
carefully measured amount of ground, and he leaves eventually on a journey to
think up more. His MECHADOLLS talk in shouted capitals because they are
machines.

Two families here are generated rather than written out. The eight
"concealed" lines differ only in where he was hiding, and the eight "all
night" lines differ only in what he built and how much greatness he is
prepared to concede -- and that concession is a ladder, tightening by one
rung per puzzle until the eighth admits the player may be above him. Written
by hand the ladder loses a rung, and nothing else in the building tells a
player they are getting further.

The quiz questions are rewritten for wording only. The correct answer to each
lives in a multichoice table in the script, keyed by position, so changing
what a question actually asks would silently make the right answer wrong. The
renderer checks every quiz still asks about the same thing.

The answer lists in data/text/trick_house_mechadolls.inc are left alone --
they are multichoice options, mostly bare species names -- but the renderer
checks each of those names against species_names.h, since an answer list that
has drifted from the species table offers the player a POKéMON that does not
exist.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

ENTRANCE = ROOT / "data" / "maps" / "Route110_TrickHouseEntrance" / "scripts.inc"
END = ROOT / "data" / "maps" / "Route110_TrickHouseEnd" / "scripts.inc"
PUZZLE5 = ROOT / "data" / "maps" / "Route110_TrickHousePuzzle5" / "scripts.inc"
MECHADOLLS = ROOT / "data" / "text" / "trick_house_mechadolls.inc"
SPECIES_TABLE = ROOT / "src" / "data" / "text" / "species_names.h"

BOX = TextBox({"{PLAYER}": 7}, width=34)

WHOLE = ("CASA DOS TRUQUES", "TRICK MASTER", "RED TENT", "BLUE TENT",
         "MECHADOLL", "LEECH LIFE", "HARBOR MAIL", "HARBOR MAILS",
         "BURN HEAL", "GREAT BALL", "SUPER POTION", "SODA POP",
         "PORTO DO SAL", "MATA DO MEIO", "CASA DA CINZA",
         "PAMPA DA ESPERA", "CONSORCIO HORIZONTE", "SEASHORE HOUSE",
         "CYCLING ROAD", "TRAINER'S SCHOOL", "PROF. ANAHI", "ROUTE 110",
         "ARAUNA")

# Where he was hiding, in the order the labels give.
HIDING: dict[str, str] = {
    "ConcealedBeneathDesk": "under this desk",
    "ConcealedBehindTree": "behind this tree",
    "ConcealedInDresser": "inside this dresser",
    "ConealedBeyondWindow": "on the far side of this window",
    "ConcealedInPlanter": "in this planter",
    "ConcealedInCupboard": "inside this cupboard",
    "ConcealedBehindWindow": "behind this window",
    "ConcealedBeneathCushion": "under this cushion",
}

# What he built for each puzzle, and how much greatness he will concede
# once it has been beaten. The ladder tightens by a rung each time.
LADDER: tuple[tuple[str, str, str], ...] = (
    ("AllNightToPlantTrees", "planting all those trees",
     "You are within one, two, three, four, five, six places of my "
     "greatness."),
    ("AllNightToMakeMaze", "making that maze",
     "You are within one, two, three, four, five places of my greatness."),
    ("AllNightToPreparePanels", "preparing those wall panels",
     "You are within one, two, three, four places of my greatness."),
    ("AllNightToShoveBoulders", "shoving in those boulders",
     "You are within one, two, three places of my greatness."),
    ("AllNightToMakeMechadolls", "building the MECHADOLLS, and another "
     "night thinking up their quiz",
     "You are within one, two places of my greatness."),
    ("AllNightToInstallDoors", "putting in those doors",
     "You are all but my equal in greatness."),
    ("AllNightSettingUpArrows", "setting up those arrows",
     "You are my equal in greatness."),
    ("AllNightPolishingFloors", "polishing those floors",
     "You are above me in greatness.|Possibly."),
)

# Each quiz's subject. The correct answer is a position in a multichoice
# table, so a rewording that changes the subject makes the right answer
# wrong; these are what the renderer holds each question to.
QUIZZES: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "Mechadoll1Quiz1": (("ROUTE 110",), (
        "MECHADOLL 1 QUIZ.",
        "ONE OF THESE POKéMON IS NOT FOUND ON ROUTE 110. WHICH?")),
    "Mechadoll1Quiz2": (("WATER",), (
        "MECHADOLL 1 QUIZ.",
        "ONE OF THESE POKéMON IS NOT A WATER TYPE. WHICH?")),
    "Mechadoll1Quiz3": (("LEECH LIFE",), (
        "MECHADOLL 1 QUIZ.",
        "ONE OF THESE POKéMON DOES NOT USE LEECH LIFE. WHICH?")),
    "Mechadoll2Quiz1": (("VAL", "father"), (
        "MECHADOLL 2 QUIZ.",
        "WHICH OF THESE POKéMON DID VAL BORROW FROM YOUR father?")),
    "Mechadoll2Quiz2": (("PROF. ANAHI",), (
        "MECHADOLL 2 QUIZ.",
        "WHICH OF THESE POKéMON WAS CHASING PROF. ANAHI?")),
    "Mechadoll2Quiz3": (("CONSORCIO HORIZONTE", "PAMPA DA ESPERA"), (
        "MECHADOLL 2 QUIZ.",
        "WHICH OF THESE POKéMON DID CONSORCIO HORIZONTE USE IN THE PAMPA DA "
        "ESPERA FOREST?")),
    "Mechadoll3Quiz1": (("HARBOR MAIL", "BURN HEAL"), (
        "MECHADOLL 3 QUIZ.",
        "WHICH COSTS MORE: THREE HARBOR MAILS, OR ONE BURN HEAL?")),
    "Mechadoll3Quiz2": (("GREAT BALL", "POTION"), (
        "MECHADOLL 3 QUIZ.",
        "SELL ONE GREAT BALL, BUY ONE POTION. HOW MUCH IS LEFT?")),
    "Mechadoll3Quiz3": (("REPEL", "SODA POP", "SUPER POTION"), (
        "MECHADOLL 3 QUIZ.",
        "DO ONE REPEL AND ONE SODA POP COST MORE THAN ONE SUPER POTION?")),
    "Mechadoll4Quiz1": (("SEASHORE HOUSE",), (
        "MECHADOLL 4 QUIZ.",
        "IN THE SEASHORE HOUSE, WERE THERE MORE MEN OR MORE WOMEN?")),
    "Mechadoll4Quiz2": (("CASA DA CINZA",), (
        "MECHADOLL 4 QUIZ.",
        "IN CASA DA CINZA, WERE THERE MORE ELDERLY MEN OR MORE ELDERLY "
        "LADIES?")),
    "Mechadoll4Quiz3": (("TRAINER'S SCHOOL", "girl"), (
        "MECHADOLL 4 QUIZ.",
        "IN THE TRAINER'S SCHOOL, HOW MANY girl STUDENTS WERE THERE?")),
    "Mechadoll5Quiz1": (("PORTO DO SAL", "FAN CLUB"), (
        "MECHADOLL 5 QUIZ.",
        "IN THE PORTO DO SAL POKéMON FAN CLUB, HOW MANY POKéMON WERE "
        "THERE?")),
    "Mechadoll5Quiz2": (("MATA DO MEIO", "tree"), (
        "MECHADOLL 5 QUIZ.",
        "IN MATA DO MEIO, HOW MANY tree HOUSES WERE THERE?")),
    "Mechadoll5Quiz3": (("CYCLING ROAD", "TRIATHLETES"), (
        "MECHADOLL 5 QUIZ.",
        "ON THE CYCLING ROAD, HOW MANY TRIATHLETES WERE THERE?")),
}

ENTRANCE_BLOCKS: dict[str, tuple[str, ...]] = {
    "Route110_TrickHouseEntrance_Text_YoureBeingWatched": (
        "You are being watched...",
    ),
    "Route110_TrickHouseEntrance_Text_TheyCallMeTrickMaster": (
        "Behold!",
        "For I am the greatest living mystery of a man in all ARAUNA!|They "
        "call me...",
        "The TRICK MASTER!|Wahahaha! Delighted, delighted.",
    ),
    "Route110_TrickHouseEntrance_Text_ComeToChallengeTrickHouse": (
        "You have come to take on my CASA DOS TRUQUES, have you not?",
        "That is why you are here. It is. I know it.",
        "Then consider your challenge accepted!",
        "Through the scroll there, and let it begin!",
        "I shall be waiting at the far end!",
    ),
    "Route110_TrickHouseEntrance_Text_ItsAScroll": (
        "It is a scroll.",
    ),
    "Route110_TrickHouseEntrance_Text_GoInHoleBehindScroll": (
        "There is a great hole behind the scroll.|Go in?",
    ),
    "Route110_TrickHouseEntrance_Text_LeavingOnJourneyNote": (
        "There is a note pinned to the scroll...",
        "“I have gone away.|Do not come looking. TRICK MASTER”",
    ),
    "Route110_TrickHouseEntrance_Text_NextTimeUseThisTrick": (
        "Next time I shall use this trick, and that scheme, and those "
        "ruses...",
        "Mufufufu... though I say it myself, it is brilliantly difficult. "
        "Even for me.",
    ),
    "Route110_TrickHouseEntrance_Text_InMidstOfDevisingNewChallenges": (
        "Hah? What?|Oh, it is you.",
        "I am in the middle of devising new and trickier challenges.",
        "A little more time to think is not too much to ask, is it? You "
        "would not begrudge me that?|Come back in a while.",
    ),
    "Route110_TrickHouseEntrance_Text_YoureHereToAcceptReward": (
        "Ah, it is you! Here for the reward from before, are you not? Yes, I "
        "am right, I am always right.",
        "Here.|Take it now.",
    ),
    "Route110_TrickHouseEntrance_Text_DidYouNotComeToClaimReward": (
        "Hah?|You did not come to claim your reward?",
    ),
    "Route110_TrickHouseEntrance_Text_MechadollWhichTent": (
        "MECHADOLL 5 AM I.|IF THE REWARD IS NOT TAKEN BY YOU, THEN THE TRICK "
        "MASTER YOU CANNOT FOLLOW.",
        "RED TENT OR BLUE TENT.|WHICH DO YOU PREFER?",
    ),
    "Route110_TrickHouseEntrance_Text_ThenFarewell": (
        "THEN FAREWELL.",
    ),
    "Route110_TrickHouseEntrance_Text_PCFullAgain": (
        "YOUR PC STATUS: FULL AGAIN.|MEAN, YOU ARE.",
    ),
    "Route110_TrickHousePuzzle_Text_FoundAScroll": (
        "{PLAYER} found a scroll.",
    ),
    "Route110_TrickHousePuzzle_Text_MemorizedSecretCode": (
        "{PLAYER} memorised the secret code written on the scroll.",
    ),
    "Route110_TrickHousePuzzle_Text_SecretCodeWrittenOnIt": (
        "There is a secret code written on it.",
    ),
    "Route110_TrickHouseEntrance_Text_DoorLockedWriteSecretCodeHere": (
        "The door is locked.",
        "...And looking closer, something is written on it: “Write the "
        "secret code here.”",
    ),
}

END_BLOCKS: dict[str, tuple[str, ...]] = {
    "Route110_TrickHouseEnd_Text_YouveMadeItToMe": (
        "Aak!|You have got all the way to me?|Hmmm... you are sharp.",
    ),
    "Route110_TrickHouseEnd_Text_FountainOfIdeasRunDry": (
        "Wh-what am I to do?|My fountain of tricks has run dry...",
        "Perhaps it is time I went round the country in search of new ones...",
    ),
    "Route110_TrickHouseEnd_Text_DefeatedMePreferWhichTent": (
        "It galls me to say it, but you have bested me.",
        "Though you must have been drawn back here again and again by my "
        "charisma. You must have been. Yes.",
        "Which has nothing whatever to do with my losing.",
        "In recognition of the friendship between you, the driven, and "
        "myself, the genius, I insist you take a keepsake.",
        "There are two, in fact.|A RED TENT and a BLUE TENT.|Which do you "
        "prefer?",
    ),
    "Route110_TrickHouseEnd_Text_NoRoomInPC": (
        "What? No room in your PC?|And what am I to make of that?",
        "I would say more, but I am far too kind. Come back later.",
    ),
    "Route110_TrickHouseEnd_Text_LeavingOnJourney": (
        "... ... ... ... ... ...",
        "I am going away, on a journey of discovery. A search for new tricks.",
        "I hope you will come one day and entertain me again.",
        "And now -- farewell!",
    ),
    "Route110_TrickHouseEnd_Text_YouHaveEarnedThisReward": (
        "Very well.|You have earned this.",
    ),
    "Route110_TrickHouseEnd_Text_NoRoomForThis": (
        "What? You have no room for it?|What in the world are you carrying?",
        "No matter. You reached me, so your reward stays here with me until "
        "you can take it.",
    ),
    "Route110_TrickHouseEnd_Text_MakeNewTricksToStumpYou": (
        "Wipe that smirk off your face! It is far too early to think you "
        "have won!",
        "I shall make new tricks and they shall stump you. You may laugh at "
        "me when you are through them.",
        "Come back for the next instalment.",
    ),
    "Route110_TrickHouseEnd_Text_YoureIgnoringMe": (
        "Now, now. Are you ignoring me?|That I find heartbreaking.",
    ),
}

PUZZLE5_BLOCKS: dict[str, tuple[str, ...]] = {
    "Route110_TrickHousePuzzle5_Text_WroteSecretCodeLockOpened": (
        "{PLAYER} wrote the secret code on the door.",
        "“TRICK MASTER is a genius.”|... ... ... ... ... ... ... ...",
        "The lock clicked open.",
    ),
    "Route110_TrickHousePuzzle5_Text_Mechadoll1Intro": (
        "CLICKETY-CLACK...|MECHADOLL 1 AM I.",
        "ANSWER THE QUIZZES CORRECTLY AND YOU WILL REACH MECHADOLL 5. THERE "
        "THE SECRET CODE CAN BE OBTAINED.",
    ),
    "Route110_TrickHousePuzzle5_Text_Mechadoll2Intro": (
        "CLICKETY-CLACK...|MECHADOLL 2 AM I.",
        "MECHADOLL 1'S QUIZ DIFFICULTY IS SET TOO LOW.",
    ),
    "Route110_TrickHousePuzzle5_Text_Mechadoll3Intro": (
        "CLICKETY-CLACK...|MECHADOLL 3 AM I.",
        "MATTERS OF MONEY ARE MY SOLE CONCERN.",
    ),
    "Route110_TrickHousePuzzle5_Text_Mechadoll4Intro": (
        "CLICKETY-CLACK...|MECHADOLL 4 THAT IS ME.",
        "MY QUIZ IS AN OBJECT OF BEAUTY.",
    ),
    "Route110_TrickHousePuzzle5_Text_Mechadoll5Intro": (
        "CLICKETY-CLACK...|MECHADOLL 5 AM I.",
        "THE MASTER'S BEST AND PROUDEST WORK AM I.",
    ),
    "Route110_TrickHousePuzzle5_Text_CorrectGoThrough": (
        "CONGRATULATIONS. CORRECT YOU ARE.|GO THROUGH. PLEASE.",
    ),
    "Route110_TrickHousePuzzle5_Text_DisappointmentError": (
        "BZZZT. DISAPPOINTMENT.|ERROR.",
    ),
    "Route110_TrickHousePuzzle5_Text_Wahahahaha": (
        "WAHAHAHAHA! WAHAHAHAHA!|CLICKETY-CLACK!",
    ),
    "Route110_TrickHousePuzzle5_Text_WaitForNextChallenge": (
        "YOUR NEXT CHALLENGE WE WAIT FOR.",
    ),
}


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    entrance = dict(ENTRANCE_BLOCKS)
    for label, place in HIDING.items():
        entrance[f"Route110_TrickHouseEntrance_Text_{label}"] = (
            "Hah? Grrr...",
            f"How did you know I had concealed myself {place}? You are "
            f"sharp!",
        )
    end = dict(END_BLOCKS)
    for label, built, concession in LADDER:
        end[f"Route110_TrickHouseEnd_Text_{label}"] = (
            f"It took me all night, {built}...",
            concession,
        )
    puzzle5 = dict(PUZZLE5_BLOCKS)
    for label, (_subjects, body) in QUIZZES.items():
        puzzle5[f"Route110_TrickHousePuzzle5_Text_{label}"] = body
    return {"entrance": entrance, "end": end, "puzzle5": puzzle5}


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"entrance": ENTRANCE, "end": END, "puzzle5": PUZZLE5}


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
                         + '\t.string "<ARAUNA_TRICK_HOUSE_EN>"\n\n'
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

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # Eight hiding places, eight different places. If two match, one of the
    # eight is telling the player they found him somewhere they did not.
    places = [flat(f"Route110_TrickHouseEntrance_Text_{label}")
              for label in HIDING]
    if len(set(places)) != len(places):
        raise ValueError("two of the eight hiding places read alike")
    for label, place in HIDING.items():
        if place not in flat(f"Route110_TrickHouseEntrance_Text_{label}"):
            raise ValueError(
                f"{label}: no longer says he was hiding {place}")

    # The concession ladder is the only running measure of progress the
    # player is given, so every rung has to be a different rung.
    rungs = [flat(f"Route110_TrickHouseEnd_Text_{label}")
             for label, _built, _concession in LADDER]
    if len(set(rungs)) != len(rungs):
        raise ValueError(
            "two rungs of the greatness ladder read alike, so beating one "
            "more puzzle tells the player nothing")
    for label, built, _concession in LADDER:
        if "all night" not in flat(f"Route110_TrickHouseEnd_Text_{label}"):
            raise ValueError(f"{label}: no longer says it took him all night")

    # The right answer to each quiz is a position in a multichoice table, so
    # a question that has drifted off its subject silently has the wrong
    # answer marked correct.
    for label, (subjects, _body) in QUIZZES.items():
        text = flat(f"Route110_TrickHousePuzzle5_Text_{label}")
        for subject in subjects:
            if subject not in text:
                raise ValueError(
                    f"{label}: no longer asks about {subject!r}, so the "
                    f"answer the script marks correct may not be")

    # The answer lists are not rewritten here, but a list that has drifted
    # from the species table offers a POKéMON that does not exist.
    species = {m.group(1): m.group(2) for m in re.finditer(
        r'\[SPECIES_(\w+)\] = _\("([^"]*)"\)',
        SPECIES_TABLE.read_text(encoding="utf-8"))}
    for match in re.finditer(r'gTrickHouse_Mechadoll_(\w+)::\n\t\.string "([^"]*)\$"',
                             MECHADOLLS.read_text(encoding="utf-8")):
        key, value = match.group(1), match.group(2)
        base = re.sub(r"\d+$", "", key).upper()
        if base == "NONE" or base not in species:
            continue
        if species[base] != value:
            raise ValueError(
                f"gTrickHouse_Mechadoll_{key}: offers {value!r}, but "
                f"species_names.h calls that species {species[base]!r}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the CASA DOS TRUQUES in English.")
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
    print(f"Trick house English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""TRAINER HILL: the reception counter, the people waiting, and the owner.

The hill runs one event, the Time Attack, and a player is told what it is
exactly once -- at the counter, before going up. Three facts in that
explanation change how the run is played and are stated nowhere else in the
building: the clock runs from the counter to the roof, the fastest times go
on the Time Board, and the battles on the way pay neither Exp. Points nor
money. The renderer keeps all three.

The owner on the roof is the one voice here that is not staff. He had the
place built to find somebody to tag with, he greets every arrival as though
it were the one, and he says so whether the player was quick or slow -- the
difference between those two endings is the only feedback on the run itself,
so the quick ending has to say the Time Board is being updated and the slow
one has to say it was slow.

TRAINER HILL keeps its name. Renaming the facility is not this renderer's to
do.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SOURCE = ROOT / "data" / "maps" / "TrainerHill_Entrance" / "scripts.inc"

BOX = TextBox({"{STR_VAR_1}": 6, "{STR_VAR_2}": 6, "{STR_VAR_3}": 6},
              width=34)

WHOLE = ("TRAINER HILL", "Time Attack", "Time Board", "Exp. Points")

TARGETS: dict[str, tuple[str, ...]] = {
    # -- the counter --------------------------------------------------------
    "TrainerHill_Entrance_Text_StillGettingReady": (
        "This is TRAINER HILL, where you may take tag battles against a "
        "great many TRAINERS.",
        "We are not quite ready for you, I am afraid. Do come back.",
    ),
    "TrainerHill_Entrance_Text_WelcomeToTrainerHill": (
        "Welcome.",
        "This is TRAINER HILL, where you may take tag battles against a "
        "great many TRAINERS.",
    ),
    "TrainerHill_Entrance_Text_SaveGameBeforeEnter": (
        "Is this your first time with us?",
        "Then the game must be saved before you go up.",
    ),
    "TrainerHill_Entrance_Text_TrainersUpToFloorX": (
        "Let me see...|The TRAINERS in today reach...",
        "As far as floor no. {STR_VAR_1}.",
    ),
    "TrainerHill_Entrance_Text_TrainersInEveryRoom": (
        "Let me see...|The TRAINERS in today reach...",
        "Every room, by the look of it. There is somebody waiting on each "
        "floor.",
    ),
    "TrainerHill_Entrance_Text_LikeToChallengeTrainers": (
        "Would you care to take on the TRAINERS waiting up there?",
    ),
    "TrainerHill_Entrance_Text_TimeProgessGetSetGo": (
        "I shall time you from here.|Best of luck.",
        "On your marks...",
        "Get set...",
        "Go!",
    ),
    "TrainerHill_Entrance_Text_PleaseVisitUsAgain": (
        "Do please come and see us again.",
    ),
    "TrainerHill_Entrance_Text_TooBadTremendousEffort": (
        "Hard luck.",
        "You battled tremendously well for it, I thought.",
        "Come back and have another go.",
    ),
    "TrainerHill_Entrance_Text_HopeYouGiveItYourBest": (
        "I hope you give it everything you have.",
    ),
    "TrainerHill_Entrance_Text_MovedReceptionHereForSwitch": (
        "When the TRAINERS change over, the coming and going gets rather "
        "wild.",
        "We moved the reception counter down here to keep you out of the "
        "crush.",
        "My apologies for the walk.",
    ),
    "TrainerHill_Entrance_Text_ThankYouForPlaying": (
        "Thank you for taking part.",
    ),
    "TrainerHill_Entrance_Text_ExplainTrainerHill": (
        "TRAINER HILL runs an event we call the Time Attack.",
        "It is a race. We time how long you take to get from this counter to "
        "our owner, who is on the roof.",
        "The quickest times go up on the Time Board. Bring your friends and "
        "see who can hold it.",
        "One thing to know before you start: the TRAINER battles on the way "
        "pay neither Exp. Points nor money.",
    ),
    "TrainerHill_Entrance_Text_NeedAtLeastTwoPokemon": (
        "Oh -- I am sorry, but you appear to have only the one POKéMON with "
        "you.",
        "The battles up there are tag battles. You will need at least two to "
        "enter.",
    ),
    "TrainerHill_Entrance_Text_ChallengeTime": (
        "{STR_VAR_1} min. {STR_VAR_2}.{STR_VAR_3} sec.",
    ),

    # -- the people waiting downstairs --------------------------------------
    "TrainerHill_Entrance_Text_WhatSortOfTrainersAreAhead": (
        "No telling what sort of TRAINERS are up there, or what they have "
        "paired together.",
        "All I know is that whatever is in my way is going aside.",
    ),
    "TrainerHill_Entrance_Text_CantWaitToTestTheWaters": (
        "I hear hard TRAINERS come to TRAINER HILL from every corner of the "
        "map.",
        "I cannot wait to find out where I stand.",
        "Whatever is in my way is going aside.",
    ),
    "TrainerHill_Entrance_Text_FriendsTryingToReachTimeBoardTop": (
        "Do you see the Time Board over there?",
        "My friends and I are all trying to get to the roof faster than the "
        "rest.",
    ),
    "TrainerHill_Entrance_Text_DoYouKnowWhenTheyOpen": (
        "You would not know when this place opens, would you?",
        "I am waiting here so as to be the first challenger it ever has.",
    ),
    "TrainerHill_Elevator_Text_ReturnToReception": (
        "Would you like to go back down to the reception counter?",
    ),

    # -- the owner, on the roof ---------------------------------------------
    "TrainerHill_Roof_Text_YouFinallyCameBravo": (
        "Hm! Hm!",
        "You came!|You have actually arrived!",
        "Wait -- do not tell me!|I know exactly why you climbed all this way "
        "on your own!",
        "You came to see me, the owner of TRAINER HILL, because...",
        "You want to make a tag team with me!|Wa-hoo!",
        "...Ah.|That is not it?",
        "No matter. I watched you all the way up.|Marvellous battling. "
        "Bravo, truly.",
    ),
    "TrainerHill_Roof_Text_HaveTheMostMarvelousGift": (
        "And for somebody as marvellous as you, I have the most marvellous "
        "gift!",
    ),
    "TrainerHill_Roof_Text_FullUpBeBackLaterForThis": (
        "Oh, no -- full to the brim, are you!|You shall have to come back "
        "for this!",
    ),
    "TrainerHill_Roof_Text_GotHereMarvelouslyQuickly": (
        "Oh, hold on!|Did you get up here marvellously quickly?",
        "How splendid! You need not have rushed so on my account!",
        "That is a delight. I shall have the Time Board at reception put "
        "right this instant.",
    ),
    "TrainerHill_Roof_Text_YouWerentVeryQuick": (
        "But, oh...|You were not very quick about getting here.",
    ),
    "TrainerHill_Roof_Text_ArriveZippierNextTime": (
        "It would please me a great deal more if you came up rather zippier "
        "next time.",
        "Then I should be delighted to make a tag team with you.",
        "Until we meet again, amigo!",
    ),
    "TrainerHill_Roof_Text_BuiltTrainerHillToFindPartner": (
        "I had TRAINER HILL built for one reason and one reason only!",
        "To find the partner best suited to making a tag team with me!",
    ),
}


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
        masked = masked[:start] + '\t.string "<ARAUNA_TRAINER_HILL_EN>"\n\n' + masked[end:]
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

    # The counter explains the event once and nothing above it repeats a
    # word of this.
    rules = flat("TrainerHill_Entrance_Text_ExplainTrainerHill")
    for fact in ("Time Attack", "roof", "Time Board", "Exp. Points",
                 "money"):
        if fact not in rules:
            raise ValueError(
                f"ExplainTrainerHill: dropped {fact!r}, which is stated "
                f"nowhere else in the building")

    # A tag battle needs two, and this is the only line that says why.
    two = flat("TrainerHill_Entrance_Text_NeedAtLeastTwoPokemon")
    if "two" not in two or "tag" not in two:
        raise ValueError(
            "NeedAtLeastTwoPokemon: no longer says two are needed, or no "
            "longer says why")

    # The only feedback on the run itself is which of the owner's two
    # endings a player gets, so the two must be tellable apart.
    quick = flat("TrainerHill_Roof_Text_GotHereMarvelouslyQuickly")
    slow = flat("TrainerHill_Roof_Text_YouWerentVeryQuick")
    if "Time Board" not in quick:
        raise ValueError(
            "GotHereMarvelouslyQuickly: no longer says the Time Board is "
            "being updated, which is the whole reward for a fast run")
    if "not very quick" not in slow.lower():
        raise ValueError(
            "YouWerentVeryQuick: no longer says the run was slow, so a "
            "player cannot tell the two endings apart")

    # Four people wait downstairs and are told apart by nothing else.
    waiting = [flat(label) for label in TARGETS
               if label.startswith("TrainerHill_Entrance_Text_")
               and label.endswith(("Ahead", "Waters", "BoardTop", "Open"))]
    if len(set(waiting)) != len(waiting):
        raise ValueError("two of the people waiting say the same thing")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render TRAINER HILL in English.")
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
    print(f"Trainer Hill English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

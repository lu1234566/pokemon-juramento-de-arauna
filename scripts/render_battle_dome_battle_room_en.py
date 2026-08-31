#!/usr/bin/env python3
"""The BATTLE DOME floor: the announcer, the REFEREES, and the MASTER.

Everything a player hears in this room comes over the public address. The
announcer works the crowd before each match, calls the result after it, and
hands the microphone over exactly once -- for the DOME ACE, whose two
entrances are the only speeches in the building that are not shouted at a
stadium.

Fifteen of these texts are the announcer's build-up lines, and they have an
unusual shape: they end on a paragraph break and then a bare terminator, so
the message box stays open and the opponent's own introduction runs on
underneath in the same window. Break that shape and the two halves of the
introduction come up as two separate boxes. So those fifteen are composed and
then deliberately left open, and the renderer checks all fifteen still are.

The names here stay as Emerald spells them -- TUCKER, DOME ACE -- because
render_circuit_masters_en_checked.py runs further down the manifest and is
the single place those are translated. Writing the final names here would put
a second authority on the same question.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SOURCE = ROOT / "data" / "maps" / "BattleFrontier_BattleDomeBattleRoom" / "scripts.inc"
PREFIX = "BattleFrontier_BattleDomeBattleRoom_Text_"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 12, "{STR_VAR_2}": 12}, width=34)

WHOLE = ("BATTLE DOME", "DOME ACE", "CIRCUIT PASS", "Tactics Symbol",
         "Battle Tournament")

# The announcer's build-up. Each ends on a paragraph break with the box left
# open, so the opponent's own introduction runs on underneath it.
BUILD_UP: dict[str, tuple[str, ...]] = {
    "BrightNewHope": (
        "A bright new hope!",
    ),
    "RisingStar": (
        "A star on the rise!",
    ),
    "WillTheyRaceToChampionship": (
        "Will this TRAINER run all the way to the title?",
    ),
    "CanAchieveChampionFirstTry": (
        "The title, at the very first attempt -- can it be done?",
    ),
    "CanLossBeAvenged": (
        "Can the last defeat be answered for?",
    ),
    "OnFireForChampionship": (
        "This TRAINER is alight, and going for a first title!",
    ),
    "WinHereAdvancesToFinal": (
        "A win here and this TRAINER is in the final!",
    ),
    "WillLongHeldDreamComeTrue": (
        "Will the title that has been wanted so long finally come?",
    ),
    "TheInvincibleChampion": (
        "The champion who cannot be beaten!",
    ),
    "CanAnyoneHopeToBeatTrainer": (
        "Is there anybody left who can beat this TRAINER?",
    ),
    "DoBattlesExistSolelyForTrainer": (
        "One begins to wonder whether battles happen for this TRAINER alone!",
    ),
    "CurrentChampAimingToRetainTitle": (
        "The reigning champion, out to keep the title!",
    ),
    "FormerChampHasReturned": (
        "The former champion has come back to us!",
    ),
    "FormerToughnessReturned": (
        "And the old hardness has come back with them!",
    ),
    "WillDoExpectedAdvanceToFinals": (
        "Will this TRAINER do the expected and reach the final?",
    ),
    "WillFormerChampRegainGlory": (
        "Can the former champion take back what was lost?",
    ),
}

CLOSED: dict[str, tuple[str, ...]] = {
    # -- the announcer, working the room -----------------------------------
    "PlayerHasEnteredDome": (
        "{PLAYER} has entered the BATTLE DOME!",
    ),
    "PlayerVersusTrainer": (
        "{STR_VAR_1} match!",
        "{PLAYER} against {STR_VAR_2}!",
        "Let the battle begin!",
    ),
    "PlayerIsWinner": (
        "{PLAYER} takes it!|Congratulations!",
    ),
    "TrainerIsWinner": (
        "{STR_VAR_2} takes it!|Congratulations!",
    ),
    "PlayerIsLv50Champ": (
        "{PLAYER} is the Level 50 Battle Tournament Champion!",
        "Congratulations!",
    ),
    "PlayerIsLvOpenChamp": (
        "{PLAYER} is the Open Level Battle Tournament Champion!",
        "Congratulations!",
    ),
    "PlayerIsLv50Champ2": (
        "{PLAYER} is the Level 50 Battle Tournament Champion!",
        "Congratulations!",
    ),
    "PlayerIsLvOpenChamp2": (
        "{PLAYER} is the Open Level Battle Tournament Champion!",
        "Congratulations!",
    ),
    "RefereeDecisionPleaseWait": (
        "What a finish!|Both of them are down!",
        "In this event a double knockout goes to the REFEREES. Those are the "
        "Battle Tournament rules.",
        "Please stay where you are while the judging is done.",
    ),
    "RefereesDecidedWinnerTrainer": (
        "The REFEREES have decided!",
        "And the winner is...|Well, I never!|The winner is {STR_VAR_1}!|"
        "Congratulations!",
    ),
    "RefereesDecidedWinnerPlayer": (
        "The REFEREES have decided!",
        "And the winner is...|Well, I never!|The winner is {PLAYER}!|"
        "Congratulations!",
    ),
    "FeelGlowOfTrueMaster": (
        "Feel the glow of a true master!",
    ),

    # -- the DOME ACE arrives ----------------------------------------------
    "MakeWayForDomeAceTucker": (
        "And now... the TRAINER standing in the way of {PLAYER}'s run...",
        "Yes! There is only one!|The COMMISSIONER of the BATTLE DOME!|Our "
        "own DOME ACE!|Make way for TUCKER!",
    ),
    "SpectatorTuckerChant": (
        "Spectators: TUCKER! TUCKER!|TUCKER! TUCKER! TUCKER!",
    ),
    "TuckerSilverIntro": (
        "TUCKER: Ahahah!",
        "Do you hear them? That is the crowd, and they are here for this "
        "match.",
        "Ahahah!",
        "I dare say you are shaking all over at the thought of battling me!",
        "Do not trouble yourself about it.",
        "I am the first star of the BATTLE DOME. I, TUCKER, the DOME ACE, "
        "shall bathe you in the glow.",
    ),
    "LetsSeeYourStrategy": (
        "Your strategy!|Let us see it!",
    ),
    "PlayerVersusTucker": (
        "The final match!",
        "{PLAYER} against the DOME ACE, TUCKER!",
        "Let the battle begin!",
    ),
    "IncredibleVictorIsPlayer": (
        "Unbelievable! Quite unbelievable!|The winner is {PLAYER}!",
    ),
    "WinnerIsTucker": (
        "The winner is TUCKER!|The DOME ACE has held!",
        "Congratulations, TUCKER!",
    ),
    "RefereesDecidedWinnerTucker": (
        "The REFEREES have decided!",
        "And the winner is...|Well, I never!|The winner is our own DOME ACE!|"
        "It is TUCKER!",
        "Congratulations! And thank you!|Let us hear it for the DOME ACE, "
        "TUCKER!",
    ),
    "SeeYourFrontierPass": (
        "TUCKER: Rules are rules.|Let me see your CIRCUIT PASS.",
    ),
    "ReceivedTacticsSymbol": (
        "The Tactics Symbol was struck into the CIRCUIT PASS!",
    ),
    "WontUnderestimateYouNextTime": (
        "... ... ... ... ... ...",
        "I took far too little of you seriously. I shall not make that "
        "mistake twice...",
    ),
    "CanWinStreakBeStretched": (
        "Can the run be stretched further?|The confidence is certainly "
        "there!",
    ),

    # -- and again, in gold -------------------------------------------------
    "LegendHasReturnedDomeAceTucker": (
        "Ladies and gentlemen!|Boys, girls and POKéMON!",
        "At last!|At last, the legend has come back!",
        "And the name of that legend?|Our own DOME ACE!|None other than "
        "TUCKER!",
    ),
    "TuckerGoldIntro": (
        "TUCKER: Ah...|That battering roar of theirs...|That furnace of a "
        "crowd...|What a place this is...",
        "To them I am the DOME ACE. I stand for what they hope for. I must "
        "never dim in their sight...",
        "So I must burn!|Brighter, and brighter still!|Until everyone who "
        "came here is lit by it!",
    ),
    "UnleashAllPowerIPossess": (
        "Every last part of what I have, I shall let out! Here! Now!",
    ),
    "NeverLostWhenPowerUnleashed": (
        "TUCKER: You are genuinely magnificent.",
        "Not once. Not one single time have I lost after letting it all out.",
        "Magnificent, truly.|Your CIRCUIT PASS, if you please?",
    ),
    "TacticsSymbolTookGoldenShine": (
        "The Tactics Symbol took on a golden shine!",
    ),
    "LookForwardToNextEncounter": (
        "You are strong. But more than that, there is something about you.",
        "I see in you the makings of a star of my own kind.",
        "I shall look forward very much to the next time.",
    ),
}

TARGETS: dict[str, tuple[str, ...]] = {**BUILD_UP, **CLOSED}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(PREFIX + label)}::?\n(?P<body>.*?)"
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
        lines = list(BOX.compose(tuple(glued_paragraphs)))
        if label in BUILD_UP:
            # Leave the box open: end on a paragraph break, then a bare
            # terminator, so the opponent's introduction runs on underneath.
            lines[-1] = lines[-1][:-1] + "\\p"
            lines.append("$")
        composed[label] = tuple(lines)
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
        masked = masked[:start] + '\t.string "<ARAUNA_DOME_BATTLE_ROOM_EN>"\n\n' + masked[end:]
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

    # The build-up runs straight into the opponent's own introduction. If the
    # box closes, the crowd's line and the opponent's arrive as two boxes.
    for label in BUILD_UP:
        lines = composed[label]
        if lines[-1] != "$" or not lines[-2].endswith("\\p"):
            raise ValueError(
                f"{label}: no longer leaves the message box open, so the "
                f"opponent's introduction will come up in a second box")
        # And every one of the sixteen has to be a different thing to shout.
    shouts = [flat(label) for label in BUILD_UP]
    if len(set(shouts)) != len(shouts):
        raise ValueError("two of the announcer's build-up lines read alike")

    # render_circuit_masters_en_checked.py translates these further down the
    # manifest and refuses to leave an untranslated one behind, so they have
    # to be spelled the way its table spells them.
    for label in ("MakeWayForDomeAceTucker", "TuckerSilverIntro",
                  "TuckerGoldIntro", "PlayerVersusTucker", "WinnerIsTucker",
                  "RefereesDecidedWinnerTucker",
                  "LegendHasReturnedDomeAceTucker"):
        if "TUCKER" not in flat(label) and "DOME ACE" not in flat(label):
            raise ValueError(
                f"{label}: names neither TUCKER nor the DOME ACE, so the "
                f"renderer that translates them has nothing to catch")

    # Both symbol awards have to say what was awarded and where it went.
    for label in ("ReceivedTacticsSymbol", "TacticsSymbolTookGoldenShine"):
        if "Tactics Symbol" not in flat(label):
            raise ValueError(f"{label}: no longer names the Tactics Symbol")

    # A draw is decided by REFEREES rather than by the battle, which is a
    # rule a player has met nowhere else in this facility.
    if "REFEREES" not in flat("RefereeDecisionPleaseWait"):
        raise ValueError(
            "RefereeDecisionPleaseWait: no longer says who decides a double "
            "knockout")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the BATTLE DOME floor in English.")
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
    print(f"Battle Dome battle room English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

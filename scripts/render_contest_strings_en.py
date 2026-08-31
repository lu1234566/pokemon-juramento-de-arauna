#!/usr/bin/env python3
"""Everything said aloud during a CONTEST, and every move-effect card.

Two surfaces share this file. One is the card a player reads while choosing a
move -- a two-line box 144px wide, describing what the move does to an
appeal. The other is the running commentary the JUDGE and the crowd give
while the round plays out.

Both are ladders, and that is the whole reason to compose them rather than
write them out. A player learns the CONTEST by comparing: "badly startles"
has to be worse than "slightly startles" every time it appears, and an appeal
that "went very well" has to sit above one that "went pretty well" and below
one that "went excellently". Emerald writes each rung by hand and the rungs
do not always line up. Here the grades are declared once, the sentences are
generated from them, and the renderer checks the ladders are still ordered
and still distinct.

Timing is not touched. Each commentary line ends in a run of pause codes that
holds the box open for a set number of frames; the renderer lifts that run
off the vanilla block and puts it back verbatim, so a rewording cannot
change how long the crowd is left waiting.

Left alone, and checked in place rather than rewritten: the thirteen move
names, which must be exactly what src/data/text/move_names.h prints; the five
CONTEST category names, the five condition words and the five "X Move"
labels, which are captions rather than sentences; and the empty string the
engine uses as a blank.
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

SOURCE = ROOT / "data" / "text" / "contest_strings.inc"
MOVE_NAMES = ROOT / "src" / "data" / "text" / "move_names.h"

# The card and the commentary share one narrow two-line box.
BOX = TextBox({"{STR_VAR_1}": 10, "{STR_VAR_2}": 12, "{STR_VAR_3}": 9},
              width=25)
CEILING = 144

WHOLE = ("JUDGE", "Appeal Time", "COOL", "BEAUTY", "CUTE", "SMART", "TOUGH")

CATEGORIES = ("COOL", "BEAUTY", "CUTE", "SMART", "TOUGH")

# -- the move-effect cards -------------------------------------------------
# Who a startling move reaches, and how hard. Both halves are declared once
# so "badly" is worse than "slightly" wherever the pair appears.
STARTLE_TARGETS: dict[str, str] = {
    "FrontMon": "the POKéMON in front",
    "Appealed": "those that have appealed",
}
STARTLE_GRADES: dict[str, str] = {
    "Slightly": "Slightly startles",
    "Badly": "Badly startles",
}

CARDS: dict[str, tuple[str, ...]] = {
    "HighlyAppealingMove": ("A highly appealing move.",),
    "UserMoreEasilyStartled": (
        "After this, the user is startled more easily.",),
    "GreatAppealButNoMoreToEnd": (
        "A great appeal, but allows no more to the end.",),
    "UsedRepeatedlyWithoutBoringJudge": (
        "Can be used again and again without boring the JUDGE.",),
    "AvoidStartledByOthersOnce": (
        "Can avoid being startled by others once.",),
    "AvoidStartledByOthers": ("Can avoid being startled by others.",),
    "AvoidStartledByOthersLittle": (
        "Can avoid being startled by others a little.",),
    "UserLessLikelyStartled": (
        "After this, the user is startled less easily.",),
    "StartleAppealedBeforeUser": (
        "Startles the POKéMON that appealed before the user.",),
    "StartleAllAppealed": (
        "Startles every POKéMON that has appealed.",),
    "ShiftJudgesAttentionFromOthers": (
        "Shifts the JUDGE's attention away from the others.",),
    "StartleMonHasJudgesAttention": (
        "Startles the POKéMON that has the JUDGE's attention.",),
    "JamOthersMissesTurn": (
        "Jams the others, and misses one turn of appeals.",),
    "StartleMonsMadeSameTypeAppeal": (
        "Startles POKéMON that made a same-type appeal.",),
    "MakeMonAfterUserNervous": (
        "Makes one POKéMON after the user nervous.",),
    "MakeAllMonsAfterUserNervous": (
        "Makes every POKéMON after the user nervous.",),
    "WorsenConditionOfThoseMadeAppeals": (
        "Worsens the condition of those that have appealed.",),
    "BadlyStartleMonsGoodCondition": (
        "Badly startles POKéMON in good condition.",),
    "AppealGreatIfPerformedFirst": (
        "The appeal works great if performed first.",),
    "AppealGreatIfPerformedLast": (
        "The appeal works great if performed last.",),
    "AppealAsGoodAsThoseBeforeIt": (
        "Makes the appeal as good as those before it.",),
    "AppealAsGoodAsOneBeforeIt": (
        "Makes the appeal as good as the one before it.",),
    "AppealBetterLaterItsPerformed": (
        "The appeal works better the later it is performed.",),
    "AppealVariesDependingOnTiming": (
        "The appeal's quality depends on its timing.",),
    "WorksWellIfSameTypeAsBefore": (
        "Works well if it is the same type as the one before.",),
    "WorksWellIfDifferentTypeAsBefore": (
        "Works well if it differs in type from the one before.",),
    "AffectedByAppealInFront": (
        "Affected by how well the appeal in front goes.",),
    "UpsConditionHelpsPreventNervousness": (
        "Ups the user's condition. Helps prevent nervousness.",),
    "AppealWorksWellIfConditionGood": (
        "The appeal works well if the user's condition is good.",),
    "NextAppealMadeEarlier": (
        "The next appeal can be made earlier next turn.",),
    "NextAppealMadeLater": (
        "The next appeal can be made later next turn.",),
    "TurnOrderMoreEasilyScrambled": (
        "Makes the next turn's order easier to scramble.",),
    "ScrambleOrderOfNextAppeals": (
        "Scrambles the order of appeals on the next turn.",),
    "AppealExcitesAudienceInAnyContest": (
        "An appeal that excites the audience in any CONTEST.",),
    "BadlyStartlesMonsGoodAppeals": (
        "Badly startles every POKéMON that appealed well.",),
    "AppealBestMoreCrowdExcited": (
        "The appeal works best the more the crowd is excited.",),
    "TemporarilyStopCrowdExcited": (
        "Stops the crowd growing excited, for a while.",),
}

# -- the running commentary ------------------------------------------------
# How much attention the appeal drew, weakest first. The player reads these
# one after another across a round and ranks their own by comparing.
ATTENTION: tuple[tuple[str, str], ...] = (
    ("MonFailedToStandOutAtAll", "{STR_VAR_1} did not stand out at all..."),
    ("MonDidntStandOutVeryMuch", "{STR_VAR_1} did not stand out much..."),
    ("MonCaughtALittleAttention", "{STR_VAR_1} caught a little attention."),
    ("MonAttractedALotOfAttention", "{STR_VAR_1} drew a great deal of "
                                    "attention."),
    ("MonCommandedTotalAttention", "{STR_VAR_1} commanded the whole room."),
)

# How the appeal itself went, worst first. Two of the rungs appear twice in
# the file under different labels; they are generated from one line so the
# pair cannot drift apart.
APPEAL_GRADES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("MonsAppealWasDud",), "{STR_VAR_1}'s appeal was a dud."),
    (("MonsAppealDidNotGoWell", "MonsAppealDidNotGoWell2",
      "MonsAppealDidNotGoWell3"), "{STR_VAR_1}'s appeal did not go well."),
    (("MonsAppealDidNotWorkVeryWell",),
     "{STR_VAR_1}'s appeal did not work very well."),
    (("MonsAppealWentSlightlyWell", "MonsAppealWentSlightlyWell2"),
     "{STR_VAR_1}'s appeal went slightly well."),
    (("MonsAppealWentPrettyWell", "MonsAppealWentPrettyWell2"),
     "{STR_VAR_1}'s appeal went pretty well."),
    (("MonsAppealWentVeryWell",), "{STR_VAR_1}'s appeal went very well."),
    (("MonsAppealWentExcellently", "MonsAppealWentExcellently2"),
     "{STR_VAR_1}'s appeal went excellently."),
)

# Three rungs of how a combination landed, worst first.
COMBO: tuple[tuple[str, str], ...] = (
    ("AppealComboWentOverWell", "The combination went over well."),
    ("AppealComboWentOverVeryWell", "The combination went over very well."),
    ("AppealComboWentOverExcellently",
     "The combination went over excellently."),
)

# Lines the file repeats verbatim under two labels. Kept as one entry so the
# pair cannot drift.
TWINNED: tuple[tuple[tuple[str, ...], str], ...] = (
    (("CheapenedMonsAppeal", "CheapenedMonsAppeal2"),
     "It cheapened {STR_VAR_2}'s appeal."),
    (("CheapenedAppealOfThoseAhead", "CheapenedAppealOfThoseAhead2"),
     "It cheapened the appeal of those ahead."),
    (("AnticipationSwelledForMonsAppealNext",
      "AnticipationSwelledForMonsAppealNext2"),
     "Anticipation swelled for {STR_VAR_1}'s appeal next."),
    (("TriedToStartleOtherMons", "TriedToStartleOtherPokemon"),
     "It tried to startle the other POKéMON."),
    (("ButItMessedUp", "ButItMessedUp2"), "But it messed up."),
)

COMMENTARY: dict[str, tuple[str, ...]] = {
    "AppealNumWhichMoveWillBePlayed": (
        "Appeal no. {STR_VAR_1}!|Which move will it be?",),
    "AppealNumButItCantParticipate": (
        "Appeal no. {STR_VAR_1}!|But it cannot take part!",),
    "MonAppealedWithMove": ("{STR_VAR_1} appealed with {STR_VAR_2}!",),
    "MonWasWatchingOthers": ("{STR_VAR_1} was watching the others.",),
    "AllOutOfAppealTime": ("That is the last of the Appeal Time!",),
    "ButAppealWasJammed": ("But the appeal was jammed.",),
    "FollowedAnotherMonsLead": ("It followed another POKéMON's lead.",),
    "WentBetterThanUsual": ("It went better than usual.",),
    "JudgeLookedAwayForSomeReason": (
        "The JUDGE looked away, for some reason.",),
    "WorkedHardToBuildOnPastMistakes": (
        "It worked hard to build on past mistakes.",),
    "CantMakeAnyMoreMoves": ("It can make no more moves.",),
    "WorkedFrighteninglyWell": ("It worked frighteningly well.",),
    "WorkedHardAsStandoutMon": (
        "It worked as hard as the standout POKéMON.",),
    "JudgedLookedOnExpectantly": ("The JUDGE looked on expectantly.",),
    "WorkedRatherWell": ("It worked rather well.",),
    "WorkedLittleBetterThanUsual": (
        "It worked a little better than usual.",),
    "MonHasntMadeItsAppeal": ("{STR_VAR_1} has not appealed yet.",),
    "JudgesViewsOnMonHeldFirm": (
        "The JUDGE's view of {STR_VAR_1} held firm.",),
    "MonsXChangedPerceptions": (
        "{STR_VAR_1}'s {STR_VAR_3} changed the room's mind.",),
    "MonsAppealEffectWoreOff": ("{STR_VAR_1}'s appeal effect wore off.",),
    "SpecialAppealsEffectWoreOff": (
        "The special appeal's effect wore off.",),
    "EveryonesAppealsMadeToLookSame": (
        "Everyone's appeals were made to look alike.",),
    "StoleAttentionAwayFromMon": (
        "It stole attention away from {STR_VAR_2}.",),
    "SeverelyCheapenedOtherAppeals": (
        "It severely cheapened the other appeals.",),
    "CheapenedJudgesFavoriteAppeal": (
        "It cheapened the JUDGE's favourite appeal.",),
    "AppealsOfOthersCheapenedByHalf": (
        "The appeals of the others were cheapened by half.",),
    "StoodOutToMakeUpForBeingJammed": (
        "It stood out to make up for being jammed.",),
    "CantParticipateInAppealsAnyMore": (
        "It can take no further part in the appeals.",),
    "TouchedJudgeForFantasticAppeal": (
        "It touched the JUDGE. A fantastic appeal.",),
    "AnticipationRoseForUpcomingAppeals": (
        "Anticipation rose for the appeals to come.",),
    "StoodOutAsMuchAsSpecialAppeals": (
        "It stood out as much as the special appeals.",),
    "StoodOutAsMuchAsMon": ("It stood out as much as {STR_VAR_1}.",),
    "JammedAppealsMadeEvenLessNoticeable": (
        "Jammed appeals were made less noticeable still.",),
    "EveryonesAppealsMadeSame": ("Everyone's appeals were made the same.",),
    "BecameMoreConsciousOfOtherMons": (
        "It grew more conscious of the other POKéMON.",),
    "MonCantMakeAnAppealAfterThis": (
        "{STR_VAR_1} can make no appeal after this.",),
    "SettledDownJustLittleBit": ("It settled down, just a little.",),
    "BecameObliviousToOtherMons": (
        "It became oblivious to the other POKéMON.",),
    "BecameLessAwareOfOtherMons": (
        "It became less aware of the other POKéMON.",),
    "StoppedCaringAboutOtherMons": (
        "It stopped caring about the other POKéMON.",),
    "TriedToDazzleOthers": ("It tried to dazzle the others.",),
    "JudgeLookedAwayFromMon": (
        "The JUDGE looked away from {STR_VAR_1}.",),
    "TriedToUnnerveNextMon": ("It tried to unnerve the next POKéMON.",),
    "MonBecameNervous": ("{STR_VAR_1} became nervous.",),
    "AppealTriedToUnnerveWaitingMons": (
        "The appeal tried to unnerve those still waiting.",),
    "TauntedMonsDoingWell": ("It taunted the POKéMON doing well.",),
    "MonRegainedItsForm": ("{STR_VAR_1} regained its form.",),
    "TriedToJamMonDoingWell": (
        "It tried to jam the POKéMON doing well.",),
    "StandoutMonHustledEvenMore": (
        "The standout {STR_VAR_1} hustled harder still.",),
    "LargelyUnnoticedMonWorkedHard": (
        "The largely unnoticed {STR_VAR_1} worked hard.",),
    "WorkedAsMuchAsMonBefore": (
        "It worked as much as the POKéMON before it.",),
    "WorkedAsMuchAsPrecedingMon": (
        "It worked as much as the preceding POKéMON.",),
    "SameTypeAsOneBeforeGood": (
        "Same type as the one before -- good!",),
    "NotSameTypeAsOneBeforeGood": (
        "Not the same type as the one before -- good!",),
    "StoodOutMuchMoreThanMonBefore": (
        "It stood out far more than the POKéMON before.",),
    "DidntDoAsWellAsMonBefore": (
        "It did not do as well as the POKéMON before.",),
    "MonsConditionRoseAboveUsual": (
        "{STR_VAR_1}'s condition rose above the usual.",),
    "MonsHotStatusMadeGreatAppeal": (
        "{STR_VAR_1} was on form. A great appeal!",),
    "MovedUpInLineForNextAppeal": (
        "It moved up in line for the next appeal.",),
    "MovedBackInLineForNextAppeal": (
        "It moved back one place for the next appeal.",),
    "ScrambledUpOrderForNextTurn": (
        "It scrambled the order for the next turn.",),
    "JudgeLookedAtMonExpectantly": (
        "The JUDGE looked at {STR_VAR_1} expectantly.",),
    "MonManagedToAvertGaze": ("{STR_VAR_1} managed to avert its gaze.",),
    "MonManagedToAvoidSeeingIt": (
        "{STR_VAR_1} managed not to see it.",),
    "MonIsntFazedByThatSortOfThing": (
        "{STR_VAR_1} is not fazed by that sort of thing.",),
    "MonBecameALittleDistracted": (
        "{STR_VAR_1} became a little distracted.",),
    "MonLookedDownOutOfDistraction": (
        "{STR_VAR_1} looked down, distracted.",),
    "MonTurnedBackOutOfDistraction": (
        "{STR_VAR_1} turned away, distracted.",),
    "MonCouldntHelpUtteringCry": (
        "{STR_VAR_1} could not help crying out.",),
    "MonCouldntHelpLeapingUp": ("{STR_VAR_1} could not help leaping up.",),
    "MonTrippedOutOfDistraction": (
        "{STR_VAR_1} tripped over, distracted.",),
    "MonWasTooNervousToMove": ("{STR_VAR_1} was too nervous to move.",),
    "ButItFailedToMakeTargetNervous": (
        "But it failed to make the target nervous.",),
    "ButItFailedToMakeAnyoneNervous": (
        "But it made nobody nervous at all.",),
    "ButItWasIgnored": ("But it was ignored...",),
    "CouldntImproveItsCondition": (
        "But its condition would not improve...",),
    "BadConditionResultedInWeakAppeal": (
        "Its poor condition made for a weak appeal.",),
    "MonWasUnaffected": ("{STR_VAR_1} was unaffected.",),
    "RepeatedAppeal": (
        "{STR_VAR_1} disappointed by repeating an appeal.",),
    "MonsXWentOverGreat": ("{STR_VAR_1}'s {STR_VAR_3} went over great.",),
    "MonsXDidntGoOverWell": (
        "{STR_VAR_1}'s {STR_VAR_3} did not go over well here...",),
    "MonsXGotTheCrowdGoing": (
        "{STR_VAR_1}'s {STR_VAR_3} got the crowd going.",),
    "MonCantAppealNextTurn": (
        "{STR_VAR_1} cannot appeal next turn...",),
    "AttractedCrowdsAttention": ("It caught the crowd's attention.",),
    "CrowdContinuesToWatchMon": (
        "The crowd keeps its eyes on {STR_VAR_3}.",),
    "MonsMoveIsIgnored": ("{STR_VAR_1}'s {STR_VAR_2} is ignored.",),
}

# Captions and names, checked in place rather than rewritten.
UNTOUCHED_MOVE_NAMES: dict[str, str] = {
    "gText_RainDance": "RAIN DANCE",
    "gText_Rage": "RAGE",
    "gText_FocusEnergy": "FOCUS ENERGY",
    "gText_Hypnosis": "HYPNOSIS",
    "gText_Softboiled": "SOFTBOILED",
    "gText_HornAttack": "HORN ATTACK",
    "gText_SwordsDance": "SWORDS DANCE",
    "gText_Conversion": "CONVERSION",
    "gText_SunnyDay": "SUNNY DAY",
    "gText_Rest2": "REST",
    "gText_Vicegrip": "VICEGRIP",
    "gText_DefenseCurl": "DEFENSE CURL",
    "gText_LockOn": "LOCK-ON",
}


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = {}
    for suffix, body in CARDS.items():
        blocks[f"gText_{suffix}"] = body
    for grade, verb in STARTLE_GRADES.items():
        for target, who in STARTLE_TARGETS.items():
            blocks[f"gText_{grade}Startle{target}"] = (f"{verb} {who}.",)
    for category in CATEGORIES:
        blocks[f"gText_BadlyStartle{category.title()}Appeals"] = (
            f"Badly startles POKéMON that made {category} appeals.",)
    # The engine keeps a second copy of two cards; generate both from one
    # line so the pair cannot come apart.
    blocks["gText_StartleAppealedBeforeUser2"] = \
        blocks["gText_StartleAppealedBeforeUser"]
    blocks["gText_StartleAllAppealed2"] = blocks["gText_StartleAllAppealed"]

    for suffix, body in COMMENTARY.items():
        blocks[f"gText_{suffix}"] = body
    for suffix, line in ATTENTION:
        blocks[f"gText_{suffix}"] = (line,)
    for labels, line in APPEAL_GRADES:
        for suffix in labels:
            blocks[f"gText_{suffix}"] = (line,)
    for suffix, line in COMBO:
        blocks[f"gText_{suffix}"] = (line,)
    for labels, line in TWINNED:
        for suffix in labels:
            blocks[f"gText_{suffix}"] = (line,)
    return blocks


TARGETS: dict[str, tuple[str, ...]] = build()

TRAILING_CODES = re.compile(r"((?:\{[A-Z_0-9 ]+\})+)\$$")


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def trailing_codes(source: str) -> dict[str, str]:
    """The pause run each vanilla block ends on, to be put back verbatim.

    These hold the message box open for a set number of frames. A rewording
    has no business changing how long the crowd is left waiting, so the run
    is lifted off the original and reattached rather than retyped.
    """
    codes: dict[str, str] = {}
    for label in TARGETS:
        body = block_pattern(label).search(source).group("body")
        payloads = re.findall(r'\.string "(.*?)"', body)
        if not payloads:
            raise ValueError(f"{label}: no .string payload to read timing from")
        match = TRAILING_CODES.search(payloads[-1])
        codes[label] = match.group(1) if match else ""
    return codes


def payloads(source: str) -> dict[str, tuple[str, ...]]:
    codes = trailing_codes(source)
    composed = {}
    for label, paragraphs in TARGETS.items():
        glued_paragraphs = []
        for paragraph in paragraphs:
            for name in WHOLE:
                paragraph = paragraph.replace(name, glued(name))
            glued_paragraphs.append(paragraph)
        lines = list(BOX.compose(tuple(glued_paragraphs)))
        if codes[label]:
            lines[-1] = lines[-1][:-1] + codes[label] + "$"
        composed[label] = tuple(lines)
    return composed


def render(source: str) -> str:
    composed = payloads(source)
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
        masked = masked[:start] + '\t.string "<ARAUNA_CONTEST_STRINGS_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    composed = payloads(source)
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

    composed = payloads(source)
    ruler = Ruler()
    move_names = MOVE_NAMES.read_text(encoding="utf-8")
    codes = trailing_codes(source)

    def flat(label: str) -> str:
        """The words only: pause runs are timing, and are checked separately."""
        text = "".join(composed[label])
        text = re.sub(r"\{PAUSE[^}]*\}", "", text)
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ", text)).strip().rstrip("$")

    # Timing is the engine's, not the writer's.
    for label, run in codes.items():
        if run and not composed[label][-1].endswith(run + "$"):
            raise ValueError(
                f"{label}: lost the pause run the vanilla block ended on, so "
                f"the box will close after a different number of frames")

    # A card that overruns is cut off mid-sentence, and the card is the only
    # place a move's effect is ever stated.
    for label in TARGETS:
        for payload in composed[label]:
            width = ruler.widest(payload)
            if width > CEILING:
                raise ValueError(
                    f"{label}: {width}px, past the {CEILING}px this box shows")

    # Startling is graded, and the grade has to survive both halves of the
    # pair or a player comparing two moves is comparing nothing.
    for target in STARTLE_TARGETS:
        slight = flat(f"gText_SlightlyStartle{target}")
        badly = flat(f"gText_Badly Startle{target}".replace(" ", ""))
        if "Slightly" not in slight or "Badly" not in badly:
            raise ValueError(
                f"Startle{target}: the two grades are no longer marked, so "
                f"the pair reads as the same effect")
        if slight == badly:
            raise ValueError(f"Startle{target}: both grades read alike")

    # Five categories, five cards, each naming its own.
    for category in CATEGORIES:
        card = flat(f"gText_BadlyStartle{category.title()}Appeals")
        if category not in card:
            raise ValueError(
                f"BadlyStartle{category.title()}Appeals: no longer names "
                f"{category}")

    # The two ladders a player ranks their own round by.
    for name, rungs in (("attention", [flat(f"gText_{s}") for s, _ in ATTENTION]),
                        ("appeal", [flat(f"gText_{labels[0]}")
                                    for labels, _ in APPEAL_GRADES]),
                        ("combo", [flat(f"gText_{s}") for s, _ in COMBO])):
        if len(set(rungs)) != len(rungs):
            raise ValueError(
                f"two rungs of the {name} ladder read alike, so a player "
                f"cannot tell a better round from a worse one")

    # Lines the engine keeps two copies of stay two copies of one line.
    for labels, _line in TWINNED + APPEAL_GRADES:
        said = {flat(f"gText_{suffix}") for suffix in labels}
        if len(said) != 1:
            raise ValueError(
                f"{labels}: the engine's duplicate copies have drifted apart")

    # The thirteen move names here are captions on the same moves the party
    # screen lists, so they have to be spelled the way it spells them.
    for label, name in UNTOUCHED_MOVE_NAMES.items():
        if f'_("{name}")' not in move_names:
            raise ValueError(
                f"{label}: {name!r} is not a name in move_names.h")
        body = block_pattern(label).search(rendered)
        if body is None or f'"{name}$"' not in body.group("body"):
            raise ValueError(f"{label}: no longer reads {name!r}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the CONTEST commentary and move cards in English.")
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
    print(f"Contest strings English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

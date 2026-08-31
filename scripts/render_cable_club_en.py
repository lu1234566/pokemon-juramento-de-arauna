#!/usr/bin/env python3
"""The link floor: TEALA's tour, the counters, and the wireless minigames.

Almost everything on this floor is instructions, and instructions that are
merely pleasant are useless. A player reading these has a cable or an adapter
in their hand and a friend waiting, and needs to come away knowing which room
to stand in and what the hardware will and will not do.

So the facts are load-bearing and are checked rather than trusted: the two
rooms and which is which, that a cable sends you to the DIRECT CORNER, the
player counts each service takes, the Lv. 30 cap in the UNION ROOM, and the
height limit on POKéMON JUMP. Every one of those is something a player can be
stopped by, and prose that loses one has made the floor harder to use than
Emerald's.

What is rewritten is the shape. TEALA gives the same tour twice -- once on
your first visit and once on request -- and Emerald keeps two hand-maintained
copies of it that have already drifted apart by a sentence. Here the tour is
written once and the two versions differ only where they should: the first
walks you upstairs, the second assumes you know the way.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

CLUB = ROOT / "data" / "text" / "cable_club.inc"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 12, "{STR_VAR_2}": 12,
               "{PLUS}": 1}, width=34)

WHOLE = ("UNION ROOM", "DIRECT CORNER", "RECORD CORNER", "BERRY CRUSH",
         "BERRY POWDER", "Wireless Adapter", "Game Link", "TRAINER CARD",
         "POKéMON CENTER", "WIRELESS CLUB", "CABLE CLUB", "SINGLE BATTLE",
         "DOUBLE BATTLE", "MULTI BATTLE", "VINE WHIP", "Lv. 30",
         "Control Pad", "A Button", "B Button", "GAME CORNER")


def tour(first_time: bool) -> tuple[str, ...]:
    """The two rooms upstairs, told once. Only the framing differs."""
    body = (
        "There are two rooms on this floor.",
        "The one on the left is the UNION ROOM.",
        "In there you link with whoever else nearby has gone in -- people "
        "you know and people you don't.",
        "You can talk, battle and trade with them.",
        "The one on the right is the DIRECT CORNER.",
        "That one is for trading and battling with friends of your own.",
    )
    if first_time:
        return body + (
            "And if the Wireless Adapter isn't connected, you can still link "
            "on a GBA Game Link cable -- but then it has to be the DIRECT "
            "CORNER.",
            "I hope you get some use out of it.",
        )
    return body + (
        "If you can't find your friends in either room, move closer to them. "
        "That is usually all it is.",
        "And if the Wireless Adapter isn't connected, you can still link on a "
        "GBA Game Link cable -- but then it has to be the DIRECT CORNER.",
        "I hope you get some use out of it.",
    )


TARGETS: dict[str, tuple[str, ...]] = {
    # -- the counter ----------------------------------------------------------
    "CableClub_Text_WelcomeWhichCableClubService": (
        "Welcome to the POKéMON CABLE CLUB.",
        "Which of our services would you like?",
    ),
    "CableClub_Text_WhichService": (
        "Which of our services would you like?",
    ),
    "CableClub_Text_TradeUsingLinkCable": (
        "Trade POKéMON with another player over a GBA Game Link cable.",
    ),
    "CableClub_Text_BattleUsingLinkCable": (
        "Battle another TRAINER over a GBA Game Link cable.",
    ),
    "CableClub_Text_RecordCornerUsingLinkCable": (
        "Use the RECORD CORNER with others over a GBA Game Link cable.",
    ),
    "CableClub_Text_CloseThisMenu": (
        "Close this menu.",
    ),
    "CableClub_Text_CancelSelectedItem": (
        "Cancels the selected MENU item.",
    ),
    "CableClub_Text_ReturnsToPreviousStep": (
        "Returns to the previous step.",
    ),
    "CableClub_Text_NeedTwoMonsForDoubleBattle": (
        "A DOUBLE BATTLE needs at least two POKéMON.",
    ),
    "CableClub_Text_NeedTwoMonsToTrade": (
        "To trade you need at least two POKéMON with you.",
    ),
    "CableClub_Text_CantTradeEnigmaBerry": (
        "A POKéMON holding the {STR_VAR_1} BERRY can't be traded.",
    ),
    "CableClub_Text_NeedBerryForBerryCrush": (
        "BERRY CRUSH needs at least one BERRY.",
    ),
    "CableClub_Text_NeedTwoMonsForUnionRoom": (
        "To go into the UNION ROOM you need at least two POKéMON.",
    ),
    "CableClub_Text_NoEnigmaBerryInUnionRoom": (
        "No POKéMON holding the {STR_VAR_1} BERRY may go into the UNION "
        "ROOM.",
    ),
    "CableClub_Text_OkayToSaveProgress": (
        "Your progress has to be saved before linking. May I save?",
    ),
    "CableClub_Text_PleaseEnter": (
        "In you go.",
    ),
    "CableClub_Text_DirectYouToYourRoom": (
        "I'll show you to your room.",
    ),
    "CableClub_Text_PleaseVisitAgain": (
        "Do come again.",
    ),
    "CableClub_Text_HopeToSeeYouAgain": (
        "I hope to see you again!",
    ),
    "CableClub_Text_Hello": (
        "Hello!",
    ),
    "CableClub_Text_PleaseWait": (
        "One moment.",
    ),
    "CableClub_Text_ParticipantsStepUpToCounter": (
        "Would everyone taking part come up to the counter, please.",
    ),

    # -- what the machine says ------------------------------------------------
    "gText_PleaseWaitForLink": (
        "Please wait.|... ... B Button: Cancel",
    ),
    "gText_ConfirmLinkWhenPlayersReady": (
        "When everyone is ready...|A Button: Confirm|B Button: Cancel",
    ),
    "gText_ConfirmStartLinkWithXPlayers": (
        "Start link with {STR_VAR_1} players.|A Button: Confirm|B Button: "
        "Cancel",
    ),
    "gText_AwaitingLinkup": (
        "Awaiting linkup...|... ... B Button: Cancel",
    ),
    "Text_SomeoneIsNotReadyToLink": (
        "Somebody isn't ready to link.",
        "Come back when everyone has sorted themselves out.",
    ),
    "Text_LinkErrorPleaseReset": (
        "Sorry -- a link error.|Reset and try again.",
    ),
    "Text_PlayersMadeDifferentSelections": (
        "The players seem to have chosen different things.",
    ),
    "CableClub_Text_IncorrectNumberOfParticipants": (
        "That is the wrong number of players.",
    ),
    "CableClub_Text_CantSingleBattleWithXPlayers": (
        "SINGLE BATTLE can't be played by {STR_VAR_1} players.",
    ),
    "CableClub_Text_CantDoubleBattleWithXPlayers": (
        "DOUBLE BATTLE can't be played by {STR_VAR_1} players.",
    ),
    "CableClub_Text_NeedFourPlayers": (
        "That Battle Mode needs four players.",
    ),
    "CableClub_Text_PleaseConfirmNumberAndRestart": (
        "Check how many of you there are and start again.",
    ),
    "Text_TerminateLinkConfirmation": (
        "Leaving the room ends the link. Is that all right?",
    ),
    "Text_TerminateLinkPleaseWait": (
        "Ending the link...|You'll be shown out. One moment.",
    ),
    "CableClub_Text_AdapterNotConnected": (
        "The Wireless Adapter isn't connected properly.",
    ),
    "CableClub_Text_OtherTrainerNotReady": (
        "The other TRAINER isn't ready.",
    ),
    "CableClub_Text_YouHaveAMonThatCantBeTaken": (
        "At least one of your POKéMON can't be taken.",
    ),
    "CableClub_Text_NotSetUpForFarAwayRegion": (
        "I'm terribly sorry.",
        "We aren't set up to trade with TRAINERS as far off as another "
        "region yet...",
    ),
    "CableClub_Text_CantMixWithJapaneseGame": (
        "Sorry -- a transmission error.",
        "You can't mix records with Japanese Ruby or Sapphire games.",
        "And you can't mix Japanese Emerald with overseas Ruby or Sapphire at "
        "the same time.",
    ),
    "CableClub_Text_TrainerCardDataOverwritten": (
        "The TRAINER CARD data will be overwritten.",
    ),

    # -- the rooms ------------------------------------------------------------
    "BattleColosseum_2P_Text_TakePlaceStartBattle": (
        "Take your place and start your battle.",
    ),
    "TradeCenter_Text_TakeSeatStartTrade": (
        "Take your seat and start your trade.",
    ),
    "RecordCorner_Text_ThanksForComing": (
        "Thanks for coming.",
    ),
    "RecordCorner_Text_TakeSeatAndWait": (
        "Take your seat and wait.",
    ),
    "RecordCorner_Text_PlayerSentOverOneX": (
        "{STR_VAR_1} sent over one {STR_VAR_2}.",
    ),
    "CableClub_Text_TooBusyToNotice": (
        "This TRAINER is too busy to notice you...",
    ),
    "CableClub_Text_GotToLookAtTrainerCard": (
        "Got a look at {STR_VAR_1}'s TRAINER CARD!",
    ),
    "CableClub_Text_GotToLookAtColoredTrainerCard": (
        "Got a look at {STR_VAR_1}'s TRAINER CARD!",
        "It's a {STR_VAR_2} one!",
    ),
    "CableClub_Text_OhExcuseMe": (
        "Oh...|Excuse me!",
    ),
    "CableClub_Text_PlayerIsWaiting": (
        "{STR_VAR_1} seems to be playing just now.|Go on, then!",
    ),

    # -- the wireless counter -------------------------------------------------
    "CableClub_Text_YouMayTradeHere": (
        "You may trade POKéMON here with another TRAINER.",
    ),
    "CableClub_Text_YouMayBattleHere": (
        "You may battle your friends here.",
    ),
    "CableClub_Text_CanMakeBerryPowder": (
        "Two to five TRAINERS can make BERRY POWDER together.",
    ),
    "CableClub_Text_CanMixRecords": (
        "The records of two to four players can be mixed.",
    ),
    "CableClub_Text_GuideToVariousServices": (
        "A guide to what the WIRELESS CLUB offers.",
    ),
    "CableClub_Text_WhichBattleMode": (
        "Which battle mode would you like?",
    ),
    "CableClub_Text_PlayWhichBattleMode": (
        "Which Battle Mode would you like to play?",
    ),
    "CableClub_Text_TradePokemon": (
        "Would you like to trade POKéMON?",
    ),
    "CableClub_Text_AccessRecordCorner": (
        "Would you like the RECORD CORNER?",
    ),
    "CableClub_Text_UseBerryCrush": (
        "Would you like the BERRY CRUSH System?",
    ),
    "CableClub_Text_ExplainBattleModes": (
        "There are three Battle Modes.",
        "SINGLE BATTLE: two TRAINERS, one or more POKéMON each, one out at a "
        "time.",
        "DOUBLE BATTLE: two TRAINERS, two or more POKéMON each, two out at a "
        "time.",
        "MULTI BATTLE: four TRAINERS, one or more POKéMON each, one out at a "
        "time.",
    ),
    "CableClub_Text_ChooseGroupLeaderOfTwo": (
        "Decide between the two of you who is the LEADER.",
        "The other must then choose “JOIN GROUP.”",
    ),
    "CableClub_Text_ChooseGroupLeaderOfFour": (
        "Decide among the four of you who is the GROUP LEADER.",
        "The rest must then choose “JOIN GROUP.”",
    ),
    "CableClub_Text_ChooseGroupLeader": (
        "Decide among yourselves who is the GROUP LEADER.",
        "The rest must then choose “JOIN GROUP.”",
    ),
    "CableClub_Text_WelcomeWhichDirectCornerRoom": (
        "Welcome to the POKéMON WIRELESS CLUB DIRECT CORNER.",
        "This is where you deal with friends of your own.",
        "Which room would you like?",
    ),
    "CableClub_Text_WelcomeUnionRoomEnter": (
        "Welcome to the POKéMON WIRELESS CLUB UNION ROOM.",
        "In here you meet other TRAINERS directly -- including ones you have "
        "never met.",
        "Would you like to go in?",
    ),
    "CableClub_Text_UnionRoomInfo": (
        "The TRAINERS in the UNION ROOM are whoever near you has also gone "
        "in.",
        "You can do a good deal in there. Greetings, to begin with.",
        "You may enter two POKéMON up to Lv. 30 for a one-on-one battle.",
        "You may join a chat of two to five people.",
        "Or you may put a POKéMON up for trade.",
        "Would you like to go in?",
    ),
    "CableClub_Text_EnjoyUnionRoom": (
        "I hope you enjoy the UNION ROOM.",
    ),
    "CableClub_Text_UnionRoomAdapterNotConnected": (
        "This is the POKéMON WIRELESS CLUB UNION ROOM.",
        "Your Wireless Adapter isn't connected properly, I'm afraid.",
        "Do come again.",
    ),
    "CableClub_Text_HopeYouEnjoyWirelessSystem": (
        "I hope you get some use out of the Wireless Communication System.",
    ),

    # -- TEALA ----------------------------------------------------------------
    "CableClub_Text_FirstTimeRightThisWay": (
        "Hello!|My name is TEALA.",
        "This is your first time up here, isn't it.",
        "Let me show you how the Wireless Communication System works.",
        "Starting with this floor of the POKéMON CENTER.",
        "This way, please.",
    ),
    "CableClub_Text_ExplainWirelessClubFirstTime": tour(True),
    "CableClub_Text_AskAboutLinking": (
        "Hello, {PLAYER}!",
        "TEALA, from the POKéMON CENTER 2F.",
        "Was there something you wanted to ask about linking?",
    ),
    "CableClub_Text_ExplainWirelessClub": (
        "Let me go over how the POKéMON WIRELESS CLUB works.",
    ) + tour(False),

    # -- the game corner ------------------------------------------------------
    "MossdeepCity_GameCorner_1F_Text_DescribeWhichGame": (
        "I can go through the rules, if you like.",
        "Which game?",
    ),
    "MossdeepCity_GameCorner_1F_Text_PokemonJumpInfo": (
        "“POKéMON JUMP”",
        "Your POKéMON skips a VINE WHIP rope. You time the jump with the A "
        "Button.",
        "Only small POKéMON -- around 28 inches or less -- can take part.",
        "And POKéMON that only swim, burrow or fly are no good at jumping, so "
        "they can't either.",
        "Good things happen when everyone jumps together.",
    ),
    "MossdeepCity_GameCorner_1F_Text_DodrioBerryPickingInfo": (
        "“DODRIO BERRY-PICKING”",
        "You work all three of a Piuiuim's heads to catch falling BERRIES.",
        "Right, up and left on the {PLUS} Control Pad move the heads.",
        "You need a Piuiuim to play it at all.",
    ),
    "MossdeepCity_GameCorner_1F_Text_TalkToOldManToPlay": (
        "If you want a game, have a word with the old man beside me.",
    ),
    "MossdeepCity_GameCorner_1F_Text_WelcomeCanYouWait": (
        "Hello, welcome!|Here for the wireless games?",
        "Can you give me just a moment?",
    ),
    "MossdeepCity_GameCorner_1F_Text_ComeAgain": (
        "Right you are. Come again!",
    ),
    "MossdeepCity_GameCorner_1F_Text_AdapterNotConnected": (
        "The Wireless Adapter isn't connected.|Come back when it's hooked "
        "up!",
    ),
    "MossdeepCity_GameCorner_1F_Text_PlayWhichGame": (
        "Right -- which game did you want?",
    ),
    "MossdeepCity_GameCorner_1F_Text_EnterWhichPokemon": (
        "Which POKéMON would you like to enter?",
    ),
    "MossdeepCity_GameCorner_1F_Text_AllGoodToGo": (
        "There you are, all set.|Don't let the others have it!",
    ),
    "MossdeepCity_GameCorner_1F_Text_LeavingDoComeAgain": (
        "Off already?|Do come again!",
    ),
    "MossdeepCity_GameCorner_1F_Text_ExplainRequiredMon": (
        "It doesn't look like you have anything you can enter...",
        "Shall I go through what can?",
    ),
    "MossdeepCity_GameCorner_1F_Text_ShortJumpingPokemonAllowed": (
        "“POKéMON JUMP” is for POKéMON around 28 inches or less.",
        "What you can't bring is anything that doesn't jump.",
        "The ones that only swim, or burrow, or fly.",
        "That's the whole of it.",
    ),
    "MossdeepCity_GameCorner_1F_Text_OnlyDodrioAllowed": (
        "DODRIO BERRY-PICKING is for Piuiuim and nothing else.",
    ),
    "MossdeepCity_GameCorner_1F_Text_RetryPlease": (
        "Could you start that over, please?",
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
        masked = masked[:start] + '\t.string "<ARAUNA_CABLE_CLUB_EN>"\n\n' + masked[end:]
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
        return re.sub(r"\\[npl]", " ", "".join(composed[label]))

    # Both tellings of the tour must name both rooms, say which is which, and
    # say where a cable sends you. That is the whole point of the tour.
    for label in ("CableClub_Text_ExplainWirelessClubFirstTime",
                  "CableClub_Text_ExplainWirelessClub"):
        text = flat(label)
        for room in ("UNION ROOM", "DIRECT CORNER"):
            if room not in text:
                raise ValueError(f"{label}: no longer names the {room}")
        if "left" not in text or "right" not in text:
            raise ValueError(f"{label}: no longer says which room is which")
        if "Game Link" not in text or "DIRECT CORNER" not in text:
            raise ValueError(
                f"{label}: no longer says a cable sends you to the DIRECT "
                f"CORNER")

    # Player counts and caps are things a player is stopped by.
    if "two to five" not in flat("CableClub_Text_CanMakeBerryPowder").lower():
        raise ValueError("BERRY POWDER lost how many players it takes")
    if "two to four" not in flat("CableClub_Text_CanMixRecords").lower():
        raise ValueError("record mixing lost how many players it takes")
    union = flat("CableClub_Text_UnionRoomInfo")
    if "Lv. 30" not in union:
        raise ValueError("UnionRoomInfo: lost the Lv. 30 cap")
    if "two to five" not in union.lower():
        raise ValueError("UnionRoomInfo: lost how many people a chat takes")

    # The three battle modes each state a player count and how many come out.
    modes = flat("CableClub_Text_ExplainBattleModes")
    for mode, players in (("SINGLE BATTLE", "two"), ("DOUBLE BATTLE", "two"),
                          ("MULTI BATTLE", "four")):
        if mode not in modes:
            raise ValueError(f"ExplainBattleModes: no longer names {mode}")
        _ = players
    for count in ("two TRAINERS", "four TRAINERS"):
        if count not in modes:
            raise ValueError(f"ExplainBattleModes: no longer says {count}")

    # The two minigames have entry conditions that decide whether a player can
    # play at all.
    for label in ("MossdeepCity_GameCorner_1F_Text_PokemonJumpInfo",
                  "MossdeepCity_GameCorner_1F_Text_ShortJumpingPokemonAllowed"):
        if "28 inches" not in flat(label):
            raise ValueError(f"{label}: lost the height limit")
    for label in ("MossdeepCity_GameCorner_1F_Text_DodrioBerryPickingInfo",
                  "MossdeepCity_GameCorner_1F_Text_OnlyDodrioAllowed"):
        if "Piuiuim" not in flat(label):
            raise ValueError(f"{label}: lost the only POKéMON that can play it")

    # TEALA is a person with a name, and says it once on each of her two
    # openings.
    for label in ("CableClub_Text_FirstTimeRightThisWay",
                  "CableClub_Text_AskAboutLinking"):
        if "TEALA" not in flat(label):
            raise ValueError(f"{label}: the attendant lost her name")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the link floor and its counters in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = CLUB.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        CLUB.write_text(rendered, encoding="utf-8")
    print(f"Cable club English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

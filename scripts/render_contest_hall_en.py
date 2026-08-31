#!/usr/bin/env python3
"""The CONTEST hall: the counter that enters you, and the MC who runs the room.

Two voices, and they are not the same person. The receptionist is polite and
brisk and is mostly delivering rules; the MC is working an audience and never
once stops selling it. Emerald writes them in the same register, which is why
its hall feels like one desk with a microphone on it.

The rank ladder is the piece of information a player actually needs from this
building -- win at NORMAL and that POKéMON may go up to SUPER in the same
category, and so on to MASTER, which can be entered as often as you like. It
is stated as a ladder here rather than as four sentences that each repeat the
one before.

Several blocks exist two or three times over because three different counters
ask the same question. Those are generated from one string apiece: three
hand-maintained copies of "Which CONTEST would you like to enter?" is three
chances for one of them to end up asking something else.

The link modes keep their hardware facts exactly. E-MODE and G-MODE, the
cable, the Wireless Adapter and the Game Pak a linking player must own are
compatibility requirements, not flavour, and a player who is told the wrong
one cannot connect.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

HALL = ROOT / "data" / "scripts" / "contest_hall.inc"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 12, "{STR_VAR_2}": 12,
               "{STR_VAR_3}": 12, "{POKEBLOCK}": 9}, width=34)

WHOLE = ("POKéMON CONTEST", "POKéMON CONTESTS", "Game Link", "Wireless Adapter",
         "Wireless Adapters", "Game Pak", "GROUP LEADER", "JOIN GROUP",
         "MASTER Rank", "NORMAL Rank", "SUPER Rank", "HYPER Rank",
         "Entry No.", "reception counter")

# The four ranks, in the order a POKéMON climbs them.
RANKS = ("NORMAL", "SUPER", "HYPER", "MASTER")

# Questions three separate counters ask, written once each.
SHARED = {
    "EnterWhichContest": "Which CONTEST would you like to enter?",
    "EnterWhichPokemon": "Which POKéMON would you like to enter?",
    "EggCannotTakePart": "I'm sorry, but an EGG cannot take part in a "
                         "POKéMON CONTEST.",
    # The first counter spells this label out in full; the later ones do not.
    "MonInNoConditionForContest": "Your POKéMON does not appear to be in any "
                                  "condition for a CONTEST...",
    "MonInNoCondition": "Your POKéMON does not appear to be in any condition "
                        "for a CONTEST...",
    "ParticipateAnotherTime": "We hope you'll take part another time.",
    "WhichTopic": "Which would you like to hear about?",
    "EnterContest": "Would you like to enter a CONTEST?",
}

TARGETS: dict[str, tuple[str, ...]] = {
    # -- the counter ----------------------------------------------------------
    "ContestReception": (
        "Hello!",
        "This is the reception counter for POKéMON CONTESTS.",
    ),
    "ReceptionDontHavePokeblockCase": (
        "Hello!",
        "This is the reception counter for POKéMON CONTESTS.",
        "Oh? It seems you haven't a {POKEBLOCK} CASE yet.",
        "Then we had better see to that first.",
    ),
    "NowThatWeveClearedThatUp": (
        "There. That's seen to.",
        "Hello!",
        "This is the reception counter for POKéMON CONTESTS.",
    ),
    "CounterOnlyFor4PlayerContests": (
        "Hello!",
        "This counter takes entries for four-player POKéMON CONTESTS only.",
    ),
    "EnterContest1": (
        "Would you like to enter one of your POKéMON in our CONTESTS?",
    ),
    "ExplainContests": (
        "A POKéMON CONTEST is four TRAINERS, one POKéMON each, judged "
        "against one another.",
        "There are two rounds of judging.",
        "The first is the audience's. They vote for the POKéMON they like "
        "best.",
        "The second is the appeals, where the POKéMON use their moves.",
        "Plan those appeals. You want the JUDGE watching you and the hall "
        "on its feet.",
        "The two scores are added at the end, and the highest wins.",
    ),
    "ExplainContestTypes": (
        "There are five kinds of CONTEST.",
        "COOL, BEAUTY, CUTE, SMART and TOUGH.",
        "Choose the one that suits the POKéMON you mean to enter.",
    ),
    "ExplainContestRanks": (
        "There are four ranks, and they are a ladder.",
        "NORMAL, then SUPER, then HYPER, then MASTER.",
        "Any POKéMON may enter at NORMAL.",
        "Win a rank and that POKéMON may go up to the next -- but only in "
        "the same category.",
        "And once it has won at MASTER, it may enter MASTER as often as its "
        "TRAINER likes.",
    ),
    "EnterWhichRank": (
        "Which Rank would you like to enter?",
    ),
    "MonNotQualifiedForRank": (
        "I'm very sorry, but your POKéMON isn't qualified for this Rank "
        "yet...",
    ),
    "AlreadyWonEnterAnyway": (
        "Oh -- that RIBBON...",
        "Your POKéMON has won this CONTEST before, hasn't it?",
        "Would you like to enter it again all the same?",
    ),
    "ConfirmContestMon": (
        "Is that your CONTEST POKéMON?",
    ),
    "YourMonIsEntryNum4": (
        "Very good. Your POKéMON is entered.",
        "You are Entry No. 4.|The CONTEST begins shortly.",
    ),
    "YourMonIsEntryNumX": (
        "Your POKéMON is entered in the CONTEST.",
        "You are Entry No. {STR_VAR_2}.",
    ),
    "ContestBeginShortly": (
        "The CONTEST begins shortly.",
    ),
    "ComeThroughHere": (
        "Through here, please.|Good luck!",
    ),
    "PokemonWonWeHavePrize": (
        "Congratulations! Your POKéMON has won the CONTEST!",
        "Your prize is here. This way, please!",
    ),
    "ComeBackForPrizeLater": (
        "Do come back for your prize later.",
    ),
    "PickUpPrizeAtCounterLater": (
        "Collect your prize at the reception counter later.",
        "And do compete again!",
    ),
    "ProgressWillBeSaved": (
        "Before the CONTEST begins, your progress will be saved.",
    ),

    # -- the MC ---------------------------------------------------------------
    "GettingStartedParticipantsAsFollows": (
        "MC: Good day! We are about to begin a {STR_VAR_3} Rank POKéMON "
        "{STR_VAR_2}!",
        "Your TRAINERS this afternoon, and their POKéMON:",
    ),
    "GettingStartedParticipantsAsFollowsLink": (
        "MC: Good day! We are about to begin a four-player linked POKéMON "
        "{STR_VAR_2}!",
        "Your TRAINERS this afternoon, and their POKéMON:",
    ),
    "GettingStartedWireless": (
        "MC: Good day! We are about to begin a four-player linked POKéMON "
        "{STR_VAR_2}!",
    ),
    "ParticipantsAsFollows": (
        "Your TRAINERS this afternoon, and their POKéMON:",
    ),
    "EntryXTrainersMon": (
        "MC: Entry No. {STR_VAR_2}!|{STR_VAR_1}'s {STR_VAR_3}!",
    ),
    "SeenContestantsAudienceWillVote": (
        "MC: And there are our four.",
        "Which brings us to the first round of judging!",
        "The hall votes for the POKéMON it likes best.",
        "So without another word from me -- let the voting begin!",
    ),
    "WeveSeenContestants": (
        "MC: And there are our four.",
        "Which brings us to the first round of judging!",
    ),
    "AudienceWillVote": (
        "The hall votes for the POKéMON it likes best.",
    ),
    "LetVotingBegin": (
        "So without another word from me -- let the voting begin!",
    ),
    "VotingUnderWay": (
        "Voting under way...",
    ),
    "VotingCompleteLetsAppeal": (
        "Voting is closed!",
        "And while they are counted, we move to the second round of judging!",
        "Which is the part you came for -- the appeals!",
        "Let our four astonish us!",
        "A little noise, if you please!|Let's appeal!",
    ),
    "VotingComplete": (
        "Voting is closed!",
        "And while they are counted, we move to the second round of judging!",
    ),
    "SecondStageOfJudging": (
        "Which is the part you came for -- the appeals!",
        "Let our four astonish us!",
    ),
    "LetsAppeal": (
        "A little noise, if you please!|Let's appeal!",
    ),
    "ThatsItForJudging": (
        "MC: And that is the judging done!",
    ),
    "ThankYouForAppeals": (
        "Thank you, every one of you, for appeals of that quality!",
        "The judging is closed. You have all done well.",
    ),
    "JudgeLooksReady": (
        "Which leaves only the announcement, and I can feel this hall "
        "holding its breath.",
        "The JUDGE is ready.",
    ),
    "WeWillNowDeclareWinner": (
        "JUDGE: I shall now declare the winner.",
    ),
    "CongratsTrainerXandMon": (
        "MC: Entry No. {STR_VAR_2}!",
        "{STR_VAR_3} and {STR_VAR_1} -- congratulations!",
    ),
    "CongratsPleaseCompeteAgain": (
        "MC: Congratulations!|And do compete again!",
    ),
    "AcceptYourPrize": (
        "MC: Here you are!|Your prize, with our compliments!",
    ),
    "ConferRibbonAsPrize": (
        "This RIBBON is yours.",
    ),
    "ReceivedRibbon": (
        "{PLAYER} received a RIBBON.",
    ),
    "PutRibbonOnMon": (
        "{PLAYER} put the RIBBON on {STR_VAR_1}.",
    ),

    # -- the linked counters --------------------------------------------------
    "OnlyRegister4Players": (
        "I register four players for a POKéMON CONTEST, and no other number.",
        "Link three others to yourself and all four may enter the same "
        "CONTEST.",
        "Would you like to take part?",
    ),
    "Explain4PlayerContest": (
        "When four of you are ready, connect over a Game Link cable and "
        "register with me.",
        "Choose the same CONTEST as the others.",
        "It begins as soon as all four have registered.",
        "After that the usual CONTEST rules apply.",
    ),
    "LinkContestReception": (
        "Welcome. This is the POKéMON CONTEST link counter.",
        "You may enter alongside one or more friends here.",
    ),
    "Transmitting": (
        "Transmitting...",
    ),
    "TransmissionError": (
        "Transmission error...",
    ),
    "TransmissionErrorTryAgain": (
        "Transmission error.|Please try again.",
    ),
    "PlayersChoseDifferentContest": (
        "One of you may have chosen a different CONTEST from the others.",
    ),
    "PlayersMadeDifferentChoice": (
        "One of you may have made a different choice from the others.",
    ),
    "PleaseWaitBButtonCancel": (
        "Please wait.|... ... B Button: Cancel",
    ),
    "PleaseDecideLinkLeader": (
        "Decide between you which will be the GROUP LEADER.",
        "The rest must then choose “JOIN GROUP.”",
    ),
    "PlayerAt4PCounterUseGMode": (
        "At least one player has registered at the four-player counter.",
        "That needs four players connected by GBA Game Link cable.",
        "When the four of you are ready, select G-MODE (GLOBAL MODE) and "
        "register again.",
    ),
    "ExplainLinkContest": (
        "This is a CONTEST for two to four players, linked by a Wireless "
        "Adapter or a GBA Game Link cable.",
        "You are asked first which mode you want. There are two.",
        "E-MODE (EMERALD MODE) takes two to four players, each with a "
        "POKéMON Emerald Game Pak.",
        "G-MODE (GLOBAL MODE) takes four players only, each with a POKéMON "
        "Emerald, Ruby or Sapphire Game Pak.",
        "Agree on the mode between you and all choose it.",
        "Once every player has chosen the same CONTEST in the same mode, the "
        "registration is done.",
        "After that it runs as any other CONTEST does.",
    ),
    "ExplainEMode": (
        "E-MODE (EMERALD MODE) runs a LINK CONTEST for two to four players, "
        "each with a POKéMON Emerald Game Pak.",
        "You must be linked by Wireless Adapters or GBA Game Link cables.",
        "If there are fewer than four of you, TRAINERS from the hall will "
        "fill the remaining places.",
        "Note that E-MODE does not exist in POKéMON Ruby or Sapphire.",
    ),
    "ExplainGMode": (
        "G-MODE (GLOBAL MODE) is for four players linked by GBA Game Link "
        "cables, and for no other arrangement.",
        "Each must have a POKéMON Emerald, Ruby or Sapphire Game Pak.",
        "It starts once every player has chosen G-MODE, or has registered "
        "at the four-player counter if they are on Ruby or Sapphire.",
    ),
    "NoWirelessAdapterInGMode": (
        "I am very sorry.",
        "G-MODE does not work over a Wireless Adapter.",
        "Choose E-MODE, or try again on a GBA Game Link cable.",
    ),
    "WhichContestMode": (
        "Which CONTEST MODE would you like?",
    ),
}

# The counters that ask the same question, and the suffixes they use.
for base, text in SHARED.items():
    for suffix in ("", "1", "2", "3"):
        TARGETS.setdefault(f"{base}{suffix}", (text,))


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^[A-Za-z0-9_]*_Text_{re.escape(label)}::?\n(?P<body>.*?)"
        rf"(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def present(source: str) -> tuple[str, ...]:
    """Only the labels this file actually has -- the shared ones vary."""
    return tuple(label for label in TARGETS
                 if block_pattern(label).search(source))


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
    for label in present(source):
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask(text: str, labels: tuple[str, ...]) -> str:
    masked = text
    for label in labels:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_CONTEST_HALL_EN>"\n\n' + masked[end:]
    return masked


def validate_slots(source: str) -> None:
    composed = payloads()
    for label in present(source):
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}",
                                   block_pattern(label).search(source).group("body")))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(source: str, rendered: str) -> None:
    labels = present(source)
    if mask(source, labels) != mask(rendered, labels):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()

    def flat(label: str) -> str:
        return re.sub(r"\\[npl]", " ", "".join(composed[label]))

    # The ladder is what a player comes to this counter to find out.
    ranks = flat("ExplainContestRanks")
    for rank in RANKS:
        if rank not in ranks:
            raise ValueError(f"ExplainContestRanks: no longer names {rank}")
    if "same category" not in ranks:
        raise ValueError(
            "ExplainContestRanks: no longer says a POKéMON climbs within one "
            "category, which is the rule the ladder turns on")

    # The five categories are choices the player is offered by name.
    types = flat("ExplainContestTypes")
    for category in ("COOL", "BEAUTY", "CUTE", "SMART", "TOUGH"):
        if category not in types:
            raise ValueError(f"ExplainContestTypes: no longer names {category}")

    # Link compatibility is a hardware fact. A player told the wrong one
    # cannot connect, and no amount of good prose fixes that.
    link = " ".join(flat(label) for label in
                    ("ExplainLinkContest", "ExplainEMode", "ExplainGMode",
                     "NoWirelessAdapterInGMode"))
    for fact in ("E-MODE", "G-MODE", "Wireless Adapter", "Game Link",
                 "Emerald", "Ruby", "Sapphire"):
        if fact not in link:
            raise ValueError(f"the link modes no longer mention {fact}")
    if "does not work over a Wireless Adapter" not in flat("NoWirelessAdapterInGMode"):
        raise ValueError(
            "NoWirelessAdapterInGMode: no longer says why the link failed")

    # The counter and the MC are two people. If the MC's lines stopped being
    # marked, the hall reads as one voice again.
    for label in labels:
        if not label.startswith(("GettingStarted", "EntryX", "SeenContestants",
                                 "CongratsTrainer", "CongratsPlease",
                                 "AcceptYourPrize", "ThatsItForJudging",
                                 "WeveSeenContestants")):
            continue
        if "MC:" not in flat(label):
            raise ValueError(f"{label}: the MC stopped being named as the speaker")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the CONTEST hall counter and MC in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = HALL.read_text(encoding="utf-8")
    validate_slots(source)
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        HALL.write_text(rendered, encoding="utf-8")
    print(f"Contest hall English renderer OK: {len(present(source))} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

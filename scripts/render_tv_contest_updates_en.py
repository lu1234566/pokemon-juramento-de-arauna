#!/usr/bin/env python3
"""POKéMON CONTEST LIVE UPDATES, and POKéMON BATTLE UPDATE.

CONTEST LIVE UPDATES is an outside broadcast from a hall the audience has not
left. The presenter holds a microphone out to whoever is nearest, so most of
this is not the presenter at all -- it is spectators, still shouting, saying
the same thing in different registers. Then the presenter turns to the POKéMON
that lost and is quietly merciless about it, which is the shape of the show:
adoration at the front, a post-mortem at the back.

The ten shouted one-liners -- cool, beautiful, cute, smart, tough, and the
same five again louder -- are generated from a table rather than typed, so the
plain and emphatic forms of a category can never disagree about which category
they are.

POKéMON BATTLE UPDATE is a results service. It has no opinions and reads like
it.
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

BOX = TextBox({"{STR_VAR_1}": 14, "{STR_VAR_2}": 14, "{STR_VAR_3}": 14}, width=34)

# category -> (what the crowd shouts, what it shouts when it means it)
CATEGORIES: dict[str, tuple[str, str]] = {
    "Cool": ("You were cool!", "There is nothing cooler!"),
    "Beautiful": ("You were beautiful!", "There is nothing more beautiful!"),
    "Cute": ("You were lovely!", "There is nothing lovelier!"),
    "Smart": ("You were clever!", "There is nothing cleverer!"),
    "Tough": ("You were tough!", "There is nothing tougher!"),
}

HANDWRITTEN: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "ContestLiveUpdates_Text_Intro": (("LIVE UPDATES", "unwilling to leave"), (
        "“POKéMON CONTEST LIVE UPDATES!”",
        "MC: Thank you for joining us!",
        "We are live from the {STR_VAR_1}, which has only just finished.",
        "And the hall is still full. Nobody wants to go home.",
        "Spectator: {STR_VAR_2}!",
        "Spectator: {STR_VAR_3}!",
        "MC: As you can hear, the CONTEST went to {STR_VAR_3}'s POKéMON "
        "{STR_VAR_2}.",
        "Spectator: {STR_VAR_2}!|There is nobody like you!",
        "Spectator: {STR_VAR_3}!|Well done!",
        "MC: Let's hear what the hall has to say about it.",
    )),
    "ContestLiveUpdates_Text_WonBothRounds": (("both primary", "keep winning"), (
        "Spectator: That {STR_VAR_2} was first in both rounds of judging!",
        "That {STR_VAR_2} is going to go on winning!",
    )),
    "ContestLiveUpdates_Text_BetterRound2": (("didn't do", "comeback"), (
        "Spectator: The {STR_VAR_2} did poorly in the first round and then "
        "took the second outright!",
        "A comeback if ever I saw one. Yippee!",
    )),
    "ContestLiveUpdates_Text_EqualRounds": (("consistent", "ordinary combo"), (
        "Spectator: That {STR_VAR_2} held its level through both rounds.",
        "{STR_VAR_3} and the {STR_VAR_2} are no ordinary pair!",
    )),
    "ContestLiveUpdates_Text_BetterRound1": (("outstanding", "better appeals"), (
        "Spectator: For being {STR_VAR_1}, that {STR_VAR_2} could not be "
        "faulted.",
        "I'd like to see it appeal better next time, mind.",
    )),
    "ContestLiveUpdates_Text_GotNervous": (("nervous", "Congratulations"), (
        "Spectator: When that {STR_VAR_2} lost its nerve, I couldn't help "
        "shouting for it.",
        "And I'd like to say this to that {STR_VAR_2}: “Well done!”",
    )),
    "ContestLiveUpdates_Text_StartledFoes": (("startled even me", "awesome"), (
        "Spectator: That {STR_VAR_2}'s appeal startled even me!",
        "{STR_VAR_2}, you were extraordinary!",
    )),
    "ContestLiveUpdates_Text_UsedCombo": (("combo", "core"), (
        "Spectator: That {STR_VAR_2}'s combination appeal was something else!",
        "I have not got over it yet!",
    )),
    "ContestLiveUpdates_Text_ExcitingAppeal": (("heart pounding",), (
        "Spectator: The winning {STR_VAR_2}'s appeal had my heart going!",
    )),
    "ContestLiveUpdates_Text_VeryExcitingAppeal": (("still has",), (
        "Spectator: The winning {STR_VAR_2}'s appeal has my heart going "
        "still!",
    )),
    "ContestLiveUpdates_Text_TookBreak": (("took a break", "captivated"), (
        "Spectator: Even when that {STR_VAR_2} stopped appealing, I couldn't "
        "look anywhere else.",
        "I am quite taken with that {STR_VAR_2}.",
    )),
    "ContestLiveUpdates_Text_GotStartled": (("startled by another", "resilient"), (
        "Spectator: When that {STR_VAR_2} was startled by somebody else's "
        "appeal, I was nearly in tears.",
        "{STR_VAR_2}, you held on!|Well done!",
    )),
    "ContestLiveUpdates_Text_MoveWonderful": (("How could it be",), (
        "Spectator: Oh...|That {STR_VAR_2}'s {STR_VAR_3}!|{STR_VAR_2}'s "
        "{STR_VAR_3}!|{STR_VAR_2}'s {STR_VAR_3}!|How can a thing be that "
        "good?",
    )),
    "ContestLiveUpdates_Text_TalkAboutAnotherMon": (("full of the", "caught my eye"), (
        "MC: There you have it -- this hall belongs to the {STR_VAR_1} "
        "tonight!",
        "Though I should say another POKéMON caught my eye: {STR_VAR_2}'s "
        "{STR_VAR_3}.",
        "{STR_VAR_2}'s {STR_VAR_3}...",
    )),
    "ContestLiveUpdates_Text_FailedToAppeal": (("single appeal", "even one appeal"), (
        "It made no appeal at all in the second round. Nerves, plainly.",
        "Next time I should like to see this {STR_VAR_1} make one, at least.",
    )),
    "ContestLiveUpdates_Text_LastInBothRounds": (("dead last", "last-place"), (
        "It came last in both rounds of judging.",
        "I hope {STR_VAR_1} takes this {STR_VAR_2} back to the beginning and "
        "puts that finish behind them both.",
    )),
    "ContestLiveUpdates_Text_NotExcitingEnough": (("audience's excitement", "fever pitch"), (
        "It had a hall ready to be moved and did nothing with it.",
        "We hope {STR_VAR_1} learns to read a room and work it up next time.",
    )),
    "ContestLiveUpdates_Text_LostAfterWinningRound1": (("finishing first", "effective appeals"), (
        "It took the first round and then failed to land anything in the "
        "second.",
        "A hard way to lose a thing you were winning.",
        "I've no doubt {STR_VAR_1} is already working out why.",
    )),
    "ContestLiveUpdates_Text_NeverExciting": (("never got excited", "pitch"), (
        "The hall was never once moved by its appeals in the second round.",
        "We hope it stops watching the other POKéMON and starts playing to "
        "the people.",
    )),
    "ContestLiveUpdates_Text_LostBySmallMargin": (("small margin", "weeping"), (
        "It lost to {STR_VAR_1}'s {STR_VAR_2} by very little indeed.",
        "There is no worse way to lose than nearly winning.",
        "I should not be surprised if {STR_VAR_3} is crying about it "
        "tonight.",
    )),
    "ContestLiveUpdates_Text_RepeatedAppeals": (("repeating the same", "guilty"), (
        "It disappointed the JUDGE by making the same appeal twice.",
        "There is no CONTEST where that is forgiven, and the POKéMON paid "
        "for it.",
        "{STR_VAR_1} ought to feel responsible for that.",
    )),
    "ContestLiveUpdates_Text_ValiantEffortButLost": (("valiant effort", "good use"), (
        "{STR_VAR_1} gave it everything, and...",
        "It came to nothing. Last place.",
        "{STR_VAR_1} should take the lesson and make something of it.",
    )),
    "ContestLiveUpdates_Text_Outro": (("usual farewell", "CONTEST winner"), (
        "I'd like to close the way we always do, with the winners.",
        "Tonight, that is {STR_VAR_1} and the {STR_VAR_2}!",
        "MC: Ready, everybody?|All together!",
        "Audience: {STR_VAR_1}! {STR_VAR_2}!|Congratulations!|The CONTEST is "
        "yours!",
    )),

    # -- the results service --------------------------------------------------
    "gTVPokemonBattleUpdateText00": (("BATTLE UPDATE", "as they come in"), (
        "“POKéMON BATTLE UPDATE!”",
        "Results of POKéMON battles, as they reach us.",
    )),
    "gTVPokemonBattleUpdateText01": (("faced each other", "victory for"), (
        "The TRAINERS {STR_VAR_1} and {STR_VAR_2} met in a {STR_VAR_3} "
        "BATTLE.",
        "The match went to {STR_VAR_1}.",
    )),
    "gTVPokemonBattleUpdateText02": (("formidable force",), (
        "In it, {STR_VAR_1}'s {STR_VAR_2} was the deciding factor, with "
        "{STR_VAR_3}.",
    )),
    "gTVPokemonBattleUpdateText03": (("weak\\n", "really hurt"), (
        "{STR_VAR_1}'s {STR_VAR_2} had a poor day of it, and it cost them.",
    )),
    "gTVPokemonBattleUpdateText04": (("Congratulations on your victory", "concludes"), (
        "Our congratulations on the win, {STR_VAR_1}.",
        "And to {STR_VAR_2}, who lost: better luck next time.",
        "That concludes this edition of “POKéMON BATTLE UPDATE!”",
    )),
    "gTVPokemonBattleUpdateText05": (("teams of TRAINERS", "MULTI BATTLE"), (
        "The TRAINERS {STR_VAR_1} and {STR_VAR_2} met, in teams, in a MULTI "
        "BATTLE.",
        "The match went to {STR_VAR_1}'s side.",
    )),
    "gTVPokemonBattleUpdateText06": (("on\\n", "formidable"), (
        "In it, the {STR_VAR_2} on {STR_VAR_1}'s side was the deciding "
        "factor, with {STR_VAR_3}.",
    )),
    "gTVPokemonBattleUpdateText07": (("weak showing", "concludes"), (
        "The {STR_VAR_3} on {STR_VAR_2}'s side had a poor day of it, and it "
        "cost them.",
        "Our congratulations to {STR_VAR_1}'s side.",
        "And to {STR_VAR_2}'s, who lost: better luck next time.",
        "That concludes this edition of “POKéMON BATTLE UPDATE!”",
    )),
}


def build() -> dict[str, tuple[tuple[str, ...], tuple[str, ...]]]:
    targets = dict(HANDWRITTEN)
    for category, (plain, emphatic) in CATEGORIES.items():
        targets[f"ContestLiveUpdates_Text_Was{category}"] = (
            ("{STR_VAR_2}",), ("{STR_VAR_2}!|" + plain,))
        targets[f"ContestLiveUpdates_Text_Very{category}"] = (
            ("{STR_VAR_2}",), ("{STR_VAR_2}!|" + emphatic,))
    return targets


TARGETS = build()


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
        masked = masked[:start] + '\t.string "<ARAUNA_TV_CONTEST_UPDATES_EN>"\n\n' + masked[end:]
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

    # The emphatic shout has to be the same category as the plain one, or the
    # crowd calls a BEAUTY win cute.
    for category in CATEGORIES:
        plain = "".join(composed[f"ContestLiveUpdates_Text_Was{category}"])
        loud = "".join(composed[f"ContestLiveUpdates_Text_Very{category}"])
        if plain == loud:
            raise ValueError(f"{category}: the two shouts are identical")
        for other in CATEGORIES:
            if other == category:
                continue
            stem = CATEGORIES[other][0].split()[-1].rstrip("!")
            if stem in plain or stem in loud:
                raise ValueError(
                    f"{category}: the shout mentions {other}, which is a "
                    f"different CONTEST category")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render CONTEST LIVE UPDATES and POKéMON BATTLE UPDATE.")
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
    print(f"TV contest updates English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

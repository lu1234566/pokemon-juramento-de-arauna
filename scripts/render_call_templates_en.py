#!/usr/bin/env python3
"""The hundred and forty-one PokeNav lines that belong to nobody in particular.

Every rematch trainer in the game draws from these when the PokeNav rings:
what they say about a wild encounter, about a battle they lost, about one they
won, about wanting a rematch here or somewhere else, and about hearing that
you did something at the frontier.

They are not written one by one, because they are not written one by one in
the game either. The engine indexes them by the caller's personality, and
index 4 is the same person in all eleven families -- vanilla keeps "Hey,
{PLAYER}{KUN}. / {STR_VAR_1} here." at index 4 of every single table. So the
fifteen voices are declared once, the topics supply only the middle, and the
blocks are composed. Getting a voice wrong then gets it wrong consistently,
which is the failure a player would forgive; getting it wrong in one family
out of eleven is the one they would not.

Line breaking is computed, not typed. A slot like {STR_VAR_2} can hold
"VILA DA PASSAGEM" or "BATTLE PYRAMID", so the wrapper charges each
placeholder its worst realistic width and breaks around that.

Which slots exist is fixed by src/match_call.c and is not a choice here:
STRS_WILD_BATTLE gives a species on the caller's route, STRS_BATTLE_POSITIVE
a species in the caller's party, STRS_BATTLE_REQUEST a map name, and
STRS_FRONTIER a facility name plus a streak count. Nothing else has a second
slot at all.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALLS = ROOT / "data" / "text" / "match_call.inc"

# The widest a composed line may get once every slot is charged its worst
# realistic content. Vanilla's own widest rendered line is 208px; this is the
# character budget that keeps composed lines comfortably inside it.
WRAP = 33
SLOT = {
    "{PLAYER}": 7,       # PLAYER_NAME_LENGTH
    "{STR_VAR_1}": 10,   # a trainer name
    "{STR_VAR_2}": 16,   # a map name -- VILA DA PASSAGEM is the longest
    "{STR_VAR_3}": 3,    # a streak count
    "{KUN}": 0,          # draws nothing in English
}
BREAK = "|"  # a hard line break inside a paragraph

# Fifteen voices, in the engine's own order. Only the wild-battle table has a
# fifteenth entry; every other table stops at fourteen.
VOICES: tuple[tuple[str, str], ...] = (
    ("Hi! {PLAYER}{KUN}, hello!|This is {STR_VAR_1}.", "Well, see you again!"),
    ("Hello, {PLAYER}{KUN}.|It's {STR_VAR_1}.", "Okay, bye!"),
    ("Hey there, {PLAYER}!|It's me, {STR_VAR_1}.", "All right, see you!"),
    ("Hey, {PLAYER}{KUN}.|{STR_VAR_1} here.", "Okay, catch you later."),
    ("Hiya, {PLAYER}{KUN}!|It's {STR_VAR_1}.", "Right, take care!"),
    ("Hey, {PLAYER}{KUN}.|{STR_VAR_1} here.", "You take care."),
    ("...Uh, {PLAYER}{KUN}?|It's me, {STR_VAR_1}.", "Sorry -- got to run!"),
    ("Oh, {PLAYER}{KUN}, how do you do?|This is {STR_VAR_1} speaking.", "See you again!"),
    ("Oh, {PLAYER}{KUN}, hi there!|This is {STR_VAR_1}!", "See you!"),
    ("Oh, {PLAYER}{KUN}, hello...|This is {STR_VAR_1}.", "See you around."),
    ("Ah, {PLAYER}{KUN}.|This is {STR_VAR_1}.", "Until the next time."),
    ("Hello, {PLAYER}{KUN}.|It's me, {STR_VAR_1}.", "See you!"),
    ("Ah, hello, {PLAYER}{KUN}!|This is {STR_VAR_1}!", "Bye now."),
    ("Oh, hi, {PLAYER}{KUN}.|This is {STR_VAR_1}.", "Bye-bye!"),
    ("Hey, {PLAYER}!|This is {STR_VAR_1}!", "See you around!"),
)

# {STR_VAR_2} here is a species standing on the caller's route.
WILD = (
    ("I had a {STR_VAR_2} in front of me a while back and couldn't close it.",
     "So near, too!"),
    ("I went after a good {STR_VAR_2} a little while ago.",
     "It got out. I was sick about it."),
    ("I took a shot at a {STR_VAR_2} just now and it went straight past me.",
     "Spoiled the whole day, that."),
    ("You know the {STR_VAR_2}?|I came near to having one.",
     "I thought it was mine, and then it wasn't.",
     "If it shows itself again I'll have it."),
    ("Catching much lately?",
     "I came close to one a while back and it slipped the ball."),
    ("Caught anything lately?",
     "I nearly had one the other day. It got around me somehow."),
    ("Wait! Wait!|I can get this {STR_VAR_2}...",
     "Aaargh! It's loose!|That wasn't close. That was had."),
    ("Have you been having any luck catching lately?",
     "I came very near a while ago, but the one I wanted got free.",
     "I must do better!"),
    ("Well? Are you getting a team together?",
     "I'm having a rotten run of it. They all get away from me!"),
    ("Listen, I came within a whisker of a {STR_VAR_2}...",
     "And then it gave me the slip...",
     "I need to try harder."),
    ("How are things with you?",
     "I went after a wild {STR_VAR_2} earlier and it got away from me.",
     "I feel beaten..."),
    ("Are you still catching?",
     "I've been trying myself, and it isn't as simple as it looks.",
     "There is more to it than people say."),
    ("Have you been catching?",
     "I keep trying and I keep coming up empty!",
     "There is more to it than people say."),
    ("Just now I went after a {STR_VAR_2}.",
     "It got away!|Oh, you can imagine how I felt!"),
    ("I've been meaning to catch a few of my own.",
     "But I can't seem to find any at all. It's a puzzle to me!",
     "I'm at my wits' end!"),
)

# No second slot: a lost battle is just a lost battle.
NEGATIVE = (
    ("I took on another TRAINER and I lost.", "Very disappointing, that."),
    ("I challenged someone after we battled.",
     "I came close, but I lost it. Oh, well!"),
    ("I just got taken apart in a battle.",
     "I need to bring my team on some more!"),
    ("I lost one earlier.", "Nothing much to say about it. I'll do better."),
    ("Battled someone this morning and lost!", "Ah, well, that's how it goes!"),
    ("I went down in a battle the other day.", "It happens. I'll get there."),
    ("I lost. I lost badly.|Don't ask me about it...",),
    ("I met another TRAINER earlier, and I am afraid I came off worse.",
     "I shall have to work at it."),
    ("I lost a battle just now!", "But I'm not down about it! The next one's mine!"),
    ("I lost again...", "I'm starting to wonder if I'm any good at this..."),
    ("I battled and lost earlier.",
     "There is something I am missing. I mean to find it."),
    ("I lost a battle this week.",
     "It taught me more than the wins did, I think."),
    ("I had a battle and I did not win it!", "Still, it was a fine match!"),
    ("I lost my battle earlier.", "I nearly cried, if you want the truth!"),
)

# {STR_VAR_2} here is a species in the caller's own party.
POSITIVE = (
    ("I battled another TRAINER earlier.|I won! I won!",
     "My {STR_VAR_2} did all the work. Isn't that something!"),
    ("I had a battle yesterday and I won it! Fantastic!",),
    ("How's your battling?",
     "I had one the other day, and my {STR_VAR_2} was enormous.",
     "Next time we meet, {PLAYER}, it won't be me losing."),
    ("I won one earlier.", "My {STR_VAR_2} did it. Good team, that."),
    ("I won a battle this morning!", "My {STR_VAR_2} was flying! What a day!"),
    ("Won one the other day.", "The {STR_VAR_2} carried it. Can't complain."),
    ("I won! Me! I actually won!",
     "My {STR_VAR_2} did something I have never seen it do!"),
    ("I am pleased to say I won a battle earlier.",
     "My {STR_VAR_2} performed beautifully."),
    ("Guess what! I won a battle!", "My {STR_VAR_2} was brilliant! I'm so pleased!"),
    ("I won one, for once...",
     "My {STR_VAR_2} held on when I was sure it wouldn't..."),
    ("I won a battle earlier.",
     "My {STR_VAR_2} has come a long way since we met."),
    ("I won a battle this week.",
     "My {STR_VAR_2} deserves the credit for it, not me."),
    ("I won my battle! I was so glad!", "My {STR_VAR_2} would not give an inch!"),
    ("I won a battle just now!", "My sweet {STR_VAR_2} was wonderful!"),
)

# {STR_VAR_2} here is the map the player is standing on.
SAME_ROUTE = (
    ("Wait -- you're near {STR_VAR_2}?",
     "Then we have to battle!|I'll be waiting! See you!"),
    ("Oh? You're around {STR_VAR_2} just now?",
     "Would you like a battle? I'll wait for you."),
    ("Hey, are you near {STR_VAR_2} right now?",
     "How about a battle, then?",
     "I'm not losing this time!|I'll be waiting!"),
    ("You're over by {STR_VAR_2}, aren't you.", "Come and battle me, then."),
    ("Are you near {STR_VAR_2}? You are!", "Perfect! Come and battle me!"),
    ("You're around {STR_VAR_2}, I hear.", "Come by. I'll be here."),
    ("Wait -- {STR_VAR_2}? You're there now?",
     "Come and battle me before I lose my nerve!"),
    ("Am I right in thinking you are near {STR_VAR_2}?",
     "Then perhaps you would give me a battle. I shall wait."),
    ("You're by {STR_VAR_2} right now?", "Oh, come and battle me! Please!"),
    ("You're near {STR_VAR_2}, aren't you...",
     "Come and battle me. I could use the practice..."),
    ("You are near {STR_VAR_2}, I believe.", "Come to me and we will battle."),
    ("You happen to be near {STR_VAR_2}?",
     "Come and battle me, then. I would be glad of it."),
    ("Are you near {STR_VAR_2} just now?", "Do come and battle me! I'd like that!"),
    ("Oh! You're near {STR_VAR_2}!", "Come and battle me! I'll be waiting!"),
)

# {STR_VAR_2} here is where the caller is, which is somewhere else.
DIFF_ROUTE = (
    ("Want a battle with me?", "I'll be waiting for you around {STR_VAR_2}!"),
    ("Would you like another battle with me?",
     "You'll find me around {STR_VAR_2}. I'll be waiting!"),
    ("My team has come on a lot since we met.",
     "I want to see where they stand against yours, {PLAYER}.",
     "So let's battle!",
     "I'll be waiting around {STR_VAR_2}."),
    ("Battle me again sometime.", "I'm around {STR_VAR_2}."),
    ("Fancy another battle?", "I'm out by {STR_VAR_2}! Come and find me!"),
    ("Come and battle me again.", "I'll be around {STR_VAR_2}."),
    ("Battle me! Before I talk myself out of it!",
     "I'm near {STR_VAR_2}. Hurry!"),
    ("Would you consider giving me another battle?",
     "I shall be near {STR_VAR_2} for some time yet."),
    ("Let's battle again! Say yes!", "I'm around {STR_VAR_2}, waiting!"),
    ("Would you battle me again...?",
     "I'm near {STR_VAR_2}. I'll be here a while..."),
    ("I would like another battle with you.",
     "I am near {STR_VAR_2}. Come when you can."),
    ("I'd be glad of another battle with you.",
     "You'll find me near {STR_VAR_2}."),
    ("Do give me another battle!", "I shall be near {STR_VAR_2}!"),
    ("Battle me again, would you?", "I'm around {STR_VAR_2}! Bye-bye!"),
)

# The frontier families differ only in the feat. What the caller thinks of it
# is the same fourteen reactions in all five.
FRONTIER_REACTION = (
    ("I heard the news!", "That's tremendous! I have to do better!"),
    ("I heard about you!", "That's really something! I ought to try harder!"),
    ("Word got round to me.", "Make it one more next time!"),
    ("There's a rumour going about you.", "I'd better step it up, too."),
    ("I heard! Everyone heard!",
     "Isn't that something! I need to work on my team!"),
    ("Heard about you.", "That's worth doing. I might have a go myself."),
    ("Someone told me -- is it true?",
     "Oh! Something rare just went past!"),
    ("I have heard about your run.",
     "Most impressive. I hope you keep it up."),
    ("I heard! I heard!", "That is so good! I'd better try harder too!"),
    ("Word reached me...",
     "That's quite a thing to have done. I need to work harder."),
    ("I hear you're the terror of the place.",
     "You're good, you.|I wonder how far I would get?"),
    ("Someone passed word about you along.", "That's quite a tale. Well done."),
    ("They say you have been doing wonders!", "I admire your energy!"),
    ("I heard about you!", "You're an inspiration!"),
)

FRONTIER_FEAT = {
    "MatchCall_BattleFrontierStreakText":
        "They say you took {STR_VAR_3} battles in a row at the {STR_VAR_2}.",
    "MatchCall_BattleFrontierRecordStreakText":
        "They say your best run at the {STR_VAR_2} stands at {STR_VAR_3} battles.",
    "MatchCall_BattleDomeText":
        "They say you took the title at the {STR_VAR_2} {STR_VAR_3} times.",
    "MatchCall_BattlePikeText":
        "They say you came through {STR_VAR_3} rooms at the {STR_VAR_2}.",
    "MatchCall_BattlePyramidText":
        "They say you climbed {STR_VAR_3} floors inside the {STR_VAR_2}.",
}

# Every block in a family must still contain these, or the file is not the one
# this renderer was written against.
FAMILIES: dict[str, tuple[int, tuple[str, ...]]] = {
    "MatchCall_WildBattleText": (15, ("{STR_VAR_1}",)),
    "MatchCall_NegativeBattleText": (14, ("{STR_VAR_1}",)),
    "MatchCall_PositiveBattleText": (14, ("{STR_VAR_1}",)),
    "MatchCall_SameRouteBattleRequestText": (14, ("{STR_VAR_1}", "{STR_VAR_2}")),
    "MatchCall_DifferentRouteBattleRequestText": (14, ("{STR_VAR_1}", "{STR_VAR_2}")),
    "MatchCall_BattleFrontierStreakText": (14, ("{STR_VAR_1}", "{STR_VAR_2}", "{STR_VAR_3}")),
    "MatchCall_BattleFrontierRecordStreakText": (14, ("{STR_VAR_1}", "{STR_VAR_2}", "{STR_VAR_3}")),
    "MatchCall_BattleDomeText": (14, ("{STR_VAR_1}", "{STR_VAR_2}", "{STR_VAR_3}")),
    "MatchCall_BattlePikeText": (14, ("{STR_VAR_1}", "{STR_VAR_2}", "{STR_VAR_3}", "rooms")),
    "MatchCall_BattlePyramidText": (14, ("{STR_VAR_1}", "{STR_VAR_2}", "{STR_VAR_3}", "floors")),
}

MIDDLES = {
    "MatchCall_WildBattleText": WILD,
    "MatchCall_NegativeBattleText": NEGATIVE,
    "MatchCall_PositiveBattleText": POSITIVE,
    "MatchCall_SameRouteBattleRequestText": SAME_ROUTE,
    "MatchCall_DifferentRouteBattleRequestText": DIFF_ROUTE,
}

# Which families the engine hands a second and third string to.
SECOND_SLOT = frozenset(
    ["MatchCall_WildBattleText", "MatchCall_PositiveBattleText",
     "MatchCall_SameRouteBattleRequestText",
     "MatchCall_DifferentRouteBattleRequestText"] + list(FRONTIER_FEAT))
THIRD_SLOT = frozenset(FRONTIER_FEAT)


def measured(text: str) -> int:
    """How wide the text gets once every slot holds its worst realistic value."""
    for slot, width in SLOT.items():
        text = text.replace(slot, "x" * width)
    if "{" in text:
        raise ValueError(f"unpriced placeholder: {text!r}")
    return len(text)


def greedy(words: list[str], width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and measured(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def wrap(paragraph: str) -> list[str]:
    """Break a paragraph, then even the lines out.

    Greedy wrapping alone leaves stragglers -- a full line and then a line
    holding "have it." -- which looks like a mistake on a two-line message
    box. Narrowing the budget until the line count would change gives the
    same break points a person would pick.
    """
    lines: list[str] = []
    for chunk in paragraph.split(BREAK):
        words = chunk.split()
        best = greedy(words, WRAP)
        for width in range(WRAP - 1, WRAP * 2 // 3, -1):
            candidate = greedy(words, width)
            if len(candidate) != len(best):
                break
            if min(map(measured, candidate)) > min(map(measured, best)):
                best = candidate
        lines.extend(best)
    return lines


def compose(paragraphs: tuple[str, ...]) -> tuple[str, ...]:
    """Paragraphs into .string payloads, with the page and scroll codes."""
    payloads: list[str] = []
    pages = [wrap(paragraph) for paragraph in paragraphs]
    for index, lines in enumerate(pages):
        last_page = index == len(pages) - 1
        for position, line in enumerate(lines):
            if position == len(lines) - 1:
                code = "$" if last_page else "\\p"
            elif position == 0:
                code = "\\n"
            else:
                code = "\\l"
            payloads.append(line + code)
    return tuple(payloads)


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = {}
    for family, (count, _) in FAMILIES.items():
        for index in range(count):
            opening, closing = VOICES[index]
            if family in FRONTIER_FEAT:
                intro, reaction = FRONTIER_REACTION[index]
                middle: tuple[str, ...] = (intro, FRONTIER_FEAT[family], reaction)
            else:
                middle = MIDDLES[family][index]
            paragraphs = (opening,) + middle + (closing,)
            blocks[f"{family}{index + 1}"] = compose(paragraphs)
    return blocks


TARGETS = build()


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}::?\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def validate_slots() -> None:
    """A slot the engine never fills prints whatever was left in the buffer."""
    for family, (count, _) in FAMILIES.items():
        for index in range(count):
            payload = "".join(TARGETS[f"{family}{index + 1}"])
            for slot, allowed in (("{STR_VAR_2}", family in SECOND_SLOT),
                                  ("{STR_VAR_3}", family in THIRD_SLOT)):
                if slot in payload and not allowed:
                    raise ValueError(
                        f"{family}{index + 1}: uses {slot}, which match_call.c "
                        f"never fills for this family")


def validate_widths() -> None:
    for label, payloads in TARGETS.items():
        for payload in payloads:
            line = payload.rstrip("$")
            line = re.sub(r"\\[npl]$", "", line)
            if measured(line) > WRAP:
                raise ValueError(
                    f"{label}: composed line is {measured(line)} wide, max {WRAP}: {line!r}")


def render(source: str) -> str:
    validate_slots()
    validate_widths()
    rendered = source
    for family, (count, markers) in FAMILIES.items():
        for index in range(count):
            label = f"{family}{index + 1}"
            matches = list(block_pattern(label).finditer(rendered))
            if len(matches) != 1:
                raise ValueError(f"{label}: expected one text block, found {len(matches)}")
            body = matches[0].group("body")
            if ".string" not in body:
                raise ValueError(f"{label}: target contains no .string payload")
            for marker in markers:
                if marker not in body:
                    raise ValueError(f"{label}: source marker missing: {marker!r}")
            new_body = "".join(f'\t.string "{payload}"\n' for payload in TARGETS[label]) + "\n"
            start, end = matches[0].span("body")
            rendered = rendered[:start] + new_body + rendered[end:]
        # The family must end where this renderer thinks it ends.
        if block_pattern(f"{family}{count + 1}").search(rendered):
            raise ValueError(f"{family}: the file has more than {count} entries")
    return rendered


def mask(text: str) -> str:
    masked = text
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_CALL_TEMPLATES_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    # These lines belong to whoever the engine hands them to, so they must not
    # name a place, a person or a creature of their own.
    forbidden = ("HOENN", "POKéMON LEAGUE", "Sucuria", "ARAUNA", "JURAMENTO",
                 "HORIZONTE", "M'BOI")
    for label, payloads in TARGETS.items():
        joined = "".join(payloads)
        for token in forbidden:
            if token in joined:
                raise ValueError(f"{label}: names something it cannot know: {token}")

    # Index N is the same person in all eleven families. If a voice drifted,
    # the greeting would stop matching across tables.
    for index in range(14):
        greetings = {
            TARGETS[f"{family}{index + 1}"][0]
            for family in FAMILIES
        }
        if len(greetings) != 1:
            raise ValueError(f"voice {index + 1} greets differently across families")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the per-personality Match Call templates in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = CALLS.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.in_place:
        CALLS.write_text(rendered, encoding="utf-8")
    print(f"Match Call template English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

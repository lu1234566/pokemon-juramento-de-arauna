#!/usr/bin/env python3
"""The eight rooms of the CASA DOS TRUQUES, and the doors between them.

Every room ends the same way: the player writes a secret code on the locked
door, the code turns out to be a compliment to the TRICK MASTER, and the lock
opens. Eight rooms, eight compliments, and they escalate -- he starts at
"fabulous" and finishes somewhere well past dignity.

That escalation is the joke, and it only works if the eight are read in
order and each is warmer than the last. Written out eight times in eight
files it is exactly the sort of thing that loses a rung, so the compliments
are declared here in one ordered table and the surrounding sentence is
generated. The renderer checks all eight are different and that each door
still says the lock opened, since that is the only confirmation a player
gets that the room is solved.

Around the doors are the people who wandered in. They are lost, dizzy,
cheating, or convinced they are about to win, and none of them is anywhere
else in the game.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

ROOMS = {n: ROOT / "data" / "maps" / f"Route110_TrickHousePuzzle{n}" / "scripts.inc"
         for n in range(1, 9)}

BOX = TextBox({"{PLAYER}": 7}, width=34)

WHOLE = ("TRICK MASTER", "CASA DOS TRUQUES", "GYM LEADER",
         "POKéMON LEAGUE", "BIRD POKéMON")

# What the code says, room by room. He gets less restrained as you get
# further in, and that progression is the whole joke.
COMPLIMENTS: tuple[str, ...] = (
    "TRICK MASTER is fabulous.",
    "TRICK MASTER is clever.",
    "TRICK MASTER is much envied.",
    "TRICK MASTER is cool.",
    "TRICK MASTER is a genius.",
    "TRICK MASTER is my whole life.",
    "TRICK MASTER is thoroughly huggable.",
    "TRICK MASTER, I love you.",
)

# room -> {trainer -> (intro, defeat, post)}
ROOM_TRAINERS: dict[int, dict[str, tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]]] = {
    1: {
        "Sally": (
            ("I shall hack and slash my way through with the CUT we have "
             "just learned.",),
            ("Why are you so serious about it?",),
            ("I never tire of hacking and slashing.",),
        ),
        "Eddie": (
            ("I wandered into this peculiar house by accident...",),
            ("And now I have lost as well...",),
            ("Lost my way, lost a battle, and I am more lost than "
             "ever...|I cannot get out...",),
        ),
        "Robin": (
            ("Who exactly is the TRICK MASTER?",),
            ("I lost while I was lost in thought.",),
            ("You are strong.|Who exactly are you?",),
        ),
    },
    2: {
        "Ted": (
            ("Which switch closes which hole?",),
            ("After that battle I am more confused than I was.",),
            ("Could I get you to press all the buttons for me?",),
        ),
        "Paul": (
            ("Oh! This is your second time through the CASA DOS TRUQUES.",),
            ("You are good at battling too?",),
            ("The TRICK MASTER rigged every trick in this house himself.",),
        ),
        "Georgia": (
            ("I want a GYM of my own one day.|So I am studying how traps are "
             "set.",),
            ("I did not study the battling half enough.",),
            ("You are strong, aren't you?|Strong enough for a GYM LEADER, "
             "perhaps.",),
        ),
    },
    3: {
        "Justin": (
            ("I keep arriving back at the same place.",),
            ("I was having trouble enough, and then you beat me. It is not "
             "fair.",),
            ("It is all doors in here!|Too small and too dark! Help!",),
        ),
        "Martha": (
            ("I do not know what is going on here.|I am starting to feel "
             "rather sad...",),
            ("You... you are awful.",),
            ("I know I am weak!|And I have no sense of direction!",),
        ),
        "Alan": (
            ("I do not understand it. What would anyone want with a house "
             "this bizarre?",),
            ("I do not understand it.|How did I lose?",),
            ("I do not understand it.|How many traps are there in this "
             "house?",
             "You may be the one to find out."),
        ),
    },
    4: {
        "Cora": (
            ("Thinking this out is far too much bother.|I only wanted to "
             "battle.",),
            ("Beaten, and I still like battling best.",),
            ("You would agree, would you not? You would go anywhere at all "
             "if TRAINERS were there.",),
        ),
        "Yuji": (
            ("Heh. Boulders like this I brush aside with one finger.",),
            ("I can push a boulder. I cannot solve the puzzle...",),
            ("Brawn is not enough in here.|You have to use your head.",),
        ),
        "Paula": (
            ("The CASA DOS TRUQUES is getting trickier, is it not?",),
            ("Aaak!",),
            ("Has anybody actually reached the end?",),
        ),
    },
    6: {
        "Sophia": (
            ("The moment I heard there was a strange house I had to come and "
             "look.",),
            ("I have discovered a tough TRAINER.",),
            ("I am having a thoroughly good time going through this place.",
             "A challenge worth doing twice."),
        ),
        "Benny": (
            ("Perhaps I could get my BIRD POKéMON to fly me over the wall...",),
            ("Gwaaah! I blew it!",),
            ("Ehehehe... I suppose I lost because I was trying to cheat.",),
        ),
        "Sebastian": (
            ("These turning doors are making me dizzy...",),
            ("Everything is spinning round and round. I cannot take any "
             "more...",),
            ("You do not seem affected in the slightest.|Or is that a poker "
             "face?",),
        ),
    },
    7: {
        "Joshua": (
            ("The TRICK MASTER always vanishes like smoke.|How does he "
             "manage it?",),
            ("Aiyeeeh! You are far too strong!|How do you manage it?",),
            ("I do wish I could appear and disappear like smoke too.",),
        ),
        "Patricia": (
            ("Going round and round the same spot...|It brings ill "
             "fortune...",),
            ("Defeated.|A bad sign...",),
            ("I have circled this same spot more than ten times now...|Ill "
             "fortune...",),
        ),
        "Alexis": (
            ("Whoever wins gets through here first. That is the feeling I "
             "have.",),
            ("Oh.|Go on ahead, then.",),
            ("You are going to solve every puzzle in the CASA DOS TRUQUES. "
             "That is the feeling I have.",),
        ),
        "Mariela": (
            ("Nufufufu. Here at last.|Let us get straight to it.",),
            ("You are terribly casual about winning.",),
            ("Humph. I am not upset.|Not in the least.",),
        ),
        "Alvaro": (
            ("I watched you coming. Ever so closely.",),
            ("This outcome I did not see coming...",),
            ("Well. We have both picked a strange place to get acquainted "
             "in.",
             "One oddity to another -- let us both do our best."),
        ),
        "Everett": (
            ("It is dreadfully cramped in here...",),
            ("Oh, yes. Strong you are.",),
            ("I was rather hoping to swap places with you when I beat "
             "you, but...",),
        ),
    },
    8: {
        "Vincent": (
            ("Not many TRAINERS have got this far.",),
            ("Which must mean you are tough as well...",),
            ("You have beaten the POKéMON LEAGUE CHAMPION?|That is too "
             "much.",),
        ),
        "Keira": (
            ("Count yourself lucky to be battling me.",),
            ("This is not right!|I cannot lose!",),
            ("It is a miracle you beat me.|You may brag about it.",),
        ),
        "Leroy": (
            ("So you have been slogging through the CASA DOS TRUQUES too.",),
            ("I see...|There is something extraordinary about your style.",),
            ("Somebody like you ought to please the TRICK MASTER.",),
        ),
    },
}


def build() -> dict[int, dict[str, tuple[str, ...]]]:
    groups: dict[int, dict[str, tuple[str, ...]]] = {n: {} for n in ROOMS}
    for index, compliment in enumerate(COMPLIMENTS, start=1):
        groups[index][
            f"Route110_TrickHousePuzzle{index}_Text_WroteSecretCodeLockOpened"] = (
            "{PLAYER} wrote the secret code on the door.",
            f"“{compliment}”|... ... ... ... ... ... ... ...",
            "The lock clicked open.",
        )
    for room, trainers in ROOM_TRAINERS.items():
        for name, (intro, defeat, after) in trainers.items():
            prefix = f"Route110_TrickHousePuzzle{room}_Text_{name}"
            groups[room][f"{prefix}Intro"] = intro
            groups[room][f"{prefix}Defeat"] = defeat
            groups[room][f"{prefix}PostBattle"] = after
    return groups


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = ROOMS


def which(label: str) -> int:
    for room, group in GROUPS.items():
        if label in group:
            return room
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


def render(sources: dict[int, str]) -> dict[int, str]:
    composed = payloads()
    rendered = dict(sources)
    for label in TARGETS:
        room = which(label)
        matches = list(block_pattern(label).finditer(rendered[room]))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered[room] = rendered[room][:start] + new_body + rendered[room][end:]
    return rendered


def mask(texts: dict[int, str]) -> dict[int, str]:
    masked = dict(texts)
    for label in TARGETS:
        room = which(label)
        match = block_pattern(label).search(masked[room])
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked[room] = (masked[room][:start]
                        + '\t.string "<ARAUNA_TRICK_ROOMS_EN>"\n\n'
                        + masked[room][end:])
    return masked


def validate_slots(sources: dict[int, str]) -> None:
    composed = payloads()
    for label in TARGETS:
        body = block_pattern(label).search(sources[which(label)]).group("body")
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}", body))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(sources: dict[int, str], rendered: dict[int, str]) -> None:
    if mask(sources) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # Eight doors, eight compliments, each one warmer than the last. Two the
    # same and the joke stops working.
    doors = []
    for index, compliment in enumerate(COMPLIMENTS, start=1):
        label = f"Route110_TrickHousePuzzle{index}_Text_WroteSecretCodeLockOpened"
        text = flat(label)
        if compliment not in text:
            raise ValueError(f"{label}: no longer carries its own compliment")
        if "TRICK MASTER" not in text:
            raise ValueError(
                f"{label}: the code no longer flatters the TRICK MASTER, "
                f"which is the whole point of it being the code")
        if "lock" not in text.lower():
            raise ValueError(
                f"{label}: no longer says the lock opened, which is the only "
                f"confirmation the player gets that the room is solved")
        doors.append(compliment)
    if len(set(doors)) != len(doors):
        raise ValueError("two rooms use the same compliment for their code")

    # The people in the rooms are told apart by nothing but what they say.
    for room, trainers in ROOM_TRAINERS.items():
        for shape in ("Intro", "Defeat", "PostBattle"):
            said = [flat(f"Route110_TrickHousePuzzle{room}_Text_{name}{shape}")
                    for name in trainers]
            if len(set(said)) != len(said):
                raise ValueError(
                    f"room {room}: two TRAINERS give an identical {shape}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the eight CASA DOS TRUQUES rooms in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    sources = {room: path.read_text(encoding="utf-8")
               for room, path in FILES.items()}
    validate_slots(sources)
    rendered = render(sources)
    validate_rendered(sources, rendered)

    if args.in_place:
        for room, path in FILES.items():
            path.write_text(rendered[room], encoding="utf-8")
    print(f"Trick house rooms English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

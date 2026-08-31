#!/usr/bin/env python3
"""The ten people the engine can put inside somebody else's SECRET BASE.

A registered base is furnished and inhabited by a stranger, and the engine
picks which of ten personalities that stranger has. Each of the ten gets six
texts: what they say when you walk in, what they say when you accept, what
they say when you decline, what they say beaten, what they say afterwards,
and what they say instead of all that once you are CHAMPION and they have
stopped offering battles.

The last of those six is the structural fact worth building on. Emerald
writes PreChampion by copying the Intro and cutting the invitation off the
end, so the two texts agree by construction. Written by hand ten times over,
they would drift, and a player who visits the same base before and after the
LEAGUE would find the same person telling a different story about why they
live there. So a stance is written once here and both texts are composed
from it; the renderer then checks the agreement it just built.

What survives from Emerald is the ten stances themselves -- the collector,
the researcher, the host, the one who waited years for a popular spot. They
are the only thing separating ten otherwise identical strangers, so they are
kept and rewritten rather than replaced.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SOURCE = ROOT / "data" / "text" / "secret_base_trainers.inc"
PREFIX = "SecretBase_Text_Trainer"

BOX = TextBox({}, width=34)

# Names printed elsewhere in the game that must not be broken across lines.
WHOLE = ("SECRET BASE", "SECRET BASES", "ARAUNA")

SHAPES = ("Intro", "AcceptBattle", "DeclineBattle",
          "Defeated", "PostBattle", "PreChampion")

# stance      -- why this person lives here. Said before and after the LEAGUE.
# offer       -- the invitation. Only the pre-LEAGUE visit carries it.
# coda        -- what they say instead of the invitation, once it is gone.
# accept/decline/defeated/after -- the four short replies.
PEOPLE: dict[int, dict[str, tuple[str, ...] | str]] = {
    0: {
        "stance": (
            "Have you dug a SECRET BASE of your own yet?",
            "I walked half of ARAUNA before I settled on this one. Up, down, "
            "in and out of every hollow I could find.",
        ),
        "offer": "Well, you have come all this way. Shall we battle?",
        "coda": ("Make yourself at home while you are here.",),
        "accept": ("Right then!|Here we come!",),
        "decline": ("Oh?|Not the moment for it, then...",),
        "defeated": ("Aaah! You are far too strong!",
                     "About this -- do keep it to yourself, would you?"),
        "after": ("So what do you make of my SECRET BASE?",
                  "Come and see me again tomorrow."),
    },
    5: {
        "stance": (
            "There is no shortage of places to put a SECRET BASE.",
            "But this is the one I like. Look at it properly and you will "
            "see why.",
        ),
        "offer": "Now -- fancy a battle?",
        "coda": (),
        "accept": ("All right, here goes!",),
        "decline": ("Ah...|Another time, then.",),
        "defeated": ("Hmmm... that is ours lost.",
                     "But you will not go telling people!|That is confidential, that is."),
        "after": ("If you are ever back this way, I hope you will look in.",),
    },
    1: {
        "stance": (
            "This is a sought-after spot. There is always somebody in it.",
            "Were you thinking of taking it off me?",
        ),
        "offer": "Tell you what. Beat me and the spot is yours.",
        "coda": ("I waited years for it to come free.|And here I am at last.",),
        "accept": ("Right!|I am defending my SECRET BASE!",),
        "decline": ("Eh? Is that so?|The spot does not tempt you at all?",),
        "defeated": ("I cannot keep this up!|I give in!",),
        "after": ("Fair is fair. The day I move on, this place is yours.",),
    },
    6: {
        "stance": (
            "Welcome to my laboratory.",
            "I study battling. Quietly, and where nobody is watching.",
        ),
        "offer": "Would you care to see how far the study has got?",
        "coda": (),
        "accept": ("I shall hold nothing back!",),
        "decline": ("Ah.|Some other day, then.",),
        "defeated": ("Hmm... there is a great deal I have not learned.",
                     "Back to the work."),
        "after": ("Thank you for the battle.",
                  "Do come back tomorrow."),
    },
    2: {
        "stance": (
            "A great house is all very well, but I would rather have this.",
            "All sorts of people come through here. That is the whole point "
            "of it.",
        ),
        "offer": "So then -- how about a battle?",
        "coda": (),
        "accept": ("That is the spirit!",),
        "decline": ("Give me a shout when you are ready!",),
        "defeated": ("Aww! Finished off!",
                     "Still good fun, mind!"),
        "after": ("Anyway. I should go and buy some more furniture.",
                  "I want this to be a place people are glad they came to."),
    },
    7: {
        "stance": (
            "I do adore shopping for decorations and furniture.",
            "And I love raising POKéMON every bit as much.",
        ),
        "offer": "If you would be so kind -- will you battle my POKéMON?",
        "coda": (),
        "accept": ("Thank you.|Shall we begin?",),
        "decline": ("Oh.|How disappointing...",),
        "defeated": ("I concede...",),
        "after": ("That was all in good fun.",
                  "Now I am off to enjoy some shopping."),
    },
    3: {
        "stance": (
            "Some people put their SECRET BASES where nobody will ever find "
            "them.",
            "What is it they are hiding from, do you suppose?",
        ),
        "offer": "You found me, though. So how about a battle?",
        "coda": (),
        "accept": ("I am not going down easily!",),
        "decline": ("Oh...|Worn out from the hunting, are you?",),
        "defeated": ("Down I go...",),
        "after": ("Where is your SECRET BASE?",
                  "I should come and see it."),
    },
    8: {
        "stance": (
            "People tell me there are all sorts of ways to come by "
            "decorations.",
            "So here is my idea. A race, you and me, for the finer "
            "furniture.",
        ),
        "offer": "In the meantime -- battle?",
        "coda": (),
        "accept": ("This is my SECRET BASE.|I cannot lose here!",),
        "decline": ("I will battle you whenever you like.",),
        "defeated": ("Eh?|Did I just lose?",),
        "after": ("You will not beat me at collecting, though.",
                  "Come again!"),
    },
    4: {
        "stance": (
            "I found a spot I liked and I did it up the way I wanted it.",
            "I raise the POKéMON I am fond of, and the two of us get "
            "stronger together.",
        ),
        "offer": "That is what I do. Care to battle?",
        "coda": ("Every day of it is a good day.",),
        "accept": ("Show me what you are made of!",),
        "decline": ("There are days when you are not in the mood. I know it.",),
        "defeated": ("Now I know exactly what you are made of.",),
        "after": ("We can both come out of that stronger.",
                  "Keep at it!"),
    },
    9: {
        "stance": (
            "You can tell a great deal about a person from what they choose "
            "to put on their walls, and from where they choose to put it.",
            "So. What do you make of my taste?|Lost for words?",
        ),
        "offer": "Would you like to see my taste in battling as well?",
        "coda": (),
        "accept": ("Nothing held back!",),
        "decline": ("I shall be glad to demonstrate my style another time.",),
        "defeated": ("You are extraordinarily gifted!",
                     "Is there any end to what you can do...?"),
        "after": ("What did you make of the style?",
                  "I shall keep polishing it!"),
    },
}


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = {}
    for index, person in PEOPLE.items():
        # A bare string here would be iterated one character at a time and
        # come out as a wall of one-letter paragraphs, so refuse it outright.
        for field in ("stance", "coda", "accept", "decline", "defeated", "after"):
            if isinstance(person[field], str):
                raise ValueError(
                    f"{index}.{field} is a bare string; it must be a tuple of "
                    f"paragraphs (a trailing comma is probably missing)")
        stance = tuple(person["stance"])
        blocks[f"{index}Intro"] = stance + (person["offer"],)
        blocks[f"{index}PreChampion"] = stance + tuple(person["coda"])
        blocks[f"{index}AcceptBattle"] = tuple(person["accept"])
        blocks[f"{index}DeclineBattle"] = tuple(person["decline"])
        blocks[f"{index}Defeated"] = tuple(person["defeated"])
        blocks[f"{index}PostBattle"] = tuple(person["after"])
    return blocks


TARGETS: dict[str, tuple[str, ...]] = build()


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
        masked = masked[:start] + '\t.string "<ARAUNA_SECRET_BASE_TRAINERS_EN>"\n\n' + masked[end:]
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
                      re.sub(r"\\[npl]", " ", "".join(composed[label]))).strip()

    for index, person in PEOPLE.items():
        stance = flat_paragraphs(person["stance"])
        # Both visits have to open on the same account of the place. If they
        # ever stop agreeing, the same neighbour tells two stories about why
        # they live where they live.
        for shape in ("Intro", "PreChampion"):
            if not flat(f"{index}{shape}").startswith(stance):
                raise ValueError(
                    f"{index}{shape}: no longer opens on this person's stance, "
                    f"so the visit before the LEAGUE and the visit after it "
                    f"disagree")
        # The invitation belongs to the pre-LEAGUE visit and only to it.
        offer = flat_paragraphs((person["offer"],))
        if offer not in flat(f"{index}Intro"):
            raise ValueError(f"{index}Intro: no longer offers a battle")
        if offer in flat(f"{index}PreChampion"):
            raise ValueError(
                f"{index}PreChampion: still offers a battle the engine will "
                f"not run once the player is CHAMPION")

    # Ten strangers with the same six lines are told apart by nothing but
    # what they say, so no two of them may say the same thing.
    for shape in SHAPES:
        said = [flat(f"{index}{shape}") for index in PEOPLE]
        if len(set(said)) != len(said):
            raise ValueError(
                f"two of the ten give an identical {shape}, and the engine "
                f"has nothing else to tell them apart by")


def flat_paragraphs(paragraphs: tuple[str, ...] | str) -> str:
    if isinstance(paragraphs, str):
        paragraphs = (paragraphs,)
    joined = " ".join(paragraphs).replace("|", " ")
    return re.sub(r"\s+", " ", joined).strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the ten SECRET BASE residents in English.")
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
    print(f"Secret base trainers English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

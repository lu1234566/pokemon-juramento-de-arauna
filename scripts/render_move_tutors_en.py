#!/usr/bin/env python3
"""The ten people scattered across ARAUNA who will teach one move each.

Every tutor gets four texts -- the offer, the refusal, the request for a
POKéMON, and what they say once the move is taught -- plus one warning they
all share about a move that can only be learned once.

The offer is the one that has to work. A player standing in front of a
stranger has to come away knowing which move is on the table, because the
move is the only reason to say yes and the game does not print it anywhere
else on that screen. So the move name is checked into all ten offers, spelled
exactly as src/data/text/move_names.h spells it: a tutor who offers
DYNAMIC PUNCH and a party screen that lists DYNAMICPUNCH have told the player
two different things.

Around that, each of the ten is written to belong to the town the engine
actually puts them in. Emerald leaves most of them placeless, which is why
its ten tutors blur together; here the one on the department store roof
is thinking about the size of BAIA DAS LUZES beneath her, and the one in
CASA DA FOGUEIRA is planning to leave it.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

SOURCE = ROOT / "data" / "text" / "move_tutors.inc"

BOX = TextBox({}, width=34)

# Names printed elsewhere that must not be broken across a line.
WHOLE = ("FURY CUTTER", "SLEEP TALK", "DOUBLE-EDGE", "DYNAMICPUNCH",
         "PORTO DO SAL", "ENCRUZILHADA", "VALE DO SILENCIO",
         "SERTAO DE DENTRO", "CAMPO DAS CINZAS", "MATA DO MEIO",
         "BAIA DAS LUZES", "MISSOES DO CEU", "AGUAS DE M'BOI",
         "CASA DA FOGUEIRA", "GYM LEADER", "HIDDEN POWER")

SHAPES = ("Teach", "Declined", "WhichMon", "Taught")

# Two of the ten labels lost their "_Text" infix in Emerald and kept it that
# way, so the label is spelled out per tutor rather than derived.
LABELS: dict[str, dict[str, str]] = {
    "Mimic": {
        "Teach": "MoveTutor_MimicTeach",
        "Declined": "MoveTutor_MimicDeclined",
        "WhichMon": "MoveTutor_Text_MimicWhichMon",
        "Taught": "MoveTutor_Text_MimicTaught",
    },
}


def labels_for(key: str) -> dict[str, str]:
    if key in LABELS:
        return LABELS[key]
    return {shape: f"MoveTutor_Text_{key}{shape}" for shape in SHAPES}


# key -> (move as the party screen spells it, town, teach, declined,
#         whichmon, taught)
TUTORS: dict[str, tuple[str, str, tuple[str, ...], tuple[str, ...],
                        tuple[str, ...], tuple[str, ...]]] = {
    "Swagger": (
        "SWAGGER", "PORTO DO SAL",
        ("My POKéMON is the best there is. Better than yours, better than "
         "anyone's on this dock.",
         "That is how I used to talk, anyway, until the CHAIRMAN heard me "
         "doing it and had a word.",
         "Took the strut clean out of me, that word did.",
         "Still. If you like, I will teach a POKéMON of yours to SWAGGER."),
        ("No? Can you not enter into the spirit of the thing?",),
        ("Right. Which POKéMON wants to learn how to SWAGGER?",),
        ("From here on I shall praise my POKéMON without the strut.",),
    ),
    "Rollout": (
        "ROLLOUT", "ENCRUZILHADA",
        ("Did you ever notice you can go from this spot a very long way that "
         "direction without turning once?",
         "I reckon I could roll it. All the way.",
         "Do you suppose your POKéMON would want to roll too?",
         "I can teach one ROLLOUT if you like."),
        ("No need to be shy about it.|Let us roll!",),
        ("Ehehe, of course! It would be grand if the POKéMON looked a bit "
         "like me.",),
        ("Rolling about in the grass is the best of it. Come on -- let us "
         "roll!",),
    ),
    "FuryCutter": (
        "FURY CUTTER", "VALE DO SILENCIO",
        ("There is a move that gets stronger the more times you use it in a "
         "row.",
         "BUG-type, and about as wicked as they come.",
         "FURY CUTTER, it is called.|Shall I teach it to a POKéMON?"),
        ("We are not on the same wavelength, you and I.",),
        ("Yay!|Show me which POKéMON I am teaching.",),
        ("The thrill of it is watching to see whether it keeps landing.",),
    ),
    "Mimic": (
        "MIMIC", "SERTAO DE DENTRO",
        ("Ah, young one!",
         "I am a young one myself, but I take on the manner and the speech "
         "of the old folk of this town.",
         "So what do you say, young one? Would you accept, were I to offer "
         "to teach the move MIMIC?"),
        ("Oh, boo! And I did want to teach your POKéMON MIMIC!",),
        ("Fwofwo! And so I shall!|Let me see the POKéMON you would have me "
         "teach.",),
        ("MIMIC is a move of great depth.",
         "Could you carry it off as well as I do, I wonder...?"),
    ),
    "Metronome": (
        "METRONOME", "CAMPO DAS CINZAS",
        ("I want all manner of things.|And my allowance is spent.",
         "Would it not be lovely if there were a spell that made money "
         "appear when you waggled a finger?",
         "If you like, I can teach your POKéMON METRONOME.",
         "No money will appear. But the finger will waggle. Yes?"),
        ("All right. I shall be here if you change your mind.",),
        ("Good!|Which POKéMON am I teaching?",),
        ("When a POKéMON waggles its finger like that, all sorts of fine "
         "things come of it.",
         "Would it not be lovely if we could do the same?"),
    ),
    "SleepTalk": (
        "SLEEP TALK", "MATA DO MEIO",
        ("Humph. My wife stays awake on HIDDEN POWER.",
         "She ought to do what I do -- take a nap, and talk in her sleep.",
         "I can teach your POKéMON to SLEEP TALK instead. Any interest?"),
        ("Fine, fine. You would rather stay awake on HIDDEN POWER as well...",),
        ("Ah, a child who appreciates things!|Which POKéMON am I teaching?",),
        ("I have never once got my wife's coin trick right.",
         "It would content me to get it right in my sleep, at least..."),
    ),
    "Substitute": (
        "SUBSTITUTE", "BAIA DAS LUZES",
        ("When I look out at the whole of BAIA DAS LUZES from up here on "
         "the roof...",
         "I think how fine it would be if there were more than one of me, so "
         "I could live every one of the lives down there.",
         "Not possible, of course.|Giggle...",
         "Oh! Would you like a POKéMON of yours to learn SUBSTITUTE?"),
        ("No?",
         "A POKéMON can put up a copy of itself with it, you know."),
        ("Giggle...|Which POKéMON shall I teach SUBSTITUTE?",),
        ("We people ought to make the very most of the one life we get!",
         "I hope you come round to it too!"),
    ),
    "DynamicPunch": (
        "DYNAMICPUNCH", "MISSOES DO CEU",
        ("I cannot do this any more!",
         "It is hopeless. Utterly hopeless.",
         "I am a FIGHTING-type TRAINER, so I cannot win at the MISSOES DO "
         "CEU GYM however hard I go at it!",
         "Aargh! Punch! Punch! Punch!|Punch! Punch! Punch!",
         "What -- do not look at me like that! I am only hitting the "
         "ground!",
         "Or shall I teach your POKéMON DYNAMICPUNCH instead?"),
        ("Blast! Are you laughing at me as well?|Punch! Punch! Punch!",),
        ("What? You will? You are a good sort!|Which POKéMON am I "
         "teaching?",),
        ("Go and win at the MISSOES DO CEU GYM with that DYNAMICPUNCH. For "
         "the both of us.",),
    ),
    "DoubleEdge": (
        "DOUBLE-EDGE", "AGUAS DE M'BOI",
        ("Sigh...",
         "AGUAS DE M'BOI's GYM LEADER CELINA is quite the most admirable "
         "person in this town.",
         "Which of course means half the town thinks so too, and I am "
         "somewhere at the back of the queue.",
         "All that appeal, and a DOUBLE-EDGE besides. I never got so much as "
         "a glance.",
         "Please -- let me teach your POKéMON DOUBLE-EDGE."),
        ("Oh...|Turned down by you as well...",),
        ("Right. Which POKéMON shall I teach DOUBLE-EDGE?",),
        ("No more living for love. I am going to get tough instead.",),
    ),
    "Explosion": (
        "EXPLOSION", "CASA DA FOGUEIRA",
        ("I do not intend to spend my whole life going nowhere on a row of "
         "planks over the sea.",
         "You watch. I will get myself to a city and I will be enormous "
         "there.",
         "I am telling you, I am going to set off an EXPLOSION of "
         "popularity.",
         "Since you overheard all that, I shall gladly teach your POKéMON "
         "EXPLOSION."),
        ("Gaah! Turning me down because I am from the middle of nowhere?",),
        ("Right! An EXPLOSION it is!|Which POKéMON wants to go up?",),
        ("Years I have spent teaching POKéMON EXPLOSION, and I have yet to "
         "set off my own...",
         "Perhaps because deep down I would sooner stay here."),
    ),
}

SHARED: dict[str, tuple[str, ...]] = {
    "MoveTutor_Text_ThisMoveCanOnlyBeLearnedOnce": (
        "This move can be taught once and once only. Is that all right?",
    ),
}


def build() -> dict[str, tuple[str, ...]]:
    blocks: dict[str, tuple[str, ...]] = dict(SHARED)
    for key, (_move, _town, teach, declined, which, taught) in TUTORS.items():
        labels = labels_for(key)
        blocks[labels["Teach"]] = teach
        blocks[labels["Declined"]] = declined
        blocks[labels["WhichMon"]] = which
        blocks[labels["Taught"]] = taught
    return blocks


TARGETS: dict[str, tuple[str, ...]] = build()


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
        masked = masked[:start] + '\t.string "<ARAUNA_MOVE_TUTORS_EN>"\n\n' + masked[end:]
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
    move_names = (ROOT / "src" / "data" / "text" / "move_names.h").read_text(
        encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip()

    for key, (move, _town, *_rest) in TUTORS.items():
        labels = labels_for(key)
        # Spelled the way the party screen spells it, or the offer and the
        # screen the player sees next describe two different moves.
        if f'_("{move}")' not in move_names:
            raise ValueError(
                f"{key}: {move!r} is not how move_names.h spells this move")
        offer = flat(labels["Teach"])
        if move not in offer:
            raise ValueError(
                f"{labels['Teach']}: no longer names {move}, which is the only "
                f"reason a player would say yes")
        # The party menu opens straight after this line; it has to be a
        # request for a POKéMON, not just an exclamation.
        if "POKéMON" not in flat(labels["WhichMon"]):
            raise ValueError(
                f"{labels['WhichMon']}: does not ask for a POKéMON, but the "
                f"party menu opens on it")

    # Ten strangers doing the same job. If two of them say the same thing,
    # one of them has stopped being a person.
    for shape in SHAPES:
        said = [flat(labels_for(key)[shape]) for key in TUTORS]
        if len(set(said)) != len(said):
            raise ValueError(f"two tutors give an identical {shape}")

    # The one warning they share is the only place the player is told the
    # lesson cannot be repeated.
    once = flat("MoveTutor_Text_ThisMoveCanOnlyBeLearnedOnce")
    if "once" not in once.lower():
        raise ValueError(
            "ThisMoveCanOnlyBeLearnedOnce: no longer says the move can be "
            "taught only once")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the ten move tutors in English.")
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
    print(f"Move tutors English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""The AGUAS DE M'BOI GYM floor, and the two children who argue about size.

The gym's basement is ten TRAINERS on an ice floor, and between them they
give the whole of the puzzle: that reaching CELINA means stepping on every
tile, and that something happens when the last one cracks. Nothing else in
the building says it, so both halves are held.

The house is a mirrored argument. A brother swears Bumba-Boi grow larger; his
sister swears Beata do. They have eight texts each and every one of hers is
the reflection of one of his -- so both sides are generated from a single
table that says whose champion is whose, and the renderer checks each half
names its own species, names the rival's, and never gets the two the wrong
way round. Written by hand, that swap is exactly the mistake nobody would
catch: the game would still run, and a child would be arguing for the other
one's side.

Both species names are checked against species_names.h.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "arauna"))
from textbox import TextBox, glued  # noqa: E402

GYM = ROOT / "data" / "maps" / "SootopolisCity_Gym_B1F" / "scripts.inc"
HOUSE = ROOT / "data" / "maps" / "SootopolisCity_LotadAndSeedotHouse" / "scripts.inc"
SPECIES_TABLE = ROOT / "src" / "data" / "text" / "species_names.h"

BOX = TextBox({"{PLAYER}": 7, "{STR_VAR_1}": 10, "{STR_VAR_2}": 10,
               "{STR_VAR_3}": 4}, width=34)

WHOLE = ("AGUAS DE M'BOI", "GYM LEADER", "POKéMON GYM", "ARAUNA", "BAG",
         "POTION", "CELINA")

# Which sibling champions which species, and how the labels are spelled.
# "Seedot" is the elder brother's; "Lotad" the younger sister's.
SIBLINGS: dict[str, dict[str, str]] = {
    "Seedot": {
        "species": "Bumba-Boi",
        "constant": "SEEDOT",
        "rival": "Beata",
        "rival_constant": "LOTAD",
        # How each refers to the other.
        "relation": "my younger brother",
        "rival_relation": "my big brother",
        "superlative": "giant",
    },
    "Lotad": {
        "species": "Beata",
        "constant": "LOTAD",
        "rival": "Bumba-Boi",
        "rival_constant": "SEEDOT",
        "relation": "my big brother",
        "rival_relation": "my younger brother",
        "superlative": "colossus",
    },
}

GYM_TRAINERS: dict[str, tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]] = {
    "Andrea": (
        ("I shall show you the fine technique I learned from our LEADER, "
         "CELINA.",),
        ("Forgive me, CELINA...",),
        ("Watch what happens if you crack every tile on this floor.",),
    ),
    "Crissy": (
        ("You have come all this way and you will not get to see CELINA.",
         "Not if you lose to me you will not."),
        ("You are strong!|Your sweet face had me completely fooled!",),
        ("You might just be good enough not to be finished by CELINA in one "
         "go.",),
    ),
    "Daphne": (
        ("The sight of CELINA running a battle...",
         "The beauty of it was what made me a TRAINER at all."),
        ("You battled with more beauty than I could find in myself...",),
        ("There is a grace about the way you fight. It is wonderful.",
         "Oh... how fortunate I am, to have found POKéMON."),
    ),
    "Connie": (
        ("Somebody ought to show you how hard a battle can be.",),
        ("Oh.|You are strong.",),
        ("I shall tell you something worth knowing.",
         "To reach CELINA you must step on every tile of the floor, and each "
         "of them only once."),
    ),
    "Bridget": (
        ("The POKéMON GYM of the highest standing anywhere in ARAUNA...",
         "That is the AGUAS DE M'BOI GYM."),
        ("What a standard you are at!",),
        ("Rather than sit content in a strong GYM, I imagine training "
         "elsewhere would make you stronger.",
         "And more to the point, it looks a great deal more fun."),
    ),
    "Olivia": (
        ("I train my POKéMON alongside CELINA.",
         "Do not take me for an easy afternoon."),
        ("Beaten...",),
        ("I think there is something in you.|Why not stay and train with "
         "us?",),
    ),
    "Tiffany": (
        ("A graceful glide across the ice, and not a line crossed...",
         "A TRAINER doing that would be a beautiful thing to watch."),
        ("Well, excuse me!",),
        ("It is obvious enough, but how strong a TRAINER is has nothing "
         "whatever to do with how old they are.",),
    ),
    "Bethany": (
        ("When I am with my POKéMON the time goes before you can say "
         "“Oops!”",),
        ("Oops!",),
        ("I do wish I could let go of a lost cause before I get as far as "
         "“Oops!”",),
    ),
    "Annika": (
        ("I can battle you with some genuinely rare POKéMON, if you like.",),
        ("Oh, there now. Did you get a proper look at mine?",),
        ("I came to this GYM because CELINA said kind things about my "
         "darlings.",
         "Oh, if only I had met CELINA years ago, when I was younger..."),
    ),
    "Brianna": (
        ("Giggle...|That grim little face of yours is quite charming.",),
        ("Oh, dear.|I went far too easy on you.",),
        ("You would not lay a finger on CELINA. I am certain of it. "
         "Giggle...",),
    ),
}


def house_blocks() -> dict[str, tuple[str, ...]]:
    prefix = "SootopolisCity_LotadAndSeedotHouse_Text_"
    blocks: dict[str, tuple[str, ...]] = {}
    for key, who in SIBLINGS.items():
        mine, rival = who["species"], who["rival"]
        blocks[f"{prefix}PleaseShowMeBig{key}"] = (
            f"Do you know the POKéMON {mine}?|You hardly ever see one in "
            f"AGUAS DE M'BOI.",
            f"Well, I love a big {mine}. The bigger the better.",
            f"But {who['relation']} says {rival} grow bigger.",
            f"Which is nonsense. A {mine} has to be bigger than that.",
            f"Hm? Have you got a {mine} with you?|P-please, let me see it!",
        )
        blocks[f"{prefix}{'GoshMightBeBiggerThanLotad' if key == 'Seedot' else 'WowMightBeBiggerThanSeedot'}"] = (
            "{STR_VAR_2} inches!|Now that is a big one!",
            f"It might even beat the great {rival} {who['relation']} saw.",
            "Thank you for showing me.|Here -- for your trouble.",
        )
        blocks[f"{prefix}SeenBigger{key}"] = (
            "{STR_VAR_2} inches, is it?",
            f"Hmm... I have seen a {mine} bigger than that one.",
        )
        blocks[f"{prefix}ThatsNot{key}"] = (
            f"Well, that is something to look at...|But it is no {mine}!",
        )
        blocks[f"{prefix}DontHaveBig{key}"] = (
            f"No big {mine} on you?|What a shame...",
            f"If you come by a big {mine}, do bring it and show me.",
        )
        blocks[f"{prefix}Biggest{key}InHistory"] = (
            f"The biggest {mine} on record.",
            "{STR_VAR_2}'s {STR_VAR_3}-inch " + who["superlative"] + ".",
            f"A {mine} bigger than any {rival}. Which is all anyone wanted.",
        )
        index = "1" if key == "Seedot" else "2"
        blocks[f"{prefix}ReceivedPotion{index}"] = (
            "{PLAYER} received a POTION.",
        )
        blocks[f"{prefix}BagCrammedFull{index}"] = (
            "Hm?|Your BAG is crammed full.",
        )
    return blocks


def build() -> dict[str, dict[str, tuple[str, ...]]]:
    gym: dict[str, tuple[str, ...]] = {}
    for name, (intro, defeat, after) in GYM_TRAINERS.items():
        gym[f"SootopolisCity_Gym_B1F_Text_{name}Intro"] = intro
        gym[f"SootopolisCity_Gym_B1F_Text_{name}Defeat"] = defeat
        gym[f"SootopolisCity_Gym_B1F_Text_{name}PostBattle"] = after
    return {"gym": gym, "house": house_blocks()}


GROUPS = build()
TARGETS: dict[str, tuple[str, ...]] = {
    label: body for group in GROUPS.values() for label, body in group.items()}
FILES = {"gym": GYM, "house": HOUSE}


def which(label: str) -> str:
    for name, group in GROUPS.items():
        if label in group:
            return name
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


def render(sources: dict[str, str]) -> dict[str, str]:
    composed = payloads()
    rendered = dict(sources)
    for label in TARGETS:
        group = which(label)
        matches = list(block_pattern(label).finditer(rendered[group]))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        if ".string" not in matches[0].group("body"):
            raise ValueError(f"{label}: target contains no .string payload")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in composed[label]) + "\n"
        start, end = matches[0].span("body")
        rendered[group] = rendered[group][:start] + new_body + rendered[group][end:]
    return rendered


def mask(texts: dict[str, str]) -> dict[str, str]:
    masked = dict(texts)
    for label in TARGETS:
        group = which(label)
        match = block_pattern(label).search(masked[group])
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked[group] = (masked[group][:start]
                         + '\t.string "<ARAUNA_MBOI_INTERIORS_EN>"\n\n'
                         + masked[group][end:])
    return masked


def validate_slots(sources: dict[str, str]) -> None:
    composed = payloads()
    for label in TARGETS:
        body = block_pattern(label).search(sources[which(label)]).group("body")
        available = set(re.findall(r"\{[A-Za-z_0-9]+\}", body))
        used = set(re.findall(r"\{[A-Za-z_0-9]+\}", "".join(composed[label])))
        if used - available:
            raise ValueError(
                f"{label}: uses {sorted(used - available)}, which the engine "
                f"does not fill here; the source uses {sorted(available)}")


def validate_rendered(sources: dict[str, str], rendered: dict[str, str]) -> None:
    if mask(sources) != mask(rendered):
        raise ValueError("non-dialogue structure changed while rendering")

    composed = payloads()
    species = SPECIES_TABLE.read_text(encoding="utf-8")

    def flat(label: str) -> str:
        return re.sub(r"\s+", " ",
                      re.sub(r"\\[npl]|\x01", " ",
                             "".join(composed[label]))).strip().rstrip("$")

    # Both halves of the gym's puzzle hint, and nothing else in the building
    # gives either.
    route = flat("SootopolisCity_Gym_B1F_Text_ConniePostBattle")
    if "every tile" not in route or "once" not in route:
        raise ValueError(
            "ConniePostBattle: no longer gives the floor rule, which is the "
            "only statement of it in the GYM")
    if "crack" not in flat("SootopolisCity_Gym_B1F_Text_AndreaPostBattle"):
        raise ValueError(
            "AndreaPostBattle: no longer hints at what cracking the tiles "
            "does")

    # Ten TRAINERS, told apart by nothing but what they say.
    for shape in ("Intro", "Defeat", "PostBattle"):
        said = [flat(f"SootopolisCity_Gym_B1F_Text_{name}{shape}")
                for name in GYM_TRAINERS]
        if len(set(said)) != len(said):
            raise ValueError(f"two GYM TRAINERS give an identical {shape}")

    # The two children are a mirror. Each half must champion its own species
    # and cite the other's -- get that backwards and the argument inverts.
    prefix = "SootopolisCity_LotadAndSeedotHouse_Text_"
    for key, who in SIBLINGS.items():
        mine, rival = who["species"], who["rival"]
        for constant, name in ((who["constant"], mine),
                               (who["rival_constant"], rival)):
            if f'[SPECIES_{constant}] = _("{name}")' not in species:
                raise ValueError(
                    f"{key}: the child argues about {name!r}, which is not "
                    f"what species_names.h calls SPECIES_{constant}")
        pitch = flat(f"{prefix}PleaseShowMeBig{key}")
        if mine not in pitch:
            raise ValueError(f"PleaseShowMeBig{key}: no longer names {mine}")
        if rival not in pitch:
            raise ValueError(
                f"PleaseShowMeBig{key}: no longer names {rival}, so there is "
                f"no argument left to have")
        if pitch.index(mine) > pitch.index(rival):
            raise ValueError(
                f"PleaseShowMeBig{key}: leads with {rival} rather than "
                f"{mine}, so this child is arguing the other one's side")
        for label in (f"SeenBigger{key}", f"ThatsNot{key}",
                      f"DontHaveBig{key}", f"Biggest{key}InHistory"):
            if mine not in flat(f"{prefix}{label}"):
                raise ValueError(f"{label}: no longer names {mine}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the AGUAS DE M'BOI GYM floor and size house.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    sources = {name: path.read_text(encoding="utf-8")
               for name, path in FILES.items()}
    validate_slots(sources)
    rendered = render(sources)
    validate_rendered(sources, rendered)

    if args.in_place:
        for name, path in FILES.items():
            path.write_text(rendered[name], encoding="utf-8")
    print(f"Aguas de M'Boi interiors English renderer OK: {len(TARGETS)} blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

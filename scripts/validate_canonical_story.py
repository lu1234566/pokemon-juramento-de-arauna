#!/usr/bin/env python3
"""Validate the canonical narrative spine of the prologue (Roteiro Canônico v2.0).

Covers two systems that the rest of the campaign hangs on:

* **P08 — the three founding stories of Dona Zila.** One block per starter,
  present in both languages, wired to the starter confirmation and reachable
  through ``VAR_ARAUNA_STARTER_CHOICE``. The canon requires the three blocks to
  carry equal weight and to be reused verbatim by the post-game radio quest, so
  they must stay in the shared story pack rather than being inlined in a map.
* **The Bond system.** Three axes (Courage, Wisdom, Compassion) packed into a
  single var so the save layout never grows, plus the First Link award of two
  points to the chosen axis (canon 9.4).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STORY_LABELS = (
    "AraunaZilaStory_Text_Pimpau",
    "AraunaZilaStory_Text_Caramelo",
    "AraunaZilaStory_Text_Quero",
)

# Starter choice value -> dispatcher branch that tells that starter's story.
STORY_BRANCHES = {
    1: "AraunaPlayerHouse_EventScript_ZilaStoryPimpau",
    2: "AraunaPlayerHouse_EventScript_ZilaStoryCaramelo",
    3: "AraunaPlayerHouse_EventScript_ZilaStoryQuero",
}

AXIS_POINTS = {
    "ARAUNA_BOND_COURAGE_POINT": 1,
    "ARAUNA_BOND_WISDOM_POINT": 32,
    "ARAUNA_BOND_COMPASSION_POINT": 1024,
}

# First Link choice value -> axis increment awarded twice (canon 9.4).
FIRST_LINK_AWARDS = {
    1: "ARAUNA_BOND_COURAGE_POINT",
    2: "ARAUNA_BOND_WISDOM_POINT",
    3: "ARAUNA_BOND_COMPASSION_POINT",
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise ValueError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def story_block(source: str, label: str) -> str:
    marker = f"{label}::"
    if marker not in source:
        fail(f"founding story is missing: {label}")
    return source.split(marker, 1)[1].split('$"', 1)[0]


def validate_founding_stories() -> None:
    english = read("data/text/arauna/en/opening.inc")
    portuguese = read("data/text/arauna/pt_br/opening.inc")

    for label in STORY_LABELS:
        for language, source in (("en", english), ("pt_br", portuguese)):
            block = story_block(source, label)
            # The canon blocks are long-form oral storytelling; a stub would
            # silently drop the emotional core of the prologue.
            require(
                block.count(".string") >= 12,
                f"{language}:{label} is too short to be the canonical block",
            )

    # Equal weight: no block may be dramatically shorter than the others.
    lengths = [len(story_block(english, label)) for label in STORY_LABELS]
    require(
        min(lengths) * 2 >= max(lengths),
        "the three founding stories must carry comparable weight",
    )

    house = read("data/maps/AraunaPlayerHouse/scripts.inc")
    require(
        "call AraunaPlayerHouse_EventScript_ZilaFoundingStory" in house,
        "the starter confirmation does not tell the founding story (P08)",
    )
    require(
        "setflag FLAG_ARAUNA_STARTER_STORY_HEARD" in house,
        "the founding story does not record FLAG_ARAUNA_STARTER_STORY_HEARD",
    )

    dispatcher = house.split(
        "AraunaPlayerHouse_EventScript_ZilaFoundingStory::", 1
    )[1].split("\nAraunaPlayerHouse_EventScript_ZilaStoryPimpau::", 1)[0]
    for choice, branch in STORY_BRANCHES.items():
        require(
            f"call_if_eq VAR_ARAUNA_STARTER_CHOICE, {choice}, {branch}" in dispatcher,
            f"starter choice {choice} does not reach its founding story",
        )

    for label, branch in zip(STORY_LABELS, STORY_BRANCHES.values()):
        block = house.split(f"{branch}::", 1)[1].split("\n\n", 1)[0]
        require(label in block, f"{branch} does not show {label}")

    require(
        "FLAG_ARAUNA_STARTER_STORY_HEARD" in read("include/constants/flags.h"),
        "FLAG_ARAUNA_STARTER_STORY_HEARD is not defined",
    )


def validate_bond_system() -> None:
    vars_source = read("include/constants/vars.h")

    require(
        "VAR_ARAUNA_BOND_AXES" in vars_source,
        "the packed Bond axes var is missing",
    )
    # The axes must stay packed in one var: adding vars would grow the save block.
    match = re.search(r"#define VARS_END\s+(0x[0-9A-Fa-f]+)", vars_source)
    require(match is not None, "VARS_END is missing")
    require(
        int(match.group(1), 16) == 0x40FF,
        "VARS_END moved: the Bond axes must stay packed so the save layout is stable",
    )

    for name, value in AXIS_POINTS.items():
        found = re.search(rf"#define {name}\s+(\d+)", vars_source)
        require(found is not None, f"{name} is not defined")
        require(
            int(found.group(1)) == value,
            f"{name} must be {value} to stay inside its 5-bit field",
        )

    notebook = read("src/arauna_notebook.c")
    require(
        "u16 GetAraunaDominantBond(void)" in notebook,
        "the dominant-bond reader is missing",
    )
    require(
        "def_special GetAraunaDominantBond" in read("data/specials.inc"),
        "GetAraunaDominantBond is not registered as a special",
    )
    # Canon 8.1: qualitative feedback only, never numbers.
    for phrase in (
        "You tend to arrive before",
        "You look for the thread before",
        "You listen to those left inside",
        "no oath holds",
    ):
        require(phrase in notebook, f"notebook Bond reading is missing: {phrase!r}")
    require(
        "ConvertIntToDecimalStringN" not in notebook,
        "the notebook must not display Bond numbers",
    )

    ruin = read("data/maps/AraunaFirstLinkRuin/scripts.inc")
    for choice, point in FIRST_LINK_AWARDS.items():
        block = ruin.split(f"setvar VAR_ARAUNA_BOND_CHOICE, {choice}", 1)[1].split(
            "msgbox", 1
        )[0]
        require(
            block.count(f"addvar VAR_ARAUNA_BOND_AXES, {point}") == 2,
            f"First Link choice {choice} must award two points to {point}",
        )


def main() -> int:
    validate_founding_stories()
    validate_bond_system()
    print(
        "Canonical story validated: three founding stories in both languages, "
        "wired to the starter choice, and the packed three-axis Bond system "
        "with the First Link award"
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, IndexError) as error:
        print(f"Canonical story validation failed: {error}", file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLOOR1 = ROOT / "data" / "maps" / "MtPyre_1F" / "scripts.inc"
FLOOR2 = ROOT / "data" / "maps" / "MtPyre_2F" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

FLOOR1_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "MtPyre_1F_Text_TakeThisForYourOwnGood": (
        ("MEMORIAL DOS NOMES", "for your own good"),
        (
            "The upper memorial is quieter.\\p",
            "Take this CLEANSE TAG.\\p",
            "It helps with wild POKéMON.\\n",
            "Grief is another matter.$",
        ),
    ),
    "MtPyre_1F_Text_ExplainCleanseTag": (
        ("CLEANSE TAG", "wild POKéMON"),
        (
            "Let a POKéMON hold that\\n",
            "CLEANSE TAG.\\p",
            "It keeps some wild POKéMON away.$",
        ),
    ),
    "MtPyre_1F_Text_ComeToPayRespects": (
        ("pay your respect", "departed POKéMON"),
        (
            "A boy named CIRO passed me.\\p",
            "He read every plaque in sight.\\p",
            "He didn't say a word.$",
        ),
    ),
    "MtPyre_1F_Text_RestingPlaceOfZigzagoon": (
        ("final resting place", "ZIGZAGOON"),
        (
            "My ZIGZAGOON's name is here.\\p",
            "Saying it aloud still hurts.\\p",
            "Not saying it hurts differently.$",
        ),
    ),
}

FLOOR2_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "MtPyre_2F_Text_MemoriesOfSkitty": (
        ("darling SKITTY", "eyes overflow"),
        (
            "My SKITTY's name is upstairs.\\p",
            "I bring these flowers each year.\\p",
            "They wilt. The name stays.$",
        ),
    ),
    "MtPyre_2F_Text_TumbledFromFloorAbove": (
        ("holes in the", "floor above"),
        (
            "Watch the cracked floor.\\p",
            "Memory deserves attention.\\n",
            "So does where you step.$",
        ),
    ),
    "MtPyre_2F_Text_MarkIntro": (
        ("searching for POKéMON", "You're rude"),
        (
            "I came looking for rare POKéMON.\\p",
            "Then I read some of the names.\\p",
            "Now I feel like an intruder.$",
        ),
    ),
    "MtPyre_2F_Text_MarkDefeat": (
        ("forgive me",),
        ("Okay... I deserved that.$",),
    ),
    "MtPyre_2F_Text_MarkPostBattle": (
        ("rare POKéMON",),
        (
            "I'll leave catching for later.\\p",
            "Some places ask for restraint.$",
        ),
    ),
    "MtPyre_2F_Text_LukeIntro": (
        ("LUCA:", "show her how cool"),
        (
            "LUCA: We came here together.\\p",
            "I said I wasn't nervous.\\p",
            "That was a lie. Battle me?$",
        ),
    ),
    "MtPyre_2F_Text_LukeDefeat": (
        ("Whoopsie",),
        ("LUCA: Yeah... still nervous.$",),
    ),
    "MtPyre_2F_Text_LukePostBattle": (
        ("right here by your side",),
        (
            "LUCA: LIA stayed beside me.\\p",
            "That helped more than bravado.$",
        ),
    ),
    "MtPyre_2F_Text_LukeNotEnoughMons": (
        ("bring some more POKéMON",),
        (
            "LUCA: Bring two POKéMON.\\p",
            "We shouldn't turn this into\\n",
            "a careless fight.$",
        ),
    ),
    "MtPyre_2F_Text_DezIntro": (
        ("LIA:", "came here on a dare"),
        (
            "LIA: We came to leave flowers.\\p",
            "LUCA keeps pretending he's calm.\\p",
            "Help me prove otherwise.$",
        ),
    ),
    "MtPyre_2F_Text_DezDefeat": (
        ("Waaaah",),
        ("LIA: Okay, that proved enough.$",),
    ),
    "MtPyre_2F_Text_DezPostBattle": (
        ("lovey-dovey",),
        (
            "LIA: Being scared together is\\n",
            "still being together.$",
        ),
    ),
    "MtPyre_2F_Text_DezNotEnoughMons": (
        ("at least two POKéMON",),
        (
            "LIA: Bring at least two POKéMON.\\p",
            "If we battle here, do it right.$",
        ),
    ),
    "MtPyre_2F_Text_LeahIntro": (
        ("unfamiliar sight", "Depart"),
        (
            "My family helps tend this floor.\\p",
            "Respect the names, and I'll\\n",
            "respect your challenge.$",
        ),
    ),
    "MtPyre_2F_Text_LeahDefeat": (
        ("You're durable",),
        ("You were careful. Good.$",),
    ),
    "MtPyre_2F_Text_LeahPostBattle": (
        ("great-grandmother", "protect this"),
        (
            "DONA ZILA says a name changes\\n",
            "when different mouths carry it.\\p",
            "That doesn't make it less true.$",
        ),
    ),
    "MtPyre_2F_Text_ZanderIntro": (
        ("terrified",),
        (
            "Did you hear that echo?\\p",
            "Please tell me that was you.$",
        ),
    ),
    "MtPyre_2F_Text_ZanderDefeat": (
        ("lost my wits",),
        ("Great. Now I'm more awake.$",),
    ),
    "MtPyre_2F_Text_ZanderPostBattle": (
        ("freaked out", "come here to train"),
        (
            "I came here to train my nerve.\\p",
            "Maybe fear deserves attention.$",
        ),
    ),
}

CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^(?P<label>{re.escape(label)}:)\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    for label, (_, payloads) in targets.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render_file(
    source: str,
    targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]],
) -> str:
    validate_widths(targets)
    rendered = source
    for label, (markers, payloads) in targets.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target body contains no .string data")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: expected source marker not found: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(
    source: str,
    targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]],
) -> str:
    masked = source
    for label in targets:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_MEMORIAL_LOWER>"\n\n' + masked[end:]
    return masked


def validate_structure(
    source: str,
    rendered: str,
    targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]],
) -> None:
    if mask_targets(source, targets) != mask_targets(rendered, targets):
        raise ValueError("non-dialogue Memorial lower-floor structure changed")

    for label, (_, payloads) in targets.items():
        match = block_pattern(label).search(rendered)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")


def validate_preserved(floor1: str, floor2: str) -> None:
    preserved_floor1 = (
        "giveitem ITEM_CLEANSE_TAG",
        "FLAG_RECEIVED_CLEANSE_TAG",
        "Common_EventScript_ShowBagIsFull",
    )
    preserved_floor2 = (
        "CaveHole_CheckFallDownHole",
        "CaveHole_FixCrackedGround",
        "setholewarp MAP_MT_PYRE_1F",
        "TRAINER_MARK",
        "TRAINER_DEZ_AND_LUKE",
        "TRAINER_LEAH",
        "TRAINER_ZANDER",
    )
    for token in preserved_floor1:
        if token not in floor1:
            raise ValueError(f"preserved Memorial 1F token missing: {token}")
    for token in preserved_floor2:
        if token not in floor2:
            raise ValueError(f"preserved Memorial 2F token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the lower Memorial dos Nomes floors in English without changing Emerald gameplay wiring."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source1 = FLOOR1.read_text(encoding="utf-8")
    source2 = FLOOR2.read_text(encoding="utf-8")
    rendered1 = render_file(source1, FLOOR1_TARGETS)
    rendered2 = render_file(source2, FLOOR2_TARGETS)
    validate_structure(source1, rendered1, FLOOR1_TARGETS)
    validate_structure(source2, rendered2, FLOOR2_TARGETS)
    validate_preserved(rendered1, rendered2)

    if args.check:
        total = len(FLOOR1_TARGETS) + len(FLOOR2_TARGETS)
        print(f"Memorial lower floors English renderer OK: {total} text blocks validated.")
        return 0
    if args.in_place:
        FLOOR1.write_text(rendered1, encoding="utf-8")
        FLOOR2.write_text(rendered2, encoding="utf-8")
        return 0

    print(f"===== {FLOOR1.relative_to(ROOT)} =====")
    print(rendered1, end="" if rendered1.endswith("\n") else "\n")
    print(f"===== {FLOOR2.relative_to(ROOT)} =====")
    print(rendered2, end="" if rendered2.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

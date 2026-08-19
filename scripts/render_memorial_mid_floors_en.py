#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLOORS = {
    "3F": ROOT / "data" / "maps" / "MtPyre_3F" / "scripts.inc",
    "4F": ROOT / "data" / "maps" / "MtPyre_4F" / "scripts.inc",
    "5F": ROOT / "data" / "maps" / "MtPyre_5F" / "scripts.inc",
    "6F": ROOT / "data" / "maps" / "MtPyre_6F" / "scripts.inc",
}
MAX_VISIBLE_WIDTH = 32

TARGETS: dict[str, dict[str, tuple[tuple[str, ...], tuple[str, ...]]]] = {
    "3F": {
        "MtPyre_3F_Text_WilliamIntro": (
            ("rich atmosphere", "psychic power"),
            (
                "Every name above us belonged\\n",
                "to a life, not a lesson.\\p",
                "If you climb carelessly,\\n",
                "I'll stop you here.$",
            ),
        ),
        "MtPyre_3F_Text_WilliamDefeat": (
            ("self-pity",),
            ("I mistook certainty for care.$",),
        ),
        "MtPyre_3F_Text_WilliamPostBattle": (
            ("psychic powers",),
            (
                "This place makes every answer\\n",
                "feel smaller than the question.$",
            ),
        ),
        "MtPyre_3F_Text_KaylaIntro": (
            ("no place for children",),
            (
                "You came all this way upward.\\p",
                "Tell me your POKéMON chose to\\n",
                "come with you.$",
            ),
        ),
        "MtPyre_3F_Text_KaylaDefeat": (
            ("lost that cleanly",),
            ("They answered before you did.$",),
        ),
        "MtPyre_3F_Text_KaylaPostBattle": (
            ("keep working", "summit"),
            (
                "A partner's trust is not proof\\n",
                "that every choice is right.$",
            ),
        ),
        "MtPyre_3F_Text_GabrielleIntro": (
            ("Why have you come here",),
            ("Why come to the MEMORIAL?$",),
        ),
        "MtPyre_3F_Text_GabrielleDefeat": (
            ("very special TRAINER",),
            ("You carry them carefully.$",),
        ),
        "MtPyre_3F_Text_GabriellePostBattle": (
            ("no longer of this world", "equally cherished"),
            (
                "The gone, the living, and those\\n",
                "you have yet to meet...\\p",
                "Care for them without turning\\n",
                "care into ownership.$",
            ),
        ),
        "MtPyre_3F_Text_GabrielleRegister": (
            ("grow up some more", "POKéNAV"),
            (
                "I want to see how your team\\n",
                "changes after this place.\\p",
                "May I register your POKéNAV?$",
            ),
        ),
        "MtPyre_3F_Text_GabrielleRematchIntro": (
            ("grown POKéMON",),
            (
                "You came back.\\p",
                "What did your POKéMON keep?$",
            ),
        ),
        "MtPyre_3F_Text_GabrielleRematchDefeat": (
            ("special person",),
            ("You both changed.$",),
        ),
        "MtPyre_3F_Text_GabriellePostRematch": (
            ("remembered that",),
            (
                "Memory changed you without\\n",
                "becoming your master.\\p",
                "That is worth remembering.$",
            ),
        ),
    },
    "4F": {
        # Emerald's 4F/5F script labels are historically swapped; preserve them.
        "MtPyre_5F_Text_AtsushiIntro": (
            ("Teacher", "watch over"),
            (
                "My teacher's name is above.\\p",
                "I still train like they might\\n",
                "correct my stance.$",
            ),
        ),
        "MtPyre_5F_Text_AtsushiDefeat": (
            ("Teacher", "forgive me"),
            ("Teacher... I rushed again.$",),
        ),
        "MtPyre_5F_Text_AtsushiPostBattle": (
            ("teacher", "true peace"),
            (
                "I used to think improvement\\n",
                "would repay the dead.\\p",
                "Now I think I simply miss them.$",
            ),
        ),
    },
    "5F": {
        "MtPyre_4F_Text_TashaIntro": (
            ("things horrifying", "shiver with fear"),
            (
                "I came here chasing fear.\\p",
                "Then the names stopped feeling\\n",
                "like scenery.\\p",
                "Battle me before I leave.$",
            ),
        ),
        "MtPyre_4F_Text_TashaDefeat": (
            ("Losing, I dislike",),
            ("Good. I needed that.$",),
        ),
        "MtPyre_4F_Text_TashaPostBattle": (
            ("dreadful things", "stay with me"),
            (
                "Dread is easy when no one has\\n",
                "a name.\\p",
                "Names make horror personal.$",
            ),
        ),
    },
    "6F": {
        "MtPyre_6F_Text_ValerieIntro": (
            ("curious power", "flows into me"),
            (
                "The higher I climb, the more\\n",
                "voices I imagine.\\p",
                "I know imagination isn't proof.$",
            ),
        ),
        "MtPyre_6F_Text_ValerieDefeat": (
            ("power is ebbing",),
            ("The noise is quieter now.$",),
        ),
        "MtPyre_6F_Text_ValeriePostBattle": (
            ("spirits", "fitful sleep"),
            (
                "Maybe the power I felt was only\\n",
                "attention sharpened by grief.$",
            ),
        ),
        "MtPyre_6F_Text_ValerieRegister": (
            ("little ability", "POKéNAV"),
            (
                "You notice things too.\\p",
                "Let me register your POKéNAV.\\p",
                "We can compare notes someday.$",
            ),
        ),
        "MtPyre_6F_Text_ValerieRematchIntro": (
            ("Behind you",),
            (
                "Behind you...\\p",
                "No. Just an old echo.$",
            ),
        ),
        "MtPyre_6F_Text_ValerieRematchDefeat": (
            ("faded away",),
            ("I chased the wrong signal.$",),
        ),
        "MtPyre_6F_Text_ValeriePostRematch": (
            ("POKéMON at rest", "play"),
            (
                "Not every echo is a message.\\p",
                "That makes the real ones matter.$",
            ),
        ),
        "MtPyre_6F_Text_CedricIntro": (
            ("lost your bearings", "Have no fear"),
            (
                "CIRO passed me on the stairs.\\p",
                "He asked which plaque held his\\n",
                "father's name.\\p",
                "I didn't know. Do you?$",
            ),
        ),
        "MtPyre_6F_Text_CedricDefeat": (
            ("Weren't you lost",),
            ("You weren't lost after all.$",),
        ),
        "MtPyre_6F_Text_CedricPostBattle": (
            ("lost TRAINER", "dirty"),
            (
                "He kept climbing after I said\\n",
                "I didn't know.\\p",
                "He looked angry at the question,\\n",
                "not at me.$",
            ),
        ),
    },
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
        masked = masked[:start] + '\t.string "<ARAUNA_MEMORIAL_MID>"\n\n' + masked[end:]
    return masked


def validate_structure(source: str, rendered: str, targets) -> None:
    if mask_targets(source, targets) != mask_targets(rendered, targets):
        raise ValueError("non-dialogue Memorial mid-floor structure changed")
    for label, (_, payloads) in targets.items():
        body = block_pattern(label).search(rendered).group("body")
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")


def validate_preserved(rendered: dict[str, str]) -> None:
    required = {
        "3F": (
            "TRAINER_WILLIAM",
            "TRAINER_KAYLA",
            "TRAINER_GABRIELLE_1",
            "register_matchcall TRAINER_GABRIELLE_1",
            "ShouldTryRematchBattle",
        ),
        "4F": ("TRAINER_ATSUSHI",),
        "5F": ("TRAINER_TASHA",),
        "6F": (
            "TRAINER_VALERIE_1",
            "TRAINER_CEDRIC",
            "register_matchcall TRAINER_VALERIE_1",
            "ShouldTryRematchBattle",
        ),
    }
    for floor, tokens in required.items():
        for token in tokens:
            if token not in rendered[floor]:
                raise ValueError(f"{floor}: preserved gameplay token missing: {token}")


def rendered_sources() -> dict[str, str]:
    output: dict[str, str] = {}
    for floor, path in FLOORS.items():
        source = path.read_text(encoding="utf-8")
        rendered = render_file(source, TARGETS[floor])
        validate_structure(source, rendered, TARGETS[floor])
        output[floor] = rendered
    validate_preserved(output)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Memorial dos Nomes 3F-6F in English without changing Emerald gameplay wiring."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = rendered_sources()
    if args.check:
        total = sum(len(targets) for targets in TARGETS.values())
        print(f"Memorial mid floors English renderer OK: {total} text blocks validated.")
        return 0
    if args.in_place:
        for floor, content in rendered.items():
            FLOORS[floor].write_text(content, encoding="utf-8")
        return 0

    for floor, content in rendered.items():
        print(f"===== {FLOORS[floor].relative_to(ROOT)} =====")
        print(content, end="" if content.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "PetalburgCity_Gym" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[str, ...]] = {
    "PetalburgCity_Gym_Text_RandallIntro": (
        "TRAINER: SPEED ROOM.\\p",
        "Moving first can set the tone\\n",
        "before a plan can settle.\\p",
        "Show me how you react.$",
    ),
    "PetalburgCity_Gym_Text_RandallDefeat": (
        "TRAINER: Fast enough for me.$",
    ),
    "PetalburgCity_Gym_Text_RandallPostBattle": (
        "Left: CONFUSION ROOM.\\p",
        "Right: DEFENSE ROOM.\\p",
        "Pick the habit you trust more.$",
    ),
    "PetalburgCity_Gym_Text_RandallPostBadge": (
        "TRAINER: ELIAS keeps us training\\n",
        "even after victory.\\p",
        "A habit stops helping when it\\n",
        "becomes automatic.$",
    ),
    "PetalburgCity_Gym_Text_ParkerIntro": (
        "TRAINER: CONFUSION ROOM.\\p",
        "Let's see whether your BOND holds\\n",
        "when commands become uncertain.$",
    ),
    "PetalburgCity_Gym_Text_ParkerDefeat": (
        "You kept listening to each other.$",
    ),
    "PetalburgCity_Gym_Text_ParkerPostBattle": (
        "Next is the POWER ROOM.\\p",
        "Expect direct pressure.$",
    ),
    "PetalburgCity_Gym_Text_ParkerPostBadge": (
        "Beating ELIAS made everyone here\\n",
        "train harder.\\p",
        "Good. Comfort dulls attention.$",
    ),
    "PetalburgCity_Gym_Text_GeorgeIntro": (
        "TRAINER: RECOVERY ROOM.\\p",
        "A battle can turn when a foe\\n",
        "refuses to stay worn down.\\p",
        "Can you keep your plan?$",
    ),
    "PetalburgCity_Gym_Text_GeorgeDefeat": (
        "You broke through every recovery.$",
    ),
    "PetalburgCity_Gym_Text_GeorgePostBattle": (
        "Next is the CRITICAL ROOM.\\p",
        "Don't count on a safe turn.$",
    ),
    "PetalburgCity_Gym_Text_GeorgePostBadge": (
        "I still want to lead a GYM one\\n",
        "day.\\p",
        "For now, I learn from each loss.$",
    ),
    "PetalburgCity_Gym_Text_BerkeIntro": (
        "TRAINER: CRITICAL ROOM.\\p",
        "I won't hold back because you're\\n",
        "ELIAS's child.\\p",
        "A critical hit tests composure.$",
    ),
    "PetalburgCity_Gym_Text_BerkeDefeat": (
        "You stayed steady. I didn't.$",
    ),
    "PetalburgCity_Gym_Text_BerkePostBattle": (
        "ELIAS is strong.\\p",
        "But your choices are not his.\\p",
        "Go show him that.$",
    ),
    "PetalburgCity_Gym_Text_BerkePostBadge": (
        "PAMPA DA ESPERA grew tougher\\n",
        "under ELIAS.\\p",
        "Now we know his child can push us\\n",
        "too.$",
    ),
    "PetalburgCity_Gym_Text_MaryIntro": (
        "TRAINER: ACCURACY ROOM.\\p",
        "When every hit lands, excuses\\n",
        "vanish quickly.$",
    ),
    "PetalburgCity_Gym_Text_MaryDefeat": (
        "You were sharper than I was.$",
    ),
    "PetalburgCity_Gym_Text_MaryPostBattle": (
        "Left: DEFENSE ROOM.\\p",
        "Right: RECOVERY ROOM.\\p",
        "Either path tests how long your\\n",
        "plan survives.$",
    ),
    "PetalburgCity_Gym_Text_MaryPostBadge": (
        "We train for more than perfect\\n",
        "moves.\\p",
        "A BOND is attention, not luck.$",
    ),
    "PetalburgCity_Gym_Text_AlexiaIntro": (
        "TRAINER: DEFENSE ROOM.\\p",
        "Strong defenses let me take risks.\\p",
        "Let's see if yours do too.$",
    ),
    "PetalburgCity_Gym_Text_AlexiaDefeat": (
        "Your defense held. Mine didn't.$",
    ),
    "PetalburgCity_Gym_Text_AlexiaPostBattle": (
        "Left: POWER ROOM.\\p",
        "Right: CRITICAL ROOM.\\p",
        "Both paths punish hesitation.$",
    ),
    "PetalburgCity_Gym_Text_AlexiaPostBadge": (
        "Tried SURF yet?\\p",
        "That COMPASS BADGE opens more\\n",
        "than this GYM.$",
    ),
    "PetalburgCity_Gym_Text_JodyIntro": (
        "TRAINER: POWER ROOM.\\p",
        "ELIAS told us to go all out.\\p",
        "Your family name changes nothing.$",
    ),
    "PetalburgCity_Gym_Text_JodyDefeat": (
        "I went all out. You answered.$",
    ),
    "PetalburgCity_Gym_Text_JodyPostBattle": (
        "Your style echoes ELIAS.\\p",
        "But it isn't a copy.\\p",
        "He's waiting ahead.$",
    ),
    "PetalburgCity_Gym_Text_JodyPostBadge": (
        "Strength matters.\\p",
        "So does why a TRAINER asks a\\n",
        "POKéMON to use it.$",
    ),
    "PetalburgCity_Gym_Text_DoorAppearsLocked": (
        "The door is locked for now.$",
    ),
    "PetalburgCity_Gym_Text_DoorAppearsLocked2": (
        "The door is locked for now.$",
    ),
    "PetalburgCity_Gym_Text_EnterSpeedRoom": (
        "SPEED ROOM\\p",
        "Enter?$",
    ),
    "PetalburgCity_Gym_Text_EnterAccuracyRoom": (
        "ACCURACY ROOM\\p",
        "Enter?$",
    ),
    "PetalburgCity_Gym_Text_EnterConfusionRoom": (
        "CONFUSION ROOM\\p",
        "Enter?$",
    ),
    "PetalburgCity_Gym_Text_EnterDefenseRoom": (
        "DEFENSE ROOM\\p",
        "Enter?$",
    ),
    "PetalburgCity_Gym_Text_EnterRecoveryRoom": (
        "RECOVERY ROOM\\p",
        "Enter?$",
    ),
    "PetalburgCity_Gym_Text_EnterStrengthRoom": (
        "POWER ROOM\\p",
        "Enter?$",
    ),
    "PetalburgCity_Gym_Text_EnterOHKORoom": (
        "CRITICAL ROOM\\p",
        "Enter?$",
    ),
    "PetalburgCity_Gym_Text_EnterGymLeadersRoom": (
        "GYM LEADER'S ROOM\\p",
        "ELIAS waits beyond this door.\\p",
        "Enter?$",
    ),
}

SOURCE_MARKERS = (
    "ROOM", "TRAINER", "LEADER", "PETALBURG CITY", "SURF", "door",
    "advantage", "bond", "critical hit", "restore HP", "soul mates",
    "POKéMON", "sign says",
)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^(?:@[^\n]*\n)*[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload.replace("$", ""))
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, payloads in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render(source: str) -> str:
    validate_widths()
    rendered = source
    for label, payloads in TARGETS.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{label}: target contains no .string payload")
        if not any(marker in body for marker in SOURCE_MARKERS):
            raise ValueError(f"{label}: source no longer resembles known gym-room surface")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(text: str) -> str:
    masked = text
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing gym-room block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_GYM_ROOM_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask_targets(source) != mask_targets(rendered):
        raise ValueError("non-dialogue Pampa gym-room structure changed")

    forbidden = (
        "PETALBURG CITY", "ONE-HIT KO ROOM", "STRENGTH ROOM",
        "soul mates", "our LEADER's kid", "your father really",
    )
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: stale gym-room token survived: {token}")

    preserved = (
        "TRAINER_RANDALL",
        "TRAINER_PARKER",
        "TRAINER_GEORGE",
        "TRAINER_BERKE",
        "TRAINER_MARY",
        "TRAINER_ALEXIA",
        "TRAINER_JODY",
        "PetalburgGymSlideOpenRoomDoors",
        "PetalburgGymUnlockRoomDoors",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved gym-room gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Pampa da Espera Gym room trainers and door prompts in English without changing room mechanics."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TARGET.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.check:
        print(f"Pampa gym-room renderer OK: {len(TARGETS)} text blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

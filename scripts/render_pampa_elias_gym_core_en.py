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
    "PetalburgCity_Gym_Text_DadYoureHereWithYourPokemon": (
        "ELIAS: {PLAYER}. You made it.\\p",
        "And you're traveling with a\\n",
        "POKéMON already.\\p",
        "I'm glad. More than I expected\\n",
        "to be.$",
    ),
    "PetalburgCity_Gym_Text_WallyIdLikeAPokemon": (
        "VAL: ELIAS...\\p",
        "I want to travel too.\\p",
        "But I don't want to go alone.$",
    ),
    "PetalburgCity_Gym_Text_DadOhYoureWallyRight": (
        "ELIAS: You're VAL, right?\\p",
        "Your family said you might come.$",
    ),
    "PetalburgCity_Gym_Text_WallyIveNeverCaughtAPokemon": (
        "VAL: I've never caught a POKéMON\\n",
        "by myself.\\p",
        "Could someone show me?$",
    ),
    "PetalburgCity_Gym_Text_DadHmISee": (
        "ELIAS: I understand.$",
    ),
    "PetalburgCity_Gym_Text_DadPlayerGoWithWally": (
        "ELIAS: {PLAYER}, go with VAL.\\p",
        "Don't do it for him.\\p",
        "Just stay close while he tries.$",
    ),
    "PetalburgCity_Gym_Text_IllLoanYouMyZigzagoon": (
        "ELIAS: VAL, borrow my POKéMON.\\p",
        "VAL received a ZIGZAGOON!$",
    ),
    "PetalburgCity_Gym_Text_WallyThankYouAndDadGivesPokeBall": (
        "VAL: Really? Thank you!\\p",
        "ELIAS: You'll need this too.\\p",
        "VAL received a POKé BALL!$",
    ),
    "PetalburgCity_Gym_Text_WallyOhWowThankYou": (
        "VAL: Thank you, ELIAS!$",
    ),
    "PetalburgCity_Gym_Text_WouldYouReallyComeWithMe": (
        "VAL: {PLAYER}...\\p",
        "You'll really come with me?$",
    ),
    "PetalburgCity_Gym_Text_DadSoDidItWorkOut": (
        "ELIAS: So? How did it go?$",
    ),
    "PetalburgCity_Gym_Text_WallyThankYouBye": (
        "VAL: I caught one myself.\\p",
        "I was scared, but I did it.\\p",
        "Thank you, {PLAYER}.\\n",
        "I'll return ZIGZAGOON now.$",
    ),
    "PetalburgCity_Gym_Text_DadGoCollectBadges": (
        "ELIAS: Now, {PLAYER}...\\p",
        "If you're serious about this,\\n",
        "travel and earn BADGES.\\p",
        "Start with the GYM in\\n",
        "SERRA DO UIVO.\\p",
        "Come back when you have grown.\\p",
        "Then we'll battle.$",
    ),
    "PetalburgCity_Gym_Text_NormanGoToRustboro": (
        "ELIAS: SERRA DO UIVO first.\\p",
        "Learn how other LEADERS test\\n",
        "their TRAINERS.$",
    ),
    "PetalburgCity_Gym_Text_NormanGoToDewford": (
        "ELIAS: Keep moving.\\p",
        "PORTO DAS REDES is another place\\n",
        "worth learning from.$",
    ),
    "PetalburgCity_Gym_Text_YouHaveGottenStronger": (
        "ELIAS: You've changed, {PLAYER}.\\p",
        "The BADGES show experience.\\p",
        "Your POKéMON show something more.$",
    ),
    "PetalburgCity_Gym_Text_NormanIntro": (
        "ELIAS: I kept something from you.\\p",
        "I approved part of the M'BOI\\n",
        "project.\\p",
        "For years I called my fear\\n",
        "prudence.\\p",
        "Today I'm your GYM LEADER.\\p",
        "After this, ask me again.$",
    ),
    "PetalburgCity_Gym_Text_NormanDefeat": (
        "ELIAS: You surpassed me.\\p",
        "I can't hide behind being your\\n",
        "father forever.$",
    ),
    "PetalburgCity_Gym_Text_ReceivedBalanceBadge": (
        "{PLAYER} received the\\n",
        "COMPASS BADGE!$",
    ),
    "PetalburgCity_Gym_Text_ExplainBalanceBadgeTakeThis": (
        "ELIAS: The COMPASS BADGE raises\\n",
        "your POKéMON's DEFENSE.\\p",
        "It also lets you use SURF\\n",
        "outside battle.\\p",
        "And take this, {PLAYER}.$",
    ),
    "PetalburgCity_Gym_Text_ExplainFacade": (
        "ELIAS: TM42 contains FACADE.\\p",
        "Its power doubles if the user\\n",
        "is poisoned, paralyzed or burned.\\p",
        "A bad state can become leverage.$",
    ),
    "PetalburgCity_Gym_Text_DadHappyAndSad": (
        "ELIAS: As LEADER, losing hurts.\\p",
        "As your father... I'm proud.\\p",
        "Those feelings can exist together.$",
    ),
    "PetalburgCity_Gym_Text_PleaseComeWithMe": (
        "MAN: {PLAYER}, there you are!\\p",
        "Please come with me.\\p",
        "I have something for you.$",
    ),
    "PetalburgCity_Gym_Text_LetMeBorrowPlayer": (
        "MAN: ELIAS, may I borrow\\n",
        "{PLAYER} for a moment?$",
    ),
    "PetalburgCity_Gym_Text_DadGoingToKeepTraining": (
        "ELIAS: Go see your mother too.\\p",
        "I'll stay here and train.\\p",
        "And when you're ready, we'll\\n",
        "speak about M'BOI.$",
    ),
    "PetalburgCity_Gym_Text_DadNoAmountOfTrainingIsEnough": (
        "ELIAS: Training never really ends.\\p",
        "Neither does learning how to\\n",
        "live with what we remember.$",
    ),
    "PetalburgCity_Gym_Text_GymGuideAdvice": (
        "GUIDE: This GYM uses seven rooms.\\p",
        "Each TRAINER tests a different\\n",
        "battle habit.\\p",
        "Win and the next doors open.\\p",
        "Choose your path carefully.$",
    ),
    "PetalburgCity_Gym_Text_GymGuidePostVictory": (
        "GUIDE: You defeated ELIAS.\\p",
        "Not as his child.\\p",
        "As a TRAINER.$",
    ),
    "PetalburgCity_Gym_Text_GymStatue": (
        "PAMPA DA ESPERA POKéMON GYM$",
    ),
    "PetalburgCity_Gym_Text_GymStatueCertified": (
        "PAMPA DA ESPERA POKéMON GYM\\p",
        "ELIAS'S CERTIFIED TRAINERS:\\n",
        "{PLAYER}$",
    ),
    "PetalburgCity_Gym_Text_NormanPreRematch": (
        "ELIAS: Being your father never\\n",
        "gave me the right to choose\\n",
        "which truths you could bear.\\p",
        "I understood that too late.$",
    ),
    "PetalburgCity_Gym_Text_NormanRematchDefeat": (
        "ELIAS: You keep forcing me to\\n",
        "stop hiding behind old answers.$",
    ),
    "PetalburgCity_Gym_Text_NormanPostRematch": (
        "ELIAS: I can't undo M'BOI.\\p",
        "I can stop calling silence\\n",
        "protection.$",
    ),
    "PetalburgCity_Gym_Text_NormanRematchNeedTwoMons": (
        "ELIAS: Some guilt does not fade\\n",
        "because we stay silent.\\p",
        "I approved part of M'BOI.\\p",
        "I spent years calling fear\\n",
        "prudence.$",
    ),
}

SOURCE_MARKERS = (
    "DAD:", "VAL:", "ELIAS:", "WALLY", "PETALBURG CITY", "NORMAN",
    "INSÍGNIA", "{PLAYER}", "GYM", "TRAINER", "BADGES",
)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^(?:@[^\n]*\n)*[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    cleaned = cleaned.replace("{PLAYER}", "PLAYERX")
    cleaned = cleaned.replace("{KUN}", "")
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
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
            raise ValueError(f"{label}: source no longer resembles known Petalburg Gym surface")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(text: str) -> str:
    masked = text
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing Elias gym block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_ELIAS_GYM_EN>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask_targets(source) != mask_targets(rendered):
        raise ValueError("non-dialogue Elias gym structure changed")

    forbidden = (
        "DAD:", "WALLY", "NORMAN", "PETALBURG CITY", "INSÍGNIA",
        "recebeu", "Algumas culpas", "Ser seu pai", "voce ", "nao ",
    )
    for label in TARGETS:
        body = block_pattern(label).search(rendered).group("body")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: stale Elias-gym visible token survived: {token}")

    preserved = (
        "TRAINER_NORMAN_1",
        "FLAG_BADGE05_GET",
        "FLAG_DEFEATED_PETALBURG_GYM",
        "VAR_PETALBURG_GYM_STATE",
        "ITEM_TM42",
        "FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_RIVAL",
        "special InitBirchState",
        "MAP_PETALBURG_CITY_WALLYS_HOUSE",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved Elias-gym gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Elias/Val story core of Pampa da Espera Gym in English without changing inherited event wiring."
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
        print(f"Pampa Elias gym core renderer OK: {len(TARGETS)} text blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

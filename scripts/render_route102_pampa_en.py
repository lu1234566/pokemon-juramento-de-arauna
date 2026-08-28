#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "data" / "maps" / "Route102" / "scripts.inc"
CITY = ROOT / "data" / "maps" / "PetalburgCity" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

ROUTE_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "Route102_Text_WatchMeCatchPokemon": (("WALLY:", "catch one properly"), (
        "VAL: {PLAYER}...\\p",
        "Could you watch me try this?\\p",
        "I'm still nervous.\\p",
        "I want to catch one myself.\\n",
        "Here goes!$",
    )),
    "Route102_Text_WallyIDidIt": (("VAL:", "proprio ritmo"), (
        "VAL: I did it!\\p",
        "I was scared the whole time.\\p",
        "But I still did it.\\p",
        "Maybe that's enough for today.$",
    )),
    "Route102_Text_LetsGoBack": (("thank you", "GYM"), (
        "VAL: Thank you, {PLAYER}.\\p",
        "Let's go back to ELIAS.$",
    )),
    "Route102_Text_ImNotVeryTall": (("not very tall", "Fwatchoo"), (
        "I'm short enough that tall grass\\n",
        "gets right in my face.\\p",
        "It makes me sneeze every time!$",
    )),
    "Route102_Text_CatchWholeBunchOfPokemon": (("whole bunch", "POKéMON"), (
        "I'm going to catch lots of\\n",
        "POKéMON and learn their habits.$",
    )),
    "Route102_Text_RouteSignOldale": (("ROUTE 102", "OLDALE TOWN"), (
        "ROUTE 102\\n",
        "{RIGHT_ARROW} VILA DA PASSAGEM$",
    )),
    "Route102_Text_RouteSignPetalburg": (("ROUTE 102", "PETALBURG CITY"), (
        "ROUTE 102\\n",
        "{LEFT_ARROW} PAMPA DA ESPERA$",
    )),
}

CITY_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "PetalburgCity_Text_WhereIsWally": (("VAL:", "proprio ritmo"), (
        "WOMAN: Have you seen VAL?\\p",
        "He went to speak with ELIAS.\\p",
        "He wants to travel, but crowds\\n",
        "still make him nervous.$",
    )),
    "PetalburgCity_Text_AreYouRookieTrainer": (("rookie TRAINER", "GYM"), (
        "BOY: New TRAINER?\\p",
        "When I reach a new town, I check\\n",
        "the local GYM first.\\p",
        "Want me to show you?$",
    )),
    "PetalburgCity_Text_ThisIsPetalburgGym": (("PETALBURG CITY", "GYM"), (
        "BOY: This is PAMPA DA ESPERA\\n",
        "GYM.$",
    )),
    "PetalburgCity_Text_ThisIsGymSign": (("GYM's sign", "looking for a GYM"), (
        "BOY: Every GYM has a sign like\\n",
        "this.\\p",
        "It tells you who leads it.$",
    )),
    "PetalburgCity_Text_WaterReflection": (("reflected in the water", "What do you see"), (
        "The water changes every time\\n",
        "the wind crosses it.\\p",
        "Still, people keep looking for\\n",
        "themselves in the reflection.$",
    )),
    "PetalburgCity_Text_FullPartyExplanation": (("six POKéMON", "STORAGE"), (
        "A party can hold six POKéMON.\\p",
        "If you catch another, it goes\\n",
        "to a PC STORAGE BOX.$",
    )),
    "PetalburgCity_Text_GymSign": (("PAMPA DA ESPERA", "ELIAS"), (
        "PAMPA DA ESPERA GYM\\n",
        "LEADER: ELIAS\\p",
        "Returning doesn't erase\\n",
        "the road.$",
    )),
    "PetalburgCity_Text_CitySign": (("PAMPA DA ESPERA", "M'BOI"), (
        "PAMPA DA ESPERA\\p",
        "A town shaped by departures\\n",
        "and returns.\\p",
        "ELIAS rarely speaks of M'BOI.$",
    )),
    "PetalburgCity_Text_WallyHouseSign": (("VAL:", "coragem"), (
        "VAL'S HOUSE$",
    )),
    "PetalburgCity_Text_AreYouATrainer": (("POKéMON TRAINER", "dressed"), (
        "SEU BENTO: Hm. New TRAINER?\\p",
        "You still look like the road\\n",
        "hasn't tested you much.$",
    )),
    "PetalburgCity_Text_WellMaybeNot": (("maybe not", "ordinary kid"), (
        "SEU BENTO: That's not an insult.\\p",
        "Everyone starts before they know\\n",
        "what kind of traveler they are.$",
    )),
    "PetalburgCity_Text_ImLookingForTalentedTrainers": (("talented TRAINERS", "taken your time"), (
        "SEU BENTO: I travel and watch\\n",
        "how TRAINERS treat their BONDS.\\p",
        "We'll meet again, {PLAYER}.$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    cleaned = cleaned.replace("{PLAYER}", "PLAYERX")
    cleaned = cleaned.replace("{RIGHT_ARROW}", ">")
    cleaned = cleaned.replace("{LEFT_ARROW}", "<")
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    for label, (_, payloads) in targets.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render(source: str, targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]], scope: str) -> str:
    validate_widths(targets)
    rendered = source
    for label, (markers, payloads) in targets.items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{scope}: {label}: expected one text block, found {len(matches)}")
        body = matches[0].group("body")
        if ".string" not in body:
            raise ValueError(f"{scope}: {label}: target contains no .string payload")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{scope}: {label}: source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(text: str, targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]], token: str) -> str:
    masked = text
    for label in targets:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"cannot mask missing block: {label}")
        start, end = match.span("body")
        masked = masked[:start] + f'\t.string "<{token}>"\n\n' + masked[end:]
    return masked


def validate_rendered(route_source: str, route: str, city_source: str, city: str) -> None:
    if mask_targets(route_source, ROUTE_TARGETS, "ARAUNA_ROUTE102_EN") != mask_targets(route, ROUTE_TARGETS, "ARAUNA_ROUTE102_EN"):
        raise ValueError("non-dialogue Route 102 structure changed")
    if mask_targets(city_source, CITY_TARGETS, "ARAUNA_PAMPA_EN") != mask_targets(city, CITY_TARGETS, "ARAUNA_PAMPA_EN"):
        raise ValueError("non-dialogue Pampa da Espera structure changed")

    route_forbidden = ("WALLY:", "OLDALE TOWN", "PETALBURG CITY", "proprio ritmo")
    city_forbidden = ("PETALBURG CITY", "VAL: Passei", "RESPONSAVEL", "Voltar nao", "talented TRAINERS")
    for label in ROUTE_TARGETS:
        body = block_pattern(label).search(route).group("body")
        for token in route_forbidden:
            if token in body:
                raise ValueError(f"{label}: stale Route 102 token survived: {token}")
    for label in CITY_TARGETS:
        body = block_pattern(label).search(city).group("body")
        for token in city_forbidden:
            if token in body:
                raise ValueError(f"{label}: stale Pampa token survived: {token}")

    route_preserved = (
        "TRAINER_CALVIN_1",
        "TRAINER_RICK",
        "TRAINER_TIANA",
        "TRAINER_ALLEN",
    )
    city_preserved = (
        "special SavePlayerParty",
        "special LoadWallyZigzagoon",
        "special StartWallyTutorialBattle",
        "special LoadPlayerParty",
        "VAR_PETALBURG_CITY_STATE",
        "VAR_PETALBURG_GYM_STATE",
        "VAR_SCOTT_STATE",
        "VAR_SCOTT_PETALBURG_ENCOUNTER",
    )
    for token in route_preserved:
        if token not in route:
            raise ValueError(f"preserved Route 102 gameplay token missing: {token}")
    for token in city_preserved:
        if token not in city:
            raise ValueError(f"preserved Pampa gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Route 102 and Pampa da Espera exterior surfaces in English without changing Emerald event wiring."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    route_source = ROUTE.read_text(encoding="utf-8")
    city_source = CITY.read_text(encoding="utf-8")
    route = render(route_source, ROUTE_TARGETS, "Route 102")
    city = render(city_source, CITY_TARGETS, "Pampa da Espera")
    validate_rendered(route_source, route, city_source, city)

    if args.check:
        print(
            "Route 102 / Pampa da Espera English renderer OK: "
            f"{len(ROUTE_TARGETS)} route blocks + {len(CITY_TARGETS)} city blocks validated."
        )
        return 0
    if args.in_place:
        ROUTE.write_text(route, encoding="utf-8")
        CITY.write_text(city, encoding="utf-8")
        return 0

    print(route, end="" if route.endswith("\n") else "\n")
    print(city, end="" if city.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

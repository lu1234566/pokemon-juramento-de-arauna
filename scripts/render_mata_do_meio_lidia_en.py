#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITY = ROOT / "data" / "maps" / "FortreeCity" / "scripts.inc"
GYM = ROOT / "data" / "maps" / "FortreeCity_Gym" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32

CITY_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "FortreeCity_Text_SawGiganticPokemonInSky": (
        ("gigantic POKéMON", "ROUTE 131"),
        (
            "Homes here grow with the trees.\\p",
            "We follow branches, not roads.\\p",
            "When a familiar route changes,\\n",
            "everyone notices.$",
        ),
    ),
    "FortreeCity_Text_SomethingBlockingGym": (
        ("POKéMON GYM", "ROUTE 120"),
        (
            "Something is blocking the GYM.\\p",
            "I trained for LIDIA's challenge,\\n",
            "but I can't reach the entrance.$",
        ),
    ),
    "FortreeCity_Text_ThisTimeIllBeatWinona": (
        ("LIDIA", "esquecem caminhos"),
        (
            "LIDIA says to watch what\\n",
            "POKéMON remember on their own.\\p",
            "Lost paths still leave clues.$",
        ),
    ),
    "FortreeCity_Text_TreesGrowByDrinkingRainwater": (
        ("sensores registram", "correntes antigas"),
        (
            "Rain feeds every layer here.\\p",
            "So do calls passed by birds.\\p",
            "Some routes are older than any\\n",
            "house in the canopy.$",
        ),
    ),
    "FortreeCity_Text_EveryoneHealthyAndLively": (
        ("CITY consists", "thirty years"),
        (
            "We live high, but not apart.\\p",
            "Every bridge is shared work.\\p",
            "If one path fails, we build\\n",
            "another together.$",
        ),
    ),
    "FortreeCity_Text_BugPokemonComeThroughWindow": (
        ("Meu POKéMON", "HORIZONTE"),
        (
            "My POKéMON knew these branches\\n",
            "before I did.\\p",
            "Today it froze when I called.\\p",
            "CIRO saw it too.\\p",
            "He stared at his HORIZON device.$",
        ),
    ),
    "FortreeCity_Text_PokemonThatEvolveWhenTraded": (
        ("evolve when", "trade them"),
        (
            "Some POKéMON change when traded.\\p",
            "Others inherit stranger things.\\p",
            "LIDIA says both can teach us.$",
        ),
    ),
    "FortreeCity_Text_SomethingUnseeable": (
        ("Something unseeable",),
        ("Something unseen blocks the way.$",),
    ),
    "FortreeCity_Text_UnseeableUseDevonScope": (
        ("DEVON SCOPE",),
        (
            "Something unseen blocks the way.\\p",
            "Use the FIELD SCOPE?$",
        ),
    ),
    "FortreeCity_Text_UsedDevonScopePokemonFled": (
        ("used the DEVON SCOPE",),
        (
            "{PLAYER} used the FIELD SCOPE.\\p",
            "An unseen POKéMON appeared!\\p",
            "It fled into the canopy.$",
        ),
    ),
    "FortreeCity_Text_CitySign": (
        ("MATA DO MEIO", "Pokemon selvagens"),
        (
            "MATA DO MEIO\\p",
            "Wild POKéMON pass routes, calls\\n",
            "and habits across generations.$",
        ),
    ),
    "FortreeCity_Text_GymSign": (
        ("RESPONSAVEL: LIDIA",),
        (
            "MATA DO MEIO POKéMON GYM\\n",
            "LEADER: LIDIA\\p",
            "Listen before you climb.$",
        ),
    ),
}

GYM_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "FortreeCity_Gym_Text_GymGuideAdvice": (
        ("MATA DO MEIO GYM LEADER WINONA",),
        (
            "Welcome to LIDIA's challenge!\\p",
            "FLYING POKéMON read wind well.\\p",
            "Here, you must read the path.\\p",
            "The rotating gates punish\\n",
            "rushing more than weakness.$",
        ),
    ),
    "FortreeCity_Gym_Text_GymGuidePostVictory": (
        ("achieved liftoff",),
        ("You did it!\\p", "You heard the whole pattern.$"),
    ),
    "FortreeCity_Gym_Text_JaredIntro": (
        ("BIRD POKéMON",),
        ("Wind changes without warning.\\p", "So should a good TRAINER.$"),
    ),
    "FortreeCity_Gym_Text_JaredDefeat": (
        ("You're strong",),
        ("You changed direction fast.$",),
    ),
    "FortreeCity_Gym_Text_JaredPostBattle": (
        ("unexpected turns", "LEADER"),
        ("Every turn tests attention.\\p", "Do not rush the next gate.$"),
    ),
    "FortreeCity_Gym_Text_EdwardoIntro": (
        ("BIRD POKéMON", "MATA DO MEIO GYM"),
        (
            "Birds inherit routes in the sky.\\p",
            "We train to notice when they\\n",
            "change.$",
        ),
    ),
    "FortreeCity_Gym_Text_EdwardoDefeat": (
        ("too much of a load",),
        ("I missed the change.$",),
    ),
    "FortreeCity_Gym_Text_EdwardoPostBattle": (
        ("world is huge", "tough TRAINERS"),
        ("A familiar route can still fail.\\p", "Adapt without erasing it.$"),
    ),
    "FortreeCity_Gym_Text_FlintIntro": (
        ("WINONA", "LEADER,"),
        ("LIDIA taught us to watch first.\\p", "Then decide what a change means.$"),
    ),
    "FortreeCity_Gym_Text_FlintDefeat": (
        ("WINONA", "I lost"),
        ("LIDIA... I lost.$",),
    ),
    "FortreeCity_Gym_Text_FlintPostBattle": (
        ("WINONA is cute",),
        ("LIDIA never guesses too early.\\p", "That's harder than it sounds.$"),
    ),
    "FortreeCity_Gym_Text_AshleyIntro": (
        ("WINONA taught me",),
        ("LIDIA taught me personally.\\p", "I won't waste that lesson.$"),
    ),
    "FortreeCity_Gym_Text_AshleyDefeat": (
        ("I was beaten",),
        ("You found the opening.$",),
    ),
    "FortreeCity_Gym_Text_AshleyPostBattle": (
        ("WINONA", "MATA DO MEIO"),
        ("MATA DO MEIO trusts LIDIA\\n", "because she listens first.$"),
    ),
    "FortreeCity_Gym_Text_HumbertoIntro": (
        ("WINONA takes to battle",),
        ("Balance matters more than speed.\\p", "Reach LIDIA and prove it.$"),
    ),
    "FortreeCity_Gym_Text_HumbertoDefeat": (
        ("couldn't stop you",),
        ("I couldn't hold the line.$",),
    ),
    "FortreeCity_Gym_Text_HumbertoPostBattle": (
        ("staring at WINONA",),
        ("Watch the gates, not the height.\\p", "The floor teaches too.$"),
    ),
    "FortreeCity_Gym_Text_DariusIntro": (
        ("FLYING-type POKéMON",),
        ("No two FLYING POKéMON read\\n", "the same wind.$"),
    ),
    "FortreeCity_Gym_Text_DariusDefeat": (
        ("know your stuff",),
        ("You read that well.$",),
    ),
    "FortreeCity_Gym_Text_DariusPostBattle": (
        ("WINONA's POKéMON",),
        ("LIDIA watches how you adapt.\\p", "She notices hesitation.$"),
    ),
    "FortreeCity_Gym_Text_WinonaIntro": (
        ("LIDIA", "esquecem caminhos"),
        (
            "LIDIA: Paths can be inherited.\\p",
            "So can songs, fear and trust.\\p",
            "Something is breaking the chain.\\p",
            "Show me what your POKéMON kept.$",
        ),
    ),
    "FortreeCity_Gym_Text_WinonaDefeat": (
        ("LIDIA", "esquecem caminhos"),
        ("LIDIA: You listened to them.\\p", "That's why they trusted you.$"),
    ),
    "FortreeCity_Gym_Text_ReceivedFeatherBadge": (
        ("INSÍGNIA PLUMA", "LIDIA"),
        ("{PLAYER} received the\\n", "PLUME BADGE from LIDIA!$"),
    ),
    "FortreeCity_Gym_Text_ExplainFeatherBadgeTakeThis": (
        ("INSÍGNIA PLUMA", "nível 70"),
        (
            "With the PLUME BADGE, POKéMON\\n",
            "up to Lv. 70 will obey you,\\n",
            "even those received in trades.\\p",
            "It also lets you use FLY\\n",
            "outside battle.\\p",
            "Take this TM as well.$",
        ),
    ),
    "FortreeCity_Gym_Text_ExplainAerialAce": (
        ("AERIAL ACE", "No POKéMON"),
        ("TM40 contains AERIAL ACE.\\p", "It strikes before foes can move.$"),
    ),
    "FortreeCity_Gym_Text_RegisteredWinona": (
        ("GYM LEADER WINONA", "POKéNAV"),
        ("Registered GYM LEADER LIDIA\\n", "in the POKéNAV.$"),
    ),
    "FortreeCity_Gym_Text_WinonaPostBattle": (
        ("LIDIA", "esquecem caminhos"),
        ("LIDIA: A path is not a command.\\p", "Memory should guide, not own us.$"),
    ),
    "FortreeCity_Gym_Text_GymStatue": (
        ("MATA DO MEIO POKéMON GYM",),
        ("MATA DO MEIO POKéMON GYM$",),
    ),
    "FortreeCity_Gym_Text_GymStatueCertified": (
        ("MATA DO MEIO POKéMON GYM", "WINONA'S CERTIFIED TRAINERS"),
        (
            "MATA DO MEIO POKéMON GYM\\p",
            "LIDIA'S CERTIFIED TRAINERS:\\n",
            "{PLAYER}$",
        ),
    ),
    "FortreeCity_Gym_Text_WinonaPreRematch": (
        ("LIDIA", "esquecem caminhos"),
        ("LIDIA: The canopy changed again.\\p", "Let's see what we carried on.$"),
    ),
    "FortreeCity_Gym_Text_WinonaRematchDefeat": (
        ("LIDIA", "esquecem caminhos"),
        ("LIDIA: You changed without\\n", "erasing what came before.$"),
    ),
    "FortreeCity_Gym_Text_WinonaPostRematch": (
        ("LIDIA", "esquecem caminhos"),
        ("LIDIA: Good. Keep listening.$",),
    ),
    "FortreeCity_Gym_Text_WinonaRematchNeedTwoMons": (
        ("LIDIA", "esquecem caminhos"),
        ("LIDIA: Bring two POKéMON\\n", "before we begin again.$"),
    ),
}

BLOCK_RE_TEMPLATE = r'(?m)^{label}:\n(?P<body>(?:\t\.string "[^\n]*"\n)+)'
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    for label, (_, payloads) in targets.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render(source: str, targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> str:
    rendered = source
    for label, (markers, payloads) in targets.items():
        pattern = re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one .string block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{label}: expected source marker not found: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def validate_rendered(rendered: str, targets: dict[str, tuple[tuple[str, ...], tuple[str, ...]]]) -> None:
    forbidden = (
        "WINONA",
        "FORTREE",
        "DEVON SCOPE",
        "RESPONSAVEL",
        "INSÍGNIA",
        "Quando os POKéMON",
        "Meu POKéMON",
        "sensores registram",
    )
    for label, (_, payloads) in targets.items():
        pattern = re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))
        match = pattern.search(rendered)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: legacy/Portuguese visible token survived: {token}")


def validate_gameplay(city: str, gym: str) -> None:
    required_city = (
        "checkitem ITEM_DEVON_SCOPE",
        "SPECIES_KECLEON",
        "FLAG_KECLEON_FLED_FORTREE",
    )
    required_gym = (
        "TRAINER_WINONA_1",
        "FLAG_DEFEATED_FORTREE_GYM",
        "FLAG_BADGE06_GET",
        "ITEM_TM_AERIAL_ACE",
        "FLAG_RECEIVED_TM_AERIAL_ACE",
        "FLAG_ENABLE_WINONA_MATCH_CALL",
        "FLAG_SCOTT_CALL_FORTREE_GYM",
        "RotatingGate_InitPuzzle",
    )
    for token in required_city:
        if token not in city:
            raise ValueError(f"preserved Mata do Meio city token missing: {token}")
    for token in required_gym:
        if token not in gym:
            raise ValueError(f"preserved Lidia gym token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Mata do Meio city and Lidia's gym in English without changing Emerald gameplay wiring."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    validate_widths(CITY_TARGETS)
    validate_widths(GYM_TARGETS)
    city_source = CITY.read_text(encoding="utf-8")
    gym_source = GYM.read_text(encoding="utf-8")
    city_rendered = render(city_source, CITY_TARGETS)
    gym_rendered = render(gym_source, GYM_TARGETS)
    validate_rendered(city_rendered, CITY_TARGETS)
    validate_rendered(gym_rendered, GYM_TARGETS)
    validate_gameplay(city_rendered, gym_rendered)

    if args.check:
        total = len(CITY_TARGETS) + len(GYM_TARGETS)
        print(f"Mata do Meio / Lidia English renderer OK: {total} text blocks validated.")
        return 0
    if args.in_place:
        CITY.write_text(city_rendered, encoding="utf-8")
        GYM.write_text(gym_rendered, encoding="utf-8")
        return 0

    print(city_rendered)
    print(gym_rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOWN = ROOT / "data" / "maps" / "LittlerootTown" / "scripts.inc"
ROUTE = ROOT / "data" / "maps" / "Route101" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TOWN_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "LittlerootTown_Text_OurNewHomeLetsGoInside": (("VILA AMANHECER", "MAE:"), (
        "MOM: {PLAYER}, we're here.\\p",
        "This is VILA AMANHECER.\\p",
        "Our new home is right there.\\p",
        "It may take time to feel ours.\\p",
        "Come see your room.$",
    )),
    "LittlerootTown_Text_WaitPlayer": (("MAE:",), (
        "MOM: Wait, {PLAYER}!$",
    )),
    "LittlerootTown_Text_WearTheseRunningShoes": (("ANAHI", "TENIS DE CORRIDA"), (
        "MOM: {PLAYER}! You found ANAHI?\\p",
        "And this POKéMON...\\p",
        "So you chose to travel together.\\p",
        "ELIAS will want to hear that.\\p",
        "If you're taking the road,\\n",
        "wear these RUNNING SHOES.$",
    )),
    "LittlerootTown_Text_SwitchShoesWithRunningShoes": (("TENIS DE CORRIDA",), (
        "{PLAYER} put on the\\n",
        "RUNNING SHOES.$",
    )),
    "LittlerootTown_Text_ExplainRunningShoes": (("Botao B", "TENIS DE CORRIDA"), (
        "MOM: Hold the B Button to run\\n",
        "while wearing RUNNING SHOES.$",
    )),
    "LittlerootTown_Text_ComeHomeIfAnythingHappens": (("companheiro de viagem",), (
        "MOM: You have your own travel\\n",
        "partner now.\\p",
        "Don't carry everything alone.\\p",
        "Come home whenever you need.\\p",
        "And send news, {PLAYER}.$",
    )),
    "LittlerootTown_Text_CanUsePCToStoreItems": (("PCs guardam",), (
        "PCs can store items and\\n",
        "POKéMON data.\\p",
        "I still find it strange to trust\\n",
        "so much to a screen.$",
    )),
    "LittlerootTown_Text_BirchSpendsDaysInLab": (("PROFESSORA ANAHI",), (
        "ANAHI spends more time outdoors\\n",
        "than in her lab.\\p",
        "If it's empty, she's probably\\n",
        "following a trail.$",
    )),
    "LittlerootTown_Text_IfYouGoInGrassPokemonWillJumpOut": (("capim alto",), (
        "Hey! Don't enter the woods\\n",
        "alone.\\p",
        "Wild POKéMON hide in tall grass.$",
    )),
    "LittlerootTown_Text_DangerousIfYouDontHavePokemon": (("Sem um POKéMON",), (
        "It's dangerous out there without\\n",
        "a POKéMON beside you.$",
    )),
    "LittlerootTown_Text_CanYouGoSeeWhatsHappening": (("PROFESSORA ANAHI",), (
        "Something's happening ahead!\\p",
        "I heard PROF. ANAHI and a\\n",
        "POKéMON in the woods.\\p",
        "Can you see if she's all right?$",
    )),
    "LittlerootTown_Text_YouSavedBirch": (("PROFESSORA ANAHI",), (
        "You helped PROF. ANAHI!\\p",
        "I heard the commotion from here.\\p",
        "I'm glad you both came back.$",
    )),
    "LittlerootTown_Text_GoodLuckCatchingPokemon": (("Boa sorte",), (
        "Traveling with POKéMON now?\\p",
        "Good luck, {PLAYER}!$",
    )),
    "LittlerootTown_Text_ProfBirchsLab": (("LABORATORIO DE CAMPO",), (
        "FIELD LAB\\n",
        "PROFESSOR ANAHI.$",
    )),
    "LittlerootTown_Text_PlayersHouse": (("CASA DE {PLAYER}",), (
        "HOME OF {PLAYER}$",
    )),
    "LittlerootTown_Text_ProfBirchsHouse": (("CASA DE CIRO",), (
        "CIRO'S HOUSE$",
    )),
    "LittlerootTown_Text_BirchSomethingToShowYouAtLab": (("ANAHI:", "registros"), (
        "ANAHI: {PLAYER}, come with me.\\p",
        "I found something in the records\\n",
        "I want to show you at the lab.$",
    )),
}

ROUTE_TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "Route101_Text_HelpMe": (("H-help me",), (
        "ANAHI: H-help me!$",
    )),
    "Route101_Text_PleaseHelp": (("Please! Help", "POKé BALL"), (
        "ANAHI: You there! Please!\\p",
        "My BAG!\\n",
        "There's a POKé BALL inside!$",
    )),
    "Route101_Text_DontLeaveMe": (("Don't leave me",), (
        "ANAHI: Where are you going?!\\p",
        "Please don't leave me here!$",
    )),
    "Route101_Text_YouSavedMe": (("ANAHI:", "VINCULO"), (
        "ANAHI: Thank you.\\p",
        "That POKéMON chose you quickly.\\p",
        "Maybe I was right to trust you.\\p",
        "Come to my lab. We should talk.$",
    )),
    "Route101_Text_TakeTiredPokemonToPokeCenter": (("POKéMON CENTER", "OLDALE"), (
        "If your POKéMON get tired,\\n",
        "visit a POKéMON CENTER.\\p",
        "The nearest one is just ahead.$",
    )),
    "Route101_Text_WildPokemonInTallGrass": (("Wild POKéMON", "tall grass"), (
        "Wild POKéMON hide in tall grass.\\p",
        "To meet them, step off the road\\n",
        "and search carefully.$",
    )),
    "Route101_Text_RouteSign": (("ROUTE 101", "OLDALE TOWN"), (
        "ROUTE 101\\n",
        "{UP_ARROW} ENCRUZILHADA CENTRAL$",
    )),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    cleaned = cleaned.replace("{PLAYER}", "PLAYERX")
    cleaned = cleaned.replace("{UP_ARROW}", "^")
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
            raise ValueError(f"{scope}: {label}: target body contains no .string data")
        for marker in markers:
            if marker not in body:
                raise ValueError(f"{scope}: {label}: expected source marker missing: {marker!r}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]

    def mask(text: str) -> str:
        masked = text
        for label in targets:
            match = block_pattern(label).search(masked)
            if not match:
                raise ValueError(f"{scope}: cannot mask missing block {label}")
            start, end = match.span("body")
            masked = masked[:start] + '\t.string "<ARAUNA_EN_BLOCK>"\n\n' + masked[end:]
        return masked

    if mask(source) != mask(rendered):
        raise ValueError(f"{scope}: non-dialogue structure changed")
    return rendered


def validate_final(town: str, route: str) -> None:
    forbidden_town = (
        "MAE:", "TENIS DE CORRIDA", "LABORATORIO DE CAMPO", "CASA DE CIRO",
        "PROFESSORA ANAHI", "Boa sorte", "Nao tente", "voce",
    )
    forbidden_route = (
        "OLDALE TOWN", "Eu ajudei a criar", "VINCULO", "Na epoca",
    )
    for label in TOWN_TARGETS:
        body = block_pattern(label).search(town).group("body")
        for token in forbidden_town:
            if token in body:
                raise ValueError(f"{label}: Portuguese/legacy token survived: {token}")
    for label in ROUTE_TARGETS:
        body = block_pattern(label).search(route).group("body")
        for token in forbidden_route:
            if token in body:
                raise ValueError(f"{label}: Portuguese/legacy token survived: {token}")

    preserved = (
        "FLAG_RESCUED_BIRCH",
        "VAR_ROUTE101_STATE",
        "special ChooseStarter",
        "special HealPlayerParty",
        "MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB",
    )
    for token in preserved:
        if token not in route:
            raise ValueError(f"Route 101 gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Vila Amanhecer and Route 101 opening surfaces in English without changing Emerald event wiring."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    town_source = TOWN.read_text(encoding="utf-8")
    route_source = ROUTE.read_text(encoding="utf-8")
    town = render(town_source, TOWN_TARGETS, "Vila Amanhecer")
    route = render(route_source, ROUTE_TARGETS, "Route 101")
    validate_final(town, route)

    if args.check:
        print(
            "Vila Amanhecer / Route 101 English renderer OK: "
            f"{len(TOWN_TARGETS)} town blocks + {len(ROUTE_TARGETS)} route blocks validated."
        )
        return 0
    if args.in_place:
        TOWN.write_text(town, encoding="utf-8")
        ROUTE.write_text(route, encoding="utf-8")
        return 0

    print(town, end="" if town.endswith("\n") else "\n")
    print(route, end="" if route.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

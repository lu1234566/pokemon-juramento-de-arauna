#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "LilycoveCity" / "scripts.inc"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

TARGETS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "LilycoveCity_Text_MovedLootIntoHideoutToday": (
        ("moved more loot", "HIDEOUT"),
        (
            "HORIZON: Another equipment crate\\n",
            "went into the operations hub.\\p",
            "...I should not say that aloud.$",
        ),
    ),
    "LilycoveCity_Text_ChanceToDoBigThings": (
        ("GRUNT", "CONSORCIO HORIZONTE"),
        (
            "HORIZON: I'm junior staff.\\p",
            "I don't know every decision,\\n",
            "but the work feels important.\\p",
            "Sometimes that worries me.$",
        ),
    ),
    "LilycoveCity_Text_DontGoNearCaveInCove": (
        ("cave in the cove", "adult"),
        (
            "HORIZON: That service tunnel is\\n",
            "restricted.\\p",
            "Please use the public waterfront.$",
        ),
    ),
    "LilycoveCity_Text_IfWorldBecomesOurs": (
        ("whole wide world", "CONSORCIO HORIZONTE"),
        (
            "HORIZON: I used to think one\\n",
            "system could fix everything.\\p",
            "M'BOI made that harder to say.$",
        ),
    ),
    "LilycoveCity_Text_WailmerLeapOutOfWater": (
        ("WAILMER", "Leap out"),
        (
            "There! WAILMER!\\n",
            "Follow the signal buoy!$",
        ),
    ),
    "LilycoveCity_Text_GetLostMessingUpTraining": (
        ("messing up our training", "get lost"),
        (
            "HORIZON: Sorry. We're testing\\n",
            "a coastal signal pattern.\\p",
            "Give the WAILMER some room.$",
        ),
    ),
    "LilycoveCity_Text_ContestHallInTown": (
        ("POKéMON CONTEST HALL", "heart swells"),
        (
            "Our CONTEST HALL draws TRAINERS\\n",
            "from across Arauna.\\p",
            "The whole waterfront gets louder\\n",
            "on event days.$",
        ),
    ),
    "LilycoveCity_Text_StrangeCaveInCove": (
        ("strange cave", "edge of town"),
        (
            "Have you seen the service tunnel\\n",
            "near HORIZON's waterfront hub?\\p",
            "It used to be a natural cavern.$",
        ),
    ),
    "LilycoveCity_Text_GoingToMoveDeleterForHMs": (
        ("MOVE DELETER", "HM moves"),
        (
            "I'm changing my POKéMON's moves\\n",
            "before the next CONTEST.\\p",
            "The MOVE DELETER can help.$",
        ),
    ),
    "LilycoveCity_Text_ImFromKanto": (
        ("I came from KANTO", "ARAUNA region"),
        (
            "I came from another region.\\p",
            "Arauna's coast feels alive.\\p",
            "I wonder what POKéMON exist only\\n",
            "around these waters.$",
        ),
    ),
    "LilycoveCity_Text_TeamAquaBeenTrainingWailmer": (
        ("CONSORCIO HORIZONTE", "WAILMER"),
        (
            "SAILOR: HORIZON has WAILMER\\n",
            "following signal buoys.\\p",
            "They're blocking the cove, so\\n",
            "our boats cannot leave.$",
        ),
    ),
    "LilycoveCity_Text_SomeonePuntedTeamAquaOut": (
        ("CONSORCIO HORIZONTE", "WAILMER"),
        (
            "SAILOR: The WAILMER moved on!\\p",
            "The cove is open again, so our\\n",
            "boats can finally leave.$",
        ),
    ),
    "LilycoveCity_Text_SomeoneStoleMyPokemon": (
        ("stole my POKéMON", "CONSORCIO HORIZONTE"),
        (
            "I fell asleep to the waves...\\p",
            "When I woke, my POKéMON was gone!\\p",
            "I blamed HORIZON immediately.\\n",
            "Maybe I was too quick.$",
        ),
    ),
    "LilycoveCity_Text_MissingPokemonCameBack": (
        ("missing POKéMON", "came back"),
        (
            "My missing POKéMON came back!\\p",
            "It had wandered down the beach.\\p",
            "I owe someone an apology.$",
        ),
    ),
    "LilycoveCity_Text_ImArtDealer": (
        ("ART DEALER", "MUSEUM"),
        (
            "I'm an ART DEALER.\\p",
            "The museum here keeps paintings,\\n",
            "crafts and old coastal maps.\\p",
            "I never leave empty-handed.$",
        ),
    ),
    "LilycoveCity_Text_SeaRemainsForeverYoung": (
        ("sea remains forever young",),
        (
            "I have watched this water for\\n",
            "most of my life.\\p",
            "The coast changes. The tide still\\n",
            "returns.$",
        ),
    ),
    "LilycoveCity_Text_SixtyYearsAgoHusbandProposed": (
        ("sixty years ago", "proposed"),
        (
            "My husband proposed here sixty\\n",
            "years ago.\\p",
            "The pier changed. I remember\\n",
            "where we stood.$",
        ),
    ),
    "LilycoveCity_Text_TeamAquaRenovatedCavern": (
        ("natural formation", "CONSORCIO HORIZONTE"),
        (
            "That tunnel began as a natural\\n",
            "cavern.\\p",
            "HORIZON reinforced it for the\\n",
            "operations hub.$",
        ),
    ),
    "LilycoveCity_Text_TeamAquaLotGoneForGood": (
        ("cave in the cove", "CONSORCIO HORIZONTE"),
        (
            "The waterfront tunnel is quiet.\\p",
            "HORIZON moved most operations\\n",
            "out after the crisis.$",
        ),
    ),
    "LilycoveCity_Text_ContestHallSign": (
        ("POKéMON CONTEST HALL", "TRAINERS"),
        (
            "BAIA DAS LUZES CONTEST HALL\\p",
            "Performance, care, partnership.$",
        ),
    ),
    "LilycoveCity_Text_MotelSign": (
        ("COVE LILY MOTEL", "LILYCOVE"),
        (
            "LUZES INN\\p",
            "Rooms facing the western cove.$",
        ),
    ),
    "LilycoveCity_Text_MuseumSign": (
        ("LILYCOVE MUSEUM", "Masterpiece"),
        (
            "BAIA DAS LUZES MUSEUM\\p",
            "Art, memory and coastal history.$",
        ),
    ),
    "LilycoveCity_Text_MuseumSignPlayersExhibit": (
        ("LILYCOVE MUSEUM", "{PLAYER}"),
        (
            "BAIA DAS LUZES MUSEUM\\p",
            "{PLAYER}'s POKéMON COLLECTION\\n",
            "is now on exhibit.$",
        ),
    ),
    "LilycoveCity_Text_HarborSignUnderConstruction": (
        ("LILYCOVE CITY HARBOR", "SLATEPORT CITY"),
        (
            "BAIA DAS LUZES HARBOR\\p",
            "Passenger ferry service is\\n",
            "under final testing.$",
        ),
    ),
    "LilycoveCity_Text_HarborSign": (
        ("LILYCOVE CITY HARBOR", "S.S. TIDAL"),
        (
            "BAIA DAS LUZES HARBOR\\p",
            "Passenger ferries depart here.$",
        ),
    ),
    "LilycoveCity_Text_TrainerFanClubSign": (
        ("POKéMON TRAINER FAN CLUB", "scribbled"),
        (
            "POKéMON TRAINER FAN CLUB\\p",
            "Names and battle notes cover\\n",
            "the sign.$",
        ),
    ),
    "LilycoveCity_Text_DepartmentStoreSign": (
        ("LILYCOVE DEPARTMENT STORE", "merchandise"),
        (
            "BAIA DAS LUZES DEPT. STORE\\p",
            "Supplies from across Arauna.$",
        ),
    ),
    "LilycoveCity_Text_MoveDeletersHouseSign": (
        ("MOVE DELETER'S HOUSE", "moves deleted"),
        (
            "MOVE DELETER\\p",
            "Unwanted POKéMON moves removed.$",
        ),
    ),
    "LilycoveCity_Text_HeardTowerCalledSkyPillar": (
        ("SKY PILLAR", "sea routes"),
        (
            "I heard about a tower beyond\\n",
            "the western sea routes.\\p",
            "They call it TORRE DO JURAMENTO.$",
        ),
    ),
    "LilycoveCity_Text_SawTallTowerOnRoute131": (
        ("tall tower", "ROUTE 131"),
        (
            "I saw a tall tower far west.\\p",
            "Could that be TORRE DO JURAMENTO?$",
        ),
    ),
    "LilycoveCity_Text_JustArrivedAndSawRarePokemon": (
        ("honeymoon vacation", "DRAGON-type"),
        (
            "We just arrived for our honeymoon.\\p",
            "We saw a huge POKéMON silhouette\\n",
            "high above the sea.\\p",
            "Arauna already surprised us.$",
        ),
    ),
    "LilycoveCity_Text_HoneymoonVowToSeeRarePokemon": (
        ("honeymoon", "rare POKéMON"),
        (
            "We promised to see as many rare\\n",
            "POKéMON as we could together.\\p",
            "The coast gave us one on day one.$",
        ),
    ),
}


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^(?P<label>{re.escape(label)}:)\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("PLAYER", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths() -> None:
    for label, (_, payloads) in TARGETS.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def render(source: str) -> str:
    rendered = source
    for label, (markers, payloads) in TARGETS.items():
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


def mask_targets(source: str) -> str:
    masked = source
    for label in TARGETS:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ARAUNA_BAIA>"\n\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str) -> None:
    if mask_targets(source) != mask_targets(rendered):
        raise ValueError("non-dialogue Baia das Luzes structure changed")

    forbidden = (
        "CONSORCIO HORIZONTE",
        "LILYCOVE",
        "SLATEPORT",
        "S.S. TIDAL",
        "SKY PILLAR",
        "KANTO",
    )
    for label, (_, payloads) in TARGETS.items():
        body = block_pattern(label).search(rendered).group("body")
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")
        for token in forbidden:
            if token in body:
                raise ValueError(f"{label}: legacy visible token survived: {token}")

    preserved = (
        "FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE",
        "FLAG_MET_WAILMER_TRAINER",
        "FLAG_BADGE07_GET",
        "CountPlayerMuseumPaintings",
        "LilycoveCity_EventScript_Rival::",
        "TRAINER_MAY_LILYCOVE_TREECKO",
        "TRAINER_BRENDAN_LILYCOVE_TREECKO",
    )
    for token in preserved:
        if token not in rendered:
            raise ValueError(f"preserved Lilycove gameplay token missing: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the common Baia das Luzes city surface in English without changing Lilycove event wiring."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate_widths()
    source = TARGET.read_text(encoding="utf-8")
    rendered = render(source)
    validate_rendered(source, rendered)

    if args.check:
        print(f"Baia das Luzes common renderer OK: {len(TARGETS)} text blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

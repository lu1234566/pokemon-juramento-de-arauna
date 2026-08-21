#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "text" / "arauna" / "en" / "mata_do_meio_interiors.json"
FILES = {
    "house1": ROOT / "data" / "maps" / "FortreeCity_House1" / "scripts.inc",
    "house2": ROOT / "data" / "maps" / "FortreeCity_House2" / "scripts.inc",
    "house3": ROOT / "data" / "maps" / "FortreeCity_House3" / "scripts.inc",
    "house4": ROOT / "data" / "maps" / "FortreeCity_House4" / "scripts.inc",
    "house5": ROOT / "data" / "maps" / "FortreeCity_House5" / "scripts.inc",
    "decor": ROOT / "data" / "maps" / "FortreeCity_DecorationShop" / "scripts.inc",
    "mart": ROOT / "data" / "maps" / "FortreeCity_Mart" / "scripts.inc",
    "center": ROOT / "data" / "maps" / "FortreeCity_PokemonCenter_1F" / "scripts.inc",
}
EXPECTED_COUNTS = {
    "house1": 7,
    "house2": 7,
    "house3": 2,
    "house4": 6,
    "house5": 3,
    "decor": 2,
    "mart": 3,
    "center": 3,
}
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

RAW_MARKERS = {
    "FortreeCity_House1_Text_YouWillTradeWontYou": ("Wrooooaaar!", "your {STR_VAR_1}"),
    "FortreeCity_House1_Text_MonYouTakeCare": ("Oh, yeah, right on!",),
    "FortreeCity_House1_Text_ThisIsntAMon": ("That isn't a {STR_VAR_1}",),
    "FortreeCity_House1_Text_YouWontTradeMe": ("You won't trade me?",),
    "FortreeCity_House1_Text_GoingToMakeVolbeatStrong": ("VOLBEAT super",),
    "FortreeCity_House1_Text_TradingMemoriesWithOthers": ("trading your own",),
    "FortreeCity_House1_Text_Zigzagoon": ("Gumomoh",),
    "FortreeCity_House2_Text_HiddenPowersArousedByNature": ("hidden powers are aroused",),
    "FortreeCity_House2_Text_CoinInWhichHand": ("I hold a coin",),
    "FortreeCity_House2_Text_CorrectTryAgainWhichHand": ("Oh! Yes, correct!",),
    "FortreeCity_House2_Text_CorrectTryAgainWhichHand2": ("Oh! Yes, correct!",),
    "FortreeCity_House2_Text_YourHiddenPowerHasAwoken": ("Your hidden power has awoken",),
    "FortreeCity_House2_Text_ExplainHiddenPower": ("HIDDEN POWER is a move",),
    "FortreeCity_House2_Text_YouGuessedWrong": ("You guessed wrong",),
    "FortreeCity_House3_Text_MetStevenHadAmazingPokemon": ("SEU BENTO:", "Nao para substituir"),
    "FortreeCity_House3_Text_OhYouHavePokedex": ("called a POKéDEX",),
    "FortreeCity_House4_Text_BringsWorldCloserTogether": ("world closer",),
    "FortreeCity_House4_Text_GoBirdPokemon": ("Go, BIRD POKéMON",),
    "FortreeCity_House4_Text_AskedWingullToRunErrand": ("asked my WINGULL",),
    "FortreeCity_House4_Text_WelcomeWingullTakeMentalHerb": ("MENTAL HERB",),
    "FortreeCity_House4_Text_FriendsFarAwayThanksToWingull": ("friends", "WINGULL"),
    "FortreeCity_House4_Text_Wingull": ("Pihyoh",),
    "FortreeCity_House5_Text_TreeHousesAreGreat": ("FORTREE",),
    "FortreeCity_House5_Text_AdaptedToNature": ("adapted to", "nature"),
    "FortreeCity_House5_Text_Zigzagoon": ("Bufuu",),
    "FortreeCity_DecorationShop_Text_MerchandiseSentToPC": ("Merchandise you buy",),
    "FortreeCity_DecorationShop_Text_BuyingDeskForDolls": ("pretty desk",),
    "FortreeCity_Mart_Text_SuperRepelBetter": ("SUPER REPEL lasts",),
    "FortreeCity_Mart_Text_StockUpOnItems": ("stock up",),
    "FortreeCity_Mart_Text_RareCandyMakesMonGrow": ("RARE CANDY",),
    "FortreeCity_PokemonCenter_1F_Text_GoToSafariZone": ("Ei, voce", "SAFARI ZONE"),
    "FortreeCity_PokemonCenter_1F_Text_RecordCornerIsNeat": ("Ja usou", "RECORD CORNER"),
    "FortreeCity_PokemonCenter_1F_Text_DoYouKnowAboutPokenav": ("HORIZONTE", "MATCH CALL"),
}

CRITICAL_TOKENS = {
    "house1": (
        "FLAG_FORTREE_NPC_TRADE_COMPLETED",
        "INGAME_TRADE_PLUSLE",
        "GetInGameTradeSpeciesInfo",
        "ChoosePartyMon",
        "CreateInGameTradePokemon",
        "DoInGameTradeScene",
        "SPECIES_ZIGZAGOON",
    ),
    "house2": (
        "FLAG_RECEIVED_TM_HIDDEN_POWER",
        "FLAG_MET_HIDDEN_POWER_GIVER",
        "ITEM_TM_HIDDEN_POWER",
        "MULTI_RIGHTLEFT",
    ),
    "house3": (),
    "house4": (
        "FLAG_RECEIVED_MENTAL_HERB",
        "FLAG_WINGULL_DELIVERED_MAIL",
        "FLAG_WINGULL_SENT_ON_ERRAND",
        "ITEM_MENTAL_HERB",
        "SPECIES_WINGULL",
        "FLAG_HIDE_MOSSDEEP_CITY_HOUSE_2_WINGULL",
    ),
    "house5": ("SPECIES_ZIGZAGOON",),
    "decor": (
        "pokemartdecoration",
        "DECOR_SMALL_DESK",
        "DECOR_SMALL_CHAIR",
    ),
    "mart": (
        "pokemart FortreeCity_Mart_Pokemart",
        "ITEM_GREAT_BALL",
        "ITEM_ULTRA_BALL",
        "ITEM_SUPER_REPEL",
    ),
    "center": (
        "HEAL_LOCATION_FORTREE_CITY",
        "CableClub_OnResume",
        "Common_EventScript_PkmnCenterNurse",
    ),
}

STALE_VISIBLE = (
    "FORTREE",
    "HORIZONTE",
    "Nao para substituir",
    "Ei, voce",
    "Ja usou",
    "Entao ",
    "voce ",
    "nao ",
)


def load_bank() -> dict[str, dict[str, tuple[str, ...]]]:
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    if set(raw) != set(FILES):
        raise ValueError(f"section contract mismatch: {sorted(raw)}")

    bank: dict[str, dict[str, tuple[str, ...]]] = {}
    for section, expected_count in EXPECTED_COUNTS.items():
        entries = raw[section]
        if not isinstance(entries, dict) or len(entries) != expected_count:
            raise ValueError(f"{section}: expected {expected_count} labels")
        converted: dict[str, tuple[str, ...]] = {}
        for label, payloads in entries.items():
            if not isinstance(payloads, list) or not payloads:
                raise ValueError(f"{label}: expected non-empty payload list")
            payload_tuple = tuple(str(payload) for payload in payloads)
            if any('"' in payload for payload in payload_tuple):
                raise ValueError(f"{label}: raw double quote is not allowed")
            if any("$" in payload for payload in payload_tuple[:-1]):
                raise ValueError(f"{label}: terminator may appear only in final payload")
            if not payload_tuple[-1].endswith("$"):
                raise ValueError(f"{label}: final payload must end with $")
            converted[label] = payload_tuple
        bank[section] = converted
    return bank


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?m)^{re.escape(label)}:\n"
        rf"(?P<body>(?:\t\.string [^\n]*\n"
        rf"(?:^(?!\t|[A-Za-z0-9_]+:|\s*$)[^\n]*\n)*)+)"
    )


def replacement(payloads: tuple[str, ...]) -> str:
    return "".join(f'\t.string "{payload}"\n' for payload in payloads)


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("LONGPHRASE123456", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths(bank: dict[str, dict[str, tuple[str, ...]]]) -> None:
    for entries in bank.values():
        for label, payloads in entries.items():
            for payload in payloads:
                for segment in visible_segments(payload):
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(
                            f"{label}: visible segment is {len(segment)} chars: {segment!r}"
                        )


def render_one(section: str, source: str, entries: dict[str, tuple[str, ...]]) -> str:
    rendered = source
    before_counts = {token: source.count(token) for token in CRITICAL_TOKENS[section]}

    for label, payloads in entries.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected exactly one text block, found {len(matches)}")
        body = matches[0].group("body")
        new_body = replacement(payloads)
        if body != new_body:
            for marker in RAW_MARKERS[label]:
                if marker not in body:
                    raise ValueError(f"{label}: expected raw marker missing: {marker!r}")
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]

    masked_source = source
    masked_rendered = rendered
    for label in entries:
        for name, text in (("source", masked_source), ("rendered", masked_rendered)):
            match = block_pattern(label).search(text)
            if not match:
                raise ValueError(f"{label}: cannot mask {name} block")
            start, end = match.span("body")
            text = text[:start] + '\t.string "<MATA_DO_MEIO_INTERIOR>"\n' + text[end:]
            if name == "source":
                masked_source = text
            else:
                masked_rendered = text
    if masked_source != masked_rendered:
        raise ValueError(f"{section}: non-dialogue structure changed")

    after_counts = {token: rendered.count(token) for token in CRITICAL_TOKENS[section]}
    if before_counts != after_counts:
        raise ValueError(f"{section}: progression token counts changed: {before_counts} -> {after_counts}")

    for label in entries:
        match = block_pattern(label).search(rendered)
        if not match:
            raise ValueError(f"{label}: rendered block missing")
        body = match.group("body")
        for token in STALE_VISIBLE:
            if token in body:
                raise ValueError(f"{label}: stale visible token survived: {token!r}")
    return rendered


def validate_identity(bank: dict[str, dict[str, tuple[str, ...]]]) -> None:
    joined = "\n".join(
        payload
        for entries in bank.values()
        for payloads in entries.values()
        for payload in payloads
    )
    for required in (
        "MATA DO MEIO",
        "SEU BENTO:",
        "HIDDEN POWER",
        "WINGULL",
        "MATCH CALL",
    ):
        if required not in joined:
            raise ValueError(f"required interior identity missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Mata do Meio daily-life interiors in English without changing inherited Fortree mechanics."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    validate_widths(bank)
    validate_identity(bank)

    rendered_by_section: dict[str, str] = {}
    for section, path in FILES.items():
        source = path.read_text(encoding="utf-8")
        rendered_by_section[section] = render_one(section, source, bank[section])

    total = sum(len(entries) for entries in bank.values())
    if args.check:
        print(f"Mata do Meio interiors English renderer OK: {total} blocks validated.")
        return 0
    if args.in_place:
        for section, path in FILES.items():
            path.write_text(rendered_by_section[section], encoding="utf-8")
        return 0

    for section in FILES:
        print(f"===== {section} =====")
        print(rendered_by_section[section], end="" if rendered_by_section[section].endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

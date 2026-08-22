#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "battle_circuit_public_services.json"
FILES = {
    "bento_room": ROOT / "data" / "maps" / "BattleFrontier_ScottsHouse" / "scripts.inc",
    "ranking": ROOT / "data" / "maps" / "BattleFrontier_RankingHall" / "scripts.inc",
    "exchange": ROOT / "data" / "maps" / "BattleFrontier_ExchangeServiceCorner" / "scripts.inc",
    "center": ROOT / "data" / "maps" / "BattleFrontier_PokemonCenter_1F" / "scripts.inc",
    "mart": ROOT / "data" / "maps" / "BattleFrontier_Mart" / "scripts.inc",
}
EXPECTED = {
    "bento_room": {
        "BattleFrontier_ScottsHouse_Text_WelcomeToBattleFrontier",
        "BattleFrontier_ScottsHouse_Text_HowMuchEffortItTookToMakeReal",
        "BattleFrontier_ScottsHouse_Text_HaveThisAsMementoOfOurPathsCrossing",
        "BattleFrontier_ScottsHouse_Text_ObtainedXBattlePoints",
        "BattleFrontier_ScottsHouse_Text_ExplainBattlePoints",
        "BattleFrontier_ScottsHouse_Text_ExpectingGreatThings",
        "BattleFrontier_ScottsHouse_Text_WhyIGoSeekingTrainers",
        "BattleFrontier_ScottsHouse_Text_HaveYouMetFrontierBrain",
        "BattleFrontier_ScottsHouse_Text_MayFindWildMonsInFrontier",
        "BattleFrontier_ScottsHouse_Text_YouveCollectedAllSilverSymbols",
        "BattleFrontier_ScottsHouse_Text_YouveCollectedAllGoldSymbols",
        "BattleFrontier_ScottsHouse_Text_SoGladIBroughtYouHere",
        "BattleFrontier_ScottsHouse_Text_BerryPocketStuffed",
        "BattleFrontier_ScottsHouse_Text_Beat50TrainersInARow",
        "BattleFrontier_ScottsHouse_Text_Beat100TrainersInARow",
        "BattleFrontier_ScottsHouse_Text_ExpectingToHearEvenGreaterThings",
        "BattleFrontier_ScottsHouse_Text_ComeBackForThisLater",
    },
    "ranking": {
        "BattleFrontier_RankingHall_Text_ExplainRankingHall",
        "BattleFrontier_RankingHall_Text_DomePikeFactoryRecords",
        "BattleFrontier_RankingHall_Text_PalaceArenaPyramidRecords",
        "BattleFrontier_RankingHall_Text_IsYourNameOnThisList",
        "BattleFrontier_RankingHall_Text_WowThatsSuper",
        "BattleFrontier_RankingHall_Text_WorkHarderIfYouSawFriendsName",
        "BattleFrontier_RankingHall_Text_MyNamesNotUpThere",
    },
    "exchange": {
        "BattleFrontier_ExchangeServiceCorner_Text_WelcomePleaseChoosePrize",
        "BattleFrontier_ExchangeServiceCorner_Text_WellSendItToPC",
        "BattleFrontier_ExchangeServiceCorner_Text_HereIsYourPrize",
        "BattleFrontier_ExchangeServiceCorner_Text_DontHaveEnoughPoints",
        "BattleFrontier_ExchangeServiceCorner_Text_PCIsFull",
        "BattleFrontier_ExchangeServiceCorner_Text_DontHaveSpaceToHoldIt",
        "BattleFrontier_ExchangeServiceCorner_Text_ThankYouVisitWithPoints",
        "BattleFrontier_ExchangeServiceCorner_Text_WishIHadAllDolls",
        "BattleFrontier_ExchangeServiceCorner_Text_GetYouAnythingYouWant",
        "BattleFrontier_ExchangeServiceCorner_Text_ItemsWillGetMonTougher",
        "BattleFrontier_ExchangeServiceCorner_Text_GoGetYourOwnDoll",
        "BattleFrontier_ExchangeServiceCorner_Text_MoreBattlePointsForRecord",
    },
    "center": {
        "BattleFrontier_PokemonCenter_1F_Text_NeverSeenPokemon",
        "BattleFrontier_PokemonCenter_1F_Text_NextStopBattleArena",
        "BattleFrontier_PokemonCenter_1F_Text_GoingThroughEveryChallenge",
        "BattleFrontier_PokemonCenter_1F_Text_Skitty",
    },
    "mart": {
        "BattleFrontier_Mart_Text_ChaperonGrandson",
        "BattleFrontier_Mart_Text_ProteinMakeNiceGift",
        "BattleFrontier_Mart_Text_FacilitiesDontAllowItems",
    },
}
GAMEPLAY_TOKENS = {
    "bento_room": (
        "FLAG_SCOTT_GIVES_BATTLE_POINTS",
        "FLAG_COLLECTED_ALL_SILVER_SYMBOLS",
        "FLAG_COLLECTED_ALL_GOLD_SYMBOLS",
        "FLAG_RECEIVED_SILVER_SHIELD",
        "FLAG_RECEIVED_GOLD_SHIELD",
        "ITEM_LANSAT_BERRY",
        "ITEM_STARF_BERRY",
        "DECOR_SILVER_SHIELD",
        "DECOR_GOLD_SHIELD",
        "FRONTIER_DATA_LVL_MODE",
        "FRONTIER_LVL_50",
        "FRONTIER_LVL_OPEN",
        "TOWER_DATA_WIN_STREAK",
        "GiveFrontierBattlePoints",
        "VAR_SCOTT_STATE",
        "LOCALID_SCOTTS_HOUSE_SCOTT",
        "random 3",
    ),
    "ranking": (
        "VAR_0x8005",
        "RANKING_HALL_TOWER_SINGLES",
        "RANKING_HALL_PYRAMID",
        "ShowRankingHallRecordsWindow",
        "ScrollRankingHallRecordsWindow",
        "RemoveRecordsWindow",
        "MSGBOX_YESNO",
    ),
    "exchange": (
        "GetFrontierBattlePoints",
        "TakeFrontierBattlePoints",
        "ShowBattlePointsWindow",
        "CloseBattlePointsWindow",
        "UpdateBattlePointsWindow",
        "ShowScrollableMultichoice",
        "checkdecorspace",
        "checkitemspace",
        "adddecoration",
        "additem",
        "EXCHANGE_CORNER_DECOR1_CLERK",
        "EXCHANGE_CORNER_VITAMIN_CLERK",
        "DECOR_KISS_POSTER",
        "ITEM_PROTEIN",
        "ITEM_LEFTOVERS",
    ),
    "center": (
        "HEAL_LOCATION_BATTLE_FRONTIER_OUTSIDE_EAST",
        "CableClub_OnResume",
        "Common_EventScript_PkmnCenterNurse",
        "LOCALID_FRONTIER_NURSE",
        "SPECIES_SKITTY",
        "playmoncry",
    ),
    "mart": (
        "pokemart BattleFrontier_Mart_Pokemart",
        "ITEM_ULTRA_BALL",
        "ITEM_FULL_RESTORE",
        "ITEM_REVIVE",
        "ITEM_PROTEIN",
        "ITEM_HP_UP",
        "LOCALID_FRONTIER_MART_OLD_WOMAN",
    ),
}
MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_SAMPLE = "LONGPHRASE123456"
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def load_bank() -> dict[str, dict[str, list[str]]]:
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(bank) != set(FILES):
        raise ValueError(f"bank sections mismatch: {sorted(bank)}")
    for section, expected in EXPECTED.items():
        actual = set(bank[section])
        if actual != expected:
            raise ValueError(
                f"{section}: label contract mismatch; "
                f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
            )
    return bank


def validate_payloads(bank: dict[str, dict[str, list[str]]]) -> None:
    for section, entries in bank.items():
        for label, payloads in entries.items():
            if not payloads or not all(isinstance(x, str) and x for x in payloads):
                raise ValueError(f"{section}/{label}: payloads must be non-empty strings")
            if not payloads[-1].endswith("$"):
                raise ValueError(f"{section}/{label}: final payload must end with $")
            if any("$" in payload for payload in payloads[:-1]):
                raise ValueError(f"{section}/{label}: early $ terminator")
            for payload in payloads:
                if '"' in payload:
                    raise ValueError(f"{section}/{label}: raw quote is not assembler-safe")
                visible = PLACEHOLDER_RE.sub(PLACEHOLDER_SAMPLE, payload).replace("$", "")
                for segment in CONTROL_RE.split(visible):
                    segment = segment.strip()
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(
                            f"{section}/{label}: {len(segment)}-char segment: {segment!r}"
                        )


def body_span(source: str, label: str) -> tuple[int, int]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::?\n", source))
    if len(matches) != 1:
        raise ValueError(f"{label}: expected one label, found {len(matches)}")
    start = matches[0].end()
    pos = start
    saw_string = False
    continuation = False
    while pos < len(source):
        newline = source.find("\n", pos)
        end = len(source) if newline < 0 else newline + 1
        line = source[pos:end]
        is_string = line.lstrip(" \t").startswith(".string ")
        if is_string or continuation:
            saw_string = saw_string or is_string
            continuation = line.rstrip("\n").endswith("\\")
            pos = end
            continue
        break
    if not saw_string:
        raise ValueError(f"{label}: no consecutive .string body found")
    return start, pos


def render_text(source: str, targets: dict[str, list[str]]) -> str:
    spans: list[tuple[int, int, str]] = []
    for label, payloads in targets.items():
        start, end = body_span(source, label)
        body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        spans.append((start, end, body))
    rendered = source
    for start, end, body in sorted(spans, reverse=True):
        rendered = rendered[:start] + body + rendered[end:]
    return rendered


def mask_targets(source: str, labels: set[str], marker: str) -> str:
    spans = [body_span(source, label) for label in labels]
    masked = source
    for start, end in sorted(spans, reverse=True):
        masked = masked[:start] + f'\t.string "<{marker}>"\n' + masked[end:]
    return masked


def validate_section(
    section: str,
    source: str,
    rendered: str,
    targets: dict[str, list[str]],
) -> None:
    marker = f"ARAUNA_BATTLE_CIRCUIT_{section.upper()}"
    if mask_targets(source, EXPECTED[section], marker) != mask_targets(
        rendered, EXPECTED[section], marker
    ):
        raise ValueError(f"{section}: non-dialogue structure changed")

    for token in GAMEPLAY_TOKENS[section]:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            raise ValueError(f"{section}: expected gameplay token missing: {token}")
        if before != after:
            raise ValueError(f"{section}: gameplay token changed: {token}: {before} -> {after}")

    for label, payloads in targets.items():
        start, end = body_span(rendered, label)
        body = rendered[start:end]
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{section}/{label}: rendered payload missing: {payload!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Battle Circuit public-services English surface.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    validate_payloads(bank)
    outputs: dict[str, str] = {}
    for section, path in FILES.items():
        source = path.read_text(encoding="utf-8")
        rendered = render_text(source, bank[section])
        validate_section(section, source, rendered, bank[section])
        outputs[section] = rendered

    owned = "\n".join(
        outputs[section][body_span(outputs[section], label)[0]:body_span(outputs[section], label)[1]]
        for section in FILES
        for label in EXPECTED[section]
    )
    for stale in (
        "CIRCUITO DE BATALHA",
        "PASSE DO CIRCUITO",
        "Pontos de Batalha",
        "TORRE DE BATALHA",
        "BATTLE FRONTIER",
        "EXCHANGE SERVICE",
        "immortal TRAINERS",
    ):
        if stale in owned:
            raise ValueError(f"stale visible token survived: {stale}")
    for required in (
        "SEU BENTO",
        "BATTLE CIRCUIT",
        "CIRCUIT PASS",
        "CIRCUIT MASTER",
        "SILVER SYMBOLS",
        "GOLD",
        "BATTLE TOWER",
        "RANKING HALL",
        "BATTLE POINT",
        "BATTLE ARENA",
        "ARAUNA",
    ):
        if required not in owned:
            raise ValueError(f"public-services identity missing: {required}")

    if args.check:
        print(
            "Battle Circuit public-services renderer OK: "
            f"{sum(len(v) for v in EXPECTED.values())} blocks across {len(FILES)} maps validated."
        )
        return 0
    if args.in_place:
        for section, path in FILES.items():
            path.write_text(outputs[section], encoding="utf-8")
        return 0

    print(outputs["bento_room"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

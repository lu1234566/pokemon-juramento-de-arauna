#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "baia_luzes_department_store.json"
FILES = {
    "1f": ROOT / "data" / "maps" / "LilycoveCity_DepartmentStore_1F" / "scripts.inc",
    "2f": ROOT / "data" / "maps" / "LilycoveCity_DepartmentStore_2F" / "scripts.inc",
    "3f": ROOT / "data" / "maps" / "LilycoveCity_DepartmentStore_3F" / "scripts.inc",
    "4f": ROOT / "data" / "maps" / "LilycoveCity_DepartmentStore_4F" / "scripts.inc",
    "5f": ROOT / "data" / "maps" / "LilycoveCity_DepartmentStore_5F" / "scripts.inc",
    "roof": ROOT / "data" / "maps" / "LilycoveCity_DepartmentStoreRooftop" / "scripts.inc",
}
EXPECTED = {
    "1f": {
        "LilycoveCity_DepartmentStore_1F_Text_WelcomeToDeptStore",
        "LilycoveCity_DepartmentStore_1F_Text_IBuyAllSortsOfThings",
        "LilycoveCity_DepartmentStore_1F_Text_MomBuyingMeFurniture",
        "LilycoveCity_DepartmentStore_1F_Text_BuyingSomethingForAzumarill",
        "LilycoveCity_DepartmentStore_1F_Text_FloorNamesSign",
    },
    "2f": {
        "LilycoveCity_DepartmentStore_2F_Text_LearnToUseItemsProperly",
        "LilycoveCity_DepartmentStore_2F_Text_GoodGiftForHusband",
        "LilycoveCity_DepartmentStore_2F_Text_StockUpOnItems",
    },
    "3f": {
        "LilycoveCity_DepartmentStore_3F_Text_ItemsBestForTougheningPokemon",
        "LilycoveCity_DepartmentStore_3F_Text_WantMoreEndurance",
        "LilycoveCity_DepartmentStore_3F_Text_GaveCarbosToSpeedUpMon",
    },
    "4f": {
        "LilycoveCity_DepartmentStore_4F_Text_AttackOrDefenseTM",
        "LilycoveCity_DepartmentStore_4F_Text_FiftyDifferentTMs",
        "LilycoveCity_DepartmentStore_4F_Text_PokemonOnlyHaveFourMoves",
    },
    "5f": {
        "LilycoveCity_DepartmentStore_5F_Text_PlaceFullOfCuteDolls",
        "LilycoveCity_DepartmentStore_5F_Text_GettingDollInsteadOfPokemon",
        "LilycoveCity_DepartmentStore_5F_Text_SellManyCuteMatsHere",
        "LilycoveCity_DepartmentStore_5F_Text_ClosedRooftopForWeather",
    },
    "roof": {
        "LilycoveCity_DepartmentStoreRooftop_Text_SetDatesForClearOutSales",
        "LilycoveCity_DepartmentStoreRooftop_Text_BeenWaitingForClearOutSale",
        "LilycoveCity_DepartmentStoreRooftop_Text_BoneDryThirsty",
        "LilycoveCity_DepartmentStoreRooftop_Text_WhichDrinkWouldYouLike",
        "LilycoveCity_DepartmentStoreRooftop_Text_CanOfDrinkDroppedDown",
        "LilycoveCity_DepartmentStoreRooftop_Text_ExtraCanOfDrinkDroppedDown",
        "LilycoveCity_DepartmentStoreRooftop_Text_NotEnoughMoney",
        "LilycoveCity_DepartmentStoreRooftop_Text_DecidedAgainstBuyingDrink",
    },
}
GAMEPLAY_TOKENS = {
    "1f": (
        "FLAG_DAILY_PICKED_LOTO_TICKET",
        "VAR_POKELOT_PRIZE_ITEM",
        "RetrieveLotteryNumber",
        "PickLotteryCornerTicket",
        "TryPutLotteryWinnerReportOnAir",
        "SPECIES_AZUMARILL",
    ),
    "2f": ("ITEM_ULTRA_BALL", "ITEM_MAX_POTION", "ITEM_MAX_REPEL", "pokemartlistend"),
    "3f": ("ITEM_PROTEIN", "ITEM_ZINC", "ITEM_X_ATTACK", "ITEM_X_ACCURACY", "pokemartlistend"),
    "4f": ("ITEM_TM_FIRE_BLAST", "ITEM_TM_HYPER_BEAM", "ITEM_TM_PROTECT", "ITEM_TM_LIGHT_SCREEN", "pokemartlistend"),
    "5f": (
        "VAR_SOOTOPOLIS_CITY_STATE",
        "DECOR_PICHU_DOLL",
        "DECOR_WATER_CUSHION",
        "DECOR_SKY_POSTER",
        "DECOR_SPIN_MAT",
        "pokemartlistend",
    ),
    "roof": (
        "POKENEWS_LILYCOVE",
        "FLAG_HIDE_LILYCOVE_DEPARTMENT_STORE_ROOFTOP_SALE_WOMAN",
        "MULTI_VENDING_MACHINE",
        "ITEM_FRESH_WATER",
        "ITEM_SODA_POP",
        "ITEM_LEMONADE",
        "checkmoney 200",
        "checkmoney 300",
        "checkmoney 350",
        "random 64",
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
    for section, labels in EXPECTED.items():
        actual = set(bank[section])
        if actual != labels:
            raise ValueError(
                f"{section}: label contract mismatch; "
                f"missing={sorted(labels - actual)}, extra={sorted(actual - labels)}"
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
                            f"{section}/{label}: visible segment is "
                            f"{len(segment)} chars: {segment!r}"
                        )


def label_match(source: str, label: str) -> re.Match[str]:
    pattern = re.compile(rf"(?m)^{re.escape(label)}::?\n")
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        raise ValueError(f"{label}: expected one label, found {len(matches)}")
    return matches[0]


def body_span(source: str, label: str) -> tuple[int, int]:
    match = label_match(source, label)
    start = match.end()
    pos = start
    saw_string = False
    continuation = False
    while pos < len(source):
        newline = source.find("\n", pos)
        end = len(source) if newline < 0 else newline + 1
        line = source[pos:end]
        stripped = line.lstrip(" \t")
        is_string = stripped.startswith(".string ")
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
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        spans.append((start, end, new_body))
    rendered = source
    for start, end, new_body in sorted(spans, reverse=True):
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_targets(source: str, labels: set[str], marker: str) -> str:
    spans = [body_span(source, label) for label in labels]
    masked = source
    for start, end in sorted(spans, reverse=True):
        masked = masked[:start] + f'\t.string "<{marker}>"\n' + masked[end:]
    return masked


def validate_structure(section: str, source: str, rendered: str) -> None:
    marker = f"ARAUNA_DEPT_{section.upper()}"
    if mask_targets(source, EXPECTED[section], marker) != mask_targets(
        rendered, EXPECTED[section], marker
    ):
        raise ValueError(f"{section}: non-dialogue Department Store structure changed")


def validate_gameplay_counts(section: str, source: str, rendered: str) -> None:
    for token in GAMEPLAY_TOKENS[section]:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            raise ValueError(f"{section}: expected gameplay/inventory token missing: {token}")
        if before != after:
            raise ValueError(
                f"{section}: gameplay/inventory token count changed: "
                f"{token}: {before} -> {after}"
            )


def validate_rendered(section: str, rendered: str, targets: dict[str, list[str]]) -> None:
    for label, payloads in targets.items():
        start, end = body_span(rendered, label)
        body = rendered[start:end]
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{section}/{label}: rendered payload missing: {payload!r}")

    owned = "\n".join(
        rendered[body_span(rendered, label)[0]:body_span(rendered, label)[1]]
        for label in EXPECTED[section]
    )
    if section == "1f" and "BAIA DAS LUZES DEPARTMENT STORE" in owned:
        raise ValueError("1f: legacy BAIA DAS LUZES store name survived")
    if section == "1f" and "BAIA DAS LUZES" not in owned:
        raise ValueError("1f: BAIA DAS LUZES identity missing")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Baia das Luzes Department Store daily-life text in English."
    )
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
        validate_structure(section, source, rendered)
        validate_gameplay_counts(section, source, rendered)
        validate_rendered(section, rendered, bank[section])
        outputs[section] = rendered

    if args.check:
        print(
            "Baia das Luzes Department Store English renderer OK: "
            f"{sum(len(labels) for labels in EXPECTED.values())} text blocks validated."
        )
        return 0
    if args.in_place:
        for section, path in FILES.items():
            path.write_text(outputs[section], encoding="utf-8")
        return 0

    print(outputs["1f"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

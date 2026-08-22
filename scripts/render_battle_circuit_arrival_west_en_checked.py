#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "battle_circuit_arrival_west.json"
TARGET_PATH = ROOT / "data" / "maps" / "BattleFrontier_OutsideWest" / "scripts.inc"
EXPECTED = {
    "BattleFrontier_OutsideWest_Text_BattleDomeSign",
    "BattleFrontier_OutsideWest_Text_BattleFactorySign",
    "BattleFrontier_OutsideWest_Text_BattlePikeSign",
    "BattleFrontier_OutsideWest_Text_ThisIsBattleTower",
    "BattleFrontier_OutsideWest_Text_MayISeeYourTicket",
    "BattleFrontier_OutsideWest_Text_MustHaveTicketToBoard",
    "BattleFrontier_OutsideWest_Text_WhereWouldYouLikeToGo",
    "BattleFrontier_OutsideWest_Text_SlateportItIs",
    "BattleFrontier_OutsideWest_Text_LilycoveItIs",
    "BattleFrontier_OutsideWest_Text_SailWithUsAnotherTime",
    "BattleFrontier_OutsideWest_Text_PleaseBoardFerry",
    "BattleFrontier_OutsideWest_Text_ThenWhereWouldYouLikeToGo",
    "BattleFrontier_OutsideWest_Text_BestOutOfAllMyFriends",
    "BattleFrontier_OutsideWest_Text_CantFindBattleTower",
    "BattleFrontier_OutsideWest_Text_GotSeasickOnWayHere",
    "BattleFrontier_OutsideWest_Text_OnlyToughTrainersBroughtHere",
    "BattleFrontier_OutsideWest_Text_SureWeCanChallengeWithNoMons",
    "BattleFrontier_OutsideWest_Text_BigGuySaidIllLendYouMons",
    "BattleFrontier_OutsideWest_Text_WhosRaisingThoseRentalMons",
    "BattleFrontier_OutsideWest_Text_ScaredOfPikeBecauseSeviper",
    "BattleFrontier_OutsideWest_Text_LetsPlayRockPaperScissors",
    "BattleFrontier_OutsideWest_Text_WonIllTakePikeChallenge",
    "BattleFrontier_OutsideWest_Text_LostIllPutOffPikeChallenge",
    "BattleFrontier_OutsideWest_Text_ChooseFishingOverBattling",
    "BattleFrontier_OutsideWest_Text_KeepBattlingUntilIGetSymbol",
    "BattleFrontier_OutsideWest_Text_YoureOffToChallengeDome",
    "BattleFrontier_OutsideWest_Text_DomeIsHereGrandpa",
    "BattleFrontier_OutsideWest_Text_WontLetGentlemenBeatMe",
    "BattleFrontier_OutsideWest_Text_NothingHereNotLongAgo",
    "BattleFrontier_OutsideWest_Text_FinallyArrivedAtFrontier",
    "BattleFrontier_OutsideWest_Text_SquareFilledWithToughPeople",
    "BattleFrontier_OutsideWest_Text_MetOlderGirlAtPike",
    "BattleFrontier_OutsideWest_Text_LastTimeOurEyesMet",
    "BattleFrontier_OutsideWest_Text_DomeAceLookedBecauseOfMyCheering",
    "BattleFrontier_OutsideWest_Text_DomeAceIsMine",
    "BattleFrontier_OutsideWest_Text_FansOverThereUsedToBeTrainers",
    "BattleFrontier_OutsideWest_Text_MonWithLongTailInFrontier",
}
GAMEPLAY_TOKENS = (
    "VAR_BRAVO_TRAINER_BATTLE_TOWER_ON",
    "FLAG_HIDE_BATTLE_TOWER_REPORTER",
    "ITEM_SS_TICKET",
    "MULTI_SSTIDAL_BATTLE_FRONTIER",
    "MAP_SLATEPORT_CITY_HARBOR",
    "MAP_LILYCOVE_CITY_HARBOR",
    "LOCALID_FRONTIER_FERRY_ATTENDANT",
    "LOCALID_FRONTIER_SS_TIDAL",
    "Common_EventScript_FerryDepartIsland",
    "LOCALID_FRONTIER_MANIAC_1",
    "LOCALID_FRONTIER_MANIAC_2",
    "LOCALID_FRONTIER_CAMPER",
    "LOCALID_FRONTIER_GIRL",
    "random 2",
)
MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_SAMPLE = "LONGPHRASE123456"
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def load_bank() -> dict[str, list[str]]:
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    actual = set(bank)
    if actual != EXPECTED:
        raise ValueError(
            f"label contract mismatch; missing={sorted(EXPECTED - actual)}, "
            f"extra={sorted(actual - EXPECTED)}"
        )
    return bank


def validate_payloads(bank: dict[str, list[str]]) -> None:
    for label, payloads in bank.items():
        if not payloads or not all(isinstance(x, str) and x for x in payloads):
            raise ValueError(f"{label}: payloads must be non-empty strings")
        if not payloads[-1].endswith("$"):
            raise ValueError(f"{label}: final payload must end with $")
        if any("$" in payload for payload in payloads[:-1]):
            raise ValueError(f"{label}: early $ terminator")
        for payload in payloads:
            if '"' in payload:
                raise ValueError(f"{label}: raw quote is not assembler-safe")
            visible = PLACEHOLDER_RE.sub(PLACEHOLDER_SAMPLE, payload).replace("$", "")
            for segment in CONTROL_RE.split(visible):
                segment = segment.strip()
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)}-char segment: {segment!r}")


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


def render(source: str, bank: dict[str, list[str]]) -> str:
    spans: list[tuple[int, int, str]] = []
    for label, payloads in bank.items():
        start, end = body_span(source, label)
        body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        spans.append((start, end, body))
    result = source
    for start, end, body in sorted(spans, reverse=True):
        result = result[:start] + body + result[end:]
    return result


def mask(source: str) -> str:
    spans = [body_span(source, label) for label in EXPECTED]
    result = source
    for start, end in sorted(spans, reverse=True):
        result = result[:start] + '\t.string "<ARAUNA_BATTLE_CIRCUIT_WEST>"\n' + result[end:]
    return result


def validate(source: str, rendered: str, bank: dict[str, list[str]]) -> None:
    if mask(source) != mask(rendered):
        raise ValueError("non-dialogue structure changed")
    for token in GAMEPLAY_TOKENS:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            raise ValueError(f"expected gameplay token missing: {token}")
        if before != after:
            raise ValueError(f"gameplay token changed: {token}: {before} -> {after}")
    for label, payloads in bank.items():
        start, end = body_span(rendered, label)
        body = rendered[start:end]
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{label}: rendered payload missing: {payload!r}")
    owned = "\n".join(
        rendered[body_span(rendered, label)[0]:body_span(rendered, label)[1]]
        for label in EXPECTED
    )
    for stale in ("BATTLE FRONTIER", "SLATEPORT CITY", "LILYCOVE CITY", "fair-weather fans"):
        if stale in owned:
            raise ValueError(f"stale visible token survived: {stale}")
    for required in ("BATTLE CIRCUIT", "PORTO DO SAL", "BAIA DAS LUZES", "BATTLE DOME", "BATTLE FACTORY", "BATTLE PIKE"):
        if required not in owned:
            raise ValueError(f"arrival-district identity missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Battle Circuit west-arrival English surface.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    validate_payloads(bank)
    source = TARGET_PATH.read_text(encoding="utf-8")
    rendered = render(source, bank)
    validate(source, rendered, bank)

    if args.check:
        print(f"Battle Circuit west-arrival renderer OK: {len(EXPECTED)} blocks validated.")
        return 0
    if args.in_place:
        TARGET_PATH.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

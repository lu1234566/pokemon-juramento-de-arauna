#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "battle_circuit_reception_gate.json"
TARGET_PATH = ROOT / "data" / "maps" / "BattleFrontier_ReceptionGate" / "scripts.inc"
EXPECTED = {
    "BattleFrontier_ReceptionGate_Text_FirstTimeHereThisWay",
    "BattleFrontier_ReceptionGate_Text_WelcomeToBattleFrontier",
    "BattleFrontier_ReceptionGate_Text_IssueFrontierPass",
    "BattleFrontier_ReceptionGate_Text_ObtainedFrontierPass",
    "BattleFrontier_ReceptionGate_Text_PlacedTrainerCardInFrontierPass",
    "BattleFrontier_ReceptionGate_Text_EnjoyBattleFrontier",
    "BattleFrontier_ReceptionGate_Text_IfItIsntPlayerYouCame",
    "BattleFrontier_ReceptionGate_Text_OhMrScottGoodDay",
    "BattleFrontier_ReceptionGate_Text_ScottGreatToSeeYouHere",
    "BattleFrontier_ReceptionGate_Text_YourGuideToFacilities",
    "BattleFrontier_ReceptionGate_Text_LearnAboutWhich2",
    "BattleFrontier_ReceptionGate_Text_BattleTowerInfo",
    "BattleFrontier_ReceptionGate_Text_BattleDomeInfo",
    "BattleFrontier_ReceptionGate_Text_BattlePalaceInfo",
    "BattleFrontier_ReceptionGate_Text_BattleArenaInfo",
    "BattleFrontier_ReceptionGate_Text_BattleFactoryInfo",
    "BattleFrontier_ReceptionGate_Text_BattlePikeInfo",
    "BattleFrontier_ReceptionGate_Text_BattlePyramidInfo",
    "BattleFrontier_ReceptionGate_Text_RankingHallInfo",
    "BattleFrontier_ReceptionGate_Text_ExchangeCornerInfo",
    "BattleFrontier_ReceptionGate_Text_YourGuideToRules",
    "BattleFrontier_ReceptionGate_Text_LearnAboutWhat",
    "BattleFrontier_ReceptionGate_Text_LevelModeInfo",
    "BattleFrontier_ReceptionGate_Text_Level50Info",
    "BattleFrontier_ReceptionGate_Text_OpenLevelInfo",
    "BattleFrontier_ReceptionGate_Text_MonEntryInfo",
    "BattleFrontier_ReceptionGate_Text_HoldItemsInfo",
    "BattleFrontier_ReceptionGate_Text_YourGuideToFrontierPass",
    "BattleFrontier_ReceptionGate_Text_LearnAboutWhich1",
    "BattleFrontier_ReceptionGate_Text_SymbolsInfo",
    "BattleFrontier_ReceptionGate_Text_RecordedBattleInfo",
    "BattleFrontier_ReceptionGate_Text_BattlePointsInfo",
}
GAMEPLAY_TOKENS = (
    "FLAG_LANDMARK_BATTLE_FRONTIER",
    "VAR_HAS_ENTERED_BATTLE_FRONTIER",
    "LOCALID_FRONTIER_RECEPTION_GREETER",
    "LOCALID_FRONTIER_RECEPTION_GUIDE",
    "LOCALID_FRONTIER_RECEPTION_SCOTT",
    "FLAG_SYS_FRONTIER_PASS",
    "MUS_OBTAIN_ITEM",
    "SCROLL_MULTI_BF_RECEPTIONIST",
    "MULTI_FRONTIER_RULES",
    "MULTI_FRONTIER_PASS_INFO",
    "ShowScrollableMultichoice",
    "MULTI_B_PRESSED",
    "BattleFrontier_ReceptionGate_Movement_ScottEnter",
    "BattleFrontier_ReceptionGate_Movement_ScottExit",
    "Common_Movement_ExclamationMark",
)
MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_SAMPLE = "LONGPHRASE123456"
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def load_bank() -> dict[str, list[str]]:
    raw = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(raw) != {"reception_gate"} or not isinstance(raw["reception_gate"], dict):
        raise ValueError("bank must contain exactly the reception_gate section")
    bank = raw["reception_gate"]
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
        result = result[:start] + '\t.string "<ARAUNA_BATTLE_CIRCUIT_RECEPTION>"\n' + result[end:]
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
    for stale in (
        "CIRCUITO DE BATALHA",
        "PASSE DO CIRCUITO",
        "Sobre qual",
        "instalacoes",
        "voce",
        "BATTLE FRONTIER",
        "FRONTIER PASS",
    ):
        if stale in owned:
            raise ValueError(f"stale visible token survived: {stale}")
    for required in (
        "BATTLE CIRCUIT",
        "CIRCUIT PASS",
        "SEU BENTO",
        "BATTLE TOWER",
        "BATTLE DOME",
        "BATTLE PALACE",
        "BATTLE ARENA",
        "BATTLE FACTORY",
        "BATTLE PIKE",
        "BATTLE PYRAMID",
        "RANKING HALL",
        "BATTLE POINT EXCHANGE",
        "LEVEL 50",
        "OPEN LEVEL",
        "SYMBOL",
    ):
        if required not in owned:
            raise ValueError(f"reception identity/rule missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Battle Circuit reception-gate English surface.")
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
        print(f"Battle Circuit reception renderer OK: {len(EXPECTED)} blocks validated.")
        return 0
    if args.in_place:
        TARGET_PATH.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

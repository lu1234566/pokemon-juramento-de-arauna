#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "circuit_pass_facilities.json"
TARGETS = {
    "dome": ROOT / "data" / "maps" / "BattleFrontier_BattleDomeLobby" / "scripts.inc",
    "palace": ROOT / "data" / "maps" / "BattleFrontier_BattlePalaceBattleRoom" / "scripts.inc",
    "arena": ROOT / "data" / "maps" / "BattleFrontier_BattleArenaBattleRoom" / "scripts.inc",
    "factory": ROOT / "data" / "maps" / "BattleFrontier_BattleFactoryBattleRoom" / "scripts.inc",
    "pike": ROOT / "data" / "maps" / "BattleFrontier_BattlePikeRoomNormal" / "scripts.inc",
    "pyramid": ROOT / "data" / "maps" / "BattleFrontier_BattlePyramidTop" / "scripts.inc",
}
EXPECTED = {
    "dome": {
        "BattleFrontier_BattleDomeLobby_Text_RecordLastMatch",
    },
    "palace": {
        "BattleFrontier_BattlePalaceBattleRoom_Text_RecordLastMatch",
        "BattleFrontier_BattlePalaceBattleRoom_Text_LetsSeeFrontierPass",
        "BattleFrontier_BattlePalaceBattleRoom_Text_ReceivedSpiritsSymbol",
        "BattleFrontier_BattlePalaceBattleRoom_Text_HurryWithFrontierPass",
    },
    "arena": {
        "BattleFrontier_BattleArenaBattleRoom_Text_RecordLastBattle",
        "BattleFrontier_BattleArenaBattleRoom_Text_GretaYoureToughAfterAll",
        "BattleFrontier_BattleArenaBattleRoom_Text_ReceivedGutsSymbol",
        "BattleFrontier_BattleArenaBattleRoom_Text_GretaBlownAway",
    },
    "factory": {
        "BattleFrontier_BattleFactoryBattleRoom_Text_NolandLetsSeeFrontierPass",
        "BattleFrontier_BattleFactoryBattleRoom_Text_ReceivedKnowledgeSymbol",
        "BattleFrontier_BattleFactoryBattleRoom_Text_OutOfMyLeagueLetsSeePass",
    },
    "pike": {
        "BattleFrontier_BattlePikeRoomNormal_Text_LucyShowMeFrontierPass",
        "BattleFrontier_BattlePikeRoomNormal_Text_ReceivedLuckSymbol",
        "BattleFrontier_BattlePikeRoomNormal_Text_LucyFrontierPass",
    },
    "pyramid": {
        "BattleFrontier_BattlePyramidTop_Text_BrandonFrontierPassPlease",
        "BattleFrontier_BattlePyramidTop_Text_ReceivedBraveSymbol",
    },
}
GAMEPLAY_TOKENS = {
    "dome": (
        "dome_save",
        "DOME_DATA_WIN_STREAK",
        "frontier_givepoints",
        "BattleFrontier_EventScript_SaveBattle",
        "FRONTIER_DATA_CHALLENGE_STATUS",
        "frontier_checkairshow",
    ),
    "palace": (
        "palace_incrementstreak",
        "frontier_getbrainstatus",
        "frontier_getsymbols",
        "frontier_givesymbol",
        "MUS_OBTAIN_SYMBOL",
        "SPECIAL_BATTLE_PALACE",
        "DoSpecialTrainerBattle",
        "FRONTIER_DATA_RECORD_DISABLED",
    ),
    "arena": (
        "arena_save",
        "frontier_getbrainstatus",
        "BattleFrontier_EventScript_SaveBattle",
        "frontier_getsymbols",
        "frontier_givesymbol",
        "MUS_OBTAIN_SYMBOL",
        "BattleFrontier_BattleArenaBattleRoom_EventScript_BattleGreta",
        "FRONTIER_DATA_RECORD_DISABLED",
    ),
    "factory": (
        "frontier_getbrainstatus",
        "frontier_getsymbols",
        "frontier_givesymbol",
        "MUS_OBTAIN_SYMBOL",
        "SPECIAL_BATTLE_FACTORY",
        "DoSpecialTrainerBattle",
        "FACTORY_DATA_WIN_STREAK",
        "FRONTIER_DATA_RECORD_DISABLED",
    ),
    "pike": (
        "pike_getbrainstatus",
        "frontier_getsymbols",
        "frontier_givesymbol",
        "MUS_OBTAIN_SYMBOL",
        "SPECIAL_BATTLE_PIKE_SINGLE",
        "SPECIAL_BATTLE_PIKE_DOUBLE",
        "DoSpecialTrainerBattle",
        "PIKE_DATA_WIN_STREAK",
    ),
    "pyramid": (
        "pyramid_save",
        "frontier_getbrainstatus",
        "frontier_getsymbols",
        "frontier_givesymbol",
        "MUS_OBTAIN_SYMBOL",
        "SPECIAL_BATTLE_PYRAMID",
        "DoSpecialTrainerBattle",
        "FRONTIER_DATA_CHALLENGE_STATUS",
    ),
}
REQUIRED = {
    "dome": ("CIRCUIT PASS", "BATTLE DOME"),
    "palace": ("CIRCUIT PASS", "SPENSER", "Spirits Symbol"),
    "arena": ("CIRCUIT PASS", "GRETA", "Guts Symbol"),
    "factory": ("CIRCUIT PASS", "NOLAND", "Knowledge Symbol"),
    "pike": ("CIRCUIT PASS", "LUCY", "Luck Symbol"),
    "pyramid": ("CIRCUIT PASS", "BRANDON", "Brave Symbol"),
}
MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_SAMPLE = "LONGPHRASE123456"
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def load_bank() -> dict[str, dict[str, list[str]]]:
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(bank) != set(EXPECTED):
        raise ValueError(f"section contract mismatch: {sorted(bank)}")
    for section, labels in EXPECTED.items():
        actual = set(bank[section])
        if actual != labels:
            raise ValueError(
                f"{section}: label contract mismatch; missing={sorted(labels - actual)}, "
                f"extra={sorted(actual - labels)}"
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


def render(source: str, entries: dict[str, list[str]]) -> str:
    spans: list[tuple[int, int, str]] = []
    for label, payloads in entries.items():
        start, end = body_span(source, label)
        body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        spans.append((start, end, body))
    result = source
    for start, end, body in sorted(spans, reverse=True):
        result = result[:start] + body + result[end:]
    return result


def mask(source: str, labels: set[str], marker: str) -> str:
    spans = [body_span(source, label) for label in labels]
    result = source
    for start, end in sorted(spans, reverse=True):
        result = result[:start] + f'\t.string "<{marker}>"\n' + result[end:]
    return result


def validate(
    section: str,
    source: str,
    rendered: str,
    entries: dict[str, list[str]],
) -> None:
    if mask(source, EXPECTED[section], section.upper()) != mask(
        rendered, EXPECTED[section], section.upper()
    ):
        raise ValueError(f"{section}: non-dialogue structure changed")

    for token in GAMEPLAY_TOKENS[section]:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            raise ValueError(f"{section}: expected gameplay token missing: {token}")
        if before != after:
            raise ValueError(f"{section}: gameplay token changed: {token}: {before} -> {after}")

    owned_parts: list[str] = []
    for label, payloads in entries.items():
        start, end = body_span(rendered, label)
        body = rendered[start:end]
        owned_parts.append(body)
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{section}/{label}: rendered payload missing: {payload!r}")
    owned = "\n".join(owned_parts)

    if "FRONTIER PASS" in owned:
        raise ValueError(f"{section}: stale visible FRONTIER PASS survived")
    for required in REQUIRED[section]:
        if required not in owned:
            raise ValueError(f"{section}: identity missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render cross-facility CIRCUIT PASS terminology.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    validate_payloads(bank)

    rendered_by_section: dict[str, str] = {}
    for section, path in TARGETS.items():
        source = path.read_text(encoding="utf-8")
        rendered = render(source, bank[section])
        validate(section, source, rendered, bank[section])
        rendered_by_section[section] = rendered

    if args.check:
        total = sum(len(v) for v in EXPECTED.values())
        print(f"Cross-facility Circuit Pass renderer OK: {total} blocks validated.")
        return 0

    if args.in_place:
        for section, path in TARGETS.items():
            path.write_text(rendered_by_section[section], encoding="utf-8")
        return 0

    for section in TARGETS:
        print(f"===== {section} =====")
        print(rendered_by_section[section], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

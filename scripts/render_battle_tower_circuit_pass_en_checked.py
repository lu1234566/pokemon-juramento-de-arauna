#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "battle_tower_circuit_pass.json"
TARGETS = {
    "lobby": ROOT / "data" / "maps" / "BattleFrontier_BattleTowerLobby" / "scripts.inc",
    "battle_room": ROOT / "data" / "maps" / "BattleFrontier_BattleTowerBattleRoom" / "scripts.inc",
}
EXPECTED = {
    "lobby": {
        "BattleFrontier_BattleTowerLobby_Text_RecordLastMatch",
    },
    "battle_room": {
        "BattleFrontier_BattleTowerBattleRoom_Text_RecordYourBattle",
        "BattleFrontier_BattleTowerLobby_Text_BattleRecordedOnPass",
        "BattleFrontier_BattleTowerBattleRoom_Text_AnabelTalentShallBeRecognized",
        "BattleFrontier_BattleTowerBattleRoom_Text_ReceivedAbilitySymbol",
        "BattleFrontier_BattleTowerBattleRoom_Text_AnabelCongratsYourPassPlease",
    },
}
GAMEPLAY_TOKENS = {
    "lobby": (
        "tower_save",
        "frontier_savebattle",
        "FRONTIER_DATA_RECORD_DISABLED",
        "TOWER_DATA_WIN_STREAK",
        "frontier_givepoints",
        "tower_giveribbons",
        "GAME_STAT_ENTERED_BATTLE_TOWER",
        "VAR_BRAVO_TRAINER_BATTLE_TOWER_ON",
        "MULTI_BATTLE_TOWER_RULES",
    ),
    "battle_room": (
        "frontier_getbrainstatus",
        "BattleFrontier_BattleTowerBattleRoom_EventScript_BattleAnabel",
        "BattleFrontier_EventScript_SaveBattle",
        "frontier_getsymbols",
        "frontier_givesymbol",
        "MUS_OBTAIN_SYMBOL",
        "FRONTIER_DATA_HEARD_BRAIN_SPEECH",
        "B_OUTCOME_WON",
        "frontier_incrementstreak",
        "FLAG_CANCEL_BATTLE_ROOM_CHALLENGE",
        "FRONTIER_DATA_RECORD_DISABLED",
    ),
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
    if "CIRCUIT PASS" not in owned:
        raise ValueError(f"{section}: CIRCUIT PASS identity missing")

    if section == "lobby" and "BATTLE TOWER" not in owned:
        raise ValueError("lobby: BATTLE TOWER context missing")
    if section == "battle_room":
        for required in ("ANABEL", "Ability Symbol"):
            if required not in owned:
                raise ValueError(f"battle_room identity missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Battle Tower CIRCUIT PASS terminology.")
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
        print(f"Battle Tower Circuit Pass renderer OK: {total} blocks validated.")
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

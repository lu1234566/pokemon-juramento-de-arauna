#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "battle_circuit_lounge_identity.json"
TARGETS = {
    "lounge3": ROOT / "data" / "maps" / "BattleFrontier_Lounge3" / "scripts.inc",
    "lounge8": ROOT / "data" / "maps" / "BattleFrontier_Lounge8" / "scripts.inc",
}
EXPECTED = {
    "lounge3": {"BattleFrontier_Lounge3_Text_YouLookToughExplainGambling"},
    "lounge8": {"BattleFrontier_Lounge8_Text_KnowAboutFrontierBrains"},
}
GAMEPLAY_TOKENS = {
    "lounge3": (
        "FLAG_MET_BATTLE_FRONTIER_GAMBLER",
        "ShowFrontierGamblerLookingMessage",
        "ShowBattlePointsWindow",
        "MULTI_FRONTIER_GAMBLER_BET",
        "VAR_FRONTIER_GAMBLER_AMOUNT_BET",
        "VAR_FRONTIER_GAMBLER_STATE",
        "TakeFrontierBattlePoints",
        "GiveFrontierBattlePoints",
        "BET_AMOUNT_5",
        "BET_AMOUNT_10",
        "BET_AMOUNT_15",
        "FLAG_SYS_TOWER_SILVER",
        "FLAG_SYS_DOME_SILVER",
        "FLAG_SYS_PALACE_SILVER",
        "FLAG_SYS_ARENA_SILVER",
        "FLAG_SYS_FACTORY_SILVER",
        "FLAG_SYS_PIKE_SILVER",
        "FLAG_SYS_PYRAMID_SILVER",
    ),
    "lounge8": (
        "BattleFrontier_Lounge8_EventScript_Man",
        "BattleFrontier_Lounge8_EventScript_Woman",
        "BattleFrontier_Lounge8_EventScript_NinjaBoy",
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

    for stale in ("BATTLE FRONTIER", "SCOTT", "FRONTIER BRAINS"):
        if stale in owned:
            raise ValueError(f"{section}: stale visible token survived: {stale}")

    if section == "lounge3":
        for required in ("BATTLE", "CIRCUIT", "Battle Points", "Best record"):
            if required not in owned:
                raise ValueError(f"lounge3 identity missing: {required}")
    elif section == "lounge8":
        for required in ("CIRCUIT MASTERS", "SEU BENTO", "BATTLE CIRCUIT"):
            if required not in owned:
                raise ValueError(f"lounge8 identity missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Battle Circuit lounge identity residues.")
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
        print(f"Battle Circuit lounge identity renderer OK: {total} blocks validated.")
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

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "battle_tent_side_identity.json"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

FILES = {
    "ash_field": ROOT / "data" / "maps" / "FallarborTown_BattleTentLobby" / "scripts.inc",
    "silent_valley": ROOT / "data" / "maps" / "VerdanturfTown_BattleTentLobby" / "scripts.inc",
}
EXPECTED = {
    "ash_field": {
        "FallarborTown_BattleTentLobby_Text_FallarborTentMyFavorite",
        "FallarborTown_BattleTentLobby_Text_ScottLookingForSomeone",
        "FallarborTown_BattleTentLobby_Text_ScottMakeChallenge",
    },
    "silent_valley": {
        "VerdanturfTown_BattleTentLobby_Text_ScottCanMeetToughTrainers",
        "VerdanturfTown_BattleTentLobby_Text_ScottVisitRegularly",
    },
}
GAMEPLAY_TOKENS = {
    "ash_field": (
        "FLAG_MET_SCOTT_IN_FALLARBOR",
        "VAR_SCOTT_STATE",
        "FRONTIER_FACILITY_ARENA",
        "CHALLENGE_STATUS_SAVING",
        "fallarbortent_init",
    ),
    "silent_valley": (
        "FLAG_MET_SCOTT_IN_VERDANTURF",
        "VAR_SCOTT_STATE",
        "FRONTIER_FACILITY_PALACE",
        "CHALLENGE_STATUS_SAVING",
        "verdanturftent_init",
    ),
}


def fail(message: str) -> None:
    raise ValueError(f"Battle Tent side identity renderer: {message}")


def load_bank() -> dict[str, dict[str, list[str]]]:
    raw = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(raw) != set(FILES):
        fail("bank section contract mismatch")
    for section, expected in EXPECTED.items():
        if set(raw[section]) != expected:
            fail(
                f"{section}: label contract mismatch; "
                f"missing={sorted(expected - set(raw[section]))}, "
                f"extra={sorted(set(raw[section]) - expected)}"
            )
        for label, payloads in raw[section].items():
            if not payloads or not all(isinstance(x, str) and x for x in payloads):
                fail(f"{label}: payload must be a non-empty string list")
            joined = "".join(payloads)
            if joined.count("$") != 1 or not joined.endswith("$"):
                fail(f"{label}: exactly one final '$' is required")
            if any('"' in payload for payload in payloads):
                fail(f"{label}: raw quote is not assembler-safe")
            for payload in payloads:
                visible = PLACEHOLDER_RE.sub("PLAYER7", payload).replace("$", "")
                for segment in CONTROL_RE.split(visible):
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        fail(f"{label}: {len(segment)}-char visible segment: {segment!r}")
    return raw


def body_span(source: str, label: str) -> tuple[int, int]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::?\n", source))
    if len(matches) != 1:
        fail(f"{label}: expected one label, found {len(matches)}")
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
        fail(f"{label}: no .string body found")
    return start, pos


def render(source: str, targets: dict[str, list[str]]) -> str:
    spans: list[tuple[int, int, str]] = []
    for label, payloads in targets.items():
        start, end = body_span(source, label)
        body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        spans.append((start, end, body))
    rendered = source
    for start, end, body in sorted(spans, reverse=True):
        rendered = rendered[:start] + body + rendered[end:]
    return rendered


def mask(source: str, labels: set[str]) -> str:
    rendered = source
    spans = [(body_span(source, label), label) for label in labels]
    for ((start, end), label) in sorted(spans, reverse=True):
        rendered = rendered[:start] + f'\t.string "<{label}>$"\n' + rendered[end:]
    return rendered


def validate(section: str, source: str, rendered: str, labels: set[str]) -> None:
    if mask(source, labels) != mask(rendered, labels):
        fail(f"{section}: non-owned Battle Tent structure changed")
    for token in GAMEPLAY_TOKENS[section]:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            fail(f"{section}: required gameplay token is absent: {token}")
        if before != after:
            fail(f"{section}: gameplay token count changed: {token}: {before} -> {after}")
    owned = "\n".join(
        rendered[body_span(rendered, label)[0]:body_span(rendered, label)[1]]
        for label in labels
    )
    for stale in ("SCOTT:", "FALLARBOR TOWN", "VERDANTURF TOWN"):
        if stale in owned:
            fail(f"{section}: stale visible identity survived: {stale}")
    if "SEU BENTO" not in owned:
        fail(f"{section}: SEU BENTO identity missing")
    if section == "ash_field" and "CAMPO DAS CINZAS" not in owned:
        fail("ash_field: canonical CAMPO DAS CINZAS identity missing")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Arauna side identity in the two reachable Battle Tents.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    for section, path in FILES.items():
        source = path.read_text(encoding="utf-8")
        rendered = render(source, bank[section])
        validate(section, source, rendered, EXPECTED[section])
        if args.in_place:
            path.write_text(rendered, encoding="utf-8")

    mode = "Rendered" if args.in_place else "Validated"
    print(f"{mode} Battle Tent side identity: 5 visible blocks across 2 maps.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

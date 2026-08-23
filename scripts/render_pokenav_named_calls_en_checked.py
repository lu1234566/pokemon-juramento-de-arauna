#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "pokenav_named_calls.json"
MATCH_CALL_PATH = ROOT / "data" / "text" / "match_call.inc"
STRINGS_PATH = ROOT / "src" / "strings.c"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

ELIAS_SUFFIXES = {
    "1": "Norman1",
    "2": "Norman2",
    "3": "Norman3",
    "4": "Norman4",
    "5": "Norman5",
    "preparing": "Norman_Preparing",
    "postgame": "Norman_PreparingPostGame",
    "ready": "Norman_RematchReady",
    "post_rematch": "Norman_PostRematch",
}
ANAHI_LABELS = {
    "register": "MatchCall_Text_BirchRegisterCall",
    "registered": "MatchCall_Text_RegisteredBirch",
}
LEADER_PREFIXES = ("Roxanne", "Brawly", "Wattson", "Flannery", "Winona", "TateLiza", "Juan")
LEADER_SUFFIXES = {
    "preparing": "Preparing",
    "postgame": "PreparingPostGame",
    "ready": "RematchReady",
    "post_rematch": "PostRematch",
}

EXPECTED_SECTIONS = {
    "otacilio",
    "elias",
    "anahi",
    "bento_steven",
    "ciro",
    "val",
    "bento_scott",
    "leaders",
}
EXPECTED_BLOCK_COUNT = 101

C_STRING_TARGETS = {
    "gText_MrStoneMatchCallDesc": "HORIZON DIRECTOR",
    "gText_MrStoneMatchCallName": "OTACILIO",
    "gText_StevenMatchCallDesc": "NAMEKEEPER",
    "gText_StevenMatchCallName": "SEU BENTO",
    "gText_MayBrendanMatchCallDesc": "FIELD RIVAL",
    "gText_NormanMatchCallDesc": "FATHER & LEADER",
    "gText_WallyMatchCallDesc": "OWN PACE",
    "gText_ScottMatchCallDesc": "FIELD NOTES",
    "gText_ScottMatchCallName": "SEU BENTO",
    "gText_RoxanneMatchCallDesc": "RIDGE WARDEN",
    "gText_BrawlyMatchCallDesc": "NET KEEPER",
    "gText_WattsonMatchCallDesc": "CROSSROADS",
    "gText_FlanneryMatchCallDesc": "ASH KEEPER",
    "gText_WinonaMatchCallDesc": "CANOPY WATCH",
    "gText_TateLizaMatchCallDesc": "SKY WITNESSES",
    "gText_JuanMatchCallDesc": "M'BOI ELDER",
    "gText_ProfBirchMatchCallDesc": "FIELD PROF.",
    "gText_ProfBirchMatchCallName": "PROF. ANAHI",
    "gText_HOFDexRating": "Spotted POKéMON: {STR_VAR_1}!\\nRecorded POKéMON: {STR_VAR_2}!\\pPROF. ANAHI's POKéDEX rating!\\pANAHI: Let's see...\\p",
    "gText_BirchInTrouble": "ANAHI is in trouble!\\nRelease a POKéMON and help her!",
}

STALE_BODY_RE = re.compile(
    r"(?:MR\. STONE|SCOTT:|STEVEN:|MAY:|BRENDAN:|WALLY:|NORMAN:|"
    r"ROXANNE:|BRAWLY:|WATTSON:|FLANNERY:|WINONA:|JUAN:|"
    r"TEAM MAGMA|TEAM AQUA|DEVON|HOENN|RUSTBORO|MAUVILLE|MOSSDEEP|SOOTOPOLIS)",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    raise ValueError(f"PokéNav named-call English renderer: {message}")


def payload_line_width(payload: str) -> None:
    visible = payload.replace("{PLAYER}", "PLAYER7")
    visible = re.sub(r"\{STR_VAR_[0-9]+\}", "VARIABLE10", visible)
    visible = PLACEHOLDER_RE.sub("TOKEN", visible).replace("$", "")
    for segment in CONTROL_RE.split(visible):
        if len(segment) > MAX_VISIBLE_WIDTH:
            fail(f"{len(segment)}-char visible segment: {segment!r}")


def validate_payload(label: str, payloads: list[str]) -> None:
    if not payloads or not all(isinstance(x, str) and x for x in payloads):
        fail(f"{label}: payload must be a non-empty string list")
    joined = "".join(payloads)
    if joined.count("$") != 1 or not joined.endswith("$"):
        fail(f"{label}: payload must contain exactly one final '$'")
    if STALE_BODY_RE.search(joined):
        fail(f"{label}: stale Emerald identity remains in English payload")
    for payload in payloads:
        if '"' in payload:
            fail(f"{label}: raw quote is not assembler-safe")
        payload_line_width(payload)


def load_bank() -> dict[str, object]:
    raw = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(raw) != EXPECTED_SECTIONS:
        fail(
            f"bank sections mismatch; missing={sorted(EXPECTED_SECTIONS - set(raw))}, "
            f"extra={sorted(set(raw) - EXPECTED_SECTIONS)}"
        )
    if set(raw["otacilio"]) != {str(i) for i in range(1, 12)}:
        fail("otacilio bank must contain calls 1..11")
    if set(raw["elias"]) != set(ELIAS_SUFFIXES):
        fail("elias bank contract mismatch")
    if set(raw["anahi"]) != set(ANAHI_LABELS):
        fail("anahi bank contract mismatch")
    if set(raw["bento_steven"]) != {str(i) for i in range(1, 8)}:
        fail("bento_steven bank must contain calls 1..7")
    if set(raw["ciro"]) != {str(i) for i in range(1, 16)}:
        fail("ciro bank must contain calls 1..15")
    if set(raw["val"]) != {str(i) for i in range(1, 8)}:
        fail("val bank must contain calls 1..7")
    if set(raw["bento_scott"]) != {str(i) for i in range(1, 8)}:
        fail("bento_scott bank must contain calls 1..7")
    leaders = raw["leaders"]
    if set(leaders) != set(LEADER_PREFIXES):
        fail("leader bank identity contract mismatch")
    for leader in LEADER_PREFIXES:
        if set(leaders[leader]) != set(LEADER_SUFFIXES):
            fail(f"{leader}: rematch-call contract mismatch")
    return raw


def build_targets(bank: dict[str, object]) -> dict[str, list[str]]:
    targets: dict[str, list[str]] = {}

    def add(label: str, payloads: list[str]) -> None:
        if label in targets:
            fail(f"duplicate generated target: {label}")
        validate_payload(label, payloads)
        targets[label] = payloads

    for number, payloads in bank["otacilio"].items():
        add(f"MatchCall_Text_MrStone{number}", payloads)
    for key, suffix in ELIAS_SUFFIXES.items():
        add(f"MatchCall_Text_{suffix}", bank["elias"][key])
    for key, label in ANAHI_LABELS.items():
        add(label, bank["anahi"][key])
    for number, payloads in bank["bento_steven"].items():
        add(f"MatchCall_Text_Steven{number}", payloads)
    for number, payloads in bank["ciro"].items():
        add(f"MatchCall_Text_May{number}", payloads)
        add(f"MatchCall_Text_Brendan{number}", payloads)
    for number, payloads in bank["val"].items():
        add(f"MatchCall_Text_Wally{number}", payloads)
    for number, payloads in bank["bento_scott"].items():
        add(f"MatchCall_Text_Scott{number}", payloads)
    for leader in LEADER_PREFIXES:
        for key, suffix in LEADER_SUFFIXES.items():
            add(f"MatchCall_Text_{leader}_{suffix}", bank["leaders"][leader][key])

    if len(targets) != EXPECTED_BLOCK_COUNT:
        fail(f"expected {EXPECTED_BLOCK_COUNT} generated blocks, found {len(targets)}")
    return targets


def asm_body_span(source: str, label: str) -> tuple[int, int]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::?\n", source))
    if len(matches) != 1:
        fail(f"{label}: expected one label, found {len(matches)}")
    start = matches[0].end()
    pos = start
    saw_string = False
    while pos < len(source):
        newline = source.find("\n", pos)
        end = len(source) if newline < 0 else newline + 1
        line = source[pos:end]
        if line.lstrip(" \t").startswith(".string "):
            saw_string = True
            pos = end
            continue
        break
    if not saw_string:
        fail(f"{label}: no .string body")
    return start, pos


def render_asm(source: str, targets: dict[str, list[str]]) -> str:
    spans: list[tuple[int, int, str]] = []
    for label, payloads in targets.items():
        start, end = asm_body_span(source, label)
        body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        spans.append((start, end, body))
    rendered = source
    for start, end, body in sorted(spans, reverse=True):
        rendered = rendered[:start] + body + rendered[end:]
    return rendered


def mask_asm(source: str, targets: dict[str, list[str]]) -> str:
    rendered = source
    spans = [(asm_body_span(source, label), label) for label in targets]
    for ((start, end), label) in sorted(spans, reverse=True):
        rendered = rendered[:start] + f'\t.string "<{label}>$"\n' + rendered[end:]
    return rendered


def validate_asm(source: str, rendered: str, targets: dict[str, list[str]]) -> None:
    if mask_asm(source, targets) != mask_asm(rendered, targets):
        fail("non-owned Match Call text structure changed")
    for label in targets:
        start, end = asm_body_span(rendered, label)
        body = rendered[start:end]
        if STALE_BODY_RE.search(body):
            fail(f"{label}: stale visible Emerald identity survived")


def c_symbol_pattern(symbol: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?m)^(?P<prefix>(?:ALIGNED\(4\)\s+)?const u8 {re.escape(symbol)}\[\]\s*=\s*_\(")'
        rf'(?P<body>(?:[^"\\]|\\.)*)'
        rf'(?P<suffix>"\);(?:\s*//[^\n]*)?$)'
    )


def render_c_strings(source: str) -> str:
    rendered = source
    for symbol, final in C_STRING_TARGETS.items():
        pattern = c_symbol_pattern(symbol)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            fail(f"{symbol}: expected one C string definition, found {len(matches)}")
        match = matches[0]
        rendered = rendered[:match.start("body")] + final + rendered[match.end("body"):]
    return rendered


def mask_c_strings(source: str) -> str:
    rendered = source
    for symbol in C_STRING_TARGETS:
        pattern = c_symbol_pattern(symbol)
        match = pattern.search(rendered)
        if match is None:
            fail(f"{symbol}: cannot mask C string")
        rendered = rendered[:match.start("body")] + f"<{symbol}>" + rendered[match.end("body"):]
    return rendered


def validate_c_strings(source: str, rendered: str) -> None:
    if mask_c_strings(source) != mask_c_strings(rendered):
        fail("non-owned src/strings.c structure changed")
    for symbol, expected in C_STRING_TARGETS.items():
        match = c_symbol_pattern(symbol).search(rendered)
        if match is None or match.group("body") != expected:
            fail(f"{symbol}: final English UI value mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Arauna named-character PokéNav calls and Match Call UI in English."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    targets = build_targets(bank)

    asm_source = MATCH_CALL_PATH.read_text(encoding="utf-8")
    asm_rendered = render_asm(asm_source, targets)
    validate_asm(asm_source, asm_rendered, targets)

    c_source = STRINGS_PATH.read_text(encoding="utf-8")
    c_rendered = render_c_strings(c_source)
    validate_c_strings(c_source, c_rendered)

    if args.in_place:
        MATCH_CALL_PATH.write_text(asm_rendered, encoding="utf-8")
        STRINGS_PATH.write_text(c_rendered, encoding="utf-8")

    mode = "Rendered" if args.in_place else "Validated"
    print(
        f"{mode} Arauna PokéNav named calls: {len(targets)} dialogue blocks and "
        f"{len(C_STRING_TARGETS)} UI strings."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

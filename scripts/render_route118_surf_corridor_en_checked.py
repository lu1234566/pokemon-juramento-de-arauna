#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "text" / "arauna" / "en" / "route118_surf_corridor.json"
TARGET = ROOT / "data" / "maps" / "Route118" / "scripts.inc"
EXPECTED_COUNT = 9
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

RAW_MARKERS: dict[str, tuple[str, ...]] = {
    "Route118_Text_StevenQuestions": ("SEU BENTO:", "Quando um nome"),
    "Route118_Text_YouAgreeGoodRodIsGood": ("GOOD ROD", "Wouldn't you agree"),
    "Route118_Text_IdenticalMindsTakeThis": ("identical minds", "GOOD ROD"),
    "Route118_Text_TryYourLuckFishing": ("Wherever there's water",),
    "Route118_Text_DontYouLikeToFish": ("Don't you like to fish",),
    "Route118_Text_TryCatchingMonWithGoodRod": ("GOOD ROD",),
    "Route118_Text_CanCrossRiversWithSurf": ("SURF", "cross rivers"),
    "Route118_Text_RouteSignMauville": ("ROUTE 118", "MAUVILLE CITY"),
    "Route118_Text_RouteSign119": ("ROUTE 118", "ROUTE 119"),
}

CRITICAL_TOKENS = (
    "ITEM_GOOD_ROD",
    "FLAG_RECEIVED_GOOD_ROD",
    "VAR_ROUTE118_STATE",
    "LOCALID_ROUTE118_STEVEN",
    "VAR_ABNORMAL_WEATHER_LOCATION",
    "ABNORMAL_WEATHER_ROUTE_118_EAST",
    "ABNORMAL_WEATHER_ROUTE_118_WEST",
    "TRAINER_ROSE_1",
    "TRAINER_DALTON_1",
    "register_matchcall TRAINER_ROSE_1",
    "register_matchcall TRAINER_DALTON_1",
)

STALE_VISIBLE = (
    "MAUVILLE CITY",
    "Quando um nome",
    "Nao para",
    "escrevo.",
)


def load_bank() -> dict[str, tuple[str, ...]]:
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or len(raw) != EXPECTED_COUNT:
        raise ValueError(f"expected exactly {EXPECTED_COUNT} Route 118 labels")
    if set(raw) != set(RAW_MARKERS):
        missing = sorted(set(RAW_MARKERS) - set(raw))
        extra = sorted(set(raw) - set(RAW_MARKERS))
        raise ValueError(f"Route 118 label contract mismatch; missing={missing}, extra={extra}")

    bank: dict[str, tuple[str, ...]] = {}
    for label, payloads in raw.items():
        if not isinstance(payloads, list) or not payloads:
            raise ValueError(f"{label}: expected non-empty payload list")
        converted = tuple(str(payload) for payload in payloads)
        if any('"' in payload for payload in converted):
            raise ValueError(f"{label}: raw double quote is not allowed")
        if any("$" in payload for payload in converted[:-1]):
            raise ValueError(f"{label}: terminator may appear only in final payload")
        if not converted[-1].endswith("$"):
            raise ValueError(f"{label}: final payload must end with $")
        bank[label] = converted
    return bank


def block_pattern(label: str) -> re.Pattern[str]:
    # Route 118 still contains historical assembler backslash-newline continuations.
    # Own only consecutive .string records plus their physical continuation lines.
    return re.compile(
        rf"(?m)^{re.escape(label)}:\n"
        rf"(?P<body>(?:\t\.string [^\n]*\n"
        rf"(?:^(?!\t|[A-Za-z0-9_]+:|\s*$)[^\n]*\n)*)+)"
    )


def replacement(payloads: tuple[str, ...]) -> str:
    return "".join(f'\t.string "{payload}"\n' for payload in payloads)


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("{LEFT_ARROW}", "<").replace("{UP_ARROW}", "^")
    cleaned = PLACEHOLDER_RE.sub("LONGPHRASE123456", cleaned).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths(bank: dict[str, tuple[str, ...]]) -> None:
    for label, payloads in bank.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(
                        f"{label}: visible segment is {len(segment)} chars, max {MAX_VISIBLE_WIDTH}: {segment!r}"
                    )


def mask_targets(text: str, labels: tuple[str, ...]) -> str:
    masked = text
    for label in labels:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ROUTE118_SURF_BLOCK>"\n' + masked[end:]
    return masked


def render(source: str, bank: dict[str, tuple[str, ...]]) -> str:
    rendered = source
    before_counts = {token: source.count(token) for token in CRITICAL_TOKENS}

    for label, payloads in bank.items():
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

    labels = tuple(bank)
    if mask_targets(source, labels) != mask_targets(rendered, labels):
        raise ValueError("Route 118 non-dialogue structure changed")

    after_counts = {token: rendered.count(token) for token in CRITICAL_TOKENS}
    if before_counts != after_counts:
        raise ValueError(f"Route 118 progression token counts changed: {before_counts} -> {after_counts}")

    for label, payloads in bank.items():
        body = block_pattern(label).search(rendered).group("body")
        if body != replacement(payloads):
            raise ValueError(f"{label}: rendered body does not match reviewed bank")
        for token in STALE_VISIBLE:
            if token in body:
                raise ValueError(f"{label}: stale visible token survived: {token!r}")
    return rendered


def validate_identity(bank: dict[str, tuple[str, ...]]) -> None:
    joined = "\n".join(payload for payloads in bank.values() for payload in payloads)
    for required in ("SEU BENTO", "SURF", "GOOD ROD", "ENCRUZILHADA CENTRAL", "MATA DO MEIO"):
        if required not in joined:
            raise ValueError(f"required Route 118 identity missing: {required}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render the Route 118 post-SURF corridor in English without changing Emerald progression."
    )
    parser.add_argument("--input", type=Path, default=TARGET)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.output and args.in_place:
        parser.error("use either --output or --in-place, not both")
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    validate_widths(bank)
    validate_identity(bank)
    source = args.input.read_text(encoding="utf-8")
    rendered = render(source, bank)

    if args.check:
        print(f"Route 118 SURF corridor English renderer OK: {len(bank)} blocks validated.")
        return 0
    if args.in_place:
        args.input.write_text(rendered, encoding="utf-8")
        return 0
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

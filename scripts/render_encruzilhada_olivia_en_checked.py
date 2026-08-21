#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "text" / "arauna" / "en" / "encruzilhada_core.json"
FILES = {
    "city": ROOT / "data" / "maps" / "MauvilleCity" / "scripts.inc",
    "gym": ROOT / "data" / "maps" / "MauvilleCity_Gym" / "scripts.inc",
}
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")
BLOCK_RE_TEMPLATE = r"(?m)^{label}:\n(?P<body>(?:\t\.string .*\n)+)"

CRITICAL_TOKENS = {
    "city": (
        "TRAINER_WALLY_MAUVILLE",
        "FLAG_DEFEATED_WALLY_MAUVILLE",
        "FLAG_ENABLE_WALLY_MATCH_CALL",
        "VAR_SCOTT_STATE",
        "ITEM_BASEMENT_KEY",
        "FLAG_GOT_BASEMENT_KEY_FROM_WATTSON",
        "ITEM_TM_THUNDERBOLT",
        "FLAG_GOT_TM_THUNDERBOLT_FROM_WATTSON",
        "VAR_NEW_MAUVILLE_STATE",
    ),
    "gym": (
        "TRAINER_WATTSON_1",
        "FLAG_DEFEATED_MAUVILLE_GYM",
        "FLAG_BADGE03_GET",
        "ITEM_TM_SHOCK_WAVE",
        "FLAG_RECEIVED_TM_SHOCK_WAVE",
        "FLAG_ENABLE_WATTSON_MATCH_CALL",
        "VAR_MAUVILLE_GYM_STATE",
        "FLAG_MAUVILLE_GYM_BARRIERS_STATE",
    ),
}

STALE_VISIBLE = (
    "WALLY",
    "WATTSON",
    "MAUVILLE",
    "RYDEL",
    "DYNAMO BADGE",
    "INSÍGNIA",
    "RESPONSAVEL",
    "HORIZONTE",
    "Passei muito",
    "Eu ainda",
    "Energia move",
)


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(BLOCK_RE_TEMPLATE.format(label=re.escape(label)))


def load_data() -> dict[str, dict[str, tuple[str, ...]]]:
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    if set(raw) != set(FILES):
        raise ValueError(f"expected data sections {sorted(FILES)}, got {sorted(raw)}")
    out: dict[str, dict[str, tuple[str, ...]]] = {}
    for section, entries in raw.items():
        if not isinstance(entries, dict) or not entries:
            raise ValueError(f"{section}: expected non-empty object")
        out[section] = {}
        for label, payloads in entries.items():
            if not isinstance(payloads, list) or not payloads:
                raise ValueError(f"{label}: expected non-empty payload list")
            values = tuple(str(x) for x in payloads)
            for i, payload in enumerate(values):
                if '"' in payload:
                    raise ValueError(f"{label}: raw double quote is not allowed")
                if "$" in payload and (i != len(values) - 1 or not payload.endswith("$")):
                    raise ValueError(f"{label}: terminator $ may appear only at final payload end")
            if not values[-1].endswith("$"):
                raise ValueError(f"{label}: final payload must end with $")
            out[section][label] = values
    return out


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("LONGPHRASE123456", payload).replace("$", "")
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_widths(data: dict[str, dict[str, tuple[str, ...]]]) -> None:
    for section, entries in data.items():
        for label, payloads in entries.items():
            for payload in payloads:
                for segment in visible_segments(payload):
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(
                            f"{section}/{label}: {len(segment)} visible chars: {segment!r}"
                        )


def replacement(payloads: tuple[str, ...]) -> str:
    return "".join(f'\t.string "{payload}"\n' for payload in payloads)


def mask_targets(source: str, entries: dict[str, tuple[str, ...]]) -> str:
    masked = source
    for label in entries:
        matches = list(block_pattern(label).finditer(masked))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected one block while masking, found {len(matches)}")
        start, end = matches[0].span("body")
        masked = masked[:start] + '\t.string "<ENCRUZILHADA_BLOCK>"\n' + masked[end:]
    return masked


def render_section(section: str, source: str, entries: dict[str, tuple[str, ...]]) -> str:
    before = {token: source.count(token) for token in CRITICAL_TOKENS[section]}
    rendered = source
    for label, payloads in entries.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{section}/{label}: expected exactly one .string block, found {len(matches)}")
        start, end = matches[0].span("body")
        rendered = rendered[:start] + replacement(payloads) + rendered[end:]

    if mask_targets(source, entries) != mask_targets(rendered, entries):
        raise ValueError(f"{section}: non-dialogue structure changed")

    after = {token: rendered.count(token) for token in CRITICAL_TOKENS[section]}
    if before != after:
        raise ValueError(f"{section}: progression token counts changed: {before} -> {after}")

    for label in entries:
        body = block_pattern(label).search(rendered).group("body")
        for token in STALE_VISIBLE:
            if token in body:
                raise ValueError(f"{section}/{label}: stale visible token survived: {token!r}")
    return rendered


def validate_identity(rendered: dict[str, str]) -> None:
    city = rendered["city"]
    gym = rendered["gym"]
    for label in (
        "MauvilleCity_Text_WallyWantToChallengeGym",
        "MauvilleCity_Text_WallyDefeat",
        "MauvilleCity_Text_WallyPokenavCall",
    ):
        if "VAL:" not in block_pattern(label).search(city).group("body"):
            raise ValueError(f"{label}: VAL identity missing")
    for label in (
        "MauvilleCity_Gym_Text_WattsonIntro",
        "MauvilleCity_Gym_Text_WattsonDefeat",
        "MauvilleCity_Gym_Text_WattsonPostBattle",
    ):
        if "OLIVIA:" not in block_pattern(label).search(gym).group("body"):
            raise ValueError(f"{label}: OLIVIA identity missing")
    badge = block_pattern("MauvilleCity_Gym_Text_ReceivedDynamoBadge").search(gym).group("body")
    if "BEACON BADGE" not in badge:
        raise ValueError("visible third badge must be BEACON BADGE")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Encruzilhada Central, Val and Olivia English surfaces.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    data = load_data()
    validate_widths(data)
    rendered: dict[str, str] = {}
    for section, path in FILES.items():
        source = path.read_text(encoding="utf-8")
        rendered[section] = render_section(section, source, data[section])
    validate_identity(rendered)

    if args.check:
        total = sum(len(v) for v in data.values())
        print(f"Encruzilhada English renderer OK: {total} blocks across {len(FILES)} map files.")
        return 0
    if args.in_place:
        for section, path in FILES.items():
            path.write_text(rendered[section], encoding="utf-8")
        return 0

    for section in FILES:
        print(f"===== {section} =====")
        print(rendered[section], end="" if rendered[section].endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

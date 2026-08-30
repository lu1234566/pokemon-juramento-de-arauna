#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "maps" / "SlateportCity" / "scripts.inc"
DATA = ROOT / "data" / "text" / "arauna" / "en" / "porto_sal_path.json"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

MARKERS: dict[str, tuple[str, ...]] = {
    "SlateportCity_Text_BattleTentSign": ("BATTLE TENT PORTO DO SAL SITE",),
    "SlateportCity_Text_SternsShipyardWantedSign": ("STERN'S SHIPYARD", "Wanted"),
    "SlateportCity_Text_SternsShipyardNearsCompletion": ("S.S. TIDAL", "PORTO DO SAL", "BAIA DAS LUZES"),
    "SlateportCity_Text_SternsShipyardFerryComplete": ("PORTO DO SAL-BAIA DAS LUZES", "S.S. TIDAL"),
    "SlateportCity_Text_PokemonFanClubSign": ("POKéMON FAN CLUB",),
    "SlateportCity_Text_OceanicMuseumSign": ("OCEANIC MUSEUM",),
    "SlateportCity_Text_CitySign": ("ARQUIVO VIVO", "DESENCANTO"),
    "SlateportCity_Text_MarketSign": ("PORTO DO SAL MARKET",),
    "SlateportCity_Text_HarborFerryUnderConstruction": ("PORTO DO SAL HARBOR", "S.S. TIDAL"),
    "SlateportCity_Text_HarborSign": ("PORTO DO SAL HARBOR", "S.S. TIDAL"),
    "SlateportCity_Text_NameRatersHouseSign": ("NAME RATER'S HOUSE",),
    "SlateportCity_Text_YouDroveTeamAquaAway": ("HORIZONTE: Nao somos soldados",),
    "SlateportCity_Text_MaybeThisTrainer": ("CIRO:", "HORIZONTE"),
    "SlateportCity_Text_LetsRegisterEachOther": ("SCOTT:", "POKéNAVS"),
    "SlateportCity_Text_RegisteredScott": ("SCOTT", "POKéNAV"),
    "SlateportCity_Text_KeepEyeOnTrainersBeSeeingYou": ("SCOTT:", "other towns"),
    "SlateportCity_Text_TakingBattleTentChallenge": ("SCOTT:", "BATTLE TENT"),
}

CRITICAL_TOKENS = (
    "VAR_SCOTT_STATE",
    "FLAG_ENABLE_SCOTT_MATCH_CALL",
    "FLAG_DELIVERED_DEVON_GOODS",
    "LOCALID_SLATEPORT_SCOTT",
)

STALE_TOKENS = (
    "SLATEPORT",
    "LILYCOVE",
    "S.S. TIDAL",
    "STERN'S SHIPYARD",
    "OCEANIC MUSEUM",
    "SCOTT:",
    "CONSORCIO HORIZONTE",
    "HORIZONTE:",
    "Voce ",
    "Nao ",
)


def load_targets() -> dict[str, tuple[str, ...]]:
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    targets: dict[str, tuple[str, ...]] = {}
    for section, entries in raw.items():
        if not isinstance(entries, dict):
            raise ValueError(f"{section}: expected object")
        for label, payloads in entries.items():
            if label in targets:
                raise ValueError(f"duplicate target label: {label}")
            if not isinstance(payloads, list) or not payloads:
                raise ValueError(f"{label}: expected non-empty payload list")
            targets[label] = tuple(str(payload) for payload in payloads)
    if set(targets) != set(MARKERS):
        missing = sorted(set(MARKERS) - set(targets))
        extra = sorted(set(targets) - set(MARKERS))
        raise ValueError(f"target contract mismatch; missing={missing}, extra={extra}")
    return targets


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?m)^{re.escape(label)}:\n(?P<body>(?:\t\.string .*\n)+)")


def visible_segments(payload: str) -> list[str]:
    cleaned = PLACEHOLDER_RE.sub("PLAYER", payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, tuple[str, ...]]) -> None:
    for label, payloads in targets.items():
        for payload in payloads:
            for segment in visible_segments(payload):
                if len(segment) > MAX_VISIBLE_WIDTH:
                    raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def mask_targets(text: str, targets: dict[str, tuple[str, ...]]) -> str:
    masked = text
    for label in targets:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing .string block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<PORTO_SAL_PATH_BLOCK>"\n' + masked[end:]
    return masked


def render(source: str) -> str:
    targets = load_targets()
    validate_widths(targets)
    rendered = source
    critical_before = {token: source.count(token) for token in CRITICAL_TOKENS}

    for label, payloads in targets.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected exactly one string block, found {len(matches)}")
        body = matches[0].group("body")
        for marker in MARKERS[label]:
            if marker not in body:
                raise ValueError(f"{label}: source marker missing: {marker!r}")
        replacement = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        start, end = matches[0].span("body")
        rendered = rendered[:start] + replacement + rendered[end:]

    if mask_targets(source, targets) != mask_targets(rendered, targets):
        raise ValueError("non-dialogue structure changed while rendering Porto do Sal story path")

    critical_after = {token: rendered.count(token) for token in CRITICAL_TOKENS}
    if critical_before != critical_after:
        raise ValueError(f"progression token counts changed: {critical_before} -> {critical_after}")

    for label in targets:
        body = block_pattern(label).search(rendered).group("body")
        for token in STALE_TOKENS:
            if token in body:
                raise ValueError(f"{label}: stale visible token survived: {token!r}")

    registered = block_pattern("SlateportCity_Text_RegisteredScott").search(rendered).group("body")
    if "SEU BENTO's field route" not in registered:
        raise ValueError("Scott registration surface no longer explains Bento's second POKéNAV channel")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Porto do Sal mandatory story-path signs and Seu Bento scene in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    source = TARGET.read_text(encoding="utf-8")
    rendered = render(source)
    if args.check:
        print(f"Porto do Sal story-path renderer OK: {len(load_targets())} blocks validated.")
        return 0
    if args.in_place:
        TARGET.write_text(rendered, encoding="utf-8")
        return 0
    print(rendered, end="" if rendered.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

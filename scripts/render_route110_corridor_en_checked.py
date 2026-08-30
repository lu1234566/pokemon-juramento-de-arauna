#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "text" / "arauna" / "en" / "route110_corridor.json"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

FILES = {
    "route": ROOT / "data" / "maps" / "Route110" / "scripts.inc",
    "south_gate": ROOT / "data" / "maps" / "Route110_SeasideCyclingRoadSouthEntrance" / "scripts.inc",
    "north_gate": ROOT / "data" / "maps" / "Route110_SeasideCyclingRoadNorthEntrance" / "scripts.inc",
}

MARKERS = {'Route110_Text_WeCantTalkAboutAquaActivities': ("CONSORCIO HORIZONTE's activities",), 'Route110_Text_KickUpARuckus': ('kick up a ruckus',), 'Route110_Text_MyFirstJobInAqua': ('first job after joining',), 'Route110_Text_AquaActionsBringSmiles': ("smiles to people's faces",), 'Route110_Text_MayLetsBattle': ('Voce continua olhando',), 'Route110_Text_MayDefeated': ('Nao confunda minha pressa',), 'Route110_Text_MayTakeThis': ('Voce continua olhando',), 'Route110_Text_MayExplainItemfinder': ('Isso e um ITEMFINDER',), 'Route110_Text_BrendanLetsBattle': ('Voce continua olhando',), 'Route110_Text_BrendanDefeated': ('Voce continua olhando',), 'Route110_Text_BrendanTakeThis': ('O HORIZONTE nao me pediu',), 'Route110_Text_BrendanExplainItemfinder': ('Isso e um ITEMFINDER',), 'Route110_Text_RideBikeAtFullSpeed': ('ride a BIKE',), 'Route110_Text_HairStreamsBehindMe': ('raven-',), 'Route110_Text_YouGotBikeFromRydel': ('RYDEL!',), 'Route110_Text_TwoRoads': ('two roads',), 'Route110_Text_WalkOnTheLowRoad': ('leisurely walk',), 'Route110_Text_BikeTechniques': ('BIKE technique',), 'Route110_Text_WhichShouldIChoose': ('Make a beeline for ENCRUZILHADA',), 'Route110_Text_CyclingChallengeResultSummary': ('Number of collisions',), 'Route110_Text_ChallengeReactionBest': ('Bravo! Splendid',), 'Route110_Text_ChallengeReactionGood': ('technique is remarkable',), 'Route110_Text_ChallengeReactionOk': ('work in',), 'Route110_Text_ChallengeReactionBad': ('border',), 'Route110_Text_ChallengeReactionWorst': ('aghast',), 'Route110_Text_RatedForNumberOfCollisions': ('rated for the number of collisions',), 'Route110_Text_AlwaysAimHigher': ('Always aim higher',), 'Route110_Text_AcroBikesDoNotQualify': ('ACRO BIKES do not qualify',), 'Route110_Text_SlateportCitySign': ('ROUTE110. As estradas',), 'Route110_Text_CyclingRoadSign': ('SEASIDE CYCLING ROAD',), 'Route110_Text_AquaWasHere': ('LEMBRANTES rules!',), 'Route110_Text_Route103Sign': ('{LEFT_ARROW} ROUTE 103',), 'Route110_Text_SeasideParkingSign': ('SEASIDE PARKING',), 'Route110_Text_MauvilleCitySign': ('ROUTE110. As estradas',), 'Route110_Text_TrainerTipsPrlzSleep': ('paralyzing it',), 'Route110_Text_TrainerTipsRegisterItems': ('pressing SELECT',), 'Route110_Text_TrickHouseSign': ('TRICK HOUSE',), 'Route110_Text_BestRecord': ('THE BEST RECORD TO DATE',), 'Route110_Text_ThereIsNoRecord': ('There is no record',), 'Route110_Text_ImagineSeeingYouHere': ('Se eu continuar calada',), 'Route110_Text_HeardYouInstallMatchCall': ('POKéDEX anytime',), 'Route110_Text_RegisteredBirchInPokenav': ('PROF. ANAHI',), 'Route110_Text_KeepAnEyeOutForRival': ('primeiros sensores de VINCULO',), 'Route110_SeasideCyclingRoadSouthEntrance_Text_GoAllOutOnCyclingRoad': ('go all out',), 'Route110_SeasideCyclingRoadSouthEntrance_Text_TooDangerousToWalk': ('too dangerous',), 'Route110_SeasideCyclingRoadNorthEntrance_Text_GoAllOutOnCyclingRoad': ('go all out',), 'Route110_SeasideCyclingRoadNorthEntrance_Text_TooDangerousToWalk': ('too dangerous',)}

CRITICAL_TOKENS = {
    "route": (
        "ITEM_ITEMFINDER",
        "VAR_ROUTE110_STATE",
        "FLAG_ENABLE_PROF_BIRCH_MATCH_CALL",
        "VAR_REGISTER_BIRCH_STATE",
        "VAR_CYCLING_CHALLENGE_STATE",
        "TRAINER_MAY_ROUTE_110_TREECKO",
        "TRAINER_BRENDAN_ROUTE_110_TREECKO",
    ),
    "south_gate": ("FLAG_SYS_CYCLING_ROAD", "VAR_TEMP_1"),
    "north_gate": ("FLAG_SYS_CYCLING_ROAD", "VAR_TEMP_1", "VAR_CYCLING_CHALLENGE_STATE"),
}

STALE_TOKENS = (
    "CONSORCIO HORIZONTE",
    "SLATEPORT",
    "MAUVILLE",
    "RYDEL",
    "SEASIDE CYCLING ROAD",
    "LEMBRANTES rules!",
    "Voce ",
    "Nao ",
    "Isso e ",
    "Se eu ",
    "sensores de VINCULO",
)

CIRO_PAIRS = (
    ("Route110_Text_MayLetsBattle", "Route110_Text_BrendanLetsBattle"),
    ("Route110_Text_MayDefeated", "Route110_Text_BrendanDefeated"),
    ("Route110_Text_MayTakeThis", "Route110_Text_BrendanTakeThis"),
    ("Route110_Text_MayExplainItemfinder", "Route110_Text_BrendanExplainItemfinder"),
)


def load_targets() -> dict[str, dict[str, tuple[str, ...]]]:
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    if set(raw) != set(FILES):
        raise ValueError(f"section contract mismatch: expected {sorted(FILES)}, found {sorted(raw)}")
    targets: dict[str, dict[str, tuple[str, ...]]] = {}
    seen: set[str] = set()
    for section, entries in raw.items():
        if not isinstance(entries, dict):
            raise ValueError(f"{section}: expected object")
        targets[section] = {}
        for label, payloads in entries.items():
            if label in seen:
                raise ValueError(f"duplicate label across sections: {label}")
            seen.add(label)
            if not isinstance(payloads, list) or not payloads:
                raise ValueError(f"{label}: expected non-empty payload list")
            targets[section][label] = tuple(str(payload) for payload in payloads)
    if seen != set(MARKERS):
        missing = sorted(set(MARKERS) - seen)
        extra = sorted(seen - set(MARKERS))
        raise ValueError(f"target contract mismatch; missing={missing}, extra={extra}")
    flat = {label: payloads for entries in targets.values() for label, payloads in entries.items()}
    for left, right in CIRO_PAIRS:
        if flat[left] != flat[right]:
            raise ValueError(f"Ciro gender-slot surfaces diverged: {left} != {right}")
    return targets


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?m)^{re.escape(label)}:\n(?P<body>(?:\t\.string .*\n)+)")


def visible_segments(payload: str) -> list[str]:
    # 16 chars is deliberately conservative for dynamic STR_VAR values.
    cleaned = PLACEHOLDER_RE.sub("X" * 16, payload).replace("$", "")
    return [segment.strip() for segment in CONTROL_RE.split(cleaned)]


def validate_widths(targets: dict[str, dict[str, tuple[str, ...]]]) -> None:
    for entries in targets.values():
        for label, payloads in entries.items():
            for payload in payloads:
                for segment in visible_segments(payload):
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(f"{label}: {len(segment)} visible chars: {segment!r}")


def mask_targets(text: str, labels: tuple[str, ...]) -> str:
    masked = text
    for label in labels:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{label}: cannot mask missing .string block")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<ROUTE110_CORRIDOR_BLOCK>"\n' + masked[end:]
    return masked


def render_file(section: str, source: str, entries: dict[str, tuple[str, ...]]) -> str:
    rendered = source
    before = {token: source.count(token) for token in CRITICAL_TOKENS[section]}
    for label, payloads in entries.items():
        matches = list(block_pattern(label).finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{label}: expected exactly one string block, found {len(matches)}")
        body = matches[0].group("body")
        replacement = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        has_source_markers = all(marker in body for marker in MARKERS[label])
        if body == replacement:
            continue
        if not has_source_markers:
            missing = [marker for marker in MARKERS[label] if marker not in body]
            raise ValueError(f"{label}: neither source nor rendered contract matched; missing markers={missing}")
        start, end = matches[0].span("body")
        rendered = rendered[:start] + replacement + rendered[end:]

    labels = tuple(entries)
    if mask_targets(source, labels) != mask_targets(rendered, labels):
        raise ValueError(f"{section}: non-dialogue structure changed")

    after = {token: rendered.count(token) for token in CRITICAL_TOKENS[section]}
    if before != after:
        raise ValueError(f"{section}: progression token counts changed: {before} -> {after}")

    for label in labels:
        body = block_pattern(label).search(rendered).group("body")
        for token in STALE_TOKENS:
            if token in body:
                raise ValueError(f"{label}: stale visible token survived: {token!r}")
    return rendered


def render_all() -> dict[str, str]:
    targets = load_targets()
    validate_widths(targets)
    rendered: dict[str, str] = {}
    for section, path in FILES.items():
        rendered[section] = render_file(section, path.read_text(encoding="utf-8"), targets[section])
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Route 110 Porto do Sal-to-Encruzilhada corridor in English.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    rendered = render_all()
    if args.check:
        count = sum(len(entries) for entries in load_targets().values())
        print(f"Route 110 corridor renderer OK: {count} blocks across {len(FILES)} files.")
        return 0
    if args.in_place:
        for section, path in FILES.items():
            path.write_text(rendered[section], encoding="utf-8")
        return 0
    for section in FILES:
        print(f"@@ {FILES[section].relative_to(ROOT)}")
        print(rendered[section], end="" if rendered[section].endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

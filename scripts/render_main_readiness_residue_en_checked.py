#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "main_readiness_residue.json"
CAVE_PATH = ROOT / "data" / "maps" / "CaveOfOrigin_B1F" / "scripts.inc"
ROUTE119_HOUSE_PATH = ROOT / "data" / "maps" / "Route119_House" / "scripts.inc"
ROUTE105_PATH = ROOT / "data" / "maps" / "Route105" / "scripts.inc"
ABANDONED_OFFICE_PATH = ROOT / "data" / "maps" / "AbandonedShip_CaptainsOffice" / "scripts.inc"
MENU_PATH = ROOT / "src" / "data" / "script_menu.h"
LANDMARK_PATH = ROOT / "src" / "landmark.c"
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

EXPECTED = {
    "cave_of_origin": {
        "CaveOfOrigin_B1F_Text_WallaceStory",
        "CaveOfOrigin_B1F_Text_WhereIsRayquaza",
        "CaveOfOrigin_B1F_Text_ButWereInCaveOfOrigin",
        "CaveOfOrigin_B1F_Text_OldLadyDidntMentionThat",
        "CaveOfOrigin_B1F_Text_CantYouRememberSomehow",
        "CaveOfOrigin_B1F_Text_WellHeadToSkyPillar",
    },
    "route119_house": {"Route119_House_Text_RumorAboutCaveOfOrigin"},
    "route105_pokenav": {
        "Route104_Text_DadPokenavCall",
        "Route104_Text_RegisteredDadInPokenav",
    },
    "abandoned_ship_office": {
        "AbandonedShip_CaptainsOffice_Text_NoSuccessFindingScanner",
        "AbandonedShip_CaptainsOffice_Text_OhCanYouDeliverScanner",
    },
}
FILES = {
    "cave_of_origin": CAVE_PATH,
    "route119_house": ROUTE119_HOUSE_PATH,
    "route105_pokenav": ROUTE105_PATH,
    "abandoned_ship_office": ABANDONED_OFFICE_PATH,
}
GAMEPLAY_TOKENS = {
    "cave_of_origin": (
        "MULTI_WHERES_RAYQUAZA",
        "FLAG_WALLACE_GOES_TO_SKY_PILLAR",
        "VAR_SOOTOPOLIS_CITY_STATE",
        "LOCALID_CAVE_OF_ORIGIN_WALLACE",
        "CaveOfOrigin_B1F_EventScript_AtSkyPillar",
    ),
    "route119_house": (
        "Route119_House_EventScript_Woman",
        "Route119_House_EventScript_Wingull",
        "SPECIES_WINGULL",
    ),
    "route105_pokenav": (
        "Route105_OnLoad",
        "Route105_OnTransition",
        "Route105_OnFrame",
        "TRAINER_ANDRES_1",
        "register_matchcall TRAINER_ANDRES_1",
    ),
    "abandoned_ship_office": (
        "FLAG_EXCHANGED_SCANNER",
        "ITEM_SCANNER",
        "FLAG_ITEM_ABANDONED_SHIP_HIDDEN_FLOOR_ROOM_2_SCANNER",
        "AbandonedShip_CaptainsOffice_EventScript_CanYouDeliverScanner",
    ),
}
STALE = (
    "WALLACE",
    "JUAN",
    "SOOTOPOLIS",
    "GROUDON",
    "KYOGRE",
    "RAYQUAZA",
    "CAVE OF ORIGIN",
    "MT. PYRE",
    "SKY PILLAR",
    "NORMAN",
    "MR. STONE",
    "DEVON",
    "CAPT. STERN",
)

ORIGINAL_MENU = '''static const struct MenuAction MultichoiceList_WheresRayquaza[] =
{
    {gText_CaveOfOrigin},
    {gText_MtPyre},
    {gText_SkyPillar},
    {gText_DontRemember},
};'''
FINAL_MENU = '''static const u8 sText_AraunaMboiCore[] = _("M'BOI CORE");
static const u8 sText_AraunaMemorial[] = _("MEMORIAL");
static const u8 sText_AraunaOathTower[] = _("OATH TOWER");

static const struct MenuAction MultichoiceList_WheresRayquaza[] =
{
    {sText_AraunaMboiCore},
    {sText_AraunaMemorial},
    {sText_AraunaOathTower},
    {gText_DontRemember},
};'''

LANDMARK_REPLACEMENTS = {
    'static const u8 LandmarkName_MrBrineysCottage[] = _("MR. BRINEY\'S COTTAGE");':
        'static const u8 LandmarkName_MrBrineysCottage[] = _("SAILOR\'S COTTAGE");',
    'static const u8 LandmarkName_SlateportBeach[] = _("PORTO DO SAL BEACH");':
        'static const u8 LandmarkName_SlateportBeach[] = _("PORTO DO SAL BEACH");',
    'static const u8 LandmarkName_NewMauville[] = _("NEW ENCRUZILHADA");':
        'static const u8 LandmarkName_NewMauville[] = _("OLD POWER RELAY");',
    'static const u8 LandmarkName_MeteorFalls[] = _("RUINAS DA QUEDA");':
        'static const u8 LandmarkName_MeteorFalls[] = _("RUINAS DA QUEDA");',
    'static const u8 LandmarkName_RusturfTunnel[] = _("GALERIAS SERRA");':
        'static const u8 LandmarkName_RusturfTunnel[] = _("GALERIAS SERRA");',
    'static const u8 LandmarkName_SafariZoneEntrance[] = _("SAFARI ZONE ENTRANCE");':
        'static const u8 LandmarkName_SafariZoneEntrance[] = _("ARAUNA PRESERVE");',
    'static const u8 LandmarkName_MtPyre[] = _("MEMORIAL DOS NOMES");':
        'static const u8 LandmarkName_MtPyre[] = _("MEMORIAL NOMES");',
    'static const u8 LandmarkName_SeafloorCavern[] = _("CAVERNAS M\'BOI");':
        'static const u8 LandmarkName_SeafloorCavern[] = _("CAVERNAS M\'BOI");',
    'static const u8 LandmarkName_GraniteCave[] = _("GRUTA DAS VOZES");':
        'static const u8 LandmarkName_GraniteCave[] = _("GRUTA DAS VOZES");',
    'static const u8 LandmarkName_SkyPillar[] = _("TORRE JURAMENTO");':
        'static const u8 LandmarkName_SkyPillar[] = _("TORRE JURAMENTO");',
    'static const u8 LandmarkName_MagmaHideout[] = _("MAGMA HIDEOUT");':
        'static const u8 LandmarkName_MagmaHideout[] = _("REMEMBRANCERS BASE");',
}


def fail(message: str) -> None:
    raise ValueError(f"Main-readiness residue renderer: {message}")


def load_bank() -> dict[str, dict[str, list[str]]]:
    raw = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(raw) != set(EXPECTED):
        fail("bank section contract mismatch")
    for section, expected in EXPECTED.items():
        if set(raw[section]) != expected:
            fail(f"{section}: label contract mismatch")
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


def render_asm(source: str, targets: dict[str, list[str]]) -> str:
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


def validate_asm(section: str, source: str, rendered: str, labels: set[str]) -> None:
    if mask(source, labels) != mask(rendered, labels):
        fail(f"{section}: non-owned script structure changed")
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
    for stale in STALE:
        if stale in owned:
            fail(f"{section}: stale visible identity survived: {stale}")
    if section == "cave_of_origin":
        for required in ("AMALIA", "M'BOI", "GUARDIAN", "MEMORIAL", "OATH TOWER"):
            if required not in owned:
                fail(f"cave_of_origin: canonical identity missing: {required}")
    if section == "route105_pokenav":
        for required in ("ELIAS", "OTACILIO", "POKéNAV"):
            if required not in owned:
                fail(f"route105_pokenav: canonical identity missing: {required}")
    if section == "abandoned_ship_office":
        for required in ("HARBOR ENGINEER", "SCANNER", "PORTO DO SAL"):
            if required not in owned:
                fail(f"abandoned_ship_office: canonical identity missing: {required}")


def render_menu(source: str) -> str:
    original_count = source.count(ORIGINAL_MENU)
    final_count = source.count(FINAL_MENU)
    if original_count == 1 and final_count == 0:
        return source.replace(ORIGINAL_MENU, FINAL_MENU, 1)
    if original_count == 0 and final_count == 1:
        return source
    fail(f"menu contract mismatch: original={original_count}, final={final_count}")


def validate_menu(source: str, rendered: str) -> None:
    if FINAL_MENU not in rendered or rendered.count(FINAL_MENU) != 1:
        fail("Arauna Cave of Origin multichoice was not installed exactly once")
    before = source.replace(ORIGINAL_MENU, "<ARAUNA_CAVE_MENU>", 1).replace(FINAL_MENU, "<ARAUNA_CAVE_MENU>", 1)
    after = rendered.replace(ORIGINAL_MENU, "<ARAUNA_CAVE_MENU>", 1).replace(FINAL_MENU, "<ARAUNA_CAVE_MENU>", 1)
    if before != after:
        fail("non-owned script_menu structure changed")
    for token in ("MULTI_WHERES_RAYQUAZA", "MultichoiceList_WheresRayquaza"):
        if source.count(token) != rendered.count(token):
            fail(f"menu token count changed: {token}")


def render_landmarks(source: str) -> str:
    rendered = source
    for old, new in LANDMARK_REPLACEMENTS.items():
        if old == new:
            # The base file already says this; the entry survives only to
            # record that the landmark was looked at. Nothing to replace.
            continue
        old_count = rendered.count(old)
        new_count = rendered.count(new)
        if old_count == 1 and new_count == 0:
            rendered = rendered.replace(old, new, 1)
        elif old_count == 0 and new_count == 1:
            continue
        else:
            fail(f"landmark contract mismatch for {old!r}: old={old_count}, final={new_count}")
    return rendered


def normalize_landmarks(source: str) -> str:
    normalized = source
    for index, (old, new) in enumerate(LANDMARK_REPLACEMENTS.items()):
        marker = f"<ARAUNA_LANDMARK_{index}>"
        if old in normalized:
            normalized = normalized.replace(old, marker, 1)
        elif new in normalized:
            normalized = normalized.replace(new, marker, 1)
        else:
            fail(f"cannot normalize landmark pair: {old!r}")
    return normalized


def validate_landmarks(source: str, rendered: str) -> None:
    if normalize_landmarks(source) != normalize_landmarks(rendered):
        fail("non-owned landmark.c structure changed")
    for final in LANDMARK_REPLACEMENTS.values():
        if final not in rendered:
            fail(f"canonical landmark missing: {final}")
    for stale in (
        "MR. BRINEY'S COTTAGE", "SLATEPORT BEACH", "NEW MAUVILLE",
        "METEOR FALLS", "RUSTURF TUNNEL", "SAFARI ZONE ENTRANCE",
        "MT. PYRE", "SEAFLOOR CAVERN", "GRANITE CAVE", "SKY PILLAR", "MAGMA HIDEOUT",
    ):
        if f'_("{stale}")' in rendered:
            fail(f"stale landmark survived: {stale}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Close high-confidence visible residues found by the main-readiness audit.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    for section, path in FILES.items():
        source = path.read_text(encoding="utf-8")
        rendered = render_asm(source, bank[section])
        validate_asm(section, source, rendered, EXPECTED[section])
        if args.in_place:
            path.write_text(rendered, encoding="utf-8")

    menu_source = MENU_PATH.read_text(encoding="utf-8")
    menu_rendered = render_menu(menu_source)
    validate_menu(menu_source, menu_rendered)
    if args.in_place:
        MENU_PATH.write_text(menu_rendered, encoding="utf-8")

    landmark_source = LANDMARK_PATH.read_text(encoding="utf-8")
    landmark_rendered = render_landmarks(landmark_source)
    validate_landmarks(landmark_source, landmark_rendered)
    if args.in_place:
        LANDMARK_PATH.write_text(landmark_rendered, encoding="utf-8")
        # This renderer is deliberately last in the official manifest. At this
        # point every reviewed overlay has been applied, so the audit sees the
        # actual compile-time visible surface rather than the vanilla sources.
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "audit_rendered_visible_residue_en.py"), "--fail-owned"],
            cwd=ROOT,
            check=True,
        )

    mode = "Rendered" if args.in_place else "Validated"
    print(
        f"{mode} main-readiness residue: 11 visible blocks + 3 private menu labels + "
        f"{len(LANDMARK_REPLACEMENTS)} canonical landmarks."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

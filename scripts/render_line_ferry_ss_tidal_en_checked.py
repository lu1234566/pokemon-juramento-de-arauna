#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "line_ferry_ss_tidal.json"
FILES = {
    "corridor": ROOT / "data" / "maps" / "SSTidalCorridor" / "scripts.inc",
    "rooms": ROOT / "data" / "maps" / "SSTidalRooms" / "scripts.inc",
}
EXPECTED = {
    "corridor": {
        "SSTidalCorridor_Text_ScottBattleFrontierInvite",
        "SSTidal_Text_FastCurrentsHopeYouEnjoyVoyage",
        "SSTidal_Text_HopeYouEnjoyVoyage",
        "SSTidal_Text_MadeLandInSlateport",
        "SSTidal_Text_MadeLandInLilycove",
        "SSTidalCorridor_Text_CanRestInCabin2",
        "SSTidalCorridor_Text_WeveArrived",
        "SSTidalCorridor_Text_VisitOtherCabins",
        "SSTidalCorridor_Text_EnjoyYourCruise",
        "SSTidalCorridor_Text_HorizonSpreadsBeyondPorthole",
        "SSTidalCorridor_Text_BrineyWelcomeAboard",
        "SSTidalCorridor_Text_Peeko",
        "SSTidalCorridor_Text_Cabin1",
        "SSTidalCorridor_Text_Cabin2",
        "SSTidalCorridor_Text_Cabin3",
        "SSTidalCorridor_Text_Cabin4",
    },
    "rooms": {
        "SSTidalRooms_Text_TakeRestOnBed",
        "SSTidalRooms_Text_ColtonIntro",
        "SSTidalRooms_Text_ColtonDefeat",
        "SSTidalRooms_Text_ColtonPostBattle",
        "SSTidalRooms_Text_MicahIntro",
        "SSTidalRooms_Text_MicahDefeat",
        "SSTidalRooms_Text_MicahPostBattle",
        "SSTidalRooms_Text_ThomasIntro",
        "SSTidalRooms_Text_ThomasDefeat",
        "SSTidalRooms_Text_ThomasPostBattle",
        "SSTidalRooms_Text_JedIntro",
        "SSTidalRooms_Text_JedDefeat",
        "SSTidalRooms_Text_JedPostBattle",
        "SSTidalRooms_Text_JedNotEnoughMons",
        "SSTidalRooms_Text_LeaIntro",
        "SSTidalRooms_Text_LeaDefeat",
        "SSTidalRooms_Text_LeaPostBattle",
        "SSTidalRooms_Text_LeaNotEnoughMons",
        "SSTidalRooms_Text_GarretIntro",
        "SSTidalRooms_Text_GarretDefeat",
        "SSTidalRooms_Text_GarretPostBattle",
        "SSTidalRooms_Text_NaomiIntro",
        "SSTidalRooms_Text_NaomiDefeat",
        "SSTidalRooms_Text_NaomiPostBattle",
        "SSTidalRooms_Text_NotSuspiciousTakeThis",
        "SSTidalRooms_Text_ExplainSnatch",
    },
}
CORRIDOR_TOKENS = (
    "VAR_SS_TIDAL_SCOTT_STATE",
    "VAR_SS_TIDAL_STATE",
    "SS_TIDAL_BOARD_SLATEPORT",
    "SS_TIDAL_BOARD_LILYCOVE",
    "SS_TIDAL_DEPART_SLATEPORT",
    "SS_TIDAL_DEPART_LILYCOVE",
    "SS_TIDAL_HALFWAY_SLATEPORT",
    "SS_TIDAL_HALFWAY_LILYCOVE",
    "SS_TIDAL_LAND_SLATEPORT",
    "SS_TIDAL_LAND_LILYCOVE",
    "SS_TIDAL_EXIT_CURRENTS_RIGHT",
    "SS_TIDAL_EXIT_CURRENTS_LEFT",
    "SetSSTidalFlag",
    "ResetSSTidalFlag",
    "HEAL_LOCATION_LILYCOVE_CITY",
    "HEAL_LOCATION_SLATEPORT_CITY",
    "MAP_LILYCOVE_CITY_HARBOR",
    "MAP_SLATEPORT_CITY_HARBOR",
    "FLAG_RECEIVED_TM_SNATCH",
    "FLAG_HIDE_SS_TIDAL_ROOMS_SNATCH_GIVER",
    "FLAG_DEFEATED_SS_TIDAL_TRAINERS",
    "FLAG_MET_SCOTT_ON_SS_TIDAL",
    "TRAINER_PHILLIP",
    "TRAINER_LEONARD",
    "TRAINER_COLTON",
    "TRAINER_MICAH",
    "TRAINER_THOMAS",
    "TRAINER_LEA_AND_JED",
    "TRAINER_GARRET",
    "TRAINER_NAOMI",
    "LOCALID_SS_TIDAL_SCOTT",
    "LOCALID_SS_TIDAL_EXIT_SAILOR",
    "LookThroughPorthole",
)
ROOM_TOKENS = (
    "FLAG_RECEIVED_TM_SNATCH",
    "ITEM_TM_SNATCH",
    "Common_EventScript_ShowBagIsFull",
    "Common_EventScript_OutOfCenterPartyHeal",
    "SSTidalRooms_EventScript_ProgessCruiseAfterBed",
    "TRAINER_COLTON",
    "TRAINER_MICAH",
    "TRAINER_THOMAS",
    "TRAINER_LEA_AND_JED",
    "TRAINER_GARRET",
    "TRAINER_NAOMI",
    "trainerbattle_single",
    "trainerbattle_double",
)
MAX_VISIBLE_WIDTH = 32
PLACEHOLDER_SAMPLE = "LONGPHRASE123456"
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")


def load_bank() -> dict[str, dict[str, list[str]]]:
    bank = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    if set(bank) != set(FILES):
        raise ValueError(f"bank sections mismatch: {sorted(bank)}")
    for section, expected in EXPECTED.items():
        actual = set(bank[section])
        if actual != expected:
            raise ValueError(
                f"{section}: label contract mismatch; "
                f"missing={sorted(expected - actual)}, extra={sorted(actual - expected)}"
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
                            f"{section}/{label}: visible segment is "
                            f"{len(segment)} chars: {segment!r}"
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
        stripped = line.lstrip(" \t")
        is_string = stripped.startswith(".string ")
        if is_string or continuation:
            saw_string = saw_string or is_string
            continuation = line.rstrip("\n").endswith("\\")
            pos = end
            continue
        break
    if not saw_string:
        raise ValueError(f"{label}: no consecutive .string body found")
    return start, pos


def render_text(source: str, targets: dict[str, list[str]]) -> str:
    spans: list[tuple[int, int, str]] = []
    for label, payloads in targets.items():
        start, end = body_span(source, label)
        body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        spans.append((start, end, body))
    rendered = source
    for start, end, body in sorted(spans, reverse=True):
        rendered = rendered[:start] + body + rendered[end:]
    return rendered


def masked(source: str, labels: set[str], marker: str) -> str:
    spans = [body_span(source, label) for label in labels]
    result = source
    for start, end in sorted(spans, reverse=True):
        result = result[:start] + f'\t.string "<{marker}>"\n' + result[end:]
    return result


def validate_structure(section: str, source: str, rendered: str) -> None:
    marker = f"ARAUNA_SS_TIDAL_{section.upper()}"
    if masked(source, EXPECTED[section], marker) != masked(rendered, EXPECTED[section], marker):
        raise ValueError(f"{section}: non-dialogue structure changed")


def validate_tokens(source: str, rendered: str, tokens: tuple[str, ...], section: str) -> None:
    for token in tokens:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            raise ValueError(f"{section}: expected gameplay token missing: {token}")
        if before != after:
            raise ValueError(f"{section}: gameplay token changed: {token}: {before} -> {after}")


def validate_rendered(section: str, rendered: str, targets: dict[str, list[str]]) -> None:
    for label, payloads in targets.items():
        start, end = body_span(rendered, label)
        body = rendered[start:end]
        for payload in payloads:
            if f'\t.string "{payload}"' not in body:
                raise ValueError(f"{section}/{label}: rendered payload missing: {payload!r}")
    owned = "\n".join(
        rendered[body_span(rendered, label)[0]:body_span(rendered, label)[1]]
        for label in EXPECTED[section]
    )
    stale = (
        "voce",
        "voce aqui",
        "Chegamos",
        "viagem",
        "Aproveite",
        "CAPITAO:",
        "CIRCUITO DE BATALHA",
        "cabine",
        "Esta balsa",
        "Esperamos que",
        "LILYCOVE CITY",
        "HOENN",
    )
    for token in stale:
        if token in owned:
            raise ValueError(f"{section}: stale visible token survived: {token}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the LINE FERRY / S.S. Tidal English surface.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    bank = load_bank()
    validate_payloads(bank)
    outputs: dict[str, str] = {}
    for section, path in FILES.items():
        source = path.read_text(encoding="utf-8")
        rendered = render_text(source, bank[section])
        validate_structure(section, source, rendered)
        validate_tokens(
            source,
            rendered,
            CORRIDOR_TOKENS if section == "corridor" else ROOM_TOKENS,
            section,
        )
        validate_rendered(section, rendered, bank[section])
        outputs[section] = rendered

    owned_all = "\n".join(
        outputs[section][body_span(outputs[section], label)[0]:body_span(outputs[section], label)[1]]
        for section in FILES
        for label in EXPECTED[section]
    )
    for required in ("PORTO DO SAL", "BAIA DAS LUZES", "BATTLE CIRCUIT", "SEU BENTO", "LINE FERRY"):
        if required not in owned_all:
            raise ValueError(f"S.S. Tidal identity missing: {required}")

    if args.check:
        print(
            "LINE FERRY / S.S. Tidal renderer OK: "
            f"{sum(len(v) for v in EXPECTED.values())} text blocks validated."
        )
        return 0
    if args.in_place:
        for section, path in FILES.items():
            path.write_text(outputs[section], encoding="utf-8")
        return 0
    print(outputs["corridor"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

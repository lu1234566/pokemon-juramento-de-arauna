#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "data" / "text" / "arauna" / "en" / "baia_luzes_harbor_tickets.json"
FILES = {
    "harbor": ROOT / "data" / "maps" / "LilycoveCity_Harbor" / "scripts.inc",
    "ticket1": ROOT / "data" / "text" / "event_ticket_1.inc",
    "ticket2": ROOT / "data" / "text" / "event_ticket_2.inc",
}
STRINGS_PATH = ROOT / "src" / "strings.c"
EXPECTED = {
    "harbor": {
        "LilycoveCity_Harbor_Text_FerryUnavailable",
        "LilycoveCity_Harbor_Text_MayISeeYourTicket",
        "LilycoveCity_Harbor_Text_NoTicket",
        "LilycoveCity_Harbor_Text_FlashTicketWhereTo",
        "LilycoveCity_Harbor_Text_SailAnotherTime",
        "LilycoveCity_Harbor_Text_SlateportItIs",
        "LilycoveCity_Harbor_Text_BattleFrontierItIs",
        "LilycoveCity_Harbor_Text_PleaseBoard",
        "LilycoveCity_Harbor_Text_WhereWouldYouLikeToGo",
        "LilycoveCity_Harbor_Text_SailorFerryUnavailable",
        "LilycoveCity_Harbor_Text_SailorFerryAvailable",
    },
    "ticket1": {
        "EventTicket_Text_ShowOldSeaMap",
        "EventTicket_Text_ThatPass",
        "EventTicket_Text_ShowEonTicket",
        "EventTicket_Text_SouthernIslandSailBack",
        "EventTicket_Text_SailHome",
        "EventTicket_Text_AsYouLike",
    },
    "ticket2": {
        "EventTicket_Text_OldSeaMapTooFar",
        "EventTicket_Text_BrineyHoldOnASecond",
        "EventTicket_Text_BrineyLetsSail",
        "EventTicket_Text_OddTicketGetOnBoard",
        "FarawayIsland_Entrance_Text_SailorReturn",
        "BirthIsland_Harbor_Text_SailorReturn",
        "EventTicket_Text_OddTicketsWhereTo",
        "NavelRock_Harbor_Text_SailorReturn",
    },
}
GAMEPLAY_TOKENS = (
    "FLAG_SYS_GAME_CLEAR",
    "FLAG_ENABLE_SHIP_SOUTHERN_ISLAND",
    "FLAG_ENABLE_SHIP_BIRTH_ISLAND",
    "FLAG_ENABLE_SHIP_FARAWAY_ISLAND",
    "FLAG_ENABLE_SHIP_NAVEL_ROCK",
    "ITEM_EON_TICKET",
    "ITEM_AURORA_TICKET",
    "ITEM_OLD_SEA_MAP",
    "ITEM_MYSTIC_TICKET",
    "FLAG_SHOWN_EON_TICKET",
    "FLAG_SHOWN_AURORA_TICKET",
    "FLAG_SHOWN_OLD_SEA_MAP",
    "FLAG_SHOWN_MYSTIC_TICKET",
    "ScriptMenu_CreateLilycoveSSTidalMultichoice",
    "GetLilycoveSSTidalSelection",
    "MAP_SOUTHERN_ISLAND_EXTERIOR",
    "MAP_NAVEL_ROCK_HARBOR",
    "MAP_BIRTH_ISLAND_HARBOR",
    "MAP_FARAWAY_ISLAND_ENTRANCE",
    "MAP_SS_TIDAL_CORRIDOR",
    "MAP_BATTLE_FRONTIER_OUTSIDE_WEST",
    "VAR_SS_TIDAL_STATE",
    "SS_TIDAL_BOARD_LILYCOVE",
    "LOCALID_LILYCOVE_HARBOR_SS_TIDAL",
    "LOCALID_LILYCOVE_HARBOR_BRINEY",
    "Common_EventScript_FerryDepart",
)
OLD_FRONTIER_DECL = 'const u8 gText_BattleFrontier[] = _("BATTLE FRONTIER");'
NEW_FRONTIER_DECL = 'const u8 gText_BattleFrontier[] = _("BATTLE CIRCUIT");'
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


def label_match(source: str, label: str) -> re.Match[str]:
    matches = list(re.finditer(rf"(?m)^{re.escape(label)}::?\n", source))
    if len(matches) != 1:
        raise ValueError(f"{label}: expected one label, found {len(matches)}")
    return matches[0]


def body_span(source: str, label: str) -> tuple[int, int]:
    match = label_match(source, label)
    start = match.end()
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


def mask_targets(source: str, labels: set[str], marker: str) -> str:
    spans = [body_span(source, label) for label in labels]
    masked = source
    for start, end in sorted(spans, reverse=True):
        masked = masked[:start] + f'\t.string "<{marker}>"\n' + masked[end:]
    return masked


def validate_structure(section: str, source: str, rendered: str) -> None:
    marker = f"ARAUNA_HARBOR_{section.upper()}"
    if mask_targets(source, EXPECTED[section], marker) != mask_targets(
        rendered, EXPECTED[section], marker
    ):
        raise ValueError(f"{section}: non-dialogue structure changed")


def validate_harbor_gameplay(source: str, rendered: str) -> None:
    for token in GAMEPLAY_TOKENS:
        before = source.count(token)
        after = rendered.count(token)
        if before == 0:
            raise ValueError(f"expected Harbor gameplay token missing: {token}")
        if before != after:
            raise ValueError(f"Harbor gameplay token changed: {token}: {before} -> {after}")


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
    stale = ("CIRO:", "DESENCANTO", "LILYCOVE", "SLATEPORT", "BRINEY:", "CAPT. BRINEY")
    for token in stale:
        if token in owned:
            raise ValueError(f"{section}: stale visible token survived: {token}")


def render_frontier_label(source: str) -> str:
    old_count = source.count(OLD_FRONTIER_DECL)
    new_count = source.count(NEW_FRONTIER_DECL)
    if old_count == 1 and new_count == 0:
        return source.replace(OLD_FRONTIER_DECL, NEW_FRONTIER_DECL, 1)
    if old_count == 0 and new_count == 1:
        return source
    raise ValueError(
        "gText_BattleFrontier anchor is ambiguous: "
        f"old={old_count}, new={new_count}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render Baia das Luzes Harbor and event-ticket English surface."
    )
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
        if section == "harbor":
            validate_harbor_gameplay(source, rendered)
        validate_rendered(section, rendered, bank[section])
        outputs[section] = rendered

    strings_source = STRINGS_PATH.read_text(encoding="utf-8")
    strings_rendered = render_frontier_label(strings_source)
    if strings_rendered.count(NEW_FRONTIER_DECL) != 1 or OLD_FRONTIER_DECL in strings_rendered:
        raise ValueError("BATTLE CIRCUIT destination label validation failed")

    owned_all = "\n".join(
        outputs[section][body_span(outputs[section], label)[0]:body_span(outputs[section], label)[1]]
        for section in FILES
        for label in EXPECTED[section]
    )
    for required in ("BAIA DAS LUZES", "PORTO DO SAL", "BATTLE CIRCUIT", "SEU BENTO"):
        if required not in owned_all:
            raise ValueError(f"Harbor identity missing: {required}")

    if args.check:
        print(
            "Baia das Luzes Harbor/event-ticket renderer OK: "
            f"{sum(len(v) for v in EXPECTED.values())} text blocks + destination label validated."
        )
        return 0
    if args.in_place:
        for section, path in FILES.items():
            path.write_text(outputs[section], encoding="utf-8")
        STRINGS_PATH.write_text(strings_rendered, encoding="utf-8")
        return 0

    print(outputs["harbor"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

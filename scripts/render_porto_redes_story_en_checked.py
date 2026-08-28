#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

DATA_FILES = (
    ROOT / "data" / "text" / "arauna" / "en" / "porto_redes_core.json",
    ROOT / "data" / "text" / "arauna" / "en" / "porto_redes_gym.json",
    ROOT / "data" / "text" / "arauna" / "en" / "porto_redes_hall.json",
    ROOT / "data" / "text" / "arauna" / "en" / "porto_redes_residents.json",
)

FILES = {
    "sailor_house": "data/maps/Route104_MrBrineysHouse/scripts.inc",
    "town": "data/maps/DewfordTown/scripts.inc",
    "gym": "data/maps/DewfordTown_Gym/scripts.inc",
    "hall": "data/maps/DewfordTown_Hall/scripts.inc",
    "house1": "data/maps/DewfordTown_House1/scripts.inc",
    "house2": "data/maps/DewfordTown_House2/scripts.inc",
    "center": "data/maps/DewfordTown_PokemonCenter_1F/scripts.inc",
    "cave1": "data/maps/GraniteCave_1F/scripts.inc",
    "bento": "data/maps/GraniteCave_StevensRoom/scripts.inc",
    "route109": "data/maps/Route109/scripts.inc",
}

REQUIRED_TOKENS = {
    "sailor_house": (
        "FLAG_MR_BRINEY_SAILING_INTRO",
        "FLAG_DELIVERED_STEVEN_LETTER",
        "FLAG_DELIVERED_DEVON_GOODS",
        "SPECIES_WINGULL",
        "VAR_BOARD_BRINEY_BOAT_STATE",
    ),
    "town": (
        "FLAG_VISITED_DEWFORD_TOWN",
        "FLAG_DELIVERED_STEVEN_LETTER",
        "MULTI_BRINEY_ON_DEWFORD",
        "ITEM_OLD_ROD",
        "FLAG_RECEIVED_OLD_ROD",
        "EASY_CHAT_TYPE_TRENDY_PHRASE",
    ),
    "gym": (
        "TRAINER_BRAWLY_1",
        "FLAG_DEFEATED_DEWFORD_GYM",
        "FLAG_BADGE02_GET",
        "ITEM_TM_BULK_UP",
        "FLAG_RECEIVED_TM_BULK_UP",
        "FLAG_ENABLE_BRAWLY_MATCH_CALL",
        "TRAINER_TAKAO",
        "TRAINER_JOCELYN",
        "TRAINER_LAURA",
        "TRAINER_BRENDEN",
        "TRAINER_CRISTIAN",
        "TRAINER_LILITH",
    ),
    "hall": (
        "Common_EventScript_BufferTrendyPhrase",
        "GetDewfordHallPaintingNameIndex",
        "ITEM_TM_SLUDGE_BOMB",
        "FLAG_RECEIVED_TM_SLUDGE_BOMB",
    ),
    "house1": ("SPECIES_ZIGZAGOON",),
    "house2": ("ITEM_SILK_SCARF", "FLAG_RECEIVED_SILK_SCARF"),
    "center": ("HEAL_LOCATION_DEWFORD_TOWN",),
    "cave1": ("ITEM_HM_FLASH", "FLAG_RECEIVED_HM_FLASH"),
    "bento": (
        "ITEM_LETTER",
        "FLAG_DELIVERED_STEVEN_LETTER",
        "ITEM_TM_STEEL_WING",
        "FLAG_REGISTERED_STEVEN_POKENAV",
    ),
    "route109": (
        "FLAG_DELIVERED_DEVON_GOODS",
        "MULTI_BRINEY_OFF_DEWFORD",
        "MAP_DEWFORD_TOWN",
        "MAP_ROUTE109",
    ),
}

FORBIDDEN_VISIBLE_TOKENS = (
    "MR. BRINEY",
    "PEEKO",
    "DEWFORD",
    "PETALBURG",
    "SLATEPORT",
    "BRAWLY",
    "STEVEN",
    "DEVON GOODS",
    "DEVON",
    "INSÍGNIA",
    "RESPONSAVEL",
    "O mar devolve coisas",
    "na memoria da agua",
    "recebeu a",
    "Voce ",
    "voce ",
    "Nao ",
    "nao ",
)

MENU_PATH = ROOT / "src" / "data" / "script_menu.h"
MENU_DEFS = '''
static const u8 sText_AraunaPampaDaEspera[] = _("PAMPA DA ESPERA");
static const u8 sText_AraunaPortoDoSal[] = _("PORTO DO SAL");
static const u8 sText_AraunaPortoDasRedes[] = _("PORTO DAS REDES");

'''
MENU_ANCHOR = "// multichoice lists\n"
MENU_ON_OLD = '''static const struct MenuAction MultichoiceList_BrineyOnDewford[] =
{
    {gText_Petalburg},
    {gText_Slateport},
    {gText_Exit},
};
'''
MENU_ON_NEW = '''static const struct MenuAction MultichoiceList_BrineyOnDewford[] =
{
    {sText_AraunaPampaDaEspera},
    {sText_AraunaPortoDoSal},
    {gText_Exit},
};
'''
MENU_OFF_OLD = '''static const struct MenuAction MultichoiceList_BrineyOffDewford[] =
{
    {gText_Dewford},
    {gText_Exit},
};
'''
MENU_OFF_NEW = '''static const struct MenuAction MultichoiceList_BrineyOffDewford[] =
{
    {sText_AraunaPortoDasRedes},
    {gText_Exit},
};
'''


def load_targets() -> dict[str, dict[str, list[str]]]:
    merged: dict[str, dict[str, list[str]]] = {}
    for path in DATA_FILES:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{path}: top-level JSON must be an object")
        for file_key, entries in data.items():
            if file_key not in FILES:
                raise ValueError(f"{path}: unknown file key {file_key!r}")
            if file_key in merged:
                raise ValueError(f"{path}: duplicate file key {file_key!r}")
            if not isinstance(entries, dict) or not entries:
                raise ValueError(f"{path}: {file_key!r} must contain text entries")
            merged[file_key] = entries

    missing = sorted(set(FILES) - set(merged))
    extra = sorted(set(merged) - set(FILES))
    if missing or extra:
        raise ValueError(f"target/file mismatch; missing={missing}, extra={extra}")
    return merged


TARGETS = load_targets()


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf'(?m)^{re.escape(label)}:\n(?P<body>(?:\t\.string ".*"\n)+)'
    )


def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    replacements = {
        "{PLAYER}": "PLAYERX",
        "{KUN}": "",
        "{STR_VAR_1}": "LONGPHRASE123456",
        "{STR_VAR_2}": "LONGPHRASE123456",
        "{LEFT_ARROW}": "<",
    }
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
    return [part.strip() for part in CONTROL_RE.split(cleaned)]


def validate_authored_data() -> None:
    seen_labels: set[str] = set()
    for file_key, entries in TARGETS.items():
        for label, payloads in entries.items():
            if label in seen_labels:
                raise ValueError(f"duplicate target label across JSON files: {label}")
            seen_labels.add(label)
            if not isinstance(payloads, list) or not payloads:
                raise ValueError(f"{file_key}:{label}: payload must be a non-empty list")
            for index, payload in enumerate(payloads):
                if not isinstance(payload, str):
                    raise ValueError(f"{file_key}:{label}: payload {index} is not text")
                if '"' in payload:
                    raise ValueError(f"{file_key}:{label}: raw double quote is unsafe in .string payload")
                for segment in visible_segments(payload):
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(
                            f"{file_key}:{label}: visible segment is {len(segment)} chars, "
                            f"max {MAX_VISIBLE_WIDTH}: {segment!r}"
                        )
            if not payloads[-1].endswith("$"):
                raise ValueError(f"{file_key}:{label}: final payload must terminate with '$'")
            if any("$" in payload for payload in payloads[:-1]):
                raise ValueError(f"{file_key}:{label}: '$' may appear only in the final payload")


def render_text(source: str, file_key: str) -> str:
    rendered = source
    for label, payloads in TARGETS[file_key].items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(
                f"{file_key}:{label}: expected one string-only block, found {len(matches)}"
            )
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads)
        start, end = matches[0].span("body")
        rendered = rendered[:start] + new_body + rendered[end:]
    return rendered


def mask_target_bodies(text: str, file_key: str) -> str:
    masked = text
    for label in TARGETS[file_key]:
        match = block_pattern(label).search(masked)
        if not match:
            raise ValueError(f"{file_key}: cannot mask missing block {label}")
        start, end = match.span("body")
        masked = masked[:start] + '\t.string "<PORTO_REDES_EN>"\n' + masked[end:]
    return masked


def validate_rendered(source: str, rendered: str, file_key: str) -> None:
    if mask_target_bodies(source, file_key) != mask_target_bodies(rendered, file_key):
        raise ValueError(f"{file_key}: non-target script structure changed")

    for label in TARGETS[file_key]:
        match = block_pattern(label).search(rendered)
        if not match:
            raise ValueError(f"{file_key}: rendered block missing: {label}")
        body = match.group("body")
        for token in FORBIDDEN_VISIBLE_TOKENS:
            if token in body:
                raise ValueError(
                    f"{file_key}:{label}: stale visible token survived: {token!r}"
                )

    for token in REQUIRED_TOKENS[file_key]:
        if token not in rendered:
            raise ValueError(f"{file_key}: preserved gameplay token missing: {token}")


def render_menu(source: str) -> str:
    has_defs = MENU_DEFS in source
    has_old_on = MENU_ON_OLD in source
    has_old_off = MENU_OFF_OLD in source
    has_new_on = MENU_ON_NEW in source
    has_new_off = MENU_OFF_NEW in source

    if has_defs and has_new_on and has_new_off and not has_old_on and not has_old_off:
        return source

    if has_defs or has_new_on or has_new_off or not has_old_on or not has_old_off:
        raise ValueError("voyage menu is in an unexpected mixed state")
    if source.count(MENU_ANCHOR) != 1:
        raise ValueError("voyage menu anchor is not unique")

    rendered = source.replace(MENU_ANCHOR, MENU_ANCHOR + MENU_DEFS, 1)
    rendered = rendered.replace(MENU_ON_OLD, MENU_ON_NEW, 1)
    rendered = rendered.replace(MENU_OFF_OLD, MENU_OFF_NEW, 1)
    return rendered


def normalize_menu(text: str) -> str:
    normalized = text.replace(MENU_DEFS, "")
    for old, new, marker in (
        (MENU_ON_OLD, MENU_ON_NEW, "<PORTO_REDES_ON_MENU>"),
        (MENU_OFF_OLD, MENU_OFF_NEW, "<PORTO_REDES_OFF_MENU>"),
    ):
        if new in normalized:
            normalized = normalized.replace(new, marker, 1)
        elif old in normalized:
            normalized = normalized.replace(old, marker, 1)
        else:
            raise ValueError(f"cannot normalize voyage menu: {marker}")
    return normalized


def validate_menu(source: str, rendered: str) -> None:
    if normalize_menu(source) != normalize_menu(rendered):
        raise ValueError("non-voyage script-menu structure changed")
    if MENU_DEFS not in rendered or MENU_ON_NEW not in rendered or MENU_OFF_NEW not in rendered:
        raise ValueError("Arauna voyage menu did not render completely")
    if any(
        token in MENU_ON_NEW + MENU_OFF_NEW
        for token in ("gText_Petalburg", "gText_Slateport", "gText_Dewford")
    ):
        raise ValueError("legacy destination string survived in Arauna voyage menu")
    for label in ("PAMPA DA ESPERA", "PORTO DO SAL", "PORTO DAS REDES"):
        if len(label) > MAX_VISIBLE_WIDTH:
            raise ValueError(f"voyage menu label too wide: {label}")


def process_text_file(file_key: str, *, in_place: bool) -> None:
    path = ROOT / FILES[file_key]
    source = path.read_text(encoding="utf-8")
    rendered = render_text(source, file_key)
    validate_rendered(source, rendered, file_key)
    if in_place:
        path.write_text(rendered, encoding="utf-8")


def process_menu(*, in_place: bool) -> None:
    source = MENU_PATH.read_text(encoding="utf-8")
    rendered = render_menu(source)
    validate_menu(source, rendered)
    if in_place:
        MENU_PATH.write_text(rendered, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render Porto das Redes, Ademar, the veteran sailor, Gruta das Vozes "
            "and Seu Bento's letter handoff in English without changing Emerald progression."
        )
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--dump-targets", action="store_true")
    args = parser.parse_args()
    if sum(bool(x) for x in (args.check, args.in_place, args.dump_targets)) > 1:
        parser.error("use only one of --check, --in-place or --dump-targets")

    validate_authored_data()

    if args.dump_targets:
        print(json.dumps(TARGETS, ensure_ascii=False, indent=2))
        return 0

    for file_key in FILES:
        process_text_file(file_key, in_place=args.in_place)
    process_menu(in_place=args.in_place)

    count = sum(len(entries) for entries in TARGETS.values())
    if args.check:
        print(
            f"Porto das Redes English renderer OK: {count} text blocks "
            f"across {len(FILES)} map files plus 2 voyage menus."
        )
    elif args.in_place:
        print(
            f"Rendered {count} Porto das Redes English text blocks "
            "and 2 voyage menus in place."
        )
    else:
        print(
            f"Validated {count} Porto das Redes English text blocks "
            "and 2 voyage menus."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

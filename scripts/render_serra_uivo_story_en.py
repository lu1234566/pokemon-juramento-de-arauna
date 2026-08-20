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
TARGET_DATA_DIR = ROOT / "data" / "text" / "arauna" / "en"
TARGET_DATA_FILES = (
    "serra_uivo_core.json",
    "serra_uivo_horizon.json",
    "serra_uivo_route.json",
    "serra_uivo_civic.json",
    "serra_uivo_residents.json",
)

FILES = {
    'city': 'data/maps/RustboroCity/scripts.inc',
    'gym': 'data/maps/RustboroCity_Gym/scripts.inc',
    'corp1': 'data/maps/RustboroCity_DevonCorp_1F/scripts.inc',
    'corp2': 'data/maps/RustboroCity_DevonCorp_2F/scripts.inc',
    'corp3': 'data/maps/RustboroCity_DevonCorp_3F/scripts.inc',
    'route116': 'data/maps/Route116/scripts.inc',
    'tunnel': 'data/maps/RusturfTunnel/scripts.inc',
    'school': 'data/maps/RustboroCity_PokemonSchool/scripts.inc',
    'cut': 'data/maps/RustboroCity_CuttersHouse/scripts.inc',
    'mart': 'data/maps/RustboroCity_Mart/scripts.inc',
    'flat21': 'data/maps/RustboroCity_Flat2_1F/scripts.inc',
    'flat22': 'data/maps/RustboroCity_Flat2_2F/scripts.inc',
    'flat23': 'data/maps/RustboroCity_Flat2_3F/scripts.inc',
    'house2': 'data/maps/RustboroCity_House2/scripts.inc',
    'flat12': 'data/maps/RustboroCity_Flat1_2F/scripts.inc',
}

TARGETS: dict[str, dict[str, list[str]]] = {}
for filename in TARGET_DATA_FILES:
    data = json.loads((TARGET_DATA_DIR / filename).read_text(encoding="utf-8"))
    overlap = TARGETS.keys() & data.keys()
    if overlap:
        raise ValueError(f"duplicate Serra do Uivo target section(s): {sorted(overlap)}")
    TARGETS.update(data)

if set(TARGETS) != set(FILES):
    missing = sorted(set(FILES) - set(TARGETS))
    extra = sorted(set(TARGETS) - set(FILES))
    raise ValueError(f"Serra do Uivo target file map mismatch; missing={missing}, extra={extra}")

REQUIRED_TOKENS = {'city': ('FLAG_DEVON_GOODS_STOLEN',
          'FLAG_RECOVERED_DEVON_GOODS',
          'FLAG_RETURNED_DEVON_GOODS',
          'ITEM_GREAT_BALL',
          'FLAG_HAS_MATCH_CALL',
          'TRAINER_MAY_RUSTBORO_TREECKO',
          'TRAINER_BRENDAN_RUSTBORO_TREECKO'),
 'gym': ('TRAINER_ROXANNE_1',
         'FLAG_BADGE01_GET',
         'FLAG_DEFEATED_RUSTBORO_GYM',
         'ITEM_TM_ROCK_TOMB',
         'FLAG_ENABLE_ROXANNE_MATCH_CALL'),
 'corp1': ('FLAG_RETURNED_DEVON_GOODS',),
 'corp2': ('VAR_FOSSIL_RESURRECTION_STATE',
           'SPECIES_LILEEP',
           'SPECIES_ANORITH',
           'ITEM_ROOT_FOSSIL',
           'ITEM_CLAW_FOSSIL'),
 'corp3': ('ITEM_LETTER', 'FLAG_RECEIVED_POKENAV', 'ITEM_EXP_SHARE', 'FLAG_DELIVERED_STEVEN_LETTER'),
 'route116': ('ITEM_REPEAT_BALL', 'FLAG_RECEIVED_REPEAT_BALL', 'VAR_ROUTE116_STATE', 'ITEM_BLACK_GLASSES'),
 'tunnel': ('TRAINER_GRUNT_RUSTURF_TUNNEL', 'ITEM_DEVON_GOODS', 'FLAG_RECOVERED_DEVON_GOODS', 'SPECIES_WINGULL'),
 'school': ('FLAG_RECEIVED_QUICK_CLAW', 'FLAG_BADGE01_GET', 'FLAG_MET_SCOTT_RUSTBORO'),
 'cut': ('ITEM_HM_CUT', 'FLAG_RECEIVED_HM_CUT'),
 'mart': ('ITEM_TIMER_BALL', 'ITEM_REPEAT_BALL', 'FLAG_MET_DEVON_EMPLOYEE'),
 'flat21': ('SPECIES_SKITTY',),
 'flat22': ('ITEM_PREMIER_BALL', 'FLAG_RECEIVED_PREMIER_BALL_RUSTBORO'),
 'flat23': (),
 'house2': (),
 'flat12': ('TryGetWallpaperWithWaldaPhrase', 'DoWaldaNamingScreen')}

FORBIDDEN_VISIBLE_TOKENS = (
    "HORIZONTEORATION",
    "CONSORCIO HORIZONTE",
    "INSÍGNIA",
    "RUSTBORO CITY",
    "PETALBURG CITY",
    "PETALBURG WOODS",
    "MR. STONE",
    "SCOTT:",
    "DEVON CORPORATION",
    "DEVON GOODS",
    "Voce ",
    "voce ",
    "Nao ",
    "nao ",
)

def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)"
    )

def visible_segments(payload: str) -> list[str]:
    cleaned = payload.replace("$", "")
    replacements = {
        "{PLAYER}": "PLAYERX",
        "{STR_VAR_1}": "ITEMNAME",
        "{STR_VAR_2}": "POKEMON",
        "{LEFT_ARROW}": "<",
    }
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
    cleaned = PLACEHOLDER_RE.sub("", cleaned)
    return [part.strip() for part in CONTROL_RE.split(cleaned)]

def validate_widths() -> None:
    for file_key, targets in TARGETS.items():
        for label, payloads in targets.items():
            for payload in payloads:
                for segment in visible_segments(payload):
                    if len(segment) > MAX_VISIBLE_WIDTH:
                        raise ValueError(
                            f"{file_key}:{label}: visible segment is {len(segment)} chars, "
                            f"max {MAX_VISIBLE_WIDTH}: {segment!r}"
                        )

def render_text(source: str, file_key: str) -> str:
    rendered = source
    for label, payloads in TARGETS[file_key].items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            raise ValueError(f"{file_key}:{label}: expected one text block, found {len(matches)}")
        new_body = "".join(f'\t.string "{payload}"\n' for payload in payloads) + "\n"
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
        masked = masked[:start] + '\t.string "<SERRA_UIVO_EN>"\n\n' + masked[end:]
    return masked

def validate_rendered(source: str, rendered: str, file_key: str) -> None:
    if mask_target_bodies(source, file_key) != mask_target_bodies(rendered, file_key):
        raise ValueError(f"{file_key}: non-dialogue structure changed")

    for label in TARGETS[file_key]:
        match = block_pattern(label).search(rendered)
        if not match:
            raise ValueError(f"{file_key}: rendered block missing: {label}")
        body = match.group("body")
        for token in FORBIDDEN_VISIBLE_TOKENS:
            if token in body:
                raise ValueError(f"{file_key}:{label}: stale visible token survived: {token!r}")

    for token in REQUIRED_TOKENS[file_key]:
        if token not in rendered:
            raise ValueError(f"{file_key}: preserved gameplay token missing: {token}")

def process(file_key: str, *, in_place: bool) -> None:
    path = ROOT / FILES[file_key]
    source = path.read_text(encoding="utf-8")
    rendered = render_text(source, file_key)
    validate_rendered(source, rendered, file_key)
    if in_place:
        path.write_text(rendered, encoding="utf-8")

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Render Serra do Uivo, Dalva, HORIZON, Route 116 and Galerias da Serra "
            "in English while preserving Emerald progression wiring."
        )
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.check and args.in_place:
        parser.error("use either --check or --in-place")

    validate_widths()
    for file_key in FILES:
        process(file_key, in_place=args.in_place)

    count = sum(len(targets) for targets in TARGETS.values())
    if args.check:
        print(f"Serra do Uivo English renderer OK: {count} text blocks across {len(FILES)} files.")
    elif args.in_place:
        print(f"Rendered {count} Serra do Uivo English text blocks in place.")
    else:
        print(f"Validated {count} Serra do Uivo English text blocks.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

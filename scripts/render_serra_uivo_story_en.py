#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import re
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_VISIBLE_WIDTH = 32
CONTROL_RE = re.compile(r"\\[npl]")
PLACEHOLDER_RE = re.compile(r"\{[^}]+\}")

FILES = {'city': 'data/maps/RustboroCity/scripts.inc',
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
 'flat12': 'data/maps/RustboroCity_Flat1_2F/scripts.inc'}

# Authored target table is compressed only to keep this large deterministic
# overlay reviewable as one source file. Use --dump-targets for readable JSON.
_TARGETS_ZLIB_B64 = """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"""
TARGETS = json.loads(zlib.decompress(base64.b64decode(_TARGETS_ZLIB_B64)).decode("utf-8"))

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
    parser.add_argument("--dump-targets", action="store_true")
    args = parser.parse_args()
    if sum(bool(x) for x in (args.check, args.in_place, args.dump_targets)) > 1:
        parser.error("use only one of --check, --in-place or --dump-targets")

    validate_widths()
    if args.dump_targets:
        print(json.dumps(TARGETS, ensure_ascii=False, indent=2))
        return 0

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

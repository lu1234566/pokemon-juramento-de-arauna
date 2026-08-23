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
    ROOT / "data" / "text" / "arauna" / "en" / "remaining_story_surface_a.json",
    ROOT / "data" / "text" / "arauna" / "en" / "remaining_story_surface_b.json",
    ROOT / "data" / "text" / "arauna" / "en" / "remaining_story_surface_c.json",
)

FILES = {
    "route104": "data/maps/Route104/scripts.inc",
    "route128": "data/maps/Route128/scripts.inc",
    "fallarbor": "data/maps/FallarborTown/scripts.inc",
    "aqua1f": "data/maps/AquaHideout_1F/scripts.inc",
    "pacifidlog": "data/maps/PacifidlogTown/scripts.inc",
    "fossil_tunnel": "data/maps/Route114_FossilManiacsTunnel/scripts.inc",
    "verdanturf": "data/maps/VerdanturfTown/scripts.inc",
    "cozmo": "data/maps/FallarborTown_CozmosHouse/scripts.inc",
    "mboi_gym": "data/maps/SootopolisCity_Gym_1F/scripts.inc",
    "mboi_house3": "data/maps/SootopolisCity_House3/scripts.inc",
    "mboi_house5": "data/maps/SootopolisCity_House5/scripts.inc",
    "petalburg_house2": "data/maps/PetalburgCity_House2/scripts.inc",
    "mossdeep_city": "data/maps/MossdeepCity/scripts.inc",
    "mossdeep_bento_house": "data/maps/MossdeepCity_StevensHouse/scripts.inc",
    "mossdeep_gym": "data/maps/MossdeepCity_Gym/scripts.inc",
    "seafloor1": "data/maps/SeafloorCavern_Room1/scripts.inc",
    "seafloor3": "data/maps/SeafloorCavern_Room3/scripts.inc",
    "seafloor4": "data/maps/SeafloorCavern_Room4/scripts.inc",
    "meteor_bento": "data/maps/MeteorFalls_StevensCave/scripts.inc",
    "val_house": "data/maps/VerdanturfTown_WandasHouse/scripts.inc",
    "pokedex": "data/text/pokedex_rating.inc",
}

EXPECTED_COUNTS = {
    "route104": 4,
    "route128": 8,
    "fallarbor": 2,
    "aqua1f": 9,
    "pacifidlog": 1,
    "fossil_tunnel": 4,
    "verdanturf": 1,
    "cozmo": 1,
    "mboi_gym": 16,
    "mboi_house3": 4,
    "mboi_house5": 2,
    "petalburg_house2": 2,
    "mossdeep_city": 8,
    "mossdeep_bento_house": 5,
    "mossdeep_gym": 16,
    "seafloor1": 6,
    "seafloor3": 6,
    "seafloor4": 6,
    "meteor_bento": 3,
    "val_house": 12,
    "pokedex": 25,
}

REQUIRED_TOKENS = {
    "route104": ("VAR_BOARD_BRINEY_BOAT_STATE", "FLAG_DEFEATED_RIVAL_ROUTE_104"),
    "route128": ("VAR_ROUTE128_STATE", "LOCALID_ROUTE128_ARCHIE", "LOCALID_ROUTE128_MAXIE", "LOCALID_ROUTE128_STEVEN"),
    "fallarbor": ("FLAG_VISITED_FALLARBOR_TOWN", "FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY"),
    "aqua1f": ("FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT", "FLAG_RECEIVED_RED_OR_BLUE_ORB", "TRAINER_GRUNT_AQUA_HIDEOUT_1"),
    "pacifidlog": ("FLAG_VISITED_PACIFIDLOG_TOWN", "STEP_CB_PACIFIDLOG_BRIDGE"),
    "fossil_tunnel": ("FLAG_SYS_GAME_CLEAR", "ITEM_ROOT_FOSSIL", "ITEM_CLAW_FOSSIL", "FLAG_RECEIVED_REVIVED_FOSSIL_MON"),
    "verdanturf": ("FLAG_VISITED_VERDANTURF_TOWN", "FLAG_RUSTURF_TUNNEL_OPENED"),
    "cozmo": ("ITEM_METEORITE", "ITEM_TM_RETURN", "FLAG_RECEIVED_TM_RETURN"),
    "mboi_gym": ("TRAINER_JUAN_1", "FLAG_BADGE08_GET", "ITEM_TM_WATER_PULSE", "FLAG_RECEIVED_TM_WATER_PULSE", "VAR_ICE_STEP_COUNT"),
    "mboi_house3": ("VAR_RESULT",),
    "mboi_house5": (),
    "petalburg_house2": (),
    "mossdeep_city": ("FLAG_RECEIVED_HM_DIVE", "VAR_MOSSDEEP_CITY_STATE", "VAR_SCOTT_STATE", "ITEM_KINGS_ROCK"),
    "mossdeep_bento_house": ("ITEM_HM_DIVE", "FLAG_RECEIVED_HM_DIVE", "ITEM_BELDUM", "FLAG_RECEIVED_BELDUM"),
    "mossdeep_gym": ("TRAINER_TATE_AND_LIZA_1", "FLAG_BADGE07_GET", "ITEM_TM_CALM_MIND", "FLAG_RECEIVED_TM_CALM_MIND"),
    "seafloor1": ("TRAINER_GRUNT_AQUA_HIDEOUT_2", "TRAINER_GRUNT_AQUA_HIDEOUT_3"),
    "seafloor3": ("TRAINER_SHELLY_SEAFLOOR_CAVERN",),
    "seafloor4": ("TRAINER_GRUNT_AQUA_HIDEOUT_5", "TRAINER_GRUNT_AQUA_HIDEOUT_6"),
    "meteor_bento": ("TRAINER_STEVEN", "FLAG_DEFEATED_METEOR_FALLS_STEVEN"),
    "val_house": ("FLAG_WALLY_SPEECH", "FLAG_DEFEATED_WALLY_VICTORY_ROAD", "FLAG_DEFEATED_LAVARIDGE_GYM", "FLAG_RUSTURF_TUNNEL_OPENED"),
    "pokedex": ("gBirchDexRatingText_AreYouCurious", "gBirchDexRatingText_DexCompleted", "gBirchDexRatingText_OnANationwideBasis"),
}

FORBIDDEN_VISIBLE_RE = re.compile(
    r"\b(?:SCOTT|JUAN|TATE|LIZA|MAY:|BRENDAN:|"
    r"VOCE|NAO|INSIGNIA|RECEBEU|LEMBRANCAS|MEMORIA|"
    r"SOOTOPOLIS CITY POK|MOSSDEEP CITY POK)\b",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    raise ValueError(f"Remaining story English renderer: {message}")


def load_targets() -> dict[str, dict[str, list[str]]]:
    merged: dict[str, dict[str, list[str]]] = {}
    for path in DATA_FILES:
        raw = json.loads(path.read_text(encoding="utf-8"))
        overlap = set(merged) & set(raw)
        if overlap:
            fail(f"duplicate JSON section(s): {sorted(overlap)}")
        merged.update(raw)

    if set(merged) != set(FILES):
        missing = sorted(set(FILES) - set(merged))
        extra = sorted(set(merged) - set(FILES))
        fail(f"JSON section mismatch; missing={missing}, extra={extra}")

    for section, expected_count in EXPECTED_COUNTS.items():
        entries = merged[section]
        if not isinstance(entries, dict) or len(entries) != expected_count:
            found = len(entries) if isinstance(entries, dict) else "non-object"
            fail(f"{section}: expected {expected_count} labels, found {found}")
        for label, chunks in entries.items():
            if not re.fullmatch(r"[A-Za-z0-9_]+", label):
                fail(f"{section}: unsafe label {label!r}")
            if not isinstance(chunks, list) or not chunks or not all(isinstance(chunk, str) and chunk for chunk in chunks):
                fail(f"{section}:{label}: payload must be a non-empty string list")
            joined = "".join(chunks)
            if joined.count("$") != 1 or not joined.endswith("$"):
                fail(f"{section}:{label}: text must contain one final '$'")
            if FORBIDDEN_VISIBLE_RE.search(joined):
                fail(f"{section}:{label}: stale Portuguese/Emerald identity in English bank")
            for chunk in chunks:
                if '"' in chunk:
                    fail(f"{section}:{label}: raw double quote is not allowed")
                for visible in CONTROL_RE.split(chunk):
                    modeled = PLACEHOLDER_RE.sub("X" * 16, visible).replace("$", "")
                    if len(modeled) > MAX_VISIBLE_WIDTH:
                        fail(f"{section}:{label}: visible line exceeds {MAX_VISIBLE_WIDTH} chars: {modeled!r}")
    return merged


def block_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?m)^(?P<label>{re.escape(label)}:\n)"
        rf"(?P<body>(?:\t\.string \"(?:[^\"\\]|\\.)*\"\n)+)"
    )


def render_text(source: str, section: str, targets: dict[str, dict[str, list[str]]]) -> str:
    rendered = source
    for label, chunks in targets[section].items():
        pattern = block_pattern(label)
        matches = list(pattern.finditer(rendered))
        if len(matches) != 1:
            fail(f"{section}:{label}: expected one target block, found {len(matches)}")
        body = "".join(f'\t.string "{chunk}"\n' for chunk in chunks)
        match = matches[0]
        rendered = rendered[:match.start("body")] + body + rendered[match.end("body"):]
    return rendered


def mask_target_bodies(source: str, section: str, targets: dict[str, dict[str, list[str]]]) -> str:
    masked = source
    for label in targets[section]:
        pattern = block_pattern(label)
        matches = list(pattern.finditer(masked))
        if len(matches) != 1:
            fail(f"{section}:{label}: cannot mask target uniquely")
        match = matches[0]
        masked = masked[:match.start("body")] + f'\t.string "<{label}>$"\n' + masked[match.end("body"):]
    return masked


def validate_text(source: str, rendered: str, section: str, targets: dict[str, dict[str, list[str]]]) -> None:
    if mask_target_bodies(source, section, targets) != mask_target_bodies(rendered, section, targets):
        fail(f"{section}: non-target source structure changed")
    for token in REQUIRED_TOKENS[section]:
        if source.count(token) != rendered.count(token):
            fail(f"{section}: gameplay token count changed for {token}")
    for label in targets[section]:
        match = block_pattern(label).search(rendered)
        if match is None:
            fail(f"{section}:{label}: rendered target missing")
        if FORBIDDEN_VISIBLE_RE.search(match.group("body")):
            fail(f"{section}:{label}: stale visible residue survived rendering")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render all remaining reviewed Arauna story surfaces into the official English build without changing gameplay structure."
    )
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--dump-targets", action="store_true")
    args = parser.parse_args()
    if sum(bool(x) for x in (args.check, args.in_place, args.dump_targets)) > 1:
        parser.error("use only one of --check, --in-place or --dump-targets")

    targets = load_targets()
    if args.dump_targets:
        print(json.dumps(targets, ensure_ascii=False, indent=2))
        return 0

    for section, rel_path in FILES.items():
        path = ROOT / rel_path
        source = path.read_text(encoding="utf-8")
        rendered = render_text(source, section, targets)
        validate_text(source, rendered, section, targets)
        if args.in_place:
            path.write_text(rendered, encoding="utf-8")

    block_count = sum(len(entries) for entries in targets.values())
    mode = "Rendered" if args.in_place else "Validated"
    print(f"{mode} remaining Arauna story English surface: {block_count} blocks across {len(FILES)} runtime files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

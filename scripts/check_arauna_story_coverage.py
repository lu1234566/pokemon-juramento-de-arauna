#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_PATH = ROOT / "scripts" / "build_arauna.sh"
POLICY_PATH = ROOT / "scripts" / "check_english_only_policy.py"
RENDERER_MANIFEST = ROOT / "scripts" / "english_renderers.txt"
EXTRA_OVERLAY_MANIFEST = ROOT / "scripts" / "english_overlay_files_extra.txt"
POKENAV_BANK = ROOT / "data" / "text" / "arauna" / "en" / "pokenav_named_calls.json"

FINAL_GAP_BANKS = {
    "data/text/arauna/en/league_finale.json": 88,
    "data/text/arauna/en/remaining_story_surface_a.json": 30,
    "data/text/arauna/en/remaining_story_surface_b.json": 53,
    "data/text/arauna/en/remaining_story_surface_c.json": 58,
}
EXPECTED_POKENAV_RUNTIME_BLOCKS = 101
EXPECTED_FINAL_GAP_BLOCKS = 330

FINAL_GAP_OVERLAYS = {
    "data/maps/Route104/scripts.inc",
    "data/maps/Route128/scripts.inc",
    "data/maps/FallarborTown/scripts.inc",
    "data/maps/AquaHideout_1F/scripts.inc",
    "data/maps/PacifidlogTown/scripts.inc",
    "data/maps/Route114_FossilManiacsTunnel/scripts.inc",
    "data/maps/VerdanturfTown/scripts.inc",
    "data/maps/FallarborTown_CozmosHouse/scripts.inc",
    "data/maps/SootopolisCity_Gym_1F/scripts.inc",
    "data/maps/SootopolisCity_House3/scripts.inc",
    "data/maps/SootopolisCity_House5/scripts.inc",
    "data/maps/PetalburgCity_House2/scripts.inc",
    "data/maps/MossdeepCity/scripts.inc",
    "data/maps/MossdeepCity_StevensHouse/scripts.inc",
    "data/maps/MossdeepCity_Gym/scripts.inc",
    "data/maps/SeafloorCavern_Room1/scripts.inc",
    "data/maps/SeafloorCavern_Room3/scripts.inc",
    "data/maps/SeafloorCavern_Room4/scripts.inc",
    "data/maps/MeteorFalls_StevensCave/scripts.inc",
    "data/maps/VerdanturfTown_WandasHouse/scripts.inc",
    "data/text/pokedex_rating.inc",
    "data/maps/EverGrandeCity/scripts.inc",
    "data/maps/EverGrandeCity_PokemonCenter_1F/scripts.inc",
    "data/maps/EverGrandeCity_PokemonLeague_1F/scripts.inc",
    "data/maps/VictoryRoad_1F/scripts.inc",
    "data/maps/VictoryRoad_B1F/scripts.inc",
    "data/maps/VictoryRoad_B2F/scripts.inc",
    "data/maps/EverGrandeCity_SidneysRoom/scripts.inc",
    "data/maps/EverGrandeCity_PhoebesRoom/scripts.inc",
    "data/maps/EverGrandeCity_GlaciasRoom/scripts.inc",
    "data/maps/EverGrandeCity_DrakesRoom/scripts.inc",
    "data/maps/EverGrandeCity_ChampionsRoom/scripts.inc",
    "data/text/match_call.inc",
}

STAGES = {
    "01_opening_vila_anahi_ciro": {
        "render_vila_amanhecer_route101_en_checked.py",
        "render_vila_amanhecer_houses_en_checked.py",
        "render_anahi_lab_en_checked.py",
        "render_route103_ciro_en_checked.py",
        "render_vila_da_passagem_en.py",
    },
    "02_pampa_val": {
        "render_route102_pampa_en_checked.py",
        "render_pampa_elias_gym_core_en_checked.py",
        "render_pampa_gym_rooms_en_checked.py",
        "render_val_house_en_checked.py",
    },
    "03_serra_uivo_porto_redes": {
        "render_petalburg_woods_surface.py",
        "render_serra_uivo_story_en_checked.py",
        "render_porto_redes_story_en_checked.py",
    },
    "04_encruzilhada": {
        "render_route110_corridor_en_checked.py",
        "render_encruzilhada_olivia_en_checked.py",
    },
    "05_casa_cinza": {
        "render_mt_chimney_surface.py",
        "render_casa_da_cinza_nara_en_checked.py",
    },
    "06_mata_meio": {
        "render_route118_surf_corridor_en_checked.py",
        "render_route119_ciro_surface_en.py",
        "render_mata_do_meio_lidia_en.py",
        "render_mata_do_meio_interiors_en_checked.py",
    },
    "07_baia_luzes": {
        "render_baia_luzes_ciro_en.py",
        "render_baia_luzes_surface_en_checked.py",
        "render_baia_luzes_interiors_en_checked.py",
        "render_baia_luzes_fan_club_en_checked.py",
        "render_baia_luzes_department_store_en_checked.py",
        "render_baia_luzes_contest_venue_en_checked.py",
        "render_baia_luzes_museum_en_checked.py",
        "render_baia_luzes_harbor_tickets_en_checked.py",
        "render_line_ferry_ss_tidal_en_checked.py",
    },
    "08_memorial_arquivo": {
        "render_ruins_memorial_en.py",
        "render_route120_bento_en.py",
        "render_central_archive_en.py",
        "render_route121_memorial_en.py",
        "render_memorial_lower_floors_en.py",
        "render_memorial_mid_floors_en.py",
        "render_remembrancers_lower_en.py",
        "render_remembrancers_core_en.py",
    },
    "09_missoes_ceu": {
        "render_missoes_ceu_ground_floor_en.py",
        "render_missoes_ceu_confrontation_en.py",
    },
    "10_porto_sal": {
        "render_porto_sal_museum_people_en_checked.py",
        "render_porto_sal_museum_science_en_checked.py",
        "render_porto_sal_museum_confrontation_en_checked.py",
        "render_porto_sal_submersivel_en.py",
        "render_porto_sal_daily_life_en.py",
        "render_porto_sal_shipyard_en.py",
        "render_porto_sal_harbor_service_en.py",
        "render_porto_sal_story_path_en_checked.py",
    },
    "11_mboi_and_residual_story": {
        "render_mboi_climax_en.py",
        "render_aguas_mboi_en_checked.py",
        "render_remaining_story_en_checked.py",
    },
    "12_battle_circuit_postgame": {
        "render_battle_circuit_arrival_west_en_checked.py",
        "render_battle_circuit_east_district_en_checked.py",
        "render_battle_circuit_reception_gate_en_checked.py",
        "render_battle_circuit_public_services_en_checked.py",
        "render_battle_circuit_analyst_en_checked.py",
        "render_battle_circuit_lounge_identity_en_checked.py",
        "render_battle_tower_circuit_pass_en_checked.py",
        "render_circuit_pass_facilities_en_checked.py",
        "render_battle_circuit_ui_en_checked.py",
        "render_circuit_masters_en_checked.py",
        "render_battle_pike_lobby_en_checked.py",
    },
    "13_crosscutting_pokenav": {"render_pokenav_named_calls_en_checked.py"},
    "14_oath_road_league_finale": {"render_arauna_league_en_checked.py"},
}

OVERLAY_LINE_RE = re.compile(r'^\s*"(?P<path>[^"]+)"\s*$')


def fail(message: str) -> None:
    raise SystemExit(f"Arauna story coverage FAILED: {message}")


def read_manifest(path: Path) -> list[str]:
    if not path.is_file():
        fail(f"missing manifest: {path.relative_to(ROOT)}")
    entries = [
        raw.strip()
        for raw in path.read_text(encoding="utf-8").splitlines()
        if raw.strip() and not raw.lstrip().startswith("#")
    ]
    if len(entries) != len(set(entries)):
        fail(f"duplicate manifest entries: {path.relative_to(ROOT)}")
    return entries


def load_base_overlay_paths(build: str) -> set[str]:
    start = build.find("overlay_files=(")
    if start < 0:
        fail("overlay_files array is missing")
    end = build.find("\n)", start)
    if end < 0:
        fail("overlay_files array is unterminated")
    paths: set[str] = set()
    for raw in build[start:end].splitlines()[1:]:
        match = OVERLAY_LINE_RE.fullmatch(raw)
        if match:
            paths.add(match.group("path"))
    return paths


def count_bank(path: Path) -> int:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        fail(f"{path.relative_to(ROOT)} is not a JSON object")
    total = 0
    for section, entries in raw.items():
        if not isinstance(entries, dict):
            fail(f"{path.relative_to(ROOT)}:{section} is not an object")
        total += len(entries)
    return total


def count_pokenav_runtime_blocks() -> int:
    if not POKENAV_BANK.is_file():
        fail(f"missing PokéNav bank: {POKENAV_BANK.relative_to(ROOT)}")
    raw = json.loads(POKENAV_BANK.read_text(encoding="utf-8"))
    required = {"otacilio", "elias", "anahi", "bento_steven", "ciro", "val", "bento_scott", "leaders"}
    if set(raw) != required:
        fail("PokéNav bank sections do not match the canonical contract")
    leaders = raw["leaders"]
    if set(leaders) != {"Roxanne", "Brawly", "Wattson", "Flannery", "Winona", "TateLiza", "Juan"}:
        fail("PokéNav leader bank does not cover the seven non-Elias rematch leaders")
    leader_blocks = sum(len(messages) for messages in leaders.values())
    # Ciro's one canonical call payload is rendered to both legacy May/Brendan
    # label families so either player gender reaches the same rival voice.
    runtime_blocks = (
        len(raw["otacilio"])
        + len(raw["elias"])
        + len(raw["anahi"])
        + len(raw["bento_steven"])
        + 2 * len(raw["ciro"])
        + len(raw["val"])
        + len(raw["bento_scott"])
        + leader_blocks
    )
    return runtime_blocks


def main() -> int:
    build = BUILD_PATH.read_text(encoding="utf-8")
    policy = POLICY_PATH.read_text(encoding="utf-8")
    renderers = read_manifest(RENDERER_MANIFEST)
    active = set(renderers)
    overlays = load_base_overlay_paths(build) | set(read_manifest(EXTRA_OVERLAY_MANIFEST))

    if len(renderers) != 64:
        fail(f"expected 64 official English renderers, found {len(renderers)}")

    missing_stages: list[str] = []
    for stage, required in STAGES.items():
        missing = sorted(required - active)
        if missing:
            missing_stages.append(f"{stage}: {', '.join(missing)}")
    if missing_stages:
        fail("canonical stage renderer gaps: " + " | ".join(missing_stages))

    missing_overlays = sorted(FINAL_GAP_OVERLAYS - overlays)
    if missing_overlays:
        fail("final-gap files are not transactional: " + ", ".join(missing_overlays))
    for required in ("src/data/trainers.h", "src/strings.c"):
        if required not in overlays:
            fail(f"required visible identity source is not transactional: {required}")

    total_blocks = 0
    for rel_path, expected in FINAL_GAP_BANKS.items():
        path = ROOT / rel_path
        if not path.is_file():
            fail(f"missing final-gap bank: {rel_path}")
        found = count_bank(path)
        if found != expected:
            fail(f"{rel_path}: expected {expected} blocks, found {found}")
        total_blocks += found

    pokenav_blocks = count_pokenav_runtime_blocks()
    if pokenav_blocks != EXPECTED_POKENAV_RUNTIME_BLOCKS:
        fail(f"expected {EXPECTED_POKENAV_RUNTIME_BLOCKS} PokéNav runtime blocks, found {pokenav_blocks}")
    total_blocks += pokenav_blocks
    if total_blocks != EXPECTED_FINAL_GAP_BLOCKS:
        fail(f"expected {EXPECTED_FINAL_GAP_BLOCKS} final-gap blocks, found {total_blocks}")

    for renderer in (
        "render_pokenav_named_calls_en_checked.py",
        "render_remaining_story_en_checked.py",
        "render_arauna_league_en_checked.py",
    ):
        if renderer not in policy:
            fail(f"completion renderer missing from English policy: {renderer}")

    required_build_markers = (
        "Portuguese builds are disabled",
        'BUILD_DIR="build/arauna-en"',
        "scripts/english_renderers.txt",
        "scripts/english_overlay_files_extra.txt",
        "python3 scripts/check_english_only_policy.py",
        "python3 scripts/check_arauna_story_coverage.py",
    )
    for marker in required_build_markers:
        if marker not in build:
            fail(f"official build is missing completion marker: {marker}")

    stage_count = len(STAGES)
    print(
        "Arauna canonical story coverage: OK "
        f"({stage_count}/{stage_count} stages; 100%; "
        f"{len(renderers)} English renderers; "
        f"{total_blocks} final-gap runtime text blocks covered; "
        f"{len(FINAL_GAP_OVERLAYS)} final-gap source files transactional)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

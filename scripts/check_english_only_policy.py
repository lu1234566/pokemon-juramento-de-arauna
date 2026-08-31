#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RENDERER_MANIFEST = ROOT / "scripts" / "english_renderers.txt"
OVERLAY_EXTRA_MANIFEST = ROOT / "scripts" / "english_overlay_files_extra.txt"
RENDERER_RE = re.compile(r"^render_[A-Za-z0-9_]+\.py$")
OVERLAY_LINE_RE = re.compile(r'^\s*"(?P<path>[^"]+)"\s*$')

EXPECTED_RENDERER_ORDER = (
    'render_shared_trainer_names_en.py',
    'render_vila_amanhecer_route101_en_checked.py',
    'render_vila_amanhecer_houses_en_checked.py',
    'render_anahi_lab_en_checked.py',
    'render_route103_ciro_en_checked.py',
    'render_vila_da_passagem_en.py',
    'render_route102_pampa_en_checked.py',
    'render_early_route_trainers_en.py',
    'render_sea_route_trainers_en.py',
    'render_beach_and_pass_trainers_en.py',
    'render_cycling_and_daycare_trainers_en.py',
    'render_desert_and_ash_trainers_en.py',
    'render_river_and_ridge_trainers_en.py',
    'render_forest_and_memorial_trainers_en.py',
    'render_east_road_trainers_en.py',
    'render_open_sea_trainers_en.py',
    'render_far_water_trainers_en.py',
    'render_match_call_people_en.py',
    'render_pampa_elias_gym_core_en_checked.py',
    'render_pampa_gym_rooms_en_checked.py',
    'render_val_house_en_checked.py',
    'render_petalburg_woods_surface.py',
    'render_serra_uivo_story_en_checked.py',
    'render_porto_redes_story_en_checked.py',
    'render_route118_surf_corridor_en_checked.py',
    'render_route119_ciro_surface_en.py',
    'render_baia_luzes_ciro_en.py',
    'render_baia_luzes_surface_en_checked.py',
    'render_baia_luzes_interiors_en_checked.py',
    'render_baia_luzes_fan_club_en_checked.py',
    'render_baia_luzes_department_store_en_checked.py',
    'render_baia_luzes_contest_venue_en_checked.py',
    'render_baia_luzes_museum_en_checked.py',
    'render_baia_luzes_harbor_tickets_en_checked.py',
    'render_line_ferry_ss_tidal_en_checked.py',
    'render_battle_circuit_arrival_west_en_checked.py',
    'render_battle_circuit_east_district_en_checked.py',
    'render_battle_circuit_reception_gate_en_checked.py',
    'render_battle_circuit_public_services_en_checked.py',
    'render_battle_circuit_analyst_en_checked.py',
    'render_battle_circuit_lounge_identity_en_checked.py',
    'render_battle_tower_circuit_pass_en_checked.py',
    'render_circuit_pass_facilities_en_checked.py',
    'render_battle_circuit_ui_en_checked.py',
    'render_circuit_masters_en_checked.py',
    'render_battle_pike_lobby_en_checked.py',
    'render_mt_chimney_surface.py',
    'render_casa_da_cinza_nara_en_checked.py',
    'render_mata_do_meio_lidia_en.py',
    'render_mata_do_meio_interiors_en_checked.py',
    'render_ruins_memorial_en.py',
    'render_route120_bento_en.py',
    'render_central_archive_en.py',
    'render_route121_memorial_en.py',
    'render_mboi_climax_en.py',
    'render_aguas_mboi_en_checked.py',
    'render_memorial_lower_floors_en.py',
    'render_memorial_mid_floors_en.py',
    'render_remembrancers_lower_en.py',
    'render_remembrancers_core_en.py',
    'render_missoes_ceu_ground_floor_en.py',
    'render_missoes_ceu_confrontation_en.py',
    'render_porto_sal_museum_people_en_checked.py',
    'render_porto_sal_museum_science_en_checked.py',
    'render_porto_sal_museum_confrontation_en_checked.py',
    'render_porto_sal_submersivel_en.py',
    'render_porto_sal_daily_life_en.py',
    'render_porto_sal_shipyard_en.py',
    'render_porto_sal_harbor_service_en.py',
    'render_porto_sal_story_path_en_checked.py',
    'render_route110_corridor_en_checked.py',
    'render_encruzilhada_olivia_en_checked.py',
    'render_pokenav_named_calls_en_checked.py',
    'render_battle_tent_side_identity_en_checked.py',
    'render_remaining_story_en_checked.py',
    'render_arauna_league_en_checked.py',
    'render_main_readiness_residue_en_checked.py',
    # The 386 Pokedex entries. Last in the order because it owns a file no other
    # renderer touches, so it cannot overlap with anything above it.
    'render_arauna_pokedex_en.py',
)
APPROVED_ENGLISH_RENDERERS = set(EXPECTED_RENDERER_ORDER)


def fail(message: str) -> None:
    raise SystemExit(f"English-only policy violation: {message}")


def read_manifest(path: Path, pattern: re.Pattern[str] | None = None) -> list[str]:
    if not path.is_file():
        fail(f"required manifest is missing: {path.relative_to(ROOT)}")
    entries: list[str] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if pattern is not None and pattern.fullmatch(line) is None:
            fail(f"invalid manifest entry at {path.relative_to(ROOT)}:{lineno}: {line}")
        entries.append(line)
    if len(entries) != len(set(entries)):
        fail(f"duplicate entries in {path.relative_to(ROOT)}")
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
            path = match.group("path")
            if path in paths:
                fail(f"duplicate base overlay path: {path}")
            paths.add(path)
    return paths


selector = (ROOT / "data/text/birch_speech.inc").read_text(encoding="utf-8")
if 'data/text/arauna/en/birch_speech.inc' not in selector:
    fail("intro selector does not include the English bank")
if "pt_br" in selector or "ARAUNA_LANGUAGE" in selector:
    fail("intro selector still exposes a Portuguese/runtime language path")

renderers = read_manifest(RENDERER_MANIFEST, RENDERER_RE)
active_renderers = set(renderers)
unknown = sorted(active_renderers - APPROVED_ENGLISH_RENDERERS)
if unknown:
    fail("official manifest contains unapproved renderer(s): " + ", ".join(unknown))
missing = sorted(APPROVED_ENGLISH_RENDERERS - active_renderers)
if missing:
    fail("approved English renderer(s) missing from official manifest: " + ", ".join(missing))
if tuple(renderers) != EXPECTED_RENDERER_ORDER:
    fail("official English renderer order changed; review overlap semantics before reordering")
if len(renderers) != len(EXPECTED_RENDERER_ORDER):
    fail(f"expected {len(EXPECTED_RENDERER_ORDER)} approved English renderers, "
         f"found {len(renderers)}")

for renderer in renderers:
    if not (ROOT / "scripts" / renderer).is_file():
        fail(f"approved renderer file is missing: {renderer}")
    lowered = renderer.lower()
    if any(token in lowered for token in ("ptbr", "pt-br", "portuguese", "portugues")):
        fail(f"Portuguese renderer path is active: {renderer}")

extra_overlays = read_manifest(OVERLAY_EXTRA_MANIFEST)
if len(extra_overlays) != 41:
    fail(f"expected 41 final transactional overlay files, found {len(extra_overlays)}")
for rel_path in extra_overlays:
    if rel_path.startswith("/") or ".." in Path(rel_path).parts:
        fail(f"unsafe overlay path: {rel_path}")
    if not (ROOT / rel_path).is_file():
        fail(f"overlay source is missing: {rel_path}")

build = (ROOT / "scripts/build_arauna.sh").read_text(encoding="utf-8")
base_overlays = load_base_overlay_paths(build)
overlap = sorted(base_overlays & set(extra_overlays))
if overlap:
    fail("overlay path duplicated between base and final manifests: " + ", ".join(overlap))

active_build_lines = [
    line.strip()
    for line in build.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
if not any("Portuguese builds are disabled" in line for line in active_build_lines):
    fail("build wrapper does not explicitly reject Portuguese builds")
if 'BUILD_DIR="build/arauna-en"' not in build:
    fail("official build output is not the English-only target")
if 'FILE_NAME="pokemon-juramento-de-arauna-en"' not in build:
    fail("official build filename is not the English-only Arauna target")
if "scripts/english_renderers.txt" not in build:
    fail("official build is not driven by the reviewed English renderer manifest")
if "scripts/english_overlay_files_extra.txt" not in build:
    fail("official build is not loading the final transactional overlay manifest")
if 'python3 "scripts/$renderer" --in-place' not in build:
    fail("official build does not execute renderer manifest entries in-place")
if "python3 scripts/check_english_only_policy.py" not in build:
    fail("official build does not enforce the English-only gate")
if "python3 scripts/check_arauna_story_coverage.py" not in build:
    fail("official build does not enforce the canonical visible coverage gate")
for line in active_build_lines:
    if line.startswith("python3 scripts/render_"):
        fail(f"renderer bypasses the reviewed manifest: {line}")

static_runner = (ROOT / "scripts/check_arauna_static.sh").read_text(encoding="utf-8")
if "bash scripts/build_arauna.sh" not in static_runner:
    fail("static readiness does not exercise the official build wrapper")
if "check_weather_institute_1f_en.py" not in static_runner or "check_weather_institute_2f_en.py" not in static_runner:
    fail("static readiness is missing Weather Institute validation")
if "check_no_proprietary_files.sh" not in static_runner:
    fail("static readiness is missing proprietary-file validation")

workflow = (ROOT / ".github/workflows/build.yml").read_text(encoding="utf-8")
if "ptbr" in workflow.lower() or "pt-br" in workflow.lower():
    fail("CI still references a Portuguese build")
if "matrix:" in workflow:
    fail("CI still uses the former language build matrix")
if "bash scripts/check_arauna_static.sh" not in workflow:
    fail("CI repository-safety job is not driven by the canonical static-readiness entrypoint")
if "run: python3 scripts/render_" in workflow:
    fail("CI still hard-codes individual renderers instead of using the official manifest")

print(
    f"English-only policy: OK ({len(renderers)} approved English renderers in locked order; "
    f"{len(extra_overlays)} final transactional overlay files)"
)

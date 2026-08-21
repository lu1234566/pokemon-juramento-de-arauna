#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

APPROVED_ENGLISH_RENDERERS = {'render_aguas_mboi_en_checked.py',
 'render_anahi_lab_en_checked.py',
 'render_baia_luzes_ciro_en.py',
 'render_baia_luzes_surface_en_checked.py',
 'render_central_archive_en.py',
 'render_mata_do_meio_lidia_en.py',
 'render_mboi_climax_en.py',
 'render_memorial_lower_floors_en.py',
 'render_memorial_mid_floors_en.py',
 'render_missoes_ceu_confrontation_en.py',
 'render_missoes_ceu_ground_floor_en.py',
 'render_mt_chimney_surface.py',
 'render_pampa_elias_gym_core_en_checked.py',
 'render_pampa_gym_rooms_en_checked.py',
 'render_petalburg_woods_surface.py',
 'render_porto_redes_story_en_checked.py',
 'render_porto_sal_daily_life_en.py',
 'render_porto_sal_harbor_service_en.py',
 'render_porto_sal_museum_confrontation_en_checked.py',
 'render_porto_sal_museum_people_en_checked.py',
 'render_porto_sal_museum_science_en_checked.py',
 'render_porto_sal_shipyard_en.py',
 'render_porto_sal_story_path_en_checked.py',
 'render_porto_sal_submersivel_en.py',
 'render_remembrancers_core_en.py',
 'render_remembrancers_lower_en.py',
 'render_route102_pampa_en_checked.py',
 'render_route103_ciro_en_checked.py',
 'render_route119_ciro_surface_en.py',
 'render_route120_bento_en.py',
 'render_route121_memorial_en.py',
 'render_ruins_memorial_en.py',
 'render_serra_uivo_story_en_checked.py',
 'render_shared_trainer_names_en.py',
 'render_val_house_en_checked.py',
 'render_vila_amanhecer_houses_en_checked.py',
 'render_vila_amanhecer_route101_en_checked.py',
 'render_vila_da_passagem_en.py'}
RENDER_LINE_RE = re.compile(r"^python3 scripts/(?P<name>render_[A-Za-z0-9_]+\.py) --in-place$")


def fail(message: str) -> None:
    raise SystemExit(f"English-only policy violation: {message}")


selector = (ROOT / "data/text/birch_speech.inc").read_text(encoding="utf-8")
if 'data/text/arauna/en/birch_speech.inc' not in selector:
    fail("intro selector does not include the English bank")
if "pt_br" in selector or "ARAUNA_LANGUAGE" in selector:
    fail("intro selector still exposes a Portuguese/runtime language path")

build = (ROOT / "scripts/build_arauna.sh").read_text(encoding="utf-8")
active_build_lines = [
    line.strip()
    for line in build.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
if not any("Portuguese builds are disabled" in line for line in active_build_lines):
    fail("build wrapper does not explicitly reject Portuguese builds")
if 'BUILD_DIR="build/arauna-en"' not in build:
    fail("official build output is not the English-only target")

active_renderers: set[str] = set()
for line in active_build_lines:
    if "python3 scripts/render_" not in line:
        continue
    match = RENDER_LINE_RE.fullmatch(line)
    if match is None:
        fail(f"renderer invocation has an unexpected shape: {line}")
    active_renderers.add(match.group("name"))

unknown = sorted(active_renderers - APPROVED_ENGLISH_RENDERERS)
if unknown:
    fail("official build invokes unapproved renderer(s): " + ", ".join(unknown))

missing = sorted(APPROVED_ENGLISH_RENDERERS - active_renderers)
if missing:
    fail("approved English renderer(s) missing from official build: " + ", ".join(missing))

for renderer in sorted(active_renderers):
    if not (ROOT / "scripts" / renderer).is_file():
        fail(f"approved renderer file is missing: {renderer}")

for line in active_build_lines:
    lowered = line.lower()
    if "python3 scripts/render_" in line and any(
        token in lowered for token in ("ptbr", "pt-br", "portuguese", "portugues")
    ):
        fail(f"Portuguese renderer path is active: {line}")

workflow = (ROOT / ".github/workflows/build.yml").read_text(encoding="utf-8")
if "ptbr" in workflow.lower() or "pt-br" in workflow.lower():
    fail("CI still references a Portuguese build")
if "matrix:" in workflow:
    fail("CI still uses the former language build matrix")

print(f"English-only policy: OK ({len(active_renderers)} approved English renderers)")

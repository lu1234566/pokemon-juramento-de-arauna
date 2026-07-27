#!/usr/bin/env bash
set -euo pipefail

LOG_PATH="${1:-repository-safety.log}"
: >"$LOG_PATH"

run_check() {
  local label="$1"
  shift
  printf '\n== %s ==\n' "$label" | tee -a "$LOG_PATH"
  "$@" 2>&1 | tee -a "$LOG_PATH"
}

run_check "Reject proprietary files" bash scripts/check_no_proprietary_files.sh
run_check "Localized text" python3 scripts/check_localization.py
run_check "English runtime" python3 tools/arauna/validate_english_runtime.py
run_check "Packed Arauna Dex" python3 tools/arauna/validate_packed_arauna_dex.py
run_check "Vertical slice shells" python3 scripts/validate_vertical_slice_shells.py

printf '\n== Reproducible village ==\n' | tee -a "$LOG_PATH"
python3 scripts/generate_arauna_vanilla_village.py --out /tmp/arauna-village-map.bin 2>&1 | tee -a "$LOG_PATH"
cmp /tmp/arauna-village-map.bin data/layouts/AraunaMapLab/map.bin 2>&1 | tee -a "$LOG_PATH"

run_check "Arauna opening" python3 scripts/validate_arauna_opening.py
run_check "Mist Route story" python3 scripts/validate_mist_route_story.py
run_check "First Link choice" python3 scripts/validate_first_link_choice.py
run_check "First Link chamber" python3 scripts/validate_first_link_chamber.py
run_check "Vertical-slice epilogue" python3 scripts/validate_vertical_slice_epilogue.py
run_check "Porto map reuse" python3 scripts/validate_arauna_porto_reuse.py
run_check "Playtest world progression" python3 scripts/validate_playtest_feedback_world_progression.py
run_check "Serra map reuse" python3 scripts/validate_arauna_serra_reuse.py
run_check "Second ROM test" python3 scripts/validate_second_rom_test.py
run_check "Masked badge trials" python3 scripts/validate_masked_badge_trials.py
run_check "Mist Route encounters" python3 scripts/validate_mist_route_encounters.py
run_check "Capture onboarding" python3 scripts/validate_capture_onboarding.py
run_check "Safe recovery" python3 scripts/validate_safe_recovery.py
run_check "Araucaria art" python3 scripts/validate_araucaria_art.py
run_check "Canonical story spine" python3 scripts/validate_canonical_story.py
run_check "Charmap encodability" python3 scripts/validate_script_charmap.py
run_check "PNG integrity" python3 scripts/validate_png_integrity.py
run_check "Assembler directives" python3 scripts/validate_inc_syntax.py
run_check "Flag/var slot collisions" python3 scripts/validate_flag_slot_collisions.py
run_check "Sprite transparency" python3 tools/arauna/fix_sprite_transparency.py --check
run_check "Event placement" python3 scripts/validate_event_placement.py
run_check "Priority-10 NPC v3" python3 scripts/validate_priority10_npcs.py
run_check "Devcontainer JSON" python3 -m json.tool .devcontainer/devcontainer.json
run_check "Visual setup shell" bash -n .devcontainer/setup-visual-tools.sh
run_check "Visual launcher shell" bash -n scripts/open_visual_tools.sh

printf '\nAll repository-safety checks passed.\n' | tee -a "$LOG_PATH"

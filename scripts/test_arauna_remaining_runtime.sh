#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
qa=review/remaining_runtime_20261014
test -f pokemon-juramento-de-arauna-en_modern.gba
test -f pokemon-juramento-de-arauna-en_modern.elf
arm-none-eabi-nm -n pokemon-juramento-de-arauna-en_modern.elf > arauna-en.symbols.txt
cc -shared -fPIC -O2 "$qa/mgba_helper.c" -lmgba -o "$qa/mgba_helper.so"
python3 "$qa/test_tent.py"
python3 "$qa/test_bento.py"
python3 "$qa/test_castform_graphics.py"
for entry in tower factory palace arena dome verdanturf fallarbor slateport; do
    for status in 0 1 2; do
        python3 "$qa/test_frontier_snapshot.py" --expect consistent --entry "$entry" --status "$status"
    done
done
for gift in good_rod super_rod pail soot_sack coin_case powder_jar cut rock_smash basement_key; do
    python3 "$qa/test_legacy_gifts.py" "$gift" --expect retry
done
for gift in mirage_root mirage_claw underpass_root underpass_claw meteorite surf dive waterfall; do
    python3 "$qa/test_story_gifts.py" "$gift" --expect retry
    python3 "$qa/test_story_gifts.py" "$gift" --expect retry --direct
done
for gift in surf dive; do
    python3 "$qa/test_story_gifts.py" "$gift" --expect retry --ineligible
done
python3 "$qa/test_uivo.py"
python3 "$qa/test_audio.py"
python3 "$qa/test_natural_start.py"
python3 "$qa/test_natural_campaign.py"
python3 "$qa/test_campaign_to_dex.py"
python3 "$qa/test_campaign_shoes.py" --expect received
python3 "$qa/test_campaign_pampa.py"
python3 scripts/check_arauna_art_freeze.py
git diff --exit-code 46d50777a45f8fbf1f7f600516a47873ec4fc804 -- graphics/ data/tilesets/ data/layouts/ sound/

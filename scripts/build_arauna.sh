#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

language="${1:-ptbr}"
if [[ $# -gt 0 ]]; then
    shift
fi

case "${language,,}" in
    ptbr|pt-br|portuguese|portugues)
        language_id=1
        suffix=ptbr
        ;;
    en|english)
        language_id=0
        suffix=en
        ;;
    *)
        echo "Unsupported intro language '$language'. Use ptbr or en." >&2
        exit 2
        ;;
esac

overlay_files=(
    "src/strings.c"
    "data/maps/PetalburgWoods/scripts.inc"
    "data/maps/MtChimney/scripts.inc"
    "data/maps/MeteorFalls_1F_1R/scripts.inc"
    "data/maps/MtPyre_Summit/scripts.inc"
    "data/maps/AquaHideout_B1F/scripts.inc"
    "data/maps/AquaHideout_B2F/scripts.inc"
    "data/maps/SeafloorCavern_Room9/scripts.inc"
    "data/maps/SootopolisCity/scripts.inc"
    "data/maps/SkyPillar_Outside/scripts.inc"
    "src/data/items.h"
    "src/data/text/item_descriptions.h"
)
overlay_backup_dir="$(mktemp -d)"

for file in "${overlay_files[@]}"; do
    mkdir -p "$overlay_backup_dir/$(dirname "$file")"
    cp "$file" "$overlay_backup_dir/$file"
done

restore_overlays() {
    for file in "${overlay_files[@]}"; do
        cp "$overlay_backup_dir/$file" "$file"
    done
    rm -rf "$overlay_backup_dir"
}
trap restore_overlays EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

python3 scripts/render_arauna_frontier_ui.py --input "src/strings.c" --in-place
python3 scripts/render_petalburg_woods_surface.py --input "data/maps/PetalburgWoods/scripts.inc" --in-place
python3 scripts/render_mt_chimney_surface.py --input "data/maps/MtChimney/scripts.inc" --in-place
python3 scripts/render_ruinas_memorial_surface_checked.py --in-place
python3 scripts/render_arquivo_central_surface.py --in-place
python3 scripts/render_mboi_climax_surface.py --in-place
python3 scripts/render_aguas_mboi_surface.py --in-place

cpp="${CPP:-arm-none-eabi-cpp}"
cpp_with_language="${cpp} -DARAUNA_LANGUAGE=${language_id}"

make \
    MODERN=1 \
    BUILD_DIR="build/arauna-intro-${suffix}" \
    FILE_NAME="pokeemerald-intro-${suffix}" \
    CPP="${cpp_with_language}" \
    "$@"

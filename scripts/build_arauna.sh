#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Arauna is English-only. Keep accepting an explicit `en`/`english` token for
# compatibility with older commands, but reject PT-BR instead of silently
# producing a Portuguese build.
if [[ $# -gt 0 ]]; then
    case "${1,,}" in
        en|english)
            shift
            ;;
        ptbr|pt-br|portuguese|portugues)
            echo "Portuguese builds are disabled: Pokemon Juramento de Arauna is English-only." >&2
            exit 2
            ;;
    esac
fi

# Legacy Portuguese narrative renderers remain dormant. English-only overlays
# are re-enabled individually after their output has been reviewed.
overlay_files=(
    "src/data/trainers.h"
    "data/maps/PetalburgWoods/scripts.inc"
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

python3 scripts/render_shared_trainer_names_en.py --in-place
python3 scripts/render_petalburg_woods_surface.py --in-place

cpp="${CPP:-arm-none-eabi-cpp}"

make \
    MODERN=1 \
    BUILD_DIR="build/arauna-en" \
    FILE_NAME="pokemon-juramento-de-arauna-en" \
    CPP="$cpp" \
    "$@"

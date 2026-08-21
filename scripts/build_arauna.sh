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
    "src/strings.c"
    "src/data/trainers.h"
    "data/maps/LittlerootTown/scripts.inc"
    "data/maps/Route101/scripts.inc"
    "data/maps/Route102/scripts.inc"
    "data/maps/Route103/scripts.inc"
    "data/maps/OldaleTown/scripts.inc"
    "data/maps/PetalburgCity/scripts.inc"
    "data/maps/PetalburgCity_Gym/scripts.inc"
    "data/maps/PetalburgCity_WallysHouse/scripts.inc"
    "data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc"
    "data/maps/LittlerootTown_MaysHouse_1F/scripts.inc"
    "data/maps/LittlerootTown_MaysHouse_2F/scripts.inc"
    "data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc"
    "data/maps/PetalburgWoods/scripts.inc"
    "data/maps/RustboroCity/scripts.inc"
    "data/maps/RustboroCity_Gym/scripts.inc"
    "data/maps/RustboroCity_DevonCorp_1F/scripts.inc"
    "data/maps/RustboroCity_DevonCorp_2F/scripts.inc"
    "data/maps/RustboroCity_DevonCorp_3F/scripts.inc"
    "data/maps/Route116/scripts.inc"
    "data/maps/RusturfTunnel/scripts.inc"
    "data/maps/RustboroCity_PokemonSchool/scripts.inc"
    "data/maps/RustboroCity_CuttersHouse/scripts.inc"
    "data/maps/RustboroCity_Mart/scripts.inc"
    "data/maps/RustboroCity_Flat2_1F/scripts.inc"
    "data/maps/RustboroCity_Flat2_2F/scripts.inc"
    "data/maps/RustboroCity_Flat2_3F/scripts.inc"
    "data/maps/RustboroCity_House2/scripts.inc"
    "data/maps/RustboroCity_Flat1_2F/scripts.inc"
    "src/data/script_menu.h"
    "data/maps/Route104_MrBrineysHouse/scripts.inc"
    "data/maps/DewfordTown/scripts.inc"
    "data/maps/DewfordTown_Gym/scripts.inc"
    "data/maps/DewfordTown_Hall/scripts.inc"
    "data/maps/DewfordTown_House1/scripts.inc"
    "data/maps/DewfordTown_House2/scripts.inc"
    "data/maps/DewfordTown_PokemonCenter_1F/scripts.inc"
    "data/maps/GraniteCave_1F/scripts.inc"
    "data/maps/GraniteCave_StevensRoom/scripts.inc"
    "data/maps/Route109/scripts.inc"
    "data/maps/Route110/scripts.inc"
    "data/maps/Route110_SeasideCyclingRoadSouthEntrance/scripts.inc"
    "data/maps/Route110_SeasideCyclingRoadNorthEntrance/scripts.inc"
    "data/maps/MauvilleCity/scripts.inc"
    "data/maps/MauvilleCity_Gym/scripts.inc"
    "data/maps/Route118/scripts.inc"
    "data/maps/Route119/scripts.inc"
    "data/maps/Route120/scripts.inc"
    "data/maps/Route121/scripts.inc"
    "data/maps/LilycoveCity/scripts.inc"
    "data/maps/SlateportCity/scripts.inc"
    "data/maps/SlateportCity_Harbor/scripts.inc"
    "data/maps/SlateportCity_OceanicMuseum_1F/scripts.inc"
    "data/maps/SlateportCity_OceanicMuseum_2F/scripts.inc"
    "data/maps/SlateportCity_SternsShipyard_1F/scripts.inc"
    "data/maps/SlateportCity_SternsShipyard_2F/scripts.inc"
    "data/maps/MtChimney/scripts.inc"
    "data/maps/LavaridgeTown/scripts.inc"
    "data/maps/LavaridgeTown_Gym_1F/scripts.inc"
    "data/maps/FortreeCity/scripts.inc"
    "data/maps/FortreeCity_Gym/scripts.inc"
    "data/maps/MeteorFalls_1F_1R/scripts.inc"
    "data/maps/MtPyre_1F/scripts.inc"
    "data/maps/MtPyre_2F/scripts.inc"
    "data/maps/MtPyre_3F/scripts.inc"
    "data/maps/MtPyre_4F/scripts.inc"
    "data/maps/MtPyre_5F/scripts.inc"
    "data/maps/MtPyre_6F/scripts.inc"
    "data/maps/MtPyre_Summit/scripts.inc"
    "data/maps/MagmaHideout_1F/scripts.inc"
    "data/maps/MagmaHideout_2F_1R/scripts.inc"
    "data/maps/MagmaHideout_2F_2R/scripts.inc"
    "data/maps/MagmaHideout_3F_1R/scripts.inc"
    "data/maps/MagmaHideout_3F_2R/scripts.inc"
    "data/maps/MagmaHideout_4F/scripts.inc"
    "data/maps/AquaHideout_B1F/scripts.inc"
    "data/maps/AquaHideout_B2F/scripts.inc"
    "data/maps/SeafloorCavern_Room9/scripts.inc"
    "data/maps/SootopolisCity/scripts.inc"
    "data/maps/SkyPillar_Outside/scripts.inc"
    "data/maps/MossdeepCity_SpaceCenter_1F/scripts.inc"
    "data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc"
    "data/text/berries.inc"
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

python3 scripts/render_shared_trainer_names_en.py --in-place
python3 scripts/render_vila_amanhecer_route101_en_checked.py --in-place
python3 scripts/render_vila_amanhecer_houses_en_checked.py --in-place
python3 scripts/render_anahi_lab_en_checked.py --in-place
python3 scripts/render_route103_ciro_en_checked.py --in-place
python3 scripts/render_vila_da_passagem_en.py --in-place
python3 scripts/render_route102_pampa_en_checked.py --in-place
python3 scripts/render_pampa_elias_gym_core_en_checked.py --in-place
python3 scripts/render_pampa_gym_rooms_en_checked.py --in-place
python3 scripts/render_val_house_en_checked.py --in-place
python3 scripts/render_petalburg_woods_surface.py --in-place
python3 scripts/render_serra_uivo_story_en_checked.py --in-place
python3 scripts/render_porto_redes_story_en_checked.py --in-place
python3 scripts/render_route118_surf_corridor_en_checked.py --in-place
python3 scripts/render_route119_ciro_surface_en.py --in-place
python3 scripts/render_baia_luzes_ciro_en.py --in-place
python3 scripts/render_baia_luzes_surface_en_checked.py --in-place
python3 scripts/render_mt_chimney_surface.py --in-place
python3 scripts/render_casa_da_cinza_nara_en_checked.py --in-place
python3 scripts/render_mata_do_meio_lidia_en.py --in-place
python3 scripts/render_ruins_memorial_en.py --in-place
python3 scripts/render_route120_bento_en.py --in-place
python3 scripts/render_central_archive_en.py --in-place
python3 scripts/render_route121_memorial_en.py --in-place
python3 scripts/render_mboi_climax_en.py --in-place
python3 scripts/render_aguas_mboi_en_checked.py --in-place
python3 scripts/render_memorial_lower_floors_en.py --in-place
python3 scripts/render_memorial_mid_floors_en.py --in-place
python3 scripts/render_remembrancers_lower_en.py --in-place
python3 scripts/render_remembrancers_core_en.py --in-place
python3 scripts/render_missoes_ceu_ground_floor_en.py --in-place
python3 scripts/render_missoes_ceu_confrontation_en.py --in-place
python3 scripts/render_porto_sal_museum_people_en_checked.py --in-place
python3 scripts/render_porto_sal_museum_science_en_checked.py --in-place
python3 scripts/render_porto_sal_museum_confrontation_en_checked.py --in-place
python3 scripts/render_porto_sal_submersivel_en.py --in-place
python3 scripts/render_porto_sal_daily_life_en.py --in-place
python3 scripts/render_porto_sal_shipyard_en.py --in-place
python3 scripts/render_porto_sal_harbor_service_en.py --in-place
python3 scripts/render_porto_sal_story_path_en_checked.py --in-place
python3 scripts/render_route110_corridor_en_checked.py --in-place
python3 scripts/render_encruzilhada_olivia_en_checked.py --in-place

cpp="${CPP:-arm-none-eabi-cpp}"

make \
    MODERN=1 \
    BUILD_DIR="build/arauna-en" \
    FILE_NAME="pokemon-juramento-de-arauna-en" \
    CPP="$cpp" \
    "$@"

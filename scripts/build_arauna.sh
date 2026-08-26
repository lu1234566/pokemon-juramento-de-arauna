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

# Every source file temporarily rewritten by reviewed English renderers is
# backed up before rendering and restored on every exit path. The historical
# reviewed set stays explicit here; final-story additions live in the small
# append-only manifest so completion work does not risk dropping old coverage.
overlay_files=(
    "src/strings.c"
    "src/data/trainers.h"
    "src/data/text/trainer_class_names.h"
    "src/data/region_map/region_map_sections.json"
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
    "data/maps/LilycoveCity_House1/scripts.inc"
    "data/maps/LilycoveCity_House2/scripts.inc"
    "data/maps/LilycoveCity_House3/scripts.inc"
    "data/maps/LilycoveCity_House4/scripts.inc"
    "data/maps/LilycoveCity_MoveDeletersHouse/scripts.inc"
    "data/maps/LilycoveCity_CoveLilyMotel_1F/scripts.inc"
    "data/maps/LilycoveCity_CoveLilyMotel_2F/scripts.inc"
    "data/maps/LilycoveCity_PokemonCenter_1F/scripts.inc"
    "data/maps/LilycoveCity_PokemonTrainerFanClub/scripts.inc"
    "data/maps/LilycoveCity_DepartmentStore_1F/scripts.inc"
    "data/maps/LilycoveCity_DepartmentStore_2F/scripts.inc"
    "data/maps/LilycoveCity_DepartmentStore_3F/scripts.inc"
    "data/maps/LilycoveCity_DepartmentStore_4F/scripts.inc"
    "data/maps/LilycoveCity_DepartmentStore_5F/scripts.inc"
    "data/maps/LilycoveCity_DepartmentStoreRooftop/scripts.inc"
    "data/maps/LilycoveCity_ContestHall/scripts.inc"
    "data/maps/LilycoveCity_ContestLobby/scripts.inc"
    "data/maps/LilycoveCity_LilycoveMuseum_1F/scripts.inc"
    "data/maps/LilycoveCity_LilycoveMuseum_2F/scripts.inc"
    "data/maps/LilycoveCity_Harbor/scripts.inc"
    "data/maps/SSTidalCorridor/scripts.inc"
    "data/maps/SSTidalRooms/scripts.inc"
    "data/maps/BattleFrontier_OutsideWest/scripts.inc"
    "data/maps/BattleFrontier_OutsideEast/scripts.inc"
    "data/maps/BattleFrontier_ReceptionGate/scripts.inc"
    "data/maps/BattleFrontier_ScottsHouse/scripts.inc"
    "data/maps/BattleFrontier_RankingHall/scripts.inc"
    "data/maps/BattleFrontier_ExchangeServiceCorner/scripts.inc"
    "data/maps/BattleFrontier_PokemonCenter_1F/scripts.inc"
    "data/maps/BattleFrontier_Mart/scripts.inc"
    "data/maps/BattleFrontier_Lounge2/scripts.inc"
    "data/maps/BattleFrontier_Lounge3/scripts.inc"
    "data/maps/BattleFrontier_Lounge8/scripts.inc"
    "data/maps/BattleFrontier_BattleTowerLobby/scripts.inc"
    "data/maps/BattleFrontier_BattleTowerBattleRoom/scripts.inc"
    "data/maps/BattleFrontier_BattleDomeLobby/scripts.inc"
    "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.inc"
    "data/maps/BattleFrontier_BattleDomeBattleRoom/scripts.inc"
    "data/maps/BattleFrontier_BattlePalaceBattleRoom/scripts.inc"
    "data/maps/BattleFrontier_BattleArenaBattleRoom/scripts.inc"
    "data/maps/BattleFrontier_BattleFactoryBattleRoom/scripts.inc"
    "data/maps/BattleFrontier_BattlePikeLobby/scripts.inc"
    "data/maps/BattleFrontier_BattlePikeRoomNormal/scripts.inc"
    "data/maps/BattleFrontier_BattlePyramidTop/scripts.inc"
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
    "data/maps/FortreeCity_House1/scripts.inc"
    "data/maps/FortreeCity_House2/scripts.inc"
    "data/maps/FortreeCity_House3/scripts.inc"
    "data/maps/FortreeCity_House4/scripts.inc"
    "data/maps/FortreeCity_House5/scripts.inc"
    "data/maps/FortreeCity_DecorationShop/scripts.inc"
    "data/maps/FortreeCity_Mart/scripts.inc"
    "data/maps/FortreeCity_PokemonCenter_1F/scripts.inc"
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
    "data/text/frontier_brain.inc"
    "data/text/berries.inc"
    "data/text/event_ticket_1.inc"
    "data/text/event_ticket_2.inc"
    "data/text/tv.inc"
    "src/data/items.h"
    "src/data/text/item_descriptions.h"
)

while IFS= read -r file; do
    [[ -z "$file" || "$file" == \#* ]] && continue
    overlay_files+=("$file")
done < scripts/english_overlay_files_extra.txt

# A build that is killed outright cannot restore anything: EXIT, HUP, INT and
# TERM are all trapped below, but SIGKILL is not trappable and a container that
# goes away takes the build with it. What is left behind is rendered source
# sitting in the tree looking like the original - and the *next* build then
# backs that up and faithfully restores it, so one un-trappable kill bakes the
# renderers' output into the repository for good, silently.
#
# So look before backing up. These files are only ever rewritten by this
# script, so any of them differing from the commit is either that residue or an
# edit somebody has not committed, and either way it must not be mistaken for
# the original.
overlay_dirty=()
for file in "${overlay_files[@]}"; do
    if git rev-parse --verify HEAD >/dev/null 2>&1 && \
       ! git diff --quiet HEAD -- "$file" 2>/dev/null; then
        overlay_dirty+=("$file")
    fi
done
if (( ${#overlay_dirty[@]} )); then
    echo >&2
    echo "!! ${#overlay_dirty[@]} English overlay file(s) differ from the commit:" >&2
    printf '     %s\n' "${overlay_dirty[@]}" >&2
    echo "   If a previous build was killed, this is its output and it will be" >&2
    echo "   backed up as though it were the original. Restore it first:" >&2
    echo "     git checkout -- ${overlay_dirty[*]}" >&2
    echo >&2
fi

overlay_backup_dir="$(mktemp -d)"

for file in "${overlay_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        echo "English overlay source is missing: $file" >&2
        exit 3
    fi
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

python3 tools/cleanup_region_map_names.py

while IFS= read -r renderer; do
    [[ -z "$renderer" || "$renderer" == \#* ]] && continue
    if [[ ! "$renderer" =~ ^render_[A-Za-z0-9_]+\.py$ ]]; then
        echo "Invalid English renderer manifest entry: $renderer" >&2
        exit 4
    fi
    python3 "scripts/$renderer" --in-place
done < scripts/english_renderers.txt

# These gates run after every reviewed overlay has been applied and before the
# compiler is allowed to emit an official ROM.
python3 scripts/check_english_only_policy.py
python3 scripts/check_arauna_story_coverage.py

cpp="${CPP:-arm-none-eabi-cpp}"

make \
    MODERN=1 \
    BUILD_DIR="build/arauna-en" \
    FILE_NAME="pokemon-juramento-de-arauna-en" \
    CPP="$cpp" \
    "$@"

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

strings_file="src/strings.c"
strings_backup="$(mktemp)"
cp "$strings_file" "$strings_backup"

restore_strings() {
    cp "$strings_backup" "$strings_file"
    rm -f "$strings_backup"
}
trap restore_strings EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

python3 scripts/render_arauna_frontier_ui.py --input "$strings_file" --in-place

cpp="${CPP:-arm-none-eabi-cpp}"
cpp_with_language="${cpp} -DARAUNA_LANGUAGE=${language_id}"

make \
    MODERN=1 \
    BUILD_DIR="build/arauna-intro-${suffix}" \
    FILE_NAME="pokeemerald-intro-${suffix}" \
    CPP="${cpp_with_language}" \
    "$@"

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

# The legacy render_* scripts contain Portuguese surface rewrites created
# during an earlier localization pass. They are intentionally dormant in the
# official build until their Arauna-specific content is rewritten in English.
# Building directly from the repository sources prevents those PT-BR overlays
# from being injected into the ROM.

cpp="${CPP:-arm-none-eabi-cpp}"

make \
    MODERN=1 \
    BUILD_DIR="build/arauna-en" \
    FILE_NAME="pokemon-juramento-de-arauna-en" \
    CPP="$cpp" \
    "$@"

#!/usr/bin/env bash
set -euo pipefail

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
        echo "Unsupported language '$language'. Use ptbr or en." >&2
        exit 2
        ;;
esac

asflags="-mcpu=arm7tdmi --defsym MODERN=1 --defsym ARAUNA_LANGUAGE=${language_id}"

exec make \
    MODERN=1 \
    BUILD_DIR="build/arauna-${suffix}" \
    FILE_NAME="pokeemerald-${suffix}" \
    ASFLAGS="${asflags}" \
    "$@"

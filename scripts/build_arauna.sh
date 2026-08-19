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
        echo "Unsupported intro language '$language'. Use ptbr or en." >&2
        exit 2
        ;;
esac

cpp="${CPP:-arm-none-eabi-cpp}"
cpp_with_language="${cpp} -DARAUNA_LANGUAGE=${language_id}"

exec make \
    MODERN=1 \
    BUILD_DIR="build/arauna-intro-${suffix}" \
    FILE_NAME="pokeemerald-intro-${suffix}" \
    CPP="${cpp_with_language}" \
    "$@"

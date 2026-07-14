#!/usr/bin/env bash

set -Eeuo pipefail

usage() {
    cat <<'USAGE'
Uso:
  bash scripts/open_visual_tools.sh porymap
  bash scripts/open_visual_tools.sh mgba [caminho-da-ROM]
  bash scripts/open_visual_tools.sh all [caminho-da-ROM]

Se o caminho for omitido, o mGBA usa pokeemerald-ptbr.gba.
USAGE
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
    usage >&2
    exit 2
fi

readonly ACTION="$1"
readonly REPO_ROOT="$(git rev-parse --show-toplevel)"
readonly LOG_DIR="${HOME}/.cache/arauna-visual"
readonly MGBA_CONFIG_ROOT="${HOME}/.config/arauna-mgba-sdl"

export PATH="${HOME}/.local/bin:/usr/local/games:/usr/games:${PATH}"
export DISPLAY="${DISPLAY:-:1}"
export LIBGL_ALWAYS_SOFTWARE="${LIBGL_ALWAYS_SOFTWARE:-1}"
export QT_X11_NO_MITSHM="${QT_X11_NO_MITSHM:-1}"

mkdir -p "${LOG_DIR}"

open_porymap() {
    if ! command -v porymap >/dev/null 2>&1; then
        printf 'Porymap não encontrado. Execute: bash .devcontainer/setup-visual-tools.sh\n' >&2
        exit 1
    fi

    (
        cd "${REPO_ROOT}"
        nohup porymap >"${LOG_DIR}/porymap.log" 2>&1 </dev/null &
        printf '%s\n' "$!" >"${LOG_DIR}/porymap.pid"
    )
    printf 'Porymap iniciado no desktop visual. Log: %s\n' "${LOG_DIR}/porymap.log"
}

open_mgba() {
    if ! command -v mgba >/dev/null 2>&1; then
        printf 'mGBA não encontrado. Execute: bash .devcontainer/setup-visual-tools.sh\n' >&2
        exit 1
    fi

    rom_path="${1:-pokeemerald-ptbr.gba}"
    if [[ "${rom_path}" != /* ]]; then
        rom_path="${REPO_ROOT}/${rom_path}"
    fi
    if [[ ! -f "${rom_path}" ]]; then
        printf 'ROM não encontrada: %s\n' "${rom_path}" >&2
        printf 'Compile primeiro com: make ARAUNA_LANGUAGE=PORTUGUESE -j$(nproc)\n' >&2
        exit 1
    fi

    mkdir -p "${MGBA_CONFIG_ROOT}"

    # O frontend Qt apresenta uma tela branca no desktop noVNC. O frontend SDL,
    # com vídeo X11 e renderização por software, funciona no mesmo ambiente.
    # O driver de áudio dummy mantém a sincronização sem depender de ALSA.
    nohup env \
        DISPLAY="${DISPLAY}" \
        XDG_CONFIG_HOME="${MGBA_CONFIG_ROOT}" \
        SDL_VIDEODRIVER=x11 \
        SDL_RENDER_DRIVER=software \
        SDL_AUDIODRIVER=dummy \
        LIBGL_ALWAYS_SOFTWARE=1 \
        mgba \
        -3 \
        -C fullscreen=0 \
        -C pauseOnFocusLost=0 \
        -C pauseOnMinimize=0 \
        "${rom_path}" \
        >"${LOG_DIR}/mgba-sdl.log" 2>&1 </dev/null &
    printf '%s\n' "$!" >"${LOG_DIR}/mgba-sdl.pid"
    printf 'mGBA SDL iniciado em janela com %s. Log: %s\n' \
        "${rom_path}" "${LOG_DIR}/mgba-sdl.log"
}

case "${ACTION}" in
    porymap)
        open_porymap
        ;;
    mgba)
        open_mgba "${2:-}"
        ;;
    all)
        open_porymap
        open_mgba "${2:-}"
        ;;
    -h|--help|help)
        usage
        ;;
    *)
        printf 'Ação desconhecida: %s\n\n' "${ACTION}" >&2
        usage >&2
        exit 2
        ;;
esac

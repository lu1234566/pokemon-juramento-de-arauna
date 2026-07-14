#!/usr/bin/env bash

set -Eeuo pipefail

readonly PORYMAP_VERSION="${PORYMAP_VERSION:-6.3.1}"
readonly TOOLS_ROOT="${ARAUNA_TOOLS_ROOT:-${HOME}/.local/share/arauna-tools}"
readonly PORYMAP_SOURCE="${TOOLS_ROOT}/porymap-${PORYMAP_VERSION}/source"
readonly PORYMAP_BUILD="${TOOLS_ROOT}/porymap-${PORYMAP_VERSION}/build"
readonly PORYMAP_INSTALL="${TOOLS_ROOT}/porymap-${PORYMAP_VERSION}/install"
readonly LOCAL_BIN="${HOME}/.local/bin"

printf 'Instalando dependências de compilação e ferramentas visuais...\n'
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    binutils-arm-none-eabi \
    build-essential \
    ca-certificates \
    gcc-arm-none-eabi \
    git \
    libgl1-mesa-dri \
    libglx-mesa0 \
    libnewlib-arm-none-eabi \
    libpng-dev \
    mesa-utils \
    mgba-qt \
    pkg-config \
    python3 \
    qt6-base-dev \
    qt6-base-dev-tools \
    qt6-charts-dev \
    qt6-declarative-dev

mkdir -p "${LOCAL_BIN}" "${TOOLS_ROOT}"

if [[ ! -x "${PORYMAP_INSTALL}/porymap" ]]; then
    printf 'Compilando Porymap %s (isso pode levar alguns minutos)...\n' "${PORYMAP_VERSION}"
    rm -rf "${PORYMAP_SOURCE}" "${PORYMAP_BUILD}" "${PORYMAP_INSTALL}"
    mkdir -p "${PORYMAP_BUILD}" "${PORYMAP_INSTALL}"

    git clone \
        --branch "${PORYMAP_VERSION}" \
        --depth 1 \
        https://github.com/huderlem/porymap.git \
        "${PORYMAP_SOURCE}"

    if command -v qmake6 >/dev/null 2>&1; then
        qmake_command=qmake6
    elif command -v qmake >/dev/null 2>&1; then
        qmake_command=qmake
    else
        printf 'Erro: qmake do Qt 6 não foi encontrado.\n' >&2
        exit 1
    fi

    build_jobs="$(nproc)"
    if (( build_jobs > 4 )); then
        build_jobs=4
    fi

    (
        cd "${PORYMAP_BUILD}"
        "${qmake_command}" "${PORYMAP_SOURCE}/porymap.pro"
        make -j"${build_jobs}"
    )

    install -m 0755 "${PORYMAP_BUILD}/porymap" "${PORYMAP_INSTALL}/porymap"
else
    printf 'Porymap %s já está instalado; compilação ignorada.\n' "${PORYMAP_VERSION}"
fi

ln -sfn "${PORYMAP_INSTALL}/porymap" "${LOCAL_BIN}/porymap"

command -v arm-none-eabi-gcc >/dev/null
command -v mgba-qt >/dev/null
test -x "${LOCAL_BIN}/porymap"

printf '\nAmbiente visual pronto.\n'
printf 'Porymap: %s\n' "${LOCAL_BIN}/porymap"
printf 'mGBA:    %s\n' "$(command -v mgba-qt)"
printf 'Manual:  project/development/CODESPACES_VISUAL.md\n'

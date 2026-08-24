#!/usr/bin/env bash
# Fail closed if the repository ever tracks a proprietary artifact.
#
# Pokemon Juramento de Arauna is distributed as source that a user builds
# against their own legally obtained Emerald ROM. A commercial ROM image, a
# save extracted from one, or a built ROM must never enter git history.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Extensions that can only be a commercial image, a save ripped from one, or a
# build artifact. data/*.gba is the one intentional exception the .gitignore
# already carves out for graphics payloads shipped with the decomp.
patterns=(
    '*.gba' '*.gbc' '*.gb' '*.nds' '*.z64' '*.n64'
    '*.sav' '*.sa1' '*.sgm' '*.srm' '*.st[0-9]'
    'baserom*' 'BASEROM*'
)

violations=()
while IFS= read -r tracked; do
    [[ -z "$tracked" ]] && continue
    case "$tracked" in
        data/*.gba) continue ;;
    esac
    violations+=("$tracked")
done < <(git ls-files -- "${patterns[@]}")

# A build output directory must stay untracked even if it exists locally.
while IFS= read -r tracked; do
    [[ -n "$tracked" ]] && violations+=("$tracked")
done < <(git ls-files -- 'build/*')

if (( ${#violations[@]} > 0 )); then
    echo "Proprietary-file policy FAILED: these artifacts must not be tracked:" >&2
    printf '  - %s\n' "${violations[@]}" >&2
    exit 1
fi

echo "Proprietary-file policy: OK (no tracked ROM, save or build artifacts)"

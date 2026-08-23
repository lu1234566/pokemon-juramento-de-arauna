#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Run the exact official English overlay composition and every post-render gate,
# but stop before invoking the ARM toolchain. build_arauna.sh owns transactional
# backup/restore, so this leaves the checkout byte-identical after validation.
ARAUNA_VALIDATE_ONLY=1 bash scripts/build_arauna.sh

echo "Arauna static readiness: PASS (official rendered composition validated; compile intentionally skipped)."

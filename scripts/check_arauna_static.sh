#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

# Run the exact official English overlay composition and all of its post-render
# gates, while replacing only the final `make` executable with a no-op. This
# exercises the same transactional renderer order as a real build without
# requiring devkitARM in a static-validation environment.
fake_bin="$(mktemp -d)"
cleanup() {
    rm -rf "$fake_bin"
}
trap cleanup EXIT HUP INT TERM
cat > "$fake_bin/make" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' "Static readiness: compile step intentionally skipped after all official render/gate checks."
EOF
chmod +x "$fake_bin/make"

PATH="$fake_bin:$PATH" bash scripts/build_arauna.sh
python3 scripts/check_weather_institute_1f_en.py
python3 scripts/check_weather_institute_2f_en.py
bash scripts/check_no_proprietary_files.sh

echo "Arauna static readiness: PASS (official rendered composition validated; ARM compile intentionally skipped)."

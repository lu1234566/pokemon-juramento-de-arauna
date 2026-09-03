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

# Guards the Arauna overworld registry: all 46 present, the save layout
# untouched, VAR_OBJ_GFX_ID_C and _D still reserved, harness still unreachable.
python3 tools/arauna/check_overworld_registry.py

# Every one of the 386 must be catchable, or the Pokedex cannot be finished.
python3 tools/arauna/check_availability.py

# Renaming things lengthens lines, and a line past the message box is silently
# cut off on screen. The ceiling is measured from vanilla, not chosen here.
python3 tools/arauna/check_text_width.py

# ld_script.ld names all 551 song objects one at a time while
# ld_script_modern.ld matches them with a wildcard, so a song added to the
# table reaches a MODERN=1 build and silently misses a MODERN=0 one. That is
# how the twenty-one Arauna songs went unlinked.
python3 tools/arauna/check_arauna_song_link.py

# Character art the GBA reads directly, plus the wiring behind it. The trap
# the Dalva work found is that art can be perfect and still render in another
# NPC's colours, so the palette tag is checked for exclusivity too.
python3 tools/validate_arauna_character_assets.py

# Some Arauna creatures sit in slots Emerald draws differently per
# individual. ESTALAGMITE inherited Unown's twenty-eight letters and POSTE
# inherited Spinda's spot overlay; both are single designs here, and this
# refuses to let either quirk come back. It also fails if Castform's
# machinery is disabled, since TUIM is deliberately deferred, not switched off.
python3 tools/arauna/check_special_species.py

# Sixteen OBJ palette banks is hardware capacity, not what an object event may
# use. This keeps the reserve boundary, the exclusive-palette pool and the
# audited same-slot pairs honest, and refuses the old 16 + PALSLOT spelling.
python3 tools/arauna/check_overworld_palette_capacity.py

# The two factions wear inherited Aqua and Magma slots, so their symbols still
# say Aqua and Magma and a graphic sliding back to vanilla art would read as
# normal in a diff. This checks the visual wiring instead of the words.
python3 tools/arauna/check_faction_visual_identity.py

echo "Arauna static readiness: PASS (official rendered composition validated; ARM compile intentionally skipped)."

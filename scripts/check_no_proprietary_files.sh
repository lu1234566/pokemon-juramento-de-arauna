#!/usr/bin/env bash

set -euo pipefail

failed=0

while IFS= read -r path; do
    case "$path" in
        data/mb_berry_fix.gba|data/mb_colosseum.gba|data/mb_ereader.gba)
            # Tracked upstream multiboot payloads required by the engine.
            continue
            ;;
        *.gba|*.sav|*.state|*.sgm|*.bps|*.ups|*.ips|*.xdelta|*.zip|*.7z|*.env|.env.*)
            printf 'Blocked tracked file: %s\n' "$path" >&2
            failed=1
            ;;
    esac
done < <(git ls-files)

if (( failed )); then
    printf 'Remove proprietary, generated or secret files from Git before continuing.\n' >&2
    exit 1
fi

printf 'Repository safety check passed.\n'

# Arauna faction placeholder cleanup

The expanded-placeholder table still exposes four Emerald faction identities in player-facing dynamic text although the story, battle names and overworlds already use Arauna's canonical cast.

## Replacement

- AQUA -> HORIZONTE
- MAGMA -> LEMBRANTES
- ARCHIE -> OTACILIO
- MAXIE -> LUZIA

Existing CIRO and ARAUNA DEX substitutions stay in the same deterministic validator.

## Safety boundary

Only visible values in `src/strings.c` are targeted. Backing Emerald symbol names remain untouched as implementation skeleton. No event IDs, trainer data, map IDs, flags, saves, route order or progression change.

## Validation

This branch starts from canonical `main` after #98 and supersedes stale #97/#99. The shared cleanup workflow already invokes `cleanup_system_ui_identity.py` and stages `src/strings.c`. Full custom Emerald ROM CI remains the preferred build gate when GitHub Actions runners are available; the deterministic generator/check is the source-level gate for this exact replacement set.

# Arauna faction placeholder cleanup

The global expanded-placeholder table still exposes four Emerald faction identities in player-facing dynamic text even though story and battle surfaces already use Arauna's canonical cast.

## Replacement

This lot extends the existing deterministic system/UI identity cleanup with four canonical substitutions:

- AQUA -> HORIZONTE;
- MAGMA -> LEMBRANTES;
- ARCHIE -> OTACILIO;
- MAXIE -> LUZIA.

The existing CIRO and ARAUNA DEX substitutions remain part of the same validator.

## Safety boundary

Only string values in `src/strings.c` are targeted. The backing symbol names remain unchanged as Emerald implementation skeleton. No faction event IDs, trainer data, map IDs, flags, saves, encounter logic, route order or badge progression are altered.

## Validation state

This activation branch was rebuilt from canonical `main` after the Val household merge, superseding stale PR #97. The shared cleanup workflow already invokes `cleanup_system_ui_identity.py` and stages `src/strings.c`. Source generation/check and a full custom Emerald ROM build remain mandatory whenever GitHub Actions runners are available; until then the PR must not be confused with a completed full-CI validation.

# Arauna faction placeholder cleanup plan

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

## Validation

The active branch starts from the current canonical `main`. The shared deterministic runner already invokes `cleanup_system_ui_identity.py` and stages `src/strings.c`; source is generated/verified on the branch. Merge remains blocked until GitHub Actions can complete both the cleanup gate and a successful full custom Emerald ROM CI on the final head.

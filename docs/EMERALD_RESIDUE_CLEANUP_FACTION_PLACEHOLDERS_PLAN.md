# Arauna faction placeholder cleanup plan

The global expanded-placeholder table still exposes four Emerald faction identities in player-facing dynamic text even though story and battle surfaces already use Arauna's canonical cast.

## Prepared replacement

This lot extends the existing deterministic system/UI identity cleanup with four canonical substitutions:

- AQUA -> HORIZONTE;
- MAGMA -> LEMBRANTES;
- ARCHIE -> OTACILIO;
- MAXIE -> LUZIA.

The existing CIRO and ARAUNA DEX substitutions remain part of the same validator.

## Safety boundary

Only string values in `src/strings.c` are targeted. The backing symbol names remain unchanged as Emerald implementation skeleton. No faction event IDs, trainer data, map IDs, flags, saves, encounter logic, route order or badge progression are altered.

## Integration sequencing

This preparation branch is intentionally not a merge candidate. After the current Val household gate lands on green `main`, recreate this tool/document on a fresh `narrative/emerald-residue-run-*` branch, let the shared deterministic runner generate `src/strings.c`, then require a completed successful full custom Emerald ROM CI on a final user-authored head before merge.

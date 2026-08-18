# Emerald residue cleanup — lot 10 (battle message)

This lot removes the last high-visibility Professor Birch identity that bypasses map dialogue and lives directly in the battle-message layer.

## Visible text corrected

The rescue battle message `PROF. BIRCH: Don't leave me like this!` becomes `ANAHI: Nao me deixe aqui!` while the underlying battle setup and script IDs remain untouched.

## Infrastructure dependency

The reusable residue-cleanup runner stages `src/battle_message.c` in addition to map/text sources. The dedicated validator accepts only the Arauna-native line and rejects the original Birch string.

## Safety boundary

No battle mechanics, move strings, trainer data, encounter logic, map events, flags, variables, saves or progression are modified. This lot changes exactly one player-facing static battle string and requires a full ROM build before merge.

## Post-generation validation

The cleanup runner successfully generated and verified the source replacement. A user-authored head commit is used to trigger a fresh full ROM CI run on the generated source before merge.

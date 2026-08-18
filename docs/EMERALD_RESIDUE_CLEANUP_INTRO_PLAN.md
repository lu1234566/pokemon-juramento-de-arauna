# Arauna opening-professor cleanup plan

The new-game professor speech is still the untouched Emerald Birch introduction, including `My name is BIRCH`, `LITTLEROOT`, and the generic Hoenn-era explanation. Because this is the first narrative text a player sees, it is a high-priority visible identity mismatch.

## Prepared replacement

The deterministic tool rewrites only the nine existing `gText_Birch_*` text blocks while preserving their labels and the character-creation flow:

- Birch's player-facing identity becomes Professora Anahi;
- the region is explicitly Arauna;
- the speech introduces VINCULOS and DESENCANTO without changing gameplay;
- the boy/girl and name prompts are localized;
- the destination becomes Vila Amanhecer;
- the final prompt directs the player to Anahi's laboratory.

## Safety boundary

The internal `gText_Birch_*` symbol names remain unchanged. No intro scene state, gender selection, player naming, save initialization, graphics, maps, flags, warps or progression logic are changed.

## Integration sequencing

This branch was recreated directly from the newest green `main` after the Vila Amanhecer cleanup. The deterministic generator is wired into the shared residue pipeline, and merge is allowed only after generated source, a final user-authored validation commit, the cleanup check and the full custom Emerald ROM build all pass on the exact final head.

Final validation trigger: the generated `birch_speech.inc` source is now present on this branch; this commit exists solely to force both deterministic cleanup verification and the full custom Emerald ROM build against the exact final user-authored head.

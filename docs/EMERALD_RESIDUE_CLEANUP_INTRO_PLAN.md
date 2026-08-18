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

After the currently running Vila Amanhecer cleanup reaches green `main`, this prepared branch should be rebased/reset onto that base, converted to the narrative residue pipeline, generated, `--check` validated and full-ROM CI validated before merge.

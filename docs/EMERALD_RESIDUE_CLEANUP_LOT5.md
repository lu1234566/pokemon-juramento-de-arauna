# Emerald residue cleanup — lot 5

This lot aligns the remaining high-visibility Professor Birch identity in shared UI/text paths with Professora Anahi, whose laboratory dialogue is already Arauna-native.

## Visible text corrected

- PokéNav registration dialogue now speaks as Anahi;
- PokéNav registration confirmation names `PROF. ANAHI`;
- the Pokédex rating entry point speaks as Anahi;
- the visible PokéNav contact becomes `PROF. ANAHI` / `PESQUISADORA`;
- the Hall of Fame Pokédex attribution now names Anahi;
- the opening rescue prompt now names Anahi and uses the correct feminine reference.

## Progression preserved

Internal Birch symbols, Match Call indexes, flags, Pokédex rating logic and event conditions remain unchanged. This is a player-facing identity/text replacement only.

## Verification scope

The deterministic shared-text cleanup now verifies the seven Seu Bento Match Call blocks plus three Anahi text blocks and six exact visible constants across `data/text` and `src/strings.c`.

## Deferred residue

Unused/internal strings such as `MatchCall_Text_UnusedProfBirch` and code-facing symbols retain their Emerald names for now because they are not surfaced in normal play. They can be handled in a later dead-code/unused-text cleanup without mixing that work into this player-facing lot.

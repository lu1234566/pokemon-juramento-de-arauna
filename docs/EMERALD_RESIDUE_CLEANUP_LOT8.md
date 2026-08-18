# Emerald residue cleanup — lot 8

This lot polishes the player's home and Ciro's household in the opening area while preserving the complete Emerald event graph underneath.

## Player home

The opening household dialogue now consistently belongs to Arauna:

- the player's mother is surfaced as `MAE` instead of the remaining English `MOM` text;
- Elias replaces generic `DAD` references and the television report now points to `PAMPA DA ESPERA`;
- Professora Anahi is referenced with the correct identity and context;
- the PokéNav conversation no longer attributes the system to Devon;
- the incorrect generic Ciro line that had leaked into the mother's TV scene is removed;
- the early home/rest/running-shoes dialogue is translated and made context-appropriate.

## Ciro household

The rival household no longer inherits Professor Birch's vanilla family setup:

- Ciro's family describes his Horizonte sponsorship rather than a professor father;
- Route 103 references are presented as Ciro's field work;
- the first Ciro meeting is now an actual introduction instead of a repeated later-arc monologue;
- the rival-room Poké Ball is explicitly Ciro's;
- remaining high-visibility English text in the targeted household blocks is removed.

## Safety boundary

Only existing `.string` blocks were rewritten. Internal May/Brendan/Birch labels remain intact because the engine still uses them as functional slots.

This lot does not change coordinates, object events, gender branches, warps, flags, variables, movement scripts, item grants, trainer data, save structures or progression.

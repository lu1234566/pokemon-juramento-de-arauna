# Emerald residue cleanup — lot 9

This lot targets the exterior/opening dialogue of Vila Amanhecer (`LittlerootTown`) after the Littleroot household cleanup and Arauna battle-name pass reached the canonical main branch.

## Visible cleanup

- opening arrival dialogue names Vila Amanhecer instead of Littleroot Town;
- running-shoes sequence is translated and contextualized around Mae, Elias and Anahi;
- the child guarding the route gives Arauna-native warnings rather than vanilla English tutorial dialogue;
- the NPC currently displaying Anahi's first-person monologue is restored to an NPC-appropriate description of her field work;
- the rescue reaction correctly refers to the player having helped Anahi;
- the laboratory sign becomes `LABORATORIO DE CAMPO / PROFESSORA ANAHI`;
- the rival-house sign becomes `CASA DE CIRO` instead of carrying the Birch household identity;
- the postgame Anahi prompt becomes an actual invitation to the laboratory rather than a recycled generic monologue.

## Safety boundary

The deterministic tool changes only existing `.string` blocks in `data/maps/LittlerootTown/scripts.inc`. No labels, event commands, coordinates, warps, flags, variables, object events, movement, item grants or progression logic are modified.

## Validation gate

The cleanup runner applies the lot, verifies every target block, then the normal PR CI performs a full custom Emerald ROM build. Merge is allowed only after both gates succeed.

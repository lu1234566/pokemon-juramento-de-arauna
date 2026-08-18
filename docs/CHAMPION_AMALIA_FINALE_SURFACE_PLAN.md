# Champion Amalia finale visible-surface cleanup

The Champion battle already uses Amalia's Arauna identity in the opening, but the mandatory finale remains internally inconsistent: the defeat line is untouched Wallace English, the Hall of Fame handoff literally starts with `WALLACE:`, and Ciro/Anahi/Amalia repeat unrelated story monologues rather than reacting to the championship result.

## Prepared finale

The existing event graph is kept intact while its string blocks become contextual:

- Amalia frames the final challenge and gives a short battle-safe defeat line;
- after the battle she recognizes the new Champion without pretending the League's historical debts vanished;
- Ciro arrives too late to advise the player and reacts to the victory;
- Professora Anahi arrives, rates the Pokédex through the same special and congratulates the player;
- Amalia escorts the player into the Hall of Fame while Anahi and Ciro wait outside.

Both inherited May/Brendan branches intentionally display Ciro text so the existing gender-dependent event structure can remain untouched.

## Safety boundary

Only existing `.string` blocks in `EverGrandeCity_ChampionsRoom/scripts.inc` are targeted. `TRAINER_WALLACE`, battle music, rival setup, Pokédex rating call, movements, objects, map tiles, Hall of Fame warp, flags, saves and game-clear progression remain unchanged.

This is preparation-only while GitHub Actions quota is exhausted. Activate from the newest canonical main after the badge PR stabilizes; Codespaces remains last resort.

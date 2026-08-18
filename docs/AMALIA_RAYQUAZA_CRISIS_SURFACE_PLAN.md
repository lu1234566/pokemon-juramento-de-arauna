# Amalia / Rayquaza crisis visible-surface cleanup

The mandatory late-game crisis still uses the inherited Wallace surface almost verbatim in the Cave of Origin, then continues into a mixed Amalia/Wallace scene outside Sky Pillar. The event graph itself is useful and must remain Emerald: the player is asked where Rayquaza is, the correct answer advances the state, the guide opens the tower and later returns to the city.

## Prepared Arauna surface

The same structural role is presented as AMALIA throughout:

- in the Cave of Origin she identifies the Groudon/Kyogre crisis and the old records about Rayquaza;
- the four existing menu choices become `CAVERNA ORIGEM`, `MEMORIAL NOMES`, `TORRE JURAMENTO` and `NAO LEMBRO`;
- wrong answers receive contextual responses instead of Wallace/Hoenn dialogue;
- choosing Torre Juramento advances the exact same event state;
- outside Torre Juramento, Amalia opens the entrance, reacts to the worsening crisis and returns to Águas de M'Boi while the player continues upward.

Pokémon species names Groudon, Kyogre and Rayquaza are intentionally preserved.

## Safety boundary

Only player-facing string blocks in `data/maps/CaveOfOrigin_B1F/scripts.inc`, `data/maps/SkyPillar_Outside/scripts.inc` and four exact menu values in `src/strings.c` are targeted. The backing `gText_*` symbols, `MULTI_WHERES_RAYQUAZA`, `FLAG_WALLACE_GOES_TO_SKY_PILLAR`, Wallace object/event labels, map IDs, state variables, movements, weather control, door metatiles, saves and progression remain untouched.

This is preparation-only while GitHub Actions quota is exhausted. Activate from the newest canonical main after the badge PR stabilizes; Codespaces remains last resort.

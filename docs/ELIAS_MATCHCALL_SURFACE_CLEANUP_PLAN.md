# Elias father / Match Call visible-residue cleanup

The inherited Norman contact still leaks the Emerald identity through `DAD`, `NORMAN`, Rustboro/Petalburg references and a Magma Emblem call. Route 105 also contains the first father PokéNav call as untouched English text naming Devon and Mr. Stone.

## Canonical reinterpretation

The same structural father contact becomes ELIAS throughout the player-visible surface. Its existing calls keep their timing and progression purpose but are rewritten around Pampa da Espera, Serra do Uivo, the Lembrantes, Elias's relationship with the player and his connection to the decisions behind M'Boi.

The PokéNav card becomes:

- name: `ELIAS`
- description: `PAI DE {PLAYER}`

The inherited Route 105 labels remain unchanged but their visible text registers ELIAS instead of DAD NORMAN and removes Devon/Mr. Stone wording.

## Safety boundary

Only existing text blocks in `data/text/match_call.inc`, two visible Route 105 string blocks and two `src/strings.c` values are targeted. Internal Norman/Dad labels, call conditions, battle/rematch state, badges, trainer teams, flags, map IDs, saves, routes and progression are untouched.

## Activation

Activate on a fresh cleanup branch from the newest green `main` once GitHub Actions runners execute normally again. Wire the tool into the shared deterministic runner, generate all target files, run `--check`, add a final user-authored validation commit and require a successful full custom Emerald ROM build before merge.

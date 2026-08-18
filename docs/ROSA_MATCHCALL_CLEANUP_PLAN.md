# Rosa Match Call visible-identity cleanup

The player's mother already uses the Arauna overworld identity integrated as Rosa, but her PokéNav card and three calls still display the vanilla `MOM` identity and Petalburg-era dialogue.

## Replacement

The same structural mother contact becomes ROSA, with three localized calls consistent with the Arauna opening, Elias and Pampa da Espera.

PokéNav card:

- `MOM` -> `ROSA`
- `CALM & KIND` -> `MAE DE {PLAYER}`

## Safety boundary

Only three existing Match Call string blocks and two visible `src/strings.c` values change. The mother call index, call conditions, map objects, home events, flags, saves and progression remain untouched.

## Activation

This preparation was recreated from the current canonical `main` while GitHub Actions quota is exhausted. Activate later through the deterministic residue runner; Codespaces is reserved for last-resort execution/build validation.

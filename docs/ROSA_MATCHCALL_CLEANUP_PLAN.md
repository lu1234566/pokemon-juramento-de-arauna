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

Activate from the newest green `main` after GitHub Actions runners resume executing jobs. Wire the deterministic tool into the shared residue cleanup, generate/check the two source files, add a final validation commit and require the full custom Emerald ROM CI before merge.

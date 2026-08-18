# Val arc visible-residue cleanup plan

The Val/Wally functional slot is already structurally integrated and uses Val graphics, but several player-facing scenes still mix three different states: untouched Emerald dialogue naming Wally and Hoenn locations, repeated placeholder-like Val monologues copied into unrelated speakers, and Arauna-native lines.

## Prepared scope

This lot follows Val through the existing Emerald event graph without changing that graph:

- Route 102 capture tutorial and route signs;
- Pampa da Espera exterior family text and Val-house sign;
- Encruzilhada challenge scene, uncle dialogue, PokéNav registration and the inherited Scott observer beat;
- Vale do Silêncio household/cousin follow-up dialogue;
- Estrada do Juramento Val battles;
- seven Val Match Call messages.

## Canonical visible identities

- Wally -> Val;
- Oldale Town -> Vila da Passagem;
- Petalburg City -> Pampa da Espera;
- Mauville -> Encruzilhada / Olívia context;
- Verdanturf -> Vale do Silêncio;
- Victory Road / Ever Grande story reference -> Estrada do Juramento;
- inherited Scott observer speech -> generic VIAJANTE role, matching the Route 119 surface treatment.

## Safety boundary

Only existing player-facing string blocks are replaced. Internal `Wally`, `Petalburg`, `Mauville`, `Verdanturf`, `VictoryRoad` and `Scott` symbol names remain untouched as Emerald implementation skeleton. No trainer IDs, parties, battle scripts, HM/TM grants, flags, variables, map IDs, coordinates, warps, object IDs, save structures, route order or badge progression change.

## Activation

Keep this preparation branch out of the active merge queue while PR #96 is waiting for GitHub Actions capacity. After the Val household lot is merged, recreate/copy this deterministic tool onto a fresh `narrative/emerald-residue-run-*` branch from the newest green `main`, wire it into the shared cleanup runner, generate the source, then require both deterministic `--check` and a full custom Emerald ROM CI build on the final head before merge.

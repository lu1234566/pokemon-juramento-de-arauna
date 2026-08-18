# Val household visible-residue cleanup plan

The Val/Wally story slot already uses Val in several rewritten scenes, but the family house still mixes first-person Val monologues with untouched English dialogue naming WALLY and VERDANTURF. That makes the household visibly inconsistent even though the event graph is correct.

## Prepared replacement

Eight existing text blocks in `PetalburgCity_WallysHouse` are rewritten so the people speaking sound like Val's parents, not Val himself. The HM Surf grant remains structurally identical.

Visible identities become:

- Wally -> Val;
- Verdanturf Town -> Vale do Silencio;
- Ever Grande reference -> Estrada do Juramento;
- family dialogue is localized and context-appropriate.

## Safety boundary

Only `.string` bodies change. The house map, local object IDs, Wally-named internal labels, flags, HM Surf item grant, event state and progression remain untouched.

## Integration sequencing

This activation branch starts from the latest green `main`, wires the tool into the shared deterministic runner, generates/checks the eight blocks and requires full-ROM CI before merge.

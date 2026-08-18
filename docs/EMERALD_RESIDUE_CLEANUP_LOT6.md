# Emerald residue cleanup — lot 6

This lot removes the remaining high-visibility May/Brendan identity from two Ciro route scenes whose core rival dialogue was already Arauna-native.

## Visible text corrected

- Route 104 PokéNav registration no longer names May, Brendan or Devon;
- both gender-routed registration confirmations now surface Ciro;
- Route 110 ITEMFINDER explanations now speak as Ciro instead of May/Brendan.

## Progression preserved

The original May/Brendan event branches, trainer IDs, battle selection, music slots, flags and rival progression remain unchanged internally. Both branches intentionally surface the same Ciro identity to the player.

## Verification scope

The dedicated route validator verifies six exact visible text blocks across `data/maps/Route104/scripts.inc` and `data/maps/Route110/scripts.inc`, rejecting `MAY:`, `BRENDAN:`, old registration names and `DEVON` inside those targets.

## Safety boundary

No coordinates, warps, item grants, flags, variables, trainer teams, movement scripts, battle flow or save-facing structures are changed.

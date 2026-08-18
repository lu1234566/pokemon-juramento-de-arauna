# Emerald residue cleanup — lot 3

This lot removes the remaining high-visibility STEVEN identity leaks from map dialogue already assigned narratively to SEU BENTO.

## Visible text corrected

- Granite Cave contact registration, registration confirmation, departure line and full-bag response;
- the Dive handoff in Bento's house at Missoes do Ceu;
- the rare-rock display that still credited STEVEN;
- the crisis guidance line in M'Boi that still surfaced STEVEN.

## Verification scope

The deterministic cleanup now verifies 22 visible map text blocks: the eight campaign sign identities, seven Serra do Uivo/Rustboro identity blocks and seven Seu Bento/Steven replacements. The generated patch for this lot touches only the three intended map script files.

## Safety boundary

Only existing `.string` blocks are replaced. Internal Emerald labels such as `...Steven`, flags, variables, local IDs, movement scripts, coordinates, warps, item IDs and progression remain untouched.

This lot deliberately leaves the global Match Call text table for a later batch, because the current generator workflow stages `data/maps` only. Keeping that change separate prevents a broader source-scope expansion from being mixed into this map-dialogue cleanup.

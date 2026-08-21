# Route 118 — post-SURF English corridor

## Scope

This pass closes the first mandatory corridor opened after the fifth Gym and HM SURF.

The earlier Pampa da Espera work already covers:

- ELIAS and the COMPASS BADGE;
- the seven inherited Gym challenge rooms;
- VAL's family house and the HM SURF gift.

The first real uncovered story gap after that point was Route 118.

This layer owns exactly nine local Route 118 text blocks in `data/maps/Route118/scripts.inc`.

## Story continuity

Route 118 is treated as the moment the world physically opens after SURF.

The river stops being only a border and becomes a road, but the writing deliberately avoids equating a new route with automatic safety.

The inherited Steven slot remains SEU BENTO on the visible surface. His short encounter reinforces his role as a recorder: when a name fades from speech, he writes it down not to replace living memory, but to leave a trail back to it.

The route now points west to **ENCRUZILHADA CENTRAL** and north toward **ROUTE 119 / MATA DO MEIO**, connecting directly into the already-active Route 119 Ciro/Seu Bento surface.

## GOOD ROD and SURF

The inherited GOOD ROD reward is unchanged mechanically. Its visible dialogue is rewritten around patience and reading the water rather than the vanilla repeated `good` joke.

The local SURF explanation is also rewritten to make the new traversal ability feel like a story transition while keeping the move and field mechanics untouched.

## Preserved internals

The checked renderer verifies that the following do not change:

- `ITEM_GOOD_ROD`;
- `FLAG_RECEIVED_GOOD_ROD`;
- `VAR_ROUTE118_STATE`;
- `LOCALID_ROUTE118_STEVEN`;
- Route 118 abnormal-weather variables and east/west weather locations;
- `TRAINER_ROSE_1` and `TRAINER_DALTON_1`;
- both inherited Match Call registrations.

No trainer parties, battle callbacks, rematches, map geometry, warps, saves, movement or weather logic are changed.

Trainer-battle dialogue stored in the shared global `data/text/trainers.inc` bank is intentionally outside this pass to avoid broad unrelated side effects.

## Renderer contract

`scripts/render_route118_surf_corridor_en_checked.py`:

- reads a plain UTF-8 JSON bank;
- requires exactly nine reviewed labels;
- owns only consecutive `.string` records directly under those labels plus historical physical continuation lines;
- accepts either clean source or the exact already-rendered body;
- validates conservative 32-character visible width;
- requires proper `$` termination;
- masks all target bodies and proves non-dialogue source structure is byte-stable;
- preserves explicit progression-token counts;
- rejects old `MAUVILLE CITY` and Portuguese Seu Bento residue inside owned blocks.

## Validation

Validated without GitHub Actions or Codespaces:

- Python syntax: PASS;
- JSON contract: 9/9;
- conservative visible-width check: PASS;
- synthetic `--check -> --in-place -> --check`: PASS;
- historical physical `.string` continuation: PASS;
- adjacent assembler-directive boundary sentinel: PASS;
- story identity contract for SEU BENTO / SURF / GOOD ROD / ENCRUZILHADA CENTRAL / MATA DO MEIO: PASS.

A full GBA ROM toolchain build is not part of this pass.

PR #58 remains outside scope.

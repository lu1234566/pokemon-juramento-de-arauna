# Route 110 — Porto do Sal to Encruzilhada, English-only

This pass closes the next mandatory corridor after Porto do Sal while preserving the inherited Emerald route graph and bike challenge.

## Scope

`render_route110_corridor_en_checked.py` owns 47 player-facing blocks across:

- `data/maps/Route110/scripts.inc` — 43 blocks;
- `data/maps/Route110_SeasideCyclingRoadSouthEntrance/scripts.inc` — 2 blocks;
- `data/maps/Route110_SeasideCyclingRoadNorthEntrance/scripts.inc` — 2 blocks.

It covers the HORIZON field staff, Ciro encounter, Anahi encounter, route residents, public signs, cycling time-trial feedback and both Cycling Road gates. Trainer battle dialogue stored in the shared trainer text bank remains a separate surface and is not silently rewritten here.

## Ciro after Porto do Sal

Ciro does not leave HORIZON. He calls the forced museum operation a consent failure and refuses to defend it, but he also refuses the conclusion that one bad decision makes measurement itself useless. His battle with the protagonist therefore continues the first-chapter conflict: Ciro wants better models and better protocol; the protagonist keeps testing what measurements omit.

Both inherited May/Brendan rival slots are required to render exactly the same Ciro dialogue.

The inherited `ITEM_ITEMFINDER` reward remains mechanically unchanged. Ciro presents it as a useful tool that should still be checked rather than obeyed blindly.

## Anahi

Anahi states in English that she helped create the early BOND sensors and that silence about misuse would make the mistake partly hers. The inherited Birch Match Call registration is reinterpreted as a field-context channel rather than a POKéDEX-rating service.

She also confirms that Ciro is angry about Porto do Sal but has not abandoned HORIZON.

## HORIZON and the road

The four inherited Aqua field NPCs become a regrouping HORIZON unit. Their dialogue shows uncertainty after Porto do Sal: they still believe they are meant to help, but at least one explicitly says force was not part of the briefing. This keeps the organization internally varied instead of turning every employee into the same moral position.

A layered-graffiti sign carries competing slogans — `HORIZON SAVES`, `LEMBRANTES REMEMBER`, and `ASK WHO CHOSE` — without making either faction the automatic answer.

## Cycling Road

The inherited Cycling Road remains fully functional and is surfaced as **COAST CYCLING ROAD**. MACH BIKE time trials, collision/time scoring, north/south gate checks, ACRO BIKE exclusion and all state variables remain unchanged.

Public route signs now connect PORTO DO SAL to ENCRUZILHADA while preserving Route 103 access and the Trick House attraction.

## Preserved internals

The renderer explicitly checks, among other tokens:

- `ITEM_ITEMFINDER`;
- `VAR_ROUTE110_STATE`;
- `FLAG_ENABLE_PROF_BIRCH_MATCH_CALL`;
- `VAR_REGISTER_BIRCH_STATE`;
- `VAR_CYCLING_CHALLENGE_STATE`;
- `FLAG_SYS_CYCLING_ROAD`;
- representative May/Brendan Route 110 trainer IDs.

No battle, trainer party, object movement, route trigger, bike gate, warp or save-format logic is changed.

## Safety

The authored surface is stored in plain UTF-8 JSON. The renderer requires exactly 47 labels, only replaces consecutive `.string` lines directly below exact labels, accepts either the reviewed source or already-rendered state, uses a conservative 16-character substitution for dynamic variables during the 32-character width check, masks all target blocks to prove non-dialogue structure is unchanged, and rejects the tracked Portuguese/Hoenn residue.

PR #58 remains outside scope. No art dependency is introduced.

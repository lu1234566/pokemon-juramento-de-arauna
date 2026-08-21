# Porto do Sal — mandatory story path, English-only

This pass closes the high-visibility gaps left between the existing Porto do Sal English renderers without rewriting the museum, shipyard, harbor-service or daily-life work that is already active.

## Scope

`render_porto_sal_story_path_en_checked.py` owns 17 player-facing blocks in `data/maps/SlateportCity/scripts.inc`:

- 11 civic/location signs;
- 6 inherited Scott surfaces, presented as Seu Bento.

The public signs now consistently expose PORTO DO SAL, its shipyard, harbor, market, museum, Fan Club, Name Rater and Battle Tent. Legacy SLATEPORT/LILYCOVE/S.S. TIDAL identity is removed only from these blocks.

## Seu Bento and the second POKéNAV registration

The player already registers Seu Bento through the inherited Steven event in Gruta das Vozes. Emerald later runs an independent Scott Match Call registration in Porto do Sal. The event graph and both internal flags remain intact, but the visible script no longer pretends that Bento and the player are exchanging numbers for the first time.

Instead, Bento says that he is enabling his **field route** in the POKéNAV. This gives the second inherited registration a visible purpose without changing save data or collapsing two unrelated Emerald systems.

## Canon

Bento recognizes that the player prevented a HORIZON field unit from taking the OCEANIC PARTS by force. He does not present that failure as proof that HORIZON is automatically evil; the museum confrontation already has Otacilio order the operation to stand down because coercion is not care.

Bento's role remains observational: he follows trainers, records what official maps miss and calls when a clue justifies travel.

## Preserved

Among other inherited internals, this pass leaves unchanged:

- `VAR_SCOTT_STATE`;
- `FLAG_ENABLE_SCOTT_MATCH_CALL`;
- `LOCALID_SLATEPORT_SCOTT`;
- `FLAG_DELIVERED_DEVON_GOODS`;
- all movement, object, warp and museum progression logic;
- the existing Porto do Sal English museum, shipyard, harbor and daily-life renderers.

## Safety

The renderer:

- loads plain UTF-8 JSON authored text;
- requires exactly 17 known labels;
- only replaces consecutive `.string` lines immediately below those labels;
- enforces a conservative 32-character visible segment limit;
- masks all targets and proves the rest of the map script is byte-stable;
- explicitly checks progression-token counts before and after rendering;
- rejects the relevant SLATEPORT/SCOTT/Portuguese residue in its targets.

PR #58 remains outside scope. No art dependency is introduced.

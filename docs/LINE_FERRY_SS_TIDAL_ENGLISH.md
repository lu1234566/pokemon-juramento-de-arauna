# LINE FERRY / S.S. Tidal — English Surface

## Scope

This pass converts the inherited S.S. Tidal onboard surface to reviewed English while preserving the complete Emerald ferry state machine.

Owned runtime files:

- `data/maps/SSTidalCorridor/scripts.inc`
- `data/maps/SSTidalRooms/scripts.inc`

The checked renderer owns exactly 42 `.string` bodies:

- 16 Corridor blocks;
- 26 Rooms blocks.

No script command, trainer battle, movement, flag, warp or state transition is owned.

## Why this pass was necessary

The Corridor still contained a large Portuguese surface even though Juramento de Arauna is now English-only. This included:

- departure/arrival announcements;
- Porto do Sal and Baía das Luzes arrival copy;
- the cabin-rest prompt;
- corridor service dialogue;
- Seu Bento's post-League Battle Circuit invitation;
- the captain's welcome;
- cabin signs.

The Rooms were mostly vanilla English but still named LILYCOVE CITY and HOENN and did not match the revised LINE FERRY tone.

## Visible direction

The vessel is consistently presented as the **LINE FERRY** connecting **PORTO DO SAL** and **BAIA DAS LUZES**.

Seu Bento remains in the inherited Scott slot for the post-League invitation to the **BATTLE CIRCUIT**. The captain in the inherited Briney corridor slot remains a separate captain, avoiding two visible versions of Seu Bento aboard the same regular voyage.

Passenger dialogue is intentionally small-scale: Contest travel, friendships, composure, shared travel, and battle-as-pastime. The ship feels used by ordinary people rather than existing only as a progression corridor.

## Preserved ferry progression

The Corridor renderer preserves representative counts for:

- `VAR_SS_TIDAL_SCOTT_STATE`;
- `VAR_SS_TIDAL_STATE`;
- all BOARD / DEPART / HALFWAY / LAND / EXIT-CURRENTS S.S. Tidal states;
- `SetSSTidalFlag` and `ResetSSTidalFlag`;
- Porto do Sal / Baía das Luzes heal locations and Harbor warps;
- TM SNATCH hide state;
- all eight inherited onboard trainer checks;
- `FLAG_DEFEATED_SS_TIDAL_TRAINERS`;
- `FLAG_MET_SCOTT_ON_SS_TIDAL`;
- Scott/exit-sailor object wiring;
- porthole special.

Resting in cabin 2 still heals the party and advances the cruise through the inherited `SSTidalRooms_EventScript_ProgessCruiseAfterBed` routine.

## Preserved cabin gameplay

The Rooms renderer preserves:

- `ITEM_TM_SNATCH`;
- `FLAG_RECEIVED_TM_SNATCH`;
- bag-full handling;
- party healing;
- cruise progression after resting;
- all inherited single and double trainer battles;
- the original trainer IDs and teams.

Only the visible dialogue is rewritten.

## Renderer safety

`render_line_ferry_ss_tidal_en_checked.py` validates:

- exact `corridor` / `rooms` JSON sections;
- exact 16 + 26 label sets;
- one occurrence of every owned label;
- final `$` with no premature terminator;
- assembler-safe text;
- conservative 32-visible-character segments using a 16-character placeholder model;
- target-masked byte equality outside owned `.string` bodies;
- representative ferry/trainer/TM token counts;
- removal of Portuguese onboard residue and stale LILYCOVE CITY / HOENN references;
- required visible identities `PORTO DO SAL`, `BAIA DAS LUZES`, `BATTLE CIRCUIT`, `SEU BENTO`, and `LINE FERRY`.

The bank was tightened before integration when the placeholder/width model identified two unsafe lines.

## Deliberate non-ownership

This pass does not change:

- S.S. Tidal state constants;
- ferry travel distance/timing;
- destination selection;
- map geometry;
- any warp;
- any trainer ID/team;
- TM SNATCH mechanics;
- porthole behavior;
- Battle Circuit facilities;
- saves;
- PR #58.

No GitHub Actions or Codespaces are required for this surface pass. A full GBA ROM toolchain compile is not claimed here.
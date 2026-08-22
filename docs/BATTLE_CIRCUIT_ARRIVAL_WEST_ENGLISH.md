# Battle Circuit — West Arrival District English Surface

## Scope

This pass completes the first player-facing district reached after the LINE FERRY unlocks the post-League Battle Circuit.

Owned runtime file:

- `data/maps/BattleFrontier_OutsideWest/scripts.inc`

The checked renderer owns exactly 37 `.string` bodies. It does not enter any Battle Frontier facility script or engine.

## Visible identity

The inherited Battle Frontier complex is presented as the **BATTLE CIRCUIT**.

The existing facility names remain technically recognizable and mechanically untouched:

- BATTLE DOME;
- BATTLE FACTORY;
- BATTLE PIKE;
- the unused local BATTLE TOWER explanatory block.

The goal of this pass is not to redesign facility rules. It is to make the arrival plaza, ferry service, signs and ambient challengers coherent with the English-only Arauna surface.

## Ferry return service

The western dock now matches the ports already established by the LINE FERRY pass:

- PORTO DO SAL;
- BAIA DAS LUZES;
- LINE FERRY.

Ticket checking, destination selection and both return warps remain inherited.

## Plaza direction

Ambient dialogue emphasizes what the player is actually learning at the Circuit:

- experienced challengers discovering that reputation elsewhere does not guarantee success;
- Factory rental Pokémon and the question of who cares for/trains them;
- uncertainty inside the Pike;
- tournament/fan culture around the Dome;
- the Circuit as a recently built complex rather than an ancient institution;
- small non-battle interests such as fishing and Pokémon sightings.

The copy avoids turning access to the Circuit into proof that a Trainer is objectively superior. Arrival is framed as the start of a new set of formats.

## Mechanics preserved

Target-masked byte equality protects all non-owned source bytes.

Representative protected tokens include:

- `VAR_BRAVO_TRAINER_BATTLE_TOWER_ON`;
- `FLAG_HIDE_BATTLE_TOWER_REPORTER`;
- `ITEM_SS_TICKET`;
- `MULTI_SSTIDAL_BATTLE_FRONTIER`;
- PORTO DO SAL / BAIA DAS LUZES internal Harbor map warps;
- ferry attendant and S.S. Tidal local IDs;
- `Common_EventScript_FerryDepartIsland`;
- Factory-challenger object IDs;
- Camper/Girl movement objects;
- the inherited `random 2` rock-paper-scissors branch.

Thus destination indices, ferry movement, plaza movements and facility entrances are not changed.

## Renderer contract

`render_battle_circuit_arrival_west_en_checked.py` validates:

- exact 37-label JSON contract;
- one occurrence of every label;
- final `$` and no early terminators;
- assembler-safe strings;
- conservative 32-visible-character segments with placeholder modeling;
- target-masked byte equality outside text bodies;
- representative gameplay-token counts;
- removal of visible `BATTLE FRONTIER`, `SLATEPORT CITY`, and `LILYCOVE CITY` residue from owned text;
- required `BATTLE CIRCUIT`, `PORTO DO SAL`, `BAIA DAS LUZES`, DOME/FACTORY/PIKE identities.

## Deliberate non-ownership

This pass does not change:

- Battle Dome rules or brackets;
- Factory rentals implementation;
- Pike path logic;
- Tower logic;
- Symbols/Battle Points;
- Frontier Brains/Aces;
- trainer data;
- map geometry or facility entrances;
- ferry destination indices or warps;
- save data;
- dormant Portuguese Frontier renderer;
- PR #58.

No GitHub Actions or Codespaces are required for this surface pass. A full GBA ROM toolchain compile is not claimed here.
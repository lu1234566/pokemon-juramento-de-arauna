# Battle Tower — CIRCUIT PASS terminology

## Scope

This pass fixes a narrow post-game terminology inconsistency after the Battle Circuit reception was converted to the visible **CIRCUIT PASS**.

Exactly **6 text blocks** are owned across two maps:

### Battle Tower Lobby — 1
- `BattleFrontier_BattleTowerLobby_Text_RecordLastMatch`

### Battle Tower Battle Room — 5
- `BattleFrontier_BattleTowerBattleRoom_Text_RecordYourBattle`
- `BattleFrontier_BattleTowerLobby_Text_BattleRecordedOnPass`
- `BattleFrontier_BattleTowerBattleRoom_Text_AnabelTalentShallBeRecognized`
- `BattleFrontier_BattleTowerBattleRoom_Text_ReceivedAbilitySymbol`
- `BattleFrontier_BattleTowerBattleRoom_Text_AnabelCongratsYourPassPlease`

All six visible `FRONTIER PASS` references in this reviewed Tower record/Symbol surface become **CIRCUIT PASS**.

## Deliberately preserved

The pass does not rename or redesign the Battle Tower itself. It preserves the inherited challenge engine and post-game progression, including:

- Singles / Doubles / Multi / Link Multi modes;
- Level 50 / Open Level selection;
- eligibility checks and party selection;
- seven-Trainer streak structure;
- win-streak active/reset behavior;
- save-before-entry and resume state;
- record-battle enable/disable state;
- ribbons after the inherited threshold;
- Battle Point rewards;
- reporter / apprentice state;
- Cable / Wireless Link flow;
- Anabel battle triggers and Brain-status checks;
- Silver/Gold Ability Symbol progression;
- `frontier_getsymbols` / `frontier_givesymbol`;
- `MUS_OBTAIN_SYMBOL`;
- battle outcome and streak increment logic;
- map warps, movements, object IDs and saves.

Internal `FRONTIER_PASS`, `FRONTIER_BRAIN`, Tower and map identifiers remain untouched. Only the reviewed player-facing strings are changed.

## Anabel

ANABEL and the inherited **SALON MAIDEN** / **Ability Symbol** identity are intentionally retained. This pass establishes nomenclature consistency, not a new Circuit Master character redesign.

## Renderer guarantees

`scripts/render_battle_tower_circuit_pass_en_checked.py` enforces:

- exact two-section JSON contract;
- exact 1 + 5 label ownership;
- final `$` terminator discipline;
- conservative 32-visible-character line limit;
- masked byte equality outside the six owned `.string` bodies;
- representative Tower lobby and battle-room gameplay-token count preservation;
- rejection of `FRONTIER PASS` inside owned output;
- required `CIRCUIT PASS`, BATTLE TOWER, ANABEL and Ability Symbol context.

## Build integration

The Battle Tower Lobby and Battle Room join the transactional Arauna English overlay. The checked renderer runs after the Battle Circuit lounge-identity renderer.

No rendered map source is committed.

## Build status

No full GBA ROM toolchain compile is claimed for this text-overlay pass. GitHub Actions and Codespaces are not required. Legacy PR #58 remains outside scope.

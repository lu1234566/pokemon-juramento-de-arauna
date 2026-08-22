# Battle Circuit — East District English Surface

## Scope

This pass owns only the visible local `.string` bodies in:

- `data/maps/BattleFrontier_OutsideEast/scripts.inc`

The inherited internal map/facility names remain unchanged. Player-facing copy treats the larger complex as the **BATTLE CIRCUIT** while retaining the recognizable facility names:

- BATTLE TOWER
- BATTLE PALACE
- BATTLE ARENA
- BATTLE PYRAMID
- RANKING HALL
- BATTLE POINT EXCHANGE

The reviewed bank contains exactly **32 text blocks**.

## Direction

The east district explains why each facility feels different instead of treating the Circuit as a generic proof of superiority.

- **Tower:** streak pressure and consistency.
- **Palace:** reading and trusting how a Pokemon acts with limited direct instruction.
- **Arena:** short-form judgment where raw power alone is not enough.
- **Pyramid:** exploration, resource/route management and uncertainty.
- **Ranking Hall:** a record marks that a run happened; it is not immortality or a complete account.
- **BP Exchange:** remains an ordinary reward service.

Seu Bento replaces visible SCOTT attribution only in owned dialogue. Internal Scott IDs/flags are not renamed.

## Sudowoodo boundary

The static Sudowoodo event is deliberately outside text ownership.

The checked renderer requires representative gameplay-token counts to remain unchanged for:

- `FLAG_SYS_CTRL_OBJ_DELETE`
- `GetBattleOutcome`
- `FLAG_DEFEATED_SUDOWOODO`
- `FLAG_HIDE_BATTLE_FRONTIER_SUDOWOODO`
- `DoWateringBerryTreeAnim`
- `SE_SUDOWOODO_SHAKE`
- `LOCALID_FRONTIER_SUDOWOODO`
- `SPECIES_SUDOWOODO`
- `setwildbattle SPECIES_SUDOWOODO, 40`
- `gText_Sudowoodo_Attacked`
- `Common_EventScript_RemoveStaticPokemon`

The encounter species, level, watering interaction, battle result handling, object deletion and post-battle state therefore remain inherited.

## Other preserved structure

The renderer also preserves the Battle Tower reporter transition state and requires byte equality for all non-owned source after masking the 32 target string bodies.

No facility engine, BP/Symbol logic, challenge rule, trainer data, map geometry, movement, warp, save data or reward system is changed.

## Text safety

The bank/renderer contract enforces:

- exact `east` JSON section;
- exact 32-label set;
- non-empty payloads;
- `$` only at the final payload of each block;
- no raw assembler-breaking double quotes;
- conservative maximum of 32 visible characters per line segment;
- target-masked structural equality;
- stale visible `BATTLE FRONTIER` and `SCOTT` rejection in owned blocks;
- required BATTLE CIRCUIT / SEU BENTO / TOWER / PALACE / ARENA / PYRAMID / RANKING HALL / BATTLE POINT EXCHANGE identity.

## Build integration

`BattleFrontier_OutsideEast/scripts.inc` is added to the official English build's transactional overlay list and restored after the build. The checked renderer runs immediately after the west-arrival Battle Circuit renderer.

No rendered map source is committed.

## Validation status

The JSON bank was independently checked for the exact 32-label count and the 32-character visible-line limit before integration. Repository compare and zero-workflow checks are performed before merge.

No full GBA toolchain compile is claimed for this narrative surface pass. GitHub Actions and Codespaces are not used. Legacy PR #58 remains outside scope.

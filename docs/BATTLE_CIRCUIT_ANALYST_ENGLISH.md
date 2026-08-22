# Battle Circuit Analyst — English Identity Surface

## Scope

This pass owns only **9 identity-bearing text blocks** in:

- `data/maps/BattleFrontier_Lounge2/scripts.inc`

The underlying Frontier Maniac hint system remains inherited.

## Why this is a narrow pass

Lounge 2 contains a large dynamic information system. It selects a facility/mode, buffers facility names, calls `ShowFrontierManiacMessage`, and reveals Silver/Gold team descriptions as the player progresses.

Most of that content is already valid English and mechanically useful. Rewriting it would add risk without improving Arauna continuity.

The pass therefore changes only:

- the Maniac's public introduction → **CIRCUIT ANALYST**;
- seven SCOTT / FRONTIER BRAINS identity blocks → **SEU BENTO / CIRCUIT MASTERS**;
- one DOUBLE BATTLE advice block that still called the complex BATTLE FRONTIER.

## Preserved dynamic system

The checked renderer preserves representative token counts for:

- `FLAG_MET_BATTLE_FRONTIER_MANIAC`;
- `VAR_FRONTIER_MANIAC_FACILITY`;
- every Tower/facility selector from `FRONTIER_MANIAC_TOWER_SINGLES` through `FRONTIER_MANIAC_PYRAMID`;
- every `STDSTRING_*` buffer used by the local scripts;
- `ShowFrontierManiacMessage`.

Target-masked byte equality also guarantees that every non-owned Silver/Gold team description and advice block remains unchanged.

## Visible leaders

The inherited titles remain recognizable:

- SALON MAIDEN
- DOME ACE
- FACTORY HEAD
- PIKE QUEEN
- ARENA TYCOON
- PALACE MAVEN
- PYRAMID KING

Internal Frontier Brain naming and progression are not renamed.

## Safety

The renderer enforces:

- exact `analyst` section;
- exact 9-label contract;
- non-empty assembler-safe payloads;
- final `$` only on the last payload;
- conservative <=32 visible-character validation;
- target-masked structural equality;
- dynamic-system token count preservation;
- rejection of visible BATTLE FRONTIER / SCOTT / FRONTIER BRAINS / FRONTIER MANIAC inside owned blocks;
- required BATTLE CIRCUIT / CIRCUIT ANALYST / SEU BENTO / CIRCUIT MASTERS / leader identities.

## Build integration

Only `BattleFrontier_Lounge2/scripts.inc` joins the transactional overlay set. The checked renderer runs with the other Battle Circuit public surfaces.

No rendered map source is committed.

No full GBA toolchain compile is claimed. GitHub Actions and Codespaces are not used. Legacy PR #58 remains outside scope.

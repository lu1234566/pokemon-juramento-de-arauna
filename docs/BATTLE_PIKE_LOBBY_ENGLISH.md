# Battle Pike lobby — Arauna English surface

This pass completes the player-facing Battle Pike reception after the Battle Circuit and Circuit Masters identity work.

## Scope

Exactly **24 active local text blocks** in `data/maps/BattleFrontier_BattlePikeLobby/scripts.inc` are owned. Unused inherited text blocks remain outside the renderer.

The lobby now introduces the challenge around its real mechanic: uncertainty is unavoidable, but the player still chooses a path and prepares for consequences. JACI is named as the Battle Pike Circuit Master without changing her inherited internal Lucy slot.

## Rules preserved in the visible copy

- choose one of three paths at each junction;
- reach the goal to complete the run and receive Battle Points;
- Level 50 and Open Level remain the two modes;
- exactly three eligible Pokemon are selected;
- species must differ;
- held items must differ;
- Level 50 entrants must be Lv. 50 or below;
- the inherited `{STR_VAR_1}` eligibility expansion remains present in both mode-error messages;
- BAG/POKeNAV restrictions, held Berry/Herb behavior and fixed party order remain described by the rules board;
- staff/save handling for interrupted runs is preserved.

## Checked renderer

`scripts/render_battle_pike_lobby_en_checked.py` validates:

- the exact 24-label JSON contract;
- non-empty payloads and final `$` termination;
- conservative 32-character visible width, modelling `{STR_VAR_1}` as a 16-character expansion;
- exactly two `{STR_VAR_1}` placeholders;
- byte-stability of everything outside the 24 `.string` bodies;
- unchanged counts for critical Pike/frontier commands and constants;
- absence of stale `PIKE QUEEN` / luck-as-merit wording in the owned surface;
- required BATTLE PIKE / JACI / MASTER JACI / Battle Points identity;
- second-pass idempotence.

## Mechanics explicitly outside scope

No changes are made to `frontier_checkineligible`, party selection, `pike_savehelditems`, `pike_resethelditems`, `pike_save`, BP rewards, Brain checks, challenge state, curtain animation, corridor warp, room generation or any Battle Pike encounter logic.

The official build treats the lobby source transactionally and restores it after compilation. No rendered map source is committed.

No full GBA toolchain compile is claimed here. GitHub Actions and Codespaces are not used, and legacy PR #58 remains outside scope.

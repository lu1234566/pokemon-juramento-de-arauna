# Battle Circuit — Lounge identity residues

## Scope

This pass is intentionally narrow. It removes two remaining player-visible Battle Frontier/Scott identity residues from Battle Circuit lounges without rewriting the lounge systems around them.

Owned maps and blocks:

- `BattleFrontier_Lounge3/scripts.inc`
  - `BattleFrontier_Lounge3_Text_YouLookToughExplainGambling`
- `BattleFrontier_Lounge8/scripts.inc`
  - `BattleFrontier_Lounge8_Text_KnowAboutFrontierBrains`

Exactly **2 text blocks** are owned.

## Lounge 3 boundary

Lounge 3 contains the inherited Battle Point betting side system. Only its introductory explanation is changed so the activity is described as taking place across **BATTLE CIRCUIT** challenges.

The following inherited mechanics remain untouched:

- `FLAG_MET_BATTLE_FRONTIER_GAMBLER`;
- `VAR_FRONTIER_GAMBLER_AMOUNT_BET`;
- `VAR_FRONTIER_GAMBLER_STATE`;
- 5 / 10 / 15 BP bet choices;
- `MULTI_FRONTIER_GAMBLER_BET`;
- `ShowFrontierGamblerLookingMessage`;
- `ShowBattlePointsWindow`;
- `TakeFrontierBattlePoints`;
- `GiveFrontierBattlePoints`;
- all seven Silver Symbol checks;
- payout/result state transitions;
- facility-specific dynamic challenge messages.

No attempt is made to redesign the betting mechanic or its internal `FRONTIER_*` identifiers.

## Lounge 8 boundary

The old visible explanation:

- `FRONTIER BRAINS`;
- `SCOTT`;
- `BATTLE FRONTIER`;

is replaced by the established Arauna post-game terms:

- **CIRCUIT MASTERS**;
- **SEU BENTO**;
- **BATTLE CIRCUIT**.

The other two Lounge 8 NPC blocks are already clean English and remain untouched.

## Lounges deliberately left unchanged

The surrounding audit found no reason to perform a blanket rewrite:

- Lounge 1: complete IV rater system;
- Lounge 4: clean social dialogue;
- Lounge 5: Nature-reading system;
- Lounge 6: in-game Pokémon trade;
- Lounge 7: two BP Move Tutors;
- Lounge 9: no dialogue.

These should only receive future changes when a concrete player-visible Arauna gap is identified.

## Renderer guarantees

`scripts/render_battle_circuit_lounge_identity_en_checked.py` enforces:

- exact two-section JSON contract;
- exact two-label ownership;
- final `$` terminator rules;
- conservative 32-visible-character line limit;
- target-masked byte equality outside the owned `.string` bodies;
- representative Lounge 3 gameplay-token count preservation;
- rejection of visible `BATTLE FRONTIER`, `SCOTT`, and `FRONTIER BRAINS` inside owned output;
- required `BATTLE CIRCUIT`, `CIRCUIT MASTERS`, `SEU BENTO`, Battle Points and record language.

## Build integration

Both map scripts join the transactional Arauna English overlay. The renderer runs after the existing Battle Circuit analyst pass.

No rendered `scripts.inc` output is committed.

## Build status

This is a text-overlay pass. No full GBA ROM toolchain compile is claimed by this document.

GitHub Actions and Codespaces are not required for the pass. Legacy PR #58 remains outside scope.

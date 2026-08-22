# Battle Circuit: global text UI overlay

This document supersedes the original Portuguese Circuito de Batalha UI-overlay plan.

## Current English-only state

Arauna's official player-facing build is English-only. The historical renderer `scripts/render_arauna_frontier_ui.py` contains Portuguese replacements and therefore remains **dormant**. It must not be invoked by the official build.

The reviewed English replacement is:

- `scripts/render_battle_circuit_ui_en_checked.py`
- bank: `data/text/arauna/en/battle_circuit_ui.json`

It owns only three declarations in `src/strings.c`:

- `gText_CheckFrontierMap`: `Check BATTLE CIRCUIT MAP.`
- `gText_PutAwayFrontierPass`: `Put away the CIRCUIT PASS.`
- `gText_BattleFrontier`: `BATTLE CIRCUIT`

Everything else in the inherited Frontier Pass text UI remains English and is deliberately left intact in this pass, including Battle Points, Battle Record, Symbol names and the seven facility descriptions.

## Strategy

`src/strings.c` remains unchanged in version control as rendered output.

During `scripts/build_arauna.sh`:

1. `src/strings.c` is already part of the transactional overlay backup;
2. the checked English UI renderer updates only the three reviewed declarations;
3. the ROM build consumes the rendered text;
4. the existing exit trap restores the original source even if the build fails or is interrupted.

The renderer masks the three owned declarations and requires every other byte in `src/strings.c` to remain stable.

## Facility names and Symbols

The inherited proper facility names remain visible:

- BATTLE TOWER
- BATTLE DOME
- BATTLE PALACE
- BATTLE ARENA
- BATTLE FACTORY
- BATTLE PIKE
- BATTLE PYRAMID

The inherited Symbol names also remain in English. This matches the current Battle Circuit map/dialogue strategy and avoids creating a second naming system in the UI.

## CIRCUIT PASS continuity

Map dialogue now uses **CIRCUIT PASS** throughout the reviewed Battle Circuit surfaces. This global UI pass closes the corresponding text-menu gap by replacing the old `FRONTIER PASS` cancel/put-away action.

## Validation

Run:

`python3 scripts/render_battle_circuit_ui_en_checked.py --check`

The renderer verifies:

- exact three-key bank contract;
- one unique C declaration per owned symbol;
- only known legacy or already-rendered input values;
- byte stability outside the three declarations;
- no `BATTLE FRONTIER` or `FRONTIER PASS` survives in owned UI text;
- `BATTLE CIRCUIT` and `CIRCUIT PASS` are present after rendering.

## Graphic debt remains separate

`src/frontier_pass.c` contains no literal player-facing `FRONTIER PASS` text. It loads the Frontier Pass graphics/tilemaps from `graphics/frontier_pass/`.

Any old title or wording embedded directly in PNG/tilemap assets is **art debt**, not text debt, and is not modified by this renderer. That graphic surface should be audited and replaced as a separate art-safe task without changing save/state logic.

## Legacy note

The old Portuguese renderer and its historical documentation remain in the repository for provenance, but the English-only build must use only the checked English renderer described above.

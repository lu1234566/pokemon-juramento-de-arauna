# Route 103 — Ciro opening battle in English

Status: English-only narrative migration.

This slice replaces the repetitive Portuguese rival surface on Route 103 with a concise first ideological/battle beat while preserving the inherited Emerald rival event graph.

## Ciro — 8 blocks

Both internal May/Brendan branches now display the same CIRO sequence:

1. HORIZON has classified the route as low DESECHANTMENT activity;
2. CIRO treats the encounter as a comparison between field data and instinct;
3. after losing, he admits that either the sensors or his interpretation missed something;
4. he returns to ANAHI still trusting the method, but less blindly.

This gives CIRO a believable early starting point: confident in HORIZON and measurement, competitive with the player, but capable of registering contradictory evidence before his later M'BOI arc.

## Route surface — 3 blocks

- the tired traveler still teaches the POTION lesson;
- the water-shortcut NPC points toward VILA DA PASSAGEM instead of legacy OLDALE naming;
- the Route 103 sign uses the same canonical destination.

The canonical mapping is defined by `tools/cleanup_region_map_names.py`: Oldale is VILA DA PASSAGEM, while Mauville is ENCRUZILHADA.

## Technical contract

`scripts/render_route103_ciro_en.py` owns the 11 base replacements and `scripts/render_route103_ciro_en_checked.py` applies the canonical VILA DA PASSAGEM destination surface.

The renderers validate exact source markers, <=32-character visible segments, structural masking and key rival/progression tokens.

Preserved: all six starter-dependent rival trainer IDs/parties, `VAR_STARTER_MON`, `FLAG_DEFEATED_RIVAL_ROUTE103`, `VAR_BIRCH_LAB_STATE`, inherited Oldale-state variables/flags, rival exit movements, Match Call trainer events, warps, saves, geometry and art.

English-only. PR #58 untouched.

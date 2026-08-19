# Porto do Sal — city, shipyard and harbor services in English

Status: English-only migration slice.

This slice complements the already-restored museum/submarine story core by converting Porto do Sal's ordinary city life, shipyard and ferry/postgame harbor service into Arauna-native English.

## Daily city — 29 blocks

Porto do Sal remains a working market city rather than only a plot location:

- training-supply shop and the unchanged effort-ribbon mechanic are surfaced as a local training shop / EFFORT BAND;
- lighthouse, seaweed, market growth, Battle Tent, Name Rater and traded-Pokémon nickname rules remain everyday topics;
- residents discuss the HARBOR ENGINEER as a researcher and occasional local celebrity;
- interviews and camera reactions preserve the existing reporter scene;
- sailors talk about old ships becoming marine habitat and the scale of the sea.

Internal Effort Ribbon state/flags remain unchanged.

## Shipyard — 11 blocks

The former Stern Shipyard becomes a practical Porto do Sal shipbuilding facility without inventing a named replacement for Stern:

- the MASTER coordinates hull construction and sends OCEANIC PARTS to the HARBOR ENGINEER at the MUSEUM;
- a VETERAN SAILOR contributes current/navigation experience;
- the LINE FERRY develops from design problems to a completed vessel;
- technicians discuss changing sea conditions, seasickness, ship-scale structural design and buoyancy.

The original MR. BRINEY / Stern / S.S. Tidal identifiers remain internal implementation details only.

## Harbor service — 21 blocks

The existing ferry and Scanner flow is preserved while visible names become Arauna-native:

- unavailable-service state;
- ticket inspection and destination selection;
- BAIA DAS LUZES and BATTLE CIRCUIT destinations;
- LINE FERRY boarding;
- ordinary sailors and submersible curiosity;
- pre-completion and completed-ferry engineer dialogue;
- unchanged SCANNER exchange for DEEPSEATOOTH / DEEPSEASCALE.

Two global menu literals in `src/strings.c` are also surfaced as `PORTO DO SAL` and `BAIA DAS LUZES` while their internal `gText_SlateportCity` / `gText_LilycoveCity` symbol names are preserved.

## Technical contract

This slice changes 61 text blocks:

- 29 city daily-life blocks;
- 9 shipyard 1F blocks;
- 2 shipyard 2F blocks;
- 21 harbor/ferry/Scanner blocks;
- plus 2 visible destination literals in `src/strings.c`.

All English width fixes are consolidated directly into the three renderers; no temporary checked wrappers are required. Existing base renderers continue to validate source markers and non-dialogue structure.

Ferry/ticket logic, destination menu values, Scanner trade, DeepSea items, veteran/Briney progression, shipyard state, Effort Ribbon mechanic, reporter events, Battle Tent, Name Rater, warps, saves, geometry and art remain untouched.

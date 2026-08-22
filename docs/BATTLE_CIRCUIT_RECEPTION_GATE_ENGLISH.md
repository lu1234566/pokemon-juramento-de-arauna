# Battle Circuit Reception Gate — English Surface

## Scope

This pass owns exactly 32 visible text blocks in:

- `data/maps/BattleFrontier_ReceptionGate/scripts.inc`

It covers the first visit, Circuit Pass issue, Seu Bento arrival scene, facility guide, shared-rules guide and Circuit Pass guide.

Internal Battle Frontier / Scott identifiers remain unchanged.

## First-entry continuity

The inherited first-entry state machine is preserved:

- `FLAG_LANDMARK_BATTLE_FRONTIER`;
- `VAR_HAS_ENTERED_BATTLE_FRONTIER`;
- greeter/player/guide movement;
- Seu Bento's inherited Scott object movement;
- item fanfare;
- `FLAG_SYS_FRONTIER_PASS`.

The visible item is called **CIRCUIT PASS**. No save flag or internal item/state identifier is renamed.

## Facility guide

The guide keeps all nine inherited menu destinations and explains the actual gameplay focus:

- BATTLE TOWER — consecutive win streaks;
- BATTLE DOME — bracket tournaments;
- BATTLE PALACE — limited direct commands and Pokemon tendencies;
- BATTLE ARENA — short three-turn judged matchups;
- BATTLE FACTORY — rental Pokemon and swaps;
- BATTLE PIKE — route choice under uncertainty;
- BATTLE PYRAMID — exploration plus battles;
- RANKING HALL — run records;
- BATTLE POINT EXCHANGE — BP rewards.

`SCROLL_MULTI_BF_RECEPTIONIST` and `ShowScrollableMultichoice` remain inherited.

## Shared-rules guide

The pass preserves the inherited `MULTI_FRONTIER_RULES` selection and describes:

- LEVEL 50;
- OPEN LEVEL;
- Pokemon entry restrictions;
- duplicate-species restriction;
- duplicate-held-item restriction.

No eligibility code is changed by this renderer.

## Circuit Pass guide

The inherited `MULTI_FRONTIER_PASS_INFO` menu remains unchanged. Visible help covers:

- seven facility SYMBOLS;
- one recorded battle;
- Battle Points.

The text explicitly notes that Pike/Pyramid runs are excluded from the recorded-battle surface, matching the inherited rule.

## Safety model

The checked renderer enforces:

- exact `reception_gate` JSON section;
- exact 32-label contract;
- non-empty assembler-safe payloads;
- `$` only in each block's final payload;
- conservative <=32 visible-character line validation with placeholder modeling;
- target-masked byte equality outside the owned `.string` bodies;
- gameplay-token count preservation for landmark/pass/menu/movement wiring;
- rejection of stale Portuguese Circuit copy and visible BATTLE FRONTIER / FRONTIER PASS wording;
- required BATTLE CIRCUIT / CIRCUIT PASS / SEU BENTO / facility / rule vocabulary.

## Non-goals

This pass does not alter:

- map geometry or warps;
- facility challenge engines;
- BP/Symbol calculations;
- trainer data;
- menu indices;
- movement sequences;
- save layout;
- global internal Battle Frontier identifiers.

No rendered map source is committed.

## Validation status

The bank was checked independently for exactly 32 labels and the conservative 32-character visible-line limit before integration. Repository compare and zero-workflow checks are required before merge.

No full GBA ROM toolchain compile is claimed. GitHub Actions and Codespaces are not used. Legacy PR #58 remains outside scope.

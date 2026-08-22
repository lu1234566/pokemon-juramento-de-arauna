# Battle Circuit Public Services — English Surface

## Scope

This pass owns exactly **43 local text blocks across five public-service maps**:

- `BattleFrontier_ScottsHouse` — 17 blocks
- `BattleFrontier_RankingHall` — 7 blocks
- `BattleFrontier_ExchangeServiceCorner` — 12 blocks
- `BattleFrontier_PokemonCenter_1F` — 4 blocks
- `BattleFrontier_Mart` — 3 blocks

It does not own any facility battle engine or lounge map.

## Seu Bento's room

The inherited Scott house is surfaced as Seu Bento's room without renaming any internal Scott identifiers.

Visible dialogue is converted from Portuguese and keeps the established Arauna characterization: Seu Bento built the Circuit by watching how different Trainers adapted, but battle results are treated as evidence rather than a complete account of a person.

The pass preserves all inherited rewards and thresholds:

- initial Battle Point gift based on `VAR_SCOTT_STATE`;
- `FLAG_SCOTT_GIVES_BATTLE_POINTS`;
- all seven Silver Symbol checks;
- LANSAT BERRY reward;
- all seven Gold Symbol checks;
- STARF BERRY reward;
- 50-win Battle Tower SILVER SHIELD;
- 100-win Battle Tower GOLD SHIELD;
- decoration-storage and Berry-pocket failure paths.

Internal Frontier/Scott symbols remain unchanged. Visible copy uses **SEU BENTO**, **CIRCUIT PASS**, **CIRCUIT MASTER** and **BATTLE CIRCUIT**.

## Ranking Hall

The ten inherited ranking categories and record-window specials remain untouched.

The Hall no longer calls recorded Trainers “immortal.” It explains records as strong recorded runs: useful evidence that a run happened, not a complete account of everything behind it.

## Battle Point Exchange

Only the shared service copy and five local NPC conversations are owned.

The following are deliberately not rewritten:

- every individual item/decor confirmation;
- every item/decor description;
- vendor list indices;
- BP prices;
- reward IDs;
- bag/decor-space checks;
- purchase and delivery logic.

The public name is **BATTLE POINT EXCHANGE**.

## Pokémon Center and Mart

Only local NPC text is changed.

Preserved Center mechanics include:

- Battle Circuit east respawn location;
- Nurse routine;
- Cable Club resume logic;
- SKITTY species/cry.

Preserved Mart mechanics include the exact inherited inventory from ULTRA BALL through HP UP and the normal shared Pokémart dialogue/routine.

## Safety model

The checked renderer enforces:

- exact five-section JSON contract;
- exact 17 + 7 + 12 + 4 + 3 target labels;
- non-empty assembler-safe payloads;
- final `$` only on the final payload;
- conservative <=32 visible-character validation with placeholder modeling;
- target-masked byte equality outside owned `.string` bodies for each map;
- representative gameplay-token count preservation per map;
- rejection of stale Portuguese Circuit/Pass wording and visible `BATTLE FRONTIER`/`EXCHANGE SERVICE` residue in owned blocks;
- required Seu Bento / Circuit / Pass / Symbol / Ranking / BP / Arena / Arauna identity.

## Build integration

All five map scripts join the official English build's transactional overlay list. The renderer runs after the Battle Circuit Reception Gate renderer and before later story-region renderers.

No rendered map source is committed.

## Non-goals

This pass does not alter:

- facility engines;
- BP prices or calculations;
- Symbol flags or criteria;
- Battle Tower streak logic;
- rewards or IDs;
- Mart inventory;
- healing/Cable Club logic;
- map geometry, movement, warps, trainer data or saves;
- Lounge1–Lounge9.

No full GBA toolchain compile is claimed for this text-surface pass. GitHub Actions and Codespaces are not used. Legacy PR #58 remains outside scope.

# Mata do Meio interiors — English daily-life surface

## Scope

This pass completes the main optional interiors of inherited Fortree after the already-active **MATA DO MEIO** exterior and LIDIA Gym renderer.

It owns 33 text blocks across eight maps:

- `FortreeCity_House1`: 7 blocks;
- `FortreeCity_House2`: 7 blocks;
- `FortreeCity_House3`: 2 blocks;
- `FortreeCity_House4`: 6 blocks;
- `FortreeCity_House5`: 3 blocks;
- `FortreeCity_DecorationShop`: 2 blocks;
- `FortreeCity_Mart`: 3 blocks;
- `FortreeCity_PokemonCenter_1F`: 3 blocks.

The goal is not to turn every resident into a plot exposition NPC. These interiors establish how ordinary people in Mata do Meio live with canopy routes, POKéMON knowledge, records, trade and distance.

## Daily-life identity

The five houses reinforce the settlement's existing exterior identity:

- homes and routes adapt to trees rather than forcing the forest to adapt to them;
- POKéMON carry routes and habits across places;
- records are useful but do not replace lived memory;
- distant relationships can be maintained through WINGULL routes and communication;
- a trade is explicitly consensual: either side may refuse without penalty.

SEU BENTO's inherited Steven-facing house line is now fully English and keeps his recorder role concise: notes leave a trail but cannot replace memory.

## Preserved side activities

### House 1 — in-game trade

The inherited PLUSLE/VOLBEAT trade remains unchanged. Only the visible conversation changes.

### House 2 — HIDDEN POWER

The three right/left choices, flags and TM reward remain unchanged. The writing reframes the scene around attention and traits that depend on the individual POKéMON.

### House 4 — WINGULL courier

The cross-city WINGULL errand and MENTAL HERB reward remain unchanged. The visible writing treats WINGULL as part of the social route network rather than generic filler.

### Shops and Center

Decoration inventories, Mart stock, healing, Cable Club behavior and all shared service scripts remain unchanged.

The Pokemon Center's old `HORIZONTE` residue is removed. MATCH CALL remains a useful tool, but the dialogue no longer attributes ordinary world infrastructure to HORIZON without a story reason.

## Technical contract

`scripts/render_mata_do_meio_interiors_en_checked.py`:

- reads one UTF-8 JSON bank;
- requires exactly 33 labels across exactly eight source files;
- owns only consecutive `.string` directives under exact labels plus historical physical continuation lines;
- accepts either the reviewed raw source or the exact already-rendered body;
- validates a conservative 32-character visible width with dynamic placeholders expanded to 16 characters;
- masks every owned body and proves all non-dialogue source structure is byte-stable;
- preserves progression-token counts for the in-game trade, HIDDEN POWER puzzle, WINGULL/Mental Herb flow, Decoration Shop inventories, Mart inventory and Pokemon Center behavior;
- rejects visible `FORTREE`, `HORIZONTE` and tracked Portuguese residue inside owned blocks.

The eight inherited source maps are added to the transactional build backup/restore stack. No rendered map source is committed.

## Validation

Validated without GitHub Actions:

- JSON contract: 33/33 labels;
- conservative width validation: PASS;
- renderer boundary model for legacy multiline `.string` blocks: PASS;
- idempotent replacement model: PASS;
- target-mask structure model: PASS;
- required MATA DO MEIO / SEU BENTO / HIDDEN POWER / WINGULL / MATCH CALL identity: PASS.

A full GBA ROM toolchain build is not part of this pass.

PR #58 remains outside scope.

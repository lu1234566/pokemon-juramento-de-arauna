# Serra do Uivo — complete English story surface

Status: English-only narrative migration for the inherited Rustboro story slot.

## Why this slice exists

The early English campaign already reaches Serra do Uivo through Vila Amanhecer, Vila da Passagem and Pampa da Espera, but Serra still mixed vanilla Rustboro/Devon dialogue, Portuguese Arauna text, malformed automated replacements and unrelated Ciro lines.

This slice closes that break without replacing Emerald's event graph.

## Narrative role

Serra do Uivo is the first place where the player can understand why HORIZON is attractive before seeing why its methods become dangerous.

- HORIZON visibly built useful infrastructure, field equipment and research capacity.
- BOND measurement is presented as evidence, not moral authority.
- DALVA is a geologist and Gym Leader whose language centers on pressure, records and adaptation.
- CIRO still believes HORIZON can improve its models. Losing does not make him abandon the organization.
- OTACILIO is introduced as competent and capable of articulating ethical limits; this makes later violations of those limits more meaningful.
- The stolen shipment becomes OCEANIC PARTS for PORTO DO SAL. The hired thief does not know who paid for the interception, avoiding an early false answer about faction responsibility.
- GALERIAS DA SERRA replaces the visible Rusturf identity around the theft/rescue sequence.

## Coverage

Five reviewable JSON files under `data/text/arauna/en/serra_uivo_*.json` store the 153 authored text blocks, grouped into core, HORIZON, route, civic and residential surfaces. `scripts/render_serra_uivo_story_en.py` validates the data and progression contract, while `scripts/render_serra_uivo_story_en_checked.py` applies it through string-only boundaries across 15 existing source files:

- Serra do Uivo exterior and CIRO encounter;
- DALVA's Gym, first battle, badge, TM and Match Call surface;
- all three HORIZON Technical Center floors used by the early story;
- Route 116 and the Galerias da Serra theft/rescue bridge;
- Trainer's School story-facing BENTO residue;
- CUT house;
- Mart NPCs;
- Horizonte residential residue and one PC-wallpaper researcher identity.

The renderer also fixes the Route 116 glasses NPC, which previously displayed an unrelated Portuguese CIRO line.

## Technical contract

The authored dialogue is plain UTF-8 JSON. The checked renderer changes only consecutive `.string` lines under the 153 labeled text blocks; it cannot cross into comments, directives or executable script commands.

It validates:

- every target label exists exactly once;
- every authored visible segment is at most 32 characters using conservative placeholder substitutions;
- all non-target script text/commands remain byte-for-byte identical after masking target bodies;
- progression-critical tokens remain present in each touched source;
- stale visible identities such as `HORIZONTEORATION`, `DEVON CORPORATION`, `RUSTBORO CITY`, Portuguese `INSÍGNIA` and Portuguese dialogue fragments do not survive in the targeted blocks.

Preserved gameplay includes:

- `FLAG_BADGE01_GET` and the inherited first-badge progression;
- `TRAINER_ROXANNE_1` and all trainer IDs/parties;
- `ITEM_TM_ROCK_TOMB`, CUT permission and HM logic;
- rival starter selection and May/Brendan internal trainer slots;
- Match Call flags;
- `ITEM_DEVON_GOODS` as the unchanged internal shipment item;
- Great Ball, Repeat Ball and expanded Mart unlock flow;
- PokéNav, Letter and Exp. Share progression;
- fossil resurrection state and Lileep/Anorith rewards;
- Wingull species/cry and tunnel rescue event;
- all map coordinates, object IDs, warps, movement, saves and geometry.

## Build integration

The 15 source files join `scripts/build_arauna.sh`'s transactional backup/restore list. The checked renderer runs after the first HORIZON forest encounter and before the later Route 119 narrative pass.

Source files are restored when the build exits, including failure or interruption.

The English-only policy gate now uses an explicit allowlist of approved English renderers instead of the obsolete blanket rule that rejected every `render_*.py` invocation. Unknown renderer invocations still fail the policy gate.

English-only. PR #58 untouched.

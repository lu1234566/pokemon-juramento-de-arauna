# Porto das Redes — complete English early-coast arc

Status: English-only narrative migration for the inherited Dewford / Granite Cave / Briney travel surface.

## Scope

This slice closes the playable bridge from Serra do Uivo to Porto do Sal without changing Emerald's route order or event graph.

The curated surface contains **117 visible text blocks across 10 map-script files**, plus the two inherited Briney destination menus.

### Story flow

1. The veteran sailor from the Galerias da Serra rescue offers passage from the coast.
2. The player reaches **PORTO DAS REDES** carrying OTACILIO's LETTER for SEU BENTO and the unchanged internal shipment later surfaced as **OCEANIC PARTS**.
3. Porto das Redes presents oral memory as ordinary community practice rather than a faction slogan: dock sayings, work songs and contradictory versions coexist.
4. **ADEMAR** leads the second Gym. His language centers on footing, timing and adapting to a current instead of forcing it.
5. The second badge is surfaced as **TIDE BADGE** while the inherited BADGE02 / Brawly internals remain unchanged.
6. **GRUTA DAS VOZES** keeps the inherited FLASH tutorial and cave traversal.
7. SEU BENTO receives OTACILIO's letter. HORIZON's coastal survey lacks a settlement that fishers still name; Bento treats the mismatch as a question to investigate, not proof that either source is automatically correct.
8. After the unchanged letter flag is set, the veteran sailor can continue to **PORTO DO SAL**, where the OCEANIC PARTS already connect to the existing harbor-engineer surface.

## Porto das Redes identity

The inherited Dewford trend / Easy Chat system is preserved mechanically but reauthored as dockside oral culture.

Dynamic phrases now appear as:

- sayings carried between boats;
- work-song refrains;
- competing versions of the same local story;
- marginal notes and corrections in the House of Tides.

This preserves Easy Chat variables, specials, painting-index logic and game stats while making the feature belong to Arauna.

## Ademar

Ademar is not written as someone who commands the sea or treats hardship as moral proof.

His Gym lesson is:

- force without footing is unstable;
- darkness can be read through sound and timing, not only sight;
- adaptation does not require pretending the previous round never happened;
- memory can be shared without becoming an obligation to remain trapped in grief.

The darkness/brightening puzzle, all six Gym trainers, rematch flow, TM08 BULK UP and FLASH permission remain inherited mechanics.

## Seu Bento and Otacilio

The letter scene deliberately preserves OTACILIO's credibility established in Serra do Uivo.

The letter asks Bento to compare HORIZON coastal survey records with names still used by local fishers. The scene does not reveal a conspiracy and does not declare institutional records or oral testimony automatically correct.

Bento's conclusion is procedural: a missing record proves a gap in the record, not that nothing happened.

## Voyage menus

The inherited destination UI originally used the global `gText_Petalburg`, `gText_Slateport` and `gText_Dewford` strings.

The renderer does **not** rename those globals. It injects three private menu labels only inside `src/data/script_menu.h`:

- PAMPA DA ESPERA
- PORTO DO SAL
- PORTO DAS REDES

Only `MultichoiceList_BrineyOnDewford` and `MultichoiceList_BrineyOffDewford` are redirected to the private labels. Other systems keep the original globals untouched.

## Technical contract

`scripts/render_porto_redes_story_en_checked.py`:

- loads four readable UTF-8 JSON banks under `data/text/arauna/en/`;
- requires all 117 labels exactly once;
- can replace only consecutive `\t.string` lines directly below a target label;
- validates visible lines at <= 32 characters using conservative 16-character Easy Chat placeholder substitutions;
- refuses raw double quotes in authored payloads;
- verifies final text terminators;
- masks target bodies and asserts all non-target script structure is byte-stable;
- asserts progression-critical flags, items, trainer IDs and state tokens survive;
- rejects visible MR. BRINEY / PEEKO / DEWFORD / PETALBURG / SLATEPORT / BRAWLY / STEVEN / DEVON residue in owned blocks;
- patches only the two voyage menu arrays and proves the remainder of `src/data/script_menu.h` is structurally unchanged.

## Preserved gameplay

Among the unchanged internals:

- `FLAG_DELIVERED_STEVEN_LETTER` and `ITEM_LETTER`;
- `FLAG_DELIVERED_DEVON_GOODS` and the internal Devon shipment IDs;
- Briney object IDs, boat movement paths, warps and location vars;
- `ITEM_OLD_ROD` / `FLAG_RECEIVED_OLD_ROD`;
- Easy Chat trend variables, stats, specials and painting logic;
- `TRAINER_BRAWLY_1` and all six inherited Gym-trainer IDs;
- `FLAG_BADGE02_GET` / `FLAG_DEFEATED_DEWFORD_GYM`;
- `ITEM_TM_BULK_UP` / `FLAG_RECEIVED_TM_BULK_UP`;
- `FLAG_ENABLE_BRAWLY_MATCH_CALL`;
- `ITEM_HM_FLASH` / `FLAG_RECEIVED_HM_FLASH`;
- `ITEM_TM_STEEL_WING` / `FLAG_REGISTERED_STEVEN_POKENAV`;
- `ITEM_TM_SLUDGE_BOMB`, `ITEM_SILK_SCARF` and their reward flags;
- map geometry, object coordinates, collision, saves and route order.

## Build integration

The ten map files and `src/data/script_menu.h` join the transactional backup/restore list in `scripts/build_arauna.sh`.

The Porto das Redes renderer runs immediately after the Serra do Uivo renderer and before later-campaign English overlays.

The English-only renderer allowlist gains exactly one entry. No GitHub Actions change is required.

PR #58 remains outside scope.

# Baia das Luzes — Department Store English surface

## Scope

This pass gives the inherited Lilycove Department Store a Baia das Luzes daily-life identity while leaving its commercial mechanics untouched.

Owned surface: **26 reviewed text blocks across 6 maps**.

- 1F: welcome, shoppers and floor directory — 5 blocks.
- 2F: travel-supply shoppers — 3 blocks.
- 3F: training-support shoppers — 3 blocks.
- 4F: TM shoppers — 3 blocks.
- 5F: decoration shoppers and weather closure — 4 blocks.
- Rooftop: sale/plaza and vending-machine feedback — 8 blocks.

The AZUMARILL cry, unused wireless copy, lottery text bank and elevator copy are deliberately outside ownership.

## Narrative direction

The store is treated as a busy coastal commercial hub rather than a plot location. NPCs talk about packing for long routes, practical gifts, Contest rewards, training choices, TMs, decorations and rooftop sales. The writing stays grounded and avoids turning HORIZON or the Living Archive into the explanation for ordinary commerce.

The visible 1F identity is **BAIA DAS LUZES DEPARTMENT STORE**.

## Preserved mechanics

All non-owned source bytes must remain identical after rendering, so the following systems remain untouched:

- 1F daily Pokemon Lottery, ticket matching, stored prizes and TV winner report;
- all 2F item lists;
- all 3F vitamin and battle-item lists;
- all 4F attack/defense TM lists;
- all 5F dolls, cushions, posters and mats;
- the inherited abnormal-weather rooftop closure driven by `VAR_SOOTOPOLIS_CITY_STATE`;
- rooftop PokeNews sale visibility and clear-out-sale inventory;
- vending-machine items and prices: FRESH WATER 200, SODA POP 300, LEMONADE 350;
- the inherited `random 64` bonus-drink behavior;
- Department Store elevator routing and `VAR_DEPT_STORE_FLOOR` are not targeted at all.

The checked renderer also preserves explicit gameplay/inventory token counts per map in addition to target-masked byte equality.

## Renderer contract

`render_baia_luzes_department_store_en_checked.py`:

- loads one UTF-8 JSON bank;
- requires exactly 6 sections and 26 labels;
- owns only consecutive `.string` bodies beneath exact labels;
- supports legacy physical string continuations;
- models dynamic placeholders conservatively at 16 visible characters;
- rejects visible segments above 32 characters;
- requires a single final `$` terminator per block;
- masks every owned body and requires byte-identical non-dialogue structure;
- checks representative lottery, inventory, weather, sale and vending tokens before/after rendering;
- is idempotent when applied to already-rendered text.

## Validation

Synthetic validation using the production body-span/masking model:

- 26/26 labels found;
- conservative width contract PASS;
- render PASS;
- target-masked structure equality PASS;
- gameplay/inventory token counts PASS;
- second render byte-identical PASS;
- sentinel labels/directives outside owned text preserved.

No full GBA ROM toolchain compile was run for this pass. GitHub Actions and Codespaces are not required. PR #58 remains outside scope.

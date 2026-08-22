# Battle Circuit map graphic title

This pass removes the final confirmed **BATTLE FRONTIER** identity baked directly into the Emerald Frontier Pass map graphics.

## Asset

`graphics/frontier_pass/map_screen.png`

The Arauna source asset before this pass was byte-identical to upstream `pret/pokeemerald`:

- original Git blob: `64061d45a9649733f8d14f73c874f3f0aab120a1`;
- dimensions: **128 x 112**;
- indexed PNG / GBA-oriented tile source;
- paired tilemap: `graphics/frontier_pass/map_screen.bin`.

The tilemap itself remains unchanged.

## Visible change

The baked map heading:

`BATTLE FRONTIER`

becomes:

`BATTLE CIRCUIT`

The lettering keeps the existing Emerald title treatment rather than introducing a new font or high-resolution asset.

## Pixel validation

The original PNG and edited PNG were reconstructed through the existing 32 x 20 `map_screen.bin` tilemap before comparison.

Validated properties:

- source tilesheet remains **128 x 112**;
- indexed palette remains unchanged;
- no new palette indexes are introduced;
- `map_screen.bin` remains byte-identical;
- reconstructed screen remains **256 x 160**;
- exactly **479 rendered pixels** change;
- every changed rendered pixel is inside the old title rectangle: **x 76-143, y 2-14**;
- map artwork, facility icons, borders and all non-title tiles remain unchanged.

## Runtime relationship

`src/frontier_pass.c` already prints facility names, descriptions, Battle Points, Symbols and contextual help dynamically. PR #214 changed the corresponding English global text to **BATTLE CIRCUIT / CIRCUIT PASS**.

This PNG edit therefore addresses only the one identity string that was confirmed to be baked into the map graphics themselves.

## Preserved

- Frontier Pass runtime logic;
- cursor and zoom behavior;
- map landmark coordinates;
- facility selection order;
- Symbol sprites and palettes;
- `map_screen.bin`;
- all internal `FRONTIER_*` identifiers;
- saves and progression.

No GitHub Actions or Codespaces are required for this asset-only pass.

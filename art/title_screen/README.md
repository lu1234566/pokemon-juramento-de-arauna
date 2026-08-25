# M'Boi title-screen background

`mboi_source.png` is the M'Boi serpent drawn to replace the Rayquaza
silhouette behind the title logo. It is the **source** art, not a drop-in
replacement for `graphics/title_screen/rayquaza.png` — that file is a
deduplicated tile bank, and `rayquaza.bin` is a 32x32 tilemap authored
against it. Overwriting the bank alone reassembles the new tiles into noise,
which is what happened the first time this was tried.

`tools/art/build_title_background.py` generates the whole set together —
tile bank, tilemap and shared palette — from this source:

    python3 tools/art/build_title_background.py [scale] [x] [y]
    # currently installed: 1.45 at (26, 58) -> 283 tiles

The sky gradient is rebuilt from a band table measured off the original
background rather than read back from `rayquaza.png`, so the tool is
idempotent and the serpent can be repositioned by re-running it.

## Why the serpent is a silhouette

Palette 14 is shared with the clouds layer, which uses indices 0, 2 and 12.
Those are left untouched. The serpent uses only:

| index | role | note |
|-------|------|------|
| 11 | darkest body | unchanged from the Rayquaza art |
| 1 | mid-dark body | unused by either layer before, repainted |
| 3 | mid body | unused by either layer before, repainted |
| 15 | markings | `UpdateLegendaryMarkingColor` repaints this every 4th frame, so the belly line pulses gold with no new code |
| 2 | eye highlight | white, also a cloud colour |

Indices 1 and 3 were verified free: `rayquaza.png` uses 0,2,4-11,15 and
`clouds.png` uses 0,2,12, and the logo is 8bpp with a maximum index of 223,
below palette 14's range at 224-239.

## Composition

The logo and subtitle occupy roughly the top half of the 240x160 screen, so
only about 78 rows are clear. The whole coiled serpent cannot fit in that
band at a readable size, so it is placed the way Emerald places Rayquaza:
head in the clear band below the subtitle, body running off the bottom of
the frame.

## Still open

The subtitle (`emerald_version.png`) was already repainted — it is a sprite
sheet with its own palette, so it dropped straight in. The copyright strip
in `press_start.png` and the ROM header are tracked separately.

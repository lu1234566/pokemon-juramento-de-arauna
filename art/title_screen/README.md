# M'Boi title-screen background — not yet installed

`mboi_source.png` is the M'Boi serpent drawn to replace the Rayquaza
silhouette behind the title logo. It is 128x128 with 10 colours, which is the
right shape, and it is **not** wired into the build, because dropping it over
`graphics/title_screen/rayquaza.png` renders scrambled. Two reasons, both
verified in the emulator:

**The tilemap is not an identity map.** `rayquaza.bin` is a 32x32 tilemap of
1024 entries that rebuilds the on-screen image from only 191 distinct tiles,
with horizontal flips. It was authored against the original art's deduplicated
tile bank. A freshly drawn 128x128 image produces 256 tiles in raster order,
so the existing tilemap reassembles them into noise.

**The palette does not match.** The background loads
`rayquaza_and_clouds.gbapal`, shared with the clouds layer. Every index the new
art uses differs from that palette, so even correctly ordered tiles would come
out the wrong colour — and touching the shared palette would recolour the
clouds too.

To finish it, one of:

- redraw the serpent *into* the existing tile bank, keeping `rayquaza.bin` and
  `rayquaza_and_clouds.pal` valid; or
- generate a new tilemap and palette from this art and update `rayquaza.bin`,
  the palette, and the clouds art together as one set.

The subtitle (`emerald_version.png`) had neither problem: it is loaded as a
sprite sheet with its own palette, so the repaint dropped straight in.

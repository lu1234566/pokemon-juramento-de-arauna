# Arauna back-sprite integration (species 217–386)

High-resolution back-sprite art for the Arauna dex was downscaled to 64×64
(premultiplied-alpha) and integrated into `src/data/graphics/arauna_fakemon_graphics.h`
by `tools/arauna/integrate_back_sprites.py`. Because a species shares one 16-colour
palette between its front and back battle sprites, each back was fitted with the
smallest change that keeps both sprites within a mean colour error of 25/441.

## Outcome

| outcome | count | what happened |
|---|---:|---|
| keep | 82 | back already ≤25 against the existing palette; front/palette untouched |
| rebuild | 72 | new combined front+back palette; front re-indexed, palette + shiny rewritten |
| residual | 11 | no shared palette fits the back ≤25 without pushing the front past it; front kept, best-effort back emitted |
| undersized | 5 | downscaled back far shorter than its front (would render tiny); species reverted |

**154/170 delivered within the 25 colour-error gate.** Front sprites of the
72 rebuilt species shift slightly (median 9.4, max 23.7 error) but stay within the same gate.

## Species reported instead of delivered faithfully

These 16 keep their original front/palette. Their back art cannot be represented
within the shared 16-colour palette at ≤25 (residual), or is drawn too small in
frame (undersized). Re-exporting these backs closer to the front palette / larger
in frame would let them integrate.

| species | reason | back error vs existing palette |
|---:|---|---:|
| 266 | residual | 28.3 |
| 272 | residual | 30.8 |
| 274 | residual | 35.8 |
| 276 | residual | 31.2 |
| 277 | residual | 33.8 |
| 297 | residual | 28.5 |
| 300 | undersized | — |
| 321 | undersized | — |
| 322 | undersized | — |
| 323 | undersized | — |
| 327 | residual | 49.3 |
| 348 | residual | 109.4 |
| 360 | undersized | — |
| 362 | residual | 123.4 |
| 368 | residual | 95.3 |
| 383 | residual | 138.1 |


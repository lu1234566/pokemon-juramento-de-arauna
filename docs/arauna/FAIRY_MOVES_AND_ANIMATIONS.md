# Fairy Moves & Battle Animation Spec — Arauana

## Engine constraints

Arauana is still using Pokémon Emerald's Generation III damage-class rule:
physical/special is derived from the move **type**, not from a per-move category.
`TYPE_FAIRY` is ID 18 and therefore lands on the special side of the split.
For that reason this pass deliberately introduces only special/status Fairy
attacks. A physical Fairy move would silently use Special Attack unless the
battle engine is upgraded first.

## Move ladder

| Move | Power | Acc. | PP | Purpose |
| --- | ---: | ---: | ---: | --- |
| Fairy Wind | 40 | 100 | 30 | early reliable Fairy STAB |
| Disarming Voice | 40 | — | 15 | never-miss spread STAB; vocal/musical lines |
| Draining Kiss | 50 | 100 | 10 | 50% engine-native drain; enchantment/water/psychic/ghost lines |
| Dazzling Gleam | 80 | 100 | 10 | mid/late spread STAB |
| Moonblast | 95 | 100 | 10 | late STAB; 30% Sp. Atk drop |
| Luar de Jaci | 100 | 90 | 5 | Jaciana signature; 30% Sp. Atk drop |
| Juramento de Arauana | 105 | 90 | 5 | Arauanaú/Arauanamon signature; +1 Sp. Def after hit |
| Eclipse Divino | 110 | 85 | 5 | Arauanamon finisher; -1 user Sp. Atk after hit |

Charm and Sweet Kiss are retyped to Fairy as utility moves.

## Native GBA art format

All new battle-animation source art is **indexed PNG** and stays within a
single 4bpp OBJ palette (maximum 16 palette entries including transparency).
The build converts it through `INCGFX` to `.4bpp.lz` plus `.gbapal.lz`,
exactly like vanilla Emerald particles.

| Asset | Source sheet | Frames | Decompressed 4bpp |
| --- | --- | ---: | ---: |
| `fairy_spark.png` | 16×64 | 4 × 16×16 | 0x0200 |
| `fairy_wave.png` | 32×96 | 3 × 32×32 | 0x0600 |
| `fairy_crescent.png` | 32×64 | 2 × 32×32 | 0x0400 |
| `fairy_oath.png` | 32×64 | 2 × 32×32 | 0x0400 |
| `fairy_eclipse.png` | 32×64 | 2 × 32×32 | 0x0400 |

The visual language intentionally follows Emerald: hard pixel edges, compact
silhouettes, a dark plum outline, bright white/pink core highlights, small gold
and cyan accents, and no anti-aliased raster glow baked into the source art.

## Motion model

The PNGs are **not** pre-rendered GIFs. Animation is split between tile-frame
cycling and engine motion:

- **Spark** — four-frame twinkle, vertical lift and sine-wave side drift.
- **Wave** — three-frame fairy-energy projectile translated from attacker to
  target using Emerald's linear-translation helper.
- **Crescent** — two-frame moon glyph with a slow vertical sine float.
- **Oath sigil** — two-frame diamond/rune pulse, usable on attacker or target.
- **Eclipse** — two-frame orb/ring pulse with a subtle float.

Move scripts layer those particles with vanilla timing primitives: delays,
palette blends, sound panning and battler shake. This keeps the animations
readable on original GBA resolution and avoids oversized modern effects.

## Learnset policy

There are 68 Fairy-type species in `ARAUNA_DEX_ENGINE_MAPPING.csv`. Their
custom level-up overlays begin with the already-approved resembled vanilla
progression and add only a restrained Fairy curve:

- Fairy Wind early.
- Disarming Voice primarily on Fairy-primary or vocal/musical species.
- Draining Kiss on Fairy-primary and water/psychic/ghost enchantment lines.
- Dazzling Gleam in the mid/late game.
- Moonblast only on final or single-stage species.
- Signature moves only on their intended owners.

Each resulting list is capped at 16 entries. When space is needed, weak
off-STAB attacks are trimmed before STAB, utility, level-1 identity moves or
Fairy/signature moves.

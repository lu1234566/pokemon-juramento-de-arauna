# Settlement block data — restoration and landscaping

## What had gone wrong

Every settlement had been put through a pass that gave it a "different look" by
shuffling its metatiles inside collision groups. Collision and elevation were
preserved at every coordinate, so the towns stayed walkable and no script or
warp ever broke — which is exactly why the damage went unnoticed for so long.

But a building is not a collision mask. A house is eight specific blocks in
eight specific relative positions; permuting blocks that happen to share a
collision value scatters roof corners, wall segments and doorsteps across the
grass as loose tiles. Sixteen settlements had between 3% and 75% of their block
grid permuted this way.

The tool that did it, `tools/remodel_emerald_cities.py`, has been removed. Its
success criterion was a minimum *percentage of blocks changed*, which is a
measure of damage, not of design.

## Restoration

`tools/art/restore_city_layouts.py` puts the authored composition back for all
sixteen settlements.

Before writing a byte it verifies, per map, that:

- the layout id, dimensions and both tilesets match the source composition;
- the map connections match;
- every `warp_events`, `object_events`, `coord_events` and `bg_events`
  coordinate matches.

All sixteen passed that check, which is what makes the restoration safe: each
door lands back under its doorway, each NPC stands on the ground it was placed
on, and the `setmetatile` coordinates in the Lilycove and Sootopolis scripts
(the Wailmer that blocks the shore, the gym doors) address the blocks they were
written for again.

| Settlement | Blocks restored |
|---|---:|
| VILA AMANHECER (LittlerootTown) | 180 / 400 |
| VILA DA PASSAGEM (OldaleTown) | 221 / 400 |
| PAMPA DA ESPERA (PetalburgCity) | 502 / 900 |
| SERRA DO UIVO (RustboroCity) | 1650 / 2400 |
| PORTO DAS REDES (DewfordTown) | 108 / 400 |
| PORTO DO SAL (SlateportCity) | 66 / 2400 |
| ENCRUZILHADA (MauvilleCity) | 418 / 800 |
| VALE DO SILENCIO (VerdanturfTown) | 169 / 400 |
| CAMPO DAS CINZAS (FallarborTown) | 152 / 400 |
| CASA DA CINZA (LavaridgeTown) | 140 / 400 |
| MATA DO MEIO (FortreeCity) | 439 / 800 |
| BAIA DAS LUZES (LilycoveCity) | 2171 / 3200 |
| MISSOES DO CEU (MossdeepCity) | 1681 / 3200 |
| AGUAS DE M'BOI (SootopolisCity) | 2330 / 3600 |
| CASA DA FOGUEIRA (PacifidlogTown) | 398 / 800 |
| ESTR. JURAMENTO (EverGrandeCity) | 2409 / 3200 |

13034 blocks in total.

## Landscaping

`tools/art/plant_town_gardens.py` adds hand-placed flower beds on top of the
restored composition. It changes only the metatile id of a block and keeps the
collision and elevation bits exactly as they are, so it cannot alter where the
player may walk, and it refuses to plant on anything that is not plain grass.

Beds are written out coordinate by coordinate as compact shapes — a strip
against a building front, a small patch of meadow — rather than sprinkled by a
random pass. That is the difference between landscaping and noise.

VILA AMANHECER has beds flanking the laboratory door that mirror the ones
already there, a bed at the front of each house away from the doorstep, and
three meadow patches breaking up the empty fields: 20 blocks.

## Looking at a map without booting the game

`tools/audit/render_map.py LAYOUT_LITTLEROOT_TOWN out.png` composes any map's
block grid into a PNG the same way the GBA does — two layers per metatile, tile
and palette split between the primary and secondary tilesets, colour index 0
transparent on the upper layer. It renders from any checkout via `--root`, so
two compositions can be put side by side.

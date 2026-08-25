# Settlement block data — restoration, landscaping and Arauna's own look

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

## Arauna's own look

The restored composition is Emerald's, and Emerald's towns look like Hoenn.
`tools/art/retheme_cities.py` gives the settlements a look of their own without
putting a single campaign coordinate at risk.

What it is allowed to change is one thing: a block's metatile id. Collision,
elevation and metatile behaviour are carried over untouched at every
coordinate, so no wall moves, no door stops being a door, no patch of
decoration becomes an encounter tile, and every step the player, an NPC or a
scripted `applymovement` could take is still exactly as available and as long
as it was. That still leaves most of what a town looks like: what the ground is
made of, where the streets run, where the squares and the gardens are.

Streets are not drawn by hand. Each town's own walkable graph is joined from
every doorstep and every route exit to a hub with straight two-lane runs, and
the material is laid with an autotile table learned from the whole Emerald
corpus — for every block of the material, which of its four neighbours are the
same material, and what the artists put in that situation. So the edges and
corners are Emerald's, and the plan follows what the town's own buildings and
exits already imply. Widening stops one block short of anything solid, which
leaves every façade its verge, and the verge is planted at a regular spacing.

Arauna's settlements are joined by packed earth rather than by Hoenn's paving.
The cities that are paved already get squares of green cut into them instead,
placed on the roomiest patches of floor the campaign never walks on.

| Settlement | Treatment | Blocks restyled |
|---|---|---:|
| VILA AMANHECER (LittlerootTown) | earth streets | 61 |
| VILA DA PASSAGEM (OldaleTown) | earth crossroads | 72 |
| PAMPA DA ESPERA (PetalburgCity) | earth streets | 52 |
| SERRA DO UIVO (RustboroCity) | green squares | 64 |
| PORTO DO SAL (SlateportCity) | green squares | 45 |
| ENCRUZILHADA (MauvilleCity) | earth streets | 94 |
| VALE DO SILENCIO (VerdanturfTown) | earth streets | 49 |
| CASA DA CINZA (LavaridgeTown) | earth streets | 36 |
| BAIA DAS LUZES (LilycoveCity) | earth avenues | 250 |
| MISSOES DO CEU (MossdeepCity) | earth avenues | 190 |
| AGUAS DE M'BOI (SootopolisCity) | green squares | 20 |

943 blocks across eleven settlements.

PORTO DAS REDES, CAMPO DAS CINZAS, MATA DO MEIO, CASA DA FOGUEIRA and
ESTR. JURAMENTO are left alone. Their ground is sand, ash, timber, plank and
cliff rather than lawn, so a street laid through them would either change a
metatile behaviour or read as a mistake; they already carry an identity of
their own.

## The gate

`tools/audit/map_invariants.py` is what makes a restyle of this size safe to
make. It reads the block data of a revision straight out of git, replays the
map's own `applymovement` scripts to find every tile a cutscene can walk
across, and then checks the current composition against that baseline:

- collision, elevation and metatile behaviour identical at every changed block;
- warp and sign behaviours unchanged;
- route seams byte-identical;
- nothing that used to be reachable, on foot or by surf, cut off.

`--verify HEAD` runs it over all sixteen settlements. `--report` prints the map
with every campaign coordinate marked, which is how a design gets checked
before it is written.

## Order

The tools stack, and the order matters, because each one reads what the last
one wrote:

1. `restore_city_layouts.py` — put the authored composition back;
2. `plant_town_gardens.py` — hand-placed beds on the restored grass;
3. `retheme_cities.py` — streets, squares and verges.

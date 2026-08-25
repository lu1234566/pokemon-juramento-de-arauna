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
| VILA AMANHECER (LittlerootTown) | earth streets | 48 |
| VILA DA PASSAGEM (OldaleTown) | earth crossroads | 71 |
| PAMPA DA ESPERA (PetalburgCity) | earth streets | 158 |
| SERRA DO UIVO (RustboroCity) | green squares | 32 |
| PORTO DO SAL (SlateportCity) | green squares | 45 |
| ENCRUZILHADA (MauvilleCity) | earth streets | 91 |
| VALE DO SILENCIO (VerdanturfTown) | earth streets | 44 |
| CASA DA CINZA (LavaridgeTown) | earth streets | 58 |
| BAIA DAS LUZES (LilycoveCity) | earth avenues | 235 |
| MISSOES DO CEU (MossdeepCity) | earth avenues | 384 |
| AGUAS DE M'BOI (SootopolisCity) | green squares | 20 |

1186 blocks across eleven settlements.

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

## Tiles that are not Emerald's, drawn with Emerald's hand

Laying Emerald's own blocks in a new plan still leaves a town wearing Hoenn's
materials. `tools/art/forge_arauna_tiles.py` adds materials that are not in
Emerald at all, without a pixel of it falling out of style and without a byte
of headroom.

There is no headroom. The primary tileset every outdoor map loads is at 512 of
512 tiles, 512 of 512 metatiles, and every one of the sixteen entries in all
six of its palettes is referenced by something. Nothing can be appended, and
raising any of those ceilings would mean moving the VRAM window the hardware
reads the tileset through.

What it has is dead space, and the tool measures it rather than assuming it:
64 metatiles that no map lays and no script names, and — after discounting the
tiles that secondary tilesets reach back into the primary set to use, and the
five ranges the animation code rewrites in VRAM every few frames — 15 tiles
that nothing draws. Writing there changes nothing on screen today and moves no
file's size at all.

So a material is forged the only way that space allows, which happens also to
be the only way that guarantees the result looks like Emerald: **take a
material the artists already drew and re-index it onto a colour ramp they
already mixed.** Not a redraw. Every pixel keeps its position, every dither
keeps its pattern, every edge keeps its shape; the only thing that changes is
which entry of which palette each pixel points at. A material forged this way
cannot drift out of style, because there is no step in which anything is drawn.

**TERRA**, the packed red earth of Arauna's roads, is Emerald's beach sand
re-indexed from the sand ramp of palette 5 onto the rock ramp of palette 3.
Palette 3 carries the identical grass green at entry F, so the material's own
edge and corner tiles still meet a lawn exactly as the originals did. It costs
8 tiles and 9 metatiles, and the blocks are named in
`include/constants/metatile_labels.h` so nothing later reads the slots as free.

A forged material appears in no Emerald map, so its autotile table cannot be
learned the way a real one's is. It does not have to be: block for block it is
the source material, so the source's learned table maps straight through the
substitution. Every town laid in earth also has any sand Emerald had already
put there swapped over, so no settlement ends up wearing two materials at once.

### One thing this pass got wrong

The paintable-ground lists first carried `0x201`. Any block id at or above
0x200 is an index into whichever secondary tileset the map loads, so that
number is a yellow flowerbed in VILA AMANHECER, a ledge in ENCRUZILHADA and
deep water in MISSOES DO CEU. Nothing was damaged — the id never came up in a
street plan, and the gate would have refused the change anyway, because a
ledge's behaviour is not a road's. But relying on the gate to catch a mistake
is worse than not making it, so `paint` now compares the behaviour of the block
it is about to lay against the behaviour of the block already there and skips
the cell when they differ. The mistake is no longer possible to express.

## Biomes

Each settlement now wears the green of the biome it was named for. The lawn is
60 to 80 per cent of the pixels on screen in a town, so this is the single
change that stops a map reading as Hoenn.

Emerald's grass is three entries of palette 2 — a highlight speckle, a body and
a shadow speckle — and that same palette already carries two more three-step
green ramps the artists mixed for other things. So a biome's lawn is the same
two tiles of grass pointing at a different ramp, forged the same way TERRA was:
re-indexed, never redrawn. Two tiles each.

| Lawn | Ramp | Settlements |
|---|---|---|
| MATA | deep Atlantic-forest green | VILA AMANHECER, VALE DO SILENCIO, MATA DO MEIO, BAIA DAS LUZES, AGUAS DE M'BOI |
| CERRADO | dry yellow-green | VILA DA PASSAGEM, ENCRUZILHADA, CASA DA CINZA, PORTO DO SAL |
| PAMPA | pale, sun-bleached | PAMPA DA ESPERA, SERRA DO UIVO, MISSOES DO CEU, ESTR. JURAMENTO |

The lawn reaches the route seam rather than stopping short of it, so a town's
biome ends at the town's edge — the way Emerald's own ash stops at Fallarbor's.
That meant relaxing one of this project's own rules: the seam used to have to
stay byte-identical. A connection is defined by the two maps' dimensions and
its offset, never by what the blocks at the join look like, and their physics
and behaviour are frozen like everything else, so restyling a seam cannot break
a join — it can only make the change visible at the edge, which is a decision.
The gate now counts seam blocks restyled and reports them instead of refusing.

### What still wears Emerald's green, and why

Rather than guess, a detector reads every block a town lays and reports any
that still draws palette 2's mint ramp. Two things do.

**Tree canopies.** Their lawn is baked into the same tiles as the foliage —
nineteen mixed tiles per biome to separate — and the primary tileset has one
free tile left. So the gaps between tree crowns keep the old green.

**The strip of grass at a building's foot**, which the Petalburg tileset draws
as part of the building's own blocks. This one is fixable: those blocks
reference the primary lawn tiles, and the secondary tilesets have real room —
`petalburg` alone has 352 free tiles and three unused palettes. It is the next
piece of work, not a limit.

**Flowerbeds** were a third case, and were dealt with. Emerald's bed is half
lawn by pixel count — the petals are drawn on a tile carrying the old green
with them — and recolouring it costs four tiles per biome, which do not exist.
Against a dark or a yellow lawn each bed read as a pale hole, so in those
biomes the beds go back to being grass. PAMPA is close enough to the green the
petals were drawn against that it keeps them.

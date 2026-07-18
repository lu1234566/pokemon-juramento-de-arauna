# Emerald map-reuse contract for Arauna

Arauna does not build campaign maps from blank layouts. Every playable area starts from an original Pokémon Emerald layout, connection, interior or route segment. Development may change warps, object scripts, encounter tables, weather, music and progression gates, but preserves the original block composition until a separately reviewed relocation is required.

## Canonical campaign reuse

| Arauna arc | Emerald foundation | Reuse purpose |
|---|---|---|
| Prologue — Vila Amanhecer | Existing Arauna technical village assembled only from Littleroot/Petalburg-era Emerald blocks | Opening, starter and first rival gate |
| 1 — Porto das Redes | Route 109, Slateport City, Slateport Harbor and Seashore House | Shoreline, fishing port, Dona Zilá, Iaraço and Iara-Mãe |
| 2 — Serra do Uivo | Route 114, Fallarbor Town and Meteor Falls | Mountain settlement, ascent, cave acoustics and Lobisomem |
| 3 — Ruínas das Missões | Route 111 desert, Desert Ruins and Mirage Tower | Cerrado plateau, threatened ruins and memory trial |
| 4 — Pampa da Espera | Route 117, Verdanturf and open Safari Zone sectors | Grassland, long sightlines and the House of the Square |
| 5 — Sertão de Dentro | Route 112, Jagged Pass, Lavaridge and Route 111 | Dry ascent, heat, scarce water and the House of Rain |
| 6 — Mata do Meio | Route 119, Fortree and Weather Institute | Dense forest, canopy settlement and the House of the Forest |
| 7 — Águas de M'Boi | Routes 120–122, Safari wetlands and water facilities | Floodplain, dam conflict and the House of the Serpent |
| 8 — Encruzilhada Central | Mauville crossroads, Route 110 junctions and a reused ceremonial interior | Final convergence and the House of the Bonfire |

The exact later-arc routing remains adjustable, but replacing these foundations with blank custom maps is prohibited unless the user explicitly changes this rule.

## Porto das Redes implementation

The first implementation reuses the maps without altering layout binaries:

- LAYOUT_ROUTE109 remains the shoreline and old landing;
- LAYOUT_SLATEPORT_CITY remains the port settlement;
- their original north/south connection is preserved;
- the old fisherman object at (33, 6) becomes the shoreline witness;
- the existing Pokémon object at (32, 6) carries the Iaraço interaction;
- the existing old-woman object at (20, 37) becomes Dona Zilá;
- the current slice reaches Porto through Route 109's established landing at (20, 28);
- no new map, layout, tileset, blockdata or collision file is created.

## Review rule

A validator must accompany every campaign map-reuse change and prove which Emerald layouts, objects and connections remain in use. Visual reconstruction from scratch is not an accepted shortcut.

## Serra do Uivo implementation

The second implementation also preserves layout binaries:

- LAYOUT_FALLARBOR_TOWN remains the ash-town settlement;
- LAYOUT_ROUTE114 remains the complete mountain ascent;
- LAYOUT_METEOR_FALLS_1F_1R remains the waterfall cave;
- the existing Fallarbor girl teaches the first three signs;
- the existing Route 114 gentleman and Poochyena become the deaf hermit and companion;
- the former Cozmo position at (13, 23) is reused for the Lobisomem interaction;
- the original Team Magma scene is bypassed through its existing state variable during Arauna progression;
- no new map, layout, tileset, blockdata or collision file is created.

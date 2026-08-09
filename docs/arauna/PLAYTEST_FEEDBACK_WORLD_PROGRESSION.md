# Playtest feedback — world progression and navigation

## Scope

This workstream implements the non-Pokémon portion of the third hands-on test feedback. Battle sprites, back sprites, shiny palettes and culturally sensitive creature redesigns remain outside this branch until approved replacement art is supplied.

## Problems confirmed by the test

1. Vila Amanhecer's visible east opening and its functional exit used different tiles.
2. Zila's notebook existed only in dialogue and could not be opened by the player.
3. The prologue ended with a direct script warp to Route 109, removing the feeling of travel.
4. Slateport still communicated its original identity more strongly than Porto das Redes.
5. Route and city progression depended too much on invisible script transitions.
6. Emerald's HM structure needed to become a visible tool-and-permission structure.

## Implemented

### Vila Amanhecer exit

- removed the hidden unconditional route warp;
- assigned the route script to both visible east-opening tiles `(18, 11)` and `(19, 11)`;
- kept the story lock on those same visible tiles;
- removed the bounce-prone destination warp at the bottom of Mist Route;
- preserved the original Emerald-derived layout and collision data.

A player who does not know the map can now find the exit by following the road artwork instead of searching nearby floor tiles.

### Zila's Notebook

The unused Fame Checker key-item slot is presented as **Zila's Notebook** without changing the save layout or shifting the global item table.

The notebook is given after the care-first partner choice and appears in **Key Items**. Using it displays a page selected from current story variables and flags. It reports:

- current objective;
- Mist Route field progress;
- physical travel objective to Porto;
- Porto investigation traces;
- Consortium confrontation state;
- Iara-Mãe Testimony;
- Maré and Uivo Badge chapter state;
- Tide Board collection state.

The first implementation uses Emerald's text interface. A bespoke illustrated notebook screen can later replace the presentation without changing the story-data contract.

### Physical progression toward Porto

The direct Vila Amanhecer → Route 109 warp and Ciro's instant-travel prompt were removed.

The current handoff is:

```text
Vila Amanhecer east opening
→ Mist Route traversal
→ Old Coast Road using Route 110's Emerald layout
→ Porto das Redes using Slateport's Emerald layout
```

The player enters Route 110 at its northern end and must cross the complete southbound road. Porto arrival is recorded only after entering the city from that road.

### Old Coast Road

Route 110 retains its original blockdata but now has an Arauna-specific event composition:

- Team Aqua, Birch, rival, cycling challenge and incompatible Hoenn trainers were removed from the map event layer;
- building warps and the Route 103 side connection were removed for this campaign slice;
- cycling and the vanilla map-name popup were disabled;
- civilians describe migration, pale water, sealed cargo and Consortium traffic;
- existing signs were reassigned to Porto, field-station and checkpoint information;
- two useful items remain reachable;
- the full walking distance is preserved;
- the northern road is closed by visible workers, a Consortium checkpoint and a complete trigger line, preventing early Mauville access.

The blocker uses the existing reserved flag `0x4F`, exposed to Arauna C code and scripts as `FLAG_ARAUNA_NORTH_ROAD_REOPENED` while retaining the canonical expansion flag table.

### Porto das Redes identity pass

Slateport's blockdata remains the city foundation, but the playable event composition is now Porto-specific:

- the `SLATEPORT CITY` popup is suppressed;
- only the coast-road and shoreline connections remain active;
- Team Aqua and unrelated commercial/story NPC clutter were removed;
- Dona Celina, the Consortium Agent and dockworker story witnesses remain in their approved locations;
- Ciro, a boatbuilder, net menders, fishers, a memorial keeper and harbor workers populate the city;
- signs identify Porto das Redes, the House of Tide, fishers' memorial, permit post, net market and board workshop;
- custom arrival text explicitly establishes that residents call the place Porto das Redes even though an old Slateport sign remains;
- only the Pokémon Center, Mart, shipyard workshop and one house remain open in this slice.

This pass changes the city's readable identity and progression while continuing to reuse Emerald art and map foundations. A later tile-composition pass can add more visible nets, crates, memorial details and pale-water tiles after visual playtesting.

### Visible progression blockers

The first persistent blocker is implemented on the north end of the Old Coast Road:

- two road workers;
- one Consortium checkpoint agent;
- a closure sign;
- a nine-tile trigger line with no walkable gap;
- dialogue explaining the landslide, structural repairs and restricted corridor.

The same pattern is now the required architecture for future incomplete routes: a visible cause, an explanatory NPC or sign, and a persistent flag that removes the obstruction only when the destination is implemented.

### Tide Board instead of field Surf

The unused Devon Scope slot is presented as the permanent **Tide Board** Key Item.

- it is awarded by Porto's boatbuilder after the Maré Badge;
- it is visible and readable in the Key Items pocket;
- the notebook directs the player to collect it;
- its permission flag satisfies calm-water access even if no party member knows Surf;
- facing calm water branches to dedicated Tide Board dialogue and reuses Emerald's existing water-movement field effect;
- Surf remains available as a battle move and as a fallback field method;
- strong-current restrictions remain separate and are not bypassed by the Board.

The same architecture can later support cutting tools, climbing equipment, a diving kit and transportation permits.

## Validation added or updated

The repository-safety suite now checks:

- visible Vila Amanhecer exit alignment;
- absence of the direct Porto teleport;
- Mist Route evidence and coast-road handoff;
- full Old Coast Road blocker coverage;
- removal of incompatible Team Aqua objects;
- Porto-specific arrival and reduced city event composition;
- Zila's Notebook item overrides and dynamic pages;
- Tide Board reward, item identity and field-permission routing;
- English-first runtime text rather than obsolete full label parity;
- current Ciro prologue conclusion instead of the removed Nilo epilogue contract;
- current partner-choice respawn and repeatable healing flow.

## Acceptance state

Implemented in source:

- no hidden tile is the only way to leave Vila Amanhecer;
- the notebook is visible and usable from Key Items;
- the main objective updates after major story flags;
- Ciro does not offer instant travel to Porto;
- reaching Porto requires traversing a full Emerald-derived route;
- incompatible northern progression is visibly blocked;
- Porto does not introduce itself through the vanilla Slateport popup;
- calm-water travel no longer requires teaching Surf;
- no Pokémon art was changed in this workstream.

Still required before merging the draft PR:

- successful ARM compilation;
- successful engine test runner execution;
- new-save mGBA playthrough from Dona Zila's house through Porto;
- visual inspection of all new object placements and city/route collision behavior;
- confirmation that the Tide Board water-entry animation behaves correctly with every possible lead-party state.

GitHub Actions jobs are currently terminating before their first recorded step, with no runner logs or artifacts. The PR therefore remains a draft and no build or emulator success is claimed.

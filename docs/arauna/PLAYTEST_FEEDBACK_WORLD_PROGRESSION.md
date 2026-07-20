# Playtest feedback — world progression and navigation

## Scope

This workstream implements the non-Pokémon portion of the third hands-on test feedback. Battle sprites, back sprites, shiny palettes and culturally sensitive creature redesigns remain outside this branch until approved replacement art is supplied.

## Problems confirmed by the test

1. Vila Amanhecer's visible east opening and its functional exit used different tiles.
2. Zila's notebook existed only in dialogue and could not be opened by the player.
3. The prologue ended with a direct script warp to Route 109, removing the feeling of travel.
4. Slateport still communicated its original identity more strongly than Porto das Redes.
5. Route and city progression still depended too much on invisible script transitions.
6. The Emerald HM structure needs to become a visible tool-and-permission structure.

## First implementation batch

### Vila Amanhecer exit

- removes the hidden unconditional route warp;
- assigns the route script to both visible east-opening tiles `(18, 11)` and `(19, 11)`;
- keeps the story lock on those same tiles;
- removes the bounce-prone destination warp at the bottom of Mist Route.

A player who does not know the map should now find the exit by following the road artwork rather than searching nearby floor tiles.

### Zila's Notebook

The unused Fame Checker key-item slot is presented as **Zila's Notebook** without changing the save layout or shifting the global item table.

The notebook is given after the partner choice and appears in **Key Items**. Using it displays a page selected from current story variables and flags. The first version reports:

- current objective;
- Mist Route field progress;
- physical travel objective to Porto;
- Porto investigation traces;
- Consortium confrontation state;
- Iara-Mãe Testimony;
- Maré and Uivo Badge chapter state.

This is deliberately a functional text interface first. A bespoke illustrated notebook UI can replace it later without changing its story data contract.

### Physical progression toward Porto

The direct Vila Amanhecer → Route 109 warp is removed.

The current handoff is:

```text
Vila Amanhecer east opening
→ Mist Route traversal
→ old coast road using Route 110's Emerald layout
→ Porto das Redes through Slateport's existing north connection
```

The player is told to travel on foot, and the Porto arrival state is recorded only when the ridge toward the coast road is crossed.

## Next commits in this workstream

### Coast Road pass

Route 110 will retain its original blockdata but receive an Arauna-specific event pass:

- remove or hide incompatible Team Aqua and Hoenn story events;
- rewrite route NPC dialogue around migration, pale water and Consortium traffic;
- rebalance or replace incompatible trainer encounters;
- add an explicit northern road closure so Mauville cannot be entered early;
- keep the full southbound walking distance instead of placing the player beside Porto.

### Porto das Redes visual and identity pass

Slateport's layout will be edited rather than merely renamed. The pass will reuse Emerald tiles and existing map structure while changing the readable composition:

- stronger fishing-dock foreground;
- nets, crates, boats and repair spaces;
- fisher memorial landmark;
- Consortium permit post and warning signs;
- House of Tide landmark for Dona Celina;
- pale-water visual treatment where technically safe;
- removal or reassignment of commercial and Hoenn-specific NPC clutter;
- custom Porto arrival text with the vanilla Slateport identity suppressed.

### Visible progression blockers

Unimplemented exits will be blocked by visible causes instead of invisible coordinates:

- road worker and landslide;
- closed Consortium checkpoint;
- damaged bridge;
- warning board and physical barricade;
- weather hazard with an NPC explanation.

Each blocker will use a persistent story flag and disappear only when its route is implemented.

### Field tools instead of HMs

The first planned conversion is the **Board**:

- permanent Key Item;
- obtained through a Porto story event;
- authorizes water movement without teaching Surf to a Pokémon;
- reuses Emerald's water movement internally;
- Surf remains available as a battle move, not a field obligation.

The same architecture can later support cutting tools, climbing equipment, a diving kit and transportation permits.

## Acceptance rules for the next playable build

- no hidden tile may be the only way to leave Vila Amanhecer;
- the notebook must be visible and usable from Key Items;
- the main objective must update after major story flags;
- Ciro must not offer instant travel to Porto;
- reaching Porto must require traversing at least one full Emerald-derived route;
- incompatible vanilla story exits must be visibly blocked;
- Porto must not introduce itself to the player as Slateport City;
- no Pokémon art is changed in this workstream.

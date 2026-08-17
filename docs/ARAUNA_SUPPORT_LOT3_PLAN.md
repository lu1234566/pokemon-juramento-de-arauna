# Arauna support characters — lot 3

This lot introduces dedicated overworld graphics for three recurring story roles by reclaiming the final three vanilla Emerald object-graphics IDs explicitly marked unused in the doll block.

| Arauna role | Dedicated ID | Reclaimed vanilla storage | Runtime palette |
| --- | ---: | --- | --- |
| Val — evolved | 79 | `OBJ_EVENT_GFX_UNUSED_WOOPER_DOLL` | `NPC_3` |
| Field operations administrator | 80 | `OBJ_EVENT_GFX_UNUSED_PIKACHU_DOLL` | `NPC_3` |
| Arquivo Vivo administrator | 81 | `OBJ_EVENT_GFX_UNUSED_PORYGON2_DOLL` | `NPC_2` |

Targeted placements preserve coordinates, scripts, flags, movement and trainer metadata:

- both late-game Victory Road Wally objects → Val evoluído
- Aqua Hideout B2F Matt event → administrador de operações de campo
- Route 119 Weather Institute 2F Shelly event → administradora do Arquivo Vivo
- Seafloor Cavern Room 3 Shelly event → the same Arquivo Vivo administrator, preserving her recurring identity

The generic Consórcio/HORIZONTE and Lembrantes grunt families remain untouched by these dedicated IDs. `NUM_OBJ_EVENT_GFX` and Emerald's one-byte graphics-ID format remain unchanged.

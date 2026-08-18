# Arauna support characters — lot 4

This lot adds a dedicated overworld identity for Ciro's mother by using the one vanilla object-graphics numeric value (239) that Emerald intentionally leaves empty.

- `OBJ_EVENT_GFX_MAE_CIRO = 239`
- `NUM_OBJ_EVENT_GFX` changes from 239 to 240.
- `OBJ_EVENT_GFX_VARS` changes from `NUM_OBJ_EVENT_GFX + 1` to `NUM_OBJ_EVENT_GFX`, so dynamic IDs remain exactly 240-255.
- No field storing object graphics IDs changes size; all remain one byte.
- Both gender-dependent rival-house mother events use the same dedicated visual.
- Coordinates, scripts, flags, movement, warps and story progression are unchanged.

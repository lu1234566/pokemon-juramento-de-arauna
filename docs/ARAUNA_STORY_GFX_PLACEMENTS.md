# Arauna story graphics placements

This layer changes only `graphics_id` values on existing Emerald object events. Coordinates, flags, scripts, warps, movement, trainer metadata, map dimensions and route progression remain unchanged.

| Story character / phase | Existing Emerald event | Dedicated graphics ID |
| --- | --- | --- |
| Dona Zilá | Mt. Pyre Summit elder | `OBJ_EVENT_GFX_DONA_ZILA` |
| Ciro — Consórcio | Lilycove final rival encounter | `OBJ_EVENT_GFX_CIRO_CONSORCIO` |
| Ciro — ruptura/final | Ever Grande Champions Room rival arrival | `OBJ_EVENT_GFX_CIRO_FINAL` |

Ciro intentionally remains on the phase-1 rival graphics during Route 103, Route 110, Lavaridge and Route 119. Several inherited rival sequences use bicycle-specific graphics there, so delaying the phase transition prevents visual reversion to Brendan/May until dedicated bike art exists.

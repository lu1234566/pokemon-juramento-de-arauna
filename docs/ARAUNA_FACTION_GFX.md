# Arauna faction overworld graphics

This visual layer reuses the original Emerald Team Aqua and Team Magma object-event slots so every inherited encounter automatically follows Arauna's rewritten faction identities without changing map scripts or progression.

| Emerald graphics slot | Arauna visual identity |
| --- | --- |
| `OBJ_EVENT_GFX_AQUA_MEMBER_M` | HORIZONTE / Consórcio security agent |
| `OBJ_EVENT_GFX_AQUA_MEMBER_F` | HORIZONTE / Consórcio field technician |
| `OBJ_EVENT_GFX_MAGMA_MEMBER_M` | Lembrante field member |
| `OBJ_EVENT_GFX_MAGMA_MEMBER_F` | Lembrante field worker |

All four sheets preserve Emerald's 144x32 / 16x32-frame structure and use the runtime palettes already assigned to those slots. No event coordinates, flags, trainer data, warps, scripts, route order or story control flow are changed.

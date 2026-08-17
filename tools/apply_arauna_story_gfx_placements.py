#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def replace_object_graphics(path_rel, anchor_key, anchor_value, old_gfx, new_gfx):
    path = ROOT / path_rel
    text = path.read_text(encoding="utf-8")
    anchor = f'"{anchor_key}": "{anchor_value}"'
    if text.count(anchor) != 1:
        raise SystemExit(f"Expected one {anchor!r} in {path_rel}, found {text.count(anchor)}")

    pos = text.index(anchor)
    start = text.rfind("    {", 0, pos)
    end = text.find("    }", pos)
    if start < 0 or end < 0:
        raise SystemExit(f"Could not isolate object containing {anchor!r} in {path_rel}")

    block = text[start:end]
    old = f'"graphics_id": "{old_gfx}"'
    new = f'"graphics_id": "{new_gfx}"'
    if block.count(old) != 1:
        raise SystemExit(f"Expected one {old!r} inside target object in {path_rel}")

    new_block = block.replace(old, new, 1)
    path.write_text(text[:start] + new_block + text[end:], encoding="utf-8")

    # Validate JSON and guarantee the target object now owns the dedicated slot.
    data = json.loads(path.read_text(encoding="utf-8"))
    matches = [
        obj for obj in data.get("object_events", [])
        if obj.get(anchor_key) == anchor_value
    ]
    if len(matches) != 1 or matches[0].get("graphics_id") != new_gfx:
        raise SystemExit(f"Post-write validation failed for {path_rel}: {anchor_value}")


# Dona Zilá uses the inherited Mt. Pyre elder story object; only its graphics ID changes.
replace_object_graphics(
    "data/maps/MtPyre_Summit/map.json",
    "local_id",
    "LOCALID_MT_PYRE_SUMMIT_OLD_LADY",
    "OBJ_EVENT_GFX_EXPERT_F",
    "OBJ_EVENT_GFX_DONA_ZILA",
)

# Ciro keeps his phase-1 rural look through the bike-capable rival scenes.
# His Consórcio appearance starts at the final Lilycove rival encounter.
replace_object_graphics(
    "data/maps/LilycoveCity/map.json",
    "script",
    "LilycoveCity_EventScript_Rival",
    "OBJ_EVENT_GFX_VAR_0",
    "OBJ_EVENT_GFX_CIRO_CONSORCIO",
)

# The Champions Room arrival uses Ciro's post-rupture/final appearance.
replace_object_graphics(
    "data/maps/EverGrandeCity_ChampionsRoom/map.json",
    "local_id",
    "LOCALID_CHAMPIONS_ROOM_RIVAL",
    "OBJ_EVENT_GFX_VAR_0",
    "OBJ_EVENT_GFX_CIRO_FINAL",
)


doc = ROOT / "docs/ARAUNA_STORY_GFX_PLACEMENTS.md"
doc.parent.mkdir(parents=True, exist_ok=True)
doc.write_text("""# Arauna story graphics placements

This layer changes only `graphics_id` values on existing Emerald object events. Coordinates, flags, scripts, warps, movement, trainer metadata, map dimensions and route progression remain unchanged.

| Story character / phase | Existing Emerald event | Dedicated graphics ID |
| --- | --- | --- |
| Dona Zilá | Mt. Pyre Summit elder | `OBJ_EVENT_GFX_DONA_ZILA` |
| Ciro — Consórcio | Lilycove final rival encounter | `OBJ_EVENT_GFX_CIRO_CONSORCIO` |
| Ciro — ruptura/final | Ever Grande Champions Room rival arrival | `OBJ_EVENT_GFX_CIRO_FINAL` |

Ciro intentionally remains on the phase-1 rival graphics during Route 103, Route 110, Lavaridge and Route 119. Several inherited rival sequences use bicycle-specific graphics there, so delaying the phase transition prevents visual reversion to Brendan/May until dedicated bike art exists.
""", encoding="utf-8")

print("Arauna story graphics placements applied successfully.")

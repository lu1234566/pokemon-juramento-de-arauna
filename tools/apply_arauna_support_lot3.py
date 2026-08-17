#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def write(path, text):
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


# 1. Reclaim the final three explicitly-unused vanilla doll IDs.
path = "include/constants/event_objects.h"
text = read(path)
if "OBJ_EVENT_GFX_VAL_EVOLUIDO" not in text:
    marker = "#define OBJ_EVENT_GFX_UNUSED_PORYGON2_DOLL        81\n"
    aliases = marker + (
        "\n// Arauna dedicated support-character slots: reclaim vanilla IDs marked unused.\n"
        "#define OBJ_EVENT_GFX_VAL_EVOLUIDO              OBJ_EVENT_GFX_UNUSED_WOOPER_DOLL\n"
        "#define OBJ_EVENT_GFX_ADMIN_CAMPO                OBJ_EVENT_GFX_UNUSED_PIKACHU_DOLL\n"
        "#define OBJ_EVENT_GFX_ADMIN_ARQUIVO              OBJ_EVENT_GFX_UNUSED_PORYGON2_DOLL\n"
    )
    text = replace_once(text, marker, aliases, "event object aliases")
write(path, text)

# 2. Point the reclaimed storage to Arauna's exact 144x32 sheets.
path = "src/data/object_events/object_event_graphics.h"
text = read(path)
replacements = {
    'const u32 gObjectEventPic_UnusedWooperDoll[] = INCGFX_U32("graphics/object_events/pics/dolls/unused_wooper_doll.png", ".4bpp");':
        'const u32 gObjectEventPic_UnusedWooperDoll[] = INCGFX_U32("graphics/object_events/pics/people/val/phase2.png", ".4bpp", "-mwidth 2 -mheight 4");',
    'const u32 gObjectEventPic_UnusedPikachuDoll[] = INCGFX_U32("graphics/object_events/pics/dolls/unused_pikachu_doll.png", ".4bpp");':
        'const u32 gObjectEventPic_UnusedPikachuDoll[] = INCGFX_U32("graphics/object_events/pics/people/arauna/admin_field.png", ".4bpp", "-mwidth 2 -mheight 4");',
    'const u32 gObjectEventPic_UnusedPorygon2Doll[] = INCGFX_U32("graphics/object_events/pics/dolls/unused_porygon2_doll.png", ".4bpp");':
        'const u32 gObjectEventPic_UnusedPorygon2Doll[] = INCGFX_U32("graphics/object_events/pics/people/arauna/admin_archive.png", ".4bpp", "-mwidth 2 -mheight 4");',
}
for old, new in replacements.items():
    if old in text:
        text = replace_once(text, old, new, old.split('[]')[0])
    elif new not in text:
        raise RuntimeError(f"graphics declaration missing: {old}")
write(path, text)

# 3. Convert each one-frame doll table into a normal nine-frame overworld table.
path = "src/data/object_events/object_event_pic_tables.h"
text = read(path)
for name in ("UnusedWooperDoll", "UnusedPikachuDoll", "UnusedPorygon2Doll"):
    old = (
        f"static const struct SpriteFrameImage sPicTable_{name}[] = {{\n"
        f"    obj_frame_tiles(gObjectEventPic_{name}),\n"
        "};"
    )
    frames = "\n".join(
        f"    overworld_frame(gObjectEventPic_{name}, 2, 4, {i})," for i in range(9)
    )
    new = f"static const struct SpriteFrameImage sPicTable_{name}[] = {{\n{frames}\n}};"
    if old in text:
        text = replace_once(text, old, new, f"pic table {name}")
    elif new not in text:
        raise RuntimeError(f"pic table missing: {name}")
write(path, text)

# 4. Turn the reclaimed graphics-info records into standard 16x32 walking NPCs.
path = "src/data/object_events/object_event_graphics_info.h"
text = read(path)
settings = {
    "UnusedWooperDoll": ("NPC_3", "NPC_3"),       # Val evolved
    "UnusedPikachuDoll": ("NPC_3", "NPC_3"),     # field administrator
    "UnusedPorygon2Doll": ("NPC_2", "NPC_2"),    # Archive administrator
}
for name, (pal_tag, pal_slot) in settings.items():
    pattern = re.compile(
        rf"const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{name} = \{{.*?\n\}};",
        re.S,
    )
    new = f'''const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{name} = {{
    .tileTag = TAG_NONE,
    .paletteTag = OBJ_EVENT_PAL_TAG_{pal_tag},
    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,
    .size = 256,
    .width = 16,
    .height = 32,
    .paletteSlot = PALSLOT_{pal_slot},
    .shadowSize = SHADOW_SIZE_M,
    .inanimate = FALSE,
    .disableReflectionPaletteLoad = FALSE,
    .tracks = TRACKS_FOOT,
    .oam = &gObjectEventBaseOam_16x32,
    .subspriteTables = sOamTables_16x32,
    .anims = sAnimTable_Standard,
    .images = sPicTable_{name},
    .affineAnims = gDummySpriteAffineAnimTable,
}};'''
    text, count = pattern.subn(new, text, count=1)
    if count != 1:
        raise RuntimeError(f"graphics info {name}: expected one block, found {count}")
write(path, text)

# 5. Target only the actual story characters, never whole generic NPC families.
def update_map(path, predicate, new_gfx, label):
    full = ROOT / path
    data = json.loads(full.read_text(encoding="utf-8"))
    matches = [obj for obj in data.get("object_events", []) if predicate(obj)]
    if len(matches) != 1:
        raise RuntimeError(f"{label}: expected one object, found {len(matches)}")
    matches[0]["graphics_id"] = new_gfx
    full.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# Victory Road uses two separate Wally objects for the same late-game Val arc.
update_map(
    "data/maps/VictoryRoad_1F/map.json",
    lambda o: o.get("local_id") == "LOCALID_VICTORY_ROAD_ENTRANCE_WALLY",
    "OBJ_EVENT_GFX_VAL_EVOLUIDO",
    "Victory Road entrance Val",
)
update_map(
    "data/maps/VictoryRoad_1F/map.json",
    lambda o: o.get("script") == "VictoryRoad_1F_EventScript_ExitWally",
    "OBJ_EVENT_GFX_VAL_EVOLUIDO",
    "Victory Road exit Val",
)
update_map(
    "data/maps/AquaHideout_B2F/map.json",
    lambda o: o.get("local_id") == "LOCALID_AQUA_HIDEOUT_MATT",
    "OBJ_EVENT_GFX_ADMIN_CAMPO",
    "Aqua Hideout field administrator",
)
update_map(
    "data/maps/Route119_WeatherInstitute_2F/map.json",
    lambda o: o.get("local_id") == "LOCALID_WEATHER_INSTITUTE_2F_SHELLY",
    "OBJ_EVENT_GFX_ADMIN_ARQUIVO",
    "Weather Institute Archive administrator",
)
update_map(
    "data/maps/SeafloorCavern_Room3/map.json",
    lambda o: o.get("script") == "SeafloorCavern_Room3_EventScript_Shelly",
    "OBJ_EVENT_GFX_ADMIN_ARQUIVO",
    "Seafloor Cavern Archive administrator",
)

# 6. Stable implementation documentation.
doc = '''# Arauna support characters — lot 3

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
'''
write("docs/ARAUNA_SUPPORT_LOT3_PLAN.md", doc)

print("Arauna support lot 3 applied successfully.")

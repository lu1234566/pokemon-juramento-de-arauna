#!/usr/bin/env python3
from pathlib import Path
import json

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


# 1) Consume the documented unused numeric value 239 while preserving dynamic IDs 240-255.
path = "include/constants/event_objects.h"
text = read(path)
if "OBJ_EVENT_GFX_MAE_CIRO" not in text:
    text = replace_once(
        text,
        "#define OBJ_EVENT_GFX_HOOH                       238\n",
        "#define OBJ_EVENT_GFX_HOOH                       238\n#define OBJ_EVENT_GFX_MAE_CIRO                   239\n",
        "Mae Ciro constant",
    )
text = text.replace("#define NUM_OBJ_EVENT_GFX                        239", "#define NUM_OBJ_EVENT_GFX                        240")
text = text.replace("#define OBJ_EVENT_GFX_VARS   (NUM_OBJ_EVENT_GFX + 1)", "#define OBJ_EVENT_GFX_VARS   (NUM_OBJ_EVENT_GFX)")
write(path, text)

# 2) Add the graphics binary declaration.
path = "src/data/object_events/object_event_graphics.h"
text = read(path)
block = 'const u32 gObjectEventPic_MaeCiro[] = INCGFX_U32("graphics/object_events/pics/people/arauna/mae_ciro.png", ".4bpp", "-mwidth 2 -mheight 4");\n'
if "gObjectEventPic_MaeCiro" not in text:
    text += "\n" + block
write(path, text)

# 3) Add a standard nine-frame 16x32 pic table.
path = "src/data/object_events/object_event_pic_tables.h"
text = read(path)
if "sPicTable_MaeCiro" not in text:
    frames = "\n".join(f"    overworld_frame(gObjectEventPic_MaeCiro, 2, 4, {i})," for i in range(9))
    text += f"\nstatic const struct SpriteFrameImage sPicTable_MaeCiro[] = {{\n{frames}\n}};\n"
write(path, text)

# 4) Add the graphics-info record using NPC_4, matching the converted sheet palette.
path = "src/data/object_events/object_event_graphics_info.h"
text = read(path)
if "gObjectEventGraphicsInfo_MaeCiro" not in text:
    text += '''\nconst struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_MaeCiro = {
    .tileTag = TAG_NONE,
    .paletteTag = OBJ_EVENT_PAL_TAG_NPC_4,
    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,
    .size = 256,
    .width = 16,
    .height = 32,
    .paletteSlot = PALSLOT_NPC_4,
    .shadowSize = SHADOW_SIZE_M,
    .inanimate = FALSE,
    .disableReflectionPaletteLoad = FALSE,
    .tracks = TRACKS_FOOT,
    .oam = &gObjectEventBaseOam_16x32,
    .subspriteTables = sOamTables_16x32,
    .anims = sAnimTable_Standard,
    .images = sPicTable_MaeCiro,
    .affineAnims = gDummySpriteAffineAnimTable,
};
'''
write(path, text)

# 5) Expose ID 239 through the main object-event graphics pointer table.
path = "src/data/object_events/object_event_graphics_info_pointers.h"
text = read(path)
if "extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_MaeCiro;" not in text:
    text = replace_once(
        text,
        "extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_HoOh;\n",
        "extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_HoOh;\nextern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_MaeCiro;\n",
        "Mae Ciro extern",
    )
if "[OBJ_EVENT_GFX_MAE_CIRO]" not in text:
    text = replace_once(
        text,
        "    [OBJ_EVENT_GFX_HOOH] =                     &gObjectEventGraphicsInfo_HoOh,\n};",
        "    [OBJ_EVENT_GFX_HOOH] =                     &gObjectEventGraphicsInfo_HoOh,\n    [OBJ_EVENT_GFX_MAE_CIRO] =                 &gObjectEventGraphicsInfo_MaeCiro,\n};",
        "Mae Ciro pointer",
    )
write(path, text)

# 6) Target only the two gender-dependent rival-house mother objects.
for map_path in (
    "data/maps/LittlerootTown_BrendansHouse_1F/map.json",
    "data/maps/LittlerootTown_MaysHouse_1F/map.json",
):
    full = ROOT / map_path
    data = json.loads(full.read_text(encoding="utf-8"))
    matches = [o for o in data.get("object_events", []) if o.get("local_id") == "LOCALID_RIVALS_HOUSE_1F_MOM"]
    if len(matches) != 1:
        raise RuntimeError(f"{map_path}: expected exactly one rival mother, found {len(matches)}")
    matches[0]["graphics_id"] = "OBJ_EVENT_GFX_MAE_CIRO"
    full.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# 7) Document the numeric-format invariant explicitly.
write(
    "docs/ARAUNA_SUPPORT_LOT4_PLAN.md",
    '''# Arauna support characters — lot 4\n\nThis lot adds a dedicated overworld identity for Ciro's mother by using the one vanilla object-graphics numeric value (239) that Emerald intentionally leaves empty.\n\n- `OBJ_EVENT_GFX_MAE_CIRO = 239`\n- `NUM_OBJ_EVENT_GFX` changes from 239 to 240.\n- `OBJ_EVENT_GFX_VARS` changes from `NUM_OBJ_EVENT_GFX + 1` to `NUM_OBJ_EVENT_GFX`, so dynamic IDs remain exactly 240-255.\n- No field storing object graphics IDs changes size; all remain one byte.\n- Both gender-dependent rival-house mother events use the same dedicated visual.\n- Coordinates, scripts, flags, movement, warps and story progression are unchanged.\n'''
)

print("Arauna support lot 4 applied successfully.")

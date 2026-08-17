#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

SPRITES = (
    "graphics/object_events/pics/people/dona_zila.png",
    "graphics/object_events/pics/people/ciro/phase2.png",
    "graphics/object_events/pics/people/ciro/phase3.png",
)


def replace_once(path_rel, old, new):
    path = ROOT / path_rel
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Expected text not found in {path_rel}: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def regex_replace_once(path_rel, pattern, replacement):
    path = ROOT / path_rel
    text = path.read_text(encoding="utf-8")
    text2, n = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"Expected exactly one regex match in {path_rel}, got {n}")
    path.write_text(text2, encoding="utf-8")


# The PNGs are committed as binary Git blobs before this script runs.
for rel in SPRITES:
    path = ROOT / rel
    if not path.is_file() or path.stat().st_size <= 0:
        raise SystemExit(f"Missing dedicated sprite: {rel}")

# Reclaim three object graphics IDs explicitly marked unused by vanilla Emerald.
constants = ROOT / "include/constants/event_objects.h"
ctext = constants.read_text(encoding="utf-8")
anchor = "#define OBJ_EVENT_GFX_UNUSED_SQUIRTLE_DOLL        78\n"
aliases = (
    anchor
    + "\n// Arauna dedicated overworld slots: reclaim three vanilla IDs marked unused.\n"
    + "#define OBJ_EVENT_GFX_DONA_ZILA                  OBJ_EVENT_GFX_UNUSED_NATU_DOLL\n"
    + "#define OBJ_EVENT_GFX_CIRO_CONSORCIO             OBJ_EVENT_GFX_UNUSED_MAGNEMITE_DOLL\n"
    + "#define OBJ_EVENT_GFX_CIRO_FINAL                 OBJ_EVENT_GFX_UNUSED_SQUIRTLE_DOLL\n"
)
if "OBJ_EVENT_GFX_DONA_ZILA" not in ctext:
    if anchor not in ctext:
        raise SystemExit("Could not locate unused graphics ID anchor")
    constants.write_text(ctext.replace(anchor, aliases, 1), encoding="utf-8")

# Keep the original symbol names at indices 76-78, but repoint them to Arauna sheets.
graphics = "src/data/object_events/object_event_graphics.h"
replace_once(
    graphics,
    'const u32 gObjectEventPic_UnusedNatuDoll[] = INCGFX_U32("graphics/object_events/pics/dolls/unused_natu_doll.png", ".4bpp");',
    'const u32 gObjectEventPic_UnusedNatuDoll[] = INCGFX_U32("graphics/object_events/pics/people/dona_zila.png", ".4bpp", "-mwidth 2 -mheight 4");',
)
replace_once(
    graphics,
    'const u32 gObjectEventPic_UnusedMagnemiteDoll[] = INCGFX_U32("graphics/object_events/pics/dolls/unused_magnemite_doll.png", ".4bpp");',
    'const u32 gObjectEventPic_UnusedMagnemiteDoll[] = INCGFX_U32("graphics/object_events/pics/people/ciro/phase2.png", ".4bpp", "-mwidth 2 -mheight 4");',
)
replace_once(
    graphics,
    'const u32 gObjectEventPic_UnusedSquirtleDoll[] = INCGFX_U32("graphics/object_events/pics/dolls/unused_squirtle_doll.png", ".4bpp");',
    'const u32 gObjectEventPic_UnusedSquirtleDoll[] = INCGFX_U32("graphics/object_events/pics/people/ciro/phase3.png", ".4bpp", "-mwidth 2 -mheight 4");',
)


def nine_frame_table(table_name, pic_name):
    frames = "\n".join(
        f"    overworld_frame({pic_name}, 2, 4, {i})," for i in range(9)
    )
    return f"static const struct SpriteFrameImage {table_name}[] = {{\n{frames}\n}};"


pic_tables = "src/data/object_events/object_event_pic_tables.h"
for table, pic in (
    ("sPicTable_UnusedNatuDoll", "gObjectEventPic_UnusedNatuDoll"),
    ("sPicTable_UnusedMagnemiteDoll", "gObjectEventPic_UnusedMagnemiteDoll"),
    ("sPicTable_UnusedSquirtleDoll", "gObjectEventPic_UnusedSquirtleDoll"),
):
    regex_replace_once(
        pic_tables,
        rf"static const struct SpriteFrameImage {table}\[\] = \{{.*?\n\}};",
        nine_frame_table(table, pic),
    )


def npc_info(struct_name, palette_tag, palette_slot, pic_table):
    return f"""const struct ObjectEventGraphicsInfo {struct_name} = {{
    .tileTag = TAG_NONE,
    .paletteTag = {palette_tag},
    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,
    .size = 256,
    .width = 16,
    .height = 32,
    .paletteSlot = {palette_slot},
    .shadowSize = SHADOW_SIZE_M,
    .inanimate = FALSE,
    .disableReflectionPaletteLoad = FALSE,
    .tracks = TRACKS_FOOT,
    .oam = &gObjectEventBaseOam_16x32,
    .subspriteTables = sOamTables_16x32,
    .anims = sAnimTable_Standard,
    .images = {pic_table},
    .affineAnims = gDummySpriteAffineAnimTable,
}};"""


info = "src/data/object_events/object_event_graphics_info.h"
for struct_name, pal_tag, pal_slot, table in (
    ("gObjectEventGraphicsInfo_UnusedNatuDoll", "OBJ_EVENT_PAL_TAG_NPC_3", "PALSLOT_NPC_3", "sPicTable_UnusedNatuDoll"),
    ("gObjectEventGraphicsInfo_UnusedMagnemiteDoll", "OBJ_EVENT_PAL_TAG_NPC_4", "PALSLOT_NPC_4", "sPicTable_UnusedMagnemiteDoll"),
    ("gObjectEventGraphicsInfo_UnusedSquirtleDoll", "OBJ_EVENT_PAL_TAG_NPC_4", "PALSLOT_NPC_4", "sPicTable_UnusedSquirtleDoll"),
):
    regex_replace_once(
        info,
        rf"const struct ObjectEventGraphicsInfo {struct_name} = \{{.*?\n\}};",
        npc_info(struct_name, pal_tag, pal_slot, table),
    )


docs = ROOT / "docs/ARAUNA_DEDICATED_GFX_SLOTS.md"
docs.parent.mkdir(parents=True, exist_ok=True)
docs.write_text("""# Arauna dedicated overworld graphics slots

Three object-event graphics IDs explicitly marked unused by vanilla Pokémon Emerald are reclaimed for Arauna story characters without increasing `NUM_OBJ_EVENT_GFX`.

| Arauna constant | ID | Vanilla storage reclaimed | Runtime palette |
| --- | ---: | --- | --- |
| `OBJ_EVENT_GFX_DONA_ZILA` | 76 | `OBJ_EVENT_GFX_UNUSED_NATU_DOLL` | `NPC_3` |
| `OBJ_EVENT_GFX_CIRO_CONSORCIO` | 77 | `OBJ_EVENT_GFX_UNUSED_MAGNEMITE_DOLL` | `NPC_4` |
| `OBJ_EVENT_GFX_CIRO_FINAL` | 78 | `OBJ_EVENT_GFX_UNUSED_SQUIRTLE_DOLL` | `NPC_4` |

The inherited unused symbols remain the numeric storage at indices 76-78, while their graphics-info records are converted to standard 16x32 walking NPCs with nine overworld frames.

This reserves stable story-character IDs while keeping Emerald's one-byte object graphics ID format and the original `NUM_OBJ_EVENT_GFX` limit unchanged.
""", encoding="utf-8")

print("Arauna dedicated overworld slots applied:")
print("  76 -> OBJ_EVENT_GFX_DONA_ZILA")
print("  77 -> OBJ_EVENT_GFX_CIRO_CONSORCIO")
print("  78 -> OBJ_EVENT_GFX_CIRO_FINAL")

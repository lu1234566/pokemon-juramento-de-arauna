#!/usr/bin/env python3
from pathlib import Path
import base64
import re

ROOT = Path(__file__).resolve().parents[1]

PAYLOADS = {
    "graphics/object_events/pics/people/dona_zila.png": "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",
    "graphics/object_events/pics/people/ciro/phase2.png": "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",
    "graphics/object_events/pics/people/ciro/phase3.png": "iVBORw0KGgoAAAANSUhEUgAAAJAAAAAgCAMAAADKUgH/AAADAFBMVEVzxaT/1bT/xZTelHN7QUFqi6w5SmIIECDVc6SkQXNSIEHV1dWLi5RBQVL///8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAClFWJnAAAAAXRSTlMAQObYZgAAA8dJREFUeJztV9tuXTkItQwSMsf//73lDk7aqm8jjeKXHLANi8VlO2v9rJ/1s/7/i3Sh/ln0X2OxResQK5y1+N8v/Rm7hhcBuvklMq1SfDsvznkRANOhqXxO3b/DQcT2x4SXTiM4pB4GALBfqj2OWPxfWOVfvC+2BBUj9MBnxm/hYP88VxbiLVUcFkc85LJJe+uPQ3VOk6LeT98XUDM/Uzh0UV0OkkSjZZZ4DdC9OwPEdhQWKIj4AvgM//xGnMGYA9R4O33oBBQDFIzcIcraomsA54mKay9tIr4F+mbgyRAZnrvTgibDPKYJehhhtF1TjiBGBpVCnLvL5T5whdTTcI4joC/+Q0Gu4LZgClRGMljRAIgRPOlwGPAam3jD/s0AI6SErxaN8eTHnGlSyN2bfyjFsRNXFVabQhEIID2URRQOMeM18zezxGhi3G8GMoeYFcCZAQh7FITIAo0jKVN4RkgCkoRvour8ZKAMhBiA8Nk/QUcd566RY9aEMjZS4j7hhzbwpxKiQwBllmSdMn42AMoke1KgiE0kthxEADamzLzLuskTv/SXUl4A0CZl41k6NPfesLPsWMDBxk82KpPtV18czFUhxwp7lNsna9TwhQHpUWkRhYkBUNiQEhl9KpNMpmu3KaHig+4pos2jUcMhZ+c88BpRZpjEkkg1eBTBLjwSEMjC6V8Zm5NBfl5oGdkPPDe+nP+tnD2gDmEMQqkQgDEZ5cBzXev1ShyQiPVzqXWUXwIpuqssVZf5qrm1Xd45SY1OVaQLKQCag8hP/CnA+3HzOz8NKA62VFq0tQG2yssiMMTCol84ekBVd0eXmLfp4iUwFJ1iEfduQjfSE6EgIeOHbZap37APPtz29cYSCO4fIue+bex6jLe+pvf9fFtAI8UXO2nqzN4C+qYxgoAckFNE4OFUUGddfwLl5Er/+U1tOQYFk70nsJJmzxnIrpHc4XaLll/1z+ig0iAiJQEyIWUPQ/s6DApTw/b+kYD4AaSR7pm0E+FFm3lJ26WzvISDYeA3YKsJuqccetEABat0RkUOyoPNLJID2qIjSYxekG+J4VcLXVUZ4dNV/FxgzUNK5srOeAbCPI8ieRy4DJu+bdcsfyIg5AcwBz6ON2ncJR+MZatSHgHI36xpL8l+Nz/mM4Q2oNyz1m7LbfRlcL4B65FN9jYs+2fxWTTHjPcMnZNJiozVpPeemgTae5MDEPcjfIZsXvvG28UNsNLev5kcw8qUoL5pccS77BPHDfeLhZmBUj3P8PWs3/zD835I7A+Ugl1xeGVCSvsLklg3HYOEqywAAAAASUVORK5CYII="
}

for rel, data in PAYLOADS.items():
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(data))

def replace_once(path_rel, old, new):
    path = ROOT / path_rel
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Expected text not found in {path_rel}: {old[:80]!r}")
    text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")

def regex_replace_once(path_rel, pattern, replacement):
    path = ROOT / path_rel
    text = path.read_text(encoding="utf-8")
    text2, n = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"Expected exactly one regex match in {path_rel} for {pattern!r}, got {n}")
    path.write_text(text2, encoding="utf-8")

# Reclaim three explicitly unused vanilla graphics IDs without increasing NUM_OBJ_EVENT_GFX.
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
    ctext = ctext.replace(anchor, aliases, 1)
    constants.write_text(ctext, encoding="utf-8")

# Point the reclaimed image symbols to Arauna character sheets and use 16x32 frame geometry.
graphics = "src/data/object_events/object_event_graphics.h"
replace_once(
    graphics,
    'const u32 gObjectEventPic_UnusedNatuDoll[] = INCGFX_U32("graphics/object_events/pics/dolls/unused_natu_doll.png", ".4bpp");',
    'const u32 gObjectEventPic_UnusedNatuDoll[] = INCGFX_U32("graphics/object_events/pics/people/dona_zila.png", ".4bpp", "-mwidth 2 -mheight 4");'
)
replace_once(
    graphics,
    'const u32 gObjectEventPic_UnusedMagnemiteDoll[] = INCGFX_U32("graphics/object_events/pics/dolls/unused_magnemite_doll.png", ".4bpp");',
    'const u32 gObjectEventPic_UnusedMagnemiteDoll[] = INCGFX_U32("graphics/object_events/pics/people/ciro/phase2.png", ".4bpp", "-mwidth 2 -mheight 4");'
)
replace_once(
    graphics,
    'const u32 gObjectEventPic_UnusedSquirtleDoll[] = INCGFX_U32("graphics/object_events/pics/dolls/unused_squirtle_doll.png", ".4bpp");',
    'const u32 gObjectEventPic_UnusedSquirtleDoll[] = INCGFX_U32("graphics/object_events/pics/people/ciro/phase3.png", ".4bpp", "-mwidth 2 -mheight 4");'
)

def nine_frame_table(table_name, pic_name):
    frames = "\n".join(
        f"    overworld_frame({pic_name}, 2, 4, {i})," for i in range(9)
    )
    return (
        f"static const struct SpriteFrameImage {table_name}[] = {{\n"
        + frames
        + "\n};"
    )

pic_tables = "src/data/object_events/object_event_pic_tables.h"
for table, pic in [
    ("sPicTable_UnusedNatuDoll", "gObjectEventPic_UnusedNatuDoll"),
    ("sPicTable_UnusedMagnemiteDoll", "gObjectEventPic_UnusedMagnemiteDoll"),
    ("sPicTable_UnusedSquirtleDoll", "gObjectEventPic_UnusedSquirtleDoll"),
]:
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
for struct_name, pal_tag, pal_slot, table in [
    ("gObjectEventGraphicsInfo_UnusedNatuDoll", "OBJ_EVENT_PAL_TAG_NPC_3", "PALSLOT_NPC_3", "sPicTable_UnusedNatuDoll"),
    ("gObjectEventGraphicsInfo_UnusedMagnemiteDoll", "OBJ_EVENT_PAL_TAG_NPC_4", "PALSLOT_NPC_4", "sPicTable_UnusedMagnemiteDoll"),
    ("gObjectEventGraphicsInfo_UnusedSquirtleDoll", "OBJ_EVENT_PAL_TAG_NPC_4", "PALSLOT_NPC_4", "sPicTable_UnusedSquirtleDoll"),
]:
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

The original unused constant names remain defined and act as the underlying numeric storage aliases, so any inherited reference still compiles. The graphics-info records at those indices are converted to standard 16x32 walking NPCs with nine overworld frames.

This reserves stable IDs for story implementation while keeping Emerald's one-byte object graphics ID format and the original `NUM_OBJ_EVENT_GFX` limit unchanged.
""", encoding="utf-8")

# Structural assertions before compilation.
for rel in PAYLOADS:
    path = ROOT / rel
    if path.stat().st_size <= 0:
        raise SystemExit(f"Empty generated sprite: {rel}")

print("Arauna dedicated overworld slots applied:")
print("  76 -> OBJ_EVENT_GFX_DONA_ZILA")
print("  77 -> OBJ_EVENT_GFX_CIRO_CONSORCIO")
print("  78 -> OBJ_EVENT_GFX_CIRO_FINAL")

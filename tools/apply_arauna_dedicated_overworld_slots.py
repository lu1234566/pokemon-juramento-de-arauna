#!/usr/bin/env python3
from pathlib import Path
import base64
import re

ROOT = Path(__file__).resolve().parents[1]

PAYLOADS = {
    "graphics/object_events/pics/people/dona_zila.png": "iVBORw0KGgoAAAANSUhEUgAAAJAAAAAgBAMAAAAPouz+AAAAMFBMVEVzxaT/1bT/xZTelHN7QUHNzd6cnL1KSntzvQBBewAQOQDNYkqUOSlSEAD///8AAAAxiAJzAAAAAXRSTlMAQObYZgAABNNJREFUeNrtlU+MHEcVh7/uaS/erMevN4AIhnhicYuQsquRERdrGrzeC7ZmLTaDhBTNGLzLIYEZI4GNEEyi3OCAzcFC4k8CRxCRITngi7MGK5FglmmDQUKaVq8jEUsEZV8zPTMBpvZx6ElsIoQQ4kgduupX9fqrqifV+8H/23/URP83HDuxPgMCELwNa/qvNzKwu8oHaYW+AthqGyDbtHvjg+ui6dvIAHjg3ZU+8OwzBzuAPMpIodxh9d4TLNQan1n6J5AXzgbjtr0lfYJrH3n8RzsAPzj0yhr43vcOFXGqALphuyMFVmZXV9hQkNxs/AlFGiDgs//p73zLvRCBml69AnwtJgSQdYkVyBZ5HJBfrawpwGOjum0ot9/XuABII8ybPwGf+MXSX4/v/wZy7oFzpyHQd3/9zLoCdxYbzwRAuOMdbAJ37p8TIP857zjnQXwtvHMphNcm58JACOQDW5sPP1k6gnr9D9oBrcQvfoyf7YLEi+l9C4jzjux9swW6IVkHmG7d5tLrHY7ZpdY84dx4XNn7cHyEuVHj6NF1p7jkxFpiYDZeN1PkxqONdlvnmv26e6kN4/FGYwrBSt39vn1WZb3tVk/myObvzqb5ahTM4/bw/VgmF7wX9v1QK/Hl19m87ymiZQ7uPMT8q0tf/U33YYQv3T7sabgg93/qWb4czsnl0VV3g+zy3749Xqxd8V8+o6CtKPPMLWknZinTnZ0/wnv62cIXXiWzMx/dqzxF1nTPvfZyG3Rn0rmozF985C+fKwkwP+l8chckt2G+kiON48PahzZhfHZYHa4qqycH/VE7QsysAuTr096qwrB0YrM+Bfv4pzfrBv38bKNWxx+dPNpq7U7JvvtTOPwHeG/riV9710KulYauzRZ7e288SQSh5stX1wDd6zwUwBpxJ9sHyyw8F4NHbsdKPQ8sb72y//kQ6t7uu/58HdEwGk23yA5u71+aFm8rI6S0dCC8koUMo97a90MI/j6y6MB1CCxJM4XAqlUDqA+rpiCVSfe3SnDa9bZvNkHeb901QMzSWwpi+6wJSGAuVWCUqGVNkAen/ZsRSGXaiysgx8yyEAlcbzutgFYGvVQBt1g2BR5bNAPKdrOigIys0swrkFWmllUga2rJrQGutz0SpPaVLWfViGUZHEgUZHj6lLsFYl4tBSzNFg0oVW3StapSn5rdWAG1vokp2XYvseNaTpIkcYnKMR30kyU4lT44cTmI5ZYCLrbFgUKp1rfxE06lOjn/xXpVGSYm9aqSJ1PnhiouNcPA4iRJFcqpbZcVgs3jlgKnxmZJBJjFsXORpL1sdNIpycD1P1tV0iRJkhTKabfbUyg7czlA2ZI+IPXUGcBAUfAJdx758c5wC5btT08Dn/f8qPXLkMPv9A9ZBv4DvPE84BtFefEv+ABc3PuFV1ToWUWdnDcDJDnfHSiQTCxRCHQysQjIySMgMOsqwHRiBmBFh02sD0BZ3C1ArDsxBaQ3CzyfrxQ1Wa3YuFb82K3nCpRXIgAZvkmUtK4AcW2lXujyLQBOWApIoi5RwKUFP41wKVC3HMClKgVJioPhYkkjQJJgNuEKUFyAxFIAl6gkCqTJXZ3MRgCSpOVEgeILwaAwmrd8TdwstUV2XQESpzNHmiU9MJUiRzPferO/a8j23zpw/O/Xo3vFPwB33LNGw2ueuQAAAABJRU5ErkJggg==",
    "graphics/object_events/pics/people/ciro/phase2.png": "iVBORw0KGgoAAAANSUhEUgAAAJAAAAAgCAMAAABTfcpyAAAAPFBMVEVzxaT/1bT/xZTelHN7QUFqi6w5SmIIECDVc6SkQXNSIEHV1dWLi5RBQVL///8AAAAAAAAAAAAAAAAAAAAAAADNfHjAAAAAE3RSTlMA/////////////wAAAAAAAAAAE7cWQAAAAdFJREFUWMPtllmSwyAMRF0iE0Jm7n9bKZOYNh7BKTuVCV7Vx2m8BCq0hCf48+mflB6Rt7dsY2TsfSKp0lDzgBdDsBaY9V4gFO9VwE8l9xGhRDho6Q6cJhNsGmLAdXQwB5cViLCbA1vRQQTxhA0VxDXJGdAHxRfwJwQ29RHMn0swi03iwA5fS+Ue6gmf7UQm7S07sYIb/5ATt7wC7a6cna2uOhhTcNsLa1QrrVIm0AmnSHy2gU3GmDrSvRfDji8l8BcLRXLS22h3QqmzobFezGRJZjWxC0FyKRak0ZZTo+ow4W1Bm6s2rf8IaRac8OTIRnkCk0u9sJ2tRaNc/cafdpucYs1CDUuC0aKmaGNe8LQ/taFmAS5CbtwSnbiQ3UCqqdNiJJjXH4HAnxYPG0pO7EJfgaioTCMqRkvNz38QYjo/GqbDeyLcYRK5WGbJ1CeA2vhZoARieNywNs4/QKeDvGn5Aa0iiIjKpQF7hVtyqHGofbykdUmUxkd47ovDsH/N76BgaE4c3ZKmf7y0VWj2yK6/zVUNtyU0ssbmv4ghzeCZQ/xTuXac++wpKgTCbhRN0NaYkfjMkc5WqaWRpd1Ee4KcXj1G0X67sZXMI3BdSdH/0XgH9/J2D5B/DwH6IAuO0AAAAASUVORK5CYII=",
    "graphics/object_events/pics/people/ciro/phase3.png": "iVBORw0KGgoAAAANSUhEUgAAAJAAAAAgCAMAAABTfcpyAAAAPFBMVEVzxaT/1bT/xZTelHN7QUFqi6w5SmIIECDVc6SkQXNSIEHV1dWLi5RBQVL///8AAAAAAAAAAAAAAAAAAAAAAADNfHjAAAAAE3RSTlMA/////////////wAAAAAAAAAAE7cWQAAAAbhJREFUWMPtllmSxCAMRBEQE0Lm9r+tlElMGo/gVHWplFP1dQK0hCL48+lfKz6id7ZsY2RsvSNp0lDzgCdDsBaY9V4gFO9VwE8l9xGhRDho6Q6cJhNsGmLAdXQwB5cViLCbA1vRQQTxhA0VxDXJGdAHxRfwJwQ29RHMn0swi03iwA5fS+Ue6gmf7UQm7S07sYIb/5ATt7wC7a6cna2uOhhTcNsLa1QrrVIm0AmnSHy2gU3GmDrSvRfDji8l8BcLRXLS22h3QqmzobFezGRJZjWxC0FyKRak0ZZTo+ow4W1Bm6s2rf8IaRac8OTIRnkCk0u9sJ2tRaNc/cafdpucYs1CDUuC0aKmaGNe8LQ/taFmAS5CbtwSnbiQ3UCqqdNiJJjXH4HAnxYPG0pO7EJfgaioTCMqRkvNz38QYjo/GqbDeyLcYRK5WGbJ1CeA2vhZoARieNywNs4/QKeDvGn5Aa0iiIjKpQF7hVtyqHGofbykdUmUxkd47ovDsH/N76BgaE4c3ZKmf7y0VWj2yK6/zVUNtyU0ssbmv4ghzeCZQ/xTuXac++wpKgTCbhRN0NaYkfjMkc5WqaWRpd1Ee4KcXj1G0X67sZXMI3BdSdH/0XgH9/J2D5B/DwH6IAuO0AAAAASUVORK5CYII="
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

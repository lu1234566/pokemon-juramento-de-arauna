#!/usr/bin/env python3
"""Make all 46 Arauna overworlds reachable without spending 46 graphics ids.

Phase one wired six species and stopped, because an object event graphics id is
one byte and only three values were free. This puts the other forty back within
reach by separating "which slot the map names" from "which creature that slot
shows", which is a pattern the engine already contains:

    if (graphicsId == OBJ_EVENT_GFX_BARD)
        return gMauvilleOldManGraphicsInfoPointers[GetCurrentMauvilleOldMan()];

OBJ_EVENT_GFX_BARD does not index gObjectEventGraphicsInfoPointers at all. It
dispatches through a second table using state held outside the object. Two
Arauna dispatcher ids do exactly the same thing against a registry of all 46:

    gAraunaOverworldGraphicsInfo[channel][VarGet(selector)]

Nothing persistent changes. ObjectEventTemplate.graphicsId and
ObjectEvent.graphicsId stay u8 and stay inside 0..239; the map still names an
ordinary graphics id; SaveBlock1 is byte-identical; and the selector rides in
VAR_OBJ_GFX_ID_C and VAR_OBJ_GFX_ID_D, two of the three object-gfx vars vanilla
never writes, so the choice survives a save without adding a var.

Two channels, because the limit that actually bites is palettes, not ids. A
graphics info names one palette slot, and two objects sharing a slot with
different tags fight over it. Channel A takes PALSLOT_NPC_SPECIAL, the vanilla
"unique NPC" slot. Channel B sets paletteSlot to 16 + PALSLOT_NPC_SPECIAL_REFLECTION,
which is the engine's own escape hatch -- TrySetupObjectEventSprite subtracts 16
and patches that hardware bank directly -- and bank 11 is otherwise only the
reflection of a special NPC, which these never cast because they set
disableReflectionPaletteLoad.

Generated:

  include/constants/arauna_overworld.h            ARAUNA_OW_* selector values
  src/data/object_events/arauna_overworld.h       the 46 x 2 registry
  src/data/object_events/object_event_pic_tables.h   46 pic tables
  src/data/object_events/object_event_graphics.h     46 sheet + palette decls

  --check   report the registry that would be built
  --write   generate it and patch the engine
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELECTION = ROOT / "docs/arauna/ARAUNA_OVERWORLD_46.csv"

OW_CONSTANTS = ROOT / "include/constants/arauna_overworld.h"
REGISTRY = ROOT / "src/data/object_events/arauna_overworld.h"
CONSTANTS = ROOT / "include/constants/event_objects.h"
VARS = ROOT / "include/constants/vars.h"
GRAPHICS = ROOT / "src/data/object_events/object_event_graphics.h"
PIC_TABLES = ROOT / "src/data/object_events/object_event_pic_tables.h"
POINTERS = ROOT / "src/data/object_events/object_event_graphics_info_pointers.h"
MOVEMENT = ROOT / "src/event_object_movement.c"

BEGIN = "// BEGIN Arauna overworld redraws"
END = "// END Arauna overworld redraws"

# The two ids phase one spent on individual species become the dispatchers.
DISPATCHERS = [
    ("OBJ_EVENT_GFX_ARAUNA_POKEMON_A", "OBJ_EVENT_GFX_ARAUNA_IEMANJA"),
    ("OBJ_EVENT_GFX_ARAUNA_POKEMON_B", "OBJ_EVENT_GFX_ARAUNA_LOBISOMEM"),
]
# Phase one also took id 239 for Preto-Velho; give it back, unused.
RETIRED = "OBJ_EVENT_GFX_ARAUNA_PRETO_VELHO"


def symbol(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def constant(name: str) -> str:
    ascii_name = unicodedata.normalize("NFD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]+", "_", ascii_name.upper()).strip("_")


def species(rows):
    return [dict(row, sym=symbol(row["slug"]), const=f"ARAUNA_OW_{constant(row['name'])}")
            for row in rows]


def splice(text: str, block: str, anchor: str) -> str:
    if BEGIN in text:
        head, rest = text.split(BEGIN, 1)
        _, tail = rest.split(END, 1)
        return f"{head}{BEGIN}\n{block}{END}{tail}"
    return text.replace(anchor, anchor + "\n" + f"{BEGIN}\n{block}{END}\n", 1)


def render_constants(mons) -> str:
    lines = [
        "#ifndef GUARD_CONSTANTS_ARAUNA_OVERWORLD_H",
        "#define GUARD_CONSTANTS_ARAUNA_OVERWORLD_H",
        "",
        "// Which of the 46 Arauna overworld redraws a dispatcher slot is showing.",
        "// Store one of these in VAR_ARAUNA_OW_A or VAR_ARAUNA_OW_B; the object event",
        "// on the map names OBJ_EVENT_GFX_ARAUNA_POKEMON_A or _B and picks it up.",
        "//",
        "// These are registry indices, not object event graphics ids and not species",
        "// ids. Nothing here reaches the save.",
        "",
        "#define ARAUNA_OW_NONE 0",
    ]
    for i, mon in enumerate(mons, start=1):
        lines.append(f"#define {mon['const']:<34} {i:>3}  // #{mon['arauna_dex']} {mon['name']}")
    lines += [
        "",
        f"#define ARAUNA_OW_COUNT {len(mons) + 1}",
        "",
        "#define ARAUNA_OW_CHANNEL_A 0",
        "#define ARAUNA_OW_CHANNEL_B 1",
        "#define ARAUNA_OW_CHANNELS  2",
        "",
        "#endif // GUARD_CONSTANTS_ARAUNA_OVERWORLD_H",
        "",
    ]
    return "\n".join(lines)


def render_graphics(mons) -> str:
    lines = []
    for mon in mons:
        name = f"{mon['arauna_dex']}_{mon['slug']}"
        lines.append(f'const u32 gObjectEventPic_Arauna{mon["sym"]}[] = '
                     f'INCGFX_U32("graphics/object_events/pics/pokemon/arauna/{name}.png", '
                     f'".4bpp", "-mwidth 8 -mheight 8");')
        lines.append(f'const u16 gObjectEventPal_Arauna{mon["sym"]}[] = '
                     f'INCGFX_U16("graphics/object_events/palettes/arauna_{name}.pal", ".gbapal");')
    return "\n".join(lines) + "\n"


def render_pic_tables(mons) -> str:
    lines = []
    for mon in mons:
        lines.append(f"static const struct SpriteFrameImage sPicTable_Arauna{mon['sym']}[] = {{")
        # South, North, West, then the walk frames, which reuse the idle pose:
        # these are single-pose redraws, so a walking creature keeps facing.
        for frame in (0, 1, 2, 0, 0, 1, 1, 2, 2):
            lines.append(f"    overworld_frame(gObjectEventPic_Arauna{mon['sym']}, 8, 8, {frame}),")
        lines.append("};")
    return "\n".join(lines) + "\n"


INFO = """static const struct ObjectEventGraphicsInfo sAraunaOverworld{channel}_{sym} = {{
    .tileTag = TAG_NONE,
    .paletteTag = OBJ_EVENT_PAL_TAG_ARAUNA_{tag},
    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,
    .size = 2048,
    .width = 64,
    .height = 64,
    .paletteSlot = {slot},
    .shadowSize = SHADOW_SIZE_M,
    .inanimate = FALSE,
    .disableReflectionPaletteLoad = TRUE,
    .tracks = TRACKS_FOOT,
    .oam = &gObjectEventBaseOam_64x64,
    .subspriteTables = sOamTables_64x64,
    .anims = sAnimTable_Standard,
    .images = sPicTable_Arauna{sym},
    .affineAnims = gDummySpriteAffineAnimTable,
}};
"""


def render_registry(mons) -> str:
    out = [
        "// Generated by tools/arauna/build_overworld_registry.py. Do not edit.",
        "//",
        "// Every one of the 46 redraws, twice: once per dispatcher channel. The two",
        "// copies differ only in which palette slot they claim, which is what lets two",
        "// different creatures stand on the same map at the same time. Channel B uses",
        "// the engine's 16 + slot form, so TrySetupObjectEventSprite patches hardware",
        "// bank PALSLOT_NPC_SPECIAL_REFLECTION directly instead of contending for the",
        "// single special slot.",
        "",
    ]
    slots = {"A": "PALSLOT_NPC_SPECIAL", "B": "16 + PALSLOT_NPC_SPECIAL_REFLECTION"}
    for channel in ("A", "B"):
        for mon in mons:
            out.append(INFO.format(channel=channel, sym=mon["sym"],
                                   tag=mon["slug"].upper(), slot=slots[channel]))
    out.append("static const struct ObjectEventGraphicsInfo *const "
               "gAraunaOverworldGraphicsInfo[ARAUNA_OW_CHANNELS][ARAUNA_OW_COUNT] =\n{")
    for channel in ("A", "B"):
        out.append(f"    [ARAUNA_OW_CHANNEL_{channel}] =")
        out.append("    {")
        # ARAUNA_OW_NONE renders the first creature rather than nothing, so a slot
        # a script forgot to set is visibly wrong instead of a null dereference.
        out.append(f"        [ARAUNA_OW_NONE] = &sAraunaOverworld{channel}_{mons[0]['sym']},")
        for mon in mons:
            out.append(f"        [{mon['const']}] = &sAraunaOverworld{channel}_{mon['sym']},")
        out.append("    },")
    out.append("};\n")
    return "\n".join(out)


def edit_event_objects(text: str) -> str:
    """Turn two of phase one's per-species ids into dispatchers, free the third."""
    for new, old in DISPATCHERS:
        pattern = re.compile(rf"^#define {re.escape(old)}(\s+)(\d+)$", re.M)
        match = pattern.search(text)
        if match:
            width = len(old) + len(match.group(1))
            text = pattern.sub(f"#define {new}{' ' * max(1, width - len(new))}{match.group(2)}",
                               text, count=1)
        elif not re.search(rf"^#define {re.escape(new)}\s+\d+$", text, re.M):
            raise ValueError(f"neither {old} nor {new} is defined")

    # Preto-Velho gave 239 back; it is reachable through the registry like the rest.
    text = re.sub(rf"^#define {re.escape(RETIRED)}\s+239\n\n"
                  r"// Id 239 was left unused.*?\n// \+1\. Arauna uses it.*?\n"
                  r"#define NUM_OBJ_EVENT_GFX                        240$",
                  "#define NUM_OBJ_EVENT_GFX                        239", text, flags=re.M | re.S)
    text = text.replace("#define OBJ_EVENT_GFX_VARS   (NUM_OBJ_EVENT_GFX)",
                        "#define OBJ_EVENT_GFX_VARS   (NUM_OBJ_EVENT_GFX + 1)")
    return text


def edit_vars(text: str) -> str:
    block = ("// Arauna overworld dispatcher selectors. These are VAR_OBJ_GFX_ID_C and _D,\n"
             "// two of the three object-gfx vars vanilla never writes, reused rather than\n"
             "// added so the save layout does not move. They hold an ARAUNA_OW_* registry\n"
             "// index, not a graphics id, and only OBJ_EVENT_GFX_ARAUNA_POKEMON_A/_B read them.\n"
             "#define VAR_ARAUNA_OW_A            VAR_OBJ_GFX_ID_C\n"
             "#define VAR_ARAUNA_OW_B            VAR_OBJ_GFX_ID_D\n")
    return splice(text, block, "#define VAR_OBJ_GFX_ID_F           0x401F")


def edit_movement(text: str) -> str:
    """Add the dispatch, mirroring the Bard branch immediately above it."""
    if "gAraunaOverworldGraphicsInfo" not in text:
        text = text.replace('#include "data/object_events/object_event_graphics_info.h"',
                            '#include "data/object_events/object_event_graphics_info.h"\n'
                            '#include "data/object_events/arauna_overworld.h"', 1)
    anchor = """    if (graphicsId == OBJ_EVENT_GFX_BARD)
    {
        bard = GetCurrentMauvilleOldMan();
        return gMauvilleOldManGraphicsInfoPointers[bard];
    }
"""
    added = """
    // Same shape as the Bard above: the id names a dispatcher, not a creature, and
    // the creature comes from a second table indexed by state held outside the
    // object. That is what keeps all 46 reachable from two one-byte ids.
    if (graphicsId == OBJ_EVENT_GFX_ARAUNA_POKEMON_A)
        return gAraunaOverworldGraphicsInfo[ARAUNA_OW_CHANNEL_A][AraunaOverworldSelection(VAR_ARAUNA_OW_A)];

    if (graphicsId == OBJ_EVENT_GFX_ARAUNA_POKEMON_B)
        return gAraunaOverworldGraphicsInfo[ARAUNA_OW_CHANNEL_B][AraunaOverworldSelection(VAR_ARAUNA_OW_B)];
"""
    if "OBJ_EVENT_GFX_ARAUNA_POKEMON_A" not in text:
        text = text.replace(anchor, anchor + added, 1)

    helper = """
// Clamp the selector so a stale or unset var can never index past the registry.
static u16 AraunaOverworldSelection(u16 var)
{
    u16 selection = VarGet(var);

    if (selection >= ARAUNA_OW_COUNT)
        return ARAUNA_OW_NONE;

    return selection;
}
"""
    if "AraunaOverworldSelection" not in text.split("const struct ObjectEventGraphicsInfo *GetObjectEventGraphicsInfo")[0]:
        text = text.replace("const struct ObjectEventGraphicsInfo *GetObjectEventGraphicsInfo(u8 graphicsId)",
                            helper.lstrip("\n") +
                            "\nconst struct ObjectEventGraphicsInfo *GetObjectEventGraphicsInfo(u8 graphicsId)", 1)
    if "SetAraunaPokemonOverworld" not in text:
        text = text.rstrip("\n") + "\n" + API

    if '#include "constants/arauna_overworld.h"' not in text:
        text = text.replace('#include "constants/event_objects.h"',
                            '#include "constants/event_objects.h"\n'
                            '#include "constants/arauna_overworld.h"', 1)
    return text


API = """
// Script API: point one dispatcher channel at a creature and refresh the object
// that is showing it, so a map can change which Arauna Pokemon stands there
// without a reload.
//
//     setvar VAR_0x8004, <localId>
//     setvar VAR_0x8005, ARAUNA_OW_CHANNEL_A
//     setvar VAR_0x8006, ARAUNA_OW_BOIUNA
//     special SetAraunaPokemonOverworld
void SetAraunaPokemonOverworld(void)
{
    u8 localId = gSpecialVar_0x8004;
    u16 channel = gSpecialVar_0x8005;
    u16 selection = gSpecialVar_0x8006;
    u8 objectEventId;

    if (channel >= ARAUNA_OW_CHANNELS || selection >= ARAUNA_OW_COUNT)
        return;

    VarSet(channel == ARAUNA_OW_CHANNEL_A ? VAR_ARAUNA_OW_A : VAR_ARAUNA_OW_B, selection);

    // Re-applying the dispatcher id makes the object re-read the registry.
    if (!TryGetObjectEventIdByLocalIdAndMap(localId, gSaveBlock1Ptr->location.mapNum,
                                            gSaveBlock1Ptr->location.mapGroup, &objectEventId))
    {
        ObjectEventSetGraphicsId(&gObjectEvents[objectEventId],
                                 channel == ARAUNA_OW_CHANNEL_A ? OBJ_EVENT_GFX_ARAUNA_POKEMON_A
                                                                : OBJ_EVENT_GFX_ARAUNA_POKEMON_B);
    }
}
"""

def edit_pointers(text: str) -> str:
    """Both dispatcher ids still need a table entry; nothing ever reads it."""
    for new, old in DISPATCHERS:
        text = re.sub(rf"^(\s*)\[{re.escape(old)}\](\s*)= &gObjectEventGraphicsInfo_\w+,$",
                      rf"\1[{new}]\2= &gObjectEventGraphicsInfo_NinjaBoy,", text, flags=re.M)
    # The retired id loses its entry along with its constant.
    text = re.sub(rf"^\s*\[{re.escape(RETIRED)}\]\s*=\s*&gObjectEventGraphicsInfo_\w+,\n", "",
                  text, flags=re.M)
    text = re.sub(r"^extern const struct ObjectEventGraphicsInfo "
                  r"gObjectEventGraphicsInfo_Arauna(Iemanja|Lobisomem|PretoVelho);\n", "",
                  text, flags=re.M)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    mons = species(list(csv.DictReader(SELECTION.open(encoding="utf-8"))))
    clashes = [c for c in {m["const"] for m in mons} if [x["const"] for x in mons].count(c) > 1]
    if clashes:
        print(f"selector names collide: {clashes}", file=sys.stderr)
        return 1
    print(f"registry: {len(mons)} creatures x 2 channels, "
          f"reachable from 2 graphics ids instead of {len(mons)}")
    if not args.check and not args.write:
        return 0
    if not args.write:
        return 0

    OW_CONSTANTS.write_text(render_constants(mons), encoding="utf-8")
    REGISTRY.write_text(render_registry(mons), encoding="utf-8")
    GRAPHICS.write_text(splice(GRAPHICS.read_text(encoding="utf-8"), render_graphics(mons),
                               GRAPHICS.read_text(encoding="utf-8").rstrip().splitlines()[-1]),
                        encoding="utf-8")
    PIC_TABLES.write_text(splice(PIC_TABLES.read_text(encoding="utf-8"), render_pic_tables(mons),
                                 PIC_TABLES.read_text(encoding="utf-8").rstrip().splitlines()[-1]),
                          encoding="utf-8")
    CONSTANTS.write_text(edit_event_objects(CONSTANTS.read_text(encoding="utf-8")), encoding="utf-8")
    VARS.write_text(edit_vars(VARS.read_text(encoding="utf-8")), encoding="utf-8")
    POINTERS.write_text(edit_pointers(POINTERS.read_text(encoding="utf-8")), encoding="utf-8")
    MOVEMENT.write_text(edit_movement(MOVEMENT.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"wrote {OW_CONSTANTS.relative_to(ROOT)}, {REGISTRY.relative_to(ROOT)} "
          f"and patched five engine files")
    return 0


if __name__ == "__main__":
    sys.exit(main())

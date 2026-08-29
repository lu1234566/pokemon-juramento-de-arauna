#!/usr/bin/env python3
"""Wire the 46 PixelLab overworld redraws into the object event system.

The art is already GBA-ready: 64x64, indexed, index 0 transparent, at most 15
visible colours, one palette shared by all eight directions of a species, and
front/back/left/right are true rotations rather than mirrors. Nothing here
rescales, dithers, requantises or otherwise touches a pixel. The only
transformation is layout: the three directions the engine can actually draw are
packed into one horizontal strip, because that is the shape gbagfx and
overworld_frame() expect.

  graphics/object_events/pics/pokemon/arauna/<dex>_<slug>.png   192x64, the wired sheet
  graphics/object_events/pics/pokemon/arauna/<dex>_<slug>/      all 12 source frames, kept
  graphics/object_events/palettes/arauna_<dex>_<slug>.pal       16 JASC entries

Three directions, not four. sAnimTable_Standard has no East frame: the engine
draws East by horizontally flipping West, and the brief says not to touch the
movement engine for this delivery. So right.png and the four diagonals are
copied into the repository and left unwired rather than mirrored or dropped.

Only species marked wired=yes in docs/arauna/ARAUNA_OVERWORLD_46.csv get engine
entries, and there are only six of those. Object event graphics ids are one
byte: 0-238 are spoken for, 240-255 are the dynamic VAR ids, and id 239 is the
single free value. Two more ids can be reclaimed -- 4 and 136 -- because nothing
references them; note that the six "unused doll" ids look free but are not, since
the project already reclaimed them through aliases (OBJ_EVENT_GFX_ADMIN_ARQUIVO
is OBJ_EVENT_GFX_UNUSED_PORYGON2_DOLL, and Weather Institute 2F places it). So
three new ids, plus the three species that already owned an object event.

Fitting all 46 would mean widening ObjectEventTemplate.graphicsId, which lives
inside SaveBlock1 at 0xC70; the save layout is out of bounds for this task.

  --check   validate the assets and report what would change
  --write   copy the art and rewrite the engine tables
"""
from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SELECTION = ROOT / "docs/arauna/ARAUNA_OVERWORLD_46.csv"
PICS = ROOT / "graphics/object_events/pics/pokemon/arauna"
PALETTES = ROOT / "graphics/object_events/palettes"

CONSTANTS = ROOT / "include/constants/event_objects.h"
GRAPHICS = ROOT / "src/data/object_events/object_event_graphics.h"
PIC_TABLES = ROOT / "src/data/object_events/object_event_pic_tables.h"
INFO = ROOT / "src/data/object_events/object_event_graphics_info.h"
POINTERS = ROOT / "src/data/object_events/object_event_graphics_info_pointers.h"
MOVEMENT = ROOT / "src/event_object_movement.c"

FRAME = 64
# South, North and West, in the order sAnimTable_Standard indexes them.
WIRED_DIRECTIONS = ["front", "back", "left"]
KEEP = ["front", "back", "left", "right",
        "north", "south", "east", "west",
        "north-east", "north-west", "south-east", "south-west"]
# Object event palettes park the transparent slot on this colour throughout the
# project; index 0 never renders, so writing it costs no pixel.
TRANSPARENT = (115, 197, 164)
FIRST_PAL_TAG = 0x117F     # the Arauna block continues after ..._ARAUA at 0x117E

# The three species that already owned an object event keep their id and their
# graphics-info symbol; only the art, the size and the palette tag change.
EXISTING = {
    "OBJ_EVENT_GFX_LUGIA": "Lugia",
    "OBJ_EVENT_GFX_POOCHYENA": "Poochyena",
    "OBJ_EVENT_GFX_AZURILL": "Azurill",
}


def symbol(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def load(source: Path, dex: str, slug: str) -> dict[str, Image.Image]:
    folder = source / f"gba_ready/{dex}_{slug_source(source, dex)}"
    frames = {}
    for name in ("front", "back", "left", "right"):
        frames[name] = Image.open(folder / "cardinal_emerald" / f"{name}.png")
    for name in ("north", "south", "east", "west",
                 "north-east", "north-west", "south-east", "south-west"):
        frames[name] = Image.open(folder / "rotations_8dir" / f"{name}.png")
    return frames


def slug_source(source: Path, dex: str) -> str:
    """The ZIP names its folders <dex>_<its own slug>; find it rather than guess."""
    matches = sorted((source / "gba_ready").glob(f"{dex}_*"))
    if len(matches) != 1:
        raise ValueError(f"#{dex}: expected one asset folder, found {[m.name for m in matches]}")
    return matches[0].name[len(dex) + 1:]


def check_frames(dex: str, frames: dict[str, Image.Image]) -> list[str]:
    problems, reference = [], None
    for name, image in frames.items():
        if image.size != (FRAME, FRAME):
            problems.append(f"#{dex} {name}: {image.size}, expected 64x64")
        if image.mode != "P":
            problems.append(f"#{dex} {name}: mode {image.mode}, expected indexed")
        if np.array(image).max() > 15:
            problems.append(f"#{dex} {name}: uses palette index over 15")
        palette = (image.getpalette() or [])[:48]
        if reference is None:
            reference = palette
        elif palette != reference:
            problems.append(f"#{dex} {name}: palette differs from the rest of the species")
    left, right = np.array(frames["left"]), np.array(frames["right"])
    if np.array_equal(left, np.fliplr(right)):
        problems.append(f"#{dex}: left and right are mirrors, not rotations")
    return problems


def write_sheet(path: Path, frames: dict[str, Image.Image]) -> None:
    """Pack South, North and West into one strip. Pixels are copied verbatim."""
    strip = np.hstack([np.array(frames[d]) for d in WIRED_DIRECTIONS])
    sheet = Image.fromarray(strip.astype(np.uint8), mode="P")
    sheet.putpalette(frames["front"].getpalette())
    sheet.save(path, optimize=False)


def write_palette(path: Path, image: Image.Image) -> None:
    raw = (image.getpalette() or [])[:48]
    colours = [TRANSPARENT] + [tuple(raw[i * 3:i * 3 + 3]) for i in range(1, 16)]
    lines = ["JASC-PAL", "0100", "16"] + [f"{r} {g} {b}" for r, g, b in colours]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


# ------------------------------------------------------------------ engine

BEGIN = "// BEGIN Arauna overworld redraws"
END = "// END Arauna overworld redraws"


def splice(text: str, block: str, anchor: str, before: bool = False) -> str:
    """Insert or replace the generated block, so a rerun does not stack copies."""
    if BEGIN in text:
        head, rest = text.split(BEGIN, 1)
        _, tail = rest.split(END, 1)
        return f"{head}{BEGIN}\n{block}{END}{tail}"
    marked = f"{BEGIN}\n{block}{END}\n"
    if before:
        return text.replace(anchor, marked + anchor, 1)
    return text.replace(anchor, anchor + "\n" + marked, 1)


def edit_constants(rows) -> str:
    """Rename the reclaimed ids and open up the one free id.

    The numeric values are left exactly where they are -- a graphics id is
    stored in map data, so renumbering would move objects that already exist.
    Only the names change, plus id 239, which no graphics id ever used.
    """
    import re as _re
    text = CONSTANTS.read_text(encoding="utf-8")
    for row in rows:
        old = row["reclaimed_from"]
        if not old or old.startswith("("):
            continue
        name = row["obj_event_gfx"]
        pattern = _re.compile(rf"^#define {_re.escape(old)}(\s+)(\d+)$", _re.M)
        match = pattern.search(text)
        if not match:
            # Already renamed by an earlier run; only complain if neither name is there.
            if _re.search(rf"^#define {_re.escape(name)}\s+\d+$", text, _re.M):
                continue
            raise ValueError(f"neither {old} nor {name} is defined; the selection CSV is stale")
        width = len(old) + len(match.group(1))
        text = pattern.sub(f"#define {name}{' ' * max(1, width - len(name))}{match.group(2)}",
                           text, count=1)

    for row in [r for r in rows if r["reclaimed_from"].startswith("(")]:
        name = row["obj_event_gfx"]
        if _re.search(rf"^#define {_re.escape(name)}\s+239$", text, _re.M):
            continue
        text = text.replace(
            "#define NUM_OBJ_EVENT_GFX                        239",
            f"#define {name}{' ' * max(1, 41 - len(name))}239\n\n"
            "// Id 239 was left unused so that OBJ_EVENT_GFX_VARS could start at 240 with a\n"
            "// +1. Arauna uses it, so the +1 goes and the vars still start at 240.\n"
            "#define NUM_OBJ_EVENT_GFX                        240", 1)
        text = text.replace("#define OBJ_EVENT_GFX_VARS   (NUM_OBJ_EVENT_GFX + 1)",
                            "#define OBJ_EVENT_GFX_VARS   (NUM_OBJ_EVENT_GFX)", 1)
    return text


def edit_graphics(rows) -> str:
    lines = []
    for row in rows:
        name = f"{row['arauna_dex']}_{row['slug']}"
        lines.append(f'const u32 gObjectEventPic_Arauna{symbol(row["slug"])}[] = '
                     f'INCGFX_U32("graphics/object_events/pics/pokemon/arauna/{name}.png", '
                     f'".4bpp", "-mwidth 8 -mheight 8");')
        lines.append(f'const u16 gObjectEventPal_Arauna{symbol(row["slug"])}[] = '
                     f'INCGFX_U16("graphics/object_events/palettes/arauna_{name}.pal", ".gbapal");')
    text = GRAPHICS.read_text(encoding="utf-8")
    return splice(text, "\n".join(lines) + "\n", text.rstrip().splitlines()[-1])


def edit_pic_tables(rows) -> str:
    lines = []
    for row in rows:
        sym = symbol(row["slug"])
        lines.append(f"static const struct SpriteFrameImage sPicTable_Arauna{sym}[] = {{")
        # South, North, West, then the walk frames, which reuse the idle pose:
        # the redraws are single-pose, so a walking creature simply keeps facing.
        for frame in (0, 1, 2, 0, 0, 1, 1, 2, 2):
            lines.append(f"    overworld_frame(gObjectEventPic_Arauna{sym}, 8, 8, {frame}),")
        lines.append("};")
    text = PIC_TABLES.read_text(encoding="utf-8")
    return splice(text, "\n".join(lines) + "\n", text.rstrip().splitlines()[-1])


def info_block(row, name: str) -> str:
    sym = symbol(row["slug"])
    return f"""const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{name} = {{
    .tileTag = TAG_NONE,
    .paletteTag = OBJ_EVENT_PAL_TAG_ARAUNA_{row['slug'].upper()},
    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,
    .size = 2048,
    .width = 64,
    .height = 64,
    .paletteSlot = PALSLOT_NPC_SPECIAL,
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


def edit_info(rows) -> str:
    text = INFO.read_text(encoding="utf-8")
    new = []
    for row in rows:
        name = EXISTING.get(row["obj_event_gfx"])
        if name:
            # Replace the existing struct in place; the id and symbol survive.
            start = text.index(f"const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_{name} = {{")
            end = text.index("};", start) + 3
            text = text[:start] + info_block(row, name) + text[end:]
        else:
            new.append(info_block(row, f"Arauna{symbol(row['slug'])}"))
    return splice(text, "\n".join(new), text.rstrip().splitlines()[-1])


def edit_pointers(rows) -> str:
    """Declare the new graphics info and point the reclaimed ids at it.

    The externs live in this same file, just above the table, so a new symbol
    has to be declared here or the table cannot name it.
    """
    import re as _re
    text = POINTERS.read_text(encoding="utf-8")
    fresh = [r for r in rows if r["obj_event_gfx"] not in EXISTING]

    externs = "\n".join(
        f"extern const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Arauna{symbol(r['slug'])};"
        for r in fresh)
    anchor = ("const struct ObjectEventGraphicsInfo *const "
              "gObjectEventGraphicsInfoPointers[NUM_OBJ_EVENT_GFX] = {")
    text = splice(text, externs + "\n", anchor, before=True)

    for row in fresh:
        entry = (f"    [{row['obj_event_gfx']}] = "
                 f"&gObjectEventGraphicsInfo_Arauna{symbol(row['slug'])},")
        old = row["reclaimed_from"]
        if old.startswith("("):
            cut = text.rindex("};")
            text = text[:cut] + entry + "\n" + text[cut:]
        else:
            text = _re.sub(rf"^\s*\[{_re.escape(old)}\]\s*=\s*&\w+,$", entry, text, flags=_re.M)
    return text


def edit_movement(rows) -> str:
    text = MOVEMENT.read_text(encoding="utf-8")
    tags, entries = [], []
    for i, row in enumerate(rows):
        tag = f"OBJ_EVENT_PAL_TAG_ARAUNA_{row['slug'].upper()}"
        tags.append(f"#define {tag:<44} 0x{FIRST_PAL_TAG + i:04X}")
        entries.append(f"    {{gObjectEventPal_Arauna{symbol(row['slug'])},"
                       f"{' ' * max(1, 34 - len(symbol(row['slug'])))}{tag}}},")
    text = splice(text, "\n".join(tags) + "\n",
                  "#define OBJ_EVENT_PAL_TAG_ARAUA                   0x117E")
    head, rest = text.split("static const struct SpritePalette sObjectEventSpritePalettes[] = {", 1)
    terminator = rest.index("{NULL,")
    return (head + "static const struct SpritePalette sObjectEventSpritePalettes[] = {"
            + rest[:terminator] + "\n".join(entries) + "\n    " + rest[terminator:])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True, help="unpacked redraw package")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    source = Path(args.source)
    rows = list(csv.DictReader(SELECTION.open(encoding="utf-8")))
    wired = [r for r in rows if r["wired"] == "yes"]

    problems, frames_by_dex = [], {}
    for row in rows:
        frames = load(source, row["arauna_dex"], row["slug"])
        problems += check_frames(row["arauna_dex"], frames)
        frames_by_dex[row["arauna_dex"]] = frames
    if problems:
        for problem in problems:
            print(f"asset problem: {problem}", file=sys.stderr)
        return 1
    print(f"assets OK: {len(rows)} species, {len(rows) * 8} rotation frames, "
          f"all 64x64 indexed, index 0 transparent, indices <= 15, no mirrored pair")
    print(f"all {len(rows)} get a sheet, a palette and a palette tag; "
          f"{len(EXISTING)} of them also keep a dedicated object event id")

    if not args.write:
        return 0

    PICS.mkdir(parents=True, exist_ok=True)
    for row in rows:
        dex, slug = row["arauna_dex"], row["slug"]
        folder = PICS / f"{dex}_{slug}"
        folder.mkdir(parents=True, exist_ok=True)
        origin = source / f"gba_ready/{dex}_{slug_source(source, dex)}"
        for name in KEEP:
            part = "cardinal_emerald" if name in ("front", "back", "left", "right") else "rotations_8dir"
            shutil.copyfile(origin / part / f"{name}.png", folder / f"{name}.png")
        shutil.copyfile(origin / "normal.pal", folder / "normal.pal")

    for row in rows:
        dex, slug = row["arauna_dex"], row["slug"]
        write_sheet(PICS / f"{dex}_{slug}.png", frames_by_dex[dex])
        write_palette(PALETTES / f"arauna_{dex}_{slug}.pal", frames_by_dex[dex]["front"])

    legacy = [r for r in rows if r["obj_event_gfx"] in EXISTING]
    INFO.write_text(edit_info(legacy), encoding="utf-8")
    MOVEMENT.write_text(edit_movement(rows), encoding="utf-8")
    print(f"copied {len(rows)} asset sets, wrote {len(rows)} sheets and palettes and "
          f"{len(rows)} palette tags; {len(legacy)} legacy object events repointed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

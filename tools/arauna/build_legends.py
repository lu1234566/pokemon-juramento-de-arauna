#!/usr/bin/env python3
"""Give the twenty held-back legendaries and mythicals a place in the world.

docs/arauna/ESPECIAIS_ESTATICOS.csv kept twenty specials out of the random
tables, waiting for a static encounter that did not exist. This builds those
encounters from docs/arauna/ARAUNA_LEGENDS.csv, one row per creature: where it
stands, its level, which dispatcher channel draws it and the line the player
reads before the cry.

They wake after the first Hall of Fame. Before that every one of them is
asleep (its flag set, its object hidden), which keeps levels 58-68 out of the
main campaign. Each later Hall of Fame wakes again any that was knocked out
rather than caught, so no species can be lost for good.

The overworld art is the creature's own battle front sprite, standing still
at 64x64 like the Emerald legendaries: no new drawing, the same picture the
battle shows. Dedicated art can replace a sheet later under the same name.

Generated or patched:

  graphics/object_events/pics/pokemon/arauna/<dex>_<slug>.png   64x64 sheet
  graphics/object_events/palettes/arauna_<dex>_<slug>.pal       its palette
  docs/arauna/ARAUNA_OVERWORLD_46.csv      a registry row each (ow_size 64s)
  src/event_object_movement.c              palette tags and palette table
  include/constants/flags.h                FLAG_ARAUNA_LEGEND_*
  data/maps/<map>/map.json                 one object event each, appended
  src/data/arauna_legends.h                the table src/arauna_legends.c reads
  data/scripts/arauna_legends.inc          the encounter scripts and texts

Run tools/arauna/build_overworld_registry.py --write afterwards: it turns the
registry rows into graphics infos and pic tables.

  --write   write everything (without it, report what would be placed)
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import struct
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LEGENDS = ROOT / "docs/arauna/ARAUNA_LEGENDS.csv"
REGISTRY_CSV = ROOT / "docs/arauna/ARAUNA_OVERWORLD_46.csv"
MAPPING = ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
PICS = ROOT / "graphics/object_events/pics/pokemon/arauna"
PALETTES = ROOT / "graphics/object_events/palettes"
MOVEMENT = ROOT / "src/event_object_movement.c"
FLAGS = ROOT / "include/constants/flags.h"
TABLE = ROOT / "src/data/arauna_legends.h"
SCRIPTS = ROOT / "data/scripts/arauna_legends.inc"

# Twenty story flags vanilla never set, 0x020-0x033.
FIRST_FLAG = 0x20
# Object palette tags 0x11D6-0x11FE are free; 0x11D6-0x11DF stay open for the
# character packages, which number their tags from the bottom of the gap.
FIRST_PAL_TAG = 0x11E0

BEGIN_TAGS = "// BEGIN Arauna legend overworlds"
END_TAGS = "// END Arauna legend overworlds"
BEGIN_FLAGS = "// BEGIN ARAUNA LEGENDS"
END_FLAGS = "// END ARAUNA LEGENDS"


def constant(slug: str) -> str:
    return slug.upper()


def symbol(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def engine_slots() -> dict[int, tuple[str, str]]:
    """Arauna dex number -> (engine species, graphics folder)."""
    return {int(row["arauna_dex"]): (row["species_constant"], row["graphics_folder"])
            for row in csv.DictReader(MAPPING.open(encoding="utf-8"))}


def rows() -> list[dict]:
    slots = engine_slots()
    out = []
    for i, row in enumerate(csv.DictReader(LEGENDS.open(encoding="utf-8"))):
        dex = int(row["dex"])
        out.append(dict(row, dex=dex, species=slots[dex][0], folder=slots[dex][1],
                        level=int(row["level"]),
                        x=int(row["x"]), y=int(row["y"]), const=constant(row["slug"]),
                        sym=symbol(row["slug"]), flag=f"FLAG_ARAUNA_LEGEND_{constant(row['slug'])}",
                        flag_value=FIRST_FLAG + i, pal_tag=FIRST_PAL_TAG + i,
                        local_id=f"LOCALID_ARAUNA_LEGEND_{constant(row['slug'])}",
                        script=f"AraunaLegends_EventScript_{symbol(row['slug'])}",
                        file=f"{dex:03d}_{row['slug']}"))
    return out


# --- art -------------------------------------------------------------------

def overworld_sheet(graphics_folder: str) -> tuple[Image.Image, str]:
    """The front sprite, moved so the creature stands on the bottom of its tile."""
    folder = ROOT / "graphics/pokemon" / graphics_folder
    front = Image.open(folder / "front.png")
    if front.mode != "P" or front.size[0] != 64:
        raise SystemExit(f"{folder}/front.png is not a 64-wide indexed sprite")
    frame = front.crop((0, 0, 64, 64))
    mask = frame.point(lambda index: 255 if index else 0)
    left, top, right, bottom = mask.getbbox()
    sheet = Image.new("P", (64, 64), 0)
    sheet.putpalette(front.getpalette())
    # Centred across, resting one pixel above the bottom edge.
    dx = (64 - (right - left)) // 2 - left
    dy = 63 - bottom
    sheet.paste(frame, (dx, dy))
    # The paste copies index 0 too; it is the transparent colour either way.
    return sheet, (folder / "normal.pal").read_text(encoding="utf-8")


# --- engine text patches -----------------------------------------------------

def splice(text: str, begin: str, end: str, block: str, anchor: str, after: bool = True) -> str:
    if begin in text:
        head, rest = text.split(begin, 1)
        _, tail = rest.split(end, 1)
        return f"{head}{begin}\n{block}{end}{tail}"
    marked = f"{begin}\n{block}{end}\n"
    if anchor not in text:
        raise SystemExit(f"anchor not found: {anchor!r}")
    return text.replace(anchor, (anchor + "\n" + marked.rstrip("\n")) if after else (marked + anchor), 1)


def patch_movement(legends) -> str:
    text = MOVEMENT.read_text(encoding="utf-8")
    tags = "".join(f"#define OBJ_EVENT_PAL_TAG_ARAUNA_{m['const']:<32} 0x{m['pal_tag']:04X}\n"
                   for m in legends)
    text = splice(text, BEGIN_TAGS, END_TAGS, tags,
                  "#define OBJ_EVENT_PAL_TAG_DONA_ZILA                 0x11D5")
    entries = "".join(f"    {{gObjectEventPal_Arauna{m['sym']},{' ' * max(1, 28 - len(m['sym']))}"
                      f"OBJ_EVENT_PAL_TAG_ARAUNA_{m['const']}}},\n" for m in legends)
    start = text.index("static const struct SpritePalette sObjectEventSpritePalettes[] = {")
    body_end = text.index("\n};", start)
    body = text[start:body_end]
    marker = f"    {BEGIN_TAGS}\n"
    if marker in body:
        head, rest = body.split(marker, 1)
        _, tail = rest.split(f"    {END_TAGS}\n", 1)
        body = f"{head}{marker}{entries}    {END_TAGS}\n{tail}"
    else:
        terminator = body.index("    // Unconditional terminator.")
        body = body[:terminator] + marker + entries + f"    {END_TAGS}\n" + body[terminator:]
    return text[:start] + body + text[body_end:]


def patch_flags(legends) -> str:
    text = FLAGS.read_text(encoding="utf-8")
    block = ("// The twenty specials of docs/arauna/ARAUNA_LEGENDS.csv. Set means the\n"
             "// creature is not standing in the world: asleep before the first Hall of\n"
             "// Fame, caught, or knocked out until the next one (see arauna_legends.c).\n")
    block += "".join(f"#define {m['flag']:<40} FLAG_UNUSED_0x{m['flag_value']:03X}\n" for m in legends)
    return splice(text, BEGIN_FLAGS, END_FLAGS, block,
                  "#endif // GUARD_CONSTANTS_FLAGS_H", after=False)


def patch_registry_csv(legends) -> bytes:
    # The manifest is CRLF; keep whatever line ending it already uses.
    raw = REGISTRY_CSV.read_bytes()
    eol = b"\r\n" if b"\r\n" in raw else b"\n"
    have = {line.split(b",")[3].decode() for line in raw.splitlines()[1:] if line}
    for m in legends:
        if m["slug"] not in have:
            raw += (f"{m['dex']:03d},{m['name']},{m['species']},{m['slug']},64s,no,,,"
                    "legend; battle front sprite standing still").encode("utf-8") + eol
    return raw


# --- maps ------------------------------------------------------------------

def tile_elevation(name: str, x: int, y: int) -> int:
    blob = json.loads((ROOT / "data/maps" / name / "map.json").read_text(encoding="utf-8"))
    layouts = {l["id"]: l for l in json.loads(
        (ROOT / "data/layouts/layouts.json").read_text(encoding="utf-8"))["layouts"] if l}
    layout = layouts[blob["layout"]]
    raw = (ROOT / layout["blockdata_filepath"]).read_bytes()
    value = struct.unpack_from("<H", raw, 2 * (y * layout["width"] + x))[0]
    return value >> 12


def object_json(m) -> str:
    obj = {
        "local_id": m["local_id"],
        "graphics_id": f"OBJ_EVENT_GFX_ARAUNA_POKEMON_{m['channel']}",
        "x": m["x"],
        "y": m["y"],
        "elevation": tile_elevation(m["map"], m["x"], m["y"]),
        "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
        "movement_range_x": 0,
        "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0",
        "script": m["script"],
        "flag": m["flag"],
    }
    body = json.dumps(obj, indent=2, ensure_ascii=False)
    return "\n".join("    " + line for line in body.splitlines())


def array_end(text: str, key: str) -> int:
    """Index of the ']' that closes text's top-level array named key."""
    start = text.index(f'"{key}": [') + len(f'"{key}": [')
    depth, in_string, escape = 1, False, False
    for i in range(start, len(text)):
        c = text[i]
        if in_string:
            escape = (c == "\\") and not escape
            if c == '"' and not escape:
                in_string = False
            continue
        if c == '"':
            in_string = True
        elif c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0:
                return i
    raise SystemExit(f"unterminated {key}")


def patch_map(name: str, legends) -> str:
    path = ROOT / "data/maps" / name / "map.json"
    text = path.read_text(encoding="utf-8")
    for m in legends:
        if f'"{m["local_id"]}"' in text:
            continue
        end = array_end(text, "object_events")
        head = text[:end].rstrip()
        sep = "" if head.endswith("[") else ","
        text = f"{head}{sep}\n{object_json(m)}\n  " + text[end:]
    json.loads(text)
    return text


# --- C table and scripts ----------------------------------------------------

def render_table(legends) -> str:
    lines = [
        "// Generated by tools/arauna/build_legends.py from docs/arauna/ARAUNA_LEGENDS.csv.",
        "// Do not edit.",
        "",
        "static const struct AraunaLegend sAraunaLegends[] =",
        "{",
    ]
    for m in legends:
        map_id = json.loads((ROOT / "data/maps" / m["map"] / "map.json")
                            .read_text(encoding="utf-8"))["id"]
        lines.append(f"    {{ {m['species']}, {m['flag']}, MAP_GROUP({map_id}), MAP_NUM({map_id}), "
                     f"{m['local_id']}, ARAUNA_OW_CHANNEL_{m['channel']}, ARAUNA_OW_{m['const']} }},"
                     f"  // #{m['dex']} {m['name']}")
    lines += ["};", ""]
    return "\n".join(lines)


def inc_string(text: str) -> str:
    parts = re.split(r"(\\n|\\p)", text)
    out, line = [], ""
    for part in parts:
        line += part
        if part in ("\\n", "\\p"):
            out.append(line)
            line = ""
    out.append(line + "$")
    return "".join(f'\t.string "{p}"\n' for p in out)


def render_scripts(legends) -> str:
    out = [
        "@ Generated by tools/arauna/build_legends.py from docs/arauna/ARAUNA_LEGENDS.csv.",
        "@ Do not edit.",
        "",
    ]
    for m in legends:
        out += [
            f"{m['script']}::",
            "\tlock",
            f"\tmsgbox AraunaLegends_Text_{m['sym']}, MSGBOX_DEFAULT",
            "\tclosemessage",
            "\twaitse",
            f"\tplaymoncry {m['species']}, CRY_MODE_ENCOUNTER",
            "\tdelay 40",
            "\twaitmoncry",
            f"\tsetwildbattle {m['species']}, {m['level']}",
            "\tcall AraunaLegends_EventScript_Battle",
            "\tgoto_if_eq VAR_RESULT, FALSE, AraunaLegends_EventScript_Remains",
            f"\tsetflag {m['flag']}",
            "\tgoto AraunaLegends_EventScript_Settled",
            "",
        ]
    out += [
        "@ The battle every legend shares. VAR_RESULT comes back TRUE when the",
        "@ creature leaves the world (caught or knocked out), FALSE when it stays.",
        "@ VAR_0x8004 keeps the outcome for AraunaLegends_EventScript_Settled.",
        "AraunaLegends_EventScript_Battle::",
        "\tsetflag FLAG_SYS_CTRL_OBJ_DELETE",
        "\tspecial StartRegiBattle",
        "\tclearflag FLAG_SYS_CTRL_OBJ_DELETE",
        "\tspecialvar VAR_0x8004, GetBattleOutcome",
        "\tsetvar VAR_RESULT, TRUE",
        "\tgoto_if_eq VAR_0x8004, B_OUTCOME_CAUGHT, AraunaLegends_EventScript_BattleDone",
        "\tgoto_if_eq VAR_0x8004, B_OUTCOME_WON, AraunaLegends_EventScript_BattleDone",
        "\tsetvar VAR_RESULT, FALSE",
        "AraunaLegends_EventScript_BattleDone::",
        "\treturn",
        "",
        "@ Caught: AraunaLegends_OnResume already took the object away before the",
        "@ screen faded back in. Knocked out: it fades now, and wakes again after",
        "@ the next Hall of Fame.",
        "AraunaLegends_EventScript_Settled::",
        "\tgoto_if_eq VAR_0x8004, B_OUTCOME_CAUGHT, AraunaLegends_EventScript_Remains",
        "\tfadescreenswapbuffers FADE_TO_BLACK",
        "\tremoveobject VAR_LAST_TALKED",
        "\tfadescreenswapbuffers FADE_FROM_BLACK",
        "\tmsgbox AraunaLegends_Text_FadedAway, MSGBOX_DEFAULT",
        "AraunaLegends_EventScript_Remains::",
        "\trelease",
        "\tend",
        "",
        "AraunaLegends_Text_FadedAway::",
        inc_string("The presence faded away.\\pPerhaps it will return after\\n"
                   "another victory at the LEAGUE.").rstrip("\n"),
        "",
    ]
    for m in legends:
        out += [f"AraunaLegends_Text_{m['sym']}::", inc_string(m["text"]).rstrip("\n"), ""]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    legends = rows()
    maps = sorted({m["map"] for m in legends})
    for name in maps:
        channels = [m["channel"] for m in legends if m["map"] == name]
        if len(channels) != len(set(channels)):
            raise SystemExit(f"{name}: two legends on one dispatcher channel")
    for m in legends:
        print(f"#{m['dex']} {m['name']:<11} Lv{m['level']}  {m['map']} ({m['x']},{m['y']}) "
              f"channel {m['channel']}  {m['species']}")
    if not args.write:
        return 0

    PICS.mkdir(parents=True, exist_ok=True)
    for m in legends:
        sheet, pal = overworld_sheet(m["folder"])
        sheet.save(PICS / f"{m['file']}.png")
        (PALETTES / f"arauna_{m['file']}.pal").write_text(pal, encoding="utf-8")
    REGISTRY_CSV.write_bytes(patch_registry_csv(legends))
    MOVEMENT.write_text(patch_movement(legends), encoding="utf-8")
    FLAGS.write_text(patch_flags(legends), encoding="utf-8")
    for name in maps:
        path = ROOT / "data/maps" / name / "map.json"
        path.write_text(patch_map(name, [m for m in legends if m["map"] == name]), encoding="utf-8")
    TABLE.write_text(render_table(legends), encoding="utf-8")
    SCRIPTS.write_text(render_scripts(legends), encoding="utf-8")
    print(f"wrote {len(legends)} legends on {len(maps)} maps; "
          "now run tools/arauna/build_overworld_registry.py --write")
    return 0


if __name__ == "__main__":
    sys.exit(main())

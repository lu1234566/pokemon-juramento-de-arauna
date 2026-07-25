#!/usr/bin/env python3
"""Integrate the approved Arauna priority-10 NPC v3 pack.

This script is intentionally idempotent. It keeps the supplied character pixel
geometry, adapts overworld colours to the closest shared Emerald NPC palette so
multiple story characters can coexist on one map, adds dedicated overworld
graphics IDs, and installs the six supplied portraits in campaign-unused
Frontier Brain picture slots without expanding the trainer-picture table.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class NpcAsset:
    key: str
    enum_name: str
    symbol: str
    overworld_file: str
    map_path: str
    map_script: str
    trainer_file: str | None = None
    trainer_enum: str | None = None
    trainer_symbol: str | None = None


ASSETS: tuple[NpcAsset, ...] = (
    NpcAsset(
        "dona_zila",
        "OBJ_EVENT_GFX_ARAUNA_DONA_ZILA",
        "AraunaDonaZila",
        "01_dona_zila_12frames_48x128.png",
        "data/maps/AraunaPlayerHouse/map.json",
        "AraunaPlayerHouse_EventScript_DonaZila",
    ),
    NpcAsset(
        "professora_anahi",
        "OBJ_EVENT_GFX_ARAUNA_PROFESSORA_ANAHI",
        "AraunaProfessoraAnahi",
        "02_professora_anahi_12frames_48x128.png",
        "data/maps/AraunaPlayerHouse/map.json",
        "AraunaPlayerHouse_EventScript_Anahi",
        "02_professora_anahi_trainer_64x64.png",
        "TRAINER_PIC_ARAUNA_ANAHI",
        "AraunaAnahi",
    ),
    NpcAsset(
        "ciro_prologo",
        "OBJ_EVENT_GFX_ARAUNA_CIRO_PROLOGUE",
        "AraunaCiroPrologue",
        "03_ciro_prologo_12frames_48x128.png",
        "data/maps/AraunaMapLab/map.json",
        "AraunaMapLab_EventScript_Ciro",
        "03_ciro_prologo_trainer_64x64.png",
        "TRAINER_PIC_ARAUNA_CIRO_PROLOGUE",
        "AraunaCiroPrologue",
    ),
    NpcAsset(
        "ciro_consorcio",
        "OBJ_EVENT_GFX_ARAUNA_CIRO_CONSORCIO",
        "AraunaCiroConsorcio",
        "04_ciro_consorcio_12frames_48x128.png",
        "data/maps/SlateportCity/map.json",
        "AraunaPorto_EventScript_CiroPorto",
        "04_ciro_consorcio_trainer_64x64.png",
        "TRAINER_PIC_ARAUNA_CIRO_CONSORCIO",
        "AraunaCiroConsorcio",
    ),
    NpcAsset(
        "dona_celina",
        "OBJ_EVENT_GFX_ARAUNA_DONA_CELINA",
        "AraunaDonaCelina",
        "06_dona_celina_12frames_48x128.png",
        "data/maps/SlateportCity/map.json",
        "AraunaPorto_EventScript_DonaCelina",
        "06_dona_celina_trainer_64x64.png",
        "TRAINER_PIC_ARAUNA_DONA_CELINA",
        "AraunaDonaCelina",
    ),
    NpcAsset(
        "agente_conformidade",
        "OBJ_EVENT_GFX_ARAUNA_COMPLIANCE_AGENT",
        "AraunaComplianceAgent",
        "07_agente_conformidade_12frames_48x128.png",
        "data/maps/SlateportCity/map.json",
        "AraunaPorto_EventScript_ConsortiumAgent",
        "07_agente_conformidade_trainer_64x64.png",
        "TRAINER_PIC_ARAUNA_COMPLIANCE_AGENT",
        "AraunaComplianceAgent",
    ),
    NpcAsset(
        "trabalhador_cais",
        "OBJ_EVENT_GFX_ARAUNA_DOCKWORKER",
        "AraunaDockworker",
        "08_trabalhador_cais_12frames_48x128.png",
        "data/maps/SlateportCity/map.json",
        "AraunaPorto_EventScript_Dockworker",
    ),
    NpcAsset(
        "pescador_memorial",
        "OBJ_EVENT_GFX_ARAUNA_MEMORIAL_FISHER",
        "AraunaMemorialFisher",
        "09_pescador_memorial_12frames_48x128.png",
        "data/maps/SlateportCity/map.json",
        "AraunaPorto_EventScript_MemorialKeeper",
    ),
    NpcAsset(
        "crianca_serra",
        "OBJ_EVENT_GFX_ARAUNA_SERRA_CHILD",
        "AraunaSerraChild",
        "10_crianca_serra_12frames_48x128.png",
        "data/maps/FallarborTown/map.json",
        "AraunaSerra_EventScript_LibrasChild",
    ),
    # eremita_surdo excluded: design rejected in ADR-024 visual review, pending regeneration.
)

TRAINER_ASSETS = tuple(asset for asset in ASSETS if asset.trainer_file is not None)


def fail(message: str) -> None:
    raise RuntimeError(message)


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str | Path, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def replace_once(source: str, old: str, new: str, context: str) -> str:
    count = source.count(old)
    if count != 1:
        fail(f"{context}: expected one occurrence of {old!r}, found {count}")
    return source.replace(old, new, 1)


def insert_before_once(source: str, marker: str, payload: str, context: str) -> str:
    if payload.strip() in source:
        return source
    return replace_once(source, marker, payload + marker, context)


def add_object_event_ids() -> None:
    path = Path("include/constants/event_objects.h")
    source = read(path)
    missing = [asset.enum_name for asset in ASSETS if asset.enum_name not in source]
    if not missing:
        return
    payload = "".join(f"    {name},\n" for name in missing)
    source = insert_before_once(source, "    NUM_OBJ_EVENT_GFX,", payload, "object event IDs")
    write(path, source)


def add_object_event_graphics(shared_slots: dict[str, int]) -> None:
    graphics_path = Path("src/data/object_events/object_event_graphics.h")
    graphics = read(graphics_path)
    declarations = []
    for asset in ASSETS:
        symbol = f"gObjectEventPic_{asset.symbol}"
        if symbol not in graphics:
            declarations.append(
                f'const u32 {symbol}[] = INCGFX_U32('
                f'"graphics/object_events/pics/people/arauna/{asset.key}.png", '
                f'".4bpp", "-mwidth 2 -mheight 4");\n'
            )
    if declarations:
        graphics = graphics.rstrip() + "\n\n// Arauna priority-10 NPC pack v3.\n" + "".join(declarations)
        write(graphics_path, graphics)

    tables_path = Path("src/data/object_events/object_event_pic_tables.h")
    tables = read(tables_path)
    blocks = []
    for asset in ASSETS:
        table = f"sPicTable_{asset.symbol}"
        if table not in tables:
            blocks.append(
                f"static const struct SpriteFrameImage {table}[] =\n"
                "{\n"
                f"    overworld_ascending_frames(gObjectEventPic_{asset.symbol}, 2, 4),\n"
                "};\n\n"
            )
    if blocks:
        tables = tables.rstrip() + "\n\n// Arauna priority-10 NPC pack v3.\n" + "".join(blocks)
        write(tables_path, tables)

    info_path = Path("src/data/object_events/object_event_graphics_info.h")
    info = read(info_path)
    blocks = []
    for asset in ASSETS:
        name = f"gObjectEventGraphicsInfo_{asset.symbol}"
        if name in info:
            continue
        slot = shared_slots[asset.key]
        blocks.append(
            f"const struct ObjectEventGraphicsInfo {name} = {{\n"
            "    .tileTag = TAG_NONE,\n"
            f"    .paletteTag = OBJ_EVENT_PAL_TAG_NPC_{slot},\n"
            "    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,\n"
            "    .size = 256,\n"
            "    .width = 16,\n"
            "    .height = 32,\n"
            f"    .paletteSlot = PALSLOT_NPC_{slot},\n"
            "    .shadowSize = SHADOW_SIZE_M,\n"
            "    .inanimate = FALSE,\n"
            "    .compressed = FALSE,\n"
            "    .tracks = TRACKS_FOOT,\n"
            "    .oam = &gObjectEventBaseOam_16x32,\n"
            "    .subspriteTables = sOamTables_16x32,\n"
            "    .anims = sAnimTable_Standard,\n"
            f"    .images = sPicTable_{asset.symbol},\n"
            "};\n\n"
        )
    if blocks:
        info = info.rstrip() + "\n\n// Arauna priority-10 NPC pack v3.\n" + "".join(blocks)
        write(info_path, info)

    pointers_path = Path("src/data/object_events/object_event_graphics_info_pointers.h")
    pointers = read(pointers_path)
    table_marker = "const struct ObjectEventGraphicsInfo *const gObjectEventGraphicsInfoPointers"
    table_start = pointers.find(table_marker)
    if table_start < 0:
        fail("cannot locate gObjectEventGraphicsInfoPointers")
    externs = []
    for asset in ASSETS:
        name = f"gObjectEventGraphicsInfo_{asset.symbol}"
        extern = f"extern const struct ObjectEventGraphicsInfo {name};\n"
        if extern not in pointers:
            externs.append(extern)
    if externs:
        pointers = pointers[:table_start] + "// Arauna priority-10 NPC pack v3.\n" + "".join(externs) + "\n" + pointers[table_start:]
        table_start = pointers.find(table_marker)
    brace_start = pointers.find("{", table_start)
    brace_end = pointers.find("\n};", brace_start)
    if brace_start < 0 or brace_end < 0:
        fail("cannot locate object graphics pointer table braces")
    entries = []
    for asset in ASSETS:
        entry = f"    [{asset.enum_name}] = &gObjectEventGraphicsInfo_{asset.symbol},\n"
        if entry not in pointers:
            entries.append(entry)
    if entries:
        pointers = pointers[:brace_end] + "\n    // Arauna priority-10 NPC pack v3.\n" + "".join(entries) + pointers[brace_end:]
    write(pointers_path, pointers)


def update_map_graphics() -> None:
    grouped: dict[str, list[NpcAsset]] = {}
    for asset in ASSETS:
        grouped.setdefault(asset.map_path, []).append(asset)
    for map_path, assets in grouped.items():
        data = json.loads(read(map_path))
        for asset in assets:
            matches = [obj for obj in data["object_events"] if obj.get("script") == asset.map_script]
            if len(matches) != 1:
                fail(f"{map_path}: expected one object for {asset.map_script}, found {len(matches)}")
            matches[0]["graphics_id"] = asset.enum_name
        write(map_path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def add_trainer_pic_ids() -> None:
    path = Path("include/constants/trainers.h")
    source = read(path)
    missing = [asset.trainer_enum for asset in TRAINER_ASSETS if asset.trainer_enum not in source]
    if not missing:
        return
    payload = "".join(f"    {name},\n" for name in missing if name is not None)
    source = insert_before_once(source, "    TRAINER_PIC_COUNT,", payload, "trainer pic IDs")
    write(path, source)


def append_trainer_graphics_declarations() -> None:
    path = Path("src/data/graphics/trainers.h")
    source = read(path)
    declarations = []
    for asset in TRAINER_ASSETS:
        assert asset.trainer_symbol is not None
        symbol = asset.trainer_symbol
        if f"gTrainerFrontPic_{symbol}" in source:
            continue
        declarations.append(
            f'const u32 gTrainerFrontPic_{symbol}[] = INCGFX_U32('
            f'"graphics/trainers/front_pics/arauna/{asset.key}.png", ".4bpp.smol");\n'
            f'const u16 gTrainerPalette_{symbol}[] = INCGFX_U16('
            f'"graphics/trainers/front_pics/arauna/{asset.key}.png", ".gbapal");\n\n'
        )
    if declarations:
        source = source.rstrip() + "\n\n// Arauna priority-10 NPC pack v3 trainer portraits.\n" + "".join(declarations)
        write(path, source)


def find_source_containing(token: str) -> Path:
    matches: list[Path] = []
    for base in (ROOT / "src", ROOT / "include"):
        for path in base.rglob("*"):
            if path.suffix not in {".c", ".h", ".inc"} or not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if token in content:
                matches.append(path)
    if len(matches) != 1:
        fail(f"expected one source containing {token!r}, found {[str(p.relative_to(ROOT)) for p in matches]}")
    return matches[0]


def extract_struct_block(source: str, marker: str) -> str:
    start = source.find(marker)
    if start < 0:
        fail(f"cannot find template block {marker}")
    brace = source.find("{", start)
    if brace < 0:
        fail(f"cannot find opening brace for {marker}")
    depth = 0
    index = brace
    while index < len(source):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                semicolon = source.find(";", index)
                if semicolon < 0:
                    fail(f"cannot find closing semicolon for {marker}")
                return source[start:semicolon + 1]
        index += 1
    fail(f"unclosed block for {marker}")


def install_trainer_pic_info() -> None:
    info_path = find_source_containing("const struct TrainerPicInfo gTrainerPicInfo")
    source = info_path.read_text(encoding="utf-8")
    template_marker = "static const struct TrainerFrontPicInfo sTrainerFrontPicInfo_Hiker"
    template = extract_struct_block(source, template_marker)
    table_marker = "const struct TrainerPicInfo gTrainerPicInfo"
    table_start = source.find(table_marker)
    if table_start < 0:
        fail("cannot locate trainer pic info table")

    definitions = []
    for asset in TRAINER_ASSETS:
        assert asset.trainer_symbol is not None
        new_name = f"sTrainerFrontPicInfo_{asset.trainer_symbol}"
        if new_name in source:
            continue
        block = template.replace("sTrainerFrontPicInfo_Hiker", new_name)
        block = block.replace("gTrainerFrontPic_Hiker", f"gTrainerFrontPic_{asset.trainer_symbol}")
        block = block.replace("gTrainerPalette_Hiker", f"gTrainerPalette_{asset.trainer_symbol}")
        definitions.append(block + "\n\n")
    if definitions:
        source = source[:table_start] + "// Arauna priority-10 NPC pack v3.\n" + "".join(definitions) + source[table_start:]
        table_start = source.find(table_marker)

    brace_start = source.find("{", table_start)
    if brace_start < 0:
        fail("cannot locate trainer pic table opening brace")
    depth = 0
    brace_end = -1
    for index in range(brace_start, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                brace_end = index
                break
    if brace_end < 0:
        fail("cannot locate trainer pic table closing brace")

    entries = []
    for asset in TRAINER_ASSETS:
        assert asset.trainer_enum is not None and asset.trainer_symbol is not None
        entry = (
            f"    [{asset.trainer_enum}] = "
            f"{{ .frontPic = &sTrainerFrontPicInfo_{asset.trainer_symbol} }},\n"
        )
        if f"[{asset.trainer_enum}]" not in source[brace_start:brace_end]:
            entries.append(entry)
    if entries:
        source = source[:brace_end] + "\n    // Arauna priority-10 NPC pack v3.\n" + "".join(entries) + source[brace_end:]
    info_path.write_text(source, encoding="utf-8")


def replace_trainer_pic(section: str, pic_name: str, gender: str | None = None) -> str:
    if not re.search(r"^Pic: .+$", section, flags=re.MULTILINE):
        fail("trainer section has no Pic field")
    section = re.sub(r"^Pic: .+$", f"Pic: {pic_name}", section, count=1, flags=re.MULTILINE)
    if gender is not None:
        if not re.search(r"^Gender: .+$", section, flags=re.MULTILINE):
            fail("trainer section has no Gender field")
        section = re.sub(r"^Gender: .+$", f"Gender: {gender}", section, count=1, flags=re.MULTILINE)
    return section


def edit_trainer_section(source: str, trainer_id: str, pic_name: str, gender: str | None = None) -> str:
    marker = f"=== {trainer_id} ==="
    start = source.find(marker)
    if start < 0:
        fail(f"missing trainer section {trainer_id}")
    next_start = source.find("\n=== ", start + len(marker))
    if next_start < 0:
        next_start = len(source)
    section = source[start:next_start]
    updated = replace_trainer_pic(section, pic_name, gender)
    return source[:start] + updated + source[next_start:]


def update_story_trainers() -> None:
    path = Path("src/data/trainers.party")
    source = read(path)
    for trainer_id in (
        "TRAINER_ARAUNA_CIRO_PIMPAU",
        "TRAINER_ARAUNA_CIRO_CARAMELO",
        "TRAINER_ARAUNA_CIRO_QUERO",
    ):
        source = edit_trainer_section(source, trainer_id, "Dome Ace Tucker")
    source = edit_trainer_section(
        source,
        "TRAINER_ARAUNA_TECH_AGENT",
        "Pike Queen Lucy",
        "Female",
    )
    source = edit_trainer_section(source, "TRAINER_ARAUNA_MARE_TRIAL", "Arena Tycoon Greta")
    # TRAINER_ARAUNA_UIVO_TRIAL (deaf hermit) left unchanged: eremita portrait rejected, pending regeneration.
    write(path, source)


def add_validator() -> None:
    path = Path("scripts/validate_priority10_npcs.py")
    content = r'''#!/usr/bin/env python3
"""Validate the integrated Arauna priority-10 NPC v3 assets."""

from __future__ import annotations

import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBJECTS = {
    "data/maps/AraunaPlayerHouse/map.json": {
        "AraunaPlayerHouse_EventScript_DonaZila": "OBJ_EVENT_GFX_ARAUNA_DONA_ZILA",
        "AraunaPlayerHouse_EventScript_Anahi": "OBJ_EVENT_GFX_ARAUNA_PROFESSORA_ANAHI",
    },
    "data/maps/AraunaMapLab/map.json": {
        "AraunaMapLab_EventScript_Ciro": "OBJ_EVENT_GFX_ARAUNA_CIRO_PROLOGUE",
    },
    "data/maps/SlateportCity/map.json": {
        "AraunaPorto_EventScript_CiroPorto": "OBJ_EVENT_GFX_ARAUNA_CIRO_CONSORCIO",
        "AraunaPorto_EventScript_DonaCelina": "OBJ_EVENT_GFX_ARAUNA_DONA_CELINA",
        "AraunaPorto_EventScript_ConsortiumAgent": "OBJ_EVENT_GFX_ARAUNA_COMPLIANCE_AGENT",
        "AraunaPorto_EventScript_Dockworker": "OBJ_EVENT_GFX_ARAUNA_DOCKWORKER",
        "AraunaPorto_EventScript_MemorialKeeper": "OBJ_EVENT_GFX_ARAUNA_MEMORIAL_FISHER",
    },
    "data/maps/FallarborTown/map.json": {
        "AraunaSerra_EventScript_LibrasChild": "OBJ_EVENT_GFX_ARAUNA_SERRA_CHILD",
    },
}

OVERWORLDS = (
    "dona_zila", "professora_anahi", "ciro_prologo", "ciro_consorcio",
    "dona_celina", "agente_conformidade", "trabalhador_cais",
    "pescador_memorial", "crianca_serra",
)
TRAINERS = {
    "salon_maiden_anabel.png": "Professora Anahi",
    "dome_ace_tucker.png": "Ciro prologue",
    "factory_head_noland.png": "Ciro Consortium",
    "arena_tycoon_greta.png": "Dona Celina",
    "pike_queen_lucy.png": "Compliance Agent",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def png_info(path: Path) -> tuple[int, int, int, bytes | None]:
    data = path.read_bytes()
    require(data.startswith(b"\x89PNG\r\n\x1a\n"), f"not a PNG: {path}")
    offset = 8
    width = height = colour_type = -1
    transparency = None
    while offset < len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        if kind == b"IHDR":
            width, height, _, colour_type, _, _, _ = struct.unpack(">IIBBBBB", payload)
        elif kind == b"tRNS":
            transparency = payload
        elif kind == b"IEND":
            break
        offset += 12 + length
    return width, height, colour_type, transparency


def main() -> None:
    for name in OVERWORLDS:
        path = ROOT / f"graphics/object_events/pics/people/arauna/{name}.png"
        width, height, colour_type, transparency = png_info(path)
        require((width, height, colour_type) == (48, 128, 3), f"invalid overworld PNG: {path}")
        require(transparency is not None and transparency[:1] == b"\x00", f"missing index-0 transparency: {path}")
    for filename, label in TRAINERS.items():
        path = ROOT / "graphics/trainers/front_pics" / filename
        width, height, colour_type, transparency = png_info(path)
        require((width, height, colour_type) == (64, 64, 3), f"invalid {label} trainer PNG: {path}")
        require(transparency is not None and transparency[:1] == b"\x00", f"missing trainer transparency: {path}")

    for map_path, expected in OBJECTS.items():
        data = json.loads((ROOT / map_path).read_text(encoding="utf-8"))
        by_script = {obj.get("script"): obj for obj in data["object_events"]}
        for script, graphics in expected.items():
            require(script in by_script, f"missing object script {script} in {map_path}")
            require(by_script[script]["graphics_id"] == graphics, f"wrong graphics for {script}")

    event_ids = (ROOT / "include/constants/event_objects.h").read_text(encoding="utf-8")
    graphics = (ROOT / "src/data/object_events/object_event_graphics_info_pointers.h").read_text(encoding="utf-8")
    for graphics_id in {value for values in OBJECTS.values() for value in values.values()}:
        require(graphics_id in event_ids, f"missing object graphics ID {graphics_id}")
        require(f"[{graphics_id}]" in graphics, f"missing object graphics pointer {graphics_id}")

    parties = (ROOT / "src/data/trainers.party").read_text(encoding="utf-8")
    for token in (
        "Pic: Dome Ace Tucker",
        "Pic: Pike Queen Lucy",
        "Pic: Arena Tycoon Greta",
    ):
        require(token in parties, f"story trainer portrait not wired: {token}")
    agent = parties.split("=== TRAINER_ARAUNA_TECH_AGENT ===", 1)[1].split("\n=== ", 1)[0]
    require("Gender: Female" in agent, "v3 Compliance Agent trainer gender is not female")

    serra = (ROOT / "data/text/arauna/en/serra_do_uivo.inc").read_text(encoding="utf-8")
    require("LOOK. WAIT. SAFE." in serra, "approved text support for Libras changed")
    for forbidden in ("LibrasLookAnimation", "LibrasWaitAnimation", "LibrasSafeAnimation"):
        require(forbidden not in "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in (ROOT / "data").rglob("*.inc")),
                f"unvalidated lexical animation was added: {forbidden}")

    docs = (ROOT / "docs/arauna/NPC_PRIORITY10_V3_INTEGRATION.md").read_text(encoding="utf-8")
    require("v3 is canonical" in docs, "v3 canonical-source contract is missing")
    require("No improvised LOOK / WAIT / SAFE animation" in docs, "Libras gate is missing from integration notes")

    print("Priority-10 NPC v3 validated: ten overworlds, six trainer portraits, story wiring and Libras safety gate.")


if __name__ == "__main__":
    main()
'''
    write(path, content)
    (ROOT / path).chmod(0o755)


def update_safety_entrypoints() -> None:
    safety_path = Path("scripts/run_repository_safety.sh")
    safety = read(safety_path)
    line = 'run_check "Priority-10 NPC v3" python3 scripts/validate_priority10_npcs.py\n'
    if line not in safety:
        marker = 'run_check "Araucaria art" python3 scripts/validate_araucaria_art.py\n'
        safety = replace_once(safety, marker, marker + line, "repository-safety NPC validator")
        write(safety_path, safety)


def add_documentation(shared_slots: dict[str, int]) -> None:
    slot_lines = "\n".join(f"- `{key}` → shared Emerald NPC palette {slot}" for key, slot in sorted(shared_slots.items()))
    content = f"""# Priority-10 NPC pack v3 integration

## Source selection

**v3 is canonical.** The v2 archive was used only for comparison. The only art revision between the two packages is the Compliance Agent, whose v3 design reads as a corporate environmental auditor rather than a conventional villain-team member.

## Integrated overworld characters

- Dona Zila;
- Professor Anahi;
- Ciro, prologue clothing;
- Ciro, Consortium clothing;
- Dona Celina;
- Compliance Agent;
- dockworker;
- memorial fisher;
- Serra child.

The deaf hermit is intentionally excluded: its v3 portrait was rejected in ADR-024 visual review and is pending regeneration.

All nine use dedicated object-event graphics IDs and are assigned by narrative script, not by globally replacing Emerald NPC classes.

## Integrated trainer portraits

Five unused Frontier Brain portrait slots in the Arauna campaign are repurposed without changing the global trainer-picture table: Anabel stores Anahi, Tucker stores prologue Ciro, Noland stores Consortium Ciro, Greta stores Dona Celina, and Lucy stores the Compliance Agent. Current story battles use Tucker, Lucy and Greta. Anahi and Consortium Ciro remain installed for later story battles. The deaf hermit's Spenser slot is left untouched until a new portrait is approved.

## Overworld palette adaptation

Emerald normally keeps only four shared NPC palettes and one swappable special-NPC palette available. Multiple competing special palettes cannot coexist on one map. To keep Porto and the Serra stable, the pack's overworld pixel geometry is retained while each sheet is remapped to the closest shared Emerald NPC palette. Trainer portraits preserve their supplied indexed palettes because battle portraits load independently.

{slot_lines}

The original v3 palette files remain the art-direction reference for a later engine-wide palette expansion, but this implementation prioritizes correct simultaneous rendering on original GBA constraints.

## Libras safety gate

The normal child and hermit overworlds are installed. **No improvised LOOK / WAIT / SAFE animation** is implemented. Lexical sign animations remain blocked until video reference, handshape/orientation/movement verification and review by a fluent Libras user or specialist are available.

## Validation

`scripts/validate_priority10_npcs.py` checks PNG format, dimensions and transparency, map-to-character wiring, dedicated object IDs, repurposed campaign portrait slots, current story-battle portraits, the v3 Agent gender, and the Libras animation block.
"""
    write("docs/arauna/NPC_PRIORITY10_V3_INTEGRATION.md", content)


def validate_staged_assets() -> None:
    import struct

    expected = {
        "graphics/object_events/pics/people/arauna/dona_zila.png": (48, 128),
        "graphics/object_events/pics/people/arauna/professora_anahi.png": (48, 128),
        "graphics/object_events/pics/people/arauna/ciro_prologo.png": (48, 128),
        "graphics/object_events/pics/people/arauna/ciro_consorcio.png": (48, 128),
        "graphics/object_events/pics/people/arauna/dona_celina.png": (48, 128),
        "graphics/object_events/pics/people/arauna/agente_conformidade.png": (48, 128),
        "graphics/object_events/pics/people/arauna/trabalhador_cais.png": (48, 128),
        "graphics/object_events/pics/people/arauna/pescador_memorial.png": (48, 128),
        "graphics/object_events/pics/people/arauna/crianca_serra.png": (48, 128),
        "graphics/trainers/front_pics/salon_maiden_anabel.png": (64, 64),
        "graphics/trainers/front_pics/dome_ace_tucker.png": (64, 64),
        "graphics/trainers/front_pics/factory_head_noland.png": (64, 64),
        "graphics/trainers/front_pics/arena_tycoon_greta.png": (64, 64),
        "graphics/trainers/front_pics/pike_queen_lucy.png": (64, 64),
    }
    for relative, dimensions in expected.items():
        path = ROOT / relative
        data = path.read_bytes()
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            fail(f"not a PNG: {relative}")
        width, height, bit_depth, colour_type = struct.unpack(">IIBB", data[16:26])
        if (width, height) != dimensions or bit_depth != 8 or colour_type != 3:
            fail(
                f"invalid indexed asset {relative}: "
                f"{width}x{height}, bit depth {bit_depth}, colour type {colour_type}"
            )


def integrate() -> None:
    shared_slots = {
        "dona_zila": 1,
        "professora_anahi": 4,
        "ciro_prologo": 4,
        "ciro_consorcio": 4,
        "dona_celina": 1,
        "agente_conformidade": 4,
        "trabalhador_cais": 4,
        "pescador_memorial": 4,
        "crianca_serra": 1,
        "eremita_surdo": 1,
    }
    validate_staged_assets()
    add_object_event_ids()
    add_object_event_graphics(shared_slots)
    update_map_graphics()
    update_story_trainers()
    add_validator()
    update_safety_entrypoints()
    add_documentation(shared_slots)

    print("Integrated Arauna priority-10 NPC v3 pack.")
    for asset in ASSETS:
        print(f"  {asset.key}: shared NPC palette {shared_slots[asset.key]}")


def main() -> int:
    try:
        integrate()
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"NPC v3 integration failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

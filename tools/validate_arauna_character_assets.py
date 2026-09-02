#!/usr/bin/env python3
"""Validate the GBA-facing art for every Arauna character in the manifest.

This began as tools/validate_dalva_assets.py, which hard-coded one character.
Seven more leaders follow the same pipeline, and seven near-identical copies
of one validator is how the checks drift apart -- so the character list moved
out into tools/arauna/character_manifest.json and the checks stayed here.

Two kinds of thing are checked.

The art itself, which the GBA reads directly and cannot correct for: a
trainer front is 64x64, an overworld sheet is nine 16x32 frames in one
144x32 strip, both are indexed with palette entry 0 the only transparent
one, no partial alpha, and at most sixteen indices. The walking pairs have
to actually differ, or the character slides along without moving their legs.

And the wiring, which is where the Dalva work found the real trap: a
character can have perfect art and still come out wrong because the graphics
info points at a palette tag shared with fifty other NPCs. So the palette tag
named in the manifest must be used by exactly one graphics info, and the
palette slot must be the one the manifest says -- either the single special
bank, or the second bank addressed as 16 + PALSLOT_NPC_SPECIAL_REFLECTION for
characters who share a map with another special-palette object.

A surface listed in a character's "surfaces" is validated strictly. One that
is absent is reported as outstanding and does not fail the run, so this can
be used while an integration is still half done.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - environment failure path
    raise SystemExit("Pillow is required to validate Arauna PNG assets") from exc

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "tools" / "arauna" / "character_manifest.json"
GRAPHICS_INFO = REPO_ROOT / "src/data/object_events/object_event_graphics_info.h"
GRAPHICS_DECL = REPO_ROOT / "src/data/object_events/object_event_graphics.h"
PIC_TABLES = REPO_ROOT / "src/data/object_events/object_event_pic_tables.h"
TRAINER_GRAPHICS = REPO_ROOT / "src/data/graphics/trainers.h"


@dataclass(frozen=True)
class PngMetadata:
    width: int
    height: int
    bit_depth: int
    color_type: int
    palette: tuple[tuple[int, int, int], ...]
    alpha: tuple[int, ...]


def parse_png(path: Path) -> PngMetadata:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("invalid PNG signature")

    chunks: dict[bytes, bytes] = {}
    offset = 8
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError("truncated PNG chunk")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data):
            raise ValueError(f"truncated {chunk_type.decode('ascii', 'replace')} chunk")
        chunks.setdefault(chunk_type, data[offset + 8:offset + 8 + length])
        offset = chunk_end

    if b"IHDR" not in chunks or b"PLTE" not in chunks:
        raise ValueError("indexed PNG requires IHDR and PLTE chunks")

    width, height, bit_depth, color_type, _, _, _ = struct.unpack(">IIBBBBB", chunks[b"IHDR"])
    raw_palette = chunks[b"PLTE"]
    if len(raw_palette) % 3:
        raise ValueError("invalid PLTE length")
    palette = tuple(tuple(raw_palette[i:i + 3]) for i in range(0, len(raw_palette), 3))
    raw_alpha = chunks.get(b"tRNS", b"")
    alpha = tuple(raw_alpha) + (255,) * (len(palette) - len(raw_alpha))
    return PngMetadata(width, height, bit_depth, color_type, palette, alpha)


def flattened_pixels(image: Image.Image) -> tuple[int, ...]:
    if hasattr(image, "get_flattened_data"):
        return tuple(image.get_flattened_data())
    return tuple(image.getdata())


def validate_indexed_png(path: Path,
                         expected_size: tuple[int, int]) -> tuple[PngMetadata, tuple[int, ...]]:
    metadata = parse_png(path)
    errors: list[str] = []

    if (metadata.width, metadata.height) != expected_size:
        errors.append(f"expected {expected_size[0]}x{expected_size[1]}, "
                      f"got {metadata.width}x{metadata.height}")
    if metadata.color_type != 3:
        errors.append(f"expected indexed PNG color type 3, got {metadata.color_type}")
    if metadata.bit_depth > 8:
        errors.append(f"expected an indexed PNG, got {metadata.bit_depth}-bit")
    if not metadata.alpha or metadata.alpha[0] != 0:
        errors.append("palette index 0 must be transparent")
    if any(alpha not in (0, 255) for alpha in metadata.alpha):
        errors.append("partial alpha is not allowed")

    with Image.open(path) as image:
        if image.mode != "P":
            errors.append(f"Pillow mode must be P, got {image.mode}")
        pixels = flattened_pixels(image)

    used = set(pixels)
    if len(used) > 16 or (used and max(used) > 15):
        errors.append(f"expected at most 16 indices in 0..15, got {sorted(used)}")
    if any(index >= len(metadata.palette) for index in used):
        errors.append("a pixel references an index outside PLTE")
    transparent = {i for i, a in enumerate(metadata.alpha) if a == 0}
    if any(index != 0 and index in transparent for index in used):
        errors.append("a visible pixel references a transparent palette entry")

    if errors:
        raise ValueError("; ".join(errors))
    return metadata, pixels


def parse_jasc_palette(path: Path) -> tuple[tuple[int, int, int], ...]:
    lines = path.read_text(encoding="ascii").splitlines()
    if len(lines) < 3 or lines[0] != "JASC-PAL" or lines[1] != "0100":
        raise ValueError("invalid JASC-PAL header")
    count = int(lines[2])
    colors = tuple(tuple(map(int, line.split())) for line in lines[3:] if line.strip())
    if count != 16 or len(colors) != count:
        raise ValueError(f"expected exactly 16 entries, header={count}, data={len(colors)}")
    if any(len(c) != 3 or any(ch not in range(256) for ch in c) for c in colors):
        raise ValueError("invalid RGB entry")
    return colors


def frame_bbox(frame: tuple[int, ...]) -> tuple[int, int, int, int] | None:
    points = [(i % 16, i // 16) for i, v in enumerate(frame) if v != 0]
    if not points:
        return None
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def validate_overworld(pixels: tuple[int, ...], metadata: PngMetadata) -> None:
    if metadata.width != 144 or metadata.height != 32:
        raise ValueError("sheet must be 144x32, nine 16x32 frames")

    frames = tuple(
        tuple(pixels[y * metadata.width + frame * 16 + x]
              for y in range(32) for x in range(16))
        for frame in range(9)
    )
    boxes = tuple(frame_bbox(frame) for frame in frames)
    if any(box is None for box in boxes):
        raise ValueError("all nine frames must contain visible pixels")
    if len({frames[0], frames[1], frames[2]}) != 3:
        raise ValueError("the south, north and west idle frames must be distinct")
    # A walk pair that does not alternate is a character gliding along with
    # both feet planted.
    for first, second, direction in ((3, 4, "south"), (5, 6, "north"), (7, 8, "west")):
        if frames[first] == frames[second]:
            raise ValueError(f"the {direction} walking frames do not alternate")

    top_edges = {box[1] for box in boxes if box is not None}
    foot_edges = {box[3] for box in boxes if box is not None}
    if max(top_edges) - min(top_edges) > 1 or max(foot_edges) - min(foot_edges) > 1:
        raise ValueError("frames have an inconsistent vertical anchor, so the "
                         "character will bob as they turn")


# A silhouette reaching an edge is ordinary: a boot sole rests on the bottom
# row, a raised weapon grazes the top, and a double portrait spans the full
# width. What is not ordinary is a long flat run of pixels along an edge --
# that is the signature of art that was cut off rather than drawn to fit. The
# threshold sits well above the few pixels a real silhouette contributes and
# well below the tens a truncated one would.
EDGE_RUN_LIMIT = 16


def validate_trainer_front(pixels: tuple[int, ...], metadata: PngMetadata) -> None:
    width, height = metadata.width, metadata.height
    if not any(pixels):
        raise ValueError("trainer front is empty")

    edges = {
        "top": sum(1 for x in range(width) if pixels[x] != 0),
        "bottom": sum(1 for x in range(width) if pixels[(height - 1) * width + x] != 0),
        "left": sum(1 for y in range(height) if pixels[y * width] != 0),
        "right": sum(1 for y in range(height) if pixels[y * width + width - 1] != 0),
    }
    cut = {edge: count for edge, count in edges.items() if count > EDGE_RUN_LIMIT}
    if cut:
        detail = ", ".join(f"{edge} {count}px" for edge, count in sorted(cut.items()))
        raise ValueError(f"a long run of pixels sits on the canvas edge "
                         f"({detail}); the art looks cut off rather than "
                         f"drawn to fit 64x64")


def graphics_info_blocks() -> dict[str, str]:
    text = GRAPHICS_INFO.read_text(encoding="utf-8")
    return dict(re.findall(r"gObjectEventGraphicsInfo_(\w+)\s*=\s*\{(.*?)\n\};",
                           text, re.S))


def validate_wiring(entry: dict, blocks: dict[str, str], errors: list[str],
                    cast: list[dict]) -> None:
    """The half that art QC cannot see: which palette this character gets."""
    name = entry["graphics_info"]
    block = blocks.get(name)
    if block is None:
        errors.append(f"gObjectEventGraphicsInfo_{name} not found")
        return

    tag = re.search(r"\.paletteTag\s*=\s*(\w+)", block)
    slot = re.search(r"\.paletteSlot\s*=\s*([^,]+),", block)
    want_tag = entry["palette_tag"]
    want_slot = entry["palette_slot"]

    if not tag or tag.group(1) != want_tag:
        errors.append(f"paletteTag is {tag.group(1) if tag else '?'}, "
                      f"manifest says {want_tag}")
    if want_slot == "ARAUNA_EXCLUSIVE_POOL":
        # The character asks the general sprite palette allocator for a bank
        # of its own. Its graphics info still names a slot, and that is the
        # documented fallback for a scene where the pool is full, so the check
        # is not "which slot" but "is it actually in the pool list".
        movement = (REPO_ROOT / "src/event_object_movement.c").read_text(encoding="utf-8")
        table = re.search(r"sAraunaExclusivePaletteTags\[\]\s*=\s*\{(.*?)\};",
                          movement, re.S)
        listed = re.findall(r"OBJ_EVENT_PAL_TAG_\w+", table.group(1)) if table else []
        if want_tag not in listed:
            errors.append(f"manifest says the pool allocates {want_tag}, but it "
                          f"is not in sAraunaExclusivePaletteTags")
        if not slot:
            errors.append("the graphics info names no fallback paletteSlot")
    elif not slot or slot.group(1).strip() != want_slot:
        errors.append(f"paletteSlot is {slot.group(1).strip() if slot else '?'}, "
                      f"manifest says {want_slot}")

    # The trap the Dalva work found: art can be perfect and still render in
    # somebody else's colours if the tag is a shared one.
    #
    # One character may legitimately occupy two graphics infos: the engine
    # picks the rival slot opposite the player's gender, so CIRO is drawn from
    # RivalBrendanNormal or RivalMayNormal and never both. That has to be
    # declared in the manifest, and the partner has to declare it back, so a
    # tag can never drift into being shared by accident.
    allowed = 1
    partner = entry.get("graphics_info_shared_with")
    if partner:
        mate = next((c for c in cast if c["name"] == partner), None)
        if mate is None:
            errors.append(f"graphics_info_shared_with names {partner!r}, "
                          f"which is not in the manifest")
        elif mate.get("graphics_info_shared_with") != entry["name"]:
            errors.append(f"{partner} does not declare the shared palette back")
        elif mate.get("palette_tag") != want_tag:
            errors.append(f"{partner} shares the graphics info but carries "
                          f"{mate.get('palette_tag')}, not {want_tag}")
        else:
            allowed = 2

    sharers = [other for other, body in blocks.items()
               if re.search(rf"\.paletteTag\s*=\s*{re.escape(want_tag)}\b", body)]
    if len(sharers) != allowed:
        errors.append(f"{want_tag} is used by {len(sharers)} graphics infos "
                      f"({', '.join(sorted(sharers))}); a character's palette "
                      f"must be their own")

    # The pic table has to walk nine distinct frames, not repeat three.
    table = re.search(rf"sPicTable_{name}\[\]\s*=\s*\{{(.*?)\}};",
                      PIC_TABLES.read_text(encoding="utf-8"), re.S)
    if table:
        indices = re.findall(r"overworld_frame\(\w+,\s*\d+,\s*\d+,\s*(\d+)\)",
                             table.group(1))
        if len(indices) == 9 and len(set(indices)) != 9:
            errors.append(f"sPicTable_{name} repeats frames {sorted(set(indices))}; "
                          f"the nine entries should be frames 0..8")

    # And the declaration has to point at the PNG the manifest names.
    declared = GRAPHICS_DECL.read_text(encoding="utf-8")
    expected_png = entry["overworld"]
    if f'"{expected_png}"' not in declared:
        errors.append(f"object_event_graphics.h does not reference {expected_png}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--manifest", default=str(MANIFEST))
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    blocks = graphics_info_blocks()
    trainer_decl = TRAINER_GRAPHICS.read_text(encoding="utf-8")

    failures = 0
    outstanding: list[str] = []

    characters = manifest["characters"]
    for entry in characters:
        name = entry["name"]
        surfaces = set(entry.get("surfaces", []))
        errors: list[str] = []

        if "front" in surfaces:
            path = REPO_ROOT / entry["front"]
            try:
                metadata, pixels = validate_indexed_png(path, (64, 64))
                validate_trainer_front(pixels, metadata)
                if f'"{entry["front"]}"' not in trainer_decl:
                    errors.append(f"trainers.h does not reference {entry['front']}")
                print(f"[PASS] {name:12} front     64x64, "
                      f"{len(set(pixels))} indices, nothing cut off")
            except (OSError, ValueError) as exc:
                errors.append(f"front: {exc}")
        elif entry.get("front_shared_with"):
            # A double battle draws one portrait for the pair, so the second
            # of them having no front of their own is the design, not a gap.
            print(f"[ ok ] {name:12} front     shares "
                  f"{Path(entry['front']).name} with "
                  f"{entry['front_shared_with']}")
        else:
            na = entry.get("surfaces_not_applicable", {}).get("front")
            if na:
                # Deliberately absent, not unfinished. A phase that never
                # battles must not hold a trainer pic slot.
                print(f"[ -- ] {name:12} front     not needed: {na[:64]}...")
            else:
                outstanding.append(f"{name}: battle portrait")

        if "overworld" in surfaces:
            path = REPO_ROOT / entry["overworld"]
            pal_path = REPO_ROOT / entry["overworld_palette"]
            try:
                metadata, pixels = validate_indexed_png(path, (144, 32))
                validate_overworld(pixels, metadata)
                palette = parse_jasc_palette(pal_path)
                if palette != metadata.palette:
                    raise ValueError(f"{entry['overworld_palette']} does not match "
                                     f"the PNG index order")
                validate_wiring(entry, blocks, errors, characters)
                print(f"[PASS] {name:12} overworld 144x32, 9 frames, "
                      f"{len(set(pixels))} indices, walk pairs alternate, "
                      f"{entry['palette_tag']} exclusive")
            except (OSError, ValueError) as exc:
                errors.append(f"overworld: {exc}")
        else:
            na = entry.get("surfaces_not_applicable", {}).get("overworld")
            if na:
                print(f"[ -- ] {name:12} overworld not possible: {na[:60]}...")
            else:
                outstanding.append(f"{name}: overworld sheet and palette")

        for error in errors:
            print(f"[FAIL] {name}: {error}", file=sys.stderr)
        failures += len(errors)

    if outstanding:
        print("\nNot yet integrated (reported, not failed):")
        for item in outstanding:
            print(f"  - {item}")

    if failures:
        print(f"\nARAUNA CHARACTER ASSET QC: FAIL ({failures} problems)",
              file=sys.stderr)
        return 1
    print("\nARAUNA CHARACTER ASSET QC: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

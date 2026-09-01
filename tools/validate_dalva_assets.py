#!/usr/bin/env python3
"""Validate the GBA-facing Dalva assets used by the vertical slice."""

from __future__ import annotations

import struct
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - environment failure path
    raise SystemExit("Pillow is required to validate Dalva's PNG assets") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
TRAINER_FRONT = REPO_ROOT / "graphics/trainers/front_pics/leader_roxanne.png"
OVERWORLD = REPO_ROOT / "graphics/object_events/pics/people/gym_leaders/roxanne.png"
OVERWORLD_PALETTE = REPO_ROOT / "graphics/object_events/palettes/dalva.pal"


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
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data):
            raise ValueError(f"truncated {chunk_type.decode('ascii', errors='replace')} chunk")
        chunks.setdefault(chunk_type, data[offset + 8 : offset + 8 + length])
        offset = chunk_end

    if b"IHDR" not in chunks or b"PLTE" not in chunks:
        raise ValueError("indexed PNG requires IHDR and PLTE chunks")

    width, height, bit_depth, color_type, _, _, _ = struct.unpack(">IIBBBBB", chunks[b"IHDR"])
    raw_palette = chunks[b"PLTE"]
    if len(raw_palette) % 3:
        raise ValueError("invalid PLTE length")
    palette = tuple(tuple(raw_palette[i : i + 3]) for i in range(0, len(raw_palette), 3))
    raw_alpha = chunks.get(b"tRNS", b"")
    alpha = tuple(raw_alpha) + (255,) * (len(palette) - len(raw_alpha))
    return PngMetadata(width, height, bit_depth, color_type, palette, alpha)


def flattened_pixels(image: Image.Image) -> tuple[int, ...]:
    if hasattr(image, "get_flattened_data"):
        return tuple(image.get_flattened_data())
    return tuple(image.getdata())


def validate_indexed_png(path: Path, expected_size: tuple[int, int]) -> tuple[PngMetadata, tuple[int, ...]]:
    metadata = parse_png(path)
    errors: list[str] = []

    if (metadata.width, metadata.height) != expected_size:
        errors.append(f"expected {expected_size[0]}x{expected_size[1]}, got {metadata.width}x{metadata.height}")
    if metadata.color_type != 3:
        errors.append(f"expected indexed PNG color type 3, got {metadata.color_type}")
    if metadata.bit_depth > 4:
        errors.append(f"expected at most 4-bit indexed PNG, got {metadata.bit_depth}-bit")
    if not 1 <= len(metadata.palette) <= 16:
        errors.append(f"expected 1..16 PLTE entries, got {len(metadata.palette)}")
    if not metadata.alpha or metadata.alpha[0] != 0:
        errors.append("palette index 0 must be transparent")
    if any(alpha not in (0, 255) for alpha in metadata.alpha):
        errors.append("partial alpha is not allowed")
    if [index for index, alpha in enumerate(metadata.alpha) if alpha == 0] != [0]:
        errors.append("palette index 0 must be the only transparent entry")

    with Image.open(path) as image:
        if image.mode != "P":
            errors.append(f"Pillow mode must be P, got {image.mode}")
        pixels = flattened_pixels(image)

    used = set(pixels)
    if len(used) > 16 or (used and max(used) > 15):
        errors.append(f"expected at most 16 total indices in range 0..15, got {sorted(used)}")
    if any(index >= len(metadata.palette) for index in used):
        errors.append("a pixel references an index outside PLTE")
    if any(index != 0 and metadata.alpha[index] != 255 for index in used):
        errors.append("a visible pixel references a transparent palette entry")

    if errors:
        raise ValueError("; ".join(errors))
    return metadata, pixels


def parse_jasc_palette(path: Path) -> tuple[tuple[int, int, int], ...]:
    lines = path.read_text(encoding="ascii").splitlines()
    if len(lines) < 3 or lines[0] != "JASC-PAL" or lines[1] != "0100":
        raise ValueError("invalid JASC-PAL header")
    count = int(lines[2])
    colors = tuple(tuple(map(int, line.split())) for line in lines[3:])
    if count != 16 or len(colors) != count:
        raise ValueError(f"expected exactly 16 palette entries, got header={count}, data={len(colors)}")
    if any(len(color) != 3 or any(channel not in range(256) for channel in color) for color in colors):
        raise ValueError("invalid RGB entry")
    return colors


def frame_bbox(frame: tuple[int, ...]) -> tuple[int, int, int, int] | None:
    points = [(index % 16, index // 16) for index, value in enumerate(frame) if value != 0]
    if not points:
        return None
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def validate_overworld(pixels: tuple[int, ...], metadata: PngMetadata) -> None:
    if metadata.width % 16 or metadata.width // 16 != 9 or metadata.height != 32:
        raise ValueError("sheet must contain exactly nine 16x32 frames")

    frames = tuple(
        tuple(pixels[y * metadata.width + frame * 16 + x] for y in range(32) for x in range(16))
        for frame in range(9)
    )
    boxes = tuple(frame_bbox(frame) for frame in frames)
    if any(box is None for box in boxes):
        raise ValueError("all nine frames must contain visible pixels")
    if len({frames[0], frames[1], frames[2]}) != 3:
        raise ValueError("south, north, and west idle frames must be distinct")
    for first, second, direction in ((3, 4, "south"), (5, 6, "north"), (7, 8, "west/east")):
        if frames[first] == frames[second]:
            raise ValueError(f"{direction} walking frames do not alternate")

    assert all(box is not None for box in boxes)
    top_edges = {box[1] for box in boxes if box is not None}
    foot_edges = {box[3] for box in boxes if box is not None}
    if max(top_edges) - min(top_edges) > 1 or max(foot_edges) - min(foot_edges) > 1:
        raise ValueError("frames have an inconsistent vertical anchor")


def validate_trainer_front(pixels: tuple[int, ...], metadata: PngMetadata) -> None:
    visible = [(index % metadata.width, index // metadata.width) for index, value in enumerate(pixels) if value != 0]
    if not visible:
        raise ValueError("trainer front is empty")
    xs, ys = zip(*visible)
    if min(xs) == 0 or min(ys) == 0 or max(xs) == metadata.width - 1 or max(ys) == metadata.height - 1:
        raise ValueError("trainer front touches the canvas edge and may be clipped")


def main() -> int:
    failures: list[tuple[str, Exception]] = []

    try:
        trainer_metadata, trainer_pixels = validate_indexed_png(TRAINER_FRONT, (64, 64))
        validate_trainer_front(trainer_pixels, trainer_metadata)
        print(f"[PASS] trainer front: 64x64, {len(set(trainer_pixels))} indices, no partial alpha")
    except (OSError, ValueError) as exc:
        print(f"[FAIL] trainer front: {exc}", file=sys.stderr)
        failures.append(("trainer front", exc))

    try:
        overworld_metadata, overworld_pixels = validate_indexed_png(OVERWORLD, (144, 32))
        validate_overworld(overworld_pixels, overworld_metadata)
        palette = parse_jasc_palette(OVERWORLD_PALETTE)
        if palette != overworld_metadata.palette:
            raise ValueError("dalva.pal does not match the overworld PNG index order")
        print(f"[PASS] overworld: 144x32, 9 frames, {len(set(overworld_pixels))} indices, walking pairs alternate")
        print("[PASS] overworld palette: 16 entries, index order matches PNG")
    except (OSError, ValueError) as exc:
        print(f"[FAIL] overworld: {exc}", file=sys.stderr)
        failures.append(("overworld", exc))

    if failures:
        print("DALVA ASSET QC: FAIL", file=sys.stderr)
        return 1
    print("DALVA ASSET QC: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

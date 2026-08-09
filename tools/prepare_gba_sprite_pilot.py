#!/usr/bin/env python3
"""Prepare Arauna pilot sprite candidates for the pokeemerald-expansion format.

This script is intentionally deterministic: it takes transparent, high-resolution
pixel-art candidates, fits them to the GBA canvas, reduces them to 15 visible
colors plus transparency, creates a two-frame front sheet and icon sheet, and
produces a proposed shiny palette without changing the sprite silhouette.
"""

from __future__ import annotations

import argparse
import colorsys
import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass(frozen=True)
class SpeciesConfig:
    slug: str
    number: int
    front_box: tuple[int, int]
    back_box: tuple[int, int]
    shiny_style: str


SPECIES = {
    "caramelo": SpeciesConfig("caramelo", 1, (56, 54), (56, 56), "caramelo"),
    "quero": SpeciesConfig("quero", 4, (48, 56), (48, 56), "quero"),
    "pimpau": SpeciesConfig("pimpau", 7, (54, 54), (52, 56), "pimpau"),
}


def opaque_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    bbox = alpha.point(lambda value: 255 if value >= 128 else 0).getbbox()
    if bbox is None:
        raise ValueError("candidate has no opaque pixels")
    return bbox


def fit_candidate(source: Path, box: tuple[int, int]) -> Image.Image:
    image = Image.open(source).convert("RGBA")
    image = image.crop(opaque_bbox(image))
    width, height = image.size
    target_width, target_height = box
    scale = min(target_width / width, target_height / height)
    size = (max(1, round(width * scale)), max(1, round(height * scale)))
    image = image.resize(size, Image.Resampling.NEAREST)

    canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    x = (64 - image.width) // 2
    y = 63 - image.height
    canvas.alpha_composite(image, (x, y))
    return canvas


def visible_palette(image: Image.Image, colors: int = 15) -> list[tuple[int, int, int]]:
    pixels = [rgb for *rgb, alpha in image.getdata() if alpha >= 128]
    if not pixels:
        raise ValueError("image has no visible pixels")
    sample = Image.new("RGB", (len(pixels), 1))
    sample.putdata([tuple(pixel) for pixel in pixels])
    quantized = sample.quantize(
        colors=colors,
        method=Image.Quantize.MAXCOVERAGE,
        dither=Image.Dither.NONE,
    )
    raw = quantized.getpalette() or []
    used = sorted(set(quantized.getdata()))
    return [tuple(raw[index * 3 : index * 3 + 3]) for index in used]


def nearest_color_index(
    color: tuple[int, int, int], palette: list[tuple[int, int, int]]
) -> int:
    red, green, blue = color
    return min(
        range(len(palette)),
        key=lambda index: sum(
            (component - palette[index][channel]) ** 2
            for channel, component in enumerate((red, green, blue))
        ),
    )


def palettize(
    image: Image.Image,
    palette: list[tuple[int, int, int]] | None = None,
) -> tuple[Image.Image, list[tuple[int, int, int]]]:
    palette = palette or visible_palette(image)
    out = Image.new("P", image.size, 0)
    flat_palette = [0, 0, 0]
    for color in palette:
        flat_palette.extend(color)
    flat_palette.extend([0] * (768 - len(flat_palette)))
    out.putpalette(flat_palette)
    indices = []
    for red, green, blue, alpha in image.getdata():
        if alpha < 128:
            indices.append(0)
        else:
            indices.append(1 + nearest_color_index((red, green, blue), palette))
    out.putdata(indices)
    out.info["transparency"] = 0
    return out, palette


def transform_shiny_color(
    color: tuple[int, int, int], style: str
) -> tuple[int, int, int]:
    red, green, blue = (value / 255 for value in color)
    hue, lightness, saturation = colorsys.rgb_to_hls(red, green, blue)
    degrees = hue * 360

    if lightness < 0.13 or saturation < 0.08:
        if style == "quero" and 0.18 < lightness < 0.83:
            hue, saturation = 0.10, 0.28
        else:
            return color
    elif style == "caramelo":
        if saturation > 0.72 and degrees < 65:
            hue, saturation = 0.56, min(1.0, saturation * 0.92)
        elif degrees < 80 or degrees > 330:
            hue, saturation = 0.96, max(0.35, saturation * 0.72)
    elif style == "quero":
        if 175 <= degrees <= 250 and saturation > 0.30:
            hue, saturation = 0.78, min(1.0, saturation * 1.05)
        elif degrees < 35 or degrees > 330:
            hue, saturation = 0.12, max(0.45, saturation)
        elif saturation < 0.30:
            hue, saturation = 0.10, 0.24
    elif style == "pimpau":
        if degrees < 35 or degrees > 330:
            hue, saturation = 0.66, min(1.0, saturation * 0.95)
        elif 35 <= degrees <= 75:
            hue, saturation = 0.43, min(1.0, saturation * 0.88)
        elif 75 < degrees < 170:
            hue, saturation = 0.12, min(1.0, saturation)

    shiny = colorsys.hls_to_rgb(hue, lightness, saturation)
    return tuple(max(0, min(255, round(channel * 255))) for channel in shiny)


def replace_palette(image: Image.Image, colors: list[tuple[int, int, int]]) -> Image.Image:
    out = image.copy()
    flat = [0, 0, 0]
    for color in colors:
        flat.extend(color)
    flat.extend([0] * (768 - len(flat)))
    out.putpalette(flat)
    out.info["transparency"] = 0
    return out


def front_sheet(frame: Image.Image) -> Image.Image:
    sheet = Image.new("P", (64, 128), 0)
    sheet.putpalette(frame.getpalette())
    sheet.paste(frame, (0, 0))
    sheet.paste(frame, (0, 64))
    sheet.info["transparency"] = 0
    return sheet


def read_jasc_palette(path: Path) -> list[tuple[int, int, int]]:
    lines = path.read_text(encoding="ascii").replace("\r", "").splitlines()
    if lines[:3] != ["JASC-PAL", "0100", "16"]:
        raise ValueError(f"unsupported palette format: {path}")
    return [tuple(map(int, line.split())) for line in lines[3:19]]


def map_to_fixed_palette(
    image: Image.Image, colors: list[tuple[int, int, int]]
) -> tuple[Image.Image, int]:
    out = Image.new("P", image.size, 0)
    flat = [component for color in colors for component in color]
    flat.extend([0] * (768 - len(flat)))
    out.putpalette(flat)
    indices = []
    error = 0
    visible = colors[1:]
    for red, green, blue, alpha in image.getdata():
        if alpha < 128:
            indices.append(0)
            continue
        palette_offset = nearest_color_index((red, green, blue), visible)
        mapped = visible[palette_offset]
        indices.append(1 + palette_offset)
        error += sum((source - target) ** 2 for source, target in zip((red, green, blue), mapped))
    out.putdata(indices)
    out.info["transparency"] = 0
    return out, error


def icon_sheet(frame: Image.Image, palette_dir: Path) -> tuple[Image.Image, int]:
    rgba = frame.convert("RGBA")
    rgba = rgba.crop(opaque_bbox(rgba))
    scale = min(28 / rgba.width, 27 / rgba.height)
    size = (max(1, round(rgba.width * scale)), max(1, round(rgba.height * scale)))
    rgba = rgba.resize(size, Image.Resampling.NEAREST)
    icon = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    icon.alpha_composite(rgba, ((32 - rgba.width) // 2, 30 - rgba.height))
    candidates = []
    for index in range(6):
        colors = read_jasc_palette(palette_dir / f"pal{index}.pal")
        mapped, error = map_to_fixed_palette(icon, colors)
        candidates.append((error, index, mapped))
    _, palette_index, icon = min(candidates, key=lambda item: item[0])

    sheet = Image.new("P", (32, 64), 0)
    sheet.putpalette(icon.getpalette())
    sheet.paste(icon, (0, 0))
    sheet.paste(icon, (0, 32))
    sheet.info["transparency"] = 0
    return sheet, palette_index


def write_jasc_palette(path: Path, colors: list[tuple[int, int, int]]) -> None:
    all_colors = [(98, 156, 131), *colors]
    if len(all_colors) != 16:
        raise ValueError(f"expected 16 palette entries, got {len(all_colors)}")
    lines = ["JASC-PAL", "0100", "16", *(" ".join(map(str, color)) for color in all_colors)]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def save_preview(image: Image.Image, path: Path, scale: int = 6) -> None:
    preview = image.convert("RGBA").resize(
        (image.width * scale, image.height * scale), Image.Resampling.NEAREST
    )
    preview.save(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--species", choices=sorted(SPECIES), required=True)
    parser.add_argument("--front", type=Path, required=True)
    parser.add_argument("--back", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--icon-palettes",
        type=Path,
        default=Path("engine-reference/graphics/pokemon/icon_palettes"),
    )
    args = parser.parse_args()

    config = SPECIES[args.species]
    destination = args.out / f"{config.number:03d}_{config.slug}"
    destination.mkdir(parents=True, exist_ok=True)

    front_rgba = fit_candidate(args.front, config.front_box)
    back_rgba = fit_candidate(args.back, config.back_box)
    combined = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    combined.alpha_composite(front_rgba, (0, 0))
    combined.alpha_composite(back_rgba, (64, 0))
    shared_palette = visible_palette(combined)

    front, shared_palette = palettize(front_rgba, shared_palette)
    back, _ = palettize(back_rgba, shared_palette)
    shiny_palette = [
        transform_shiny_color(color, config.shiny_style) for color in shared_palette
    ]
    shiny_front = replace_palette(front, shiny_palette)
    shiny_back = replace_palette(back, shiny_palette)

    normal_front_sheet = front_sheet(front)
    shiny_front_sheet = front_sheet(shiny_front)
    icon, icon_palette_index = icon_sheet(front, args.icon_palettes)

    normal_front_sheet.save(destination / "anim_front.png")
    back.save(destination / "back.png")
    icon.save(destination / "icon.png")
    write_jasc_palette(destination / "normal.pal", shared_palette)
    write_jasc_palette(destination / "shiny.pal", shiny_palette)
    shiny_front_sheet.save(destination / "anim_front_shiny_preview.png")
    shiny_back.save(destination / "back_shiny_preview.png")

    save_preview(front, destination / "front_preview.png")
    save_preview(back, destination / "back_preview.png")
    save_preview(shiny_front, destination / "front_shiny_preview.png")
    save_preview(shiny_back, destination / "back_shiny_preview.png")
    save_preview(icon, destination / "icon_preview.png")
    (destination / "candidate_profile.json").write_text(
        json.dumps(
            {
                "dex": config.number,
                "name": config.slug,
                "status": "awaiting-visual-approval",
                "frontPicBox": list(config.front_box),
                "backPicBox": list(config.back_box),
                "iconPalIndex": icon_palette_index,
                "visibleColors": len(shared_palette),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"{config.number:03d} {config.slug}: "
        f"front={front.size}, back={back.size}, icon={icon.size}, "
        f"visible_colors={len(shared_palette)}+transparent, icon_palette={icon_palette_index}"
    )


if __name__ == "__main__":
    main()

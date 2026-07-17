#!/usr/bin/env python3
"""Build a complete, deterministic 386-species GBA art set for Arauna.

The supplied Dex contains one front reference for entries 001-314 and structured
design data for all 386 entries.  This tool turns every entry into the files used
by pokeemerald-expansion:

* 64x128 two-frame indexed front sheet;
* 64x64 indexed back sprite;
* 32x64 indexed menu icon;
* normal and shiny 16-color JASC palettes;
* previews and a machine-readable production profile.

Entries 001-009 reuse the hand-prepared packages.  Entries 010-314 are isolated
from their presentation backgrounds and converted.  Since those references only
show the front, their back view is a deterministic silhouette reconstruction.
Entries 315-386 have no supplied art and receive distinct procedural concept
sprites derived from their name, type, category and inspiration.
"""

from __future__ import annotations

import argparse
import colorsys
import csv
import hashlib
import json
import math
import random
import re
import shutil
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage


TRANSPARENT_RGB = (98, 156, 131)
TYPE_RGB = {
    "normal": (184, 176, 144), "fire": (224, 72, 38),
    "water": (47, 137, 211), "grass": (74, 161, 71),
    "electric": (239, 194, 37), "ice": (103, 201, 214),
    "fighting": (178, 61, 45), "poison": (151, 69, 163),
    "ground": (181, 139, 73), "flying": (125, 159, 218),
    "psychic": (226, 75, 133), "bug": (139, 161, 42),
    "rock": (154, 129, 67), "ghost": (91, 73, 137),
    "dragon": (96, 68, 198), "dark": (84, 72, 69),
    "steel": (153, 161, 177), "fairy": (219, 134, 178),
}

SHINY_HUE = {
    "normal": 0.12, "fire": 0.56, "water": 0.78, "grass": 0.12,
    "electric": 0.92, "ice": 0.91, "fighting": 0.62,
    "poison": 0.38, "ground": 0.48, "flying": 0.94,
    "psychic": 0.55, "bug": 0.78, "rock": 0.48,
    "ghost": 0.10, "dragon": 0.02, "dark": 0.55,
    "steel": 0.14, "fairy": 0.52,
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def stable_seed(entry: dict) -> int:
    raw = f"{entry['id']}|{entry['name']}|{entry.get('inspiration', '')}".encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big")


def opaque_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    bbox = image.getchannel("A").point(lambda x: 255 if x >= 128 else 0).getbbox()
    if bbox is None:
        raise ValueError("sprite has no opaque pixels")
    return bbox


def remove_presentation_background(path: Path) -> Image.Image:
    """Isolate the main design from smooth beige/white presentation backgrounds."""
    source = Image.open(path).convert("RGBA")
    source.thumbnail((256, 256), Image.Resampling.NEAREST)
    rgba = np.asarray(source).copy()
    if np.any(rgba[:, :, 3] < 16):
        mask = rgba[:, :, 3] >= 64
    else:
        rgb = rgba[:, :, :3].astype(np.int32)
        border = np.concatenate((rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]), axis=0)
        strip = Image.fromarray(border.astype(np.uint8).reshape(1, -1, 3), "RGB")
        quant = strip.quantize(colors=10, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        pal = np.array(quant.getpalette()[:30], dtype=np.int32).reshape(-1, 3)
        used = np.unique(np.asarray(quant))
        bg_colors = pal[used]
        distance = np.full(rgb.shape[:2], 1_000_000, dtype=np.int32)
        for color in bg_colors:
            delta = rgb - color
            distance = np.minimum(distance, np.sum(delta * delta, axis=2))
        candidate = distance <= 48 * 48
        seed = np.zeros(candidate.shape, dtype=bool)
        seed[[0, -1], :] = candidate[[0, -1], :]
        seed[:, [0, -1]] = candidate[:, [0, -1]]
        background = ndimage.binary_propagation(seed, mask=candidate)
        mask = ~background

    labels, count = ndimage.label(mask)
    if count:
        sizes = np.bincount(labels.ravel())
        sizes[0] = 0
        largest = int(sizes.max())
        keep = sizes >= max(4, round(largest * 0.006))
        mask = keep[labels]
        mask = ndimage.binary_fill_holes(mask)

    rgba[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
    rgba[~mask, :3] = 255
    return Image.fromarray(rgba, "RGBA")


def fit_rgba(image: Image.Image, box: tuple[int, int] = (58, 58)) -> Image.Image:
    image = image.crop(opaque_bbox(image))
    scale = min(box[0] / image.width, box[1] / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    image = image.resize(size, Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    canvas.alpha_composite(image, ((64 - image.width) // 2, 63 - image.height))
    return canvas


def largest_and_companions(image: Image.Image) -> Image.Image:
    arr = np.asarray(image).copy()
    labels, count = ndimage.label(arr[:, :, 3] >= 128)
    if not count:
        return image
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    largest = int(sizes.max())
    mask = sizes[labels] >= max(1, round(largest * 0.003))
    arr[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def reconstructed_back(front: Image.Image) -> Image.Image:
    """Create a battle-usable rear silhouette where no rear reference exists."""
    back = front.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    arr = np.asarray(back).copy()
    alpha = arr[:, :, 3] >= 128
    # Subtle shade shift makes the rear read separately without inventing anatomy.
    rgb = arr[:, :, :3].astype(np.float32)
    yy = np.linspace(0.86, 1.04, 64, dtype=np.float32)[:, None, None]
    rgb = np.clip(rgb * yy, 0, 255)
    arr[:, :, :3] = rgb.astype(np.uint8)
    arr[~alpha, 3] = 0
    return Image.fromarray(arr, "RGBA")


def palette_for(images: list[Image.Image]) -> tuple[list[tuple[int, int, int]], int]:
    visible: list[tuple[int, int, int]] = []
    for image in images:
        visible.extend(tuple(px[:3]) for px in image.getdata() if px[3] >= 128)
    sample = Image.new("RGB", (len(visible), 1))
    sample.putdata(visible)
    q = sample.quantize(colors=15, method=Image.Quantize.MAXCOVERAGE, dither=Image.Dither.NONE)
    raw = q.getpalette() or []
    used = sorted(set(q.getdata()))
    colors = [tuple(raw[i * 3:i * 3 + 3]) for i in used]
    actual = len(colors)
    while len(colors) < 15:
        colors.append(colors[-1] if colors else (0, 0, 0))
    return colors[:15], actual


def nearest_index(rgb: tuple[int, int, int], palette: list[tuple[int, int, int]]) -> int:
    return min(range(len(palette)), key=lambda i: sum((rgb[c] - palette[i][c]) ** 2 for c in range(3)))


def palettize(image: Image.Image, colors: list[tuple[int, int, int]]) -> Image.Image:
    out = Image.new("P", image.size, 0)
    flat = [0, 0, 0] + [v for color in colors for v in color]
    out.putpalette(flat + [0] * (768 - len(flat)))
    indices = []
    for r, g, b, a in image.getdata():
        indices.append(0 if a < 128 else 1 + nearest_index((r, g, b), colors))
    out.putdata(indices)
    out.info["transparency"] = 0
    return out


def shiny_palette(colors: list[tuple[int, int, int]], types: list[str]) -> list[tuple[int, int, int]]:
    primary = types[0] if types else "normal"
    secondary = types[1] if len(types) > 1 else primary
    targets = (SHINY_HUE.get(primary, 0.5), SHINY_HUE.get(secondary, 0.1))
    out = []
    for i, color in enumerate(colors):
        r, g, b = (x / 255 for x in color)
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        if l < 0.10:
            nl, ns, nh = l, s, h
        elif s < 0.10:
            nh = targets[i % 2]
            ns = 0.18 if 0.18 < l < 0.86 else s
            nl = l
        else:
            nh = targets[0] if i % 3 else targets[1]
            ns = min(1.0, max(0.35, s * 0.92))
            nl = min(0.90, max(0.10, l * (1.08 if i % 2 else 0.92)))
        out.append(tuple(round(v * 255) for v in colorsys.hls_to_rgb(nh, nl, ns)))
    return out


def apply_palette(image: Image.Image, colors: list[tuple[int, int, int]]) -> Image.Image:
    out = image.copy()
    flat = [0, 0, 0] + [v for color in colors for v in color]
    out.putpalette(flat + [0] * (768 - len(flat)))
    out.info["transparency"] = 0
    return out


def animated_sheet(frame: Image.Image) -> Image.Image:
    sheet = Image.new("P", (64, 128), 0)
    sheet.putpalette(frame.getpalette())
    sheet.paste(frame, (0, 0))
    # Frame two is a restrained one-pixel idle lift, safe for every silhouette.
    sheet.paste(frame.crop((0, 1, 64, 64)), (0, 64))
    sheet.info["transparency"] = 0
    return sheet


def read_jasc(path: Path) -> list[tuple[int, int, int]]:
    lines = path.read_text(encoding="ascii").replace("\r", "").splitlines()
    return [tuple(map(int, line.split())) for line in lines[3:19]]


def icon_sheet(frame: Image.Image, palette_dir: Path) -> tuple[Image.Image, int]:
    rgba = frame.convert("RGBA").crop(opaque_bbox(frame.convert("RGBA")))
    scale = min(28 / rgba.width, 27 / rgba.height)
    rgba = rgba.resize((max(1, round(rgba.width * scale)), max(1, round(rgba.height * scale))), Image.Resampling.NEAREST)
    icon_rgba = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    icon_rgba.alpha_composite(rgba, ((32 - rgba.width) // 2, 30 - rgba.height))
    candidates = []
    for index in range(6):
        pal = read_jasc(palette_dir / f"pal{index}.pal")
        mapped = Image.new("P", (32, 32), 0)
        mapped.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
        error = 0
        values = []
        for r, g, b, a in icon_rgba.getdata():
            if a < 128:
                values.append(0)
            else:
                j = 1 + nearest_index((r, g, b), pal[1:])
                values.append(j)
                error += sum((x - y) ** 2 for x, y in zip((r, g, b), pal[j]))
        mapped.putdata(values)
        mapped.info["transparency"] = 0
        candidates.append((error, index, mapped))
    _, index, frame32 = min(candidates, key=lambda x: x[0])
    sheet = Image.new("P", (32, 64), 0)
    sheet.putpalette(frame32.getpalette())
    sheet.paste(frame32, (0, 0))
    sheet.paste(frame32.crop((0, 1, 32, 32)), (0, 32))
    sheet.info["transparency"] = 0
    return sheet, index


def write_jasc(path: Path, colors: list[tuple[int, int, int]]) -> None:
    colors = colors[:15]
    while len(colors) < 15:
        colors.append(colors[-1] if colors else (0, 0, 0))
    lines = ["JASC-PAL", "0100", "16"] + [" ".join(map(str, c)) for c in [TRANSPARENT_RGB, *colors]]
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def lighten(color: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(c + (255 - c) * amount) for c in color)


def darken(color: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(round(c * (1 - amount)) for c in color)


def classify_shape(entry: dict) -> str:
    text = " ".join(str(entry.get(k, "")) for k in ("name", "category", "inspiration")).lower()
    types = entry.get("types", [])
    rules = [
        ("bird", ("ave", "pássar", "passar", "arara", "tuim", "periqu", "beija-flor", "urubu", "coruja", "galinha", "pato", "tucan", "gavião", "gaviao")),
        ("insect", ("inset", "formig", "besour", "mosquit", "maripos", "borbolet", "abelh", "vespa", "cigarr", "cupim", "barata")),
        ("serpent", ("cobra", "serpente", "minhoca", "enguia", "sucuri", "boitatá", "boitata", "lagarta")),
        ("aquatic", ("peixe", "boto", "arraia", "tubarão", "tubarao", "carangue", "camarão", "camarao", "siri", "lula", "polvo", "água-viva", "agua-viva")),
        ("object", ("lata", "bituca", "garrafa", "pneu", "lixo", "chorume", "ferrug", "óleo", "oleo", "lampião", "lampiao", "pipa", "boneco", "panela", "sino", "rede", "papel")),
        ("humanoid", ("guardião", "guardiao", "guerreiro", "caboclo", "saci", "curup", "caipora", "dança", "danca", "festa", "lenda", "entidade", "humano")),
    ]
    for shape, words in rules:
        if any(word in text for word in words):
            return shape
    if "bug" in types:
        return "insect"
    if "flying" in types:
        return "bird"
    if "water" in types and stable_seed(entry) % 3 == 0:
        return "aquatic"
    return "quadruped"


def procedural_sprite(entry: dict, rear: bool = False) -> Image.Image:
    """Draw an original 32px concept silhouette and scale it to the GBA canvas."""
    rng = random.Random(stable_seed(entry) + (1009 if rear else 0))
    shape = classify_shape(entry)
    types = entry.get("types") or ["normal"]
    base = TYPE_RGB.get(types[0], TYPE_RGB["normal"])
    accent = TYPE_RGB.get(types[1], lighten(base, 0.35)) if len(types) > 1 else lighten(base, 0.38)
    shadow, outline, highlight = darken(base, 0.34), darken(base, 0.72), lighten(base, 0.58)
    image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)

    def ellipse(box, fill, width=1):
        d.ellipse(box, fill=outline)
        if width and box[2] - box[0] > 2 and box[3] - box[1] > 2:
            d.ellipse((box[0] + width, box[1] + width, box[2] - width, box[3] - width), fill=fill)

    def polygon(points, fill):
        d.polygon(points, fill=outline)
        cx = sum(x for x, _ in points) / len(points)
        cy = sum(y for _, y in points) / len(points)
        inner = [(round(cx + (x - cx) * 0.78), round(cy + (y - cy) * 0.78)) for x, y in points]
        d.polygon(inner, fill=fill)

    if shape == "bird":
        polygon([(8, 17), (2, 12), (4, 22), (12, 24)], accent)
        ellipse((8, 8, 24, 26), base)
        ellipse((18, 5, 27, 15), base)
        polygon([(26, 9), (31, 11), (26, 13)], accent)
        polygon([(10, 23), (7, 29), (13, 25)], shadow)
        if not rear:
            d.rectangle((23, 8, 24, 9), fill=highlight)
    elif shape == "insect":
        ellipse((11, 6, 21, 14), base)
        ellipse((9, 12, 23, 25), shadow)
        polygon([(11, 10), (3, 8), (6, 18), (12, 17)], accent)
        polygon([(21, 10), (29, 8), (26, 18), (20, 17)], accent)
        for y in (15, 19, 23):
            d.line((10, y, 4, y + rng.choice((-2, 2))), fill=outline, width=1)
            d.line((22, y, 28, y + rng.choice((-2, 2))), fill=outline, width=1)
        d.line((14, 7, 10, 2), fill=outline)
        d.line((18, 7, 22, 2), fill=outline)
        if not rear:
            d.point((14, 9), fill=highlight); d.point((18, 9), fill=highlight)
    elif shape == "serpent":
        d.line([(5, 25), (11, 28), (18, 25), (13, 20), (18, 15), (23, 17)], fill=outline, width=7)
        d.line([(5, 25), (11, 28), (18, 25), (13, 20), (18, 15), (23, 17)], fill=base, width=4)
        ellipse((18, 7, 29, 18), base)
        polygon([(21, 8), (22, 3), (25, 8)], accent)
        if not rear:
            d.rectangle((25, 11, 26, 12), fill=highlight)
    elif shape == "aquatic":
        ellipse((5, 10, 25, 24), base)
        polygon([(6, 13), (1, 7), (2, 18)], accent)
        polygon([(7, 21), (2, 27), (12, 23)], accent)
        polygon([(24, 14), (31, 10), (29, 20)], shadow)
        if not rear:
            d.rectangle((20, 14, 21, 15), fill=highlight)
    elif shape == "object":
        variant = stable_seed(entry) % 3
        if variant == 0:
            polygon([(8, 7), (23, 7), (25, 26), (6, 26)], base)
            d.line((8, 11, 23, 11), fill=accent, width=2)
        elif variant == 1:
            ellipse((7, 7, 25, 27), base)
            polygon([(12, 5), (15, 1), (18, 5)], accent)
        else:
            polygon([(5, 12), (12, 5), (25, 8), (28, 22), (17, 28), (6, 24)], base)
        d.rectangle((11, 15, 21, 18), fill=shadow)
        if not rear:
            d.point((13, 16), fill=highlight); d.point((19, 16), fill=highlight)
    elif shape == "humanoid":
        ellipse((10, 3, 22, 15), base)
        polygon([(9, 13), (23, 13), (26, 27), (6, 27)], base)
        polygon([(9, 15), (3, 22), (7, 24), (13, 18)], accent)
        polygon([(23, 15), (29, 22), (25, 24), (19, 18)], accent)
        if stable_seed(entry) % 2:
            polygon([(9, 6), (16, 0), (23, 6)], accent)
        if not rear:
            d.rectangle((13, 8, 14, 9), fill=highlight); d.rectangle((18, 8, 19, 9), fill=highlight)
    else:
        ellipse((7, 11, 25, 25), base)
        ellipse((17, 6, 28, 17), base)
        polygon([(19, 8), (19, 3), (23, 7)], accent)
        polygon([(25, 8), (29, 4), (28, 11)], accent)
        for x in (9, 14, 20, 24):
            d.rectangle((x, 22, x + 3, 29), fill=outline)
            d.rectangle((x + 1, 22, x + 2, 28), fill=shadow)
        d.line((7, 16, 2, 10 + stable_seed(entry) % 8), fill=outline, width=3)
        d.line((7, 16, 2, 10 + stable_seed(entry) % 8), fill=accent, width=1)
        if not rear:
            d.rectangle((24, 9, 25, 10), fill=highlight)

    # Seeded markings make every procedural design visibly distinct.
    for _ in range(2 + stable_seed(entry) % 4):
        x, y = rng.randint(9, 23), rng.randint(11, 23)
        if image.getpixel((x, y))[3]:
            d.rectangle((x, y, min(31, x + rng.randint(0, 2)), min(31, y + 1)), fill=accent)
    image = image.resize((64, 64), Image.Resampling.NEAREST)
    return fit_rgba(image, (58, 58))


def copy_prepared_package(source: Path, destination: Path, entry: dict) -> dict:
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("anim_front.png", "back.png", "icon.png", "normal.pal", "shiny.pal"):
        shutil.copy2(source / name, destination / name)
    profile = json.loads((source / "candidate_profile.json").read_text(encoding="utf-8"))
    profile.update(
        {
            "dex": entry["id"],
            "name": entry["name"],
            "types": entry.get("types", []),
            "status": "integrated",
            "productionMethod": "hand-prepared-approved",
            "referenceStatus": "available",
            "animation": profile.get("animation") or "two-frame-idle-lift",
            "shiny": profile.get("shiny") or "type-directed-palette",
        }
    )
    (destination / "candidate_profile.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return profile


def build_package(entry: dict, source: Path | None, destination: Path, palette_dir: Path) -> dict:
    destination.mkdir(parents=True, exist_ok=True)
    if source:
        raw = remove_presentation_background(source)
        front_rgba = largest_and_companions(fit_rgba(raw))
        back_rgba = reconstructed_back(front_rgba)
        method = "reference-front-plus-reconstructed-back"
        reference = "available"
    else:
        front_rgba = procedural_sprite(entry, rear=False)
        back_rgba = procedural_sprite(entry, rear=True)
        method = "procedural-concept-front-and-back"
        reference = "missing-created-from-dex-data"

    colors, actual = palette_for([front_rgba, back_rgba])
    front = palettize(front_rgba, colors)
    back = palettize(back_rgba, colors)
    shiny = shiny_palette(colors, entry.get("types") or ["normal"])
    icon, icon_index = icon_sheet(front, palette_dir)

    animated_sheet(front).save(destination / "anim_front.png")
    back.save(destination / "back.png")
    icon.save(destination / "icon.png")
    write_jasc(destination / "normal.pal", colors)
    write_jasc(destination / "shiny.pal", shiny)

    normal_preview = front.convert("RGBA")
    shiny_preview = apply_palette(front, shiny).convert("RGBA")
    back_preview = back.convert("RGBA")
    for name, image in (("front_preview.png", normal_preview), ("front_shiny_preview.png", shiny_preview), ("back_preview.png", back_preview)):
        image.resize((256, 256), Image.Resampling.NEAREST).save(destination / name)

    profile = {
        "dex": entry["id"], "name": entry["name"], "types": entry.get("types", []),
        "status": "integrated", "productionMethod": method, "referenceStatus": reference,
        "frontPicBox": [58, 58], "backPicBox": [58, 58],
        "iconPalIndex": icon_index, "visibleColors": actual,
        "animation": "two-frame-idle-lift", "shiny": "type-directed-palette",
    }
    (destination / "candidate_profile.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return profile


def prepared_lookup(root: Path, output: Path | None = None) -> dict[int, Path]:
    result = {}
    for folder in root.glob("**/[0-9][0-9][0-9]_*"):
        if output is not None and (folder == output or output in folder.parents):
            continue
        if (folder / "anim_front.png").is_file():
            result[int(folder.name[:3])] = folder
    return result


def contact_sheets(entries: list[dict], packages: Path, out: Path) -> list[Path]:
    out.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    written = []
    for page, start in enumerate(range(0, len(entries), 48), start=1):
        chunk = entries[start:start + 48]
        sheet = Image.new("RGB", (8 * 144, 6 * 118), (244, 239, 223))
        draw = ImageDraw.Draw(sheet)
        for index, entry in enumerate(chunk):
            row, col = divmod(index, 8)
            x, y = col * 144, row * 118
            folder = packages / f"{entry['id']:03d}_{slugify(entry['name'])}"
            front = Image.open(folder / "anim_front.png").crop((0, 0, 64, 64)).convert("RGBA")
            shiny_colors = read_jasc(folder / "shiny.pal")[1:]
            shiny = apply_palette(Image.open(folder / "anim_front.png").crop((0, 0, 64, 64)), shiny_colors).convert("RGBA")
            back = Image.open(folder / "back.png").convert("RGBA")
            sheet.paste(front.resize((64, 64), Image.Resampling.NEAREST), (x + 4, y + 18), front.resize((64, 64), Image.Resampling.NEAREST))
            sheet.paste(shiny.resize((48, 48), Image.Resampling.NEAREST), (x + 68, y + 30), shiny.resize((48, 48), Image.Resampling.NEAREST))
            sheet.paste(back.resize((40, 40), Image.Resampling.NEAREST), (x + 102, y + 42), back.resize((40, 40), Image.Resampling.NEAREST))
            draw.text((x + 4, y + 3), f"#{entry['id']:03d} {entry['name'][:17]}", fill=(32, 42, 35), font=font)
            draw.text((x + 4, y + 88), "/".join(entry.get("types", [])).upper(), fill=(58, 79, 65), font=font)
        path = out / f"arauna-fakemons-{page:02d}.png"
        sheet.save(path)
        written.append(path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dex", type=Path, default=Path("arauna_dex_import/pokedex.json"))
    parser.add_argument("--sprites", type=Path, default=Path("arauna_dex_import/sprites"))
    parser.add_argument("--prepared", type=Path, default=Path("art_candidates"))
    parser.add_argument("--icon-palettes", type=Path, default=Path("engine-reference/graphics/pokemon/icon_palettes"))
    parser.add_argument("--out", type=Path, default=Path("art_candidates/full_dex/gba"))
    parser.add_argument("--previews", type=Path, default=Path("previews/full_dex"))
    parser.add_argument("--only", type=int, nargs="*")
    args = parser.parse_args()

    entries = json.loads(args.dex.read_text(encoding="utf-8"))["pokemon"]
    if len(entries) != 386 or [e["id"] for e in entries] != list(range(1, 387)):
        raise SystemExit("Dex must contain consecutive entries 001-386")
    prepared = prepared_lookup(args.prepared, args.out)
    selected = set(args.only or range(1, 387))
    rows = []
    for entry in entries:
        number = entry["id"]
        if number not in selected:
            continue
        folder = args.out / f"{number:03d}_{slugify(entry['name'])}"
        if number in prepared:
            profile = copy_prepared_package(prepared[number], folder, entry)
        else:
            filename = Path(entry.get("spriteFile") or "").name
            source = args.sprites / filename if filename and (args.sprites / filename).is_file() else None
            profile = build_package(entry, source, folder, args.icon_palettes)
        rows.append(profile)
        print(f"{number:03d}/386 {entry['name']}: {profile['productionMethod']}")

    if not args.only:
        sheets = contact_sheets(entries, args.out, args.previews)
        manifest = args.out.parent / "full_dex_art_manifest.csv"
        keys = ["dex", "name", "types", "status", "productionMethod", "referenceStatus", "frontPicBox", "backPicBox", "iconPalIndex", "visibleColors", "animation", "shiny"]
        with manifest.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=keys)
            writer.writeheader()
            for entry in entries:
                folder = args.out / f"{entry['id']:03d}_{slugify(entry['name'])}"
                row = json.loads((folder / "candidate_profile.json").read_text(encoding="utf-8"))
                writer.writerow({k: "/".join(map(str, row[k])) if isinstance(row.get(k), list) else row.get(k, "") for k in keys})
        print(f"complete: packages=386 manifest={manifest} sheets={len(sheets)}")


if __name__ == "__main__":
    main()

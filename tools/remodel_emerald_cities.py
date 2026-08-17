#!/usr/bin/env python3
"""Remodel Hoenn settlements with vanilla Emerald map resources only.

Story/progression invariants are stricter than visual similarity: map dimensions,
connections, scripts, events, warp destinations and collision/elevation at every
coordinate remain exactly as Emerald. Visual block composition and weather are
changed aggressively enough that each settlement acquires a distinct identity.
"""
from __future__ import annotations

import json
import random
import struct
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS_JSON = ROOT / "data/layouts/layouts.json"
MASK_COLLISION_ELEVATION = 0xFC00
MASK_METATILE = 0x03FF
MIN_VISUAL_CHANGE = 0.18

CITY_CONFIG = {
    "LittlerootTown": (101, "WEATHER_SUNNY_CLOUDS", "aldeia-jardim clara, compacta e acolhedora"),
    "OldaleTown": (103, "WEATHER_SUNNY", "entroncamento rural aberto e ensolarado"),
    "PetalburgCity": (102, "WEATHER_RAIN", "cidade-jardim úmida organizada em bairros"),
    "RustboroCity": (104, "WEATHER_SHADE", "centro urbano pétreo, denso e sombreado"),
    "DewfordTown": (106, "WEATHER_SUNNY_CLOUDS", "vila costeira compacta de brisa marítima"),
    "SlateportCity": (109, "WEATHER_SUNNY", "porto comercial amplo, luminoso e irregular"),
    "MauvilleCity": (110, "WEATHER_SUNNY_CLOUDS", "cruzamento urbano seco e movimentado"),
    "VerdanturfTown": (117, "WEATHER_FOG_HORIZONTAL", "vila verde de névoa baixa e jardins"),
    "FallarborTown": (113, "WEATHER_VOLCANIC_ASH", "povoado de cinzas vulcânicas e terreno áspero"),
    "LavaridgeTown": (112, "WEATHER_DROUGHT", "cidade termal quente, seca e mineral"),
    "FortreeCity": (119, "WEATHER_RAIN", "assentamento florestal chuvoso em plataformas"),
    "LilycoveCity": (121, "WEATHER_DOWNPOUR", "metrópole costeira em terraços sob chuva oceânica"),
    "MossdeepCity": (124, "WEATHER_SUNNY", "ilha tecnológica clara, espaçada e marítima"),
    "SootopolisCity": (126, "WEATHER_RAIN_THUNDERSTORM", "cidade-cratera dramática, vertical e tempestuosa"),
    "PacifidlogTown": (131, "WEATHER_RAIN", "aldeia flutuante chuvosa de passarelas"),
    "EverGrandeCity": (128, "WEATHER_FOG_HORIZONTAL", "santuário de altitude envolto em névoa"),
}


def layouts_by_id():
    data = json.loads(LAYOUTS_JSON.read_text(encoding="utf-8"))
    return {x["id"]: x for x in data["layouts"]}


def protect_square(out, width, height, x, y, radius=0):
    for yy in range(max(0, y-radius), min(height, y+radius+1)):
        for xx in range(max(0, x-radius), min(width, x+radius+1)):
            out.add((xx, yy))


def protected_cells(map_data, width, height):
    out = set()
    # Only the transition rim is frozen. This keeps every route connection exact.
    for y in range(height):
        for x in range(width):
            if x == 0 or y == 0 or x == width-1 or y == height-1:
                out.add((x, y))
    # Doors and scripted coordinates keep enough local visual context to remain readable.
    for e in map_data.get("warp_events", []):
        protect_square(out, width, height, int(e["x"]), int(e["y"]), 1)
    for e in map_data.get("coord_events", []):
        if "x" in e and "y" in e:
            protect_square(out, width, height, int(e["x"]), int(e["y"]), 1)
    for kind in ("bg_events", "object_events"):
        for e in map_data.get(kind, []):
            if "x" in e and "y" in e:
                protect_square(out, width, height, int(e["x"]), int(e["y"]), 0)
    return out


def collision(value):
    return value & MASK_COLLISION_ELEVATION


def shuffle_values(grid, groups, rng):
    moved = 0
    for indices in groups.values():
        if len(indices) < 2:
            continue
        values = [grid[i] for i in indices]
        rng.shuffle(values)
        if all(grid[i] == v for i, v in zip(indices, values)):
            values = values[1:] + values[:1]
        for i, value in zip(indices, values):
            if collision(grid[i]) != collision(value):
                raise RuntimeError("collision/elevation mismatch during remix")
            if grid[i] != value:
                moved += 1
            grid[i] = value
    return moved


def contextual_pass(grid, original, width, height, protected, rare_ids, rng):
    """Swap common visual blocks only among cells with the same physical context."""
    groups = defaultdict(list)
    def cmask(x, y):
        if x < 0 or y < 0 or x >= width or y >= height:
            return -1
        return collision(original[y*width+x])
    for y in range(1, height-1):
        for x in range(1, width-1):
            if (x, y) in protected:
                continue
            i = y*width+x
            if (original[i] & MASK_METATILE) in rare_ids:
                continue
            key = (collision(original[i]), cmask(x,y-1), cmask(x+1,y), cmask(x,y+1), cmask(x-1,y))
            groups[key].append(i)
    return shuffle_values(grid, groups, rng)


def common_role_pass(grid, original, width, height, protected, rare_ids, rng):
    """Stronger fallback: common blocks may move within the same collision/elevation role."""
    groups = defaultdict(list)
    for i, value in enumerate(original):
        x, y = i % width, i // width
        if (x, y) in protected or (value & MASK_METATILE) in rare_ids:
            continue
        groups[collision(value)].append(i)
    return shuffle_values(grid, groups, rng)


def chunk_pass(grid, original, width, height, protected, rare_ids, cw, ch, ox, oy, rng):
    """Move coherent micro-regions while keeping the physical mask at each coordinate."""
    groups = defaultdict(list)
    for y0 in range(1+oy, height-1-ch+1, ch):
        for x0 in range(1+ox, width-1-cw+1, cw):
            cells = [(x0+dx, y0+dy) for dy in range(ch) for dx in range(cw)]
            if any(c in protected for c in cells):
                continue
            idxs = [y*width+x for x,y in cells]
            if any((original[i] & MASK_METATILE) in rare_ids for i in idxs):
                continue
            signature = tuple(collision(original[i]) for i in idxs)
            groups[signature].append(idxs)
    moved = 0
    for chunks in groups.values():
        if len(chunks) < 2:
            continue
        payloads = [[grid[i] for i in idxs] for idxs in chunks]
        rng.shuffle(payloads)
        for idxs, values in zip(chunks, payloads):
            for i, value in zip(idxs, values):
                if collision(original[i]) != collision(value):
                    raise RuntimeError("chunk collision/elevation mismatch")
                if grid[i] != value:
                    moved += 1
                grid[i] = value
    return moved


def remodel_city(city, config, layouts):
    seed, weather, theme = config
    map_path = ROOT / f"data/maps/{city}/map.json"
    map_data = json.loads(map_path.read_text(encoding="utf-8"))
    original_map = json.loads(json.dumps(map_data))
    layout = layouts[map_data["layout"]]
    width, height = int(layout["width"]), int(layout["height"])
    block_path = ROOT / layout["blockdata_filepath"]
    raw = block_path.read_bytes()
    if len(raw) != width*height*2:
        raise RuntimeError(f"{city}: invalid blockdata size")
    original = list(struct.unpack(f"<{width*height}H", raw))
    grid = list(original)
    protected = protected_cells(map_data, width, height)
    frequencies = Counter(v & MASK_METATILE for v in original)
    rare_ids = {mid for mid, count in frequencies.items() if count <= 1}
    for i, value in enumerate(original):
        if (value & MASK_METATILE) in rare_ids:
            protected.add((i % width, i // width))

    rng = random.Random(seed)
    # Several offset chunk passes alter landscaping/architecture in coherent pieces.
    for cw, ch in ((3,3),(2,2),(2,1),(1,2),(2,2),(2,1)):
        for ox in range(min(cw, 2)):
            for oy in range(min(ch, 2)):
                chunk_pass(grid, original, width, height, protected, rare_ids, cw, ch, ox, oy, rng)
    # Context-aware visual remix greatly reduces resemblance without changing walkability.
    for _ in range(3):
        contextual_pass(grid, original, width, height, protected, rare_ids, rng)

    def changed_ratio():
        return sum(a != b for a,b in zip(original, grid)) / len(grid)
    # Small towns have few repeatable chunks; use common role pools only when needed.
    attempts = 0
    while changed_ratio() < MIN_VISUAL_CHANGE and attempts < 8:
        common_role_pass(grid, original, width, height, protected, rare_ids, rng)
        attempts += 1

    # Hard safety invariants.
    original_values = set(original)
    for i, (old, new) in enumerate(zip(original, grid)):
        if collision(old) != collision(new):
            raise RuntimeError(f"{city}: collision/elevation changed at {i}")
        if new not in original_values:
            raise RuntimeError(f"{city}: non-vanilla block introduced")
        x, y = i % width, i // width
        if (x, y) in protected and old != new:
            raise RuntimeError(f"{city}: protected coordinate changed at {x},{y}")
    ratio = changed_ratio()
    if ratio < MIN_VISUAL_CHANGE:
        raise RuntimeError(f"{city}: visual change only {ratio:.1%}; target is {MIN_VISUAL_CHANGE:.0%}")
    block_path.write_bytes(struct.pack(f"<{len(grid)}H", *grid))

    map_data["weather"] = weather
    a, b = dict(map_data), dict(original_map)
    a.pop("weather", None); b.pop("weather", None)
    if a != b:
        raise RuntimeError(f"{city}: map metadata other than weather changed")
    map_path.write_text(json.dumps(map_data, indent=2) + "\n", encoding="utf-8")
    changed = sum(a != b for a,b in zip(original, grid))
    return {"city":city,"theme":theme,"weather":weather,"changed":changed,"total":len(grid),"percent":100*ratio,"protected":len(protected)}


def write_manifest(results):
    docs = ROOT / "docs"; docs.mkdir(exist_ok=True)
    lines = [
        "# Remodelação das cidades — base Emerald", "",
        "A progressão, ordem de rotas, conexões, scripts, eventos, warps, dimensões e geometria física de Pokémon Emerald permanecem intactas.", "",
        "A composição visual foi remixada somente com blocos/metatiles já presentes no próprio mapa vanilla; nenhum gráfico externo foi adicionado.", "",
        "| Cidade | Identidade | Clima | Composição visual alterada |", "|---|---|---|---:|",
    ]
    for r in results:
        lines.append(f"| {r['city']} | {r['theme']} | `{r['weather']}` | {r['changed']}/{r['total']} ({r['percent']:.1f}%) |")
    lines += ["", "## Invariantes verificadas automaticamente", "", "- ordem e conexões de progressão do Emerald preservadas;", "- warps, object events, coord events, bg events e scripts preservados;", "- colisão e elevação preservadas bit a bit em todas as coordenadas;", "- bordas, portas e coordenadas sensíveis preservadas;", "- somente blocos existentes no mapa vanilla são reutilizados;", "- em `map.json`, somente `weather` é alterado;", f"- nenhuma cidade pode ficar abaixo de {MIN_VISUAL_CHANGE:.0%} de composição visual alterada.", ""]
    (docs / "EMERALD_CITY_REMODEL.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    layouts = layouts_by_id()
    results = [remodel_city(city, cfg, layouts) for city, cfg in CITY_CONFIG.items()]
    write_manifest(results)
    for r in results:
        print(f"{r['city']}: {r['percent']:.1f}% changed, weather={r['weather']}")

if __name__ == "__main__":
    main()

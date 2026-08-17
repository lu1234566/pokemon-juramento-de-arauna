#!/usr/bin/env python3
"""Remodel Hoenn settlements using only metatiles already present in vanilla Emerald.

Design constraints:
- Keep map dimensions, connections, warps, triggers, scripts, collision and elevation intact.
- Never import external graphics or new metatile IDs.
- Rearrange coherent micro-regions only when their collision/elevation masks match.
- Protect borders and all event-sensitive coordinates.
- Give every settlement a deliberate climate using weather already implemented by Emerald.
"""
from __future__ import annotations

import json
import random
import struct
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS_JSON = ROOT / "data/layouts/layouts.json"

CITY_CONFIG = {
    "LittlerootTown": {"seed": 101, "weather": "WEATHER_SUNNY_CLOUDS", "passes": [(3, 3), (2, 2), (2, 1)], "theme": "aldeia-jardim clara, compacta e acolhedora"},
    "OldaleTown": {"seed": 103, "weather": "WEATHER_SUNNY", "passes": [(2, 2), (1, 2), (2, 1)], "theme": "entroncamento rural aberto e ensolarado"},
    "PetalburgCity": {"seed": 102, "weather": "WEATHER_RAIN", "passes": [(3, 3), (3, 2), (2, 2)], "theme": "cidade-jardim úmida organizada em bairros"},
    "RustboroCity": {"seed": 104, "weather": "WEATHER_SHADE", "passes": [(4, 3), (3, 2), (2, 2)], "theme": "centro urbano pétreo, denso e sombreado"},
    "DewfordTown": {"seed": 106, "weather": "WEATHER_SUNNY_CLOUDS", "passes": [(2, 2), (1, 2), (2, 1)], "theme": "vila costeira compacta de brisa marítima"},
    "SlateportCity": {"seed": 109, "weather": "WEATHER_SUNNY", "passes": [(4, 3), (3, 2), (2, 2)], "theme": "porto comercial amplo, luminoso e irregular"},
    "MauvilleCity": {"seed": 110, "weather": "WEATHER_SUNNY_CLOUDS", "passes": [(3, 2), (2, 2), (2, 1)], "theme": "cruzamento urbano seco e movimentado"},
    "VerdanturfTown": {"seed": 117, "weather": "WEATHER_FOG_HORIZONTAL", "passes": [(2, 2), (1, 2), (2, 1)], "theme": "vila verde de névoa baixa e jardins"},
    "FallarborTown": {"seed": 113, "weather": "WEATHER_VOLCANIC_ASH", "passes": [(2, 2), (1, 2), (2, 1)], "theme": "povoado de cinzas vulcânicas e terreno áspero"},
    "LavaridgeTown": {"seed": 112, "weather": "WEATHER_DROUGHT", "passes": [(2, 2), (2, 1), (1, 2)], "theme": "cidade termal quente, seca e mineral"},
    "FortreeCity": {"seed": 119, "weather": "WEATHER_RAIN", "passes": [(3, 2), (2, 2), (2, 1)], "theme": "assentamento florestal chuvoso em plataformas"},
    "LilycoveCity": {"seed": 121, "weather": "WEATHER_DOWNPOUR", "passes": [(4, 4), (3, 2), (2, 2)], "theme": "metrópole costeira em terraços sob chuva oceânica"},
    "MossdeepCity": {"seed": 124, "weather": "WEATHER_SUNNY", "passes": [(4, 3), (3, 2), (2, 2)], "theme": "ilha tecnológica clara, espaçada e marítima"},
    "SootopolisCity": {"seed": 126, "weather": "WEATHER_RAIN_THUNDERSTORM", "passes": [(4, 3), (3, 3), (2, 2)], "theme": "cidade-cratera dramática, vertical e tempestuosa"},
    "PacifidlogTown": {"seed": 131, "weather": "WEATHER_RAIN", "passes": [(2, 2), (1, 2), (2, 1)], "theme": "aldeia flutuante chuvosa de passarelas"},
    "EverGrandeCity": {"seed": 128, "weather": "WEATHER_FOG_HORIZONTAL", "passes": [(4, 3), (3, 2), (2, 2)], "theme": "santuário de altitude envolto em névoa"},
}

MASK_COLLISION_ELEVATION = 0xFC00
MASK_METATILE = 0x03FF


def load_layout_table():
    data = json.loads(LAYOUTS_JSON.read_text(encoding="utf-8"))
    return {entry["id"]: entry for entry in data["layouts"]}


def protect_square(protected, width, height, x, y, radius):
    for yy in range(max(0, y - radius), min(height, y + radius + 1)):
        for xx in range(max(0, x - radius), min(width, x + radius + 1)):
            protected.add((xx, yy))


def protected_cells(map_data, width, height):
    protected = set()
    # Connections and edge transitions are sacrosanct.
    border = 3
    for y in range(height):
        for x in range(width):
            if x < border or y < border or x >= width - border or y >= height - border:
                protected.add((x, y))

    for event in map_data.get("warp_events", []):
        protect_square(protected, width, height, int(event["x"]), int(event["y"]), 3)
    for event in map_data.get("coord_events", []):
        if "x" in event and "y" in event:
            protect_square(protected, width, height, int(event["x"]), int(event["y"]), 2)
    for event in map_data.get("bg_events", []):
        if "x" in event and "y" in event:
            protect_square(protected, width, height, int(event["x"]), int(event["y"]), 1)
    for event in map_data.get("object_events", []):
        if "x" in event and "y" in event:
            radius = 1 + max(int(event.get("movement_range_x", 0)), int(event.get("movement_range_y", 0)))
            protect_square(protected, width, height, int(event["x"]), int(event["y"]), min(radius, 3))
    return protected


def chunk_cells(x0, y0, cw, ch):
    return [(x0 + dx, y0 + dy) for dy in range(ch) for dx in range(cw)]


def apply_chunk_pass(grid, width, height, protected, cw, ch, rng):
    groups = defaultdict(list)
    for y0 in range(3, height - 3 - ch + 1, ch):
        for x0 in range(3, width - 3 - cw + 1, cw):
            cells = chunk_cells(x0, y0, cw, ch)
            if any(cell in protected for cell in cells):
                continue
            values = tuple(grid[y * width + x] for x, y in cells)
            # Rare/special metatiles are intentionally left anchored.
            signature = tuple(value & MASK_COLLISION_ELEVATION for value in values)
            groups[signature].append((cells, values))

    before = list(grid)
    moved = 0
    for chunks in groups.values():
        if len(chunks) < 2:
            continue
        order = list(range(len(chunks)))
        rng.shuffle(order)
        if order == list(range(len(chunks))):
            order = order[1:] + order[:1]
        for dst_idx, src_idx in enumerate(order):
            dst_cells, _ = chunks[dst_idx]
            _, src_values = chunks[src_idx]
            for (x, y), value in zip(dst_cells, src_values):
                idx = y * width + x
                # Signature equality guarantees collision/elevation stay identical.
                if (grid[idx] & MASK_COLLISION_ELEVATION) != (value & MASK_COLLISION_ELEVATION):
                    raise RuntimeError("collision/elevation signature mismatch")
                if grid[idx] != value:
                    moved += 1
                grid[idx] = value

    # Absolute safety invariant for this pass.
    for old, new in zip(before, grid):
        if (old & MASK_COLLISION_ELEVATION) != (new & MASK_COLLISION_ELEVATION):
            raise RuntimeError("collision/elevation changed")
    return moved


def remodel_city(city, config, layouts):
    map_path = ROOT / f"data/maps/{city}/map.json"
    map_data = json.loads(map_path.read_text(encoding="utf-8"))
    original_map_data = json.loads(json.dumps(map_data))

    layout = layouts[map_data["layout"]]
    width, height = int(layout["width"]), int(layout["height"])
    block_path = ROOT / layout["blockdata_filepath"]
    raw = block_path.read_bytes()
    if len(raw) != width * height * 2:
        raise RuntimeError(f"{city}: unexpected blockdata size {len(raw)} for {width}x{height}")

    original = list(struct.unpack(f"<{width * height}H", raw))
    grid = list(original)
    protected = protected_cells(map_data, width, height)

    # Protect rare metatiles globally: doors, specialty signs, stairs, ledges and one-offs
    # tend to fall into this category, so they remain exactly where Emerald put them.
    freq = defaultdict(int)
    for value in original:
        freq[value & MASK_METATILE] += 1
    rare_ids = {mid for mid, count in freq.items() if count <= 3}
    for idx, value in enumerate(original):
        if (value & MASK_METATILE) in rare_ids:
            protected.add((idx % width, idx // width))

    rng = random.Random(config["seed"])
    moved_total = 0
    for cw, ch in config["passes"]:
        moved_total += apply_chunk_pass(grid, width, height, protected, cw, ch, rng)

    # Final hard invariants: story-sensitive cells and physical map geometry remain unchanged.
    for x, y in protected:
        idx = y * width + x
        if grid[idx] != original[idx]:
            raise RuntimeError(f"{city}: protected cell changed at {x},{y}")
    for idx, (old, new) in enumerate(zip(original, grid)):
        if (old & MASK_COLLISION_ELEVATION) != (new & MASK_COLLISION_ELEVATION):
            raise RuntimeError(f"{city}: collision/elevation changed at index {idx}")
        if new not in original:
            raise RuntimeError(f"{city}: introduced a metatile entry not present in vanilla map")

    changed = sum(1 for a, b in zip(original, grid) if a != b)
    block_path.write_bytes(struct.pack(f"<{len(grid)}H", *grid))

    map_data["weather"] = config["weather"]
    check = dict(map_data)
    old_check = dict(original_map_data)
    check.pop("weather", None)
    old_check.pop("weather", None)
    if check != old_check:
        raise RuntimeError(f"{city}: map metadata other than weather changed")
    map_path.write_text(json.dumps(map_data, indent=2) + "\n", encoding="utf-8")

    return {
        "city": city,
        "theme": config["theme"],
        "weather": config["weather"],
        "width": width,
        "height": height,
        "changed": changed,
        "total": len(grid),
        "percent": 100.0 * changed / len(grid),
        "protected": len(protected),
        "moved_operations": moved_total,
    }


def write_manifest(results):
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    lines = [
        "# Remodelação das cidades — base Emerald",
        "",
        "Princípio: a ordem de progressão de Pokémon Emerald permanece intacta. Conexões entre mapas, warps, triggers, scripts, dimensões, colisão e elevação não são alterados.",
        "",
        "Os layouts abaixo foram remixados exclusivamente com entradas de metatile que já existiam no próprio mapa vanilla. Nenhum tileset, sprite, paleta ou gráfico externo foi introduzido.",
        "",
        "| Cidade | Identidade | Clima | Blocos alterados |",
        "|---|---|---|---:|",
    ]
    for r in results:
        lines.append(f"| {r['city']} | {r['theme']} | `{r['weather']}` | {r['changed']}/{r['total']} ({r['percent']:.1f}%) |")
    lines += [
        "",
        "## Invariantes verificadas automaticamente",
        "",
        "- dimensões de cada mapa preservadas;",
        "- conexões de rota preservadas;",
        "- warps, object events, coord events e bg events preservados;",
        "- colisão e elevação de cada coordenada preservadas bit a bit;",
        "- células sensíveis a eventos e bordas preservadas integralmente;",
        "- somente metatiles já presentes no mapa vanilla podem aparecer no resultado;",
        "- a única alteração em `map.json` é o campo `weather`.",
        "",
    ]
    (docs / "EMERALD_CITY_REMODEL.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    layouts = load_layout_table()
    results = []
    for city, config in CITY_CONFIG.items():
        results.append(remodel_city(city, config, layouts))
    write_manifest(results)
    for r in results:
        print(f"{r['city']}: {r['changed']}/{r['total']} blocks changed ({r['percent']:.1f}%), weather={r['weather']}")


if __name__ == "__main__":
    main()

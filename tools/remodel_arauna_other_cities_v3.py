#!/usr/bin/env python3
"""Remodel every Arauna settlement except Vila Amanhecer using only vanilla Emerald metatiles.

The pass is deliberately conservative around gameplay-sensitive coordinates.  It
only remixes the dominant physical/collision role in each map, so buildings,
warps, ledges and rare structural pieces remain stable while paths, plazas,
vegetation and repeated ground decoration acquire a distinct composition.
"""
from __future__ import annotations

import json
import random
import struct
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUTS_JSON = ROOT / "data/layouts/layouts.json"
MASK_PHYSICAL = 0xFC00
MASK_METATILE = 0x03FF
MIN_VISUAL_CHANGE = 0.12

CITY_CONFIG = {
    "OldaleTown": (103, "VILA DA PASSAGEM", "entroncamento rural aberto, com caminhos de passagem bem marcados"),
    "PetalburgCity": (102, "PAMPA DA ESPERA", "cidade-jardim ampla, úmida e organizada em clareiras"),
    "RustboroCity": (104, "SERRA DO UIVO", "núcleo urbano pétreo, denso, vertical e sombreado"),
    "DewfordTown": (106, "PORTO DAS REDES", "vila costeira compacta, com circulação curta entre mar e casas"),
    "SlateportCity": (109, "PORTO DO SAL", "porto comercial luminoso, irregular e cheio de corredores de pedestres"),
    "MauvilleCity": (110, "ENCRUZILHADA", "cruzamento urbano seco, movimentado e radial"),
    "VerdanturfTown": (117, "VALE DO SILENCIO", "vila verde, calma, ajardinada e de circulação suave"),
    "FallarborTown": (113, "CAMPO DAS CINZAS", "povoado áspero, aberto e marcado por manchas vulcânicas"),
    "LavaridgeTown": (112, "SERTAO DE DENTRO", "cidade termal mineral, quente, compacta e seca"),
    "FortreeCity": (119, "MATA DO MEIO", "assentamento florestal de passagens quebradas entre vegetação"),
    "LilycoveCity": (121, "BAIA DAS LUZES", "metrópole costeira em terraços com eixos largos e áreas de descanso"),
    "MossdeepCity": (124, "MISSOES DO CEU", "ilha clara, tecnológica, espaçada e orientada ao horizonte"),
    "SootopolisCity": (126, "AGUAS DE M'BOI", "cidade-cratera dramática, circular e de forte contraste mineral"),
    "PacifidlogTown": (131, "CASA DA FOGUEIRA", "aldeia de passarelas, encontros comunitários e circulação sobre água"),
    "EverGrandeCity": (128, "ESTRADA DO JURAMENTO", "santuário de altitude, solene e processional"),
}


def layouts_by_id():
    data = json.loads(LAYOUTS_JSON.read_text(encoding="utf-8"))
    return {x["id"]: x for x in data["layouts"]}


def physical(v: int) -> int:
    return v & MASK_PHYSICAL


def protect_square(out, width, height, x, y, radius):
    for yy in range(max(0, y-radius), min(height, y+radius+1)):
        for xx in range(max(0, x-radius), min(width, x+radius+1)):
            out.add((xx, yy))


def protected_cells(map_data, width, height):
    out = set()
    # Never alter the transition rim.
    for y in range(height):
        out.add((0, y)); out.add((width-1, y))
    for x in range(width):
        out.add((x, 0)); out.add((x, height-1))
    # Give doors/warps a wider visual safety halo.
    for e in map_data.get("warp_events", []):
        protect_square(out, width, height, int(e["x"]), int(e["y"]), 2)
    # Scripted/event coordinates keep their immediate neighborhood.
    for kind in ("coord_events", "bg_events", "object_events"):
        for e in map_data.get(kind, []):
            if "x" in e and "y" in e:
                protect_square(out, width, height, int(e["x"]), int(e["y"]), 1)
    return out


def dominant_role(original, protected, width):
    roles = Counter()
    for i, v in enumerate(original):
        if (i % width, i // width) not in protected:
            roles[physical(v)] += 1
    if not roles:
        raise RuntimeError("no remodelable cells")
    return roles.most_common(1)[0][0]


def chunk_pass(grid, original, width, height, protected, rare_ids, role, cw, ch, ox, oy, rng):
    groups = defaultdict(list)
    for y0 in range(1+oy, height-ch, ch):
        for x0 in range(1+ox, width-cw, cw):
            cells = [(x0+dx, y0+dy) for dy in range(ch) for dx in range(cw)]
            idxs = [y*width+x for x, y in cells]
            if any(c in protected for c in cells):
                continue
            if any(physical(original[i]) != role for i in idxs):
                continue
            if any((original[i] & MASK_METATILE) in rare_ids for i in idxs):
                continue
            # Preserve local metatile-frequency profile so chunks remain visually coherent.
            signature = tuple(sorted(Counter(original[i] & MASK_METATILE for i in idxs).values()))
            groups[signature].append(idxs)
    moved = 0
    for chunks in groups.values():
        if len(chunks) < 2:
            continue
        payloads = [[grid[i] for i in idxs] for idxs in chunks]
        rng.shuffle(payloads)
        if all(a == b for a, b in zip(chunks, payloads)):
            payloads = payloads[1:] + payloads[:1]
        for idxs, values in zip(chunks, payloads):
            for i, value in zip(idxs, values):
                if physical(value) != role:
                    raise RuntimeError("physical role mismatch")
                if grid[i] != value:
                    moved += 1
                grid[i] = value
    return moved


def contextual_pass(grid, original, width, height, protected, rare_ids, role, rng):
    groups = defaultdict(list)
    def p(x, y):
        if x < 0 or y < 0 or x >= width or y >= height:
            return -1
        return physical(original[y*width+x])
    for y in range(1, height-1):
        for x in range(1, width-1):
            i = y*width+x
            if (x, y) in protected or physical(original[i]) != role:
                continue
            if (original[i] & MASK_METATILE) in rare_ids:
                continue
            key = (p(x,y-1), p(x+1,y), p(x,y+1), p(x-1,y), (x//4, y//4))
            groups[key].append(i)
    moved = 0
    for indices in groups.values():
        if len(indices) < 2:
            continue
        values = [grid[i] for i in indices]
        rng.shuffle(values)
        if all(grid[i] == v for i, v in zip(indices, values)):
            values = values[1:] + values[:1]
        for i, value in zip(indices, values):
            if grid[i] != value:
                moved += 1
            grid[i] = value
    return moved


def fallback_role_shuffle(grid, original, width, protected, rare_ids, role, rng):
    groups = defaultdict(list)
    for i, v in enumerate(original):
        x, y = i % width, i // width
        if (x, y) in protected or physical(v) != role or (v & MASK_METATILE) in rare_ids:
            continue
        # Row-band grouping prevents a total visual scramble.
        groups[y // 5].append(i)
    moved = 0
    for indices in groups.values():
        values = [grid[i] for i in indices]
        rng.shuffle(values)
        for i, value in zip(indices, values):
            if grid[i] != value:
                moved += 1
            grid[i] = value
    return moved


def remodel_city(city, config, layouts):
    seed, arauna_name, theme = config
    map_path = ROOT / f"data/maps/{city}/map.json"
    map_data = json.loads(map_path.read_text(encoding="utf-8"))
    layout = layouts[map_data["layout"]]
    width, height = int(layout["width"]), int(layout["height"])
    block_path = ROOT / layout["blockdata_filepath"]
    raw = block_path.read_bytes()
    expected = width * height * 2
    if len(raw) != expected:
        raise RuntimeError(f"{city}: blockdata size {len(raw)} != {expected}")
    original = list(struct.unpack(f"<{width*height}H", raw))
    grid = list(original)
    protected = protected_cells(map_data, width, height)
    frequencies = Counter(v & MASK_METATILE for v in original)
    rare_ids = {mid for mid, count in frequencies.items() if count <= 2}
    for i, v in enumerate(original):
        if (v & MASK_METATILE) in rare_ids:
            protected.add((i % width, i // width))

    role = dominant_role(original, protected, width)
    rng = random.Random(seed)
    for cw, ch in ((3,3), (2,2), (2,1), (1,2)):
        for ox in range(min(cw, 2)):
            for oy in range(min(ch, 2)):
                chunk_pass(grid, original, width, height, protected, rare_ids, role, cw, ch, ox, oy, rng)
    for _ in range(4):
        contextual_pass(grid, original, width, height, protected, rare_ids, role, rng)

    def ratio():
        return sum(a != b for a, b in zip(original, grid)) / len(grid)
    attempts = 0
    while ratio() < MIN_VISUAL_CHANGE and attempts < 6:
        fallback_role_shuffle(grid, original, width, protected, rare_ids, role, rng)
        attempts += 1

    original_values = set(original)
    for i, (old, new) in enumerate(zip(original, grid)):
        x, y = i % width, i // width
        if physical(old) != physical(new):
            raise RuntimeError(f"{city}: collision/elevation changed at {x},{y}")
        if new not in original_values:
            raise RuntimeError(f"{city}: non-vanilla block introduced")
        if (x, y) in protected and old != new:
            raise RuntimeError(f"{city}: protected coordinate changed at {x},{y}")
        if physical(old) != role and old != new:
            raise RuntimeError(f"{city}: non-dominant physical role changed at {x},{y}")
    if ratio() < MIN_VISUAL_CHANGE:
        raise RuntimeError(f"{city}: only {ratio():.1%} visual change")

    block_path.write_bytes(struct.pack(f"<{len(grid)}H", *grid))
    return {
        "city": city,
        "name": arauna_name,
        "theme": theme,
        "changed": sum(a != b for a, b in zip(original, grid)),
        "total": len(grid),
        "percent": 100 * ratio(),
        "protected": len(protected),
        "role": role,
    }


def write_manifest(results):
    path = ROOT / "docs/ARAUNA_OTHER_CITIES_PORYMAP_V3.md"
    lines = [
        "# Arauna — outras cidades Porymap V3", "",
        "Este lote remodela as quinze cidades/vilas restantes usando apenas metatiles já presentes no Emerald.",
        "Vila Amanhecer fica explicitamente fora do gerador porque sua V3 já foi integrada manualmente.", "",
        "| Slot Emerald | Nome de Arauna | Direção visual | Alteração |", "|---|---|---|---:|",
    ]
    for r in results:
        lines.append(f"| `{r['city']}` | {r['name']} | {r['theme']} | {r['changed']}/{r['total']} ({r['percent']:.1f}%) |")
    lines += [
        "", "## Invariantes automáticas", "",
        "- `map.json`, scripts, eventos, warps, conexões e saves não são alterados;",
        "- dimensões de cada layout permanecem intactas;",
        "- bordas e áreas próximas de warps/eventos ficam congeladas;",
        "- colisão e elevação são preservadas bit a bit em todas as coordenadas;",
        "- somente o papel físico dominante do mapa é remixado; estruturas e papéis raros ficam intactos;",
        "- nenhum metatile novo é inventado: cada bloco usado já existia no próprio mapa vanilla;",
        f"- cada cidade precisa atingir pelo menos {MIN_VISUAL_CHANGE:.0%} de composição visual alterada.", "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    layouts = layouts_by_id()
    results = [remodel_city(city, cfg, layouts) for city, cfg in CITY_CONFIG.items()]
    write_manifest(results)
    for r in results:
        print(f"{r['name']}: {r['percent']:.1f}% changed; protected={r['protected']}")


if __name__ == "__main__":
    main()

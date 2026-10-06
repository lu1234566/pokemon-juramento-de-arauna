#!/usr/bin/env python3
"""Variantes Arauna dos layouts trocados por script (setmaplayoutindex).

Mirage Tower, Ilha Miragem, Sky Pillar, marés da Shoal Cave e o Sky Pillar
"limpo" trocam o layout do mapa por uma variante. As variantes do repo são as
vanilla, com os bancos de Hoenn, e o mapa Arauna voltava ao visual original.

As marés da Shoal Cave já têm variantes Arauna próprias
(LAYOUT_ARAUNA_MARE_HIGHTIDE*_V1, com bancos de maré alta) e não entram aqui.

Cada variante Arauna é o layout Arauna atual com as células que o vanilla muda
entre a base e a variante copiadas da variante vanilla (ID, colisão e
elevação). Nessas áreas o layout Arauna repete os IDs da base vanilla, e os
bancos Arauna dão a esses IDs a mesma conduta da variante (conferido por
--verificar). Os layouts novos entram no fim de layouts.json.

uso: variantes_troca_layout.py [--verificar]
"""
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAYOUTS = ROOT / "data/layouts/layouts.json"

# (base vanilla, variante vanilla, layout Arauna, novo id, nova pasta)
VARIANTES = [
    ("LAYOUT_ROUTE111", "LAYOUT_ROUTE111_NO_MIRAGE_TOWER",
     "LAYOUT_ARAUNA_ROUTE111_THREE_ACTS_V1", "LAYOUT_ARAUNA_ROUTE111_THREE_ACTS_NO_TOWER_V1",
     "Route111_AraunaThreeActsNoTower"),
    ("LAYOUT_ROUTE130", "LAYOUT_ROUTE130_MIRAGE_ISLAND",
     "LAYOUT_ARAUNA_ROUTE130_CROSS_CURRENTS_V1", "LAYOUT_ARAUNA_ROUTE130_CROSS_CURRENTS_MIRAGE_ISLAND_V1",
     "Route130_AraunaCrossCurrentsMirageIsland"),
    ("LAYOUT_ROUTE131", "LAYOUT_ROUTE131_SKY_PILLAR",
     "LAYOUT_ARAUNA_ROUTE131_LAST_FREE_SEA_V1", "LAYOUT_ARAUNA_ROUTE131_LAST_FREE_SEA_SKY_PILLAR_V1",
     "Route131_AraunaLastFreeSeaSkyPillar"),
] + [
    ("LAYOUT_SKY_PILLAR_%s" % f, "LAYOUT_SKY_PILLAR_%s_CLEAN" % f,
     "LAYOUT_ARAUNA_TORRE_%s_V1" % f, "LAYOUT_ARAUNA_TORRE_%s_CLEAN_V1" % f,
     "AraunaTorre_%sClean" % {"TOP": "Top"}.get(f, f))
    for f in ["1F", "2F", "3F", "4F", "5F", "TOP"]
]


def grade(layout):
    data = (ROOT / layout["blockdata_filepath"]).read_bytes()
    return [b for (b,) in struct.iter_unpack("<H", data)]


def comportamentos():
    hdr = (ROOT / "src/data/tilesets/headers.h").read_text()
    meta = (ROOT / "src/data/tilesets/metatiles.h").read_text()
    cache = {}

    def attrs(name):
        if name not in cache:
            blk = re.search(r"const struct Tileset %s =\s*\{(.*?)\};" % name, hdr, re.S).group(1)
            sym = re.search(r"\.metatileAttributes\s*=\s*(\w+)", blk).group(1)
            path = re.search(r'%s\[\] = INCBIN_U16\("([^"]+)"' % sym, meta).group(1)
            data = (ROOT / path).read_bytes()
            cache[name] = struct.unpack("<%dH" % (len(data) // 2), data)
        return cache[name]

    def mb(layout, metatile):
        if metatile < 0x200:
            a = attrs(layout["primary_tileset"])
            return a[metatile] & 0xFF if metatile < len(a) else None
        a = attrs(layout["secondary_tileset"])
        i = metatile - 0x200
        return a[i] & 0xFF if i < len(a) else None
    return mb


def main():
    verificar = "--verificar" in sys.argv
    doc = json.loads(LAYOUTS.read_text())
    por_id = {l["id"]: l for l in doc["layouts"] if l}
    mb = comportamentos()
    erros = 0
    for base_id, var_id, arauna_id, novo_id, pasta in VARIANTES:
        base, var, arauna = por_id[base_id], por_id[var_id], por_id[arauna_id]
        assert (base["width"], base["height"]) == (var["width"], var["height"]) == (arauna["width"], arauna["height"]), arauna_id
        B, V, A = grade(base), grade(var), grade(arauna)
        mudam = [i for i in range(len(B)) if B[i] != V[i]]
        novo = list(A)
        for i in mudam:
            novo[i] = V[i]
        divergem = sum(1 for i in mudam if mb(var, V[i] & 0x3FF) != mb(arauna, V[i] & 0x3FF))
        erros += divergem
        destino = ROOT / "data/layouts" / pasta / "map.bin"
        dados = struct.pack("<%dH" % len(novo), *novo)
        registro = {
            "id": novo_id,
            "name": pasta + "_Layout",
            "width": arauna["width"],
            "height": arauna["height"],
            "primary_tileset": arauna["primary_tileset"],
            "secondary_tileset": arauna["secondary_tileset"],
            "border_filepath": arauna["border_filepath"],
            "blockdata_filepath": "data/layouts/%s/map.bin" % pasta,
        }
        if verificar:
            ok = destino.exists() and destino.read_bytes() == dados and por_id.get(novo_id) == registro
            print("%-55s %s  células trocadas %4d  comportamento divergente %d"
                  % (novo_id, "ok" if ok else "DESATUALIZADO", len(mudam), divergem))
            erros += 0 if ok else 1
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(dados)
        if novo_id in por_id:
            doc["layouts"][doc["layouts"].index(por_id[novo_id])] = registro
        else:
            doc["layouts"].append(registro)
        por_id[novo_id] = registro
        print("%-55s células trocadas %4d  comportamento divergente %d" % (novo_id, len(mudam), divergem))
    if not verificar:
        LAYOUTS.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()

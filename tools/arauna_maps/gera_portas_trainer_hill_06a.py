#!/usr/bin/env python3
"""Gera as animações das portas de elevador do Trainer Hill para os bancos 06A.

A animação de porta de 16x32 redesenha o metatile da porta e o de cima só com a
camada de baixo. Os bancos do pavilhão redesenharam a parede acima das duas
portas, mas a animação nativa continuava pintando a parede de Hoenn: durante a
abertura aparecia um bloco branco (saguão) ou verde-água (cobertura).

Cada quadro novo é o desenho parado do banco novo, com os pixels que a animação
nativa muda (as folhas da porta) copiados dela. Cada tile 8x8 recebe a paleta do
banco que o reproduz com menor erro. A parede e a moldura saem exatas; na faixa
em que o friso novo (paleta 12, cheia) encontra a folha da porta, o interior da
porta usa a cor mais próxima da paleta 12. Uso, na raiz do repositório:

    python3 tools/arauna_maps/gera_portas_trainer_hill_06a.py
"""
import json
import struct
from pathlib import Path

from PIL import Image

from render_native_map import ROOT, Renderer, indexed_tiles, resolve_tileset

PORTAS = (
    # saída, mapa, (x, y) da porta, png nativo, paletas nativas por tile
    ("arauna_trainer_hill_lobby_elevator", "TrainerHill_Entrance", (17, 8),
     "trainer_hill_lobby_elevator", (7, 7, 7, 7, 7, 7, 7, 7)),
    ("arauna_trainer_hill_roof_elevator", "TrainerHill_Roof", (15, 5),
     "trainer_hill_roof_elevator", (9, 9, 7, 7, 7, 7, 7, 7)),
)
ORIGINAL = ("gTileset_Building", "gTileset_TrainerHill")


def banco(primario, secundario):
    return Renderer(resolve_tileset(primario), resolve_tileset(secundario))


def parado(r, acima, porta):
    fundo = r.palettes[0][0]
    out = Image.new("RGB", (16, 32))
    for i, mid in enumerate((acima, porta)):
        t = Image.new("RGBA", (16, 16), fundo + (255,))
        t.alpha_composite(r.metatile(mid))
        out.paste(t.convert("RGB"), (0, i * 16))
    return out


def quadro(r, indices, larg, n, paletas):
    """Quadro n da animação nativa, em RGB, como o jogo o desenha."""
    fundo = r.palettes[0][0]
    out = Image.new("RGB", (16, 32))
    for t in range(8):
        pal = r.palettes[paletas[t]]
        tx, ty = (t % 2) * 8, (t // 2) * 8
        for y in range(8):
            for x in range(8):
                c = indices[(n * 32 + ty + y) * larg + tx + x] & 15
                out.putpixel((tx + x, ty + y), pal[c] if c else fundo)
    return out


def quantiza(r, rgb):
    """Uma paleta por tile 8x8; devolve índices e paletas."""
    fundo = r.palettes[0][0]
    idx = Image.new("P", rgb.size)
    paletas = []
    for t in range(rgb.width // 8 * (rgb.height // 8)):
        tx, ty = (t % 2) * 8, (t // 2) * 8
        px = [rgb.getpixel((tx + x, ty + y)) for y in range(8) for x in range(8)]
        melhor = None
        for p, pal in enumerate(r.palettes):
            erro, escolha = 0, []
            for c in px:
                if c == fundo:
                    escolha.append(0)
                    continue
                k = min(range(1, 16), key=lambda i: sum(abs(a - b) for a, b in zip(pal[i], c)))
                erro += sum(abs(a - b) for a, b in zip(pal[k], c))
                escolha.append(k)
            if melhor is None or erro < melhor[0]:
                melhor = (erro, p, escolha)
        erro, p, escolha = melhor
        paletas.append(p)
        for i, k in enumerate(escolha):
            idx.putpixel((tx + i % 8, ty + i // 8), k)
    return idx, paletas


def cor_pixel(r, idx, paletas, x, y):
    """Cor que o jogo mostra no pixel (x, y) do quadro quantizado."""
    k = idx.getpixel((x, y))
    return r.palettes[0][0] if k == 0 else r.palettes[paletas[(y // 8) * 2 + x // 8]][k]


def main():
    layouts = {l["id"]: l for l in json.loads((ROOT / "data/layouts/layouts.json").read_text())["layouts"] if l}
    velho = banco(*ORIGINAL)
    cinza = [v for i in range(16) for v in (255 - i * 17,) * 3]
    for saida, mapa, (x, y), nativo, paletas in PORTAS:
        lay = layouts[json.loads((ROOT / f"data/maps/{mapa}/map.json").read_text())["layout"]]
        raw = (ROOT / lay["blockdata_filepath"]).read_bytes()
        grade = struct.unpack(f"<{len(raw) // 2}H", raw)
        largura = lay["width"]
        acima, porta = grade[(y - 1) * largura + x] & 0x3FF, grade[y * largura + x] & 0x3FF
        novo = banco(lay["primary_tileset"], lay["secondary_tileset"])
        img = Image.open(ROOT / f"graphics/door_anims/{nativo}.png")
        indices, larg = list(img.get_flattened_data()), img.width
        antes, depois = parado(velho, acima, porta), parado(novo, acima, porta)
        folha = Image.new("P", (16, img.height))
        usadas = None
        for n in range(img.height // 32):
            original = quadro(velho, indices, larg, n, paletas)
            alvo = depois.copy()
            folha_porta = set()
            for py in range(32):
                for px in range(16):
                    if original.getpixel((px, py)) != antes.getpixel((px, py)):
                        alvo.putpixel((px, py), original.getpixel((px, py)))
                        folha_porta.add((px, py))
            idx, pals = quantiza(novo, alvo)
            for py in range(32):
                for px in range(16):
                    cor = cor_pixel(novo, idx, pals, px, py)
                    erro = sum(abs(a - b) for a, b in zip(cor, alvo.getpixel((px, py))))
                    # parede e moldura exatas; folha da porta com desvio pequeno
                    assert erro <= (60 if (px, py) in folha_porta else 0), (saida, n, px, py, erro)
            assert usadas in (None, pals), (saida, "paletas mudam entre quadros")
            usadas = pals
            folha.paste(idx, (0, n * 32))
        folha.putpalette(cinza)
        folha.save(ROOT / f"graphics/door_anims/{saida}.png", bits=4)
        print(f"{saida}: paletas {{{', '.join(map(str, usadas))}}}")


if __name__ == "__main__":
    main()

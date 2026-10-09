#!/usr/bin/env python3
"""Integra as portas da Battle Tower 07A à parede nova.

Os bancos 07A mantiveram nativos os metatiles acima das portas (0x206 sobre a
porta de elevador, 0x2A5/0x2A6 sobre a porta dupla Multi e 0x207, a porta
aberta do corredor). A parede nativa tinha uma faixa branca no alto e a nova é
cinza-esverdeada, então sobrava um retângulo branco acima de cada porta.

1. Nesses metatiles, as linhas 0-5 passam a ser a parede lisa nova (0x209) e,
   nas linhas 6-7, fica só o que a porta nativa desenha diferente da parede
   nativa (a linha escura da moldura). A parede vai na camada de baixo e a
   moldura num tile novo da camada de cima, nas paletas nativas.
2. As animações da porta de elevador e da porta dupla redesenham esses
   metatiles só com a camada de baixo; os quadros novos são o desenho parado
   novo com as folhas da porta copiadas da animação nativa. Na faixa de cima,
   a linha da moldura usa a cor mais próxima da paleta 12.

Uso, na raiz do repositório:
    python3 tools/arauna_maps/corrige_portas_frontier_07a.py
"""
import struct

from PIL import Image

from gera_portas_trainer_hill_06a import banco, cor_pixel
from render_native_map import ROOT, indexed_tiles

ORIGINAL = ("gTileset_Building", "gTileset_BattleFrontier")
NOVO = ("gTileset_AraunaFrontier07ATowerBase", "gTileset_AraunaFrontier07ATowerArt")
SECUNDARIO = ROOT / "data/tilesets/secondary/arauna_frontier07a_tower"
PAREDE = 0x209
TOPOS = (0x206, 0x2A5, 0x2A6, 0x207)
LINHA_MOLDURA = 6
# saída, png nativo, metatiles da porta por coluna (acima, porta), largura em metatiles
PORTAS = (
    ("arauna_frontier07a_tower_elevator", "battle_tower_elevator", ((0x206, 0x20E),), 1),
    ("arauna_frontier07a_tower_multi_corridor", "battle_tower_multi_corridor", ((0x2A5, 0x2AD), (0x2A6, 0x2AE)), 2),
)
# paleta por tile da animação: faixa de cima na paleta 12, resto na paleta nativa 7
PALETAS = (12, 12, 7, 7, 7, 7, 7, 7)


def rgb(r, mid):
    t = Image.new("RGBA", (16, 16), r.palettes[0][0] + (255,))
    t.alpha_composite(r.metatile(mid))
    return t.convert("RGB")


def alvo(velho, novo, mid):
    """Desenho parado desejado: parede nova em cima, moldura nativa embaixo."""
    out, nativo = rgb(novo, mid), rgb(velho, mid)
    pv, pn = rgb(velho, PAREDE), rgb(novo, PAREDE)
    for y in range(8):
        for x in range(16):
            manter = y >= LINHA_MOLDURA and nativo.getpixel((x, y)) != pv.getpixel((x, y))
            out.putpixel((x, y), nativo.getpixel((x, y)) if manter else pn.getpixel((x, y)))
    return out


def ler_palavras(path):
    raw = path.read_bytes()
    return list(struct.unpack(f"<{len(raw) // 2}H", raw))


def corrige_banco(velho):
    novo = banco(*NOVO)
    metas = ler_palavras(SECUNDARIO / "metatiles.bin")
    folha = Image.open(SECUNDARIO / "tiles.png")
    paleta_png = folha.getpalette()
    idx, por_linha, total = indexed_tiles(SECUNDARIO / "tiles.png")
    tiles = [bytes(idx.crop((t % por_linha * 8, t // por_linha * 8, t % por_linha * 8 + 8,
                             t // por_linha * 8 + 8)).tobytes()) for t in range(total)]
    alvos = {mid: alvo(velho, novo, mid) for mid in TOPOS}
    parede = metas[(PAREDE - 0x200) * 8:(PAREDE - 0x200) * 8 + 2]
    pn = rgb(novo, PAREDE)
    for mid in TOPOS:
        base = (mid - 0x200) * 8
        for q in range(2):
            # na segunda execução a paleta nativa já está na camada de cima
            pal_nativa = metas[base + q] >> 12 if metas[base + q] != parede[q] else metas[base + 4 + q] >> 12
            cores = velho.palettes[pal_nativa]
            px = bytearray(64)
            for y in range(LINHA_MOLDURA, 8):
                for x in range(8):
                    c = alvos[mid].getpixel((q * 8 + x, y))
                    if c != pn.getpixel((q * 8 + x, y)):
                        px[y * 8 + x] = cores.index(c)
            px = bytes(px)
            espelho = bytes(px[y * 8 + 7 - x] for y in range(8) for x in range(8))
            if px in tiles:
                palavra = (512 + tiles.index(px))
            elif espelho in tiles:
                palavra = (512 + tiles.index(espelho)) | 0x400
            else:
                tiles.append(px)
                palavra = 512 + len(tiles) - 1
            metas[base + q] = parede[q]
            metas[base + 4 + q] = palavra | (pal_nativa << 12)
    # grava a folha de tiles (16 por linha) e os metatiles
    linhas = (len(tiles) + por_linha - 1) // por_linha
    nova = Image.new("P", (por_linha * 8, linhas * 8))
    for t, px in enumerate(tiles):
        nova.paste(Image.frombytes("P", (8, 8), px), (t % por_linha * 8, t // por_linha * 8))
    nova.putpalette(paleta_png)
    nova.save(SECUNDARIO / "tiles.png", bits=4)
    (SECUNDARIO / "metatiles.bin").write_bytes(struct.pack(f"<{len(metas)}H", *metas))
    novo = banco(*NOVO)
    for mid in TOPOS:
        assert rgb(novo, mid).tobytes() == alvos[mid].tobytes(), hex(mid)
    return novo, len(tiles) - total


def parado(r, colunas):
    out = Image.new("RGB", (16 * len(colunas), 32))
    for c, (acima, porta) in enumerate(colunas):
        out.paste(rgb(r, acima), (c * 16, 0))
        out.paste(rgb(r, porta), (c * 16, 16))
    return out


def paleta_do_tile(x, y):
    """Índice em PALETAS do tile 8x8 em (x, y) de um quadro (cada coluna de 16 px repete o arranjo)."""
    return (y // 16) * 4 + ((y % 16) // 8) * 2 + (x % 16) // 8


def quadro(r, indices, larg, n, largura):
    fundo = r.palettes[0][0]
    out = Image.new("RGB", (16 * largura, 32))
    for y in range(32):
        for x in range(16 * largura):
            c = indices[(n * 32 + y) * larg + x] & 15
            out.putpixel((x, y), r.palettes[7][c] if c else fundo)
    return out


def gera_animacoes(velho, novo):
    cinza = [v for i in range(16) for v in (255 - i * 17,) * 3]
    for saida, nativo, colunas, largura in PORTAS:
        img = Image.open(ROOT / f"graphics/door_anims/{nativo}.png")
        indices, larg = list(img.get_flattened_data()), img.width
        antes, depois = parado(velho, colunas), parado(novo, colunas)
        folha = Image.new("P", img.size)
        for n in range(img.height // 32):
            original = quadro(velho, indices, larg, n, largura)
            for y in range(32):
                for x in range(16 * largura):
                    folha_porta = original.getpixel((x, y)) != antes.getpixel((x, y))
                    c = original.getpixel((x, y)) if folha_porta else depois.getpixel((x, y))
                    p = PALETAS[paleta_do_tile(x, y)]
                    cores = novo.palettes[p]
                    if c == novo.palettes[0][0]:
                        k = 0
                    else:
                        k = min(range(1, 16), key=lambda i: sum(abs(a - b) for a, b in zip(cores[i], c)))
                    erro = 0 if k == 0 else sum(abs(a - b) for a, b in zip(cores[k], c))
                    # faixa de cima: só a linha da moldura aproxima; resto exato
                    limite = 60 if folha_porta else (30 if y == 7 else 0)
                    assert erro <= limite, (saida, n, x, y, erro)
                    folha.putpixel((x, n * 32 + y), k)
        folha.putpalette(cinza)
        folha.save(ROOT / f"graphics/door_anims/{saida}.png", bits=4)
        print(f"{saida}: paletas {{{', '.join(map(str, PALETAS))}}}")


def main():
    velho = banco(*ORIGINAL)
    novo, acrescentados = corrige_banco(velho)
    print(f"metatiles {', '.join(hex(m) for m in TOPOS)} corrigidos; tiles novos no secundário: {acrescentados}")
    gera_animacoes(velho, novo)


if __name__ == "__main__":
    main()

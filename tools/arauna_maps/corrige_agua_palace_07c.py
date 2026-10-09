#!/usr/bin/env python3
"""Devolve a água ao metatile 0x226 do banco 07C do pátio do Battle Palace.

No original (General + BattlePalace), 0x226 é água com a margem de pedra à
esquerda: a mesma camada de baixo de 0x190 e quase a mesma margem (só o tile
superior esquerdo da camada de cima muda). O banco 07C o redesenhou como um
bloco de parede, e a sala de batalha do Palace ficou com um bloco cinza dentro
da água em (2,4) e (2,5), as duas únicas células que usam 0x226.

A correção copia para 0x226 as oito palavras gráficas do 0x190 novo; os
atributos (comportamento de água e tipo de camada) não mudam. Pode ser rodada
de novo sem efeito. Uso, na raiz do repositório:

    python3 tools/arauna_maps/corrige_agua_palace_07c.py
"""
import struct

from bancos_nativos import bank_words
from render_native_map import ROOT, Renderer, resolve_tileset

ORIGINAL = ("gTileset_General", "gTileset_BattlePalace")
SECUNDARIO = ROOT / "data/tilesets/secondary/arauna_frontier07c_palace_garden"
ALVO, MODELO = 0x226, 0x190


def main():
    velho = Renderer(*(resolve_tileset(s) for s in ORIGINAL))
    a, b = bank_words(velho, ALVO), bank_words(velho, MODELO)
    # no original os dois só diferem no tile superior esquerdo da camada de cima
    assert [i for i in range(8) if a[i] != b[i]] == [4], (a, b)
    novo = Renderer(resolve_tileset("gTileset_AraunaFrontier07CPalaceGardenBase"), SECUNDARIO)
    palavras = list(bank_words(novo, MODELO))  # 0x190 fica no primário do pátio
    path = SECUNDARIO / "metatiles.bin"
    raw = path.read_bytes()
    metas = list(struct.unpack(f"<{len(raw) // 2}H", raw))
    alvo = (ALVO - 0x200) * 8
    metas[alvo:alvo + 8] = palavras
    path.write_bytes(struct.pack(f"<{len(metas)}H", *metas))
    print(f"{hex(ALVO)} agora usa os gráficos de {hex(MODELO)}: {[hex(w) for w in palavras]}")


if __name__ == "__main__":
    main()

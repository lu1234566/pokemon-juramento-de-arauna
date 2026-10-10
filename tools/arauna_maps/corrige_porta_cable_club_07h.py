#!/usr/bin/env python3
"""Leva a parede nova do Centro Pokémon 07H para cima das portas do Cable Club.

No 2º andar, o metatile 0x25C (acima das portas 0x264) ficou nativo, e a
parede ao lado (0x20B) ganhou uma faixa marrom no alto. Sobravam duas faixas
claras sobre as portas. No original, 0x25C é igual a 0x20B nas linhas 0-6: a
metade de cima é parede, a de baixo é a moldura da porta.

A correção copia para os dois quadrantes de cima de 0x25C (camada de baixo e
de cima) as palavras da parede nova 0x20B; os quadrantes de baixo continuam
com a moldura nativa. A animação da porta do Cable Club, que só toca em jogo
por cabo e já não batia com o desenho parado no original, não muda.

Pode ser rodada de novo sem efeito. Uso, na raiz do repositório:

    python3 tools/arauna_maps/corrige_porta_cable_club_07h.py
"""
import struct

from bancos_nativos import bank_words
from render_native_map import ROOT, Renderer, resolve_tileset

ORIGINAL = ("gTileset_Building", "gTileset_PokemonCenter")
SECUNDARIO = ROOT / "data/tilesets/secondary/arauna_frontier07h_clinic"
ALVO, PAREDE = 0x25C, 0x20B


def main():
    velho = Renderer(*(resolve_tileset(s) for s in ORIGINAL))
    a, b = velho.metatile(ALVO), velho.metatile(PAREDE)
    # no original, a metade de cima (linhas 0-6) de 0x25C é a parede 0x20B
    assert all(a.getpixel((x, y)) == b.getpixel((x, y)) for y in range(7) for x in range(16))
    path = SECUNDARIO / "metatiles.bin"
    raw = path.read_bytes()
    metas = list(struct.unpack(f"<{len(raw) // 2}H", raw))
    alvo, parede = (ALVO - 0x200) * 8, (PAREDE - 0x200) * 8
    for q in (0, 1, 4, 5):  # quadrantes de cima nas duas camadas
        metas[alvo + q] = metas[parede + q]
    path.write_bytes(struct.pack(f"<{len(metas)}H", *metas))
    novo = Renderer(resolve_tileset("gTileset_AraunaFrontier07HClinicBase"), SECUNDARIO)
    print(f"{hex(ALVO)}: {[hex(w) for w in bank_words(novo, ALVO)]}")


if __name__ == "__main__":
    main()

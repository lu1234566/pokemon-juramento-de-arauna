#!/usr/bin/env python3
"""Gera o patch BPS que se publica, a partir da sua copia do jogo original.

O que se distribui numa ROM hack nao e a ROM montada -- ela carrega o jogo da
Nintendo inteiro dentro. Distribui-se o patch, e cada jogador aplica na copia
legitima dele. Este repositorio ja segue essa regra: o
`scripts/check_no_proprietary_files.sh` recusa `.gba`, `.bps`, `.ips`, `.ups`
e `.xdelta` no Git.

Uso:
    python3 tools/arauna/make_patch.py SUA_EMERALD.gba \\
        --alvo pokemon-juramento-de-arauna-en_modern.gba \\
        --saida juramento-de-arauana-beta.bps

O arquivo de origem nunca e copiado para lugar nenhum: ele e lido, comparado,
e o que sai e so a diferenca mais os tres checksums que o formato exige.

Sobre o formato: BPS guarda CRC32 da origem, do alvo e do proprio patch, entao
o aplicador recusa sozinho uma ROM base errada -- que e o erro numero um de
quem instala hack. IPS nao tem isso e nem aguenta 16 MB, por isso nao e opcao
aqui.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import zlib
from pathlib import Path

# Acoes do BPS. So as duas primeiras sao usadas: "veio igual da origem" e
# "estes bytes sao novos". As outras duas (SourceCopy/TargetCopy) rendem patch
# menor em ROM muito repetitiva, e custam um casador de padroes que nao vale o
# risco de errar num arquivo que outra pessoa vai aplicar.
SOURCE_READ = 0
TARGET_READ = 1


def varint(number: int) -> bytes:
    """O inteiro de tamanho variavel do BPS: 7 bits por byte, com o bit alto
    marcando o ultimo, e o menos-um acumulado a cada passo."""
    out = bytearray()
    while True:
        lowest = number & 0x7F
        number >>= 7
        if number == 0:
            out.append(0x80 | lowest)
            return bytes(out)
        out.append(lowest)
        number -= 1


def runs(source: bytes, target: bytes):
    """Corta o alvo em trechos iguais e trechos diferentes da origem.

    Um trecho so vira "diferente" quando a diferenca comeca; enquanto os dois
    arquivos concordam byte a byte, o patch nao carrega nada.
    """
    limit = min(len(source), len(target))
    position = 0
    while position < len(target):
        same = position < limit and source[position] == target[position]
        start = position
        while position < len(target):
            if position < limit:
                if (source[position] == target[position]) != same:
                    break
            elif same:
                break
            position += 1
        yield (SOURCE_READ if same else TARGET_READ), start, position - start


def build(source: bytes, target: bytes, metadata: bytes = b"") -> bytes:
    patch = bytearray(b"BPS1")
    patch += varint(len(source))
    patch += varint(len(target))
    patch += varint(len(metadata))
    patch += metadata

    for action, start, length in runs(source, target):
        patch += varint((length - 1) << 2 | action)
        if action == TARGET_READ:
            patch += target[start:start + length]

    patch += zlib.crc32(source).to_bytes(4, "little")
    patch += zlib.crc32(target).to_bytes(4, "little")
    patch += zlib.crc32(bytes(patch)).to_bytes(4, "little")
    return bytes(patch)


def read_varint(data: bytes, at: int) -> tuple[int, int]:
    number, shift = 0, 0
    while True:
        byte = data[at]
        at += 1
        number += (byte & 0x7F) << shift
        if byte & 0x80:
            return number, at
        shift += 7
        number += 1 << shift


def apply(source: bytes, patch: bytes) -> bytes:
    """Aplica o patch, do mesmo jeito que o aplicador do jogador aplicaria.

    Existe para o gerador se provar: quem publica um patch nao pode descobrir
    que ele nao aplica depois que mil pessoas baixaram.
    """
    if patch[:4] != b"BPS1":
        raise ValueError("nao e um BPS")
    at = 4
    _, at = read_varint(patch, at)          # tamanho da origem
    target_size, at = read_varint(patch, at)
    metadata_size, at = read_varint(patch, at)
    at += metadata_size

    out = bytearray()
    end = len(patch) - 12
    while at < end:
        control, at = read_varint(patch, at)
        action, length = control & 3, (control >> 2) + 1
        if action == SOURCE_READ:
            out += source[len(out):len(out) + length]
        elif action == TARGET_READ:
            out += patch[at:at + length]
            at += length
        else:
            raise ValueError("acao %d nao e emitida por este gerador" % action)
    if len(out) != target_size:
        raise ValueError("o patch produziu %d bytes, devia produzir %d"
                         % (len(out), target_size))
    return bytes(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("origem", help="a sua copia do Pokemon Emerald")
    ap.add_argument("--alvo", default="pokemon-juramento-de-arauna-en_modern.gba",
                    help="a ROM montada deste repositorio")
    ap.add_argument("--saida", default="juramento-de-arauana.bps")
    args = ap.parse_args()

    origem, alvo = Path(args.origem), Path(args.alvo)
    for caminho in (origem, alvo):
        if not caminho.exists():
            print("nao encontrei: %s" % caminho, file=sys.stderr)
            return 1

    source, target = origem.read_bytes(), alvo.read_bytes()
    patch = build(source, target)

    # O patch se prova antes de ser escrito: aplicado de volta na origem, tem
    # de devolver o alvo byte a byte.
    refeito = apply(source, patch)
    if refeito != target:
        print("o patch gerado NAO reproduz o alvo -- nada foi escrito",
              file=sys.stderr)
        return 1

    Path(args.saida).write_bytes(patch)

    iguais = sum(n for a, _, n in runs(source, target) if a == SOURCE_READ)
    print("origem : %-42s %9d bytes  CRC32 %08X"
          % (origem.name, len(source), zlib.crc32(source)))
    # O jogador precisa deste numero para saber se a copia dele serve. A ROM
    # usada aqui vira a ROM obrigatoria para todo mundo: o BPS guarda o CRC32
    # dela e o aplicador recusa qualquer outra.
    print("         publique este MD5 da base: %s"
          % hashlib.md5(source).hexdigest())
    print("alvo   : %-42s %9d bytes  CRC32 %08X"
          % (alvo.name, len(target), zlib.crc32(target)))
    # O CRC que o formato grava e o de tudo que vem antes dele, nao o do
    # arquivo inteiro -- e esse que um aplicador mostra.
    print("patch  : %-42s %9d bytes  CRC32 %08X"
          % (args.saida, len(patch), zlib.crc32(patch[:-4])))
    print("%.1f%% do alvo veio igual da origem; o patch carrega o resto."
          % (100.0 * iguais / len(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

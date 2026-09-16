#!/usr/bin/env python3
"""Confere se o PDF do manual contem tudo que o dossie diz que existe.

Um manual diagramado erra de um jeito que nao se ve: a pagina enche, o
conteudo que nao coube some, e a pagina continua bonita. Foi o que aconteceu
na terceira versao -- a pagina de habilidades trazia 24 das 35, a de golpes 16
dos 27, e as duas terminavam sem nenhuma marca de que faltava algo.

Isto le o texto do PDF e procura, uma por uma, cada coisa que o dossie tem:
as 386 criaturas, o elenco, os lendarios pendentes, as criaturas dos treze
chefes, as habilidades e os golpes. O que nao for encontrado e nomeado.

A busca e por texto e nao por posicao, entao ela sobrevive a rediagramacao: se
o desenhista mudar a ordem, o tamanho ou a coluna, o teste continua valendo.
Ela so responde "esta no documento?", e nao "esta bonito?".

Uso:  python3 tools/arauna/check_dossier_pdf.py MANUAL.pdf
Sai com 1 se faltar qualquer coisa.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def flatten(text: str) -> str:
    """Tira acento, caixa e espaco repetido.

    O PDF espaca letra por letra em titulo -- "H A B I L I D A D E S" -- e usa
    aspa curva onde o dado usa reta. Comparar cru acusaria diferenca onde nao
    ha nenhuma.
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def pdf_text(path: Path) -> str:
    if not shutil.which("pdftotext"):
        print("pdftotext nao esta instalado (apt-get install poppler-utils)",
              file=sys.stderr)
        raise SystemExit(2)
    done = subprocess.run(["pdftotext", str(path), "-"],
                          capture_output=True, text=True, check=True)
    return flatten(done.stdout)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    args = ap.parse_args()

    corpo = pdf_text(Path(args.pdf))
    base = json.loads((ROOT / "docs/arauna/DOSSIE_BETA.json").read_text(encoding="utf-8"))
    extras = json.loads((ROOT / "docs/arauna/DOSSIE_EXTRAS.json").read_text(encoding="utf-8"))

    # Cada secao e conferida pelo campo que a identifica sem ambiguidade. A
    # descricao vale mais que o nome para habilidade e golpe: um nome curto
    # pode aparecer por acaso noutra pagina, uma frase inteira nao.
    secoes = [
        ("criaturas da dex", [m["nome"] for m in base["dex"]]),
        ("elenco", [novo for _, novo in base["elenco"]]),
        ("lendarios pendentes",
         [s["name"] for s in base["especiais_pendentes"] if not s["tem_casa"]]),
        ("criaturas dos treze chefes",
         [m["nome"] for g in base["ginasios"] + base["elite"] for m in g["time"]]),
        ("habilidades", [a["descricao"] for a in extras["habilidades"]]),
        ("golpes", [m["descricao"] for m in extras["golpes"]]),
    ]

    rotulo = {
        "habilidades": {a["descricao"]: "n%d %s" % (a["numero"], a["nome"])
                        for a in extras["habilidades"]},
        "golpes": {m["descricao"]: m["nome_completo"] for m in extras["golpes"]},
    }

    faltou = 0
    for nome, itens in secoes:
        ausentes = [i for i in itens if flatten(str(i)) not in corpo]
        estado = "OK" if not ausentes else "FALTAM %d" % len(ausentes)
        print("%-28s %4d esperados   %s" % (nome, len(itens), estado))
        for item in ausentes:
            print("      %s" % rotulo.get(nome, {}).get(item, item))
        faltou += len(ausentes)

    print()
    if faltou:
        print("%d entradas do dossie nao estao no PDF." % faltou)
        return 1
    print("o PDF contem tudo que o dossie declara.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""As tres coisas que faltavam no dossie: arte, encontros e o que cada
habilidade e cada golpe novo faz.

O dossie nasceu com numeros e sem explicacao. Uma tabela que diz "FOGO LEAL"
e nao diz o que FOGO LEAL faz nao serve para quem vai jogar, e uma dex sem
figura nao e uma dex.

Tres saidas, todas geradas do repositorio:

  docs/DOSSIE_EXTRAS.md            as habilidades e os golpes com descricao,
                                   e a tabela de encontros mapa a mapa
  docs/arauna/DOSSIE_EXTRAS.json   o mesmo, estruturado
  docs/arauna/sprites/             a arte: 386 frentes, 386 icones, e uma
                                   folha de contato para o diagramador

A arte sai da mesma fonte que o jogo compila -- graphics/pokemon/<pasta>/ --
convertida de paleta indexada para PNG com transparencia, que e o que uma
ferramenta de diagramacao sabe usar.

Uso:  python3 tools/arauna/build_dossier_extras.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_stab_pool import dex_table, move_table  # noqa: E402

SPRITES = ROOT / "docs/arauna/sprites"


def _strings(path: Path) -> dict[str, str]:
    """simbolo -> texto que o jogador le.

    Os dois arquivos escrevem a mesma coisa de dois jeitos. O abilities.h poe
    um `_("...")` por simbolo, numa linha. O move_descriptions.h poe varios
    literais dentro de **um** `_( ... )` que atravessa linhas, e o compilador
    os cola. Ler so a forma de uma linha devolve descricao vazia para os 27
    golpes novos, sem erro nenhum -- foi o que aconteceu na primeira versao.

    Entao a leitura nao tenta casar a forma: vai do `=` ate o `;` que fecha a
    declaracao, e tira de la todos os literais.

    O `;` que fecha nao pode ser achado com uma busca nao-gulosa. Seis
    descricoes de habilidade tem ponto e virgula **dentro do texto** -- "Ups
    fire, dragon; no burn." -- e um `.*?;` para no primeiro, que esta no meio
    da string. O resultado nao e erro: e descricao vazia, silenciosa, em
    exatamente essas seis. Por isso o fim da declaracao e achado varrendo os
    caracteres e contando aspas, que e a unica forma de saber se um `;` esta
    dentro ou fora de um literal.
    """
    text = path.read_text(encoding="utf-8")
    out = {}
    for inicio in re.finditer(r"static const u8 (\w+)\[\]\s*=", text):
        posicao, dentro, escapado = inicio.end(), False, False
        while posicao < len(text):
            letra = text[posicao]
            if escapado:
                escapado = False
            elif letra == "\\":
                escapado = True
            elif letra == '"':
                dentro = not dentro
            elif letra == ";" and not dentro:
                break
            posicao += 1
        corpo = text[inicio.end():posicao]
        colado = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', corpo))
        out[inicio.group(1)] = (colado.replace("\\n", " ").replace("\\p", " ")
                                .replace("\\l", " ").strip())
    return out


def abilities():
    """(numero, nome em jogo, descricao em jogo) das habilidades de Arauna."""
    path = ROOT / "src/data/text/abilities.h"
    text = path.read_text(encoding="utf-8")
    descriptions = _strings(path)
    names = dict(re.findall(r"\[(ABILITY_\w+)\]\s*=\s*_\(\"([^\"]*)\"\)", text))
    pointers = dict(re.findall(r"\[(ABILITY_\w+)\]\s*=\s*(\w+Description)", text))
    numbers = dict(re.findall(r"#define (ABILITY_\w+)\s+(\d+)",
                              (ROOT / "include/constants/abilities.h").read_text()))
    out = []
    for key, number in numbers.items():
        if key in ("ABILITY_NONE",) or int(number) < 78:
            continue
        out.append({
            "id": key, "numero": int(number),
            "nome": names.get(key, key[len("ABILITY_"):]),
            "descricao": descriptions.get(pointers.get(key, ""), ""),
        })
    return sorted(out, key=lambda a: a["numero"])


def signature_moves():
    """Os golpes que so existem neste jogo, com ficha completa."""
    names_path = ROOT / "src/data/text/move_names.h"
    names = dict(re.findall(r"\[(MOVE_\w+)\]\s*=\s*_\(\"([^\"]*)\"\)",
                            names_path.read_text(encoding="utf-8")))
    desc_path = ROOT / "src/data/text/move_descriptions.h"
    descriptions = _strings(desc_path)
    rows = dict(re.findall(r"\[MOVE_(\w+)\s*-\s*1\]\s*=\s*(\w+)\s*,",
                           desc_path.read_text(encoding="utf-8")))
    numbers = dict(re.findall(r"#define (MOVE_\w+)\s+(\d+)",
                              (ROOT / "include/constants/moves.h").read_text()))
    battle = (ROOT / "src/data/battle_moves.h").read_text(encoding="utf-8")
    stats = {}
    for block in re.finditer(r"\[(MOVE_\w+)\]\s*=\s*\{(.*?)\n    \}", battle, re.S):
        body = block.group(2)
        grab = lambda field: (re.search(r"\.%s\s*=\s*(\w+)" % field, body) or [None, None])[1] \
            if re.search(r"\.%s\s*=\s*(\w+)" % field, body) else None
        stats[block.group(1)] = {
            "efeito": (grab("effect") or "")[len("EFFECT_"):],
            "poder": int(grab("power") or 0),
            "tipo": (grab("type") or "")[len("TYPE_"):].capitalize(),
            "precisao": int(grab("accuracy") or 0),
            "pp": int(grab("pp") or 0),
            "chance": int(grab("secondaryEffectChance") or 0),
        }
    out = []
    for key, number in numbers.items():
        if int(number) <= 354 or key not in stats:
            continue
        bare = key[len("MOVE_"):]
        # O nome em jogo cabe em doze caracteres e sai cortado -- ANCESTRAL
        # WISP vira "ANCESTRAL WI" na tela. Num manual impresso nao ha esse
        # limite, entao os dois vao: o cortado, que e o que o jogador ve, e o
        # inteiro, que e o que se escreve num titulo.
        entry = {"id": key, "numero": int(number),
                 "nome": names.get(key, bare.replace("_", " ").title()),
                 "nome_completo": bare.replace("_", " ").title(),
                 "descricao": descriptions.get(rows.get(bare, ""), "")}
        entry.update(stats[key])
        out.append(entry)
    return sorted(out, key=lambda m: m["numero"])


def encounters():
    """Mapa -> metodo -> lista de (criatura, nivel minimo, nivel maximo)."""
    dex = dex_table()
    by_species = {v[1]: (k, v[0]) for k, v in dex.items()}
    data = json.loads((ROOT / "src/data/wild_encounters.json").read_text())
    rotulo = {"land_mons": "grama", "water_mons": "surfe",
              "rock_smash_mons": "pedra", "fishing_mons": "pesca"}
    out = {}
    for group in data["wild_encounter_groups"]:
        for entry in group.get("encounters", []):
            nome = entry.get("map")
            if not nome:
                continue
            mapa = out.setdefault(nome[len("MAP_"):], {})
            for field, como in rotulo.items():
                if not entry.get(field):
                    continue
                vistos = {}
                for mon in entry[field]["mons"]:
                    dexno, criatura = by_species.get(mon["species"], (0, mon["species"]))
                    faixa = vistos.setdefault((dexno, criatura), [99, 0])
                    faixa[0] = min(faixa[0], mon["min_level"])
                    faixa[1] = max(faixa[1], mon["max_level"])
                mapa[como] = {
                    "taxa": entry[field]["encounter_rate"],
                    "criaturas": [{"dex": d, "nome": n, "min": f[0], "max": f[1]}
                                  for (d, n), f in sorted(vistos.items())],
                }
    return out


def export_sprites():
    """Exporta a arte dos 386 em PNG com transparencia, e uma folha de contato.

    O jogo guarda a arte em paleta indexada de 16 cores, com a cor 0 sendo o
    fundo. Uma ferramenta de diagramacao nao sabe disso -- para ela a cor 0 e
    so mais uma cor, e o sprite sai dentro de um retangulo. Aqui a cor 0 vira
    alfa zero, que e o que faz o bicho recortar no papel.
    """
    from PIL import Image

    dex = dex_table()
    folders = {}
    import csv
    with open(ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            folders[int(row["arauna_dex"])] = row["graphics_folder"]

    for pasta in ("frente", "icone"):
        (SPRITES / pasta).mkdir(parents=True, exist_ok=True)

    # Duas pastas do Emerald nao guardam a arte na raiz, e as duas sao
    # historicas: o Unown separa uma subpasta por letra, e o Castform separa
    # uma por clima e deixa so os .4bpp crus la fora. A forma base de cada um
    # e a que o jogo mostra por padrao.
    RAIZ_ALTERNATIVA = {"unown": "a", "castform": "normal"}

    feitos, faltando = [], []
    for numero in sorted(dex):
        pasta = folders.get(numero, "")
        origem = ROOT / "graphics/pokemon" / pasta
        if pasta in RAIZ_ALTERNATIVA and not (origem / "front.png").exists():
            origem = origem / RAIZ_ALTERNATIVA[pasta]
        frente = origem / "front.png"
        # O Castform guarda o icone so na pasta de cima.
        icone = origem / "icon.png"
        if not icone.exists():
            icone = origem.parent / "icon.png"
        if not frente.exists():
            faltando.append(numero)
            continue
        alvo = "%03d_%s" % (numero, re.sub(r"[^\w-]", "_", dex[numero][0]))

        arte = Image.open(frente).convert("RGBA")
        fundo = Image.open(frente).convert("P").getpixel((0, 0))
        pixels = Image.open(frente).convert("P").load()
        recorte = arte.load()
        for y in range(arte.height):
            for x in range(arte.width):
                if pixels[x, y] == fundo:
                    recorte[x, y] = (0, 0, 0, 0)
        arte.save(SPRITES / "frente" / (alvo + ".png"))

        if icone.exists():
            # O icone tem dois quadros empilhados; o de cima basta.
            mini = Image.open(icone).convert("RGBA").crop((0, 0, 32, 32))
            base = Image.open(icone).convert("P")
            marca = base.getpixel((0, 0))
            leitura, escrita = base.load(), mini.load()
            for y in range(32):
                for x in range(32):
                    if leitura[x, y] == marca:
                        escrita[x, y] = (0, 0, 0, 0)
            mini.save(SPRITES / "icone" / (alvo + ".png"))
        feitos.append(numero)

    # A folha de contato: os 386 icones numa grade, para o diagramador ver o
    # elenco inteiro de uma vez e escolher onde cada um entra.
    colunas, lado = 20, 32
    linhas = (len(feitos) + colunas - 1) // colunas
    folha = Image.new("RGBA", (colunas * lado, linhas * lado), (0, 0, 0, 0))
    for posicao, numero in enumerate(feitos):
        alvo = "%03d_%s.png" % (numero, re.sub(r"[^\w-]", "_", dex[numero][0]))
        caminho = SPRITES / "icone" / alvo
        if caminho.exists():
            folha.paste(Image.open(caminho),
                        ((posicao % colunas) * lado, (posicao // colunas) * lado))
    folha.save(SPRITES / "folha_de_contato.png")
    return feitos, faltando


def markdown(d):
    L = []
    add = L.append
    add("# Dossie da beta — o que faltava")
    add("")
    add("Complemento de `docs/DOSSIE_BETA.md`, com o que aquele documento nao")
    add("trazia: o que cada habilidade e cada golpe novo **faz**, a tabela de")
    add("encontros mapa a mapa, e a arte das 386 criaturas.")
    add("")
    add("Gerado por `tools/arauna/build_dossier_extras.py`, do proprio")
    add("repositorio: as descricoes sao as que o jogador le na tela do jogo.")
    add("")

    add("## A arte")
    add("")
    add("`docs/arauna/sprites/` tem tres coisas:")
    add("")
    add("| pasta | o que e |")
    add("|---|---|")
    add("| `frente/` | %d PNG de 64x64, o retrato de batalha, fundo transparente |"
        % len(d["sprites"]["exportados"]))
    add("| `icone/` | %d PNG de 32x32, o icone de menu, fundo transparente |"
        % len(d["sprites"]["exportados"]))
    add("| `folha_de_contato.png` | os %d icones numa grade de 20 colunas |"
        % len(d["sprites"]["exportados"]))
    add("")
    add("Os arquivos sao nomeados `NNN_Nome.png`, entao ordenar por nome e")
    add("ordenar por numero da dex.")
    add("")

    add("## As %d habilidades novas" % len(d["habilidades"]))
    add("")
    add("A descricao e exatamente a que aparece na tela de resumo do jogo.")
    add("")
    add("| # | habilidade | o que faz |")
    add("|---:|---|---|")
    for a in d["habilidades"]:
        add("| %d | **%s** | %s |" % (a["numero"], a["nome"], a["descricao"]))
    add("")

    add("## Os %d golpes exclusivos" % len(d["golpes"]))
    add("")
    add("O nome em jogo cabe em doze caracteres; o inteiro esta ao lado, para")
    add("usar em titulo.")
    add("")
    add("| golpe | em jogo | tipo | poder | precisao | PP | o que faz |")
    add("|---|---|---|---:|---:|---:|---|")
    for m in d["golpes"]:
        add("| **%s** | `%s` | %s | %s | %s | %d | %s |"
            % (m["nome_completo"], m["nome"], m["tipo"],
               m["poder"] if m["poder"] and m["poder"] > 1 else "—",
               "%d%%" % m["precisao"] if m["precisao"] else "sempre",
               m["pp"], m["descricao"]))
    add("")

    add("## Onde cada criatura aparece")
    add("")
    add("%d mapas com encontro. A taxa e a chance de o mapa gerar um encontro"
        % len(d["encontros"]))
    add("a cada passo; quanto maior, mais frequente.")
    add("")
    for mapa in sorted(d["encontros"]):
        metodos = d["encontros"][mapa]
        add("### %s" % mapa)
        add("")
        for como in ("grama", "surfe", "pedra", "pesca"):
            if como not in metodos:
                continue
            bloco = metodos[como]
            criaturas = ", ".join(
                "#%03d %s (%d%s)" % (c["dex"], c["nome"], c["min"],
                                     "" if c["min"] == c["max"] else "-%d" % c["max"])
                for c in bloco["criaturas"])
            add("- **%s** (taxa %d): %s" % (como, bloco["taxa"], criaturas))
        add("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--sem-arte", action="store_true",
                    help="pula a exportacao de sprites")
    args = ap.parse_args()

    exportados, faltando = ([], []) if args.sem_arte else export_sprites()
    data = {
        "habilidades": abilities(),
        "golpes": signature_moves(),
        "encontros": encounters(),
        "sprites": {"exportados": exportados, "sem_arte": faltando},
    }

    # Descricao vazia nao e erro de leitura: e leitura que devolveu nada e
    # seguiu em frente. Foi assim que os 27 golpes sairam em branco numa
    # versao, e seis habilidades noutra -- as seis cujo texto tem ponto e
    # virgula. Nas duas vezes o documento saiu bonito e errado. Aqui isso
    # reprova.
    mudos = ([("habilidade", a["nome"]) for a in data["habilidades"] if not a["descricao"]]
             + [("golpe", m["nome"]) for m in data["golpes"] if not m["descricao"]])
    if mudos:
        print("descricao vazia em %d entradas -- nada foi escrito:" % len(mudos),
              file=sys.stderr)
        for tipo, nome in mudos:
            print("  %s %s" % (tipo, nome), file=sys.stderr)
        return 1
    text = markdown(data)
    if args.write:
        (ROOT / "docs/DOSSIE_EXTRAS.md").write_text(text + "\n", encoding="utf-8")
        (ROOT / "docs/arauna/DOSSIE_EXTRAS.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print("escrito: docs/DOSSIE_EXTRAS.md, docs/arauna/DOSSIE_EXTRAS.json")
        if not args.sem_arte:
            print("arte: %d exportadas, %d sem arquivo %s"
                  % (len(exportados), len(faltando), faltando[:5] if faltando else ""))
    else:
        print(text[:3000])
    return 0


if __name__ == "__main__":
    sys.exit(main())

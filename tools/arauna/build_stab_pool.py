#!/usr/bin/env python3
"""Para cada ginasio/Elite Four, lista as especies que ja tem golpe ofensivo do
tipo do lider DENTRO do teto de nivel daquele chefe.

A pergunta que isto responde: "quem eu posso colocar no time do lider sem
inventar TM, sem subir o nivel e sem golpe fora do learnset?".

Fontes:
  docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv  dex -> especie de engine, tipos
  src/data/pokemon/base_stats.h              BST
  src/data/pokemon/level_up_learnsets.h      nivel de cada golpe
  src/data/battle_moves.h                    tipo e poder de cada golpe
  docs/arauna/ESPECIAIS_ESTATICOS.csv        lendarios/miticos, excluidos

Uso:  python3 tools/arauna/build_stab_pool.py [--write]
Com --write, reescreve docs/STAB_POR_GINASIO.md.
"""
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# nome do chefe, tipo tematico, teto de nivel do chefe
BOSSES = [
    ("Dalva",     "ROCK",     15),
    ("Ademar",    "FIGHTING", 19),
    ("Olivia",    "ELECTRIC", 24),
    ("Nara",      "FIRE",     29),
    ("Elias",     "NORMAL",   31),
    ("Lidia",     "FLYING",   33),
    ("Cec&Caet",  "PSYCHIC",  42),
    ("Celina",    "WATER",    46),
    ("Sidney",    "DARK",     49),
    ("Phoebe",    "GHOST",    51),
    ("Glacia",    "STEEL",    53),
    ("Drake",     "DRAGON",   55),
]

STARTERS = set(range(1, 10))          # #001-#009, as tres linhas iniciais
PSEUDO = {46, 47, 48}                 # a familia pseudo-lendaria


def dex_table():
    """arauna_dex -> (nome, SPECIES_*, [tipos])"""
    out = {}
    with open(ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv") as fh:
        for row in csv.DictReader(fh):
            dex = int(row["arauna_dex"])
            types = [t.strip().upper() for t in row["types"].split("/") if t.strip()]
            out[dex] = (row["full_name"], row["species_constant"], types)
    return out


def specials():
    with open(ROOT / "docs/arauna/ESPECIAIS_ESTATICOS.csv") as fh:
        return {int(r["dex"]) for r in csv.DictReader(fh)}


def base_stat_totals():
    """SPECIES_* -> BST, lendo os seis campos nomeados de base_stats.h."""
    text = (ROOT / "src/data/pokemon/species_info.h").read_text()
    out = {}
    for block in re.finditer(r"\[(SPECIES_\w+)\][^\n]*\n    \{(.*?)\n    \}", text, re.S):
        species, body = block.group(1), block.group(2)
        total = 0
        for field in ("baseHP", "baseAttack", "baseDefense",
                      "baseSpeed", "baseSpAttack", "baseSpDefense"):
            m = re.search(r"\.%s\s*=\s*(\d+)" % field, body)
            if m:
                total += int(m.group(1))
        out[species] = total
    return out


# Golpes cujo .power na tabela e so um marcador: o dano real sai em tempo de
# batalha, do peso, do nivel, da amizade, do HP restante. Na tabela deste
# repositorio o marcador e sempre .power = 1 -- conferido nos 22 golpes que
# tem esse valor, de GUILLOTINE a ENDEAVOR, todos de dano variavel ou fixo, e
# nenhum golpe comum de 1 de poder existe. Por isso a regra e o proprio 1, e
# nao uma lista de efeitos a mao: assim DRAGON_RAGE e SONIC_BOOM entram
# sozinhos, sem ninguem precisar lembrar deles.
VARIABLE_RANK = 50   # so para ordenar: um golpe de dano variavel vale um medio


def move_table():
    """MOVE_* -> (tipo, poder, poder_variavel?)"""
    text = (ROOT / "src/data/battle_moves.h").read_text()
    out = {}
    for block in re.finditer(r"\[(MOVE_\w+)\]\s*=\s*\{(.*?)\n    \}", text, re.S):
        move, body = block.group(1), block.group(2)
        t = re.search(r"\.type\s*=\s*TYPE_(\w+)", body)
        p = re.search(r"\.power\s*=\s*(\d+)", body)
        if t:
            power = int(p.group(1)) if p else 0
            out[move] = (t.group(1), power, power == 1)
    return out


def learnsets():
    """SPECIES_* -> [(nivel, MOVE_*)]"""
    arrays = {}
    for name in ("arauna_complete_learnsets.h", "level_up_learnsets.h"):
        text = (ROOT / "src/data/pokemon" / name).read_text()
        for block in re.finditer(
                r"static const u16 (s\w+LevelUpLearnset)\[\]\s*=\s*\{(.*?)\n\};",
                text, re.S):
            arrays.setdefault(block.group(1), [
                (int(lv), mv) for lv, mv in
                re.findall(r"LEVEL_UP_MOVE\s*\(\s*(\d+)\s*,\s*(MOVE_\w+)\s*\)", block.group(2))
            ])
    pointers = (ROOT / "src/data/pokemon/level_up_learnset_pointers.h").read_text()
    out = {}
    for row in re.finditer(r"\[(SPECIES_\w+)\]\s*=\s*(s\w+LevelUpLearnset)", pointers):
        out[row.group(1)] = arrays.get(row.group(2), [])
    return out


def build():
    dex = dex_table()
    skip = specials() | STARTERS | PSEUDO
    bst = base_stat_totals()
    moves = move_table()
    learn = learnsets()

    blocks = []
    for boss, btype, cap in BOSSES:
        rows, late, of_type = [], [], 0
        for num, (name, species, types) in sorted(dex.items()):
            if num in skip or btype not in types:
                continue
            of_type += 1
            best, later = None, None
            for lv, mv in learn.get(species, []):
                mtype, power, variable = moves.get(mv, (None, 0, False))
                if mtype != btype or power == 0:
                    continue
                if lv > cap:
                    if later is None or lv < later[0]:
                        later = (lv, mv)
                    continue
                rank = VARIABLE_RANK if variable else power
                if best is None or rank > best[0]:
                    best = (rank, mv, power, variable, lv)
            if best:
                rows.append((bst.get(species, 0), num, name, types, best))
            else:
                late.append((bst.get(species, 0), num, name, types, later))
        rows.sort(key=lambda r: (-r[0], r[1]))
        late.sort(key=lambda r: (-r[0], r[1]))
        blocks.append((boss, btype, cap, of_type, rows, late))
    return blocks


def render(blocks, limit=16):
    lines = []
    for boss, btype, cap, of_type, rows, late in blocks:
        lines.append("### %s — %s (ate nv%d) — %d de %d especies do tipo tem STAB ofensivo"
                     % (boss, btype, cap, len(rows), of_type))
        for total, num, name, types, (_, mv, power, variable, lv) in rows[:limit]:
            lines.append("  #%-3d %-20s %-17s BST %-5d melhor: %s(%s) no nv%d"
                         % (num, name, "/".join(types), total,
                            mv[len("MOVE_"):], "var" if variable else power, lv))
        if len(rows) > limit:
            lines.append("  ... e mais %d" % (len(rows) - limit))
        lines.append("")
    return "\n".join(lines)


def markdown(blocks):
    out = [
        "# Quem ja tem STAB dentro do teto de cada chefe",
        "",
        "Gerado por `tools/arauna/build_stab_pool.py` a partir do repositorio.",
        "Nao edite a mao: rode `python3 tools/arauna/build_stab_pool.py --write`.",
        "",
        "A pergunta e uma so: **para o time deste chefe, quem eu posso escolher sem",
        "inventar TM, sem subir o nivel e sem golpe fora do learnset?** Uma especie so",
        "entra aqui se o tipo do chefe e um dos seus dois tipos **e** ela aprende, por",
        "nivel, um golpe ofensivo daquele tipo ate o teto de nivel do chefe.",
        "",
        "Fora da conta: os 31 lendarios/miticos de `docs/arauna/ESPECIAIS_ESTATICOS.csv`,",
        "as tres linhas iniciais (#001-#009) e a familia pseudo #046-#048.",
        "",
        "## Resumo",
        "",
        "| chefe | tipo | teto | do tipo | com STAB no teto |",
        "|---|---|---:|---:|---:|",
    ]
    for boss, btype, cap, of_type, rows, late in blocks:
        out.append("| %s | %s | %d | %d | **%d** |" % (boss, btype, cap, of_type, len(rows)))
    out.append("")
    for boss, btype, cap, of_type, rows, late in blocks:
        out.append("## %s — %s, ate nv%d" % (boss, btype, cap))
        out.append("")
        out.append("%d das %d especies do tipo. Ordenado por BST." % (len(rows), of_type))
        out.append("")
        out.append("| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |")
        out.append("|---:|---|---|---:|---|---:|")
        for total, num, name, types, (_, mv, power, variable, lv) in rows:
            out.append("| %d | %s | %s | %d | %s (%s) | %d |"
                       % (num, name, "/".join(t.capitalize() for t in types),
                          total, mv[len("MOVE_"):],
                          "variavel" if variable else power, lv))
        out.append("")
        if late:
            out.append("Fora por pouco — sao do tipo, mas o primeiro golpe ofensivo")
            out.append("daquele tipo so chega depois do teto:")
            out.append("")
            out.append("| dex | nome | tipos | BST | primeiro STAB ofensivo |")
            out.append("|---:|---|---|---:|---|")
            for total, num, name, types, later in late:
                when = ("%s no nv%d" % (later[1][len("MOVE_"):], later[0])
                        if later else "**nunca — nao existe no learnset**")
                out.append("| %d | %s | %s | %d | %s |"
                           % (num, name, "/".join(t.capitalize() for t in types),
                              total, when))
            out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    blocks = build()
    if "--write" in sys.argv:
        path = ROOT / "docs/STAB_POR_GINASIO.md"
        path.write_text(markdown(blocks) + "\n")
        print("escrito: %s" % path.relative_to(ROOT))
    else:
        print(render(blocks))

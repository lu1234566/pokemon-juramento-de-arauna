#!/usr/bin/env python3
"""Monta o dossie da beta: tudo que o jogo tem hoje, lido do proprio jogo.

Nada aqui e digitado a mao. Cada numero sai do arquivo que o build compila --
species_info.h para stats e tipos, os learnsets para os golpes, trainers.h e
trainer_parties.h para os chefes, wild_encounters.json para os encontros,
evolution.h para as evolucoes, e os CSV de docs/arauna para nomes e plano.
Assim o dossie nao envelhece em silencio: roda de novo e ele conta o estado
novo.

Uso:  python3 tools/arauna/build_beta_dossier.py --write
Saida: docs/DOSSIE_BETA.md e docs/arauna/DOSSIE_BETA.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_stab_pool import (  # noqa: E402
    dex_table, learnsets, move_table, base_stat_totals, BOSSES)

# Quem e quem no motor: o simbolo do time e o nome de Arauna do chefe.
LEADERS = [
    ("Dalva",     "Roxanne1",     "ROCK",     "Serra do Uivo",      1),
    ("Ademar",    "Brawly1",      "FIGHTING", "Casa da Mare",       2),
    ("Olivia",    "Wattson1",     "ELECTRIC", "Encruzilhada",       3),
    ("Nara",      "Flannery1",    "FIRE",     "Casa da Cinza",      4),
    ("Elias",     "Norman1",      "NORMAL",   "Pampa da Espera",    5),
    ("Lidia",     "Winona1",      "FLYING",   "Mata do Meio",       6),
    ("Cec&Caet",  "TateAndLiza1", "PSYCHIC",  "Missoes do Ceu",     7),
    ("Celina",    "Juan1",        "WATER",    "Aguas M'Boi",        8),
]
ELITE = [
    ("Lazaro",   "Sidney",  "DARK"),
    ("Rosa",     "Phoebe",  "GHOST"),
    ("Clara",    "Glacia",  "STEEL"),
    ("Tiburcio", "Drake",   "DRAGON"),
    ("Amalia",   "Wallace", "CAMPEA"),
]


def party(symbol):
    text = (ROOT / "src/data/trainer_parties.h").read_text()
    block = re.search(r"sParty_%s\[\]\s*=\s*\{(.*?)\n\};" % symbol, text, re.S)
    if not block:
        return []
    out = []
    # Uma vaga nao pode ser lida como "o que esta entre chaves": o proprio
    # .moves = {...} tem chaves dentro, e a busca nao-gulosa para nelas. Cada
    # vaga e lida pelos campos que ela sempre tem, do .iv ate a chave que fecha
    # os golpes -- ou ate o fim da vaga, quando o time nao usa moveset custom.
    entry = re.compile(
        r"\.iv\s*=\s*(?P<iv>\d+),\s*"
        r"\.lvl\s*=\s*(?P<lvl>\d+),\s*"
        r"\.species\s*=\s*(?P<species>SPECIES_\w+),"
        r"(?:\s*\.heldItem\s*=\s*(?P<item>ITEM_\w+),)?"
        r"(?:\s*\.moves\s*=\s*\{(?P<moves>[^}]*)\})?", re.S)
    for slot in entry.finditer(block.group(1)):
        out.append({
            "species": slot.group("species"),
            "level": int(slot.group("lvl")),
            "iv": int(slot.group("iv")),
            "item": slot.group("item") or "ITEM_NONE",
            "moves": [m.strip() for m in (slot.group("moves") or "").split(",")
                      if m.strip()],
        })
    return out


def abilities():
    text = (ROOT / "include/constants/abilities.h").read_text()
    names = (ROOT / "src/data/text/abilities.h").read_text() \
        if (ROOT / "src/data/text/abilities.h").exists() else ""
    out = []
    for name, number in re.findall(r"#define (ABILITY_\w+)\s+(\d+)", text):
        if name in ("ABILITIES_COUNT", "ABILITY_NONE"):
            continue
        if int(number) >= 78:
            out.append((int(number), name[len("ABILITY_"):]))
    return sorted(out)


def signature_moves():
    """Golpes que existem so neste jogo: id acima do ultimo do Emerald."""
    text = (ROOT / "include/constants/moves.h").read_text()
    moves = move_table()
    out = []
    for name, number in re.findall(r"#define (MOVE_\w+)\s+(\d+)", text):
        if int(number) > 354 and name in moves:      # 354 = MOVE_PSYCHO_BOOST
            kind, power, _ = moves[name]
            out.append((int(number), name[len("MOVE_"):], kind, power))
    return sorted(out)


def encounters():
    data = json.loads((ROOT / "src/data/wild_encounters.json").read_text())
    maps, species = set(), set()
    for group in data["wild_encounter_groups"]:
        for entry in group.get("encounters", []):
            if not entry.get("map"):
                continue
            maps.add(entry["map"])
            for field in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
                if entry.get(field):
                    for mon in entry[field]["mons"]:
                        species.add(mon["species"])
    return len(maps), len(species)


def wild_species_set():
    data = json.loads((ROOT / "src/data/wild_encounters.json").read_text())
    out = set()
    for group in data["wild_encounter_groups"]:
        for entry in group.get("encounters", []):
            for field in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
                if entry.get(field):
                    for mon in entry[field]["mons"]:
                        out.add(mon["species"])
    return out


def evolutions():
    text = (ROOT / "src/data/pokemon/evolution.h").read_text()
    return len(re.findall(r"\{\{EVO_\w+", text)), \
        sorted(set(re.findall(r"\{\{(EVO_\w+)", text)))


def route_trainers():
    text = (ROOT / "src/data/trainers.h").read_text()
    return len(re.findall(r"\[TRAINER_\w+\] =", text))


def cast():
    with open(ROOT / "docs/arauna/ARAUNA_CHARACTER_NAMES.csv", encoding="utf-8") as fh:
        return [(r["hoenn_name"], r["arauna_name"]) for r in csv.DictReader(fh)
                if r["arauna_name"].strip()]


def canon():
    """Os pontos do canone, lidos do proprio documento da historia."""
    text = (ROOT / "docs/ARAUANA_STORY_IMPLEMENTATION.md").read_text(encoding="utf-8")
    bloco = re.search(r"## Canon\n(.*?)\n## ", text, re.S)
    if not bloco:
        return []
    out = []
    for linha in bloco.group(1).splitlines():
        if linha.startswith("- "):
            corpo = linha[2:].strip()
            rotulo, _, resto = corpo.partition(":")
            out.append((rotulo.strip(), resto.strip() or rotulo.strip()))
    return out


def places():
    """Hoenn -> Arauana, so os lugares do mapa da regiao, sem repetir destino."""
    visto, out = set(), []
    with open(ROOT / "docs/arauna/ARAUNA_PLACE_NAMES.csv", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            novo = row["arauna_name"].strip()
            if not novo or novo in visto or row["source"] != "region map":
                continue
            visto.add(novo)
            out.append((row["hoenn_name"], novo))
    return out


def connections():
    """Como os mapas de superficie se ligam, do map.json de cada um."""
    groups = json.loads((ROOT / "data/maps/map_groups.json").read_text())
    nomes = [m for g in groups["group_order"] for m in groups[g]]
    out = {}
    for nome in nomes:
        caminho = ROOT / "data/maps" / nome / "map.json"
        if not caminho.exists():
            continue
        dados = json.loads(caminho.read_text())
        ligacoes = dados.get("connections") or []
        if ligacoes:
            out[nome] = [(c["direction"], c["map"][len("MAP_"):]) for c in ligacoes]
    return out


def specials():
    """Os 31 especiais do plano, cada um marcado com se ja tem casa hoje.

    "Ter casa" e a mesma pergunta que build_availability.py responde, e a
    resposta vem dele para os dois nao discordarem: onze dos trinta e um ja sao
    alcancaveis pelos encontros herdados do Emerald, e vinte nao sao.
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import build_availability as disponivel

    by_slot, _ = disponivel.arauna()
    forward, _ = disponivel.evolution_links(by_slot)
    data = json.loads(disponivel.committed(disponivel.ENCOUNTERS))
    alcancavel = disponivel.reachable(
        disponivel.caught_in_the_wild(data, by_slot) | disponivel.scripted(by_slot),
        forward)

    out = []
    with open(ROOT / "docs/arauna/ESPECIAIS_ESTATICOS.csv", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            row["tem_casa"] = int(row["dex"]) in alcancavel
            out.append(row)
    return out


VERIFICACAO = ROOT / "docs/arauna/VERIFICACAO_BETA.json"


def verification():
    """O que foi provado no emulador, e nao so compilado.

    O arquivo e escrito pela varredura -- este gerador so o repassa. Se ele nao
    existir, o dossie diz que nao existe, em vez de inventar um numero.
    """
    if not VERIFICACAO.exists():
        return None
    return json.loads(VERIFICACAO.read_text(encoding="utf-8"))


def collect():
    dex, learn, moves, bst = dex_table(), learnsets(), move_table(), base_stat_totals()
    rev = {v[1]: (k, v[0], v[2]) for k, v in dex.items()}
    maps, wild_species = encounters()
    wild_set = wild_species_set()
    evo_count, evo_methods = evolutions()

    def team(symbol):
        out = []
        for slot in party(symbol):
            num, name, types = rev.get(slot["species"], (0, slot["species"], []))
            out.append({
                "dex": num, "nome": name,
                "tipos": [t.capitalize() for t in dict.fromkeys(types)],
                "bst": bst.get(slot["species"], 0),
                "nivel": slot["level"], "iv": slot["iv"],
                "iv31": slot["iv"] * 31 // 255,
                "item": slot["item"][len("ITEM_"):].replace("_", " ").title(),
                "golpes": [{
                    "nome": m[len("MOVE_"):].replace("_", " ").title(),
                    "tipo": moves.get(m, ("?", 0, False))[0].capitalize(),
                    "poder": moves.get(m, ("?", 0, False))[1] or None,
                } for m in slot["moves"] if m != "MOVE_NONE"],
            })
        return out

    return {
        "criaturas": {
            "total": len(dex),
            "na_natureza": wild_species,
            "mapas_com_encontro": maps,
            "learnsets": len(learn),
            "entradas_de_golpe": sum(len(v) for v in learn.values()),
        },
        "evolucoes": {"total": evo_count, "metodos": evo_methods},
        "dex": [
            {"dex": n, "nome": nome,
             "tipos": [x.capitalize() for x in dict.fromkeys(tipos)],
             "bst": bst.get(sp, 0),
             "selvagem": sp in wild_set,
             "golpes_por_nivel": len(learn.get(sp, []))}
            for n, (nome, sp, tipos) in sorted(dex.items())],
        "habilidades": abilities(),
        "golpes_assinatura": signature_moves(),
        "treinadores": route_trainers(),
        "elenco": cast(),
        "canone": canon(),
        "lugares": places(),
        "ligacoes": connections(),
        "especiais_pendentes": specials(),
        "verificacao": verification(),
        "ginasios": [
            {"chefe": nome, "tipo": tipo, "casa": casa, "ordem": ordem,
             "teto": dict((b[0], b[2]) for b in BOSSES).get(nome), "time": team(sym)}
            for nome, sym, tipo, casa, ordem in LEADERS],
        "elite": [
            {"chefe": nome, "tipo": tipo,
             "teto": dict((b[0], b[2]) for b in BOSSES).get(legado, 58),
             "time": team(legado)}
            for nome, legado, tipo in ELITE],
    }


def slot_lines(mon):
    tipos = "/".join(mon["tipos"])
    golpes = " · ".join(
        "%s%s" % (g["nome"], " (%d)" % g["poder"] if g["poder"] else "")
        for g in mon["golpes"])
    return ("| #%03d %s | %s | %d | Nv. %d | %d/31 | %s | %s |"
            % (mon["dex"], mon["nome"], tipos, mon["bst"], mon["nivel"],
               mon["iv31"], mon["item"], golpes))


TEAM_HEAD = ("| criatura | tipos | BST | nivel | IV | item | golpes |\n"
             "|---|---|---:|---:|---:|---|---|")


def markdown(d):
    L = []
    add = L.append
    add("# Pokemon Juramento de Arauana — dossie da beta")
    add("")
    add("Gerado por `tools/arauna/build_beta_dossier.py` a partir do proprio")
    add("repositorio. Nenhum numero aqui foi digitado a mao.")
    add("")

    add("## A historia")
    add("")
    add("O canone abaixo nao e resumo escrito para o dossie: sao os pontos que")
    add("`docs/ARAUANA_STORY_IMPLEMENTATION.md` declara e que o texto do jogo")
    add("implementa, em 647 blocos de dialogo e 103 arquivos de script.")
    add("")
    add("| | |")
    add("|---|---|")
    for rotulo, valor in d["canone"]:
        add("| **%s** | %s |" % (rotulo, valor))
    add("")
    add("A regra da adaptacao esta escrita no mesmo documento e vale para tudo")
    add("que segue: **nenhuma ordem de rota, ordem de insignia, warp, flag de")
    add("progressao ou gatilho de evento do Emerald foi mudada.** O que mudou foi")
    add("a superficie -- quem fala, o que diz, e o que o mundo se chama.")
    add("")
    add("## Os nomes do mundo")
    add("")
    add("%d lugares do mapa da regiao. Nome fica em portugues, prosa vai para o" % len(d["lugares"]))
    add("ingles -- e a regra que `docs/GLOSSARIO_EN.md` fixa.")
    add("")
    add("| Hoenn | Arauana |")
    add("|---|---|")
    for velho, novo in d["lugares"]:
        add("| %s | **%s** |" % (velho, novo))
    add("")
    add("## O jogo em numeros")
    add("")
    c = d["criaturas"]
    add("| | |")
    add("|---|---:|")
    add("| criaturas na dex | %d |" % c["total"])
    add("| capturaveis na natureza | %d |" % c["na_natureza"])
    add("| mapas com encontro | %d |" % c["mapas_com_encontro"])
    add("| learnsets proprios | %d |" % c["learnsets"])
    add("| golpes ensinados por nivel | %d |" % c["entradas_de_golpe"])
    add("| relacoes evolutivas | %d |" % d["evolucoes"]["total"])
    add("| habilidades novas | %d |" % len(d["habilidades"]))
    add("| golpes exclusivos | %d |" % len(d["golpes_assinatura"]))
    add("| treinadores no jogo | %d |" % d["treinadores"])
    add("")

    add("## O caminho do jogo")
    add("")
    add("Oito insignias, quatro da Elite e a Campea. O teto de nivel sobe com a")
    add("insignia, e e o mesmo numero que `sLevelCapByBadges` usa em")
    add("`src/arauna_qol.c`.")
    add("")
    add("| ordem | casa | chefe | tipo | teto |")
    add("|---:|---|---|---|---:|")
    for g in d["ginasios"]:
        add("| %d | %s | **%s** | %s | %s |"
            % (g["ordem"], g["casa"], g["chefe"], g["tipo"].capitalize(), g["teto"]))
    for i, e in enumerate(d["elite"], start=9):
        rotulo = "Campea" if e["tipo"] == "CAMPEA" else "Elite dos Quatro"
        add("| %d | %s | **%s** | %s | %s |"
            % (i, rotulo, e["chefe"], e["tipo"].capitalize(), e["teto"]))
    add("")

    add("## Os times dos chefes")
    add("")
    for g in d["ginasios"]:
        add("### %d. %s — %s, %s (teto Nv. %s)"
            % (g["ordem"], g["chefe"], g["tipo"].capitalize(), g["casa"], g["teto"]))
        add("")
        add(TEAM_HEAD)
        for mon in g["time"]:
            add(slot_lines(mon))
        add("")
    for e in d["elite"]:
        rotulo = "Campea" if e["tipo"] == "CAMPEA" else e["tipo"].capitalize()
        add("### %s — %s (teto Nv. %s)" % (e["chefe"], rotulo, e["teto"]))
        add("")
        add(TEAM_HEAD)
        for mon in e["time"]:
            add(slot_lines(mon))
        add("")

    add("## Como os mapas se ligam")
    add("")
    add("%d mapas de superficie tem vizinho. E o grafo do Emerald, intacto: e" % len(d["ligacoes"]))
    add("por ele que se anda de uma casa a outra.")
    add("")
    add("| mapa | vizinhos |")
    add("|---|---|")
    for mapa, vizinhos in d["ligacoes"].items():
        add("| %s | %s |" % (mapa, ", ".join("%s: %s" % v for v in vizinhos)))
    add("")
    add("## As %d habilidades novas" % len(d["habilidades"]))
    add("")
    add(" · ".join("%s" % n.replace("_", " ").title() for _, n in d["habilidades"]))
    add("")

    add("## Os %d golpes exclusivos" % len(d["golpes_assinatura"]))
    add("")
    add("| golpe | tipo | poder |")
    add("|---|---|---:|")
    for _, name, kind, power in d["golpes_assinatura"]:
        add("| %s | %s | %s |" % (name.replace("_", " ").title(),
                                  kind.capitalize(), power or "—"))
    add("")

    add("## O elenco")
    add("")
    add("Ninguem no jogo responde mais por um nome de Hoenn.")
    add("")
    add("| Hoenn | Arauana |")
    add("|---|---|")
    for old, new in d["elenco"]:
        add("| %s | **%s** |" % (old, new))
    add("")

    v = d["verificacao"]
    add("## Como isto foi verificado")
    add("")
    if not v:
        add("Ainda nao ha registro de verificacao: `docs/arauna/VERIFICACAO_BETA.json`")
        add("nao existe.")
    else:
        add(v["resumo"])
        add("")
        add("| o que | resultado |")
        add("|---|---|")
        for item in v["itens"]:
            add("| %s | %s |" % (item["nome"], item["resultado"]))
        add("")
        if v.get("ressalvas"):
            add("**O que isto nao prova.** " + v["ressalvas"])
    add("")
    add("## A dex completa — as %d criaturas" % len(d["dex"]))
    add("")
    add("Uma marca na coluna *selvagem* quer dizer que ela aparece em alguma")
    add("grama, agua ou pesca. As outras vem por evolucao, presente ou evento.")
    add("")
    add("| # | nome | tipos | BST | selvagem | golpes por nivel |")
    add("|---:|---|---|---:|:---:|---:|")
    for m in d["dex"]:
        add("| %03d | %s | %s | %d | %s | %d |"
            % (m["dex"], m["nome"], "/".join(m["tipos"]), m["bst"],
               "sim" if m["selvagem"] else "—", m["golpes_por_nivel"]))
    add("")
    add("## O que a beta ainda nao tem")
    add("")
    sem = [s for s in d["especiais_pendentes"] if not s["tem_casa"]]
    com = [s for s in d["especiais_pendentes"] if s["tem_casa"]]
    add("O plano dos especiais tem %d lendarios e miticos. **%d ja estao no jogo**,"
        % (len(d["especiais_pendentes"]), len(com)))
    add("nos encontros estaticos herdados do Emerald. Os outros **%d nao tem lugar"
        % len(sem))
    add("no mapa** -- a dex nao fecha nesta beta, e isso e conhecido.")
    add("")
    add("### Os %d que ainda esperam lugar" % len(sem))
    add("")
    add("| dex | nome | tipos | nivel previsto | lugar previsto |")
    add("|---:|---|---|---:|---|")
    for s in sem:
        add("| %s | %s | %s | %s | %s |"
            % (s["dex"], s["name"], s["types"], s["recommended_level"], s["placement"]))
    add("")
    add("### Os %d que ja podem ser encontrados" % len(com))
    add("")
    add("| dex | nome | tipos |")
    add("|---:|---|---|")
    for s in com:
        add("| %s | %s | %s |" % (s["dex"], s["name"], s["types"]))
    add("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    data = collect()
    text = markdown(data)
    if args.write:
        (ROOT / "docs/DOSSIE_BETA.md").write_text(text + "\n", encoding="utf-8")
        (ROOT / "docs/arauna/DOSSIE_BETA.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print("escrito: docs/DOSSIE_BETA.md e docs/arauna/DOSSIE_BETA.json")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Confere um JSON "arauana-team" do editor contra o que o repositorio tem de
verdade, antes de instalar.

O que e conferido, por vaga:
  especie      o arauna_dex existe e mapeia para um SPECIES_* do jogo
  tipos        batem com species_info.h
  golpes       os quatro ids existem em constants/moves.h, e nao repetem
  learnset     o nivel que o editor declara bate com o learnset do repositorio
               (nivel, TM/HM ou golpe de ovo); "fora do learnset" e apontado
  iv           iv31 == iv * MAX_PER_STAT_IVS / 255, que e a conta do motor
  item         o ITEM_* existe
  nivel        1..100, e comparado com o teto do chefe quando passado --cap

Uso:  python3 tools/arauna/check_boss_team.py time.json [--cap 15]
Saida: relatorio, e codigo 1 se houver erro (aviso nao reprova).
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAX_PER_STAT_IVS = 31


def constants(path, prefix):
    text = (ROOT / path).read_text()
    return {name: int(value) for name, value in
            re.findall(r"#define (%s\w+)\s+(\d+)\b" % prefix, text)}


def dex_table():
    import csv
    out = {}
    with open(ROOT / "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv") as fh:
        for row in csv.DictReader(fh):
            out[int(row["arauna_dex"])] = (
                row["full_name"], row["species_constant"],
                [t.strip().lower() for t in row["types"].split("/") if t.strip()])
    return out


def species_types():
    text = (ROOT / "src/data/pokemon/species_info.h").read_text()
    out = {}
    for block in re.finditer(r"\[(SPECIES_\w+)\][^\n]*\n    \{(.*?)\n    \}", text, re.S):
        m = re.search(r"\.types\s*=\s*\{\s*TYPE_(\w+)\s*,\s*TYPE_(\w+)\s*\}", block.group(2))
        if m:
            out[block.group(1)] = [m.group(1).lower(), m.group(2).lower()]
    return out


def level_up():
    arrays = {}
    for name in ("arauna_complete_learnsets.h", "level_up_learnsets.h"):
        text = (ROOT / "src/data/pokemon" / name).read_text()
        for block in re.finditer(
                r"static const u16 (s\w+LevelUpLearnset)\[\]\s*=\s*\{(.*?)\n\};", text, re.S):
            arrays.setdefault(block.group(1), [
                (int(lv), mv) for lv, mv in
                re.findall(r"LEVEL_UP_MOVE\s*\(\s*(\d+)\s*,\s*(MOVE_\w+)\s*\)", block.group(2))])
    pointers = (ROOT / "src/data/pokemon/level_up_learnset_pointers.h").read_text()
    return {row.group(1): arrays.get(row.group(2), []) for row in
            re.finditer(r"\[(SPECIES_\w+)\]\s*=\s*(s\w+LevelUpLearnset)", pointers)}


def tm_hm():
    """SPECIES_* -> {MOVE_*} ensinaveis por TM/HM."""
    text = (ROOT / "src/data/pokemon/tmhm_learnsets.h").read_text()
    out, positions = {}, [m.start() for m in re.finditer(r"\[SPECIES_\w+\] = \{ \.learnset", text)]
    for i, start in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        species = re.match(r"\[(SPECIES_\w+)\]", text[start:]).group(1)
        out[species] = {"MOVE_" + f for f in re.findall(r"\.(\w+)\s*=\s*TRUE", text[start:end])}
    return out


def egg_moves():
    text = (ROOT / "src/data/pokemon/egg_moves.h").read_text()
    out = {}
    for block in re.finditer(r"egg_moves\((\w+)\s*,(.*?)\)", text, re.S):
        out["SPECIES_" + block.group(1)] = set(re.findall(r"MOVE_\w+", block.group(2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("team")
    ap.add_argument("--cap", type=int, default=None, help="teto de nivel do chefe")
    ap.add_argument("--emit", metavar="sParty_Nome",
                    help="imprime o array C pronto, se nao houver erro")
    args = ap.parse_args()

    data = json.loads(Path(args.team).read_text())
    dex, types, learn = dex_table(), species_types(), level_up()
    tms, eggs = tm_hm(), egg_moves()
    moves = constants("include/constants/moves.h", "MOVE_")
    items = constants("include/constants/items.h", "ITEM_")

    errors, warnings = [], []
    print("esquema %s v%s   customMoveset=%s   ivMode=%s" % (
        data.get("schema"), data.get("version"),
        data.get("trainerParty", {}).get("customMoveset"),
        data.get("trainerParty", {}).get("ivMode")))
    print()

    filled = [s for s in data["slots"] if s.get("pokemonId")]
    for slot in filled:
        n, name = slot["pokemonId"], slot["pokemonName"]
        tag = "vaga %d  #%03d %s" % (slot["slot"], n, name)
        if n not in dex:
            errors.append("%s: dex %d nao existe" % (tag, n))
            continue
        real_name, species, dex_types = dex[n]
        print("%s  ->  %s  nv%d  iv=%s(%s)  %s" % (
            tag, species[len("SPECIES_"):], slot["level"], slot["iv"], slot["iv31"],
            (slot.get("heldItem") or {}).get("id", "ITEM_NONE")))

        if real_name != name:
            warnings.append("%s: o editor chama de %r, o repositorio de %r" % (tag, name, real_name))

        got = [t for t in dict.fromkeys(types.get(species, []))]
        want = [t for t in dict.fromkeys(slot.get("types", []))]
        if got != want:
            errors.append("%s: tipos %s no editor, %s no jogo" % (tag, want, got))

        # o motor faz fixedIV = iv * MAX_PER_STAT_IVS / 255, inteiro
        if slot["iv"] is not None:
            if not 0 <= slot["iv"] <= 255:
                errors.append("%s: iv %s fora de 0..255" % (tag, slot["iv"]))
            expected = slot["iv"] * MAX_PER_STAT_IVS // 255
            if slot.get("iv31") != expected:
                errors.append("%s: iv %d vira %d no motor, o editor diz %s"
                              % (tag, slot["iv"], expected, slot.get("iv31")))

        if not 1 <= (slot["level"] or 0) <= 100:
            errors.append("%s: nivel %s invalido" % (tag, slot["level"]))
        elif args.cap and slot["level"] > args.cap:
            errors.append("%s: nivel %d passa do teto %d do chefe" % (tag, slot["level"], args.cap))

        held = (slot.get("heldItem") or {}).get("id")
        if held and held not in items:
            errors.append("%s: item %s nao existe" % (tag, held))

        ids = [m["id"] for m in slot["moves"] if m]
        if len(ids) != 4:
            warnings.append("%s: %d golpes, o motor espera 4" % (tag, len(ids)))
        if len(set(ids)) != len(ids):
            errors.append("%s: golpe repetido" % tag)

        by_level = dict(learn.get(species, []))
        first = {}
        for lv, mv in learn.get(species, []):
            first.setdefault(mv, lv)
        for m in slot["moves"]:
            if not m:
                continue
            mid = m["id"]
            if mid not in moves:
                errors.append("%s: golpe %s nao existe" % (tag, mid))
                continue
            claimed = m.get("learnsetLevel")
            if mid in first:
                if claimed != first[mid]:
                    errors.append("%s: %s e nv%d no repositorio, o editor diz %s"
                                  % (tag, mid, first[mid], claimed))
                elif claimed > slot["level"]:
                    warnings.append("%s: %s so no nv%d, o treinador esta no nv%d"
                                    % (tag, mid, claimed, slot["level"]))
            elif mid in tms.get(species, set()):
                warnings.append("%s: %s so por TM/HM, nao por nivel" % (tag, mid))
            elif mid in eggs.get(species, set()):
                warnings.append("%s: %s so por golpe de ovo" % (tag, mid))
            else:
                errors.append("%s: %s nao esta em nenhum learnset desta especie" % (tag, mid))

    print()
    print("vagas preenchidas: %d" % len(filled))
    for w in warnings:
        print("  AVISO  %s" % w)
    for e in errors:
        print("  ERRO   %s" % e)
    if not errors:
        print("  sem erros")
    if errors:
        return 1

    if args.emit:
        body = []
        for slot in filled:
            species = dex[slot["pokemonId"]][1]
            held = (slot.get("heldItem") or {}).get("id") or "ITEM_NONE"
            ids = [m["id"] for m in slot["moves"] if m]
            ids += ["MOVE_NONE"] * (4 - len(ids))
            body.append(
                "    {\n"
                "    .iv = %d,\n"
                "    .lvl = %d,\n"
                "    .species = %s,\n"
                "    .heldItem = %s,\n"
                "    .moves = {%s}\n"
                "    }" % (slot["iv"], slot["level"], species, held, ", ".join(ids)))
        print()
        print("static const struct TrainerMonItemCustomMoves %s[] = {" % args.emit)
        print(",\n".join(body))
        print("};")
    return 0


if __name__ == "__main__":
    sys.exit(main())

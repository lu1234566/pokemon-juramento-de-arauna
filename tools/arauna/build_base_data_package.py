#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re, hashlib, shutil, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
POKEDEX=ROOT/"tools/arauna/package_sources/lovable/pokedex.ts"
MAPPING=ROOT/"docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
SPECIES_INFO=ROOT/"src/data/pokemon/species_info.h"

STARTER_FAMILY=set(range(1,10))
PSEUDO_FAMILY={46,47,48}
TYPE_C={
"normal":"TYPE_NORMAL","fighting":"TYPE_FIGHTING","flying":"TYPE_FLYING","poison":"TYPE_POISON",
"ground":"TYPE_GROUND","rock":"TYPE_ROCK","bug":"TYPE_BUG","ghost":"TYPE_GHOST","steel":"TYPE_STEEL",
"fire":"TYPE_FIRE","water":"TYPE_WATER","grass":"TYPE_GRASS","electric":"TYPE_ELECTRIC",
"psychic":"TYPE_PSYCHIC","ice":"TYPE_ICE","dragon":"TYPE_DRAGON","dark":"TYPE_DARK","fairy":"TYPE_FAIRY"}
BOOSTER={
"normal":"ITEM_SILK_SCARF","fighting":"ITEM_BLACK_BELT","flying":"ITEM_SHARP_BEAK",
"poison":"ITEM_POISON_BARB","ground":"ITEM_SOFT_SAND","rock":"ITEM_HARD_STONE",
"bug":"ITEM_SILVER_POWDER","ghost":"ITEM_SPELL_TAG","steel":"ITEM_METAL_COAT",
"fire":"ITEM_CHARCOAL","water":"ITEM_MYSTIC_WATER","grass":"ITEM_MIRACLE_SEED",
"electric":"ITEM_MAGNET","psychic":"ITEM_TWISTED_SPOON","ice":"ITEM_NEVER_MELT_ICE",
"dragon":"ITEM_DRAGON_FANG","dark":"ITEM_BLACK_GLASSES"}

def objects(text):
    """Extract only top-level objects from the POKEDEX array.

    Evolution targets and stats contain nested object literals, so searching for
    '{ id:' directly incorrectly treats those as Pokémon.
    """
    marker=text.index("export const POKEDEX")
    i=text.index("[",marker)
    out=[]; square=0; curly=0; q=False; esc=False; obj_start=None
    while i<len(text):
        c=text[i]
        if q:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': q=False
        else:
            if c=='"':
                q=True
            elif c=="[":
                square+=1
            elif c=="]":
                square-=1
                if square==0: break
            elif c=="{" and square==1:
                if curly==0: obj_start=i
                curly+=1
            elif c=="}" and square==1 and curly:
                curly-=1
                if curly==0 and obj_start is not None:
                    out.append(text[obj_start:i+1]); obj_start=None
        i+=1
    return out

def field(o,key):
    m=re.search(rf'\b{key}:\s*"([^"]*)"',o)
    return m.group(1) if m else ""

def parse_pokedex():
    text=POKEDEX.read_text(encoding="utf-8")
    mons=[]
    for o in objects(text):
        mi=re.search(r"\bid:\s*(\d+)",o)
        if not mi: continue
        dex=int(mi.group(1))
        name=field(o,"name")
        types=re.findall(r'"([^"]+)"',(re.search(r"\btypes:\s*\[([^\]]*)\]",o) or ["",""])[1])
        sm=(re.search(r"\bstats:\s*\{([^}]*)\}",o) or ["",""])[1]
        stats={k:int(v) for k,v in re.findall(r"(hp|atk|def|spa|spd|spe):\s*(\d+)",sm)}
        evo_to=[int(x) for x in re.findall(r"\bid:\s*(\d+)",(re.search(r"\bevolvesTo:\s*\[([^\]]*)\]",o) or ["",""])[1])]
        ef=re.search(r"\bevolvesFrom:\s*(\d+)",o)
        mons.append({
            "dex":dex,"name":name,"types":types,"stats":stats,
            "category":field(o,"category"),"inspiration":field(o,"inspiration"),"dex_text":field(o,"dex"),
            "legendary":bool(re.search(r"\blegendary:\s*true",o)),
            "mythical":bool(re.search(r"\bmythical:\s*true",o)),
            "evolves_to":evo_to,"evolves_from":int(ef.group(1)) if ef else None})
    mons.sort(key=lambda x:x["dex"])
    if [m["dex"] for m in mons] != list(range(1,387)):
        raise SystemExit(f"Pokédex parse incomplete: {len(mons)} entries")
    return mons

def mapping():
    with MAPPING.open(encoding="utf-8") as f:
        return {int(r["arauna_dex"]):r for r in csv.DictReader(f)}

def current_rows():
    text=SPECIES_INFO.read_text(encoding="utf-8")
    rows={}
    pat=re.compile(r"    \[(SPECIES_\w+)\] = // #(\d{3}) .*?\n    \{(.*?)\n    \},",re.S)
    for m in pat.finditer(text):
        body=m.group(3)
        def val(k,default):
            x=re.search(rf"\.{k}\s*=\s*([^,\n]+)",body); return x.group(1).strip() if x else default
        ab=re.search(r"\.abilities\s*=\s*\{([^}]+)\}",body)
        rows[int(m.group(2))]={
          "constant":m.group(1),"abilities":ab.group(1).strip() if ab else "ABILITY_NONE, ABILITY_NONE",
          "bodyColor":val("bodyColor","BODY_COLOR_BROWN"),"noFlip":val("noFlip","FALSE"),
          "safariZoneFleeRate":val("safariZoneFleeRate","0")}
    return rows

def family_meta(mons):
    by={m["dex"]:m for m in mons}
    def root(d):
        seen=set()
        while by[d]["evolves_from"] and d not in seen:
            seen.add(d); d=by[d]["evolves_from"]
        return d
    def path(r):
        p=[r]; seen=set()
        while by[p[-1]]["evolves_to"] and p[-1] not in seen:
            seen.add(p[-1]); p.append(by[p[-1]]["evolves_to"][0])
        return p
    meta={}
    for m in mons:
        r=root(m["dex"]); fam=path(r)
        meta[m["dex"]]={"root":r,"family":fam,"family_len":len(fam),"stage":fam.index(m["dex"])+1 if m["dex"] in fam else 1}
    return meta

def catch_rate(m,f):
    d=m["dex"]; bst=sum(m["stats"].values())
    if m["legendary"] or m["mythical"]: return 3
    if d in STARTER_FAMILY or d in PSEUDO_FAMILY: return 45
    if f["family_len"]>=3:
        return [180,90,45][min(f["stage"],3)-1]
    if f["family_len"]==2:
        return 190 if f["stage"]==1 else 75
    if bst<=350:return 200
    if bst<=450:return 120
    if bst<=525:return 75
    return 45

def exp_yield(m,f):
    bst=sum(m["stats"].values()); d=m["dex"]
    if m["legendary"] or m["mythical"]: return min(255,max(180,round(bst*.36)))
    if d in PSEUDO_FAMILY:
        return [90,150,220][min(f["stage"],3)-1]
    if f["family_len"]>=3:
        ratios=[.28,.32,.39]; bounds=[(45,125),(90,170),(140,220)]
        lo,hi=bounds[min(f["stage"],3)-1]
        return min(hi,max(lo,round(bst*ratios[min(f["stage"],3)-1])))
    if f["family_len"]==2:
        if f["stage"]==1:return min(135,max(50,round(bst*.29)))
        return min(210,max(120,round(bst*.37)))
    return min(210,max(55,round(bst*.34)))

def ev_yield(m,f):
    stats=m["stats"]; bst=sum(stats.values())
    if m["legendary"] or m["mythical"] or (f["stage"]==f["family_len"] and f["family_len"]>1):
        total=3
    elif f["stage"]>1: total=2
    elif f["family_len"]==1 and bst>=480: total=2
    else: total=1
    order=sorted(stats.items(),key=lambda kv:(-kv[1],["hp","atk","def","spa","spd","spe"].index(kv[0])))
    ev={k:0 for k in stats}
    if total==1: ev[order[0][0]]=1
    elif total==2:
        if order[0][1]-order[1][1]>=15:ev[order[0][0]]=2
        else: ev[order[0][0]]=ev[order[1][0]]=1
    else:
        if order[0][1]-order[1][1]>=20: ev[order[0][0]]=2; ev[order[1][0]]=1
        elif order[0][1]-order[2][1]<=10:
            for k,_ in order[:3]: ev[k]=1
        else: ev[order[0][0]]=2; ev[order[1][0]]=1
    return ev

def gender(m):
    if m["legendary"] or m["mythical"]: return "MON_GENDERLESS"
    if m["dex"] in STARTER_FAMILY:return "PERCENT_FEMALE(12.5)"
    return "PERCENT_FEMALE(50)"

def egg_cycles(m,f):
    if m["legendary"] or m["mythical"]:return 120
    if m["dex"] in PSEUDO_FAMILY:return 40
    if "bug" in m["types"] and f["stage"]==1:return 15
    if f["family_len"]>=3:return [15,20,25][min(f["stage"],3)-1]
    if f["family_len"]==2:return 15 if f["stage"]==1 else 20
    return 20

def friendship(m):
    if m["mythical"]:return 100
    if m["legendary"]:return 35
    if m["dex"] in PSEUDO_FAMILY:return 35
    return 70

def growth(m,f):
    if m["legendary"] or m["mythical"] or m["dex"] in PSEUDO_FAMILY:return "GROWTH_SLOW"
    if m["dex"] in STARTER_FAMILY:return "GROWTH_MEDIUM_SLOW"
    if "bug" in m["types"] and f["family_len"]>=2:return "GROWTH_FAST"
    if f["family_len"]>=3:return "GROWTH_MEDIUM_SLOW"
    if f["family_len"]==1 and sum(m["stats"].values())>=520:return "GROWTH_SLOW"
    return "GROWTH_MEDIUM_FAST"

def egg_groups(m):
    if m["legendary"] or m["mythical"]:
        return ["EGG_GROUP_NO_EGGS_DISCOVERED"]*2
    t=m["types"]; lore=(m["name"]+" "+m["category"]+" "+m["inspiration"]+" "+m["dex_text"]).lower()
    def has(*w):return any(x in lore for x in w)
    if "bug" in t:
        return ["EGG_GROUP_BUG","EGG_GROUP_FLYING" if "flying" in t else ("EGG_GROUP_GRASS" if "grass" in t else "EGG_GROUP_BUG")]
    if "dragon" in t:
        second="EGG_GROUP_DRAGON"
        if "water" in t:second="EGG_GROUP_WATER_1"
        elif "flying" in t:second="EGG_GROUP_FLYING"
        elif "rock" in t or "steel" in t:second="EGG_GROUP_MINERAL"
        elif "grass" in t:second="EGG_GROUP_GRASS"
        elif "fairy" in t:second="EGG_GROUP_FAIRY"
        elif has("cachorro","lobo","onça","jaguar","mamífer","cavalo"):second="EGG_GROUP_FIELD"
        return ["EGG_GROUP_DRAGON",second]
    if "flying" in t or has("ave","pássaro","arara","tucano","quero-quero","pica-pau","beija-flor"):
        return ["EGG_GROUP_FLYING","EGG_GROUP_FIELD" if "grass" not in t else "EGG_GROUP_GRASS"]
    if "water" in t:
        if has("peixe","pirarucu","sard","tubar","bagre"):return ["EGG_GROUP_WATER_2","EGG_GROUP_WATER_2"]
        if has("cobra","sucuri","jacaré","tartaruga"):return ["EGG_GROUP_WATER_1","EGG_GROUP_DRAGON"]
        if "fairy" in t:return ["EGG_GROUP_WATER_1","EGG_GROUP_FAIRY"]
        return ["EGG_GROUP_WATER_1","EGG_GROUP_WATER_1"]
    if "grass" in t:
        return ["EGG_GROUP_GRASS","EGG_GROUP_FAIRY" if "fairy" in t else "EGG_GROUP_FIELD"]
    if "rock" in t or "steel" in t:
        return ["EGG_GROUP_MINERAL","EGG_GROUP_FIELD"]
    if "ghost" in t:
        return ["EGG_GROUP_AMORPHOUS","EGG_GROUP_FAIRY" if "fairy" in t else "EGG_GROUP_AMORPHOUS"]
    if "psychic" in t and has("espírito","entidade","fantasma"):
        return ["EGG_GROUP_AMORPHOUS","EGG_GROUP_AMORPHOUS"]
    if "fighting" in t or has("humano","guerreiro","homem","mulher"):
        return ["EGG_GROUP_HUMAN_LIKE","EGG_GROUP_FIELD"]
    if "fairy" in t:
        return ["EGG_GROUP_FAIRY","EGG_GROUP_FIELD"]
    return ["EGG_GROUP_FIELD","EGG_GROUP_FIELD"]

def held_items(m,f):
    d=m["dex"]; bst=sum(m["stats"].values())
    if m["legendary"] or m["mythical"] or d in STARTER_FAMILY:return ("ITEM_NONE","ITEM_NONE")
    eligible=(f["stage"]==f["family_len"] and (f["family_len"]>1 or bst>=480))
    if not eligible:return ("ITEM_NONE","ITEM_NONE")
    if d==48:return ("ITEM_NONE","ITEM_DRAGON_FANG")
    for typ in m["types"]:
        if typ in BOOSTER:return ("ITEM_NONE",BOOSTER[typ])
    return ("ITEM_NONE","ITEM_NONE")

def audit(mons,fam):
    findings=[]
    by={m["dex"]:m for m in mons}
    spreads={}
    for m in mons:
        bst=sum(m["stats"].values())
        if bst<250: findings.append(("WARN",m["dex"],m["name"],f"BST muito baixo: {bst}"))
        if bst>600 and not (m["legendary"] or m["mythical"]):
            findings.append(("HIGH",m["dex"],m["name"],f"BST {bst} acima de 600 sem flag Legendary/Mythical"))
        if m["dex"] in {3,6,9} and bst>550:
            findings.append(("HIGH",m["dex"],m["name"],f"Starter final BST {bst}; alvo clássico costuma ficar ~525-535"))
        key=tuple(m["stats"][k] for k in ["hp","atk","def","spa","spd","spe"])
        spreads.setdefault(key,[]).append(m["dex"])
        for nxt in m["evolves_to"]:
            if nxt in by and sum(by[nxt]["stats"].values()) <= bst:
                findings.append(("HIGH",m["dex"],m["name"],f"Evolui para #{nxt:03d} sem aumento de BST ({bst} -> {sum(by[nxt]['stats'].values())})"))
    for spread,ids in spreads.items():
        if len(ids)>=4:
            findings.append(("WARN",ids[0],by[ids[0]]["name"],f"Spread exato {spread} repetido em {len(ids)} espécies: {ids}"))
    return findings

def main():
    if len(sys.argv)<2: raise SystemExit("usage: build_base_data_package.py OUT_DIR")
    out=Path(sys.argv[1])
    if out.exists():shutil.rmtree(out)
    for d in ["master","generated","reports","docs"]: (out/d).mkdir(parents=True,exist_ok=True)
    mons=parse_pokedex(); mp=mapping(); cur=current_rows(); fam=family_meta(mons)
    result=[]
    for m in mons:
        f=fam[m["dex"]]; common,rare=held_items(m,f)
        row={
          "dex":m["dex"],"name":m["name"],"species_constant":mp[m["dex"]]["species_constant"],
          "types":m["types"],"stats":m["stats"],"bst":sum(m["stats"].values()),
          "family_root":f["root"],"family_length":f["family_len"],"evolution_stage":f["stage"],
          "legendary":m["legendary"],"mythical":m["mythical"],"pseudo_family":m["dex"] in PSEUDO_FAMILY,
          "catch_rate":catch_rate(m,f),"exp_yield":exp_yield(m,f),"ev_yield":ev_yield(m,f),
          "gender_ratio":gender(m),"egg_cycles":egg_cycles(m,f),"friendship":friendship(m),
          "growth_rate":growth(m,f),"egg_groups":egg_groups(m),
          "item_common":common,"item_rare":rare,
          "abilities_preserved":cur.get(m["dex"],{}).get("abilities","ABILITY_NONE, ABILITY_NONE"),
          "body_color_preserved":cur.get(m["dex"],{}).get("bodyColor","BODY_COLOR_BROWN"),
          "no_flip_preserved":cur.get(m["dex"],{}).get("noFlip","FALSE")}
        result.append(row)
    (out/"master/base_data_386.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    with (out/"master/base_data_386.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["dex","name","species","types","bst","hp","atk","def","spa","spd","spe","catch_rate","exp_yield","ev_hp","ev_atk","ev_def","ev_spa","ev_spd","ev_spe","gender_ratio","egg_cycles","friendship","growth_rate","egg_group_1","egg_group_2","item_common","item_rare","family_root","family_length","stage","legendary","mythical","pseudo_family"])
        for r in result:
            ev=r["ev_yield"]; st=r["stats"]
            w.writerow([r["dex"],r["name"],r["species_constant"],"/".join(r["types"]),r["bst"],st["hp"],st["atk"],st["def"],st["spa"],st["spd"],st["spe"],r["catch_rate"],r["exp_yield"],ev["hp"],ev["atk"],ev["def"],ev["spa"],ev["spd"],ev["spe"],r["gender_ratio"],r["egg_cycles"],r["friendship"],r["growth_rate"],*r["egg_groups"],r["item_common"],r["item_rare"],r["family_root"],r["family_length"],r["evolution_stage"],r["legendary"],r["mythical"],r["pseudo_family"]])
    # full C preview; preserve current abilities/body color
    lines=["// Generated Arauna Base Data v2 preview.","// Abilities/bodyColor/noFlip are intentionally preserved from the current ROM.",""]
    for r in result:
        st=r["stats"];ev=r["ev_yield"];types=[TYPE_C[x] for x in r["types"]]; types=(types+[types[0]])[:2]
        lines += [f"[{r['species_constant']}] = // #{r['dex']:03d} {r['name']}","{",
          f"    .baseHP = {st['hp']}, .baseAttack = {st['atk']}, .baseDefense = {st['def']},",
          f"    .baseSpeed = {st['spe']}, .baseSpAttack = {st['spa']}, .baseSpDefense = {st['spd']},",
          f"    .types = {{ {types[0]}, {types[1]} }}, .catchRate = {r['catch_rate']}, .expYield = {r['exp_yield']},",
          f"    .evYield_HP = {ev['hp']}, .evYield_Attack = {ev['atk']}, .evYield_Defense = {ev['def']},",
          f"    .evYield_Speed = {ev['spe']}, .evYield_SpAttack = {ev['spa']}, .evYield_SpDefense = {ev['spd']},",
          f"    .itemCommon = {r['item_common']}, .itemRare = {r['item_rare']},",
          f"    .genderRatio = {r['gender_ratio']}, .eggCycles = {r['egg_cycles']}, .friendship = {r['friendship']},",
          f"    .growthRate = {r['growth_rate']}, .eggGroups = {{ {r['egg_groups'][0]}, {r['egg_groups'][1]} }},",
          f"    .abilities = {{ {r['abilities_preserved']} }}, .safariZoneFleeRate = 0,",
          f"    .bodyColor = {r['body_color_preserved']}, .noFlip = {r['no_flip_preserved']},","};",""]
    (out/"generated/species_info_base_data_preview.h").write_text("\n".join(lines),encoding="utf-8")
    findings=audit(mons,fam)
    with (out/"reports/audit_findings.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f);w.writerow(["severity","dex","species","finding"]);w.writerows(findings)
    md=["# Auditoria Base Data — Arauana","",f"Espécies: {len(result)}",f"Achados: {len(findings)}","",
        "O pacote NÃO altera silenciosamente os seis base stats aprovados. Outliers ficam listados abaixo para decisão de balanceamento.",""]
    for sev,d,n,msg in findings: md.append(f"- **{sev}** #{d:03d} {n}: {msg}")
    (out/"reports/AUDIT_FINDINGS.md").write_text("\n".join(md)+"\n",encoding="utf-8")
    rules="""# Base Data v2 — regras

## Princípios
- Os seis base stats e tipos vêm do Pokédex aprovado; a auditoria apenas sinaliza outliers.
- Starters seguem convenções de captura/gênero/crescimento de starters Pokémon.
- A família pseudo-lendária #046–#048 recebe crescimento Slow, catch 45 e egg cycle 40.
- Legendary/Mythical: catch 3, genderless, Undiscovered, 120 egg cycles.
- Mythical usa friendship 100; Legendary usa 35.
- EV yield total: 1 em básicos, 2 em intermediários/standalones fortes, 3 em finais/especiais.
- Egg groups usam anatomia/lore + tipos, não apenas o tipo primário.
- Held items são conservadores: nenhum item comum; finais elegíveis podem ter 5% de item amplificador do tipo. Starters e especiais não viram farms de item.
- Abilities, bodyColor e noFlip são preservados: abilities pertencem ao pacote específico já criado.

## Catch rate
Starter family 45; pseudo family 45; especiais 3.
3 estágios: 180/90/45. 2 estágios: 190/75.
Standalone: 200/120/75/45 por faixa de BST.

## Growth
Starter: Medium Slow. Pseudo/especiais: Slow. Bugs evolutivos: Fast.
Demais 3-estágios: Medium Slow; standalones >=520 BST: Slow; resto Medium Fast.

## Segurança
O arquivo generated/species_info_base_data_preview.h é uma prévia completa.
Antes de aplicar ao ROM, revisar reports/AUDIT_FINDINGS.md, especialmente os starters finais e spreads duplicados.
"""
    (out/"docs/BASE_DATA_RULES.md").write_text(rules,encoding="utf-8")
    summary={
      "species":386,"legendary":sum(r["legendary"] for r in result),
      "mythical":sum(r["mythical"] for r in result),
      "pseudo_family_members":sum(r["pseudo_family"] for r in result),
      "audit_findings":len(findings),
      "rare_item_species":sum(r["item_rare"]!="ITEM_NONE" for r in result),
      "genderless":sum(r["gender_ratio"]=="MON_GENDERLESS" for r in result)}
    (out/"reports/summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    readme="""# Arauna Base Data 386 v2

Pacote completo do item 1: stats/tipos + catch rate + EXP yield + EV yield +
gender + egg cycles + friendship + growth + egg groups + held items.

Use:
- master/base_data_386.json como fonte de verdade estruturada;
- master/base_data_386.csv para revisão;
- generated/species_info_base_data_preview.h para integração C;
- reports/AUDIT_FINDINGS.md antes de aplicar;
- docs/BASE_DATA_RULES.md para entender cada derivação.

Abilities não são sobrescritas: o pacote das 35 custom abilities continua sendo
a camada responsável por elas.
"""
    (out/"README.md").write_text(readme,encoding="utf-8")
    checks=[]
    for p in sorted(x for x in out.rglob("*") if x.is_file() and x.name!="CHECKSUMS.sha256"):
        checks.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(out).as_posix())
    (out/"CHECKSUMS.sha256").write_text("\n".join(checks)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()

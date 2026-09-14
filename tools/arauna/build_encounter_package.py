#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, math, re, shutil, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
POKEDEX=ROOT/"tools/arauna/package_sources/lovable/pokedex.ts"
MAPPING=ROOT/"docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
EVOS=ROOT/"docs/arauna/ARAUNA_EVOLUTIONS.csv"
ENCOUNTERS=ROOT/"src/data/wild_encounters.json"

CATCHABLE_GROUP="gWildMonHeaders"
STARTER_ROOTS={1,4,7}
STARTER_FAMILY=set(range(1,10))
FEebAS_REPLACEMENT_DEX=121  # Pirarim: rare Route119 fishing mechanic.
WATER_KINDS={"water_mons","fishing_mons"}
TABLE_CAP={"land_mons":4,"water_mons":2,"fishing_mons":3,"rock_smash_mons":2}

REGION_TAGS={
 "Cerrado de Arauana":{"cerrado"},
 "Amazônia de Arauana":{"amazonia","rios","mata"},
 "Mata Atlântica de Arauana":{"mata"},
 "Cidades de Arauana":{"cidades"},
 "Litoral de Arauana":{"litoral"},
 "Serra de Arauana":{"serra"},
 "Rios de Arauana":{"rios"},
 "Caatinga de Arauana":{"caatinga","sertao"},
 "Pantanal de Arauana":{"pantanal","rios","banhados"},
 "Pampas de Arauana":{"pampas"},
 "Cavernas de Arauana":{"cavernas"},
 "Chapadas de Arauana":{"chapadas","serra"},
 "Sertão de Arauana":{"sertao","caatinga"},
 "Banhados de Arauana":{"banhados","pantanal"},
 "Rio Amazonas de Arauana":{"amazonia","rios"},
 "Rio Solimões de Arauana":{"amazonia","rios"},
 "Periferia de Arauana":{"periferia","cidades"},
 "Campos queimados de Arauana":{"caatinga","serra"},
}
ADJ={
 "cerrado":{"pampas","caatinga","sertao","chapadas","pantanal","cidades"},
 "amazonia":{"mata","rios","pantanal","banhados"},
 "mata":{"amazonia","serra","cerrado","litoral"},
 "cidades":{"periferia","cerrado","litoral"},
 "litoral":{"rios","pantanal","mata","cidades"},
 "serra":{"chapadas","mata","cavernas","caatinga"},
 "rios":{"amazonia","pantanal","banhados","litoral"},
 "caatinga":{"sertao","cerrado","chapadas","serra"},
 "pantanal":{"rios","banhados","cerrado","amazonia"},
 "pampas":{"cerrado","banhados"},
 "cavernas":{"serra","chapadas"},
 "chapadas":{"serra","caatinga","cerrado","cavernas"},
 "sertao":{"caatinga","cerrado"},
 "banhados":{"pantanal","rios","pampas"},
 "periferia":{"cidades","cerrado"},
}

def top_objects(text):
    marker=text.index("export const POKEDEX")
    i=text.index("[",text.index("=",marker)); sq=cu=0; q=esc=False; start=None; out=[]
    while i<len(text):
        c=text[i]
        if q:
            if esc: esc=False
            elif c=="\\": esc=True
            elif c=='"': q=False
        else:
            if c=='"': q=True
            elif c=="[": sq+=1
            elif c=="]":
                sq-=1
                if sq==0: break
            elif c=="{" and sq==1:
                if cu==0:start=i
                cu+=1
            elif c=="}" and sq==1 and cu:
                cu-=1
                if cu==0 and start is not None:
                    out.append(text[start:i+1]); start=None
        i+=1
    return out

def load_mons():
    text=POKEDEX.read_text(encoding="utf-8"); out={}
    for o in top_objects(text):
        mi=re.search(r"\bid:\s*(\d+)",o)
        if not mi: continue
        dex=int(mi.group(1))
        def quoted(k):
            m=re.search(rf'\b{k}:\s*"([^"]+)"',o); return m.group(1) if m else ""
        tb=(re.search(r"\btypes:\s*\[([^\]]*)\]",o) or [None,""])[1]
        types=re.findall(r'"([^"]+)"',tb)
        sm=(re.search(r"\bstats:\s*\{([^}]*)\}",o) or [None,""])[1]
        stats={k:int(v) for k,v in re.findall(r"(hp|atk|def|spa|spd|spe):\s*(\d+)",sm)}
        out[dex]=dict(dex=dex,name=quoted("name"),region=quoted("region"),category=quoted("category"),
                      inspiration=quoted("inspiration"),dex_text=quoted("dex"),types=types,stats=stats,
                      bst=sum(stats.values()),legendary=bool(re.search(r"\blegendary:\s*true",o)),
                      mythical=bool(re.search(r"\bmythical:\s*true",o)))
    if sorted(out)!=list(range(1,387)): raise RuntimeError(f"pokedex parse: {len(out)}")
    return out

def load_mapping():
    with MAPPING.open(encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    by_dex={int(r["arauna_dex"]):r for r in rows}
    by_species={r["species_constant"]:int(r["arauna_dex"]) for r in rows}
    return by_dex,by_species

def evolution_graph():
    forward=defaultdict(list); backward={}
    gates={}
    with EVOS.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            a,b,lv=int(r["arauna_dex"]),int(r["target_dex"]),int(r["level"])
            forward[a].append(b); backward[b]=a; gates[b]=lv
    return forward,backward,gates

def mon_tags(mon):
    return set(REGION_TAGS.get(mon["region"],{"cerrado"}))

def map_tags(name):
    if name=="MAP_ROUTE101": return {"pampas","cerrado","periferia"}
    if name=="MAP_ROUTE102": return {"pampas","cerrado","rios"}
    if name=="MAP_ROUTE103": return {"pampas","banhados","rios"}
    if name=="MAP_ROUTE104" or "PETALBURG_WOODS" in name: return {"mata","litoral"}
    if name=="MAP_ROUTE116": return {"serra","chapadas","cerrado"}
    if "RUSTURF_TUNNEL" in name: return {"serra","cavernas"}
    if "GRANITE_CAVE" in name: return {"cavernas","serra","chapadas"}
    if re.match(r"MAP_ROUTE10[5-9]$",name) or name in {"MAP_DEWFORD_TOWN","MAP_SLATEPORT_CITY"}:
        return {"litoral","rios","cidades" if name=="MAP_SLATEPORT_CITY" else "litoral"}
    if name=="MAP_ROUTE110": return {"cidades","cerrado","litoral"}
    if name=="MAP_ROUTE111": return {"caatinga","sertao","cerrado","chapadas"}
    if name=="MAP_ROUTE112": return {"caatinga","serra"}
    if name=="MAP_ROUTE113": return {"serra","caatinga","cerrado"}
    if name=="MAP_ROUTE114": return {"serra","rios","cerrado"}
    if name=="MAP_ROUTE115": return {"serra","litoral","mata"}
    if name=="MAP_ROUTE117": return {"cerrado","cidades","mata"}
    if name=="MAP_ROUTE118": return {"rios","cerrado","mata"}
    if name=="MAP_ROUTE119": return {"amazonia","mata","rios","pantanal"}
    if name=="MAP_ROUTE120": return {"mata","cerrado","serra"}
    if name=="MAP_ROUTE121": return {"mata","cidades","litoral"}
    if name=="MAP_ROUTE122": return {"rios","litoral","memorial"}
    if name=="MAP_ROUTE123": return {"mata","rios","cerrado"}
    if re.match(r"MAP_ROUTE12[4-9]$",name) or re.match(r"MAP_ROUTE13[0-4]$",name):
        return {"litoral","rios","amazonia"}
    if "UNDERWATER" in name: return {"litoral","rios","cavernas"}
    if "ABANDONED_SHIP" in name: return {"litoral","cidades","memorial"}
    if "MT_PYRE" in name: return {"serra","memorial","mata"}
    if "FIERY_PATH" in name or "MAGMA_HIDEOUT" in name: return {"serra","caatinga","cavernas","fire_zone"}
    if "JAGGED_PASS" in name: return {"serra","caatinga","chapadas"}
    if "METEOR_FALLS" in name: return {"serra","cavernas","chapadas","rios"}
    if "NEW_MAUVILLE" in name: return {"cidades","electric_zone"}
    if "SAFARI_ZONE_SOUTHWEST" in name: return {"pantanal","rios","mata","banhados"}
    if "SAFARI_ZONE_NORTHWEST" in name: return {"amazonia","pantanal","rios","mata"}
    if "SAFARI_ZONE_SOUTHEAST" in name: return {"caatinga","cerrado","pampas","postgame"}
    if "SAFARI_ZONE_NORTHEAST" in name: return {"serra","chapadas","mata","postgame"}
    if "SAFARI_ZONE_SOUTH" in name: return {"cerrado","pampas","pantanal"}
    if "SAFARI_ZONE_NORTH" in name: return {"mata","amazonia","serra"}
    if "VICTORY_ROAD" in name or name=="MAP_EVER_GRANDE_CITY": return {"serra","chapadas","cavernas","endgame"}
    if "SEAFLOOR_CAVERN" in name: return {"cavernas","litoral","rios","mboi"}
    if "CAVE_OF_ORIGIN" in name or name=="MAP_SOOTOPOLIS_CITY": return {"cavernas","serra","rios","mboi"}
    if "SHOAL_CAVE" in name: return {"litoral","cavernas","ice_zone"}
    if "SKY_PILLAR" in name: return {"serra","chapadas","sky_zone","endgame"}
    if "MIRAGE_TOWER" in name: return {"caatinga","sertao","chapadas"}
    if "DESERT_UNDERPASS" in name: return {"caatinga","cavernas","sertao"}
    if "ARTISAN_CAVE" in name: return {"cavernas","serra","postgame"}
    if "ALTERING_CAVE" in name: return {"mata","cerrado","amazonia","caatinga","serra","cavernas","postgame"}
    if name=="MAP_LILYCOVE_CITY": return {"litoral","cidades"}
    if name=="MAP_MOSSDEEP_CITY": return {"litoral","cidades","sky_zone"}
    if name=="MAP_PACIFIDLOG_TOWN": return {"litoral","rios"}
    if name=="MAP_PETALBURG_CITY": return {"pampas","cidades","rios"}
    return {"cerrado"}

def stage_level(name):
    if name in {"MAP_ROUTE101","MAP_ROUTE102","MAP_ROUTE103","MAP_ROUTE104","MAP_PETALBURG_WOODS"}:return 5
    if name in {"MAP_ROUTE116","MAP_RUSTURF_TUNNEL"}:return 9
    if "GRANITE_CAVE" in name:return 12
    if re.match(r"MAP_ROUTE10[5-9]$",name) or name in {"MAP_DEWFORD_TOWN","MAP_SLATEPORT_CITY"}:return 13
    if name=="MAP_ROUTE110":return 15
    if name in {"MAP_ROUTE112","MAP_ROUTE113","MAP_FIERY_PATH"}:return 18
    if name in {"MAP_ROUTE111","MAP_ROUTE114","MAP_ROUTE117","MAP_JAGGED_PASS"} or "MIRAGE_TOWER" in name:return 22
    if "NEW_MAUVILLE" in name:return 25
    if name in {"MAP_ROUTE115","MAP_ROUTE118"}:return 27
    if name in {"MAP_ROUTE119","MAP_ROUTE120","MAP_ROUTE121","MAP_ROUTE122","MAP_ROUTE123"} or "MT_PYRE" in name:return 30
    if "SAFARI_ZONE" in name:return 34 if "EAST" not in name else 40
    if re.match(r"MAP_ROUTE12[4-9]$",name) or re.match(r"MAP_ROUTE13[0-4]$",name):return 34
    if "UNDERWATER" in name or "SHOAL_CAVE" in name:return 34
    if "SEAFLOOR_CAVERN" in name or "CAVE_OF_ORIGIN" in name:return 37
    if "MAGMA_HIDEOUT" in name:return 32
    if "METEOR_FALLS" in name:return 35
    if "VICTORY_ROAD" in name:return 43
    if "SKY_PILLAR" in name:return 42
    if "DESERT_UNDERPASS" in name:return 44
    if "ARTISAN_CAVE" in name:return 48
    if "ALTERING_CAVE" in name:return 45
    if name=="MAP_EVER_GRANDE_CITY":return 42
    return 30

def expected_bst(stage):
    return min(525,260 + stage*5.5)

def adjacency_score(a,b):
    if a & b:return 120 + 15*(len(a & b)-1)
    near=0
    for x in a:
        near=max(near,len(ADJ.get(x,set()) & b))
    return 45 if near else -35

def habitat_bonus(mon,tags):
    t=set(mon["types"]); score=0
    if "mata" in tags or "amazonia" in tags:
        if t & {"grass","bug","fairy","flying"}:score+=25
    if tags & {"caatinga","sertao","fire_zone"}:
        if t & {"fire","ground","rock","electric"}:score+=30
    if tags & {"serra","chapadas","cavernas"}:
        if t & {"rock","ground","steel","ghost","dark","dragon"}:score+=20
    if tags & {"rios","litoral","pantanal","banhados"}:
        if "water" in t:score+=35
        if t & {"flying","bug","grass"}:score+=10
    if "cidades" in tags and t & {"normal","electric","steel","dark","poison","psychic"}:score+=20
    if "memorial" in tags and t & {"ghost","dark","psychic","fairy"}:score+=35
    if "electric_zone" in tags and t & {"electric","steel"}:score+=60
    if "fire_zone" in tags and t & {"fire","ground","rock"}:score+=60
    if "ice_zone" in tags and t & {"ice","water"}:score+=60
    if "sky_zone" in tags and t & {"flying","dragon","psychic","fairy"}:score+=45
    if "mboi" in tags and t & {"water","dragon","ghost","dark","psychic"}:score+=40
    return score

def eligible(mon,kind,tags):
    types=set(mon["types"])
    if kind in WATER_KINDS:
        return "water" in types
    if kind=="rock_smash_mons":
        return bool(types & {"rock","ground","steel"})
    if kind=="land_mons":
        if types=={"water"}:return False
        return True
    return False

def fish_like(mon):
    lore=(" ".join([mon["name"],mon["category"],mon["inspiration"],mon["dex_text"]])).lower()
    return any(x in lore for x in ["peixe","bagre","tubar","sard","pacu","pirarucu","traíra","tucunar","aruanã","poraquê"])

def iter_tables(data):
    group=next(g for g in data["wild_encounter_groups"] if g.get("label")==CATCHABLE_GROUP)
    for enc_idx,e in enumerate(group["encounters"]):
        mapname=e.get("map",e.get("base_label","?"))
        for kind in ("land_mons","water_mons","rock_smash_mons","fishing_mons"):
            if kind in e:
                yield dict(enc_idx=enc_idx,map=mapname,base_label=e.get("base_label",""),
                           kind=kind,obj=e[kind],mons=e[kind]["mons"],tags=map_tags(mapname),
                           stage=stage_level(mapname),key=(enc_idx,kind))

def species_score(mon,table):
    score=adjacency_score(mon_tags(mon),table["tags"])+habitat_bonus(mon,table["tags"])
    score-=abs(mon["bst"]-expected_bst(table["stage"]))*0.34
    if table["kind"]=="fishing_mons":
        score+=25 if fish_like(mon) else -8
    elif table["kind"]=="water_mons":
        score+=8 if not fish_like(mon) else 0
    if mon["bst"]>520 and table["stage"]<25:score-=150
    if mon["bst"]>470 and table["stage"]<12:score-=90
    if mon["dex"]==46 and table["stage"]<30:score-=500
    return score

def incoming_gates():
    g={}
    with EVOS.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):g[int(r["target_dex"])]=int(r["level"])
    return g

def evolved_allowed(dex,stage,gates,backward):
    cur=dex; hardest=0
    while cur in backward:
        hardest=max(hardest,gates.get(cur,1));cur=backward[cur]
    return stage+3>=hardest

def choose_slot(table,mon,used):
    free=[i for i in range(len(table["mons"])) if (table["key"],i) not in used]
    if not free:return None
    rare=mon["bst"]>=480 or mon["dex"]==46
    common=mon["bst"]<=355
    if table["kind"]=="land_mons":
        pref=([10,11,8,9,7,6,5,4,3,2,1,0] if rare else
              [0,1,2,3,4,5,6,7,8,9,10,11] if common else
              [6,7,4,5,8,9,2,3,10,11,1,0])
    elif table["kind"]=="water_mons":
        pref=[4,3,2,1,0] if rare else ([0,1,2,3,4] if common else [2,3,1,4,0])
    elif table["kind"]=="fishing_mons":
        pref=[9,8,7,6,5,4,3,2,1,0] if rare else ([0,1,2,3,4,5,6,7,8,9] if common else [3,4,5,6,2,7,8,1,9,0])
    else:
        pref=[4,3,2,1,0] if rare else ([0,1,2,3,4] if common else [2,3,1,4,0])
    for i in pref:
        if i in free:return i
    return free[0]

def static_plan(mons):
    out=[]
    for d,m in sorted(mons.items()):
        if not (m["legendary"] or m["mythical"]):continue
        tags=mon_tags(m); types=set(m["types"])
        if d==386:loc="TORRE JURAMENTO / evento final dedicado";lvl=75
        elif d in {337,348}:loc="TORRE JURAMENTO / ESTR. JURAMENTO";lvl=68 if d==348 else 62
        elif "litoral" in tags or ("water" in types and "amazonia" not in tags):
            loc="BAIA DAS LUZES / aguas costeiras - encontro estatico";lvl=60
        elif "amazonia" in tags or "rios" in tags:
            loc="MATA DO MEIO / CAVERNAS M'BOI - encontro estatico";lvl=60
        elif "caatinga" in tags or "sertao" in tags:
            loc="SERRA DA CINZA / torre ou ruina dedicada";lvl=58
        elif "chapadas" in tags:
            loc="RUINAS DA QUEDA / ESTR. JURAMENTO";lvl=62
        elif "cerrado" in tags:
            loc="Cerrado tardio / santuario dedicado";lvl=58
        else:
            loc="SERRA DO UIVO / TORRE JURAMENTO - santuario dedicado";lvl=60
        if m["mythical"]:lvl=max(lvl,65)
        if d>=376:lvl=max(lvl,65)
        out.append(dict(dex=d,name=m["name"],types="/".join(m["types"]),region=m["region"],
                        recommended_level=lvl,placement=loc,random_encounter="NO"))
    return out

def main():
    if len(sys.argv)<2:raise SystemExit("usage: build_encounter_package.py OUT_DIR")
    out=Path(sys.argv[1])
    if out.exists():shutil.rmtree(out)
    for d in ("master","generated","reports","docs"): (out/d).mkdir(parents=True,exist_ok=True)
    mons=load_mons(); by_dex,by_species=load_mapping(); forward,backward,gates=evolution_graph()
    data=json.loads(ENCOUNTERS.read_text(encoding="utf-8"))
    tables=list(iter_tables(data))
    roots=set(mons)-set(backward)
    specials={d for d,m in mons.items() if m["legendary"] or m["mythical"]}
    regular_roots=sorted(roots-specials-{FEebAS_REPLACEMENT_DEX})
    # Starters are postgame wild only so all three can be completed in one save.
    used=set(); loads=Counter(); placements=[]
    def candidates_for_root(d):
        m=mons[d]; opts=[]
        for t in tables:
            if loads[t["key"]]>=TABLE_CAP[t["kind"]]:continue
            if not eligible(m,t["kind"],t["tags"]):continue
            if d in STARTER_ROOTS and not ("postgame" in t["tags"] and "SAFARI_ZONE" in t["map"]):continue
            if d not in STARTER_ROOTS and "postgame" in t["tags"] and t["stage"]>=40:
                post_penalty=-20
            else:post_penalty=0
            score=species_score(m,t)+post_penalty-loads[t["key"]]*18
            opts.append((score,t))
        return sorted(opts,key=lambda x:(-x[0],x[1]["map"],x[1]["kind"]))
    # Constrained/high-power first.
    order=[]
    for d in regular_roots:
        opts=candidates_for_root(d)
        order.append((len(opts),-mons[d]["bst"],d))
    for _,__,d in sorted(order):
        opts=candidates_for_root(d)
        if not opts:raise RuntimeError(f"no encounter home for #{d:03d} {mons[d]['name']}")
        _,t=opts[0]; idx=choose_slot(t,mons[d],used)
        if idx is None:raise RuntimeError(f"no free slot {t['key']}")
        used.add((t["key"],idx));loads[t["key"]]+=1
        t["mons"][idx]["species"]=by_dex[d]["species_constant"]
        placements.append(dict(dex=d,name=mons[d]["name"],engine_species=by_dex[d]["species_constant"],
                               map=t["map"],base_label=t["base_label"],table=t["kind"],slot=idx,
                               min_level=t["mons"][idx]["min_level"],max_level=t["mons"][idx]["max_level"],
                               region=mons[d]["region"],types="/".join(mons[d]["types"]),
                               bst=mons[d]["bst"],coverage="root"))
    # Fill all other slots from coherent local rosters, excluding specials.
    all_regular=[m for d,m in mons.items() if d not in specials and d not in STARTER_FAMILY]
    inc_gates=incoming_gates()
    patterns={
      "land_mons":[0,1,0,2,1,3,0,4,2,5,6,7],
      "water_mons":[0,0,1,2,3],
      "rock_smash_mons":[0,0,1,2,3],
      "fishing_mons":[0,1,0,2,1,3,4,3,5,6],
    }
    for t in tables:
        reserved={i for key,i in used if key==t["key"]}
        reserved_dex={by_species.get(t["mons"][i]["species"]) for i in reserved}
        pool=[]
        for m in all_regular:
            if m["dex"]==FEebAS_REPLACEMENT_DEX:continue
            if m["dex"] in reserved_dex:continue
            if not eligible(m,t["kind"],t["tags"]):continue
            if not evolved_allowed(m["dex"],t["stage"],inc_gates,backward):continue
            sc=species_score(m,t)
            pool.append((sc,m))
        pool.sort(key=lambda x:(-x[0],x[1]["dex"]))
        roster=[m for _,m in pool[:8]]
        if not roster:raise RuntimeError(f"empty fill roster {t['map']} {t['kind']}")
        pat=patterns[t["kind"]]
        for i,slot in enumerate(t["mons"]):
            if i in reserved:continue
            m=roster[pat[i] % len(roster)]
            slot["species"]=by_dex[m["dex"]]["species_constant"]
    # Validate random tables and reachability.
    wild=set()
    legend_random=[]
    for t in tables:
        for slot in t["mons"]:
            d=by_species.get(slot["species"])
            if d:
                wild.add(d)
                if d in specials:legend_random.append((d,t["map"],t["kind"]))
    intended_roots=set(regular_roots)
    missing_roots=sorted(intended_roots-wild)
    seeds=set(wild)|{FEebAS_REPLACEMENT_DEX}
    reachable=set(seeds); stack=list(seeds)
    while stack:
        d=stack.pop()
        for nxt in forward.get(d,[]):
            if nxt not in reachable:reachable.add(nxt);stack.append(nxt)
    non_special=set(mons)-specials
    missing_non_special=sorted(non_special-reachable)
    if missing_roots or legend_random or missing_non_special:
        raise RuntimeError(f"validation failed missing roots={missing_roots}, legends={legend_random}, non-special={missing_non_special}")
    # Write artifacts.
    (out/"generated/wild_encounters.json").write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    with (out/"master/encounter_root_placements.csv").open("w",encoding="utf-8",newline="") as f:
        cols=["dex","name","engine_species","map","base_label","table","slot","min_level","max_level","region","types","bst","coverage"]
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(sorted(placements,key=lambda x:x["dex"]))
    with (out/"master/map_biomes.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f);w.writerow(["map","base_label","table","stage","biome_tags","coverage_roots"])
        for t in tables:w.writerow([t["map"],t["base_label"],t["kind"],t["stage"],"/".join(sorted(t["tags"])),loads[t["key"]]])
    sp=static_plan(mons)
    with (out/"master/static_legend_mythical_plan.csv").open("w",encoding="utf-8",newline="") as f:
        cols=["dex","name","types","region","recommended_level","placement","random_encounter"]
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(sp)
    pir=by_dex[FEebAS_REPLACEMENT_DEX]["species_constant"]
    patch=f"""// Route119 rare-tile mechanic correction.
// SPECIES_FEEBAS is Arauna #349 Aracua (Flying/Normal), so leaving the vanilla
// hardcoded slot creates a Flying Pokemon while fishing.
// Replace in src/wild_encounter.c:
//
// static const struct WildPokemon sWildFeebas = {{20, 25, SPECIES_FEEBAS}};
//
// with:
static const struct WildPokemon sWildFeebas = {{20, 25, {pir}}}; // #121 Pirarim
"""
    (out/"generated/route119_rare_fishing_patch.txt").write_text(patch,encoding="utf-8")
    summary={
      "species":386,"encounter_maps":len({t["map"] for t in tables}),
      "encounter_tables":len(tables),"root_species":len(roots),"random_root_placements":len(placements),
      "wild_species_total":len(wild),"non_special_reachable_with_evolution_and_pirarim":len(reachable & non_special),
      "non_special_total":len(non_special),"legendary_mythical_random_slots":len(legend_random),
      "static_legendary_mythical":len(sp),"starters_postgame_wild":sorted(STARTER_ROOTS),
      "route119_rare_species":{"dex":121,"name":mons[121]["name"],"engine_species":pir},
      "missing_roots":missing_roots,"missing_non_special":missing_non_special}
    (out/"reports/summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    # Distribution report.
    biome_counts=Counter(); table_counts=Counter()
    for p in placements:
        table_counts[p["table"]]+=1
        for tag in map_tags(p["map"]):biome_counts[tag]+=1
    report=["# Encounter Table v2 - validation","",
            f"- 386 species analyzed.",
            f"- {len(placements)} non-special family roots receive a deliberate random-wild home.",
            f"- Pirarim #121 is reserved for the Route119 rare fishing-tile mechanic.",
            f"- {len(sp)} Legendary/Mythical species are excluded from random grass/surf/fishing tables.",
            f"- All {len(non_special)} non-special species are reachable through wild roots + evolution.",
            f"- Starter roots #001/#004/#007 occur only in postgame Safari expansion tables.",
            f"- Random Legendary/Mythical contamination: {len(legend_random)}.",
            f"- Missing non-special species after evolution closure: {len(missing_non_special)}.","",
            "## Important engine correction","",
            "Vanilla sWildFeebas currently points at SPECIES_FEEBAS, which is Arauna #349 Aracua (Flying/Normal). "
            "The package changes that rare Route119 mechanic to #121 Pirarim, a Water Pokemon, via the included patch.","",
            "## Placement principles","",
            "- Region/lore is the primary habitat signal.",
            "- Water and fishing tables contain Water-type species only.",
            "- Rock Smash is restricted to Rock/Ground/Steel.",
            "- BST and campaign stage prevent high-power roots from flooding the opening routes.",
            "- Evolved forms only enter filler rosters once the map stage is near their evolution gate.",
            "- Special species are static encounters, not 1% random grass rolls.",""]
    (out/"reports/ENCOUNTER_VALIDATION.md").write_text("\n".join(report),encoding="utf-8")
    rules="""# Arauana Encounter Design v2

This pass replaces the old vanilla-strength permutation / duplicate-slot filler with an ecology-first table.

Rules:
1. Every non-special evolutionary root must have a deliberate acquisition route.
2. Legendary and Mythical Pokemon never appear in normal random tables.
3. The three starter roots are obtainable only in postgame Safari expansion areas, preserving the starter choice during the story while allowing one-save Dex completion.
4. Pirarim #121 owns the Route119 Feebas-style rare fishing mechanic. Aracua #349 must not inherit that mechanic just because it occupies SPECIES_FEEBAS.
5. Water/Surf/Fishing tables require Water typing. Rock Smash requires Rock/Ground/Steel.
6. Region labels from the approved Pokedex drive habitat: Cerrado, Amazonia, Mata Atlantica, cities, coast, mountains, rivers, Caatinga, Pantanal, Pampas, caves, chapadas, sertao and wetlands.
7. Campaign stage and BST are secondary constraints. Strong roots are pushed later and into rarer slots.
8. Evolved forms may fill local ecology slots only when the map stage is close to or beyond their evolution gate.
9. Existing encounter rates, slot counts and level ranges are preserved exactly. Only species assignments change.
10. Static Legendary/Mythical placement is documented separately and should be implemented through story/event scripts.

The generated wild_encounters.json is a full drop-in replacement for src/data/wild_encounters.json.
"""
    (out/"docs/ENCOUNTER_DESIGN_RULES.md").write_text(rules,encoding="utf-8")
    readme="""# Arauana Encounter Table v2

Files:
- generated/wild_encounters.json: full drop-in encounter table.
- generated/route119_rare_fishing_patch.txt: fixes the inherited Feebas hardcode.
- master/encounter_root_placements.csv: where every non-special family root is deliberately placed.
- master/map_biomes.csv: inferred ecology and campaign stage for each encounter table.
- master/static_legend_mythical_plan.csv: static-only plan for special species.
- reports/ENCOUNTER_VALIDATION.md and summary.json: closure checks.
- docs/ENCOUNTER_DESIGN_RULES.md: design policy.

The build fails if any non-special family becomes unobtainable or if any Legendary/Mythical leaks into a random encounter table.
"""
    (out/"README.md").write_text(readme,encoding="utf-8")
    checks=[]
    for p in sorted(x for x in out.rglob("*") if x.is_file() and x.name!="CHECKSUMS.sha256"):
        checks.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(out).as_posix())
    (out/"CHECKSUMS.sha256").write_text("\n".join(checks)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return 0
if __name__=="__main__":
    raise SystemExit(main())

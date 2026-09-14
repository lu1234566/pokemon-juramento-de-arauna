#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, re, shutil, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"docs/arauna/ARAUNA_EVOLUTIONS.csv"
MAP=ROOT/"docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv"
POKEDEX=ROOT/"tools/arauna/package_sources/lovable/pokedex.ts"

OVERRIDES={
    17:  dict(method="EVO_FRIENDSHIP",       param="0",               gate_level=34,
              reason="Curupira represents the forest guardian accepting a trainer; trust is more thematic than a raw level."),
    92:  dict(method="EVO_ITEM",             param="ITEM_MOON_STONE", gate_level=32,
              reason="The nocturnal Morcego becomes the Dark-type Vampiro through a Moon Stone."),
    98:  dict(method="EVO_ITEM",             param="ITEM_FIRE_STONE", gate_level=34,
              reason="The Fire Stone is the supernatural ignition that turns Mula into Mula-sem-Cabeca."),
    163: dict(method="EVO_FRIENDSHIP_NIGHT", param="0",               gate_level=24,
              reason="Corrects stale self-evolution metadata and makes the nocturnal owl mature through trust at night."),
    362: dict(method="EVO_ITEM",             param="ITEM_SUN_STONE",  gate_level=40,
              reason="Beija-Luz reaches its solar final form through the Sun Stone instead of an arbitrary level."),
}
SUPPORTED={"EVO_LEVEL","EVO_FRIENDSHIP","EVO_FRIENDSHIP_DAY","EVO_FRIENDSHIP_NIGHT","EVO_ITEM"}

def load():
    base=list(csv.DictReader(BASE.open(encoding="utf-8")))
    mapping={int(r["arauna_dex"]):r for r in csv.DictReader(MAP.open(encoding="utf-8"))}
    return base,mapping

def design_rows(base):
    out=[]
    for r in base:
        a=int(r["arauna_dex"]); b=int(r["target_dex"]); lv=int(r["level"])
        o=OVERRIDES.get(a)
        if o:
            method=o["method"]; param=o["param"]; gate=o["gate_level"]; reason=o["reason"]; decision="Especializado v2"
        else:
            method=r["method"]; param=str(lv); gate=lv; reason="Mantem a progressao de nivel aprovada."; decision=r.get("decision","Mantido")
        out.append(dict(arauna_dex=a,name=r["name"],method=method,param=param,
                        gate_level=gate,target_dex=b,target_name=r["target_name"],
                        decision=decision,reason=reason))
    return out

def validate(rows,mapping):
    problems=[]; rel={}
    for r in rows:
        a,b=r["arauna_dex"],r["target_dex"]
        if a==b: problems.append(f"#{a:03d} evolves into itself")
        if a not in mapping or b not in mapping: problems.append(f"mapping missing for #{a:03d} -> #{b:03d}")
        if r["method"] not in SUPPORTED: problems.append(f"unsupported method {r['method']} on #{a:03d}")
        if r["method"]=="EVO_LEVEL":
            try: p=int(r["param"])
            except: p=-1
            if not 2<=p<=80: problems.append(f"invalid level {r['param']} on #{a:03d}")
        if r["method"]=="EVO_ITEM" and not r["param"].startswith("ITEM_"):
            problems.append(f"invalid item param on #{a:03d}")
        rel[a]=b
    for t,n in Counter(rel.values()).items():
        if n>1: problems.append(f"#{t:03d} is target of {n} evolutions")
    for a in rel:
        seen=[]; cur=a
        while cur in rel and cur not in seen:
            seen.append(cur); cur=rel[cur]
        if cur in seen:
            problems.append("cycle: "+" -> ".join(f"#{x:03d}" for x in seen+[cur]))
            break
    return problems

def render(rows,mapping):
    width=max(len(mapping[r["arauna_dex"]]["species_constant"]) for r in rows)
    lines=["// Arauna evolution design v2.",
           "// 81 relations; uses only methods already supported by the Emerald engine.",
           "const struct Evolution gEvolutionTable[NUM_SPECIES][EVOS_PER_MON] =","{"]
    for r in rows:
        src=mapping[r["arauna_dex"]]["species_constant"]; dst=mapping[r["target_dex"]]["species_constant"]
        lines.append(f"    [{src}]{' '*(width-len(src))} = "
                     f"{{{{{r['method']}, {r['param']}, {dst}}}}}, "
                     f"// #{r['arauna_dex']:03d} {r['name']} -> #{r['target_dex']:03d} {r['target_name']}")
    lines+=["};",""]
    return "\n".join(lines)

def top_objects(text):
    marker=text.index("export const POKEDEX")
    i=text.index("[",text.index("=",marker)); sq=0;cu=0;q=False;esc=False;start=None;out=[]
    while i<len(text):
        c=text[i]
        if q:
            if esc:esc=False
            elif c=="\\":esc=True
            elif c=='"':q=False
        else:
            if c=='"':q=True
            elif c=="[":sq+=1
            elif c=="]":
                sq-=1
                if sq==0:break
            elif c=="{" and sq==1:
                if cu==0:start=i
                cu+=1
            elif c=="}" and sq==1 and cu:
                cu-=1
                if cu==0 and start is not None:
                    out.append(text[start:i+1]);start=None
        i+=1
    return out

def parse_pokedex_evos():
    text=POKEDEX.read_text(encoding="utf-8"); out={}
    for o in top_objects(text):
        mid=re.search(r"\bid:\s*(\d+)",o)
        if not mid:continue
        dex=int(mid.group(1)); nm=re.search(r'\bname:\s*"([^"]+)"',o); name=nm.group(1) if nm else ""
        bm=re.search(r"\bevolvesTo:\s*\[([\s\S]*?)\]",o); blk=bm.group(1) if bm else ""
        tos=[dict(target=int(m.group(1)),method=m.group(2)) for m in re.finditer(r'\{\s*id:\s*(\d+),\s*method:\s*"([^"]+)"\s*\}',blk)]
        fm=re.search(r"\bevolvesFrom:\s*(\d+)",o)
        out[dex]=dict(name=name,evolves_to=tos,evolves_from=int(fm.group(1)) if fm else None)
    return out

def expected_sync(rows,pdex):
    to=defaultdict(list); frm={}
    for r in rows:
        if r["method"]=="EVO_LEVEL": human=f"Nivel {r['param']}"
        elif r["method"]=="EVO_ITEM":
            labels={"ITEM_MOON_STONE":"Pedra da Lua","ITEM_FIRE_STONE":"Pedra de Fogo","ITEM_SUN_STONE":"Pedra do Sol"}
            human=labels.get(r["param"],r["param"])
        elif r["method"]=="EVO_FRIENDSHIP":human="Amizade alta"
        elif r["method"]=="EVO_FRIENDSHIP_NIGHT":human="Amizade alta a noite"
        else:human=r["method"]
        to[r["arauna_dex"]].append({"id":r["target_dex"],"method":human})
        frm[r["target_dex"]]=r["arauna_dex"]
    return [{"id":dex,"name":pdex.get(dex,{}).get("name",""),"evolvesFrom":frm.get(dex),"evolvesTo":to.get(dex,[])}
            for dex in range(1,387)]

def divergence(rows,pdex):
    findings=[]
    for r in rows:
        a=r["arauna_dex"]; have=pdex.get(a,{}).get("evolves_to",[])
        targets=[x["target"] for x in have]
        if targets != [r["target_dex"]]:
            findings.append(("HIGH",a,pdex.get(a,{}).get("name",r["name"]),
                             f"pokedex.ts target {targets or 'none'}; design v2 target #{r['target_dex']:03d}"))
        if r["method"]=="EVO_LEVEL" and have:
            m=re.search(r"(\d+)",have[0]["method"])
            if m and int(m.group(1))!=int(r["param"]):
                findings.append(("MED",a,pdex.get(a,{}).get("name",r["name"]),
                                 f"pokedex.ts says {have[0]['method']}; approved level is {r['param']}"))
    expected_from={r["target_dex"]:r["arauna_dex"] for r in rows}
    for dex,src in expected_from.items():
        have=pdex.get(dex,{}).get("evolves_from")
        if have!=src:
            findings.append(("HIGH",dex,pdex.get(dex,{}).get("name",""),f"evolvesFrom is {have}; should be #{src:03d}"))
    return findings

def main():
    if len(sys.argv)<2:raise SystemExit("usage: build_evolution_package.py OUT_DIR")
    out=Path(sys.argv[1])
    if out.exists():shutil.rmtree(out)
    for d in ["master","generated","reports","docs"]: (out/d).mkdir(parents=True,exist_ok=True)
    base,mapping=load(); rows=design_rows(base); problems=validate(rows,mapping)
    if problems:
        for p in problems:print("ERROR",p,file=sys.stderr)
        return 1
    pdex=parse_pokedex_evos(); findings=divergence(rows,pdex); sync=expected_sync(rows,pdex)
    with (out/"master/ARAUNA_EVOLUTIONS_V2.csv").open("w",encoding="utf-8",newline="") as f:
        cols=["arauna_dex","name","method","param","gate_level","target_dex","target_name","decision","reason"]
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
    (out/"master/evolution_design_81.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"generated/evolution.h").write_text(render(rows,mapping),encoding="utf-8")
    (out/"generated/pokedex_evolution_sync.json").write_text(json.dumps(sync,ensure_ascii=False,indent=2),encoding="utf-8")
    with (out/"reports/source_divergences.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f);w.writerow(["severity","dex","species","finding"]);w.writerows(findings)
    methods=Counter(r["method"] for r in rows)
    gates=[
      ("Moon Stone","ITEM_MOON_STONE","Morcego #092 -> Vampiro #093",32,"Place before the intended lv32 pacing point."),
      ("Fire Stone","ITEM_FIRE_STONE","Mula #098 -> Mula-sem-Cabeca #099",34,"Place no earlier than midgame; guaranteed by intended lv34 pacing."),
      ("Sun Stone","ITEM_SUN_STONE","Beija-Luz #362 -> Beija-Sol #363",40,"Late-midgame gate; guaranteed before intended lv40 pacing."),
    ]
    with (out/"reports/special_item_requirements.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f);w.writerow(["item","constant","evolution","recommended_gate_level","placement_requirement"]);w.writerows(gates)
    report=["# Evolutions v2 - audit","",
            f"- Relations: **{len(rows)}**",
            f"- Level: **{methods['EVO_LEVEL']}**",
            f"- Friendship: **{methods['EVO_FRIENDSHIP']}**",
            f"- Friendship at night: **{methods['EVO_FRIENDSHIP_NIGHT']}**",
            f"- Evolution items: **{methods['EVO_ITEM']}**",
            f"- Source divergences found in copied Lovable Pokedex: **{len(findings)}**","",
            "## Special evolutions","",
            "- #017 Curupim -> #018 Curupira: high friendship.",
            "- #092 Morcego -> #093 Vampiro: Moon Stone.",
            "- #098 Mula -> #099 Mula-sem-Cabeca: Fire Stone.",
            "- #163 Corurupim -> #164 Coruja: high friendship at night; removes stale #163 -> #163 loop.",
            "- #362 Beija-Luz -> #363 Beija-Sol: Sun Stone.","",
            "## Source synchronization","",
            "generated/pokedex_evolution_sync.json is the canonical metadata for refreshing reference data. "
            "The ROM table is generated from ARAUNA_EVOLUTIONS_V2.csv, not stale evolvesTo strings in pokedex.ts.",""]
    for sev,d,n,msg in findings: report.append(f"- **{sev}** #{d:03d} {n}: {msg}")
    (out/"reports/EVOLUTION_AUDIT.md").write_text("\n".join(report)+"\n",encoding="utf-8")
    rules="""# Arauna Evolution Design v2

## Goals
1. No trade evolutions: every species stays obtainable in a single-player GBA ROM.
2. Most wildlife evolves by level for readable progression.
3. Special methods exist only where lore clearly benefits.
4. Only evolution methods already implemented by Pokemon Emerald are used.
5. Item evolutions retain a gate_level: stones must be placed in the campaign around that point.
6. The pseudo family remains level-based.
7. Starters remain level 17 / 36.
8. No branching evolution is invented where the approved dex has one target.

## Special methods
- Friendship: Curupim -> Curupira.
- Friendship Night: Corurupim -> Coruja.
- Moon Stone: Morcego -> Vampiro.
- Fire Stone: Mula -> Mula-sem-Cabeca.
- Sun Stone: Beija-Luz -> Beija-Sol.

## Engine safety
Methods used: EVO_LEVEL, EVO_FRIENDSHIP, EVO_FRIENDSHIP_NIGHT, EVO_ITEM.
All are vanilla Emerald behavior; no save-layout changes or new evolution code are required.
"""
    (out/"docs/EVOLUTION_DESIGN_RULES.md").write_text(rules,encoding="utf-8")
    summary={"species":386,"relations":len(rows),"methods":dict(methods),"special_evolutions":len(OVERRIDES),
             "self_evolutions":0,"cycles":0,"source_divergences":len(findings),"item_dependencies":3}
    (out/"reports/summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    readme="""# Arauna Evolutions v2

Implementation-ready evolution package.

Use:
- master/ARAUNA_EVOLUTIONS_V2.csv - source of truth.
- generated/evolution.h - drop-in gEvolutionTable.
- generated/pokedex_evolution_sync.json - fixes metadata/reference-source drift.
- reports/EVOLUTION_AUDIT.md - divergences and corrections.
- reports/special_item_requirements.csv - campaign placement requirements.
- docs/EVOLUTION_DESIGN_RULES.md - design rationale.

The table contains all 81 approved evolution relations and no self-evolutions,
cycles or trade-only methods.
"""
    (out/"README.md").write_text(readme,encoding="utf-8")
    checks=[]
    for p in sorted(x for x in out.rglob("*") if x.is_file() and x.name!="CHECKSUMS.sha256"):
        checks.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(out).as_posix())
    (out/"CHECKSUMS.sha256").write_text("\n".join(checks)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "tools/arauna/package_sources/lovable"

FAIRY_MOVE_IDS = {
    "MOVE_FAIRY_WIND","MOVE_DISARMING_VOICE","MOVE_DRAINING_KISS",
    "MOVE_DAZZLING_GLEAM","MOVE_MOONBLAST","MOVE_LUAR_DE_JACI",
    "MOVE_JURAMENTO_DE_ARAUANA","MOVE_ECLIPSE_DIVINO",
}
FAIRY_ENGINE_READY_SIGNATURES = {"LUAR_DE_JACI","JURAMENTO_DE_ARAUANA","ECLIPSE_DIVINO"}

FAIRY_OVERLAY_FILES = [
    "include/constants/moves.h","include/constants/battle_move_effects.h",
    "data/battle_scripts_1.s","src/battle_tv.c","src/data/battle_moves.h",
    "src/data/text/move_names.h","src/data/text/move_descriptions.h",
    "include/constants/battle_anim.h","include/graphics.h","src/graphics.c",
    "src/data/battle_anim.h","src/battle_anim_fairy.c","data/battle_anim_scripts.s",
    "src/data/pokemon/arauna_fairy_learnsets.h",
    "src/data/pokemon/level_up_learnset_pointers.h","src/pokemon.c",
    "tools/arauna/build_movesets.py","src/pokedex.c","src/data/union_room.h",
    "data/battle_ai_scripts.s","docs/arauna/FAIRY_MOVES_AND_ANIMATIONS.md",
    "docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv",
    "graphics/battle_anims/sprites/fairy_spark.png",
    "graphics/battle_anims/sprites/fairy_wave.png",
    "graphics/battle_anims/sprites/fairy_crescent.png",
    "graphics/battle_anims/sprites/fairy_oath.png",
    "graphics/battle_anims/sprites/fairy_eclipse.png",
]

def parse_learnsets(text):
    out = {}
    pat = re.compile(r"^\s{2}(\d+): \[(.*?)\],$", re.M)
    ent = re.compile(r'\{ level: (\d+), move: "([A-Z0-9_]+)" \}')
    for m in pat.finditer(text):
        out[int(m.group(1))] = [{"level":int(a),"move":b} for a,b in ent.findall(m.group(2))]
    return out

def extract_object_block(text, marker):
    i=text.index(marker); lb=text.index("{", i); depth=0; quoted=False; esc=False
    for j in range(lb, len(text)):
        ch=text[j]
        if quoted:
            if esc: esc=False
            elif ch=="\\": esc=True
            elif ch=='"': quoted=False
            continue
        if ch=='"': quoted=True
        elif ch=="{": depth+=1
        elif ch=="}":
            depth-=1
            if depth==0: return text[lb+1:j]
    raise ValueError(marker)

def parse_signature_moves(text):
    block=extract_object_block(text,"export const SIGNATURE_MOVES")
    out={}
    row=re.compile(r'^\s{2}([A-Z0-9_]+): \{ (.*?) \},$',re.M)
    for m in row.finditer(block):
        mid,body=m.groups()
        def s(key):
            x=re.search(rf'{key}: "([^"]*)"',body); return x.group(1) if x else None
        def n(key):
            x=re.search(rf'{key}: (null|-?\d+)',body)
            return None if (not x or x.group(1)=="null") else int(x.group(1))
        owners=re.search(r"ownerIds: \[([^\]]*)\]",body)
        out[mid]={
            "id":mid,"rom_constant":"MOVE_"+mid,"name_pt":s("namePt"),"name_en":s("nameEn"),
            "type":s("type"),"category":s("category"),"power":n("power"),
            "accuracy":n("accuracy"),"pp":n("pp"),"priority":n("priority"),
            "effect":s("effect"),
            "owner_ids":[int(x.strip()) for x in owners.group(1).split(",") if x.strip()] if owners else [],
            "rationale":s("rationale"),"balance_note":s("balanceNote"),
            "suggested_level":n("suggestedLevel"),
            "engine_status":"implemented_fairy" if mid in FAIRY_ENGINE_READY_SIGNATURES else "design_spec",
        }
    return out

def parse_mapping():
    out={}
    with (ROOT/"docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f): out[int(r["arauna_dex"])]=r
    return out

def parse_fairy_overlay():
    text=(ROOT/"src/data/pokemon/arauna_fairy_learnsets.h").read_text(encoding="utf-8")
    out={}
    for chunk in re.split(r"(?=// #\d{3} )",text):
        h=re.match(r"// #(\d{3}) ",chunk)
        if not h: continue
        dex=int(h.group(1)); rows=[]
        for level,move in re.findall(r"LEVEL_UP_MOVE\(\s*(\d+),\s*(MOVE_[A-Z0-9_]+)\)",chunk):
            if move in FAIRY_MOVE_IDS: rows.append({"level":int(level),"move":move})
        out[dex]=rows
    return out

def merge_fairy(base,fairy):
    out={d:[dict(x) for x in rows] for d,rows in base.items()}
    for dex,adds in fairy.items():
        rows=out.setdefault(dex,[])
        for row in rows:
            if row["move"] in FAIRY_ENGINE_READY_SIGNATURES: row["move"]="MOVE_"+row["move"]
        for a in adds:
            rows[:]=[r for r in rows if r["move"]!=a["move"]]
            rows.append(dict(a))
        rows.sort(key=lambda r:(r["level"],r["move"]))
    return out

def rom_move(move):
    return move if move.startswith("MOVE_") else "MOVE_"+move

def generate_c(master,mapping,outdir):
    h=["#ifndef GUARD_ARAUNA_COMPLETE_LEARNSETS_H","#define GUARD_ARAUNA_COMPLETE_LEARNSETS_H","",
       "/* Generated complete 386-species learnsets. Non-Fairy custom signatures",
       " * require their BattleMove/effect definitions before compiling. */",""]
    p=["#ifndef GUARD_ARAUNA_COMPLETE_LEARNSET_POINTERS_H",
       "#define GUARD_ARAUNA_COMPLETE_LEARNSET_POINTERS_H","",
       "const u16 *const gAraunaCompleteLevelUpLearnsets[NUM_SPECIES] =","{"]
    for dex in range(1,387):
        r=mapping[dex]; species=r["species_constant"]; short=species.removeprefix("SPECIES_")
        arr="sAraunaComplete"+short+"LevelUpLearnset"
        h += [f"// #{dex:03d} {r['full_name']} ({species})",f"static const u16 {arr}[] = {{"]
        for e in master[dex]: h.append(f"    LEVEL_UP_MOVE({e['level']:2d}, {rom_move(e['move'])}),")
        h += ["    LEVEL_UP_END","};",""]
        p.append(f"    [{species}] = {arr},")
    h += ["#endif // GUARD_ARAUNA_COMPLETE_LEARNSETS_H",""]
    p += ["};","","#endif // GUARD_ARAUNA_COMPLETE_LEARNSET_POINTERS_H",""]
    (outdir/"arauna_complete_learnsets.h").write_text("\n".join(h),encoding="utf-8")
    (outdir/"arauna_complete_learnset_pointers.h").write_text("\n".join(p),encoding="utf-8")

def copy_overlay(out):
    root=out/"rom_ready/fairy_overlay"
    for rel in FAIRY_OVERLAY_FILES:
        src=ROOT/rel
        if not src.exists(): raise SystemExit("missing overlay file: "+rel)
        dst=root/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)

def write_csv(master,mapping,path):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f); w.writerow(["dex_id","pokemon","species_constant","level","move"])
        for dex in range(1,387):
            for e in master[dex]:
                w.writerow([dex,mapping[dex]["full_name"],mapping[dex]["species_constant"],e["level"],e["move"]])

def checksum_tree(out):
    lines=[]
    for p in sorted(x for x in out.rglob("*") if x.is_file() and x.name!="CHECKSUMS.sha256"):
        lines.append(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.relative_to(out).as_posix())
    (out/"CHECKSUMS.sha256").write_text("\n".join(lines)+"\n",encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",required=True); args=ap.parse_args()
    out=Path(args.out)
    if out.exists(): shutil.rmtree(out)
    for d in ["master","rom_ready/generated","source_reference/lovable","reports"]:
        (out/d).mkdir(parents=True,exist_ok=True)

    base=parse_learnsets((SRC/"learnsets.ts").read_text(encoding="utf-8"))
    signatures=parse_signature_moves((SRC/"moves.ts").read_text(encoding="utf-8"))
    mapping=parse_mapping(); fairy=parse_fairy_overlay(); master=merge_fairy(base,fairy)

    if set(base)!=set(range(1,387)): raise SystemExit(f"base coverage mismatch: {len(base)}")
    if len(signatures)!=22: raise SystemExit(f"signature count mismatch: {len(signatures)}")
    if len(fairy)!=68: raise SystemExit(f"Fairy overlay mismatch: {len(fairy)}")

    for name in ["learnsets.ts","moves.ts","pokedex.ts","types.ts"]:
        shutil.copy2(SRC/name,out/"source_reference/lovable"/name)

    (out/"master/learnsets_386_base.json").write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"master/learnsets_386_integrated_fairy.json").write_text(json.dumps(master,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"master/signature_moves_22.json").write_text(json.dumps(signatures,ensure_ascii=False,indent=2),encoding="utf-8")
    (out/"master/fairy_overlay_entries_68.json").write_text(json.dumps(fairy,ensure_ascii=False,indent=2),encoding="utf-8")
    write_csv(master,mapping,out/"master/learnsets_386_integrated_fairy.csv")
    generate_c(master,mapping,out/"rom_ready/generated")
    copy_overlay(out)

    base_entries=sum(len(x) for x in base.values()); master_entries=sum(len(x) for x in master.values())
    fairy_entries=sum(len(x) for x in fairy.values())
    sig_assign=sum(1 for rows in master.values() for e in rows if e["move"].removeprefix("MOVE_") in signatures)
    report={
        "species":386,"base_entries":base_entries,"integrated_entries":master_entries,
        "fairy_species":68,"fairy_overlay_entries":fairy_entries,"signature_moves":22,
        "signature_assignments_in_integrated_learnsets":sig_assign,
        "fairy_engine_ready_signatures":sorted(FAIRY_ENGINE_READY_SIGNATURES),
        "non_fairy_signature_specs_pending_engine_definition":sorted(set(signatures)-FAIRY_ENGINE_READY_SIGNATURES),
    }
    (out/"reports/coverage.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    readme=f"""# Pokemon Juramento de Arauna - Complete Moveset Implementation Package

SOURCE OF TRUTH
- master/learnsets_386_integrated_fairy.json : all 386 level-up learnsets with Fairy work merged.
- master/signature_moves_22.json : all 22 signature move specifications.
- master/learnsets_386_integrated_fairy.csv : spreadsheet-friendly flat export.

ROM-READY DATA
- rom_ready/generated/arauna_complete_learnsets.h
- rom_ready/generated/arauna_complete_learnset_pointers.h
- rom_ready/fairy_overlay/ : exact repository-path Fairy engine/assets overlay.

COVERAGE
- 386/386 species.
- {base_entries} base balanced learnset entries.
- {master_entries} entries after Fairy integration.
- 68 Fairy species.
- {fairy_entries} Fairy overlay assignments.
- 22 signature moves.

FAIRY ENGINE
The package includes Fairy Wind, Disarming Voice, Draining Kiss, Dazzling Gleam,
Moonblast, Luar de Jaci, Juramento de Arauana and Eclipse Divino, plus Charm and
Sweet Kiss retyped to Fairy. Luar de Jaci, Juramento de Arauana and Eclipse
Divino have native engine effects and custom GBA battle animation assets.

IMPORTANT
The master dataset intentionally retains all 22 signature assignments. Three
Fairy signatures are engine-ready. The remaining 19 signature moves are fully
specified in master/signature_moves_22.json but still require BattleMove/effect/
animation definitions before compiling a complete learnset that references
those constants. No signature assignment is silently replaced or deleted.

GBA FAIRY ART
fairy_spark.png    16x64  - 4 frames of 16x16
fairy_wave.png     32x96  - 3 frames of 32x32
fairy_crescent.png 32x64  - 2 frames of 32x32
fairy_oath.png     32x64  - 2 frames of 32x32
fairy_eclipse.png  32x64  - 2 frames of 32x32
All are indexed/4bpp-compatible source art. Motion is engine-side, not GIF.

GEN III RULE
The current ROM derives physical/special from type. Fairy is special in this
engine. Do not implement physical Fairy attacks until damage category is moved
to a per-move split.

INTEGRATION ORDER
1. Apply rom_ready/fairy_overlay over the repository root.
2. Review reports/coverage.json.
3. Use the generated all-species C tables for the 386 learnsets.
4. Implement the 19 remaining non-Fairy signatures from signature_moves_22.json.
5. Build and runtime-test all new signature moves before merging.
"""
    (out/"README_IMPLEMENTACAO.md").write_text(readme,encoding="utf-8")
    checksum_tree(out)
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()

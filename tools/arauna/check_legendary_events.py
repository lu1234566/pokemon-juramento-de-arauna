#!/usr/bin/env python3
from __future__ import annotations
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PLAN=ROOT/"docs/arauna/ARAUNA_LEGENDARY_MYTHICAL_EVENTS.csv"

EXPECT={
 "src/roamer.c":[
   "ROAMER->species = SPECIES_VIBRAVA; // #329 Guaraciana",
   "ROAMER->species = SPECIES_FLYGON;  // #330 Jaciana",
   "ROAMER->level = 55;",
 ],
 "data/maps/SouthernIsland_Interior/scripts.inc":[
   "setvar VAR_TEMP_4, SPECIES_FLYGON  @ #330 Jaciana",
   "setvar VAR_TEMP_4, SPECIES_VIBRAVA  @ #329 Guaraciana",
   "seteventmon SPECIES_FLYGON, 55",
   "seteventmon SPECIES_VIBRAVA, 55",
 ],
 "data/maps/AncientTomb/scripts.inc":["setwildbattle SPECIES_SOLROCK, 60"],
 "data/maps/DesertRuins/scripts.inc":["setwildbattle SPECIES_CRAWDAUNT, 60"],
 "data/maps/IslandCave/scripts.inc":["setwildbattle SPECIES_CLAYDOL, 60"],
 "data/maps/BirthIsland_Exterior/scripts.inc":["seteventmon SPECIES_ANORITH, 65"],
 "data/maps/MarineCave_End/scripts.inc":[
   "setflag FLAG_HIDE_MARINE_CAVE_KYOGRE",
   "setwildbattle SPECIES_KYOGRE, 70",
 ],
 "data/maps/TerraCave_End/scripts.inc":[
   "setflag FLAG_HIDE_TERRA_CAVE_GROUDON",
   "setwildbattle SPECIES_GROUDON, 70",
 ],
 "data/maps/FarawayIsland_Interior/scripts.inc":["seteventmon SPECIES_RAYQUAZA, 65"],
 "data/maps/SkyPillar_Top/scripts.inc":["setwildbattle SPECIES_DEOXYS, 75"],
 "src/battle_setup.c":[
   "case SPECIES_DEOXYS: // #386 Araua",
   "MUS_ARAUNA_ARAUA_BATTLE",
   "default:",
 ],
}
FORBID={
 "data/maps/SkyPillar_Top/scripts.inc":["setwildbattle SPECIES_RAYQUAZA, 70"],
 "data/maps/FarawayIsland_Interior/scripts.inc":["seteventmon SPECIES_MEW, 30"],
 "data/maps/BirthIsland_Exterior/scripts.inc":["seteventmon SPECIES_DEOXYS, 30"],
}
EXPECTED_IMPLEMENTED={329,330,338,342,344,347,382,383,384,386}

def main()->int:
    failures=[]
    rows=list(csv.DictReader(PLAN.open(encoding="utf-8")))
    dex=[int(r["dex"]) for r in rows]
    if len(rows)!=31 or len(set(dex))!=31:
        failures.append(f"plan must list exactly 31 unique specials, got {len(rows)} rows/{len(set(dex))} unique")
    implemented={int(r["dex"]) for r in rows if r["status"]=="IMPLEMENTED"}
    if implemented!=EXPECTED_IMPLEMENTED:
        failures.append(f"implemented set mismatch: {sorted(implemented)}")
    for rel,needles in EXPECT.items():
        text=(ROOT/rel).read_text(encoding="utf-8")
        for n in needles:
            if n not in text:failures.append(f"{rel}: missing {n!r}")
    for rel,needles in FORBID.items():
        text=(ROOT/rel).read_text(encoding="utf-8")
        for n in needles:
            if n in text:failures.append(f"{rel}: stale target still present: {n!r}")
    if failures:
        print("Arauna legendary event validation FAILED:")
        for f in failures:print("-",f)
        return 1
    print("Arauna legendary event validation PASS: 31 planned, 10 Wave-1 events implemented.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())

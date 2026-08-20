#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAX=32
CTRL=re.compile(r"\\[npl]")
PH=re.compile(r"\{[^}]+\}")
T:dict[str,dict[str,tuple[str,...]]]={}
def add(p,l,*x): T.setdefault(p,{})[l]=x

R113="data/maps/Route113/scripts.inc"
add(R113,"Route113_Text_AshCanBeFashionedIntoGlass",
    "Volcanic ash can be shaped into\\n","glass.\\p",
    "People in CAMPO DAS CINZAS learned\\n","to make useful things from it.$")
add(R113,"Route113_Text_FunWalkingThroughAsh",
    "Ash keeps every footprint for a\\n","while.\\p",
    "Wind erases the path later, but not\\n","the fact that someone crossed it.$")
add(R113,"Route113_Text_RouteSign111","ROUTE 113\\n","{RIGHT_ARROW} ROUTE 111$")
add(R113,"Route113_Text_RouteSignFallarbor","ROUTE 113\\n","{LEFT_ARROW} CAMPO DAS CINZAS$")
add(R113,"Route113_Text_GlassWorkshopSign",
    "ASH GLASS WORKSHOP\\p","Turning volcanic ash into glass.$")

FALL="data/maps/FallarborTown/scripts.inc"
add(FALL,"FallarborTown_Text_ShadyCharactersCozmosHome",
    "Something is wrong.\\p",
    "HORIZON personnel have been moving\\n","around the researcher's house.$")
add(FALL,"FallarborTown_Text_RegionKnownForMeteors",
    "This region has stories of falling\\n","stones older than HORIZON.\\p",
    "RUINAS DA QUEDA carries many of\\n","those stories.$")
add(FALL,"FallarborTown_Text_HaveYouChallengedFlannery",
    "NARA leads CASA DA CINZA in\\n","SERTAO DE DENTRO.\\p",
    "She says grief is not weakness and\\n","ash is proof that something burned.$")
add(FALL,"FallarborTown_Text_BattleTentSign",
    "CAMPO DAS CINZAS BATTLE TENT\\p","Teams gather where ash settles.$")
add(FALL,"FallarborTown_Text_TownSign",
    "CAMPO DAS CINZAS\\p",
    "The DISENCHANTMENT advances where\\n","the land was already wounded.\\p",
    "DONA ZILA sees a pattern older than\\n","the HORIZON CONSORTIUM.$")
add(FALL,"FallarborTown_Text_MoveTutorSign",
    "MOVE TUTOR'S HOUSE\\p","New moves taught to POKéMON.$")

R114="data/maps/Route114/scripts.inc"
add(R114,"Route114_Text_MeteorFallsSign",
    "RUINAS DA QUEDA\\n","PATH TOWARD SERRA DO UIVO$")
add(R114,"Route114_Text_FossilManiacsHouseSign",
    "FOSSIL RESEARCHER'S HOUSE$")
add(R114,"Route114_Text_LanettesHouse",
    "FIELD STORAGE RESEARCHER'S HOUSE$")

PAC="data/maps/PacifidlogTown/scripts.inc"
add(PAC,"PacifidlogTown_Text_FastRunningCurrent",
    "The current east of CASA DA FOGUEIRA\\n","runs fast.\\p",
    "If you SURF into it, the sea chooses\\n","part of your route.$")
add(PAC,"PacifidlogTown_Text_NeatHousesOnWater",
    "Our houses rest on the water.\\p",
    "Stories move between them the same\\n","way: repeated, changed, still alive.$")
add(PAC,"PacifidlogTown_Text_SkyPillarTooScary",
    "TORRE DO JURAMENTO?\\p",
    "That tall tower rises beyond the\\n","current.\\p",
    "I prefer sea level and the stories\\n","that return to the fire.$")
add(PAC,"PacifidlogTown_Text_TownSign",
    "CASA DA FOGUEIRA\\p",
    "Stories are repeated here to stay\\n","alive, not to remain identical.$")

P={
    R113:("STEP_CB_ASH","WEATHER_VOLCANIC_ASH"),
    FALL:("FLAG_VISITED_FALLARBOR_TOWN","FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY"),
    R114:("VAR_ABNORMAL_WEATHER_LOCATION","ITEM_TM_ROAR"),
    PAC:("FLAG_VISITED_PACIFIDLOG_TOWN","STEP_CB_PACIFIDLOG_BRIDGE"),
}

def pat(l): return re.compile(rf"(?ms)^{re.escape(l)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")
def widths():
    for p,d in T.items():
        for l,lines in d.items():
            for line in lines:
                clean=PH.sub("PLAYER",line.replace("$",""))
                for s in CTRL.split(clean):
                    if len(s.strip())>MAX:
                        raise ValueError(f"{p}: {l}: {len(s.strip())}: {s.strip()!r}")
def mask(text,labels):
    out=text
    for l in labels:
        m=pat(l).search(out)
        if not m: raise ValueError(f"missing {l}")
        a,b=m.span("body"); out=out[:a]+'\t.string "<ARAUNA_EN>"\n\n'+out[b:]
    return out
def render(p,src):
    out=src; labels=tuple(T[p])
    for l,lines in T[p].items():
        ms=list(pat(l).finditer(out))
        if len(ms)!=1: raise ValueError(f"{p}: {l}: expected 1, got {len(ms)}")
        body="".join(f'\t.string "{x}"\n' for x in lines)+"\n"
        a,b=ms[0].span("body"); out=out[:a]+body+out[b:]
    if mask(src,labels)!=mask(out,labels): raise ValueError(f"{p}: non-dialogue structure changed")
    for token in P[p]:
        if token not in out: raise ValueError(f"{p}: missing preserved token {token}")
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ap.add_argument("--in-place",action="store_true"); a=ap.parse_args()
    if a.check and a.in_place: ap.error("choose --check or --in-place")
    widths(); total=sum(map(len,T.values())); changed=0
    for rel in T:
        p=ROOT/rel; src=p.read_text(encoding="utf-8"); out=render(rel,src)
        if out!=src:
            changed+=1
            if a.in_place:p.write_text(out,encoding="utf-8")
    print(f"Secondary towns English renderer OK: {total} blocks across {len(T)} files; {changed} changed.")
    return 0
if __name__=="__main__": raise SystemExit(main())

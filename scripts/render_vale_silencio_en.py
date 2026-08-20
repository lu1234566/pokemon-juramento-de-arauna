#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MAX=32
CTRL=re.compile(r"\\[npl]")
PH=re.compile(r"\{[^}]+\}")
T: dict[str,dict[str,tuple[str,...]]]={}
def add(path,label,*lines): T.setdefault(path,{})[label]=lines

R117="data/maps/Route117/scripts.inc"
add(R117,"Route117_Text_RouteSignVerdanturf","ROUTE 117\\n","{LEFT_ARROW} VALE DO SILENCIO$")
add(R117,"Route117_Text_RouteSignMauville","ROUTE 117\\n","{RIGHT_ARROW} ENCRUZILHADA CENTRAL$")
add(R117,"Route117_Text_AirIsTastyHere","The air feels quiet here.\\p","Even frightened POKéMON settle.$")

VT="data/maps/VerdanturfTown/scripts.inc"
add(VT,"VerdanturfTown_Text_ManTryingToDigTunnel","The galleries are full of timid\\n","POKéMON. Loud machines scare them.\\p","One man still digs by hand.$")
add(VT,"VerdanturfTown_Text_ManDugTunnelForLove","He opened the passage by hand.\\p","People here remember why.$")
add(VT,"VerdanturfTown_Text_AirCleanHere","The wind keeps volcanic ash away.\\p","Families displaced by the\\n","DISENCHANTMENT settled here too.$")
add(VT,"VerdanturfTown_Text_GuyTryingToBustThroughCave","The cave by the MART reaches toward\\n","GALERIAS DA SERRA.\\p","Someone is clearing it by hand.$")
add(VT,"VerdanturfTown_Text_EasyToGetToRustboroNow","The passage is open now.\\p","It reaches GALERIAS DA SERRA and\\n","the road to SERRA DO UIVO.$")
add(VT,"VerdanturfTown_Text_TownSign","VALE DO SILENCIO\\p","Displaced families live here.\\p","Many remember a lost place but\\n","can no longer say its name.$")
add(VT,"VerdanturfTown_Text_WandasHouse","VAL'S FAMILY HOUSE$")
add(VT,"VerdanturfTown_Text_BattleTentSign","VALE DO SILENCIO BATTLE TENT\\p","Practice without pretending.$")
add(VT,"VerdanturfTown_Text_RusturfTunnelSign","GALERIAS DA SERRA\\p","Hand-cleared passage toward\\n","SERRA DO UIVO.$")

WH="data/maps/VerdanturfTown_WandasHouse/scripts.inc"
add(WH,"VerdanturfTown_WandasHouse_Text_StrongerSpeech","VAL: I still get afraid.\\p","Now I know courage isn't erasing\\n","fear. It is walking with it.\\p","I want to grow without becoming\\n","someone else's idea of strong.$")
add(WH,"VerdanturfTown_WandasHouse_Text_StrongerSpeechShort","VAL: I am training at my own pace.\\p","Fear still comes. So do I.$")
add(WH,"VerdanturfTown_WandasHouse_Text_WallysNextDoor","UNCLE: VAL is resting next door.\\p","This valley gives him room to move\\n","without being rushed.$")
add(WH,"VerdanturfTown_WandasHouse_Text_WallySlippedOff","UNCLE: VAL left to train again.\\p","He did not sneak away from fear.\\p","He chose the road himself.$")
add(WH,"VerdanturfTown_WandasHouse_Text_WallyGoneThatFar","UNCLE: VAL reached the ESTRADA DO\\n","JURAMENTO?\\p","Then his own pace carried him far.$")
add(WH,"VerdanturfTown_WandasHouse_Text_MeetWanda","COUSIN: You must be {PLAYER}.\\p","VAL told us about you.\\p","He is livelier here, but nobody\\n","pushes him to perform wellness.$")
add(WH,"VerdanturfTown_WandasHouse_Text_DontWorryAboutWally","COUSIN: VAL still has hard days.\\p","We do not treat that as failure.$")
add(WH,"VerdanturfTown_WandasHouse_Text_CanSeeGirlfriendEveryDay","The passage lets us see each other\\n","without a day-long detour.\\p","That matters more than it sounds.$")
add(WH,"VerdanturfTown_WandasHouse_Text_DaughtersBoyfriendDriven","My daughter's partner kept digging\\n","the passage by hand.\\p","We worried about him, and about the\\n","POKéMON disturbed by machinery.$")
add(WH,"VerdanturfTown_WandasHouse_Text_DaughtersBoyfriendWasDigging","He really opened the passage by\\n","hand. No heavy machines.$")
add(WH,"VerdanturfTown_WandasHouse_Text_IfAnythingHappenedToWally","AUNT: VAL left to keep training.\\p","I worry, but worry cannot be a cage.$")
add(WH,"VerdanturfTown_WandasHouse_Text_WallyWasInEverGrande","AUNT: VAL reached the ESTRADA DO\\n","JURAMENTO.\\p","He has gone farther than we feared\\n","and farther than we imagined.$")

P={R117:("FLAG_PENDING_DAYCARE_EGG","TRAINER_ISAAC_1"),VT:("FLAG_VISITED_VERDANTURF_TOWN","FLAG_RUSTURF_TUNNEL_OPENED"),WH:("FLAG_WALLY_SPEECH","FLAG_DEFEATED_WALLY_MAUVILLE","FLAG_DEFEATED_WALLY_VICTORY_ROAD")}
def pat(label): return re.compile(rf"(?ms)^{re.escape(label)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")
def widths():
    for rel,d in T.items():
        for label,lines in d.items():
            for line in lines:
                clean=PH.sub("PLAYER",line.replace("$",""))
                for seg in CTRL.split(clean):
                    if len(seg.strip())>MAX: raise ValueError(f"{rel}: {label}: {len(seg.strip())}: {seg.strip()!r}")
def mask(text,labels):
    out=text
    for label in labels:
        m=pat(label).search(out)
        if not m: raise ValueError(f"missing block {label}")
        a,b=m.span("body"); out=out[:a]+'\t.string "<ARAUNA_EN>"\n\n'+out[b:]
    return out
def render(rel,src):
    out=src; labels=tuple(T[rel])
    for label,lines in T[rel].items():
        ms=list(pat(label).finditer(out))
        if len(ms)!=1: raise ValueError(f"{rel}: {label}: expected 1 block, got {len(ms)}")
        body="".join(f'\t.string "{x}"\n' for x in lines)+"\n"; a,b=ms[0].span("body"); out=out[:a]+body+out[b:]
    if mask(src,labels)!=mask(out,labels): raise ValueError(f"{rel}: non-dialogue structure changed")
    for token in P[rel]:
        if token not in out: raise ValueError(f"{rel}: missing preserved token {token}")
    return out
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ap.add_argument("--in-place",action="store_true"); a=ap.parse_args()
    if a.check and a.in_place: ap.error("choose --check or --in-place")
    widths(); total=sum(map(len,T.values())); changed=0
    for rel in T:
        p=ROOT/rel; src=p.read_text(encoding="utf-8"); out=render(rel,src)
        if out!=src:
            changed+=1
            if a.in_place: p.write_text(out,encoding="utf-8")
    print(f"Vale do Silencio English renderer OK: {total} blocks across {len(T)} files; {changed} changed.")
    return 0
if __name__=="__main__": raise SystemExit(main())

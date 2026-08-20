#!/usr/bin/env python3
from __future__ import annotations
import argparse,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAX=32; CTRL=re.compile(r"\\[npl]"); PH=re.compile(r"\{[^}]+\}")
T:dict[str,dict[str,tuple[str,...]]]={}
def add(p,l,*x): T.setdefault(p,{})[l]=x

TOWN="data/maps/LavaridgeTown/scripts.inc"
for who in ("May","Brendan"):
    add(TOWN,f"LavaridgeTown_Text_{who}NiceBadgesTakeThis",
        "CIRO: Four BADGES already.\\p",
        "You're moving faster than I\\n","expected. Take these GO-GOGGLES.$")
    add(TOWN,f"LavaridgeTown_Text_{who}ExplainGoGogglesChallengeDad",
        "CIRO: They let you cross the\\n","desert safely.\\p",
        "If the data is right, the\\n","DISENCHANTMENT can be treated.\\p",
        "I'd rather test an answer than\\n","turn suffering into tradition.$")
add(TOWN,"LavaridgeTown_Text_BatheInHotSpringsEveryDay",
    "I use the hot springs every day.\\p",
    "NARA says strength is not acting\\n","like nothing ever hurt.$")
add(TOWN,"LavaridgeTown_Text_TownSign",
    "SERTAO DE DENTRO\\p",
    "Ash, heat and abandonment marked\\n","this region.\\p",
    "Here, grief is not called weakness.$")
add(TOWN,"LavaridgeTown_Text_GymSign",
    "CASA DA CINZA\\n","LEADER: NARA\\p","Ash also keeps memory.$")

GYM="data/maps/LavaridgeTown_Gym_1F/scripts.inc"
add(GYM,"LavaridgeTown_Gym_1F_Text_GymGuideAdvice",
    "CASA DA CINZA is led by NARA.\\p",
    "She uses FIRE POKéMON.\\p",
    "WATER and GROUND can help.\\p",
    "The hot-sand traps connect both\\n","floors of the GYM.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_GymGuidePostVictory",
    "That battle burned clean.\\p","The ASH BADGE is yours.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_AxleDefeat","I hope NARA tests you harder.$")
add(GYM,"LavaridgeTown_Gym_B1F_Text_KeeganPostBattle",
    "Your skill is real.\\p","NARA will make you face what\\n","remains after the heat.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_DaniellePostBattle",
    "I want to become strong like NARA.\\p",
    "She never asks us to hide pain.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_FlanneryIntro",
    "NARA: Ash is what remains after\\n","fire.\\p",
    "It is not the end of everything.\\p",
    "But we should not pretend nothing\\n","burned. Show me what you carry.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_FlanneryDefeat",
    "NARA: You endured the heat without\\n","denying what it changed.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_ReceivedHeatBadge",
    "{PLAYER} received the\\n","ASH BADGE from NARA.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_ExplainHeatBadgeTakeThis",
    "With the ASH BADGE, traded POKéMON\\n","up to Lv. 50 obey you.\\p",
    "It also lets you use STRENGTH\\n","outside battle. Take this TM.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_RegisteredFlannery",
    "Registered GYM LEADER NARA\\n","in the POKéNAV.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_FlanneryPostBattle",
    "NARA: Healing is not restoring a\\n","world that no longer exists.\\p",
    "It is learning what can grow in\\n","the ash.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_GymStatue","SERTAO DE DENTRO POKéMON GYM$")
add(GYM,"LavaridgeTown_Gym_1F_Text_GymStatueCertified",
    "SERTAO DE DENTRO POKéMON GYM\\p",
    "NARA'S CERTIFIED TRAINERS:\\n","{PLAYER}$")
add(GYM,"LavaridgeTown_Gym_1F_Text_FlanneryPreRematch",
    "NARA: Old ash moves when new wind\\n","arrives. Ready?$")
add(GYM,"LavaridgeTown_Gym_1F_Text_FlanneryRematchDefeat",
    "NARA: Different fire. Different ash.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_FlanneryPostRematch",
    "NARA: Return when something else\\n","changes what you carry.$")
add(GYM,"LavaridgeTown_Gym_1F_Text_FlanneryRematchNeedTwoMons",
    "NARA: Bring at least two POKéMON\\n","for a rematch.$")

P={TOWN:("FLAG_VISITED_LAVARIDGE_TOWN","ITEM_GO_GOGGLES","FLAG_RECEIVED_GO_GOGGLES"),GYM:("TRAINER_FLANNERY_1","FLAG_BADGE04_GET","ITEM_TM_OVERHEAT","FLAG_DEFEATED_LAVARIDGE_GYM")}
def pat(l): return re.compile(rf"(?ms)^{re.escape(l)}:\n(?P<body>.*?)(?=^[A-Za-z0-9_]+(?:::|:)(?:\n|$)|\Z)")
def widths():
    for p,d in T.items():
        for l,lines in d.items():
            for line in lines:
                clean=PH.sub("PLAYER",line.replace("$",""))
                for s in CTRL.split(clean):
                    if len(s.strip())>MAX: raise ValueError(f"{p}: {l}: {len(s.strip())}: {s.strip()!r}")
def mask(text,labels):
    out=text
    for l in labels:
        m=pat(l).search(out)
        if not m: raise ValueError(f"missing block {l}")
        a,b=m.span("body"); out=out[:a]+'\t.string "<ARAUNA_EN>"\n\n'+out[b:]
    return out
def render(p,src):
    out=src; labels=tuple(T[p])
    for l,lines in T[p].items():
        ms=list(pat(l).finditer(out))
        if len(ms)!=1: raise ValueError(f"{p}: {l}: expected 1, got {len(ms)}")
        body="".join(f'\t.string "{x}"\n' for x in lines)+"\n"; a,b=ms[0].span("body"); out=out[:a]+body+out[b:]
    if mask(src,labels)!=mask(out,labels): raise ValueError(f"{p}: non-dialogue structure changed")
    for token in P[p]:
        if token not in out: raise ValueError(f"{p}: missing {token}")
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
    print(f"Sertao/Nara English renderer OK: {total} blocks across {len(T)} files; {changed} changed.")
    return 0
if __name__=="__main__": raise SystemExit(main())

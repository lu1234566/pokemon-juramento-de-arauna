#!/usr/bin/env python3
from __future__ import annotations
import argparse,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAX=32; CTRL=re.compile(r"\\[npl]"); PH=re.compile(r"\{[^}]+\}")
T:dict[str,dict[str,tuple[str,...]]]={}
def add(p,l,*x): T.setdefault(p,{})[l]=x

A1="data/maps/AquaHideout_1F/scripts.inc"
add(A1,"AquaHideout_1F_Text_OurBossIsSnatchingSomething",
    "HORIZON: The director left to obtain\\n","a key LIVING ARCHIVE component.\\p",
    "Don't expect me to say where.$")
add(A1,"AquaHideout_1F_Text_WhereMightMagmaHideoutBe",
    "HORIZON: The REMEMBRANCERS built a\\n","base near SERRA DA CINZA.\\p",
    "LUZIA wants the records before we\\n","reach them.$")
add(A1,"AquaHideout_1F_Text_BossWentToJackASubmarine",
    "HORIZON: OTACILIO went to\\n","PORTO DO SAL.\\p",
    "The submersible can reach the caves\\n","of M'BOI.$")
add(A1,"AquaHideout_1F_Text_BossIsOnRoute122",
    "HORIZON: OTACILIO went to\\n","MEMORIAL DOS NOMES on ROUTE 122.\\p",
    "He wants the records kept there.$")
add(A1,"AquaHideout_1F_Text_TeamMagmaAtMtChimney",
    "HORIZON: The REMEMBRANCERS are at\\n","SERRA DA CINZA.\\p",
    "They say LUZIA plans to return\\n","memories taken by force.$")
add(A1,"AquaHideout_1F_Text_BossIsInSlateportCity",
    "HORIZON: OTACILIO is in PORTO DO SAL.\\p",
    "The public LIVING ARCHIVE demo starts\\n","there.$")
add(A1,"AquaHideout_1F_Text_Grunt1Intro",
    "HORIZON: Sensors detect unstable\\n","BONDS before full DISENCHANTMENT.\\p",
    "That could save entire families.$")
add(A1,"AquaHideout_1F_Text_Grunt1Defeat",
    "HORIZON: The LIVING ARCHIVE does not\\n","erase people.\\p",
    "It separates trauma from identity.\\p",
    "At least, that is what we were taught.$")
add(A1,"AquaHideout_1F_Text_Grunt1PostBattle",
    "HORIZON: Sensors detect unstable\\n","BONDS before full DISENCHANTMENT.\\p",
    "That could save entire families.$")

F1="data/maps/RustboroCity_Flat2_1F/scripts.inc"
add(F1,"RustboroCity_Flat2_1F_Text_DevonWorkersLiveHere",
    "Many HORIZON CONSORTIUM employees\\n","live in this building.$")

F2="data/maps/RustboroCity_Flat2_2F/scripts.inc"
add(F2,"RustboroCity_Flat2_2F_Text_DevonWasTinyInOldDays",
    "The HORIZON CONSORTIUM began as a\\n","very small project.$")
add(F2,"RustboroCity_Flat2_2F_Text_MyDaddyMadeThisYouCanHaveIt",
    "My dad works for HORIZON.\\p",
    "He helped make this! I don't use it,\\n","so you can have it.$")
add(F2,"RustboroCity_Flat2_2F_Text_GoingToWorkAtDevonToo",
    "My dad works for HORIZON.\\p",
    "When I grow up, I want to do field\\n","research too.$")

F3="data/maps/RustboroCity_Flat2_3F/scripts.inc"
add(F3,"RustboroCity_Flat2_3F_Text_PresidentCollectsRareStones",
    "HORIZON leadership keeps rare samples\\n","collected from the mountain.$")
add(F3,"RustboroCity_Flat2_3F_Text_PresidentsSonAlsoCollectsRareStones",
    "Many people here collect stones and\\n","minerals from field work.$")

MOTEL="data/maps/LilycoveCity_CoveLilyMotel_1F/scripts.inc"
add(MOTEL,"LilycoveCity_CoveLilyMotel_1F_Text_NoGuestsWithTeamAqua",
    "Oh, sorry! I was watching TV.\\p",
    "Since the HORIZON CONSORTIUM came to\\n","town, tourists have stayed away.$")
add(MOTEL,"LilycoveCity_CoveLilyMotel_1F_Text_HeardAquaHideoutBusted",
    "Oh, sorry! I was watching TV.\\p",
    "I heard someone broke into the\\n","HORIZON hideout.\\p",
    "Now a large group booked rooms.\\p",
    "They called themselves GAME FREAK.$")

P={
 A1:("TRAINER_GRUNT_AQUA_HIDEOUT_1","FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT","FLAG_RECEIVED_RED_OR_BLUE_ORB"),
 F1:("SPECIES_SKITTY",),
 F2:("ITEM_PREMIER_BALL","FLAG_RECEIVED_PREMIER_BALL_RUSTBORO"),
 F3:("RustboroCity_Flat2_3F_EventScript_DevonEmployee",),
 MOTEL:("FLAG_SYS_GAME_CLEAR","FLAG_BADGE07_GET","LOCALID_MOTEL_OWNER"),
}
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
        if not m: raise ValueError(f"missing {l}")
        a,b=m.span("body"); out=out[:a]+'\t.string "<ARAUNA_EN>"\n\n'+out[b:]
    return out
def render(p,src):
    out=src; labels=tuple(T[p])
    for l,lines in T[p].items():
        ms=list(pat(l).finditer(out))
        if len(ms)!=1: raise ValueError(f"{p}: {l}: expected 1 got {len(ms)}")
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
    print(f"HORIZON gap renderer OK: {total} blocks across {len(T)} files; {changed} changed.")
    return 0
if __name__=="__main__": raise SystemExit(main())

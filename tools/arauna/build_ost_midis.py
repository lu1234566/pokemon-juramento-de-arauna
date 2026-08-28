#!/usr/bin/env python3
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transcribe_ost import transcribe
import numpy as np

RAW=os.environ.get("ARAUNA_OST_RAW", "ost_masters")  # dir with the 21 MP3s (external, not versioned)
MIDI_OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "sound", "songs", "midi")

# (order#, mp3, MUS const, midi basename, PlayerContext, is_battle)
SONGS = [
 (1,"Juramento de Arauna.mp3","MUS_ARAUNA_MAIN","mus_arauna_main",False),
 (2,"Onde a Jornada Nasce.mp3","MUS_ARAUNA_VILA_AMANHECER","mus_arauna_vila_amanhecer",False),
 (3,"Terra de Arauna.mp3","MUS_ARAUNA_ROUTE","mus_arauna_route",False),
 (4,"Instinto Selvagem.mp3","MUS_ARAUNA_WILD_BATTLE","mus_arauna_wild_battle",True),
 (5,"Um Desafio à Frente.mp3","MUS_ARAUNA_TRAINER_BATTLE","mus_arauna_trainer_battle",True),
 (6,"Sempre Um Passo à Frente.mp3","MUS_ARAUNA_CIRO","mus_arauna_ciro",False),
 (7,"Rival à Altura.mp3","MUS_ARAUNA_CIRO_BATTLE","mus_arauna_ciro_battle",True),
 (8,"O Preço de Vencer.mp3","MUS_ARAUNA_CIRO_FINAL","mus_arauna_ciro_final",True),
 (9,"Progresso a Qualquer Custo.mp3","MUS_ARAUNA_HORIZON","mus_arauna_horizon",False),
 (10,"Máquina de Controle.mp3","MUS_ARAUNA_HORIZON_BATTLE","mus_arauna_horizon_battle",True),
 (11,"Prova de Arauna.mp3","MUS_ARAUNA_GYM_BATTLE","mus_arauna_gym_battle",True),
 (12,"Algo Não Deveria Estar Aqui.mp3","MUS_ARAUNA_STORY_BOSS","mus_arauna_story_boss",True),
 (13,"Vozes Antes dos Homens.mp3","MUS_ARAUNA_LEGEND_ENCOUNTER","mus_arauna_legend_encounter",False),
 (14,"Força Primordial.mp3","MUS_ARAUNA_LEGEND_BATTLE","mus_arauna_legend_battle",True),
 (15,"Aquele Que Lembra.mp3","MUS_ARAUNA_ARAUA_ENCOUNTER","mus_arauna_araua_encounter",False),
 (16,"O Primeiro Juramento.mp3","MUS_ARAUNA_ARAUA_BATTLE","mus_arauna_araua_battle",True),
 (17,"O Peso do Juramento.mp3","MUS_ARAUNA_OATH_ROAD","mus_arauna_oath_road",False),
 (18,"Os Que Permaneceram de Pé.mp3","MUS_ARAUNA_ELITE_BATTLE","mus_arauna_elite_battle",True),
 (19,"Até Onde Você Chegou.mp3","MUS_ARAUNA_CHAMPION_BATTLE","mus_arauna_champion_battle",True),
 (20,"Depois do Juramento.mp3","MUS_ARAUNA_CREDITS","mus_arauna_credits",False),
 (21,"The Sapphire Crypt.mp3","MUS_ARAUNA_SAPPHIRE_CRYPT","mus_arauna_sapphire_crypt",False),
]

BASE_INDEX=610
results=[]
rms_list=[]
for order,mp3,const,base,is_batt in SONGS:
    st=transcribe(os.path.join(RAW,mp3), os.path.join(MIDI_OUT,base+".mid"))
    st.update(order=order,mp3=mp3,const=const,base=base,is_batt=is_batt)
    results.append(st); rms_list.append(st["rms"])

# perceptual volume normalisation: target a reference RMS, map to -V (60..110)
ref=np.median(rms_list)
for st in results:
    ratio=ref/max(st["rms"],1e-6)
    v=int(np.clip(round(80*ratio),60,110))
    st["vol"]=v

# emit wiring snippets
lines_table=[]; lines_const=[]; lines_cfg=[]
for i,st in enumerate(results):
    idx=BASE_INDEX+i
    lines_table.append(f"\tsong {st['base']}, MUSIC_PLAYER_BGM, 0")
    lines_const.append(f"#define {st['const']:<32} {idx}")
    pri=" -P1" if st["is_batt"] else ""
    lines_cfg.append(f"{st['base']}.mid:{' '*(30-len(st['base']))}-E -R50 -G_arauna_ost -V{st['vol']:03d}{pri}")

open("wiring_table.txt","w").write("\n".join(lines_table)+"\n")
open("wiring_const.txt","w").write("\n".join(lines_const)+"\n")
open("wiring_cfg.txt","w").write("\n".join(lines_cfg)+"\n")

for st in results:
    print(f"{st['order']:2} {st['base']:30} idx? bpm={st['bpm']:3} dur={st['dur']:5.1f} mel={st['mel']:3} bass={st['bass']:3} V{st['vol']:03d}")
print("\n== wiring snippets written to scratchpad/ost/wiring_*.txt ==")
json.dump(results, open("ost_results.json","w"), ensure_ascii=False, indent=1)

#!/usr/bin/env python3
"""Verify the actual native streams and the actual C selector, without a ROM harness."""
import json, re, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from export import ROOT, HERE, decode_lz

GBAGFX=ROOT/'tools/gbagfx/gbagfx'

def native_streams(p, tmp):
    """Rebuild os tres fluxos nativos com o gbagfx do proprio repositorio.

    O que esta versionado e tiles.png, map.bin e palette.pal -- .4bpp, .gbapal
    e .lz sao produto de build: o .gitignore os ignora e o clean-assets do
    Makefile apaga os tres em toda a arvore. Refazer aqui, com a ferramenta que
    a compilacao usa, confere duas coisas de uma vez: os fluxos continuam
    validos e sao os mesmos que a ROM vai receber.
    """
    saida={}
    for origem,destino in [('tiles.png','tiles.4bpp'),('palette.pal','palette.gbapal')]:
        alvo=tmp/(p.name+'_'+destino)
        subprocess.run([str(GBAGFX),str(p/origem),str(alvo)],check=True)
        saida[destino]=alvo
    saida['map.bin']=p/'map.bin'
    for nome,caminho in list(saida.items()):
        comprimido=tmp/(p.name+'_'+nome+'.lz')
        subprocess.run([str(GBAGFX),str(caminho),str(comprimido)],check=True)
        assert decode_lz(comprimido.read_bytes())==caminho.read_bytes(),(p.name,nome)
    return saida

def verify_assets(records):
  with tempfile.TemporaryDirectory() as _tmp:
    tmp=Path(_tmp)
    for row in records:
        p=ROOT/'graphics/battle_environment/arauna'/row['id'].lower()
        fluxos=native_streams(p,tmp)
        raw=np.frombuffer(fluxos['tiles.4bpp'].read_bytes(),dtype='uint8')
        tiles=np.stack([raw&15,raw>>4],axis=-1).reshape(-1,8,8)
        tilemap=np.frombuffer((p/'map.bin').read_bytes(),dtype='<u2').reshape(2,32,32)
        assert np.all((tilemap&1023)<len(tiles))
        assert set((tilemap>>12).ravel())<={2,3,4}
        pal=np.frombuffer(fluxos['palette.gbapal'].read_bytes(),dtype='<u2')
        rgb=np.stack([pal&31,(pal>>5)&31,(pal>>10)&31],axis=-1)
        rgb=((rgb*255+15)//31).astype('uint8');out=np.zeros((128,240,3),dtype='uint8')
        for y in range(16):
            for x in range(30):
                v=int(tilemap[0,y,x]);t=tiles[v&1023]
                if v&1024:t=t[:,::-1]
                if v&2048:t=t[::-1]
                out[y*8:y*8+8,x*8:x*8+8]=rgb[t+((v>>12)-2)*16]
        assert np.array_equal(out,np.array(Image.open(p/'scene.png').convert('RGB'))),row['id']
        assert len(tiles)<=512 and len(pal)==48
    assert len(records)==47

def verify_selector(records):
    # Stub only the ROM bytes/hardware globals; compile the production selector.
    source='''#include <stdint.h>
#include <stddef.h>
#include <assert.h>
typedef uint8_t bool8;
typedef uint16_t u16;
typedef uint32_t u32;
#include "constants/map_groups.h"
#include "constants/opponents.h"
#include "constants/battle.h"
#define INCBIN_U32(path) {0}
// O header usa INCGFX, que e macro do preproc do repositorio e nao do cc.
// Aqui so interessa o seletor, entao os fluxos viram array vazio.
#define INCGFX_U32(path, ext) {0}
struct BattleBackground {const void *tileset,*tilemap,*entryTileset,*entryTilemap,*palette;};
struct TestSave {struct {uint8_t mapGroup,mapNum;} location;} save, *gSaveBlock1Ptr=&save;
u32 gBattleTypeFlags;
u16 gTrainerBattleOpponent_A;
uint8_t gBattleEnvironment;
#include "data/arauna_battle_backgrounds.h"
static void place(u16 map) {save.location.mapGroup=map>>8;save.location.mapNum=map&255;}
int main(void) {
'''
    assertions=0
    def check(expr):
        nonlocal source,assertions
        source+='assert('+expr+');\n';assertions+=1
    for c in records[:34]:
        id=c['id'];water=c['terrain']=='água'
        env='WATER' if water else ('SAND' if id=='R111' else 'GRASS')
        source+=f'place(MAP_ROUTE{id[1:]});gBattleTypeFlags=0;gBattleEnvironment=BATTLE_ENVIRONMENT_{env};\n'
        check(f'GetAraunaBattleBackground()==&sAraunaBg_{id}')
        source+=f'gBattleEnvironment=BATTLE_ENVIRONMENT_{"GRASS" if water else "WATER"};\n'
        check('GetAraunaBattleBackground()==NULL')
        source+='gBattleEnvironment=BATTLE_ENVIRONMENT_UNDERWATER;\n';check('GetAraunaBattleBackground()==NULL')
    source+='place(MAP_ROUTE111);gBattleEnvironment=BATTLE_ENVIRONMENT_PLAIN;\n';check('GetAraunaBattleBackground()==NULL')
    for row in json.loads((HERE/'map_coverage.json').read_text()):
        source+=f'place({row["map"]});gBattleEnvironment=BATTLE_ENVIRONMENT_BUILDING;\n'
        check(f'GetAraunaBattleBackground()==&sAraunaBg_{row["background"]}')
    source+='place(MAP_ROUTE101);gBattleTypeFlags=BATTLE_TYPE_TRAINER;\n'
    for n,name in enumerate(['ROXANNE','BRAWLY','WATTSON','FLANNERY','NORMAN','WINONA','TATE_AND_LIZA','JUAN'],1):
        for level in range(1,6):
            source+=f'gTrainerBattleOpponent_A=TRAINER_{name}_{level};\n'
            check(f'GetAraunaBattleBackground()==&sAraunaBg_G{n:02d}')
    for n,name in enumerate(['SIDNEY','PHOEBE','GLACIA','DRAKE','WALLACE'],1):
        source+=f'gTrainerBattleOpponent_A=TRAINER_{name};\n'
        check(f'GetAraunaBattleBackground()==&sAraunaBg_{"C01" if n==5 else f"E{n:02d}"}')
    for flag in ['LINK','FRONTIER','RECORDED','RECORDED_LINK','EREADER_TRAINER','TRAINER_HILL','SECRET_BASE','GROUDON','KYOGRE','KYOGRE_GROUDON','RAYQUAZA','INGAME_PARTNER']:
        source+=f'gBattleTypeFlags=BATTLE_TYPE_TRAINER|BATTLE_TYPE_{flag};\n';check('GetAraunaBattleBackground()==NULL')
    source+='gBattleTypeFlags=0;place(MAP_LITTLEROOT_TOWN);\n';check('GetAraunaBattleBackground()==NULL')
    source+='return 0;}\n'
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp);(p/'selector.c').write_text(source)
        subprocess.run(['cc','-std=c99','-I',str(ROOT/'include'),'-I',str(ROOT/'src'),str(p/'selector.c'),'-o',str(p/'selector')],check=True)
        subprocess.run([str(p/'selector')],check=True)
    return assertions

if __name__=='__main__':
    records=json.loads((HERE/'manifest.json').read_text());verify_assets(records);count=verify_selector(records)
    result={'assets':47,'selector_assertions':count,'native_reconstruction':'pixel-exact','lz77':'round-trip pass','vram':'all <=512 tiles','palette':'3 banks x16 RGB555','status':'PASS'}
    print(json.dumps(result,indent=2))

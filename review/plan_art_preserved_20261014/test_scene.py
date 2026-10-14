"""Directed Ciro animation fixtures; not a natural playthrough."""
import ctypes as C,json,re,subprocess
from pathlib import Path
from PIL import Image
Q=Path(__file__).resolve().parent;R=Q.parent.parent
l=C.CDLL(str(Q/'mgba_helper.so'));l.boot.argtypes=[C.c_char_p];l.invokex.argtypes=[C.c_uint32,C.POINTER(C.c_uint32),C.POINTER(C.c_uint32)];l.rd.restype=C.c_uint32;l.pc.restype=C.c_uint32
listing=subprocess.check_output(['arm-none-eabi-nm','-n',str(R/'pokemon-juramento-de-arauna-en_modern.elf')],text=True)
syms={n:int(a,16) for a,k,n in (line.split() for line in listing.splitlines() if len(line.split())==3)}
def call(n,*args):
    v=C.c_uint32();a=(C.c_uint32*8)(*(list(args)+[0]*8)[:8]);assert l.invokex(syms[n],a,C.byref(v)),(n,l.pc());return v.value
def rd(a,n=4):return l.rd(a,n)
def wr(a,v,n=4):l.wr(a,v,n)
def const(name):
    s='\n'.join(p.read_text() for p in (R/'include/constants').glob('*.h'));defs=dict(re.findall(r'^#define\s+(\w+)\s+([^\n]+)',s,re.M))
    def resolve(n):
        e=defs[n].split('//')[0].strip();e=re.sub(r'\b[A-Za-z_]\w*\b',lambda m:str(resolve(m[0])) if m[0] in defs else m[0],e);assert re.fullmatch(r'[0-9a-fA-FxX()+* /|&~<>-]+',e);return int(eval(e,{'__builtins__':{}}))
    return resolve(name)
def snap(name):
    p=Q/(name+'.rgba');l.pixels(str(p).encode());Image.frombytes('RGBA',(240,160),p.read_bytes()).save(Q/(name+'.png'));p.unlink()
assert l.boot(str(R/'pokemon-juramento-de-arauna-en_modern.gba').encode())
l.frames(0,750);call('NewGameInitData');call('ScriptContext_Stop');call('SetWarpDestination',0,18,255,10,8);call('WarpIntoMap');call('SetMainCallback2',syms['CB2_LoadMap']|1);l.frames(0,110)
for gender in (0,1):
    sb2=rd(syms['gSaveBlock2Ptr']);wr(sb2+8,gender,1);call('ResetInitialPlayerAvatarState');call('SetMainCallback2',syms['CB2_LoadMap']|1);l.frames(0,120)
    for phase,gfx in [('f2',const('OBJ_EVENT_GFX_CIRO_CONSORCIO')),('f3',const('OBJ_EVENT_GFX_CIRO_FINAL'))]:
        idx=call('SpawnSpecialObjectEventParameterized',gfx,0,200,19,15,3);assert idx<16;obj=syms['gObjectEvents']+idx*0x24
        for direction in ('SOUTH','NORTH'):
            action=const('MOVEMENT_ACTION_WALK_NORMAL_'+{'SOUTH':'DOWN','NORTH':'UP'}[direction])
            for step in range(2):
                call('ObjectEventClearHeldMovement',obj);call('ObjectEventForceSetHeldMovement',obj,action)
                for i in range(8):l.frames(0,2);snap(f'ciro_g{gender}_{phase}_{direction}_{step}_{i}')
        call('RemoveObjectEventByLocalIdAndMap',200,18,0)
print('Ciro F2/F3 north/south, both player genders: PASS')

#!/usr/bin/env python3
"""Build six Vale do Silêncio interiors from native rustic modules."""
from __future__ import annotations
import json, struct, shutil, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
import render_vale_interiors_native as render

ATLAS = ROOT / 'art/arauna_vale_interiors_v1/source_atlas.png'
BANK = ROOT / 'data/tilesets/secondary/arauna_vale_interiors_v1'
LAYOUTS = ROOT / 'data/layouts/layouts.json'
OUT = ROOT / 'review/vale_interiors_v1'
SYMBOL = 'AraunaValeInteriorsV1'
GRAYS = render.INDEX_GRAYS

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

def words(path): return render.words(path)
def packed(items): return struct.pack('<%dH' % len(items), *items)

def artwork():
    src = Image.open(ATLAS).convert('RGB')
    assert src.width >= 1200 and src.height >= 1200
    configs = [
        ('floor', (32,32),6), ('wall',(48,48),6), ('window',(48,48),11), ('door',(48,48),6),
        ('hearth',(48,48),8), ('table',(48,48),7), ('rug',(48,32),7), ('lantern',(16,32),8),
        ('shelf',(32,32),7), ('bed',(32,32),7), ('chart',(32,32),7), ('stair',(32,32),6),
        ('healer',(64,48),9), ('pc',(32,32),9), ('link',(48,32),9), ('plant',(32,32),10),
    ]
    raw = {}
    for i,(name,size,palette) in enumerate(configs):
        row,col=divmod(i,4)
        x0=round(col*src.width/4)+23; x1=round((col+1)*src.width/4)-22
        y0=round(row*src.height/4)+21; y1=round((row+1)*src.height/4)-20
        part=src.crop((x0,y0,x1,y1)).convert('RGBA')
        part.putdata([(r,g,b,0 if r>160 and b>160 and g<130 else 255) for r,g,b,a in part.getdata()])
        if name != 'floor': part=part.crop(part.getbbox())
        part=part.resize(size,Image.Resampling.NEAREST)
        raw[name]=(part,palette)
    palette_colors={}
    for slot in range(6,13):
        colors=[(r,g,b) for image,s in raw.values() if s==slot for r,g,b,a in image.getdata() if a]
        if not colors: continue
        sample=Image.new('RGB',(len(colors),1));sample.putdata(colors)
        q=sample.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
        palette_colors[slot]=[(255,0,255)]+[tuple(round(c*31/255)*255//31 for c in q[j:j+3]) for j in range(0,45,3)]
    output={}
    dest=ROOT/'art/arauna_vale_interiors_v1/native_assets';dest.mkdir(parents=True,exist_ok=True)
    for name,(im,slot) in raw.items():
        palette=palette_colors[slot]
        indices=[0 if not a else min(range(1,16),key=lambda j:sum((v-w)**2 for v,w in zip((r,g,b),palette[j]))) for r,g,b,a in im.getdata()]
        tile=Image.new('L',im.size);tile.putdata(indices);output[name]=(tile,slot)
        preview=Image.new('RGBA',im.size);preview.putdata([(*palette[index],255 if index else 0) for index in indices]);preview.save(dest/(name+'.png'))
    # Native indexed timber: shallow seams, no transparent gutters.
    floor=Image.new('L',(32,32))
    floor.putdata([4 if y%8==7 else (3 if x%16==(8 if (y//8)%2 else 0) else
                   (1 if (x*7+y*11)%37==0 else 2)) for y in range(32) for x in range(32)])
    output['floor']=(floor,6)
    # Cream plaster over a timber dado; columns repeat at module boundaries.
    wall=Image.new('L',(48,48))
    wall.putdata([6 if x in (0,1,46,47) else
                  (5 if y in (30,31,46,47) else
                   (2 if y<30 else 4))
                  for y in range(48) for x in range(48)])
    output['wall']=(wall,12)
    palette_colors[12]=[(255,0,255),(239,230,204),(214,206,181),(184,168,139),
                       (148,120,87),(112,84,60),(78,59,46)]+[(78,59,46)]*9
    return output,palette_colors

class Tiles:
    FIXED={0x21e,0x25d,0x264,0x2dc,0x2e4,0x290,0x291,0x298,0x299}
    FIXED.update(range(0x280,0x28e))
    FIXED.update(range(0x2a0,0x2ae))
    def __init__(self):
        self.art,self.palettes=artwork(); self.sheet=[Image.new('L',(8,8)) for _ in range(512)]
        self.cache={};self.meta_cache={};self.entries=[0]*4096;self.attrs=[0]*512
        self.used=0;self.labels={};self.ids=set();self.blank=self.tile(Image.new('L',(8,8)))
    def tile(self,im):
        key=im.tobytes()
        if key in self.cache:return self.cache[key]
        i=self.used
        if i >= 480: raise ValueError(f'Secondary 4bpp tile budget exceeded: {i}')
        self.used+=1;self.sheet[i]=im.copy()
        for transform,flags in ((None,0),(Image.Transpose.FLIP_LEFT_RIGHT,0x400),(Image.Transpose.FLIP_TOP_BOTTOM,0x800),(Image.Transpose.ROTATE_180,0xc00)):
            self.cache.setdefault(key if transform is None else im.transpose(transform).tobytes(),512+i|flags)
        return 512+i
    def quarters(self,im,slot):
        return [self.tile(im.crop((x,y,x+8,y+8)))|(slot<<12) for x,y in ((0,0),(8,0),(0,8),(8,8))]
    def meta(self,lower,upper=None,attr=0,label=''):
        entries=tuple(lower)+tuple(upper if upper is not None else [self.blank]*4)
        key=entries+(attr,)
        if key in self.meta_cache:return self.meta_cache[key]
        m=next(i for i in range(512,1024) if i not in self.ids and i not in self.FIXED)
        if m>=1024:raise ValueError('Metatile budget exceeded')
        self.ids.add(m);self.meta_cache[key]=m;self.labels[str(m)]=label
        self.entries[(m-512)*8:(m-512)*8+8]=entries;self.attrs[m-512]=attr
        return m
    def fixed(self,mid,lower,upper,attr,label):
        assert mid in self.FIXED
        self.ids.add(mid);self.labels[str(mid)]=label
        self.entries[(mid-512)*8:(mid-512)*8+8]=tuple(lower)+tuple(upper)
        self.attrs[mid-512]=attr
    def stamp(self,name,lower,blocking=True,attr=0):
        im,slot=self.art[name];result=[]
        for y in range(0,im.height,16):
            row=[]
            for x in range(0,im.width,16):
                q=self.quarters(im.crop((x,y,x+16,y+16)),slot)
                row.append(self.meta(lower,q,attr if attr else (0x1000 if blocking else 0),name))
            result.append(row)
        return result
    def save(self):
        BANK.mkdir(parents=True,exist_ok=True)
        shutil.copytree(ROOT/'data/tilesets/secondary/generic_building/palettes',BANK/'palettes',dirs_exist_ok=True)
        sheet=Image.new('P',(128,256))
        sheet.putpalette([v for g in GRAYS for v in (g,g,g)]+[0]*720)
        for i,im in enumerate(self.sheet):sheet.paste(im,(i%16*8,i//16*8))
        sheet.save(BANK/'tiles.png',bits=4)
        for slot,palette in self.palettes.items():
            (BANK/f'palettes/{slot:02}.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,rgb)) for rgb in palette)+'\n')
        count=max(self.ids)-511
        (BANK/'metatiles.bin').write_bytes(packed(self.entries[:count*8]))
        (BANK/'metatile_attributes.bin').write_bytes(packed(self.attrs[:count]))
        return count

def build_room(t,w,h,kind,number=0):
    floor=t.art['floor'][0]; fslot=t.art['floor'][1]
    base=[t.meta(t.quarters(floor.crop((x,y,x+16,y+16)),fslot),label='timber floor') for y in (0,16) for x in (0,16)]
    plain=t.meta(t.quarters(floor.crop((0,0,16,16)),fslot),label='plank floor')
    walls=t.stamp('wall',t.quarters(floor.crop((0,0,16,16)),fslot))
    windows=t.stamp('window',t.quarters(floor.crop((0,0,16,16)),fslot))
    door=t.stamp('door',t.quarters(floor.crop((0,0,16,16)),fslot))
    furniture={n:t.stamp(n,t.quarters(floor.crop((0,0,16,16)),fslot)) for n in ('hearth','table','rug','lantern','shelf','bed','chart','stair','healer','pc','link','plant')}
    if kind!='house':
        # Shared Cable Club scripts replace these metatiles by their numeric IDs.
        floor_q=t.quarters(floor.crop((0,0,16,16)),fslot)
        t.fixed(0x21e,floor_q,[t.blank]*4,0,'link barrier upper')
        mid=furniture['link'][1][1];t.fixed(0x25d,floor_q,t.entries[(mid-512)*8+4:(mid-512)*8+8],0x1000,'link barrier lower')
        door_image,door_slot=t.art['door']
        t.fixed(0x264,floor_q,t.quarters(door_image.crop((16,16,32,32)),door_slot),0x69,'cable club door')
        for mid in (0x2dc,0x2e4):t.fixed(mid,floor_q,[t.blank]*4,0,'opened link barrier')
        stair_image,stair_slot=t.art['stair']
        original_center_attrs=words(ROOT/'data/tilesets/secondary/pokemon_center/metatile_attributes.bin')
        stair_quads=[t.quarters(stair_image.crop((x,y,x+16,y+16)),stair_slot) for y in (0,16) for x in (0,16)]
        for ids in ((0x280,0x281,0x288,0x289,0x290,0x291),(0x298,0x299,0x2a0,0x2a1,0x2a8,0x2a9)):
            for index,mid in enumerate(ids):
                attr=original_center_attrs[mid-512]
                t.fixed(mid,floor_q,stair_quads[index%4],attr,'timber escalator')
        for mid in t.FIXED-t.ids:
            if 0x280<=mid<=0x28d or 0x2a0<=mid<=0x2ad:
                t.fixed(mid,floor_q,stair_quads[mid&1],original_center_attrs[mid-512],'escalator animation')
    grid=[0x3000|base[(y%2)*2+x%2] for y in range(h) for x in range(w)]
    occupied=set(); modules=[]
    def put(x,y,mid,z=3,blocked=False):
        assert 0<=x<w and 0<=y<h,(kind,x,y)
        grid[y*w+x]=mid|(z<<12)|(0x400 if blocked else 0)
        if blocked:occupied.add((x,y))
        else:occupied.discard((x,y))
    def stamp(name,x,y,blocking=True):
        shape={'wall':walls,'window':windows,'door':door}.get(name,furniture.get(name))
        assert shape,name
        coords=[]
        for dy,row in enumerate(shape):
            for dx,mid in enumerate(row):
                put(x+dx,y+dy,mid,3,blocking)
                coords.append((x+dx,y+dy))
        modules.append({'name':name,'cells':coords})
    # Timber wall, rope-bound corner columns and sea-facing window. Top rows block movement.
    for y in range(2):
        for x in range(w):put(x,y,walls[y][x%3],0,True)
    for y in range(2,h):
        for x in (0,w-1):put(x,y,walls[1][x%3],3,True)
    for x in range(2,w-3,5):
        for dy in range(2):
            for dx in range(3):put(x+dx,dy,windows[dy][dx],0,True)
    if kind=='house':
        cx=w//2
        # House5 is the longhouse: broad central hearth, tables to either side.
        if number==5:
            stamp('hearth',cx-2,4)
            stamp('table',2,5)
            stamp('table',w-5,5)
            stamp('rug',cx-2,9,False)
            stamp('shelf',2,2);stamp('chart',w-4,2)
            stamp('lantern',2,9);stamp('lantern',w-3,9)
        else:
            types={1:[('table',2,3),('bed',w-4,2),('rug',4,7)],
                   2:[('chart',2,2),('shelf',w-4,3),('rug',4,7)],
                   3:[('shelf',2,2),('table',w-5,3),('bed',2,6)],
                   4:[('bed',2,3),('table',w-5,3),('plant',w-3,7)]}[number]
            for name,x,y in types:stamp(name,x,y,name not in ('rug',))
            stamp('lantern',w-2,2)
        exits=[(cx-1,h-1),(cx,h-1)]
        # A threshold keeps the two original warp indices and their action behavior.
        for x,y in exits:put(x,y,t.meta(t.quarters(floor.crop((0,0,16,16)),fslot),attr=0x1065,label='house threshold'),0,False)
    elif kind=='center1':
        stamp('healer',5,0)
        stamp('shelf',11,2);stamp('plant',11,6)
        stamp('pc',11,4)
        x,y=11,5;mid=grid[y*w+x]&1023;content=t.entries[(mid-512)*8:(mid-512)*8+8]
        put(x,y,t.meta(content[:4],content[4:],0x1083,'functional PC'),3,True)
        stamp('rug',5,5,False)
        for sy,ids in ((5,(0x280,0x281)),(6,(0x288,0x289)),(7,(0x290,0x291))):
            for sx,mid in enumerate(ids):put(sx,sy,mid,4 if (sx,sy)==(1,6) else 3,sx==0 and sy==6)
        exits=[(7,8),(6,8)]
        for x,y in exits:put(x,y,t.meta(t.quarters(floor.crop((0,0,16,16)),fslot),attr=0x1065,label='center threshold'),3,False)
    else:
        for sy,ids in ((5,(0x298,0x299)),(6,(0x2a0,0x2a1)),(7,(0x2a8,0x2a9))):
            for sx,mid in enumerate(ids):put(sx,sy,mid,4 if (sx,sy)==(1,6) else 3,sx==0 and sy==6)
        stamp('link',4,4);stamp('link',8,4)
        stamp('rug',5,7,False)
        exits=[(1,6),(5,1),(9,1)]
        for x in (5,9):
            put(x,2,0x21e,3,True);put(x,3,0x25d,3,True)
        for x,y in ((5,1),(9,1)):
            put(x,y,0x264,3,False)
            occupied.discard((x,y))
    return grid,sorted(occupied),modules,exits

NAMES=('VerdanturfTown_House','VerdanturfTown_FriendshipRatersHouse','VerdanturfTown_WandasHouse',
       'VerdanturfTown_Mart','VerdanturfTown_PokemonCenter_1F','VerdanturfTown_PokemonCenter_2F',
       'VerdanturfTown_BattleTentLobby','VerdanturfTown_BattleTentCorridor','VerdanturfTown_BattleTentBattleRoom')
MARK='VALE_INTERIORS_V1'
def layout_id(name):return 'LAYOUT_ARAUNA_VALE_INTERIORS_'+name.removeprefix('VerdanturfTown_').upper()
def domestic(t,name):
    large=name.endswith('WandasHouse');shop=name.endswith('Mart')
    w,h=(18,12) if large else ((14,11) if shop else (12,11))
    floor,slot=t.art['floor'];q=t.quarters(floor.crop((0,0,16,16)),slot)
    base=[t.meta(t.quarters(floor.crop((x,y,x+16,y+16)),slot),label='warm timber') for y in (0,16) for x in (0,16)]
    walls=t.stamp('wall',q);window=t.stamp('window',q)
    grid=[0x3000|base[(y%2)*2+x%2] for y in range(h) for x in range(w)]
    modules=[]
    def put(x,y,mid,blocked=False,z=3):
        assert 0<=x<w and 0<=y<h
        grid[y*w+x]=mid|(0x400 if blocked else 0)|(z<<12)
    def stamp(art,x,y,blocked=True):
        shape=t.stamp(art,q,blocking=blocked)
        for dy,row in enumerate(shape):
            for dx,mid in enumerate(row):put(x+dx,y+dy,mid,blocked)
        modules.append({'name':art,'at':[x,y]})
    for y in range(2):
        for x in range(w):put(x,y,walls[y][x%3],True,0)
    for y in range(2,h):
        for x in (0,w-1):put(x,y,walls[1][x%3],True)
    for x in ((3,11) if large else (4,)):
        for dy in range(2):
            for dx in range(3):put(x+dx,dy,window[dy][dx],True,0)
    if large:
        stamp('shelf',1,2);stamp('chart',9,2);stamp('bed',14,2)
        stamp('table',5,4);stamp('rug',11,7,False);stamp('plant',1,8)
        npc=((14,6),(4,5),(8,3),(3,7),(8,6))
    elif shop:
        stamp('shelf',9,2);stamp('shelf',11,2);stamp('chart',5,2)
        stamp('plant',10,7)
        # A single-row counter allows the engine's MB_COUNTER interaction.
        image,palette=t.art['table']
        for dx in range(3):
            mid=t.meta(q,t.quarters(image.crop((dx*16,0,dx*16+16,16)),palette),0x1080,'shop counter')
            put(2+dx,4,mid,True)
        npc=((3,3),(7,6),(9,6),(5,7))
    elif name.endswith('FriendshipRatersHouse'):
        stamp('shelf',1,2);stamp('plant',8,2);stamp('rug',4,6,False)
        stamp('table',7,5)
        npc=((4,4),(5,4))
    else:
        stamp('bed',8,2);stamp('table',1,3);stamp('shelf',6,2)
        stamp('rug',5,7,False);stamp('plant',9,7)
        npc=((5,5),(5,4))
    exits=((w//2-1,h-1),(w//2,h-1))
    for x,y in exits:put(x,y,t.meta(q,attr=0x1065,label='south threshold'),False,0)
    return grid,w,h,npc,exits,modules

TENT_BANK=ROOT/'data/tilesets/secondary/arauna_vale_pavilhao'
TENT_SYMBOL='AraunaValePavilhao'
class TentArt:
    def __init__(self,t):
        original=ROOT/'data/tilesets/secondary/battle_tent'
        clone=Image.open(original/'tiles.png')
        self.image=Image.new('P',(128,256));self.image.putpalette(clone.getpalette());self.image.paste(clone,(0,0))
        self.used=256;self.cache={};self.metacache={}
        self.entries=words(original/'metatiles.bin');self.attrs=words(original/'metatile_attributes.bin')
        self.primary_attrs=words(ROOT/'data/tilesets/primary/general/metatile_attributes.bin')
        self.art=t.art;self.palettes=t.palettes
        TENT_BANK.mkdir(exist_ok=True);shutil.copytree(original/'palettes',TENT_BANK/'palettes',dirs_exist_ok=True)
        self.blank=self.tile(Image.new('L',(8,8)))
    def tile(self,image):
        key=image.tobytes()
        if key not in self.cache:
            assert self.used<480
            self.cache[key]=512+self.used
            self.image.paste(image,(self.used%16*8,self.used//16*8));self.used+=1
        return self.cache[key]
    def q(self,image,slot):
        return [self.tile(image.crop((x,y,x+8,y+8)))|(slot<<12) for x,y in ((0,0),(8,0),(0,8),(8,8))]
    def block(self,original,lower,upper=None):
        attr=self.attrs[original-512] if original>=512 else self.primary_attrs[original]
        entries=tuple(lower)+tuple(upper or [self.blank]*4)
        key=(entries,attr)
        if key not in self.metacache:
            mid=512+len(self.attrs);assert mid<1024
            self.metacache[key]=mid;self.entries.extend(entries);self.attrs.append(attr)
        return self.metacache[key]
    def artblock(self,name,x,y):
        image,slot=self.art[name];return self.q(image.crop((x,y,x+16,y+16)),slot)
    def save(self):
        self.image.save(TENT_BANK/'tiles.png',bits=4)
        (TENT_BANK/'metatiles.bin').write_bytes(packed(self.entries))
        (TENT_BANK/'metatile_attributes.bin').write_bytes(packed(self.attrs))
        for slot,palette in self.palettes.items():
            # Door animation uses original palette 9, which remains unchanged.
            if slot==9:continue
            (TENT_BANK/f'palettes/{slot:02}.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in palette)+'\n')

def tent_room(tent,name,template):
    w,h=template['width'],template['height'];old=words(ROOT/template['blockdata_filepath']);grid=[]
    lobby=name.endswith('Lobby');corridor=name.endswith('Corridor')
    for i,raw in enumerate(old):
        x,y=i%w,i//w;original=raw&1023
        # Original doorway/frame IDs stay available to opendoor/closedoor.
        if original in (610,611,612,618,619,620) or original==1 and (lobby or corridor):
            grid.append(raw);continue
        floor=tent.artblock('floor',(x%2)*16,(y%2)*16)
        if original in (517,525) or (lobby and (y<2 or x in (0,12) and raw&0x400)):
            graphic=tent.artblock('wall',(x%3)*16,min(y,1)*16)
            mid=tent.block(original,floor,graphic)
        elif lobby and raw&0x400 and 2<=x<=10 and 2<=y<=5:
            pane=Image.new('L',(16,16))
            pane.putdata([1 if py in (0,1) else (7 if py==15 or px in (0,15) else 3)
                          for py in range(16) for px in range(16)])
            graphic=tent.q(pane,6)
            if (x,y)==(4,5):
                image,palette=tent.art['chart']
                graphic=tent.q(image.resize((16,16),Image.Resampling.NEAREST),palette)
            mid=tent.block(original,floor,graphic)
        elif not lobby and not corridor and 688<=original<=725:
            # A quiet woven arena instead of the yellow court/Poké Ball graphic.
            native=Image.new('L',(16,16))
            native.putdata([3 if (px+py)%5==0 else 2 for py in range(16) for px in range(16)])
            tent.palettes[8]=[(255,0,255),(123,139,98),(82,106,74),(65,82,57)]+[(49,65,49)]*12
            mid=tent.block(original,tent.q(native,8))
        else:mid=tent.block(original,floor)
        grid.append((raw&~1023)|mid)
    return grid,w,h

def main():
    import subprocess,re
    node=json.loads(LAYOUTS.read_text());t=Tiles();tent=TentArt(t);report={}
    for name in NAMES:
        p=ROOT/'data/maps'/name/'map.json'
        original=json.loads(subprocess.check_output(['git','show','HEAD:data/maps/'+name+'/map.json'],cwd=ROOT))
        event=json.loads(json.dumps(original));template=next(r for r in node['layouts'] if r['id']==original['layout'])
        if 'BattleTent' in name:
            grid,w,h=tent_room(tent,name,template);modules=[]
        elif 'PokemonCenter' in name:
            kind='center1' if name.endswith('1F') else 'center2';w,h=(14,9) if kind=='center1' else (14,10)
            grid,_,modules,exits=build_room(t,w,h,kind)
            if kind=='center1':
                event['object_events'][0].update(x=7,y=3,elevation=3)
                event['object_events'][2].update(x=10,y=4,elevation=3)
                event['object_events'][3].update(x=9,y=7,elevation=3)
        else:
            grid,w,h,npc,exits,modules=domestic(t,name)
            for e,(x,y) in zip(event['object_events'],npc):e.update(x=x,y=y,elevation=3)
            for e,(x,y) in zip(event['warp_events'],exits):e.update(x=x,y=y,elevation=0)
        identity=layout_id(name);dest=ROOT/'data/layouts'/(name+'_Arauna');dest.mkdir(exist_ok=True)
        (dest/'map.bin').write_bytes(packed(grid));(dest/'border.bin').write_bytes((ROOT/template['border_filepath']).read_bytes())
        record=dict(template,id=identity,name=name+'_Arauna_Layout',width=w,height=h,secondary_tileset='gTileset_'+(TENT_SYMBOL if 'BattleTent' in name else SYMBOL),
                    blockdata_filepath=str((dest/'map.bin').relative_to(ROOT)),border_filepath=str((dest/'border.bin').relative_to(ROOT)))
        found=next((r for r in node['layouts'] if r['id']==identity),None)
        if found:found.update(record)
        else:node['layouts'].append(record)
        event['layout']=identity;write_json(p,event)
        report[name]={'size':[w,h],'modules':modules,'warps':len(event['warp_events']),'objects':len(event['object_events'])}
    write_json(LAYOUTS,node);count=t.save();tent.save()
    bodies={
      'graphics.h':f'const u32 gTilesetTiles_{SYMBOL}[] = INCGFX_U32("data/tilesets/secondary/arauna_vale_interiors_v1/tiles.png", ".4bpp.lz");\n'
        +f'const u16 gTilesetPalettes_{SYMBOL}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("data/tilesets/secondary/arauna_vale_interiors_v1/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
      'metatiles.h':f'const u16 gMetatiles_{SYMBOL}[] = INCBIN_U16("data/tilesets/secondary/arauna_vale_interiors_v1/metatiles.bin");\n'
        +f'const u16 gMetatileAttributes_{SYMBOL}[] = INCBIN_U16("data/tilesets/secondary/arauna_vale_interiors_v1/metatile_attributes.bin");\n',
      'headers.h':f'const struct Tileset gTileset_{SYMBOL} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n'
        +f'    .tiles = gTilesetTiles_{SYMBOL},\n    .palettes = gTilesetPalettes_{SYMBOL},\n'
        +f'    .metatiles = gMetatiles_{SYMBOL},\n    .metatileAttributes = gMetatileAttributes_{SYMBOL},\n    .callback = NULL,\n}};\n'}
    for filename,body in list(bodies.items()):
        extra=body.replace(SYMBOL,TENT_SYMBOL).replace('arauna_vale_interiors_v1','arauna_vale_pavilhao')
        bodies[filename]=body+'\n'+extra
    for filename,body in bodies.items():
        p=ROOT/'src/data/tilesets'/filename
        clean=re.sub(r'\n*// '+MARK+r'_BEGIN\n.*?// '+MARK+r'_END\n','',p.read_text(),flags=re.S)
        p.write_text(clean.rstrip()+'\n\n// '+MARK+'_BEGIN\n'+body+'// '+MARK+'_END\n')
    write_json(OUT/'geometry.json',{'maps':report,'tiles':t.used,'metatiles':count,'used_metatiles':len(t.ids)})
    print(json.dumps({'maps':len(NAMES),'tiles':t.used,'metatiles':count}))

if __name__=='__main__':main()

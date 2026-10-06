#!/usr/bin/env python3
"""Compile Atlantic forest landmarks into a dedicated native secondary bank.

Preserves the original collision, elevations, events and encounter behaviors.
Large landmarks occupy existing blocked vegetation; exposed roots are walkable.
"""
import json
import shutil
import struct
from pathlib import Path
import numpy as np
from scipy.ndimage import label, find_objects
from PIL import Image
from bancos_nativos import resolve_bank
from render_native_map import Renderer, words, palette

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'graphics/arauna/maps/mata_espera_v1/source.png'
TARGET=ROOT/'data/tilesets/secondary/arauna_mata_espera_v1'
LAYOUT='LAYOUT_ARAUNA_MATA_ESPERA_V1'

def dump(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def write_palette(path,colors):
    path.write_bytes(('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%c for c in colors)).encode())

def components():
    src=np.array(Image.open(ART).convert('RGBA'))
    labels,count=label(src[:,:,3]>127)
    regions=find_objects(labels)
    selected=[]
    for i,region in enumerate(regions,1):
        if region is not None:
            area=int((labels[region]==i).sum())
            if area>10000: selected.append((i,region))
    assert len(selected)==4
    # Stable spatial names rather than the amount of transparent padding.
    named={}
    for i,region in selected:
        x,y=region[1].start,region[0].start
        name='tree' if y<100 else 'log' if y<800 else 'fern' if x<600 else 'root'
        pixels=src[region].copy();pixels[:,:,3]=np.where(labels[region]==i,255,0)
        named[name]=Image.fromarray(pixels)
    sizes={'tree':(80,96),'log':(64,32),'fern':(32,32),'root':(48,16)}
    return {name:im.resize(sizes[name],Image.Resampling.NEAREST) for name,im in named.items()}

def main():
    node=json.loads((ROOT/'data/layouts/layouts.json').read_text())
    old=next(l for l in node['layouts'] if l['id']=='LAYOUT_PETALBURG_WOODS')
    grid=words(ROOT/old['blockdata_filepath']);w,h=old['width'],old['height']
    event_path=ROOT/'data/maps/PetalburgWoods/map.json';event=json.loads(event_path.read_text())
    # The source geometry remains the immutable baseline for repeatable builds.
    active={c&1023 for c in grid+words(ROOT/old['border_filepath']) if c&1023>=512}
    src=resolve_bank(ROOT,old['secondary_tileset'])
    TARGET.mkdir(parents=True,exist_ok=True);(TARGET/'palettes').mkdir(exist_ok=True)
    for i in range(16):shutil.copyfile(src/'palettes'/f'{i:02}.pal',TARGET/'palettes'/f'{i:02}.pal')
    original_meta=words(src/'metatiles.bin');original_attrs=words(src/'metatile_attributes.bin')
    # Unused city definitions do not belong in this dedicated forest bank.
    meta=[0]*len(original_meta);attrs=[0]*len(original_attrs)
    for mid in active:
        meta[(mid-512)*8:(mid-511)*8]=original_meta[(mid-512)*8:(mid-511)*8]
        attrs[mid-512]=original_attrs[mid-512]
    sheet=Image.new('P',(128,256),0)
    grays=[255,238,222,205,189,172,156,139,115,98,82,65,49,32,16,0]
    sheet.putpalette([c for v in grays for c in (v,v,v)]+[0]*(768-48))
    original_sheet=Image.open(src/'tiles.png')
    used={v&1023 for v in meta if v&1023>=512}
    for tid in used:
        local=tid-512;x,y=local%16*8,local//16*8
        sheet.paste(original_sheet.crop((x,y,x+8,y+8)),(x,y))
    free=iter(i for i in range(512,1008) if i not in used)
    tiles={};art=components()
    all_colors=[]
    for image in art.values():
        data=np.array(image);all_colors.extend(map(tuple,data[:,:,:3][data[:,:,3]>127]))
    sample=Image.new('RGB',(len(all_colors),1));sample.putdata(all_colors)
    quant=sample.quantize(colors=15,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    colors=[(0,0,0)]+[tuple((c>>3)<<3 for c in quant.getpalette()[i*3:i*3+3]) for i in range(15)]
    write_palette(TARGET/'palettes/10.pal',colors)
    def indexed(image):
        data=np.array(image);out=Image.new('P',image.size,0);values=[]
        for rgba in data.reshape(-1,4):
            values.append(0 if rgba[3]<128 else min(range(1,16),key=lambda k:sum((int(rgba[j])-colors[k][j])**2 for j in range(3))))
        out.putdata(values);return out
    def tile_id(tile):
        key=tile.tobytes()
        if key not in tiles:
            tid=next(free);tiles[key]=tid
            sheet.paste(tile,((tid-512)%16*8,(tid-512)//16*8))
        return tiles[key]
    primary=resolve_bank(ROOT,'gTileset_AraunaMataEspera')
    pm=words(primary/'metatiles.bin');pa=words(primary/'metatile_attributes.bin')
    base=pm[8:12] # Ground beneath every transparent sprite: never VRAM black.
    def append(entries,attr=0):
        mid=512+len(attrs);assert mid<1024
        meta.extend(entries);attrs.append(attr);return mid
    # A damp, brown-green humus palette reuses the original ground texture.
    humus=palette(primary/'palettes/02.pal')
    for i,c in enumerate(humus):
        if i:humus[i]=tuple((v>>3)<<3 for v in (int(c[0]*.72+14),int(c[1]*.48+22),int(c[2]*.36+16)))
    humus[13]=(112,112,80);humus[14]=(104,104,72);humus[15]=(96,104,72)
    original_ground_palette=palette(primary/'palettes/02.pal')
    humus[1:4]=original_ground_palette[13:16]
    write_palette(TARGET/'palettes/09.pal',humus)
    soil=append([(e&0x0fff)|(9<<12) for e in base]+[0]*4,pa[1])
    # Exposed roots keep the source behavior and can be stepped over.
    ids={}
    for name,image in art.items():
        image=indexed(image);cols,rows=image.width//16,image.height//16;result=[]
        for yy in range(rows):
            for xx in range(cols):
                top=[tile_id(image.crop((xx*16+dx,yy*16+dy,xx*16+dx+8,yy*16+dy+8)))|(10<<12)
                     for dx,dy in ((0,0),(8,0),(0,8),(8,8))]
                result.append(append(base+top))
        ids[name]=(cols,rows,result)
    new=list(grid)
    protected={(e['x'],e['y']) for key in ('object_events','warp_events','coord_events','bg_events') for e in event[key]}
    # Curved forest trails follow the existing terrain and lead into the story
    # clearing; encounter grass, ledges and the Cut gates are left intact.
    route=[(16,38),(16,35),(13,33),(10,31),(10,27),(12,25),(18,25),
           (23,25),(26,24),(27,22),(27,20),(27,17),(25,16),(20,16),
           (14,16),(9,16),(7,14),(7,11),(8,9),(12,8),(13,6),(14,5)]
    def distance(px,py,a,b):
        dx,dy=b[0]-a[0],b[1]-a[1]
        t=max(0,min(1,((px-a[0])*dx+(py-a[1])*dy)/(dx*dx+dy*dy)))
        return ((px-a[0]-t*dx)**2+(py-a[1]-t*dy)**2)**.5
    primary_renderer=Renderer(primary,src)
    terrain={}
    for i,c in enumerate(grid):
        point=(i%w,i//w);mid=c&1023
        # Cut switches on fixed metatile IDs, not only grass behaviors. Keep
        # every encounter-grass ID intact instead of aliasing it for artwork.
        if mid!=1 or point in protected or min(distance(*point,a,b) for a,b in zip(route,route[1:]))>=1.5:continue
        # Clip the soil at pixel scale, giving the trail soft irregular edges
        # instead of a staircase of entire brown metatiles.
        tile=Image.new('P',(16,16),0);pixels=[]
        ground_entries=pm[mid*8:mid*8+4]
        for py in range(16):
            for px in range(16):
                entry=ground_entries[(py//8)*2+px//8]
                source=primary_renderer._tile(entry&1023)
                sx,sy=px%8,py%8
                if entry&0x400:sx=7-sx
                if entry&0x800:sy=7-sy
                original_index=source.getpixel((sx,sy))
                d=min(distance(point[0]+(px-7.5)/16,point[1]+(py-7.5)/16,a,b) for a,b in zip(route,route[1:]))
                radius=.7+.13*((px+7*py)%13/13-.5)
                pixels.append(original_index if d<radius else {13:1,14:2,15:3}.get(original_index,1))
        tile.putdata(pixels)
        bottom=[tile_id(tile.crop((dx,dy,dx+8,dy+8)))|(9<<12) for dx,dy in ((0,0),(8,0),(0,8),(8,8))]
        top=pm[mid*8+4:(mid+1)*8]
        key=tuple(bottom+top+[pa[mid]])
        if key not in terrain:terrain[key]=append(bottom+top,pa[mid])
        new[i]=(c&0xfc00)|terrain[key]
    placements={'tree':[(2,0),(31,12)],'log':[(21,12),(37,20)],
                'fern':[(1,16),(21,14),(43,10),(43,24)],'root':[(11,24),(15,9),(29,22),(35,34)]}
    placed=[]
    for name,locations in placements.items():
        cols,rows,mids=ids[name]
        for x,y in locations:
            points=[(x+xx,y+yy) for yy in range(rows) for xx in range(cols)]
            if any(p in protected or not (0<=p[0]<w and 0<=p[1]<h) for p in points):continue
            expected=0 if name=='root' else 1
            if any(((grid[py*w+px]>>10)&3)!=expected or (name=='root' and grid[py*w+px]&1023!=1) for px,py in points):continue
            for k,(px,py) in enumerate(points):
                mid=mids[k]
                if name=='root' and new[py*w+px]&1023>=512:
                    beneath=(new[py*w+px]&1023)-512
                    mid=append(meta[beneath*8:beneath*8+4]+meta[(mid-512)*8+4:(mid-511)*8])
                new[py*w+px]=(grid[py*w+px]&0xfc00)|mid
            placed.append({'asset':name,'x':x,'y':y,'size':[cols,rows]})
    assert sum(p['asset']=='tree' for p in placed)==2 and sum(p['asset']=='root' for p in placed)>=2
    sheet.save(TARGET/'tiles.png')
    (TARGET/'metatiles.bin').write_bytes(struct.pack('<%dH'%len(meta),*meta))
    (TARGET/'metatile_attributes.bin').write_bytes(struct.pack('<%dH'%len(attrs),*attrs))
    folder=ROOT/'data/layouts/PetalburgWoods_AraunaV1';folder.mkdir(exist_ok=True)
    (folder/'map.bin').write_bytes(struct.pack('<%dH'%len(new),*new));shutil.copyfile(ROOT/old['border_filepath'],folder/'border.bin')
    record={**old,'id':LAYOUT,'name':'PetalburgWoods_AraunaV1_Layout','primary_tileset':'gTileset_AraunaMataEspera',
            'secondary_tileset':'gTileset_AraunaMataEsperaV1','blockdata_filepath':str((folder/'map.bin').relative_to(ROOT)),
            'border_filepath':str((folder/'border.bin').relative_to(ROOT))}
    existing=next((l for l in node['layouts'] if l['id']==LAYOUT),None)
    if existing:existing.update(record)
    else:node['layouts'].append(record)
    event['layout']=LAYOUT;dump(event_path,event);dump(ROOT/'data/layouts/layouts.json',node)
    slug='data/tilesets/secondary/arauna_mata_espera_v1';symbol='AraunaMataEsperaV1'
    declarations={
        'graphics.h':f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{slug}/tiles.png", ".4bpp.lz");\nconst u16 gTilesetPalettes_{symbol}[][16] =\n{{\n'+''.join(f'    INCGFX_U16("{slug}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
        'metatiles.h':f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{slug}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{slug}/metatile_attributes.bin");\n',
        'headers.h':f'const struct Tileset gTileset_{symbol} =\n{{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_{symbol},\n    .palettes = gTilesetPalettes_{symbol},\n    .metatiles = gMetatiles_{symbol},\n    .metatileAttributes = gMetatileAttributes_{symbol},\n    .callback = NULL,\n}};\n'}
    for name,text in declarations.items():
        path=ROOT/'src/data/tilesets'/name
        if symbol not in path.read_text():path.write_text(path.read_text()+'\n'+text)
    report={'layout':LAYOUT,'dimensions':[w,h],'new_static_tiles':len(tiles),'secondary_metatiles':len(attrs),
            'placements':placed,'changed_visual_cells':sum(a!=b for a,b in zip(grid,new)),
            'events_unchanged_except_layout':True,'collision_and_elevation_unchanged':all(a&0xfc00==b&0xfc00 for a,b in zip(grid,new))}
    (ROOT/'review').mkdir(exist_ok=True);dump(ROOT/'review/mata_espera_v1_build.json',report);print(json.dumps(report,indent=2))

if __name__=='__main__':main()

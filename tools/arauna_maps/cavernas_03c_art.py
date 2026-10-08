"""Native metatile engineering from the installed mineral atlas and glyph masks."""
from PIL import Image,ImageDraw
from build_cavernas_03a import pieces

DOOR_IDS=(553,554,555,556,562,563,564,565,566,567,519)

def safe_pair(pair):
    pair.dynamic.update(range(928,932));pair.free=[i for i in pair.free if i>=512 and i not in pair.dynamic]
    pair.tile_cache={raw:i for i,raw in pair.tiles.items() if i>=512 and i not in pair.dynamic and i not in pair.free}
    assert pair.reader._tile(0).tobytes()==bytes(64);pair.tile_cache[bytes(64)]=0

def opaque(im,fill=3):
    out=im.copy();out.putdata([v if v else fill for v in im.getdata()]);return out

def glyph_mask(reader,mid):
    # Preserve the luminous strokes of the actual installed inscription. The
    # dialogue's Braille text/font remain untouched in the functional contract.
    im=reader.metatile(mid).convert('RGB');mask=Image.new('L',(16,16))
    bright={(205,172,123):15,(200,168,120):15}
    mask.putdata([bright.get(rgb,0) if 0<=i%16<16 and 0<=i//16<14 else 0 for i,rgb in enumerate(im.getdata())])
    assert sum(v!=0 for v in mask.getdata())>0,('Missing inscription strokes',mid)
    return mask

def inscription(pair,art,mid):
    slab=opaque(art['lower']);d=ImageDraw.Draw(slab)
    d.rectangle((0,0,15,13),fill=3);d.line((0,0,15,0),fill=7);d.line((0,13,15,13),fill=1)
    mask=glyph_mask(pair.reader,mid)
    return pair.entries(slab,7)+pair.entries(mask,7),mask

def stairs(pair,art):
    floor=art['floor0'];top=Image.new('L',(16,16),0);d=ImageDraw.Draw(top)
    for y,w in ((5,6),(8,8),(11,10)):
        x=(16-w)//2;d.rectangle((x,y,x+w-1,y+1),fill=3);d.line((x,y,x+w-1,y),fill=8)
    return pair.entries(floor,9)+pair.entries(top,11)

def ladder(pair,art):
    top=Image.new('L',(16,16),0);d=ImageDraw.Draw(top)
    d.rectangle((3,0,4,15),fill=8);d.rectangle((11,0,12,15),fill=8)
    for y in (2,6,10,14):d.line((4,y,11,y),fill=14);d.line((4,y+1,11,y+1),fill=4)
    return pair.entries(art['floor0'],9)+pair.entries(top,11)

def install_landmarks(pair,family,exit_ids,puzzle=False):
    art=pieces(family);report={'changed_native_ids':[], 'glyph_masks':{}}
    def put(mid,entries):
        pair.meta[1][(mid-512)*8:(mid-512)*8+8]=entries;report['changed_native_ids'].append(mid)
    if puzzle:
        # The six native door pieces form one continuous 48x32 arch. No alias
        # is introduced, so every script-written ID retains its own artwork.
        wall=Image.new('L',(48,32),3)
        for y in (0,16):
            for x in (0,16,32):wall.paste(opaque(art['single']),(x,y))
        d=ImageDraw.Draw(wall);d.rectangle((15,12,32,31),fill=1);d.polygon([(15,12),(20,7),(27,7),(32,12)],fill=1)
        d.line((13,13,18,6,29,6,34,13),fill=8,width=2)
        d.line((13,14,13,30),fill=6,width=2);d.line((34,14,34,30),fill=6,width=2)
        # Dark passage is opaque index 1, not transparent index 0.
        for row,ids in enumerate(((554,555,556),(562,563,564))):
            for col,mid in enumerate(ids):put(mid,pair.entries(wall.crop((col*16,row*16,col*16+16,row*16+16)),7)+[0]*4)
        put(553,pair.entries(opaque(art['single']),7)+[0]*4)
        for mid in (565,567):
            entries,mask=inscription(pair,art,mid);put(mid,entries);report['glyph_masks'][str(mid)]=list(mask.getdata())
        cracked=opaque(art['single']);dd=ImageDraw.Draw(cracked);dd.line((9,0,7,5,9,9),fill=1);put(566,pair.entries(cracked,7)+[0]*4)
        put(519,stairs(pair,art))
    # Original outward-opening exit row, three blocks wide below the warp.
    # Keep the integrator's nine passthrough cells exactly as installed.
    exit_im=Image.new('L',(48,16),0)
    for x in (0,16,32):exit_im.paste(art['single'],(x,0))
    d=ImageDraw.Draw(exit_im);d.ellipse((11,-6,36,10),fill=1);d.line((15,5,32,5),fill=15,width=2)
    d.line((13,8,34,8),fill=8);d.line((11,9,36,9),fill=6)
    for x in range(48):
        for y in range(11,16):exit_im.putpixel((x,y),0)
    for col,mid in enumerate(exit_ids):
        put(mid,pair.entries(art['floor0'],9)+pair.entries(exit_im.crop((col*16,0,col*16+16,16)),7))
    if not puzzle:
        put(572,stairs(pair,art))
        for mid in (535,575):put(mid,ladder(pair,art))
    report['changed_native_ids']=sorted(set(report['changed_native_ids']))
    return report

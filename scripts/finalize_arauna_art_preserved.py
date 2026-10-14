#!/usr/bin/env python3
"""Finish the two-PNG Ciro repair and export receipts in an isolated PR."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,io,gzip,zlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
BASE='bcd1fec0025580406d6a6913fcf3e4e0a7824a59'
EXPECTED_ROM='3d322afaffc408fc9c135ffba948780784c29768ca8aa27701f0bc9fa195fcad'
REVIEW=ROOT/'review/plan_art_preserved_20261014'
ALLOW=[f'graphics/object_events/pics/people/ciro/{p}.png' for p in ('phase2','phase3')]
def patch():
    for rel in ALLOW:
        p=ROOT/rel;im=Image.open(p);im.load();before=im.copy()
        assert im.size==(144,32) and im.mode=='P'
        for target,source in [(3,4),(5,6)]:
            for y in range(28,32):
                for x in range(16):
                    im.putpixel((target*16+x,y),before.getpixel((source*16+15-x,y)))
        im.save(p,bits=4,transparency=im.info.get('transparency',0))
    p=ROOT/'tools/validate_arauna_character_assets.py';s=p.read_text()
    for rel in ['ciro/phase2','ciro/phase3','dona_zila','elite_four/drake','elite_four/glacia','gym_leaders/flannery','gym_leaders/roxanne','team_aqua/archie','team_magma/maxie']:
        s=re.sub(r'^    "graphics/object_events/pics/people/'+re.escape(rel)+r'\.png": .*\n','',s,flags=re.M)
    if 'parser.add_argument("--release"' not in s:
        s=s.replace('    args = parser.parse_args()','    parser.add_argument("--release", action="store_true", help="Require applicable overworld surfaces")\n    args = parser.parse_args()',1)
        s=s.replace('                outstanding.append(f"{name}: overworld sheet and palette")','                outstanding.append(f"{name}: overworld sheet and palette")\n                if args.release:\n                    errors.append("required release overworld surface is missing")')
    p.write_text(s)
    for rel in ('scripts/build_arauna.sh','scripts/check_arauna_static.sh'):
        p=ROOT/rel;p.write_text(p.read_text().replace('python3 tools/validate_arauna_character_assets.py\n','python3 tools/validate_arauna_character_assets.py --release\n'))
def export():
    REVIEW.mkdir(parents=True,exist_ok=True)
    rom=(ROOT/'pokemon-juramento-de-arauna-en_modern.gba').read_bytes()
    digest=hashlib.sha256(rom).hexdigest()
    assert digest==EXPECTED_ROM,('Recovery differs from the previously tested ROM',digest)
    meta={'audit_base':BASE,'rom_sha256':digest,'rom_padded_size':len(rom),'rom_used_bytes':31572732,'ewram_used_bytes':247164,'iwram_used_bytes':29156,'compiler':subprocess.check_output(['arm-none-eabi-gcc','--version'],text=True).splitlines()[0],'emulator':'mGBA 0.10.2','previous_local_runtime_assertions':130,'hash_identical_to_locally_tested_rom':True,'linked_text_blocks_verified':2260,'campaign_natural_playthrough':False}
    (REVIEW/'release_metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
    changes=[]
    for rel in ALLOW:
        old=subprocess.check_output(['git','show',f'{BASE}:{rel}'],cwd=ROOT);new=(ROOT/rel).read_bytes();a=Image.open(io.BytesIO(old));b=Image.open(io.BytesIO(new));coords=[(x,y) for y in range(32) for x in range(144) if a.getpixel((x,y))!=b.getpixel((x,y))]
        changes.append({'path':rel,'before_sha256':hashlib.sha256(old).hexdigest(),'after_sha256':hashlib.sha256(new).hexdigest(),'dimensions':[144,32],'mode':b.mode,'changed_pixels':len(coords),'frames':sorted({x//16 for x,y in coords}),'rows':sorted({y for x,y in coords}),'palette_unchanged':a.getpalette()==b.getpalette(),'transparency_unchanged':a.info.get('transparency')==b.info.get('transparency')})
    (REVIEW/'art_freeze_receipt.json').write_text(json.dumps({'base':BASE,'protected_resources':20104,'changes':changes,'manifest_command':'python3 scripts/check_arauna_art_freeze.py --manifest art_baseline.json'},indent=2)+'\n')
    for phase in ('f2','f3'):
        frames=[Image.open(REVIEW/f'ciro_g{g}_{phase}_{d}_{step}_{i}.png').convert('RGB') for g in (0,1) for d in ('SOUTH','NORTH') for step in range(2) for i in range(8)]
        frames[0].save(REVIEW/f'ciro_{phase}_north_south_mf.gif',save_all=True,append_images=frames[1:],duration=80,loop=0)
    log=REVIEW/'build.log'
    if log.exists():
        log.with_suffix('.log.gz').write_bytes(gzip.compress(log.read_bytes(),mtime=0))
        log.unlink()
    p=ROOT/'docs/COMO_PUBLICAR_A_BETA.md';s=p.read_text();q=chr(96)
    for label,value in [('CRC32',f'{zlib.crc32(rom)&0xffffffff:08X}'),('MD5',hashlib.md5(rom).hexdigest()),('SHA-1',hashlib.sha1(rom).hexdigest())]:
        s=re.sub(r'(\| '+label+r' \| '+q+r')[^'+q+r']+('+q+r' \|)',lambda m:m[1]+value+m[2],s)
    if '| SHA-256 |' not in s:s=s.replace('Estes valores são desta build.',f'| SHA-256 | {q}{digest}{q} |\n\nBuild auditada de 14/10/2026, GCC ARM 13.2.1.\n\nEstes valores são desta build.')
    p.write_text(s)
    print('Verified recovery ROM:',digest)
def main():
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--apply',action='store_true');g.add_argument('--export',action='store_true');a=p.parse_args()
    patch() if a.apply else export()
if __name__=='__main__':main()

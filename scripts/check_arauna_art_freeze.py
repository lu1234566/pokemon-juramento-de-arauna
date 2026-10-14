#!/usr/bin/env python3
"""Freeze all compiled art/audio/map resources; allow only Ciro frames 3/5."""
from pathlib import Path
import argparse,subprocess,hashlib,io,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE='bcd1fec0025580406d6a6913fcf3e4e0a7824a59'
ALLOW={'graphics/object_events/pics/people/ciro/phase2.png','graphics/object_events/pics/people/ciro/phase3.png'}
def protected(p):return p.startswith(('graphics/','data/tilesets/','data/layouts/','sound/','src/data/tilesets/','src/data/object_events/')) or p=='data/scripts/rival_graphics.inc' or (p.startswith('data/maps/') and not p.endswith('/scripts.inc'))
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--base',default=BASE);a.add_argument('--manifest',type=Path);args=a.parse_args()
 names=subprocess.check_output(['git','ls-tree','-r','--name-only',args.base],cwd=ROOT).decode().splitlines();tracked=set(subprocess.check_output(['git','ls-files'],cwd=ROOT).decode().splitlines());errors=[];records={}
 proc=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for p in filter(protected,names):
  proc.stdin.write(f'{args.base}:{p}\n'.encode());proc.stdin.flush();head=proc.stdout.readline().split();old=proc.stdout.read(int(head[2]));proc.stdout.read(1)
  record={'sha256':hashlib.sha256(old).hexdigest(),'size':len(old)}
  if p.endswith('.png'):im=Image.open(io.BytesIO(old));record.update(dimensions=list(im.size),mode=im.mode)
  records[p]=record
  if p not in tracked or not (ROOT/p).is_file():errors.append('Deleted/renamed frozen resource: '+p);continue
  new=(ROOT/p).read_bytes()
  if p.endswith('.pal'):new=new.replace(b'\r\n',b'\n')
  if old==new:continue
  if p not in ALLOW:errors.append('Changed frozen resource: '+p);continue
  a=Image.open(io.BytesIO(old));b=Image.open(io.BytesIO(new))
  if b.size!=(144,32) or a.size!=b.size or a.mode!=b.mode or old[24]!=new[24]:errors.append('PNG shape/mode/depth changed: '+p);continue
  if a.getpalette()!=b.getpalette() or a.info.get('transparency')!=b.info.get('transparency'):errors.append('Palette/alpha changed: '+p)
  if set(b.getdata())-set(a.getdata()):errors.append('New indices: '+p)
  for y in range(32):
   for x in range(144):
    if a.getpixel((x,y))!=b.getpixel((x,y)) and x//16 not in (3,5):errors.append(f'Forbidden pixel: {p} {x},{y}')
 proc.stdin.close();proc.wait()
 extras=(tracked-set(names))|set(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=ROOT).decode().splitlines())
 errors += ['New compiled resource: '+p for p in extras if protected(p)]
 if args.manifest:args.manifest.parent.mkdir(parents=True,exist_ok=True);args.manifest.write_text(json.dumps({'base':args.base,'assets':records},indent=2)+'\n')
 if errors:print('\n'.join(errors));return 1
 print(f'Art freeze PASS: {len(records)} assets; only Ciro frames 3/5 may differ.');return 0
if __name__=='__main__':raise SystemExit(main())

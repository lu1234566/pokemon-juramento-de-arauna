#!/usr/bin/env python3
"""Compare installed text with linked ROM bytes using the canonical preproc."""
import argparse,re,subprocess,tempfile
from pathlib import Path
import sync_arauna_curated_text as sync
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--elf',type=Path,default=ROOT/'pokemon-juramento-de-arauna-en_modern.elf');p.add_argument('--rom',type=Path,default=ROOT/'pokemon-juramento-de-arauna-en_modern.gba');p.add_argument('--nm',default='arm-none-eabi-nm');a=p.parse_args()
 listing=subprocess.check_output([a.nm,'-n',str(a.elf)],text=True);symbols={n:int(v,16) for v,k,n in (line.split() for line in listing.splitlines() if len(line.split())==3)};rom=a.rom.read_bytes();count=0
 for path,source in sync.outputs().items():
  if path.suffix=='.inc':assembly=source
  else:assembly='\n'.join(f'{n}:\n\t.string "{body}"' for n,body in re.findall(r'(?:static )?const u8 (\w+)\[\] = _\("([^"\n]*)"\);',source))+'\n'
  with tempfile.TemporaryDirectory() as tmp:
   text=Path(tmp)/'text.s';text.write_text(assembly);encoded=subprocess.check_output([str(ROOT/'tools/preproc/preproc'),str(text),str(ROOT/'charmap.txt')],text=True)
  for label,body in re.findall(r'(?m)^(\w+)::?\n((?:\s*\.byte [^\n]+\n)+)',encoded):
   if label not in symbols:continue
   values=[]
   try:
    for line in body.strip().splitlines():values.extend(int(x.strip(),0) for x in line.split('.byte',1)[1].split(','))
   except ValueError:continue
   offset=symbols[label]-0x08000000
   if rom[offset:offset+len(values)]!=bytes(values):raise SystemExit('Compiled text mismatch: '+label)
   count+=1
 print(f'ROM text byte equivalence PASS: {count} linked text blocks.');return 0
if __name__=='__main__':raise SystemExit(main())

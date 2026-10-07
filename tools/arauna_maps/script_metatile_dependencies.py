"""Resolve map scripts and transitively referenced shared script labels."""
import re
from pathlib import Path

def collect(repo,mapname,labels):
 repo=Path(repo);blocks={}
 for p in (repo/'data').rglob('*.inc'):
  if '/scripts/' not in p.as_posix() and '/maps/' not in p.as_posix():continue
  text=p.read_text(errors='replace');defs=list(re.finditer(r'^([A-Za-z_]\w*)::?\s*$',text,re.M))
  for i,m in enumerate(defs):blocks[m[1]]=text[m.end():defs[i+1].start() if i+1<len(defs) else len(text)]
 text='\n'.join(p.read_text() for p in (repo/'data/maps'/mapname).glob('*.inc'));pending=set(re.findall(r'\b[A-Za-z_]\w*\b',text))&blocks.keys();visited=set();parts=[text]
 while pending:
  label=min(pending);pending.remove(label)
  if label in visited:continue
  visited.add(label);block=blocks[label];parts.append(block);pending.update((set(re.findall(r'\b[A-Za-z_]\w*\b',block))&blocks.keys())-visited)
 text='\n'.join(parts);ids={labels[k] for k in re.findall(r'METATILE_\w+',text) if k in labels}
 for token in re.findall(r'^\s*setmetatile\s+[^,]+,[^,]+,\s*(0x[\da-fA-F]+|\d+)\s*,',text,re.M):ids.add(int(token,0))
 return ids,sorted(visited)

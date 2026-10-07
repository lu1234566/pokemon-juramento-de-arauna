#!/usr/bin/env python3
"""Deterministic full cave/Lanette review render, including camera aliases."""
import argparse,json
from pathlib import Path
from native_visuals_v2 import ROOT
from bancos_nativos import resolve_bank
from render_native_map import Renderer,render_map
ap=argparse.ArgumentParser();ap.add_argument('map');ap.add_argument('output',type=Path);a=ap.parse_args();m=json.loads((ROOT/'data/maps'/a.map/'map.json').read_text());l=next(l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'] if l['id']==m['layout']);r=Renderer(*[resolve_bank(ROOT,l[k]) for k in ('primary_tileset','secondary_tileset')]);p=ROOT/'review/grutas_bordas_v2/visual_grids'/f'{a.map}.bin';assert p.exists(),'Map has no contextual camera grid';a.output.parent.mkdir(parents=True,exist_ok=True);render_map(r,p,l['width'],l['height']).save(a.output);print(a.output)

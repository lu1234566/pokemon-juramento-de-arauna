"""06C2: native forest bases over reconciled 06C1 and GitHub maintenance."""
import subprocess
from native_visuals_v2 import ROOT
from secret_06c1_common import inventory,parts,SecretRenderer,render
BASE='6cfba8c79b4bc674d9962063f7fdb2d18a238fa4'
GITHUB_BASE='872f56e86f09d3dff41a9e6c7a8bc5640386fe86'
PREVIOUS='0098c5c3b54e32b925e4ff839cd0535e772b6778'
OUT=ROOT/'review/secret_bases_06c2'
COLORS=('Tree','Shrub')
NAMES=tuple(f'SecretBase_{color}{i}' for color in COLORS for i in range(1,5))
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}
def require_base(repo):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE

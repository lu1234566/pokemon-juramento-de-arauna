"""Five service maps on the official 07G integration, without changing gameplay."""
import subprocess
from native_visuals_v2 import ROOT,callback
from safari_05_common import inventory
from frontier_07g_common import renderer,render,render_grid
BASE='531352ce3715e41389382de692e917a32b9e60be'
PREVIOUS='4122b9fa98db5604cb302468ff89dfc0145865a0'
EARLIER='eb49778fa84f058c496fdcdcdacc4888e3602c97'
GITHUB_9F='9f0a056e90fd42fa426030aca2f2e241401c0700'
OLDER='989c33c94fb89b92c5f608f78233fdd8deded4c4'
MAIN='979fb6c1b6731561f3c993efd6045a9bbf096c54'
OUT=ROOT/'review/frontier_07h'
NAMES=tuple('BattleFrontier_'+s for s in ('ExchangeServiceCorner','Mart','PokemonCenter_1F','PokemonCenter_2F','RankingHall'))
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}
ROLES=('Troca por Battle Points','Mercado','Cura e PC','Comunicação e troca','Galeria dos recordes')
def require_base(repo):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE

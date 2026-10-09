"""Ten lounges/house maps retain their three shared layouts and original services."""
import subprocess
from native_visuals_v2 import ROOT,callback
from safari_05_common import inventory
from frontier_07f_common import renderer,render,render_grid
BASE='eb49778fa84f058c496fdcdcdacc4888e3602c97'
PREVIOUS='fd298f4467329eddfa8f65f57f9ee88ab365e3e2'
EARLIER='9a3f9464ea6ba1e30b599c76648e4eb0e1a49405'
GITHUB_9F='9f0a056e90fd42fa426030aca2f2e241401c0700'
OLDER='989c33c94fb89b92c5f608f78233fdd8deded4c4'
MAIN='979fb6c1b6731561f3c993efd6045a9bbf096c54'
OUT=ROOT/'review/frontier_07g'
NAMES=tuple('BattleFrontier_Lounge'+str(i) for i in range(1,10))+('BattleFrontier_ScottsHouse',)
MUTABLE={'data/layouts/layouts.json',*('src/data/tilesets/'+f for f in ('graphics.h','metatiles.h','headers.h'))}
ROLES=('Avaliador de IVs','Notícias das sete instalações','Aposta de Battle Points','Conversas de descanso','Natureza dos Pokémon','Troca de Pokémon','Dois tutores por Battle Points','Dicas do circuito','Aprendiz','Bento — recompensas do Frontier')
def require_base(repo):
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==BASE

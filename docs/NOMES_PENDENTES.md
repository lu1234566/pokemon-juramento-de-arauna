# Os nomes de Hoenn acabaram

Este documento pedia treze nomes. Não pede mais nenhum: as 227 falas que ainda
chamavam personagens pelo elenco do Emerald foram renomeadas, e o gate
`tools/arauna/build_character_names.py --check` agora relata **zero**.

Foram dois caminhos diferentes, porque os dois grupos estavam em estados
diferentes.

## A Elite dos Quatro já tinha nome — faltava rodar o renderer

`scripts/render_arauna_league_en_checked.py` existia, estava na ordem travada
de `scripts/english_renderers.txt`, carregava a tabela de nomes desde sempre e
**nunca tinha sido aplicado**. Bastou rodá-lo:

| Hoenn | Arauna |
|---|---|
| SIDNEY | **LÁZARO** |
| PHOEBE | **ROSA** |
| GLACIA | **CLARA** |
| DRAKE | **TIBÚRCIO** |

Junto com os quatro `trainerName`, ele reescreveu 88 blocos de texto em onze
mapas: a Estrada do Juramento inteira, as quatro salas da Elite, a sala da
Campeã e o Centro.

## Os outros dez não tinham nome nenhum

Esses foram escolhidos agora, e `tools/arauna/build_remaining_names.py` os
aplicou em 280 menções e 74 arquivos.

| Hoenn | Arauna | menções | quem é |
|---|---|---:|---|
| RYDEL | **ZEFERINO** | 68 | a loja de bicicletas na ENCRUZILHADA |
| CAPT. STERN | **CAPT. NUNES** | 54 | o capitão do submersível |
| SCOTT | **BENTO** | 42 | o recrutador do BATTLE CIRCUIT |
| MR. BRINEY | **MR. HONÓRIO** | 42 | o velho marinheiro do barco |
| PEEKO | **PÉROLA** | 21 | a ave dele |
| MR. STONE | **MR. AMARAL** | 19 | presidente da HORIZON |
| LANETTE | **LENITA** | 13 | a dona do sistema de PC |
| PROF. COZMO | **PROF. SALÚSTIO** | 13 | o pesquisador do METEORITE |
| WINSTRATE | **QUEIROZ** | 5 | a família de quatro da ROUTE 111 |
| BILL | **ELCIO** | 3 | a assinatura numa carta |

**O BENTO não foi escolha minha.** O projeto já tinha decidido: o renderer
`render_battle_circuit_public_services_en_checked.py` chama o mapa
`BattleFrontier_ScottsHouse` de `bento_room`, e o texto lá já dizia
`MR. BENTO`. Só faltava o resto do jogo saber.

Os outros nove foram conferidos contra tudo que já tem nome no jogo — as 386
criaturas, os 434 treinadores de rota, os 526 do Frontier, os 16 aprendizes, os
lugares e o elenco da história. **Nenhum colide.** Foi por isso que caíram
alguns candidatos melhores de ouvido: NIVALDO, JOAQUIM, CELSO e TITO já eram
gente no jogo.

## Trocar um destes nomes é editar uma célula

Todos saem da coluna `arauna_name` de `docs/arauna/ARAUNA_CHARACTER_NAMES.csv`.
Para trocar um:

```
edite a célula, depois
python3 tools/arauna/build_remaining_names.py --write
python3 tools/arauna/rewrap_text.py --write
python3 tools/arauna/check_text_width.py
```

O renomeador compara com o que está na árvore, então rodar duas vezes não
empilha. O da Elite dos Quatro mora em `TRAINER_NAMES`, dentro do renderer da
Liga.

## Duas coisas que o título carrega

**O título anda junto.** `MR. BRINEY` e um `BRINEY` solto são o mesmo homem, e
os dois foram renomeados. `CAPT. STERN` virou `CAPT. NUNES`, e o estaleiro que
leva o nome dele virou `NUNES'S SHIPYARD`.

**O STONE é a exceção, e é por isso que não foi uma lista de palavras.** O
presidente é `MR. STONE` e `PRESIDENT STONE`, mas o jogo também vende MOON
STONE, WATER STONE, FIRE STONE e LEAF STONE. Só as duas formas com título foram
trocadas; um `STONE` sozinho continua sendo pedra.

## Um defeito que só apareceu porque o renderer rodou

O renderer da Liga escrevia **`SEU BENTO`** na fala do Centro de Ever Grande.
Como ele nunca tinha sido aplicado, o `check_english_only_policy.py` nunca tinha
visto aquela linha — e "seu" está no léxico português, então ela reprovou o
gate na hora.

O resto do jogo já dizia `MR. BENTO`, que é a forma que passa. Corrigido na
origem, em `data/text/arauna/en/league_finale.json`, e não no texto gerado.

Vale a nota para quem vier depois: os bancos JSON de `data/text/arauna/en/`
**não são varridos pelo gate de português** — ele lê `.inc`, `.s` e C. Ainda
existem cinco `SEU BENTO` em `baia_luzes_harbor_tickets.json` e
`baia_luzes_interiors.json` que vão reprovar o gate no dia em que aqueles
renderers forem aplicados.

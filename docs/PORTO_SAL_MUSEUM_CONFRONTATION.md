# Porto do Sal — confronto no Museu

Este lote cura o evento plot-critical de `SlateportCity_OceanicMuseum_2F` e a superficie visivel de `ITEM_DEVON_GOODS` sem alterar qualquer identificador interno ou fluxo de progressao.

## Pecas Oceanicas

`ITEM_DEVON_GOODS` permanece exatamente o mesmo ID interno. Apenas a superficie muda:

- `DEVON GOODS` -> `PECAS OCEAN.`;
- descricao -> pecas para pesquisa oceanografica em grande profundidade.

Isso preserva todos os scripts que entregam, transportam ou removem o item, mas evita que a animacao de entrega no Museu mostre a organizacao vanilla DEVON.

Na cena, o ENGENHEIRO explica que as pecas servem para calibrar sensores de profundidade usados em expedicoes maritimas.

## Tentativa do Horizonte

Dois agentes do HORIZONTE tentam requisitar as pecas porque elas podem ajudar a mapear anomalias sob M'BOI.

A superficie deixa claro que:

- a equipe civil nao autorizou a requisicao;
- os agentes acreditam estar cumprindo uma operacao de campo;
- o confronto com o jogador nao fazia parte do plano;
- depois de duas derrotas, eles nao conseguem concluir a requisicao.

`TRAINER_GRUNT_MUSEUM_1` e `TRAINER_GRUNT_MUSEUM_2` permanecem intactos, assim como parties, IA, flags e movimentos.

## Otacilio

OTACILIO chega para entender a demora e reconhece que as pecas seriam uteis no mapeamento das cavernas de M'BOI.

Nesta fase da historia, porem, ele recua:

- reconhece que transformar um MUSEU em operacao forcada nao e cuidado;
- manda os agentes recuarem;
- decide procurar outra forma.

Esse comportamento e deliberadamente anterior a `PORTO_SAL_SUBMERSIVEL.md`.

Na crise posterior, com as leituras de M'BOI ja disparando, OTACILIO cruza uma linha que aqui ainda recusava cruzar e requisita o submersivel sem esperar permissao. A diferenca entre as duas cenas funciona como escalada do personagem, nao como inconsistencia.

## Entrega ao engenheiro

Depois da retirada do HORIZONTE:

- o jogador entrega `ITEM_DEVON_GOODS` pelo mesmo script original;
- a superficie chama o item de PECAS OCEANICAS;
- o ENGENHEIRO leva as pecas ao laboratorio do porto;
- a expedicao ao fundo do mar continua.

`Common_EventScript_PlayerHandedOverTheItem` e todos os flags de entrega permanecem intactos.

## Estrutura preservada

Permanecem intactos:

- `ITEM_DEVON_GOODS`;
- `FLAG_DELIVERED_DEVON_GOODS`;
- `FLAG_MET_TEAM_AQUA_HARBOR`;
- `VAR_SLATEPORT_MUSEUM_1F_STATE`;
- os dois treinadores do Museu;
- entrada/saida de OTACILIO e agentes;
- musicas, movimentos, `LOCALID_*` e coordenadas;
- `Common_EventScript_PlayerHandedOverTheItem`;
- retorno ao 1F, warps, saves e progressao.

Nenhum `scripts.inc` e commitado modificado.

## Validacao

`scripts/render_porto_sal_museum_confrontation.py` cobre 13 blocos plot-critical e tambem valida o nome/descricao visiveis das PECAS OCEANICAS.

Todas as linhas novas respeitam o teto de 32 caracteres. O renderer usa labels exatos, assinaturas conhecidas da superficie anterior, comparacao estrutural mascarada e anchors unicos para `DEVON GOODS`/`sDevonGoodsDesc`.

O build aplica esta camada depois de `render_ruinas_memorial_surface_checked.py`, pois ambos alteram `items.h`/`item_descriptions.h`. O auditor global reproduz a mesma ordem explicitamente.

Entrada:

`python3 scripts/render_porto_sal_museum_confrontation.py --check`

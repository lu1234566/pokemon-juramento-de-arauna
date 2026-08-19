# Missoes do Ceu — 1F, operacao civil e ocupacao

Esta camada complementa `MISSOES_CEU_CONFRONTATION.md` e cura os 28 blocos visiveis de `MossdeepCity_SpaceCenter_1F`.

O centro continua sendo uma instalacao espacial funcional. A intencao nao e transformar todos os NPCs em expositores do ARQUIVO VIVO, mas preservar a identidade cientifica de MISSOES DO CEU e fazer a ocupacao dos LEMBRANTES reagir a essa rotina real.

## Operacao normal

As falas civis passam para PT-BR e mantem a funcao original do local:

- contagem semanal de lancamentos;
- lancamento iminente;
- historico de lancamentos seguros;
- exigencia de precisao para missoes espaciais;
- chuvas de meteoros de Arauna;
- curiosidade sobre POKéMON e espaco;
- moradores fascinados por foguetes e pelo ceu.

O contador continua usando `GetWeekCount`, `buffernumberstring` e `{STR_VAR_1}` exatamente como no Emerald.

## Sun Stone

O NPC que entrega `ITEM_SUN_STONE` continua com:

- o mesmo item;
- a mesma `FLAG_RECEIVED_SUN_STONE_MOSSDEEP`;
- o mesmo tratamento de bolsa cheia;
- o mesmo fluxo antes/durante a ocupacao.

Apenas a fala visivel muda: a pedra foi encontrada perto da costa e o NPC prefere entrega-la ao jogador enquanto o predio esta ocupado.

## Ocupacao

Durante `VAR_MOSSDEEP_CITY_STATE == 2`:

- cientistas explicam que o uplink conversa com estacoes em quase toda Arauna;
- civis demonstram desconforto tanto com a ocupacao dos LEMBRANTES quanto com a possibilidade de entregar a rede ao HORIZONTE;
- SEU BENTO identifica a chave de sincronismo no andar superior e recusa a ideia de uma faccao decidir sozinha pela rede;
- quatro LEMBRANTES deixam de repetir paragrafo generico e explicam transmissor, comandos remotos, sensores, RAUL/LUZIA e o desconforto de ocupar um centro publico;
- o aviso no terminal declara explicitamente que o objetivo e neutralizar a chave de sincronismo, sem apagar dados civis.

Isso prepara diretamente o confronto do 2F.

## Estrutura preservada

Permanecem intactos:

- `GetWeekCount`, `dotimebasedevents` e contador de lancamentos;
- `ITEM_SUN_STONE` e `FLAG_RECEIVED_SUN_STONE_MOSSDEEP`;
- `Common_EventScript_ShowBagIsFull`;
- `TRAINER_GRUNT_SPACE_CENTER_1/2/3/4`;
- scripts e flags de batalha;
- `VAR_MOSSDEEP_CITY_STATE`;
- `VAR_MOSSDEEP_SPACE_CENTER_STAIR_GUARD_STATE`;
- movimentos especiais do guarda da escada, inclusive comportamento herdado/BUGFIX;
- metatile da nota;
- objetos, coordenadas, warps, saves e progressao.

## Validacao

`scripts/render_missoes_ceu_ground_floor.py` cobre 28 blocos.

O renderer exige:

- labels exatos;
- assinatura reconhecida da superficie anterior;
- maximo de 32 caracteres visiveis por segmento;
- placeholder do contador tratado de forma conservadora;
- comparacao estrutural mascarada;
- ausencia de residuos centrais em ingles/Hoenn nas falas alvo.

Entrada:

`python3 scripts/render_missoes_ceu_ground_floor.py --check`

O build aplica primeiro o renderer do 1F e depois o confronto do 2F. Os dois arquivos sao protegidos pelo backup transacional e restaurados no `EXIT`.

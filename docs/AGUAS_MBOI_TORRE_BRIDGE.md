# Aguas de M'Boi + ponte para a Torre do Juramento

Este lote cura a crise de `SootopolisCity` e a transicao para `SkyPillar_Outside` sem alterar o grafo de eventos herdado do Pokemon Emerald.

## Aguas de M'Boi

A cidade deixa de funcionar apenas como a cena visual de dois lendarios e passa a mostrar o custo humano do colapso do ARQUIVO VIVO.

Os moradores relatam efeitos coerentes com o DESENCANTO e com o colapso dos VINCULOS:

- lembrancas de casas e pessoas que nunca conheceram;
- esquecimento temporario de nomes familiares;
- memorias alheias que permanecem mesmo depois de as correntes recuarem;
- a necessidade de confirmar nomes e identidades depois da crise.

Esses relatos substituem falas vanilla em ingles sobre POKéMON gigantes, a cor dos lendarios e a destruicao de SOOTOPOLIS.

## Luzia e Otacilio

Os slots internos Maxie e Archie permanecem intactos.

Na superficie visivel:

- LUZIA reconhece que devolver toda memoria sem escolha tambem pode virar imposicao;
- OTACILIO reconhece que encerrar a dor sem consentimento tambem e exercicio de poder;
- depois da intervencao do Guardiao, ambos admitem o proprio erro em vez de repetir a mesma explicacao generica;
- a saida posterior para o MEMORIAL continua preservada pelo evento original.

## Iara-Mae e Anhanguera

O repositorio ja estabelece:

- IARA-MAE como corrente que puxa VINCULOS de volta;
- ANHANGUERA como corrente que encerra os que nao podem continuar.

Por isso os nomes aparecem na crise de Aguas de M'Boi, onde as duas correntes se manifestam juntas.

Este lote nao cria uma equivalencia tecnica explicita entre esses nomes e `SPECIES_KYOGRE`/`SPECIES_GROUDON`. Os identificadores internos e a apresentacao visual permanecem herdados ate existir uma decisao canonica/artistica inequivoca.

## Seu Bento

O slot interno Steven continua inalterado. A superficie de SEU BENTO passa a:

- explicar que o fenomeno nao e simplesmente uma batalha de POKéMON;
- conduzir o jogador ao nucleo da cidade;
- apontar AMALIA como a pessoa que encontrou registros antigos da TORRE DO JURAMENTO;
- permanecer na cidade enquanto o jogador segue para a Torre;
- reconhecer depois que o Guardiao respondeu ao JURAMENTO;
- informar que LUZIA e OTACILIO retornaram ao MEMORIAL para devolver o que retiraram.

## Amalia

O slot interno Wallace e preservado.

AMALIA agora:

- prioriza impedir a perda de identidade da cidade antes de julgar Luzia e Otacilio;
- direciona o jogador para a TORRE DO JURAMENTO;
- reconhece, depois da crise, que o jogador impediu que duas ideias se transformassem em sentenca;
- mantem intacta a entrega da HM e a progressao do GINASIO.

## Guardiao da Torre

`SPECIES_RAYQUAZA`, objetos, animacoes, cries, batalha posterior e flags continuam intactos.

O nome `RAYQUAZA` deixa de ser apresentado como identidade canonica na fala de AMALIA na entrada da Torre. Ate existir nome/arte definitiva, a superficie usa `GUARDIAO DA TORRE`.

A fala final existente no topo da Torre ja expressa corretamente a tese do JURAMENTO e nao foi alterada.

## Estrutura preservada

Permanecem intactos:

- `VAR_SOOTOPOLIS_CITY_STATE`;
- `VAR_SKY_PILLAR_STATE`;
- `FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE`;
- `FLAG_STEVEN_GUIDES_TO_CAVE_OF_ORIGIN`;
- `FLAG_WALLACE_GOES_TO_SKY_PILLAR`;
- todos os `LOCALID_*`;
- layouts alternativos;
- clima, tremores, camera e movimentos;
- `SPECIES_KYOGRE`, `SPECIES_GROUDON` e `SPECIES_RAYQUAZA`;
- entrega de HM, Ginasio, warps, saves e progressao.

## Validacao

A entrada oficial e:

`python3 scripts/render_aguas_mboi_surface.py --check`

O renderer valida anchors exatos, largura visivel maxima de 32 caracteres e compara a estrutura mascarada antes/depois para rejeitar alteracoes fora dos corpos de dialogo selecionados.

`scripts/build_arauna.sh` inclui `SootopolisCity/scripts.inc` e `SkyPillar_Outside/scripts.inc` no backup transacional e restaura os fontes no `EXIT`.

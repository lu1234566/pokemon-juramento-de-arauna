# Cavernas de M'Boi — clímax da sala 9

Este lote cura os quinze blocos de diálogo da sequência herdada `SeafloorCavern_Room9` sem alterar nenhum comando, movimento, batalha, flag, warp ou objeto da cena.

## Objetivo dramático

A versão anterior já usava termos de Arauna, mas havia sido produzida por uma reescrita ampla e repetia parágrafos genéricos em momentos que exigem reação específica. A nova superfície segue a ordem real do evento:

1. OTACILIO impede o jogador de tocar no núcleo do ARQUIVO;
2. reconhece que o jogador já leu os arquivos de M'BOI;
3. explica que há sob M'BOI uma corrente antiga capaz de puxar VINCULOS de volta;
4. batalha para impedir o desligamento do experimento;
5. usa o REGISTRO-MATRIZ retirado do Memorial para sincronizar o ARQUIVO;
6. o registro reage sem comando e o sistema perde o controle;
7. a corrente deixa a caverna;
8. uma chamada externa informa que as leituras estão subindo em toda Arauna;
9. OTACILIO percebe que o ARQUIVO espalhou, em vez de conter, o fenômeno;
10. LUZIA chega e confronta OTACILIO;
11. os dois entendem que as duas correntes reagiram;
12. LUZIA leva o jogador para observar o desastre nas AGUAS DE M'BOI.

## Nomes míticos

O repositório já estabelece que IARA-MAE puxa VINCULOS de volta e ANHANGUERA encerra os que não podem continuar. Entretanto, este lote não fixa uma equivalência explícita entre esses nomes e os slots internos Kyogre/Groudon, porque essa associação não está formalizada de maneira inequívoca no material auditado.

Por isso a sala usa `corrente` e `corrente de retorno` onde o esqueleto Emerald usa Kyogre. Os nomes míticos ficam para a cena seguinte, em que ambas as correntes estão presentes ao mesmo tempo.

## Estrutura preservada

Continuam intactos:

- `TRAINER_ARCHIE`;
- todos os `LOCALID_SEAFLOOR_CAVERN_*`;
- `SPECIES_KYOGRE` e seus objetos/movimentos;
- efeito do orbe, clima, tremores e música;
- `VAR_ROUTE128_STATE`, `VAR_SOOTOPOLIS_CITY_STATE` e `VAR_SEAFLOOR_CAVERN_STATE`;
- todas as flags de Hide/Legendary;
- warp final para Route 128;
- save e progressão.

Esses identificadores continuam sendo apenas a infraestrutura do Emerald.

## Validação

`python3 scripts/render_mboi_climax_surface.py --check`

O renderer exige os quinze labels e marcadores de origem, limita cada segmento visível a 32 caracteres e compara a estrutura antes/depois com os corpos de diálogo mascarados. Qualquer alteração fora dos textos selecionados aborta o processo.

`scripts/build_arauna.sh` inclui `SeafloorCavern_Room9/scripts.inc` no backup transacional e restaura o fonte no `EXIT`.

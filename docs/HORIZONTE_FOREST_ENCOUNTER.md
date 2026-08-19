# Primeiro encontro com o Consorcio Horizonte

Este lote converte a superficie textual do primeiro encontro herdado de Team Aqua em `PetalburgWoods` sem alterar a estrutura de evento do Emerald.

## Canon usado

O proprio repositorio ja define os slots de Team Aqua como agentes do HORIZONTE / Consorcio Horizonte e as classes de batalha `TRAINER_CLASS_TEAM_AQUA`, `AQUA_ADMIN` e `AQUA_LEADER` como identidades HORIZONTE. Este lote apenas alinha o dialogo a esse canon existente.

## Superficie convertida

Doze blocos de dialogo da cena principal passam a:

- apresentar o agressor como membro do Consorcio Horizonte;
- usar `PESQUISADOR` em vez de `DEVON RESEARCHER`;
- evitar o nome legado `PETALBURG WOODS`, usando referencia neutra a mata;
- substituir a referencia visivel a `RUSTBORO` por `SERRA DO UIVO`;
- remover o dialogo ingles do pesquisador, agressor e pos-batalha;
- preservar a recompensa, mas sem depender de mencionar `GREAT BALL` no dialogo.

O nome SHROOMISH tambem deixa de ser necessario para a cena; o pesquisador passa a dizer que acompanha a fauna local. Isso evita fixar uma especie herdada como elemento narrativo antes da revisao completa da fauna de Arauna.

## Estrutura preservada

Continuam intactos:

- `TRAINER_GRUNT_PETALBURG_WOODS`;
- `LOCALID_PETALBURG_WOODS_*`;
- `PetalburgWoods_Movement_Aqua*`;
- `MUS_ENCOUNTER_AQUA`;
- `VAR_PETALBURG_WOODS_STATE`;
- `ITEM_GREAT_BALL` e toda a logica de BOLSA cheia;
- movimentos, coordenadas, flags, batalha e progressao.

Esses nomes sao identificadores internos do esqueleto Emerald e nao devem ser renomeados.

## Build reversivel

`scripts/build_arauna.sh` cria backup temporario tanto de `src/strings.c` quanto de `data/maps/PetalburgWoods/scripts.inc`, aplica as camadas narrativas e restaura os arquivos em `EXIT` mesmo se a compilacao falhar.

## Validacao

`python3 scripts/render_petalburg_woods_surface.py --check`

O renderer exige os 12 labels e marcadores esperados, valida largura visivel maxima de 32 caracteres e rejeita a sobrevivencia de `PETALBURG WOODS`, `DEVON RESEARCHER`, `RUSTBORO` ou `TEAM AQUA` dentro dos blocos renderizados.

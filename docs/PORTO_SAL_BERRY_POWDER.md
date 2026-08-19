# PO DE BERRY em Porto do Sal

## Objetivo

Fechar a superficie visivel do sistema Berry Powder em Porto do Sal sem alterar a mecanica, o formato de save ou os custos do vendedor.

## Dialogos

Nove blocos do vendedor foram localizados:

- explicacao de BERRIES e remedios;
- explicacao das maquinas que produzem po;
- pergunta sobre a quantidade trazida;
- selecao de troca;
- confirmacao da troca por item;
- falta de quantidade suficiente;
- convite para novas trocas;
- retorno quando houver mais po;
- despedida da banca.

A expressao visivel usada e `PO DE BERRY`.

## UI

Dois literais compartilhados pela propria mecanica tambem sao renderizados:

- `gText_Powder` -> `PO DE BERRY`;
- `gText_PowderQty` -> `PO DE BERRY: {STR_VAR_1}`.

Os simbolos, quantidade e janela continuam usando as mesmas funcoes internas.

## Preservado

Permanecem intactos:

- `berryPowderAmount` no save;
- criptografia do valor;
- limite `MAX_BERRY_POWDER = 99999`;
- `HasEnoughBerryPowder`;
- `GiveBerryPowder`;
- `TakeBerryPowder`;
- `GetBerryPowder`;
- custos dos itens;
- menu do vendedor;
- `DisplayBerryPowderVendorMenu`;
- `PrintPlayerBerryPowderAmount`;
- Powder Jar e demais IDs internos.

## Seguranca

`scripts/render_porto_sal_berry_powder.py` valida:

- 9 labels exatos de dialogo;
- marcadores da superficie inglesa anterior;
- segmentos de no maximo 32 caracteres;
- comparacao estrutural mascarada do mapa;
- dois anchors unicos em `src/strings.c`;
- ausencia de `BERRY POWDER`, `BERRY CRUSH` e `POWDER QTY` na superficie alvo renderizada.

`src/strings.c` ja faz parte do backup transacional do build. A camada roda depois de `render_arauna_frontier_ui.py`, preservando a identidade do Circuito e acrescentando apenas os literais do PO DE BERRY.

O auditor renderizado compoe tanto a camada ASM quanto a camada C para refletir a ROM final.

Sem arte, sem Codespaces e PR #58 intocado.

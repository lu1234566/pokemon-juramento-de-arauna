# Serra da Cinza: conflito Horizonte x Lembrantes

Este lote corrige a superficie narrativa do slot `MtChimney` sem alterar nenhum elemento estrutural do mapa ou da progressao Emerald.

## Problema encontrado

O mapa ja continha trechos de Arauna, mas a reescrita antiga havia deixado uma mistura inconsistente:

- LUZIA e OTACILIO ja apareciam em algumas falas;
- grunts que o jogador enfrenta no lado Magma/Lembrante mudavam para falas `HORIZONTE` depois da derrota;
- NPCs ocupando slots Aqua/Horizonte apareciam como `LEMBRANTE`;
- varios blocos plot-critical ainda falavam de expandir terra, vulcao, WATER POKéMON, BOSS e objetivos de Team Magma;
- a maquina do meteorito continuava sem relacao textual com VINCULO/ARQUIVO;
- a placa ainda apontava para `JAGGED PATH` / `LAVARIDGE TOWN`.

## Canon aplicado

- slot Aqua -> HORIZONTE / Consorcio Horizonte;
- Archie -> OTACILIO;
- slot Magma -> LEMBRANTES;
- Maxie -> LUZIA;
- Mt. Chimney -> SERRA DA CINZA;
- Lavaridge-facing destination -> SERTAO DE DENTRO;
- maquina do meteorito -> amplificador de VINCULO.

A cena passa a tratar o conflito como uma disputa sobre consentimento: Luzia tenta devolver memorias extraidas, enquanto Horizonte tenta impedir uma liberacao sem controle. Os proprios Lembrantes reconhecem que devolver memoria a forca tambem pode ser uma forma de violencia.

## Cobertura

O renderer cobre 31 blocos plot-critical:

- Luzia: introducao, derrota e retirada;
- Otacilio: pedido de intervencao, fala durante o confronto e agradecimento;
- comandante Lembrante no slot Tabitha;
- os dois grunts combatidos pelo jogador;
- NPCs Horizonte e Lembrantes ocupados no conflito ao fundo;
- equipamento do meteorito, remocao e estado desligado;
- placa de saida da Serra da Cinza.

NPCs comuns, loja de Lava Cookie e treinadores opcionais ficam fora deste lote para evitar uma reescrita editorial ampla demais.

## Preservado

Continuam intactos `TRAINER_MAXIE_MT_CHIMNEY`, `TRAINER_TABITHA_MT_CHIMNEY`, grunts, `LOCALID_MT_CHIMNEY_*`, `MUS_ENCOUNTER_MAGMA`, `FLAG_HIDE_MT_CHIMNEY_TEAM_AQUA`, `FLAG_HIDE_MT_CHIMNEY_TEAM_MAGMA`, `FLAG_DEFEATED_EVIL_TEAM_MT_CHIMNEY`, `ITEM_METEORITE`, movimentos, coordenadas, warps, clima, saves e progressao.

## Build e validacao

`scripts/build_arauna.sh` inclui `data/maps/MtChimney/scripts.inc` no backup temporario e restaura o fonte no `EXIT`.

`python3 scripts/render_mt_chimney_surface.py --check`

O renderer exige os 31 labels e marcadores de origem e valida largura visivel maxima de 32 caracteres. O auditor global analisa a versao renderizada da cena em vez do fonte legado.

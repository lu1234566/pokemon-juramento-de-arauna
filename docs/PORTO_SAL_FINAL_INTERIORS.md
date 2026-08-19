# Fechamento dos interiores de Porto do Sal

## Objetivo

Eliminar as ultimas falas map-specific herdadas de Slateport nos interiores civis de Porto do Sal.

Este lote fecha tres mapas pequenos que restavam depois de Museu, Estaleiro, Cais, Tenda de Batalha, Clube de Fas e Avaliador de Nomes.

## Cobertura

`scripts/render_porto_sal_final_interiors.py` cobre seis blocos:

### Casa comum

`data/maps/SlateportCity_House/scripts.inc`

- natureza HASTY e crescimento de atributos;
- visitante que indica a TENDA DE BATALHA de Porto do Sal.

### POKé MART

`data/maps/SlateportCity_Mart/scripts.inc`

- diferenca entre MERCADO e POKé MART;
- explicacao de GREAT BALL vs. POKé BALL.

O estoque do Mart permanece original.

### Centro POKéMON 1F

`data/maps/SlateportCity_PokemonCenter_1F/scripts.inc`

- dica de equilibrio entre tipos;
- comentario sobre troca de POKéMON com item.

A enfermeira continua usando `Common_EventScript_PkmnCenterNurse` sem qualquer alteracao.

### Centro POKéMON 2F

Nao possui dialogo map-specific ativo. O mapa apenas chama a infraestrutura compartilhada de Cable Club, portanto nao recebe overlay neste lote.

## Marco de conclusao

Com este renderer, todos os mapas `SlateportCity_*` com falas locais ativas estao cobertos por camadas de Arauna/PT-BR ou nao possuem texto proprio.

Isso significa que residuos futuros visiveis dentro de Porto do Sal devem ser tratados como **superficies compartilhadas do sistema** — por exemplo nurse, Cable Club, marts ou menus globais — e nao como residuos map-specific de Slateport.

## Preservado

- estoque e precos do Mart;
- `ITEM_*`;
- `HEAL_LOCATION_SLATEPORT_CITY` interno;
- `Common_EventScript_UpdateBrineyLocation` interno;
- `Common_EventScript_PkmnCenterNurse`;
- Cable Club;
- respawn;
- warps;
- objetos;
- flags;
- vars;
- saves.

## Seguranca

O renderer exige:

- cada label alvo exatamente uma vez;
- no maximo duas linhas por pagina;
- no maximo 32 caracteres por segmento visivel;
- identidade estrutural depois de mascarar `.string`;
- aplicacao apenas no build transacional.

O auditor renderizado usa a mesma camada antes de classificar residuos.

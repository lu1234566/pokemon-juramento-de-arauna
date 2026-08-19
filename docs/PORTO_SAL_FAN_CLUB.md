# Clube de Fas de POKéMON de Porto do Sal

## Objetivo

Localizar integralmente a superficie ativa do Clube de Fas de POKéMON de Porto do Sal e as seis recompensas visiveis ligadas ao local, preservando as regras de Contest, amizade e save herdadas de Emerald.

## Dialogos

`scripts/render_porto_sal_fan_club.py` cobre 22 blocos ativos em:

`data/maps/SlateportCity_PokemonFanClub/scripts.inc`

Inclui:

- apresentacao do presidente;
- interesse por POKéMON de CONCURSO;
- avaliacao das cinco condicoes;
- recomendacao de POKéBLOCKS;
- recompensa e BOLSA cheia;
- explicacao das cinco fitas;
- estado em que todas as fitas ja foram recebidas;
- avaliacao de amizade;
- entrega do SINO CALMANTE;
- orientacao sobre confianca/amizade;
- NPC sobre desmaios;
- NPC sobre PROTEIN;
- falas/sons de SKITTY, ZIGZAGOON e AZUMARILL.

## Recompensas visiveis

Os IDs internos permanecem os mesmos, mas os nomes exibidos passam a ser:

| ID interno | Nome visivel |
|---|---|
| `ITEM_RED_SCARF` | FITA VERMELHA |
| `ITEM_BLUE_SCARF` | FITA AZUL |
| `ITEM_PINK_SCARF` | FITA ROSA |
| `ITEM_GREEN_SCARF` | FITA VERDE |
| `ITEM_YELLOW_SCARF` | FITA AMARELA |
| `ITEM_SOOTHE_BELL` | SINO CALMANTE |

As descricoes da Bolsa tambem sao localizadas.

As categorias das fitas sao apresentadas como:

- ESTILO;
- BELEZA;
- FOFURA;
- ESPERTEZA;
- RESISTENCIA.

## Preservado

Continuam intactos:

- `VAR_SLATEPORT_FAN_CLUB_STATE`;
- `FLAG_MET_SLATEPORT_FANCLUB_CHAIRMAN`;
- `FLAG_ENTERED_CONTEST`;
- `FLAG_RECEIVED_RED_SCARF`;
- `FLAG_RECEIVED_BLUE_SCARF`;
- `FLAG_RECEIVED_PINK_SCARF`;
- `FLAG_RECEIVED_GREEN_SCARF`;
- `FLAG_RECEIVED_YELLOW_SCARF`;
- `FLAG_RECEIVED_SOOTHE_BELL`;
- `CheckLeadMonCool`;
- `CheckLeadMonBeauty`;
- `CheckLeadMonCute`;
- `CheckLeadMonSmart`;
- `CheckLeadMonTough`;
- `GetLeadMonFriendshipScore`;
- limiar `FRIENDSHIP_150_TO_199`;
- `ITEM_*` internos;
- `HOLD_EFFECT_FRIENDSHIP_UP` do Soothe Bell;
- check de espaco na Bolsa;
- cries dos POKéMON;
- vars, flags e formato de save.

Nenhuma regra de obtencao foi alterada.

## Seguranca

O renderer exige:

- cada bloco de dialogo exatamente uma vez;
- cada nome de item legado exatamente uma vez;
- cada label de descricao exatamente uma vez;
- maximo de duas linhas por pagina de dialogo;
- maximo de 32 caracteres por segmento visivel;
- identidade estrutural do mapa depois de mascarar `.string`;
- aplicacao transacional durante o build.

`src/data/items.h` e `src/data/text/item_descriptions.h` continuam como fontes-base e sao restaurados ao fim do build.

## CI e auditoria

O CI executa:

```sh
python3 scripts/render_porto_sal_fan_club.py --check
```

O auditor renderizado aplica o Clube sobre as camadas anteriores de itens antes de classificar residuos. Assim `RED SCARF`, `SOOTHE BELL` e os dialogos vanilla nao contam como superficie final quando o build ja os substitui.

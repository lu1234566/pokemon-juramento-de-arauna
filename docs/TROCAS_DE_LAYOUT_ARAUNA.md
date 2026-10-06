# Trocas de layout por script nos mapas Arauna

Alguns mapas trocam de layout em tempo de jogo com `setmaplayoutindex`.
Depois da conversão para a Arauna, esses scripts continuavam apontando para
as variantes vanilla, que usam os bancos de Hoenn. Quando o evento disparava,
o mapa voltava ao visual original:

| Mapa | Evento | Antes | Agora |
| --- | --- | --- | --- |
| Rota 111 | Mirage Tower oculta (quase sempre) | `LAYOUT_ROUTE111_NO_MIRAGE_TOWER` | `LAYOUT_ARAUNA_ROUTE111_THREE_ACTS_NO_TOWER_V1` |
| Rota 130 | Ilha Miragem presente / ausente | `LAYOUT_ROUTE130_MIRAGE_ISLAND` / `LAYOUT_ROUTE130` | `LAYOUT_ARAUNA_ROUTE130_CROSS_CURRENTS_MIRAGE_ISLAND_V1` / `LAYOUT_ARAUNA_ROUTE130_CROSS_CURRENTS_V1` |
| Rota 131 | Sky Pillar revelado | `LAYOUT_ROUTE131_SKY_PILLAR` | `LAYOUT_ARAUNA_ROUTE131_LAST_FREE_SEA_SKY_PILLAR_V1` |
| Shoal Cave, entrada e sala interna | maré alta / baixa | `LAYOUT_SHOAL_CAVE_*_TIDE_*` | `LAYOUT_ARAUNA_MARE_HIGHTIDE*_V1` / `LAYOUT_ARAUNA_MARE_LOWTIDE*_V1` |
| Sky Pillar 1F–Topo | piso limpo | `LAYOUT_SKY_PILLAR_*_CLEAN` | `LAYOUT_ARAUNA_TORRE_*_CLEAN_V1` |

As trocas de Littleroot (`*_CIRO`) e de Sootopolis/Birch já ficavam entre
layouts do mesmo banco e não mudaram.

## Como as variantes foram feitas

- As marés da Shoal Cave já tinham variantes Arauna, com bancos de maré alta
  próprios. Elas só não estavam ligadas aos scripts. O `map.bin` delas é
  idêntico byte a byte ao que o transplante abaixo produz.
- As outras nove variantes são geradas por
  `tools/arauna_maps/variantes_troca_layout.py`. A ferramenta parte do layout
  Arauna atual e copia da variante vanilla, com ID, colisão e elevação, as
  células que o vanilla muda entre a base e a variante:
  - Rota 111: 18 células.
  - Rota 130: 955 células.
  - Rota 131: 336 células.
  - Sky Pillar: de 15 a 155 células por andar.
- Nessas áreas, o layout Arauna repete os IDs da base vanilla. Os bancos
  Arauna dão aos IDs transplantados a mesma conduta da variante vanilla: 0
  divergências de comportamento (água, grama, portas, buracos, colisão).
- Os renders conferidos mostram a arte Arauna: a torre some do deserto, a
  Ilha Miragem e o Sky Pillar aparecem nas paletas do mar Arauna, e as
  rachaduras e pedras saem dos andares do Sky Pillar limpo.
- Os layouts novos entram no fim de `layouts.json`, sem renumerar os
  existentes. Cada um usa os bancos e a borda do layout Arauna de origem.

`python3 tools/arauna_maps/variantes_troca_layout.py --verificar` confere se
os arquivos estão atualizados e se não há divergência de comportamento.
Se um layout Arauna de origem mudar, a ferramenta deve ser rodada de novo.

## Verificação

- Na Rota 111, as quatro travessias a pé (para e a partir das Rotas 112 e
  113) ficam idênticas ao carregamento direto. Antes, a chegada vinda das
  Rotas 112 e 113 diferia em 44 tiles e 92 cores, porque a troca caía no
  layout vanilla.
- Os demais eventos dependem de estado de história (Sky Pillar, Rayquaza)
  ou de sorteio (Ilha Miragem). Foram conferidos nos renders estáticos.

# Dungeons — 71 mapas (V1)

Instalação do lote `Pokemon_Juramento_de_Arauna_Dungeons_71_Mapas_V1`: 13
pacotes, 71 mapas, 33 tilesets novos (primários e secundários). Cada pacote
tem o seu documento próprio em `docs/*_V1.md` e a revisão em `review/*_v1/`.

| Pacote | Doc |
|---|---|
| Arquivo Central Horizonte | `ARQUIVO_CENTRAL_V1.md` |
| Esconderijo da Serra | `ESCONDERIJO_SERRA_V1.md` |
| Galerias da Serra | `GALERIAS_SERRA_V1.md` |
| Gruta da Maré | `GRUTA_DA_MARE_V1.md` |
| Gruta da Origem | `GRUTA_DA_ORIGEM_V1.md` |
| Gruta das Vozes | `GRUTA_DAS_VOZES_V1.md` |
| Memorial dos Nomes | `MEMORIAL_NOMES_V1.md` |
| Navio Perdido | `NAVIO_PERDIDO_V1.md` |
| Ruínas da Queda | `RUINAS_DA_QUEDA_V1.md` |
| Serra da Cinza | `SERRA_CINZA_V1.md` |
| Torre do Juramento | `TORRE_JURAMENTO_V1.md` |
| Trilha de Brasa | `TRILHA_DE_BRASA_V1.md` |
| Usina Velha | `USINA_VELHA_V1.md` |

## O que muda

Só o visual. Nos 71 `map.json` o único campo alterado é `layout`; scripts,
eventos, warps, NPCs, encontros e clima ficam como estavam. Os layouts novos
têm o mesmo tamanho dos antigos e, comparados tile a tile, repetem exatamente
a colisão, a elevação e o comportamento de metatile (warps, buracos, piso
rachado, água, saltos, escadas, grama de encontro). O único callback de
animação usado é `InitTilesetAnim_General`.

## Correções feitas na instalação

- **`MtPyre_Exterior`**: o pacote do Memorial partia de um `map.json` antigo
  sem o `"weather": "WEATHER_SHADE"` do repo. Ficou o layout do pacote
  (`LAYOUT_ARAUNA_MEMORIAL_EXTERIOR_V1`) com o clima do repo.
- **Declarações de tileset descartadas**: o `declaration_block()` dos
  instaladores corta o bloco na primeira declaração cujo nome não começa com
  o da primeira, então, numa sequência de tilesets contíguos do mesmo
  pacote, só o primeiro entrava. Doze tilesets ficaram referenciados em
  `layouts.json` sem `gTileset_*`; as 60 declarações que faltavam foram
  copiadas dos arquivos do próprio pacote, na ordem deles.
- **Unidade de tradução errada**: os pacotes punham as `gTilesetTiles_*` e
  `gTilesetPalettes_*` dos 8 primários novos em `src/graphics.c`, mas quem
  as usa é `src/data/tilesets/headers.h`, incluído só por `src/tilesets.c`.
  Foram para `src/data/tilesets/graphics.h`; `src/graphics.c` não muda.

## Verificação

- `make MODERN=1`: ok.
- `check_arauna_static.sh` 189/189, `check_overworld_palette_capacity.py`
  95/95, `audit_visible_residue.py` 0 candidatos.
- Emulador: um mapa por pacote (o maior de cada), andando nas quatro
  direções: todos carregam, renderizam com a arte nova e sem tile corrompido;
  as paradas de tela observadas eram batalhas selvagens.

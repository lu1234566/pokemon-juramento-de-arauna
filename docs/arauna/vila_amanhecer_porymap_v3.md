# Vila Amanhecer — Porymap V3

Este lote redesenha apenas `data/layouts/LittlerootTown/map.bin` usando exclusivamente metatiles já existentes em `gTileset_General` + `gTileset_Petalburg`.

Objetivos visuais:
- entrada norte mais legível;
- caminho principal de terra ligando a entrada, as duas casas e o laboratório;
- praça central mais definida;
- ramal até a placa da vila;
- pequenos jardins/florais para quebrar o chão verde uniforme;
- preservação das construções e da moldura florestal atuais.

Preservação técnica:
- `MAP_LITTLEROOT_TOWN`, `LAYOUT_LITTLEROOT_TOWN`, warps, eventos, flags, scripts e conexões intactos;
- tilesets continuam `gTileset_General` e `gTileset_Petalburg`;
- `map.bin` permanece 20×20, 800 bytes;
- portas/placas existentes não são substituídas;
- nenhuma GitHub Action necessária para este lote de layout.

Coordenadas funcionais preservadas:
- casa: warp `(5, 8)`;
- segunda casa: warp `(14, 8)`;
- laboratório: warp `(7, 16)`;
- entrada/trigger norte: `(10–11, 1–2)`;
- placas: `(7, 8)`, `(12, 8)`, `(15, 13)`, `(6, 17)`.

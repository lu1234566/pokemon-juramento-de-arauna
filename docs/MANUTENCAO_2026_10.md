# Manutenção depois do ciclo de cavernas, Dive e Safari

Rodada feita sobre `a08835a98f`, depois do Safari V1.

## 1. Varredura de bugs no jogo todo

### Mapas

Para cada um dos 528 mapas, as ferramentas carregam tiles, paletas,
metatiles e atributos como a ROM declara (`headers.h`, `graphics.h`,
`metatiles.h`) e conferem:

- IDs da grade, da borda e das grades visuais de câmera fora do tamanho do
  banco;
- metatiles com tile ausente, que aparecem em magenta no render;
- bordas totalmente transparentes, que aparecem pretas, em mapas externos
  (rota, cidade, vila, mar e fundo do mar).

Resultado: um único problema, a borda de Petalburg. O `border.bin` usava o
`0x01D`, transparente no banco atual, e o norte e o sul da cidade ficavam
pretos. A borda agora usa a moita de capim `0x211`, a mesma que fecha o
contorno da cidade, com os mesmos bits de colisão e elevação.

### Metatiles colocados por scripts

São 255 casos, comparados com o tileset original do Emerald pelo prefixo da
constante. As correções desta varredura, Altering e Space Center de
Mossdeep, já estão em `CAVERNAS_CHECKPOINT_03C_03B_V11.md`. Sobram dez
diferenças: tipo de camada em Littleroot e na Rota 114, e as peças da base
da Mirage Tower, tratadas por alias no Dive 04.

### Portas animadas

A animação de porta é escolhida pelo número do metatile, sem olhar o banco.
Uma porta redesenhada num banco privado pode abrir com a animação de outra.
Nas 111 portas com warp, o primeiro quadro da animação, nas paletas do banco
do mapa, foi comparado com o desenho parado. Numa porta correta a diferença
média fica em torno de 20.

- **Oldale, Centro Pokémon e Loja (d≈78):** abriam com a porta de vidro azul
  de Hoenn sobre a porta de madeira. O `field_door.c` só usava a animação de
  madeira com o primário do Início, e Oldale passou a ter primário próprio
  no Sul/Pampa. A condição agora inclui
  `gTileset_AraunaBorderOldaleTownBaseUivoV1`. Com a animação de madeira, a
  diferença cai para 12,5, conferida quadro a quadro no mGBA.
- **Cable Club, 2º andar dos Centros Pokémon (0x264):** o desenho parado não
  é de porta. Essas portas só se abrem em jogo por cabo; ficam registradas.
- **Casa dos trabalhadores da Rota 116 (d≈54):** a porta vermelha da Uivo
  abre com a animação General, de cores um pouco diferentes. Fica
  registrada.

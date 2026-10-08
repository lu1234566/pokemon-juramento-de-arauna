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

## 2. Saves reais

Uma ROM com harness leva o jogador ao ponto, abre o menu e salva pelo
"Save" de verdade. O `.sav` do mGBA é então carregado na ROM normal, sem
harness, e o jogo continua pela tela de título com "Continue". Depois do
continue, o layout ativo é lido da RAM (`gMapHeader.mapLayoutId`).

- **Mesma versão.** 12 saves continuam no mapa e na posição certos, com a
  mesma imagem de antes de salvar, a não ser pelas animações e pelos NPCs
  que se mexem. Os 12 mapas são:
  - cavernas com grade de câmera: Victory Road, Terra Cave, Altering,
    Artisan e Sealed Chamber;
  - Dive na Rota 124 e Safari Sul;
  - Rota 111 com a Mirage Tower;
  - Rustboro e Rota 116 (layouts novos);
  - Space Center de Mossdeep e Littleroot.
- **Save de versão antiga.** Foram feitos 13 saves na versão `591aeb2497`,
  anterior ao Sul/Pampa, ao Uivo e às cavernas 03, e continuados na versão
  atual. Todos abrem no mapa e na posição certos:
  - Rotas 102, 103 e 104, Rustboro e Rotas 115 e 116 migram para os layouts
    novos (`…_SUL_PAMPA_V1`, `…_UIVO_…`);
  - Oldale, Rota 111, Terra Cave, Victory Road, Rota 124 submersa, Safari e
    Littleroot mantêm o layout e ganham a arte nova;
  - a imagem é a mesma do carregamento direto na versão atual.

## 3. Bancos sem uso tirados da ROM

Dos 409 tilesets declarados, 98 não são usados por nenhum layout: 85 da
Arauna e 13 de Hoenn. Saíram da ROM os 26 que mais nada cita: nem o código,
nem as ferramentas do autor em `tools/`, nem os registros em `review/`.
Com eles saíram os 104 arrays de tiles, paletas, metatiles e atributos que
só eles usavam. São bancos regionais e de interface de versões antigas das
rotas:

- Serra do Uivo, Porto do Sal, Encruzilhada, Vale do Silêncio, Missões do
  Céu V2, Mangue, Ciclovia, Eixo Interior, Pedra Escura, Vale Transição,
  Costa Serrana, Campos Cultivados, Rio Fronteira, Arquipélago, Águas do
  M'Boi, Recife Mergulho;
- 111 Regions, 112 Casa da Cinza Interface V2, 114 Campo Interface V4,
  115 Arrebentação, 117 Lavoura, 124 Missões Interface V3, 126 Estruturas,
  128 Recife;
- Casa da Cinza Primary V2 e Cumulative V2.

Só mudaram `src/data/tilesets/headers.h`, `graphics.h` e `metatiles.h`.
Os arquivos de dados em `data/tilesets/` continuam no repositório.

Ficaram 59 bancos da Arauna sem uso por layout, cerca de 0,86 MB:

- **54 citados pelo seletor de bordas** (`arauna_border_visuals.c`,
  `arauna_border_priority_v2.h`), **pelo Cut** (`fldeff_cut.c`) **ou pela
  ponte de validação do autor** (`tools/arauna_maps/host_visual_selector_v2.py`
  com `review/*/borders_build.json`). Esses três arquivos de código são
  protegidos por hash nos contratos 03C, Dive 04 e Safari 05. A ponte
  compila o seletor com esses nomes, e é usada pelos validadores de 03A,
  Dive 04 e Safari 05. Tirar esses bancos quebra esses validadores e a
  pré-checagem dos próximos instaladores.
- **5 citados por ferramentas de build ou registros de pacote:** 03B
  original (3), recepção antiga do Safari e 118 Mata Úmida.

A remoção completa (85 bancos, 1,23 MB) foi montada e testada: 744 layouts
idênticos e fotos idênticas sem sprites e sem clima. Ela fica para o fim
do projeto, quando não vierem mais pacotes, junto com a atualização da
ponte do autor.

Os 13 tilesets de Hoenn sem uso ficaram, para não afastar o código do
original.

Verificação:

- **Dados de cada layout.** Os 744 layouts da ROM nova foram comparados
  com os da anterior: blockdata, borda, tiles, paletas, metatiles,
  atributos e callback de cada tileset. Todos idênticos.
- **Fotos.** 20 pontos espalhados pelo jogo, fotografados nas duas ROMs
  sem sprites e sem clima, saíram iguais pixel a pixel.
- **Gates.** Todos passam.
- **Pontes do autor.** A ponte do seletor compila nas três versões: host,
  Safari 05 e Dive 04.
- **Validador antigo.** `validate_border_visuals_119_118.py` acusa
  diferença de cache na Rota 119. Ele já falha igual no código sem esta
  mudança, porque a Rota 119 passou para os bancos Uivo depois dele.

Resultado: a ROM passou de 19.408.140 para 18.982.036 bytes, 426 KB a
menos (de 57,8% para 56,6%).

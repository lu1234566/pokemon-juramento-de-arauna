# Fundos de batalha nativos

47 cenários próprios: 34 rotas, oito ginásios, quatro salas da Elite e a sala
da campeã. Cada um foi desenhado para a câmera de batalha, com a base do
adversário perto de y=64, a base do jogador perto de y=108 e a interface
começando em y=112.

## O que está versionado

Em `graphics/battle_environment/arauna/<id>/`:

| Arquivo | O que é |
|---|---|
| `scene.png` | A cena como se vê, 240×128, indexada, um banco de paleta por tile de 8×8. É o arquivo que se edita. |
| `tiles.png` | O atlas de tiles de 8×8. As cores que aparecem nele são as do primeiro banco; a cor final de cada tile depende do mapa. |
| `map.bin` | O tilemap de 512×256, com índice, espelhamento e banco de paleta por tile. |
| `palette.pal` | Paleta JASC de 48 cores: três bancos de 16, carregados nos slots 2–4. |

E em `common/`: `entry.png` e `entry_map.bin`, que são a camada de entrada —
um tile vazio e um tilemap zerado. Ela existe para deixar transparente a
camada decorativa de grama/água da vanilla, cujas cores não teriam nada a ver
com estes cenários, sem perder a abertura da janela nem o deslize do treinador.

**Não há binário compilado versionado.** `.4bpp`, `.gbapal` e `.lz` são produto
de build: o `.gitignore` ignora os três e o alvo `clean-assets` do Makefile os
apaga em toda a árvore. O pacote original trazia esses 237 arquivos prontos, o
que compilava na máquina de quem instalou e teria falhado em qualquer clone
novo — e sumido no primeiro `make clean`. A declaração em
`src/data/arauna_battle_backgrounds.h` usa `INCGFX`, como o resto do
repositório, e o compilador refaz os fluxos a cada build. A ROM resultante é
byte a byte a mesma.

## Como o jogo escolhe

`GetAraunaBattleBackground()`, no mesmo header, responde antes de tudo o que o
`src/battle_bg.c` faria, e devolve `NULL` quando nenhum cenário se aplica —
nesse caso o motor segue pelo caminho original. A ordem é:

1. Link, gravações, instalações de batalha, base secreta, parceiro e as cenas
   especiais de Groudon, Kyogre e Rayquaza têm precedência e **não** recebem
   cenário novo.
2. Batalha de treinador: os oito líderes, com as cinco equipes de revanche cada,
   os quatro da Elite e a campeã têm cenário próprio.
3. Caso contrário, vale o mapa. Cada rota exige o terreno compatível com o
   concept: uma rota terrestre devolve `NULL` em batalha de Surf em vez de
   forçar terra firme sobre água, e vice-versa. A Rota 111 só usa o dela na
   areia.

## O que ainda não tem cenário

As 19 variações de terreno do levantamento. Surf numa rota cujo concept é
terrestre, trechos fora do deserto na 111, ilhotas que não combinam com os
concepts marítimos e tudo que é submerso continuam com o ambiente original.
Isto é, os 47 cenários principais estão prontos; os fundos genéricos não
desapareceram de todos os terrenos.

## Reexportar

Edite `scene.png` mantendo o modo indexado e um único banco por tile. Depois:

```bash
python3 tools/arauna/battle_backgrounds/export.py     # refaz as fontes
python3 tools/arauna/battle_backgrounds/validate.py   # 47 cenas + 176 asserções
```

O `export.py` grava só o que é versionado. O `validate.py` precisa de numpy e
Pillow; ele refaz os três fluxos nativos com o `gbagfx` do próprio repositório,
confere a ida e volta do LZ77, os limites de VRAM e os bancos de paleta,
redesenha cada cena a partir dos bytes e compara pixel a pixel com o
`scene.png`, e então compila o seletor de verdade com os globais dublados e
roda 176 asserções sobre ele.

## Conferido

- 47 cenas reconstruídas dos bytes e idênticas ao `scene.png`; nenhuma passa de
  512 tiles.
- 176 asserções sobre o seletor real: rotas, terrenos incompatíveis, líderes,
  as cinco revanches de cada um, Liga e a precedência dos modos especiais.
- ROM de 14.604.476 bytes, contra 13.954.052 antes: 650.424 bytes a mais, 43,5%
  dos 32 MB. EWRAM e IWRAM sem mudança.
- Cinco batalhas de verdade fotografadas no emulador, em
  `docs/arauna/fundos/`: selvagem na Rota 101, Dalva, a campeã Amália, Clara e
  a Rota 111 na areia.

Ninguém jogou a campanha inteira com eles, e as animações de golpe não foram
varridas uma a uma.

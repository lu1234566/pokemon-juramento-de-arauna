# Integração seletiva — 42 mapas do checkpoint 71

Origem: `Arauna_Preparacao_42_Mapas_2026_10_05` (extração do checkpoint
`979fb6c1b6` feita pelo autor). O restaurador do checkpoint não foi usado: ele
desfaria 67 commits deste branch. O patch foi gerado pelo
`planejar_integracao.py` do autor contra o HEAD atual, que preserva scripts,
encontros, clima, conexões, flags e NPCs, e só migra coordenadas de eventos
reconhecidas.

## O que entrou

- 27 rotas redesenhadas: 104, 105, 108–118, 121–134. Dimensões e eventos
  iguais aos atuais; muda só o layout.
- Exteriores: Lavaridge (Casa da Cinza V2), Fallarbor (Campo das Cinzas V3,
  20×20 → 32×25, eventos reposicionados, ponto de cura acompanha o Centro) e
  Mossdeep V2 → V3 (casado com as rotas 124, 125 e 127 por tilesets de
  "interface").
- Interiores: Oldale (5), Dewford (5), ginásio e Game Corner de Mossdeep (3).
- 56 tilesets Arauna novos.

## Correções na integração

- O validador do autor recusava `LAYOUT_UNUSED_OUTDOOR_AREA` (vanilla, sem
  mapa, secundário `0`) e bloqueava por bordas incompatíveis; as bordas já
  existiam no jogo atual (18 conexões antes, 29 depois) e são tratadas à parte.
- Os gráficos dos 14 primários novos iam para `src/graphics.c`; foram para
  `src/data/tilesets/graphics.h`, a unidade de tradução que os usa.
- Seis `tiles.png` vieram em RGB (rampa de cinza) e o `gbagfx` só aceita PNG
  indexado: convertidos sem mudar pixels, com o índice 0 = branco do projeto.
- `AraunaArcoCosteiro`, `AraunaMangue` e `AraunaMataEspera` tinham arte própria
  nos tiles 482–487, que a animação `General` sobrescreve com a espuma de
  Emerald: a arte foi para slots vagos e os metatiles Arauna foram
  reapontados (os secundários de Emerald continuam com a espuma animada).
- `AraunaArcoCosteiro` paleta 4, índice 4 era magenta de preenchimento e é
  usado pelos quadros da espuma: recebeu o tom de água da própria paleta.
- Route126: 52 pontos de mergulho novos caíam sobre rocha no mapa submarino;
  ganharam clones dos metatiles com `MB_OCEAN_WATER` (mesmo desenho, sem
  mergulho).

## Conferência

- Varredura de todos os layouts: nenhuma paleta 13–15, metatile ou tile fora
  do tileset (fora as bases secretas originais).
- Eventos: nenhum warp fora de tile de warp, NPC em parede ou gatilho
  bloqueado; mergulho e emersão consistentes com os mapas submarinos.
- Travessias de borda iguais às anteriores; Fallarbor ↔ rotas 113/114 com
  mais passagens (9→11, 11→13), travessia real feita no emulador.
- Emulador: 27 amostras (rotas, cidades e interiores) sem travamento.
- Mudanças de jogo vindas do autor: grama alta nova na Route104, correntezas
  nas rotas 130/131, faixa de terra na Route109; interiores de Oldale e
  Dewford perdem estante, mapa da região e TV como os do Vale.

## Bordas entre mapas vizinhos

O GBA desenha a faixa do mapa vizinho (até 7 células) com os tilesets do
mapa atual. Quando o mesmo ID de metatile tem outro desenho no tileset do
vizinho, aparece lixo na borda até o jogador cruzar. O jogo já tinha isso em
18 conexões antes desta integração (Pacifidlog com as rotas 131/132, rotas
112/113, Rustboro/116 e outras) e ficaria com 29 depois dela.

`tools/arauna_maps/corrige_bordas_conexoes.py` (simula sem argumento; grava
com `--aplicar`; precisa de `PREP` apontando para os scripts do pacote de
preparação do autor) cria, para cada célula de borda com problema, um
metatile novo com o mesmo ID nos dois lados: no tileset do dono é clone
exato; nos tilesets de quem enxerga a borda, os tiles e as cores são
transplantados para slots livres (sem tocar em slots de animação). Quem já
via a célula bem recebe um clone do próprio metatile. IDs que aparecem em
bordas de outros vizinhos não são reaproveitados.

Resultado: 169 dos 173 grupos de células corrigidos (os 4 restantes, Route118
vista de Fortree/Mata do Meio, ficam como estavam porque o tileset não tem
tiles livres). Por critério de cor, 29 conexões melhoraram e nenhuma piorou
(Pacifidlog vista da Route132: 286 → 31 células erradas; Route131: 244 → 13;
rotas 111/112/113: zeradas). O visual próprio dos 51 layouts que usam os
tilesets alterados é idêntico pixel a pixel, e colisão e comportamento das
19 grades alteradas são idênticos. As diferenças restantes são de paleta
entre biomas (o mesmo desenho com o tom do mapa atual), não lixo de tile.

## Observação de arte

Os pisos de madeira dos interiores de Oldale (Vila da Passagem) usam o índice
0 na camada de baixo, que o GBA mostra como o fundo preto: as tábuas aparecem
com vãos pretos largos. É assim também no preview do autor; ficou como está.

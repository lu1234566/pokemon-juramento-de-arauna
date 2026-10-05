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

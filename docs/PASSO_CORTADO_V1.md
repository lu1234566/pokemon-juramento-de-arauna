# Passo Cortado — descida vulcânica V1

A direção vem da Master Map Design Bible, página 27: descida exterior em
zigue-zague, patamares, ledges geológicos, rocha escura e cinza. Não há prancha
dedicada ao Passo Cortado no pacote de concepts recuperado. A prancha da Serra
da Cinza serve apenas como referência de materiais do mesmo conjunto vulcânico.

O mapa recebeu encostas em carvão e pedra violeta, árvores cobertas de cinza
em tons frios e 25 detalhes planos de fissuras e fragmentos. A vegetação da
base permanece verde para marcar a saída da região vulcânica. São dois tilesets
próprios e dois metatiles adicionais, em arte nativa de 8×8/16×16 pixels.

A composição e as dimensões técnicas de 30×46 foram mantidas; a Bíblia propõe
32×30, portanto esta rodada adapta os materiais sem reconstruir o percurso.
Os cinco warps, sete objetos, dez eventos de coordenada, dois itens ocultos,
saltos, caminhos de bicicleta, grama com cinza, bordas e colisões permanecem
iguais. As duas células alteradas pela cena de abertura do esconderijo e os
scripts da cena foram preservados. O callback de animação General foi mantido.

O pacote inclui instalador com backup, verificação de conflitos, reprodução
dos assets e validação nativa. Instalação isolada, reaplicação e conversão de
mapa são verificadas pelo empacotador. Compilação de ROM e teste em emulador
permanecem pendentes; a comparação foi renderizada dos dados nativos do mapa.

## Instalação no repositório

- `map.json` muda só no `layout`; colisão, elevação e comportamento repetem
  o layout antigo tile a tile.
- Os metatiles trocados em jogo mantêm desenho e comportamento: a parede e a
  entrada do esconderijo (cena da abertura), a grama com cinza que vira grama
  comum ao ser pisada (`field_tasks.c`) e o campo que o Corte deixa
  (`fldeff_cut.c`).
- O primário novo mantém intactos os slots de tile que a animação `General`
  sobrescreve; nenhum metatile usado no mapa os referencia. O secundário não
  tem animação (o do Lavaridge animava vapor e lava, ausentes aqui).
- Build ARM, gates e emulador verificados; no emulador, a cinza sai da grama
  ao passar.

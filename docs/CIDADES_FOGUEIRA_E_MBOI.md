# Casa da Fogueira e Águas de M'Boi — os exteriores

Dois exteriores nativos, instalados dos pacotes V2 sobre a base
`979fb6c1b6731561f3c993efd6045a9bbf096c54`.

| | Slot herdado | Tamanho | Banco de tiles |
|---|---|---|---|
| Casa da Fogueira | PacifidlogTown | 34 × 40 (era 20 × 40) | `gTileset_AraunaCasaFogueiraV2` |
| Águas de M'Boi | SootopolisCity | 48 × 50 (era 60 × 60) | `gTileset_AraunaAguasMBoiV2` |

A Casa da Fogueira é o assentamento sobre água: plataformas irregulares de
madeira escura ligadas por pontes, casa comunal com lareira, círculo de pedras
com a fogueira, casas sobre estacas e ancoradouros. As Águas de M'Boi são a
comunidade alagada: ilhas de pedra e capim, palafitas de telhado inclinado,
pontes baixas, a Casa Dupla e a entrada do arquivo. O mapa da crise divide o
mesmo exterior e conserva os 24 metatiles e as 96 posições de tiles animados
da cena original.

## O que precisou de mescla

Os dois instaladores comparam o checkout inteiro com a base deles e param no
primeiro arquivo diferente. Desde aquele commit a Arauna escreveu bastante, e
três categorias de divergência apareceram. Nenhuma foi ignorada no escuro:
cada dispensa foi verificada antes de valer, e o script que fez isso está em
`docs/` apenas descrito — ele não entra no repositório porque é de uso único.

**Seis `scripts.inc` de interiores** (cinco de Sootopolis, um de Pacifidlog)
diferiam da base. Conferido linha a linha com `difflib`: a diferença é
inteiramente em linhas `.string`, ou seja, o texto que a Arauna reescreveu.
Nenhum desses arquivos está no conjunto de escrita dos pacotes — eles só
conferem o hash. Dispensados.

**As tabelas de encontros** de Sootopolis e de Pacifidlog. Na base dos pacotes
elas ainda são o marcador antigo — em Sootopolis, cinco linhas de RHYDON — e
hoje são as tabelas de verdade, instaladas pelo pacote de encontros. Os
instaladores só leem esse arquivo. Dispensados.

**Dois conflitos de escrita de verdade**, resolvidos e não descartados:

- `data/maps/SootopolisCity/scripts.inc`: a Arauna mudou 163 linhas, todas
  `.string`; o pacote mudou 378, nenhuma `.string` — são as coordenadas dos
  `setmetatile` das portas, que se moveram com a geometria nova. Mesclado com
  `git merge-file`. Sobrou um trecho em conflito, no fim do arquivo, onde os
  dois lados mexeram: de um lado a fala da Amália em inglês, do outro a mesma
  fala ainda em português mais um bloco novo com duas rotas de aproximação à
  Caverna da Origem. Resolvido ficando com a fala em inglês e com o bloco
  novo. Conferido depois: o conjunto de rótulos do arquivo mesclado é
  exatamente o que o pacote espera, sem nenhum a mais nem a menos.
- `data/maps/PacifidlogTown/map.json`: a única diferença da Arauna sobre a
  base é `WEATHER_RAIN` → `WEATHER_SUNNY`, da passagem de clima por bioma. O
  pacote mexe só em coordenadas. O arquivo do pacote entrou e o clima da
  Arauna voltou por cima.

## Conferido em jogo

Quatro pontos de partida percorridos no emulador, 300 voltas cada, com
checagem de tela parada e do ponteiro do save a cada volta: centro e norte de
cada cidade. Nenhuma assinatura de travamento. As fotos estão em
`docs/arauna/cidades/`.

Renderizam corretos, com a paleta certa: a fogueira acesa no círculo de
pedras, a casa comunal, as pontes e a água na Casa da Fogueira; a Casa Dupla,
os caminhos de pedra, a chuva e a entrada da Caverna da Origem com o guarda
em frente nas Águas de M'Boi.

**As saídas laterais não foram atravessadas a pé porque exigem Surf** — as
duas cidades são cercadas de água, como os slots herdados. A aritmética das
conexões foi conferida à parte: Rota 132 à esquerda e Rota 131 à direita, as
três com altura 40 e deslocamento 0, recíprocas dos dois lados. A análise de
alcance do próprio pacote dá 1245 estados alcançáveis com Surf em cada lado.

## O que continua pendente

- O retorno do mergulho em Underwater_SootopolisCity não foi testado: exige
  Dive. O pacote afirma ter mantido a margem de enquadramento.
- O interior da casa comunal da Casa da Fogueira, o destino `House5`, ainda
  usa o interior herdado e espera adaptação narrativa própria.
- Ninguém jogou as duas cidades dentro da campanha, com os eventos na ordem.

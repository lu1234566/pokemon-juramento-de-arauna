# Sprites de overworld: por que os últimos não prestaram

Arte que fica bonita a 64×64 e some no jogo não é azar: é uma faixa numérica.
O Emerald desenha 126 NPCs dentro de uma faixa bem estreita, e o que o projeto
entregou até agora cai fora dela em dois eixos — cor e passo.

Este arquivo é a faixa medida, não uma opinião. Os números saem dos 94 sheets
da vanilla que o projeto ainda não tocou.

> **Atualização — lotes 01 e 02 instalados.** Quinze slots receberam arte nova.
> Os quatro eixos — cor, tons, passo e escala — estão dentro da faixa da
> vanilla pela primeira vez. Detalhe no fim do arquivo.

## O diagnóstico, em duas linhas

**A cor.** Os 32 personagens redesenhados têm saturação média 34. Os mesmos
personagens na vanilla tinham 43, e o elenco da vanilla vai de 29 a 69. O
elenco novo inteiro cabe entre 26 e 40 — todo mundo na mesma faixa de bege
acinzentado. De longe eles não se distinguem uns dos outros, e é por isso que
o mapa vira uma papa.

**O passo.** Em 23 sheets uma das poses de caminhada era cópia exata da pose
parada; o lote 01 corrigiu dez, faltam treze. O motor toca `pose A → parado → pose B → parado`; se a pose A é a
parada, o personagem fica imóvel em três quartos de cada passo e dá um
chute só. Dez desses sheets tinham a animação certa na vanilla e a perderam
na substituição.

Nenhum dos dois aparece olhando a folha de sprites. Os dois aparecem na hora
em que o NPC anda na sua frente.

## A faixa da vanilla

Medido no frame 0 (parado, virado para baixo) de 94 sheets.

| medida | p10 | mediana | p90 | o que é |
|---|---:|---:|---:|---|
| saturação média do corpo | 29 | **44** | 69 | quanto de cor o personagem tem |
| luminância média | 86 | 104 | 127 | quão claro ele é **no geral** |
| desvio de luminância | 62 | **73** | 87 | quanto ele varia por dentro |
| tons distintos | 11 | **13** | 15 | quantos degraus de sombra |
| altura do corpo | 19 | **20** | 21 | em pixels |
| largura do corpo | 7 | 14 | 16 | |
| topo do corpo (y) | 10 | 11 | 12 | onde a cabeça começa |
| preenchimento da caixa | 0,69 | 0,75 | 0,81 | quanto da bounding box é corpo |
| borda | 0,21 | 0,23 | 0,39 | fração de pixels na silhueta |

E o elenco redesenhado hoje:

| medida | faixa atual | faixa da vanilla |
|---|---|---|
| saturação | 26 – 40 | 29 – 69 |
| luminância média | 94 – 108 | 86 – 127 |
| desvio de luminância | 59 – 71 | 62 – 87 |
| tons distintos | 10 – 11 | 11 – 15 |

Altura, largura, âncora, preenchimento e borda estão certos. O que saiu da
faixa foi só cor e número de tons — e o passo.

## O que fazer com isso na próxima leva

1. **Saturação entre 40 e 65 na maioria.** Não é "colorir mais": é que um NPC
   da vanilla tem *uma* peça de roupa forte — camisa vermelha, vestido
   amarelo, macacão verde — e o resto neutro. O personagem é reconhecido por
   essa mancha. Sem ela, sobra silhueta bege.

2. **Deixe os personagens diferirem em brilho geral.** A vanilla espalha a
   luminância média de 86 a 127 entre personagens. Se todos saírem em 100, o
   mapa fica plano mesmo com cada um individualmente correto. Normalizar a
   exposição personagem a personagem é justamente o que causa isso — não faça.

3. **12 a 14 tons no corpo, não 10.** Um tom a mais em cada peça é o que dá
   volume no tamanho pequeno.

4. **Três poses por direção, de verdade.** Parado, pé esquerdo, pé direito.
   As duas de caminhada precisam diferir da parada *e* uma da outra. Se só
   houver uma pose de caminhada, a segunda não pode ser a parada repetida.

5. Altura do corpo 19–21 px, topo em y 10–12, largura até 16. Isso já está
   saindo certo — não mexa.

## O que o QC passou a checar

`tools/validate_arauna_character_assets.py` já verificava formato e ligação de
paleta. Agora também recusa uma pose de caminhada que seja cópia da parada.

Os 23 sheets que hoje têm esse defeito estão numa lista explícita dentro do
próprio arquivo (`KNOWN_DEAD_WALK_POSES`) para o gate continuar verde. Cada
linha dessa lista é uma promessa, não um perdão: **apague a linha quando
redesenhar o personagem**, e a partir daí o sheet é checado como qualquer
outro. Qualquer sheet novo já entra checado.

### Os treze que faltam

`prof_birch` (ANAHI), `team_aqua/archie`, `team_magma/maxie`,
`ciro/phase1_brendan`, `ciro/phase1_may`, `ciro/phase2`, `ciro/phase3`,
`dona_zila`, `elite_four/drake`, `elite_four/glacia`, `gym_leaders/flannery`,
`gym_leaders/roxanne`.

`hot_springs_old_woman` é da vanilla assim mesmo — não é problema do projeto.

## Os três que estão fora de escala — e o que isso causa

| sprite | corpo | topo (y) | onde | na vanilla era |
|---|---:|---:|---|---|
| `mom.png` | 25 px | 6 | 5 mapas, incluindo a primeira casa | 20 px, topo 11 |
| `link_receptionist.png` | 27 px | 5 | **10 mapas** — o balcão de link de todo CENTRO | 20 px, topo 11 |
| `dusclops.png` | 26 px | 6 | 1 mapa | 20 px, topo 11 |

Um NPC da vanilla começa a cabeça em y=11. Esses três começam em y=5 ou 6 —
seis pixels acima de todo o resto do elenco. Num frame de 32 px isso não é só
"alto demais": **a cabeça invade o tile de cima**, que é exatamente o sprite
sobreposto que apareceu na screenshot 5 da beta.

Nenhum dos três tem arte de substituição nos pacotes recebidos. A recepcionista
é a de maior exposição, porque está em dez mapas; a mãe é a mais visível,
porque aparece nos primeiros minutos. Trocar a arte da mãe exige antes lhe dar
paleta própria — hoje ela usa uma paleta genérica compartilhada com outros NPCs.

`union_room_nurse.png` também tem 27 px, mas é arquivo morto: nenhuma
declaração em `object_event_graphics.h` aponta para ele, e a vanilla nunca teve
esse arquivo. Não chega à ROM.

## Ao redesenhar, a âncora importa mais que a altura

O frame tem 32 px de altura e o pé fica na base. Se o corpo cresce, ele cresce
para cima e entra no tile de cima. Por isso a faixa é **corpo 19–21 px com o
topo em y=10–12**, e não "menos de 25". Duas medidas, não uma.


## O que o lote 01 resolveu

Quinze slots trocados em 13/09, a partir de `Arauna_Sprites_Nativos_Lote_01`.
O pacote foi gerado contra o commit `979fb6c1b6` e acertou os quinze destinos e
as quinze paletas exatamente como o manifesto os declara.

| medida | antes (15 slots) | lote 01 | faixa da vanilla |
|---|---|---|---|
| saturação | 21 – 47, med **33** | 35 – 60, med **47** | 29 – 69 |
| tons distintos | 9 – 12 | 12 – 15, med **15** | 11 – 15 |
| pose de caminhada morta | 10 dos 15 | **nenhuma** | — |
| altura do corpo | 21 (certo) | 20 – 29, med **24** | 19 – 21 |
| topo do corpo | y=11 (certo) | y=2 – 11, med **7** | y=10 – 12 |

Cor e animação entraram na faixa. A escala saiu dela: catorze dos quinze
ficaram mais altos do que estavam, e a altura extra sobe, porque o pé continua
na base do quadro. Maira chegou a 29 px com o topo em y=2 — nove pixels acima
da linha onde começa a cabeça de qualquer outro NPC. **Isso foi corrigido pelo
lote 02**, abaixo.

Vale registrar o tamanho real do desvio: das 126 folhas da vanilla, **112 têm
19 a 21 px** e as quatro que passam disso não são gente parada — são o
`quinty_plump`, as duas bicicletas e a pose de mergulho. Para um NPC humano de
pé, 19–21 px com o topo em y=10–12 não é recomendação, é o formato.

Na prática a leitura melhorou muito mesmo assim, e boa parte da altura extra é
cabelo e chapéu, não corpo. Mas a cabeça atravessando o tile de cima é o mesmo
artefato de `mom`, `link_receptionist` e `dusclops`. Se for refazer a escala,
o alvo é **cortar 3 a 8 px do topo**, não redimensionar a figura inteira.


## O lote 02 fechou a escala

Correção dos mesmos 19 personagens, entregue depois do `docs/FEEDBACK_LOTE_02.md`.
171 de 171 quadros com o topo em y=10 (Amaro em y=11, que já estava certo), pé
em y=30 e altura 21 px. Nenhum pixel visível acima de y=10.

Conferido contra o que o pacote afirma, e a afirmação se sustenta:

- Os 19 hashes SHA-256 do lote 01 gravados no `baseline.json` batem com os
  arquivos que estavam instalados, ou seja, a correção partiu exatamente do
  que estava no jogo.
- Da linha protegida para baixo (y=13 a y=16, individual por personagem) os
  pixels são **idênticos byte a byte** ao lote 01. O corpo não foi mexido.
- Acima dela todos mudaram, menos Amaro, declarado intocado e de fato intocado.
- Os 17 sprites de batalha e as 15 paletas são byte a byte os mesmos. Só as
  14 folhas de overworld aparecem como modificadas no git.

Não foi corte: o topo do cabelo não ficou chapado, foi redesenhado com menos
volume vertical.

### Estado final dos 15 slots

| medida | antes dos lotes | lote 01 | lote 02 | faixa da vanilla |
|---|---|---|---|---|
| saturação | 21 – 47, med 33 | 35 – 60, med 47 | 38 – 61, med **47** | 29 – 69 |
| tons distintos | 9 – 12 | 12 – 15 | 13 – 15, med **15** | 11 – 15 |
| pose de caminhada morta | 10 dos 15 | nenhuma | **nenhuma** | — |
| altura do corpo | 21 | 20 – 29, med 24 | **20 – 21** | 19 – 21 |
| topo do corpo | y=11 | y=2 – 11, med 7 | **y=10 – 11** | y=10 – 12 |

A distribuição de altura do elenco inteiro voltou a ser a da vanilla: p10=19,
mediana=20, p90=21.

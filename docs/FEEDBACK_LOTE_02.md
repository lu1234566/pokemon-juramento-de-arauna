> **ATENDIDO.** O lote 02 cumpriu a regra em 171 de 171 quadros e foi
> instalado. O lote 03 fechou a correção da Mãe do Ciro (seção 5, item 1) e
> as duas prioridades por exposição da seção 6 — a mãe do protagonista e a
> recepcionista de link. Este arquivo fica como registro do que foi pedido e
> do formato que os próximos lotes devem seguir: a seção 1 (*não mexa*)
> continua valendo, e continuam abertos o item 2 e o item 3 da seção 5 (que
> são decisões suas, não técnicas) e os personagens da seção 6.

# Feedback do lote 01 — o que mudar no lote 02

Lote 01 instalado, compilado e conferido no jogo. **Um defeito só, e é de
escala.** Todo o resto passou, inclusive as duas coisas que os lotes anteriores
erravam.

---

## 1. O que já está certo — não mexa

Isto foi medido nos 19 personagens, não é impressão. Se o lote 02 mudar
qualquer um destes itens, piora.

| item | estado no lote 01 |
|---|---|
| Formato PNG | indexado 4 bits, índice 0 transparente, ≤16 cores — 36/36 |
| Folha de caminhada | 144×32, nove quadros de 16×32 — 19/19 |
| Ordem dos quadros | `0` frente parada, `1` costas, `2` perfil esq., `3/4` passo frente, `5/6` passo costas, `7/8` passo perfil — correta |
| Paleta `.pal` | JASC 16 entradas, correspondência exata com o PNG — 19/19 |
| **Linha do pé** | **y=30 em todos os 9 quadros de todos os 19. Variação zero.** |
| Largura máxima | 12 a 15 px (limite 16) — todos dentro |
| **Saturação** | 35 a 60, mediana 47 (a vanilla vai de 29 a 69) — **corrigido** |
| **Tons distintos** | 12 a 15, mediana 15 (vanilla 11 a 15) — **corrigido** |
| **Poses de caminhada** | nenhuma é cópia da pose parada — **corrigido** |
| Sprites de batalha 64×64 | altura 60, base em y=61, largura 23 a 49. A vanilla usa altura 50–63, base 62, largura 30–53. **Dentro da faixa, nada a fazer.** |

Os três itens em negrito eram exatamente os defeitos dos lotes anteriores. O
lote 01 resolveu os três.

---

## 2. O defeito: o personagem não cabe na caixa

O quadro tem 32 linhas, de y=0 a y=31. Um NPC do Emerald ocupa **de y=10 a
y=30** — 21 linhas. Isso não é preferência: das 126 folhas da vanilla, 112 têm
19 a 21 px de corpo, e as quatro que passam disso não são gente de pé (são o
boneco gigante `quinty_plump`, as duas bicicletas e a pose de mergulho).

O pé já está certo em todos: **linha y=30**. O que sobra, sobra **para cima**.

> **Regra do lote 02: nenhum pixel visível acima da linha y=10.**
> Corpo de 19 a 21 px de altura, ocupando de y=10 a y=30.

### Por que isso importa no jogo

O quadro de 32 px é mais alto que o tile de 16 px onde o personagem está. O que
passa de y=10 é desenhado **por cima do tile de cima** — na prática a cabeça
invade o cenário ou o NPC de trás. É o mesmo artefato que já existe com a mãe
do protagonista e a recepcionista de link, e que apareceu numa screenshot da
beta como "sprite sobreposto".

### Onde está o excesso

Em todos os casos é **volume de cabelo e chapéu**, não corpo. O corpo abaixo do
pescoço está na proporção certa.

**Não corte o topo.** Cortar deixa o cabelo com a ponta chapada. O certo é
**redesenhar o cabelo/chapéu com menos volume vertical**, mantendo o corpo onde
está.

---

## 3. Quanto tirar, por personagem

| personagem | topo atual | altura | tirar |
|---|---:|---:|---:|
| maira | y=2 | 29 px | **−8 px** |
| jaci | y=3 | 28 px | **−7 px** |
| admin_arquivo | y=4 | 27 px | **−6 px** |
| horizonte_f | y=4 | 27 px | **−6 px** |
| breno | y=6 | 25 px | **−4 px** |
| horizonte_m | y=6 | 25 px | **−4 px** |
| nilo | y=6 | 25 px | **−4 px** |
| admin_campo | y=7 | 24 px | −3 px |
| amalia | y=7 | 24 px | −3 px |
| crianca_floresta | y=7 | 24 px | −3 px |
| dario | y=7 | 24 px | −3 px |
| lembrante_f | y=8 | 23 px | −2 px |
| lembrante_m | y=8 | 23 px | −2 px |
| mae_ciro | y=8 | 23 px | −2 px |
| marta | y=8 | 23 px | −2 px |
| rita | y=8 | 23 px | −2 px |
| raul | y=9 | 22 px | −1 px |
| tadeu | y=9 | 22 px | −1 px |
| **amaro** | **y=11** | **20 px** | **nada — use como referência** |

`amaro` já está certo. É o modelo: mesmo estilo, mesma paleta, mesma qualidade
de desenho, dentro da caixa.

---

## 4. Como conferir antes de entregar

Roda em qualquer pasta com os PNGs, só precisa de Python 3 e Pillow:

```python
from PIL import Image
from pathlib import Path

for f in sorted(Path('.').rglob('overworld.png')):
    im = Image.open(f); px = im.load()
    ys = [y for y in range(32) for x in range(16) if px[x, y] != 0]
    top, bot, h = min(ys), max(ys), max(ys) - min(ys) + 1
    ok = (top >= 10 and bot == 30 and 19 <= h <= 21)
    print(f"{'OK ' if ok else 'NAO'} {f.parent.name:20s} topo=y{top} pe=y{bot} altura={h}")
```

Passa quando imprimir `OK` para todos: `topo>=10`, `pe=30`, `altura` entre 19 e 21.

---

## 5. Pendências do próprio lote 01

1. ~~**Mãe do Ciro** — o lado do portfólio e da ponta da faixa está trocado nos
   três quadros de costas (`5`, `6` e o `1`).~~ **Corrigido no lote 03**: os
   quadros `1`, `5` e `6`, linhas 20 a 27, exatamente 99 pixels, paleta
   idêntica — bate com o que o pacote declara.
2. **Mãe do Ciro e Criança da Floresta** não entraram no jogo: não têm slot
   próprio no projeto. As folhas estão prontas; falta decidir em que mapas eles
   ficam para eu criar o gráfico e a paleta.
3. **Alternativas dos administradores** (`admin_campo`, `admin_arquivo`) não
   foram aplicadas. Hoje esses slots são do Breno e da Marta, e o overlay
   principal já traz a arte deles. Trocar é decisão de elenco, não técnica.

---

## 6. O que falta dos 42

Os 23 que o lote 01 não trouxe — o lote 03 entregou a **mãe do protagonista**,
e a **recepcionista de link** (que não estava nesta lista, mas era a de maior
exposição de todas). Faltam 21:

Protagonista masculino, Protagonista feminina, Ciro, Anahi, Val, Elias,
Otacílio, Luzia, Zila, Bento, Dalva, Ademar, Olivia, Nara, Lídia, Cecilia,
Caetano, Celina, Lázaro, Rosa, Clara, Tibúrcio.

Três observações para quando forem feitos:

- **Anahi** precisa também da imagem de abertura `birch.png` (42×63, é o retrato
  grande da apresentação da região).
- **Os protagonistas** precisam das superfícies extras além da caminhada:
  bicicleta, surf, pesca, field move, e a costas de batalha.
- ~~**Prioridade por exposição:** a recepcionista de link aparece em dez mapas e
  a mãe do protagonista em cinco, incluindo a primeira casa do jogo. Ambas
  estão hoje com 27 px e 25 px, fora da caixa.~~ **Feito no lote 03**: as duas
  estão em 21 px com o topo em y=10, cada uma com paleta própria. Sobra o
  `dusclops.png`, com 26 px, num mapa só.

# Sprites de overworld: por que os últimos não prestaram

Arte que fica bonita a 64×64 e some no jogo não é azar: é uma faixa numérica.
O Emerald desenha 126 NPCs dentro de uma faixa bem estreita, e o que o projeto
entregou até agora cai fora dela em dois eixos — cor e passo.

Este arquivo é a faixa medida, não uma opinião. Os números saem dos 94 sheets
da vanilla que o projeto ainda não tocou.

## O diagnóstico, em duas linhas

**A cor.** Os 32 personagens redesenhados têm saturação média 34. Os mesmos
personagens na vanilla tinham 43, e o elenco da vanilla vai de 29 a 69. O
elenco novo inteiro cabe entre 26 e 40 — todo mundo na mesma faixa de bege
acinzentado. De longe eles não se distinguem uns dos outros, e é por isso que
o mapa vira uma papa.

**O passo.** Em 23 sheets uma das poses de caminhada é cópia exata da pose
parada. O motor toca `pose A → parado → pose B → parado`; se a pose A é a
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

### Os 23, para conferência

Dez são regressões — a vanilla animava e a substituição parou de animar:

`prof_birch` (ANAHI), `wallace` (AMALIA), `aqua_member_m`, `aqua_member_f`,
`archie`, `magma_member_f`, `maxie`, `anabel`, `brandon`, `noland`, `tucker`.

Os outros não têm original na vanilla: `admin_archive`, `admin_field`,
`ciro/phase1_brendan`, `ciro/phase1_may`, `ciro/phase2`, `ciro/phase3`,
`dona_zila`, `elite_four/drake`, `elite_four/glacia`, `gym_leaders/flannery`,
`gym_leaders/roxanne`.

`hot_springs_old_woman` é da vanilla assim mesmo — não é problema do projeto.

## O que ainda está fora de escala

Quatro sprites continuam altos demais, e não há arte de substituição para eles
nos pacotes recebidos: a mãe do protagonista (25 px contra 20–21), a
recepcionista de link (27), a enfermeira da sala de união (27) e o Dusclops do
overworld (26). A mãe é a mais visível, porque aparece nos primeiros minutos;
trocar a arte dela exige antes lhe dar paleta própria, já que hoje ela usa uma
paleta genérica compartilhada.

# Os treinadores de rota

O pacote `Arauna_Times_Treinadores_Rotas_v1` entrou: 287 times de rota e 214
times de revanche, 1293 Pokémon ao todo.

## O que foi conferido antes de instalar

| | |
|---|---:|
| times-base no pacote | 287, com 634 Pokémon |
| times de revanche | 214, com 659 Pokémon |
| símbolos `sParty_*` que o repositório **já tinha** | **501 de 501** |
| espécies desconhecidas | 0 |
| golpes que a espécie não aprende | **0 de 2439** |

O número que mais importa é o do meio: **todos os 501 arrays já existiam**. Isto
não cria treinador nenhum, troca o time de quem já estava lá — por isso o risco é
pequeno e o diff é grande.

O segundo que mais importa é o último. Cada golpe de cada Pokémon de cada time
foi conferido contra o que a espécie realmente aprende: tabela de nível até o
nível daquele Pokémon, TM/HM, ou golpe de ovo. **2439 golpes, nenhum impossível.**
O pacote de fato usou os movesets que instalamos.

## Dois defeitos achados

**Sete golpes sem o prefixo `MOVE_`.** `GALOPE_SEM_CABECA`,
`FOGO_FATUO_ANCESTRAL` e `CANTO_DA_IARA` aparecem crus em sete lugares do
`REMATCH_PARTIES_REFERENCE.h`. Isso não compila. Corrigido na instalação.

**A conta de BST vale só para os times-base.** A validação diz "0 Pokémon acima
de 560 BST". Nos 634 Pokémon dos times-base é verdade: **zero**. Nas revanches há
**doze**, todos Ararunão com 598, entre os níveis 37 e 47. Como revanche é
pós-jogo, isso é defensável — mas a afirmação, sem qualificar, não é.

As outras quatro batem exatamente: 0 lendários, 0 iniciais, 0 da família pseudo
#046–048, 0 espécie repetida dentro do mesmo time.

## O que a instalação teve de fazer além de copiar

O pacote escreve os 501 times como `TrainerMonNoItemCustomMoves` — sem item
segurado. Mas **31 desses times carregam item hoje**: 51 vagas, entre elas doze
Nuggets, dezoito Oran Berries e três Sitrus. Copiar o pacote como está tiraria
todos, em silêncio, e o build continuaria verde.

A instalação preserva: para essas 31, ela emite `TrainerMonItemCustomMoves` e
carrega o item que cada vaga já tinha. **34 itens de verdade** (fora os
`ITEM_NONE`) sobreviveram. Onde o time novo tem mais Pokémon que o antigo, as
vagas extras ficam sem item; onde tem menos, o item da cauda se perde — não há
como adivinhar melhor do que isso.

Também foram trocadas **434 macros** em `src/data/trainers.h`, de
`NO_ITEM_DEFAULT_MOVES` para `NO_ITEM_CUSTOM_MOVES` (ou as versões com item),
porque um time com golpes explícitos precisa da flag
`F_TRAINER_PARTY_CUSTOM_MOVESET` — sem ela o motor ignora os golpes escolhidos e
usa os quatro últimos por nível. Conferido depois: **nenhuma macro em desacordo
com a struct do seu array**, nos 854 times do arquivo.

## O rival e os chefes ficaram de fora

Como o pacote pede. Nenhum `sParty_May*`, `sParty_Brendan*`, `sParty_Wally*`,
`sParty_Steven*` nem de líder foi tocado — conferido no diff.

## A curva

Os times-base sobem de nível com a rota, sem degrau invertido:

| rota | níveis | | rota | níveis |
|---|---|---|---|---|
| 102 | 6 | | 119 | 29–32 |
| 104 | 8–10 | | 123 | 32–34 |
| 110 | 18–20 | | 128 | 36–39 |
| 114 | 23–26 | | 134 | 40–42 |

Route 116 aparece em 9–11, fora da ordem numérica, e está certo: ela fica cedo na
geografia, entre a 104 e a 105.

**Contra o teto de nível:** o mais alto dos times-base é 42, que é exatamente o
teto com seis insígnias; o mais alto das revanches é 50, contra os 58 do
Campeão. As duas curvas fecham no topo. O meio do jogo depende da ordem dos
ginásios, que este pacote não declara — se uma rota cair antes da insígnia que eu
suponho, os treinadores dela ficam acima do teto do jogador naquele trecho.

## Conferido no emulador

Entrei no campo de visão do CAIO, o primeiro treinador da Route 102:

| | pacote | lido da RAM |
|---|---|---|
| espécie | `SPECIES_CASTFORM` (#351 Tuim) | 385, que é CASTFORM |
| nível | 6 | 6 |
| golpes | SCRATCH, ABSORB | 10, 71 |

Os golpes são a parte que prova mais: um Tuim de nível 6 com moveset padrão não
teria esses dois. Vê-los significa que a flag de moveset customizado pegou.

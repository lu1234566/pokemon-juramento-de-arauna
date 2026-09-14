# Os movesets das 386 espécies

O pacote `Arauna_Move_Package_386_Fairy` entrou inteiro. São três camadas, e
elas foram instaladas nessa ordem porque cada uma depende da anterior:

1. **o tipo Fairy e os seus oito golpes** — `TYPE_FAIRY` já existia com a tabela
   de efetividade completa, inclusive a imunidade do Dragon; faltavam os golpes;
2. **os 22 signatures** — três Fairy com animação própria, dezenove montados
   sobre efeitos que o motor já tem;
3. **as 386 tabelas de nível** — 5221 entradas, de 9 a 20 por espécie.

## O que existe agora

| | |
|---|---:|
| golpes novos | 27 (ids 355 a 381) |
| `MOVES_COUNT` | 382 |
| learnsets instalados | 386 |
| entradas de nível | 5221 |
| ponteiros na tabela | 412 (386 + 26 preservados) |
| espécies com golpe Fairy | 68 |

Os 26 ponteiros preservados são `SPECIES_NONE` e os 25 `OLD_UNOWN`: o pacote não
os cobre e deixá-los nulos daria um ponteiro solto no primeiro Pokémon que os
lesse. Eles continuam apontando para o que apontavam.

## Os oito golpes Fairy

| id | nome na tela | pot | prec | efeito |
|---:|---|---:|---:|---|
| 355 | FAIRY WIND | 40 | 100 | dano |
| 356 | DISARM VOICE | 40 | — | nunca erra |
| 357 | DRAIN KISS | 50 | 100 | absorve |
| 358 | DAZZLE GLEAM | 80 | 100 | dano |
| 359 | MOONBLAST | 95 | 100 | pode baixar SP. ATK |
| 360 | JACI MOON | 100 | 90 | pode baixar SP. ATK |
| 361 | ARAUANA OATH | 105 | 90 | sobe a SP. DEF do usuário |
| 362 | ECLIPSE | 110 | 85 | baixa a SP. ATK do usuário |

Os três últimos são os signatures Fairy, e são os únicos golpes novos com
**animação própria**: cinco folhas de sprite em `graphics/battle_anims/sprites/`
(`fairy_spark`, `fairy_wave`, `fairy_crescent`, `fairy_oath`, `fairy_eclipse`),
com código em `src/battle_anim_fairy.c` e roteiro em `data/battle_anim_scripts.s`.

Dois slots de efeito que o Emerald declarava e nunca usava foram reaproveitados
para `EFFECT_SPECIAL_DEFENSE_UP_HIT` e `EFFECT_SPECIAL_ATTACK_DOWN_USER_HIT`.
Nenhum golpe vanilla os usava, então nada mudou de comportamento.

## Os dezenove signatures restantes

Cada um pertence a uma espécie só e é aprendido tarde. Nenhum foi trocado por um
golpe vanilla: todos existem com nome, descrição, tipo, potência e precisão
próprios. O que é emprestado é o **efeito**, porque escrever um efeito novo é
mexer no motor de batalha.

| golpe | dono | nível | tipo | pot/prec | efeito emprestado |
|---|---|---:|---|---:|---|
| CELESTIAL ST | Draguará | 46 | Fire | 90/100 | pode queimar |
| WETLAND BURS | Terolibra | 46 | Water | 90/95 | pode baixar SPEED |
| GRANITE HAMM | Petropico | 46 | Rock | 95/90 | pode baixar DEFENSE |
| ANCESTRAL WI | Boitatá | 45 | Fire | 85/100 | pode queimar |
| BACKWARD STE | Curupira | 44 | Grass | 80/100 | prioridade +1 |
| IARA SONG | Iaraço | 42 | Water | 75/100 | pode confundir |
| SACI WHIRLWI | Sacizinho | 43 | Flying | 80/95 | prioridade +1 |
| RIVER ENCHAN | Botogaláu | 45 | Psychic | 85/100 | pode confundir |
| BOIUNA EMBRA | Boiuna | 55 | Dragon | 95/90 | prende 2 a 5 turnos |
| HEADLESS GAL | Mula-sem-Cabeça | 48 | Fire | 90/100 | recuo |
| MOTHER TIDE | Iemanjá | 50 | Water | 90/100 | absorve |
| OGUN FORGE | Ogum | 50 | Steel | 90/100 | sobe a DEFENSE do usuário |
| GREAT SERPEN | Cobra-Norato | 48 | Ghost | —/90 | paralisa |
| GUARACI DAWN | Guaraciana | 60 | Fire | —/— | sol por cinco turnos |
| TUPA THUNDER | Tupanaú | 62 | Electric | 105/85 | pode paralisar |
| SUPREME CURR | Iaraú | 60 | Water | 100/95 | pode baixar SPEED |
| PRIMORDIAL B | Fogaréu | 65 | Fire | 110/85 | recuo |
| ATLANTIC SUR | Marulho | 65 | Water | 105/90 | pode fazer hesitar |
| PRIMORDIAL E | Arauá | 70 | Dragon | 110/90 | baixa a SP. ATK do usuário |

ARAUANA OATH tem dois donos, Arauanaú e Arauanamon, ambos no nível 65.

### As sete aproximações, ditas em voz alta

Sete desses dezenove fazem **menos** do que o conceito do pacote pede. A
descrição que aparece no jogo descreve o que o motor faz hoje, não o que o golpe
deveria virar — assim ninguém é enganado pela tela de resumo:

| golpe | o conceito pede | o motor entrega |
|---|---|---|
| BACKWARD STE | prioridade **e** inverter mudanças de atributo | só a prioridade |
| SACI WHIRLWI | prioridade **e** trocar o alvo de posição | só a prioridade |
| HEADLESS GAL | recuo **e** queimadura garantida | só o recuo |
| PRIMORDIAL B | recuo **e** queimadura garantida | só o recuo |
| GREAT SERPEN | paralisia **e** prender o alvo no lugar | só a paralisia |
| GUARACI DAWN | dano **e** sol | só o sol |
| PRIMORDIAL E | dano pesado com efeito de campo | só a queda de SP. ATK do usuário |

GUARACI DAWN é o caso que mais mudou de forma. Ele chegou declarado com potência
100 e precisão 90, mas `EFFECT_SUNNY_DAY` não calcula dano nem testa precisão —
os dois números seriam **lidos por ninguém**, exceto pela IA, que pontua golpe
por potência e passaria a escolher um golpe de dano zero achando que vale 100.
Está declarado agora com a forma da Sunny Day vanilla: potência 0, precisão 0,
alvo o próprio usuário. Quando o efeito real existir, os números voltam.

Os outros doze fazem exatamente o que a descrição diz.

## Como isso foi conferido

**A arte, três vezes, em três lugares diferentes.** Os cinco PNGs chegaram
truncados na primeira versão do pacote — assinatura e IHDR válidos, IDAT cortado,
e o `CHECKSUMS.sha256` passava porque assinava os bytes quebrados. A versão
corrigida foi conferida:

1. **estrutura** — assinatura, limites e CRC de cada chunk, IEND exatamente no
   fim do arquivo, IDAT que descomprime inteiro, filtros válidos, e
   `bit_depth = 4` com paleta indexada de 16 cores, que é o que o `.4bpp.lz`
   espera;
2. **conversão** — o `.4bpp` gerado pelo `gbagfx` foi decodificado de volta tile
   a tile, na ordem em que o hardware de OBJ lê, e comparado pixel a pixel com o
   PNG: **0 divergências** nas cinco folhas, o que prova que os offsets de quadro
   em `src/battle_anim_fairy.c` (0/4/8/12 para o spark, 0/16/32 para a onda,
   0/16 para as outras) caem onde devem;
3. **na tela** — os três signatures Fairy foram disparados numa batalha selvagem
   de verdade e fotografados no auge da animação. JACI MOON mostra a lua, as
   fagulhas e a onda com a tela escurecida; ARAUANA OATH mostra o losango sobre o
   alvo; ECLIPSE mostra o disco negro com a coroa, sobre o tingimento violeta.

Um detalhe que custou algumas tentativas: com precisão 90 e 85, esses golpes
erram, e **um erro pula a animação inteira**. As primeiras capturas vieram vazias
não por defeito de arte, mas porque o golpe errou. O roteiro de teste passou a
atacar de novo no mesmo combate até acertar.

**As tabelas de nível, contra a RAM.** Um Pokémon criado no nível 25 foi lido da
memória — personality, substructs desembaralhados e decifrados — e os quatro
movimentos comparados com o que a tabela instalada declara:

| espécie | a tabela diz | o jogo deu |
|---|---|---|
| 167 Sementim | GROWTH, VINE WHIP, LEECH SEED, RAZOR LEAF | 74, 22, 73, 75 |
| 168 | GROWTH, VINE WHIP, LEECH SEED, RAZOR LEAF | 74, 22, 73, 75 |
| 169 | LEECH SEED, RAZOR LEAF, GIGA DRAIN, SOLAR BEAM | 73, 75, 202, 76 |

As três batem campo a campo, e a terceira difere das duas primeiras — o que
mostra que o jogo está lendo a tabela por espécie, e não um ponteiro só.

**Dois defeitos foram achados assim, e nenhum aparecia na compilação.**

O primeiro: os dezenove signatures não-Fairy apontavam todos para a **mesma**
descrição, a do ECLIPSE. Compilava, ligava e teria mostrado "A divine eclipse
erupts" na tela de resumo de dezenove golpes diferentes. A descrição chega por
uma tabela de ponteiros, então nada no build repara em duas entradas iguais.

O segundo: duas descrições Fairy do pacote eram **mais largas que a janela**, e o
excesso é cortado em silêncio na tela — "Moonlight erupts at the foe." com 148px
e "Jaci's moonlight crashes down." com 158px, contra os 147px da linha mais larga
que o jogo original desenha nesse arquivo.

Os dois agora são guardados por `tools/arauna/check_text_width.py`, que já media
a largura das descrições de item e passou a medir também as de golpe, e a recusar
qualquer texto usado por mais de um golpe. O gate roda dentro de
`scripts/check_arauna_static.sh`, junto com os outros.

## Se for mexer nisso

A fonte é o pacote, não este repositório:
`master/learnsets_386_integrated_fairy.json`. O arquivo
`src/data/pokemon/arauna_complete_learnsets.h` é gerado e diz isso no cabeçalho.
Editar o `.h` na mão funciona até o próximo pacote chegar e apagar a edição.

`level_up_learnset_pointers.h` **não** é gerado — ele carrega os 26 ponteiros
preservados que o pacote não conhece. Regerar por cima dele perde esses 26.

# Conforto de jogo

Doze adições. Nove são opcionais — o jogador só as encontra se as procurar — e
o teto de experiência, o EXP Share nativo e a liberdade dos HMs mudam regra
sozinhas, que é o que foi pedido delas.

## O menu ARAUNA

Entrada nova no START, entre POKéNAV e o nome do jogador. Abre sete itens:

| item | o que faz |
|---|---|
| **LEVEL** | diz o nível do próximo chefe e, se você quiser, sobe a equipe até ele |
| **REMEMBER** | reaprende qualquer movimento que aquele Pokémon já passou no nível |
| **LINEAGE** | ensina os egg moves da linhagem dele |
| **STORAGE** | abre o PC de onde você estiver |
| **REST** | restaura HP, PP e status da equipe inteira, de graça |
| **WARD** | liga/desliga o repelente permanente |
| **POTENTIAL** | liga/desliga a leitura de IVs na tela de resumo |

É um **script**, não uma tela nova em C. O `multichoice` do próprio motor já
resolve janela, cursor, botão B e a linha de cancelar, e o relearner já era
dirigido por script — então as duas coisas se encaixam sem nenhuma UI nova para
dar errado.

### O level cap

O teto é o ás do próximo chefe ainda à frente, lido das próprias equipes em
`src/data/trainer_parties.h`, não escolhido por gosto:

| insígnias | próximo | teto |
|---:|---|---:|
| 0 | Serra do Uivo | 15 |
| 1 | Porto das Redes | 19 |
| 2 | Encruzilhada | 24 |
| 3 | Casa da Cinza | 29 |
| 4 | Pampa da Espera | 31 |
| 5 | Mata do Meio | 33 |
| 6 | Missões do Céu | 42 |
| 7 | Águas de M'Boi | 46 |
| 8 | Elite, primeira cadeira | 49 |
| Elite vencida | Campeão | 58 |

Depois do jogo fechado o teto abre: não há mais chefe para acompanhar.

**O botão só sobe.** Descer de nível não devolve movimento nem desfaz evolução,
então deixaria o Pokémon num estado que o jogo não sabe descrever.

**O teto também segura a experiência.** Um Pokémon no teto para de ganhar XP.
Isso monta no mesmo galho que o jogo já tinha para um Pokémon no nível 100, em
`Cmd_getexp`: ele simplesmente não ganha, sem mensagem de repreensão.

> **Um aviso sobre a curva, que é do jogo e não desta mudança:** entre a sexta e
> a sétima insígnia o ás salta de 33 para 42. Nove níveis. É o único ponto em
> que o teto vai parecer um muro em vez de um guia. Fechar esse vão é mexer em
> equipe de chefe, que está fora do escopo daqui.

### O tutor de linhagem

Reaproveita a tela do relearner inteira. A única diferença entre os dois é de
onde sai a lista de movimentos, e isso é uma variável que o script liga antes
de abrir a tela. Nenhuma tela nova, nenhum desenho novo.

## Os dois interruptores

**WARD — repelente que não acaba.** A regra é a mesma de um repelente comprado:
selvagens de nível abaixo do líder da equipe são pulados. Não é "sem encontro
nenhum", então nada raro fica inalcançável por ligar isso. Um repelente comprado
continua contando os passos, mas não anuncia mais que acabou, porque o efeito
não acaba.

**POTENTIAL — a página SKILLS mostra os IVs.** Mesmos seis campos, mesmo
desenho: só os números trocam, de "no que ele virou" para "com o que ele
nasceu". O HP aparece como `IV/31` para dar a escala. Desligar devolve os
atributos na hora.

## As cinco de fora do menu

**Correr por padrão.** Opção `AUTO RUN` no menu Opções, ligada em jogo novo. Com
ela o B inverte: você corre andando e segura B para andar devagar, que é o que
se quer para alinhar num tile apertado. As Running Shoes continuam necessárias,
então o começo do jogo lê igual.

A lista de opções passou de sete itens para oito. A moldura é desenhada em
linhas de tile fixas — a lista ocupa as linhas 4 a 19 e não há para onde crescer
— então o espaçamento das linhas caiu de 16 px para 14. O texto tem 12 px de
altura, então nada é cortado. O valor está em `OPTION_ROW_HEIGHT`, num lugar só.

**Ovos chocam em dois passos.** A vanilla só olha os ovos a cada 255 passos e
tira um ou dois de um contador que começa perto de vinte. Agora olha a cada
passo e zera o contador de uma vez: o primeiro passo leva o ovo à última volta,
o segundo choca. O intervalo é `ARAUNA_EGG_STEPS_PER_CHECK`; pôr 255 devolve o
ritmo original.

**EXP Share nativo.** Todo Pokémon vivo da equipe ganha da batalha sem carregar
o item. O rateio em si é o do jogo — metade para quem lutou, metade dividida —
então o que muda é só o banco parar de ficar para trás. A chave é
`ARAUNA_NATIVE_EXP_SHARE`; pôr `FALSE` devolve o item ao comando.

**Sem HM slave.** Os oito movimentos de HM são oferecidos por qualquer Pokémon
assim que a insígnia correspondente estiver na mão, tanto no menu da equipe
quanto nos avisos do mundo (cortar árvore, quebrar rocha, empurrar pedra,
surfar, mergulhar, cachoeira). **A insígnia continua obrigatória** — cada script
checa a sua antes de qualquer coisa, e `CursorCb_FieldMove` também — então a
ordem em que o mundo abre é exatamente a mesma. O que some é a vaga que um
Bidoof ocupava.

Dig, Teleport, Sweet Scent e Milk Drink ficaram como estavam: são coisas que um
Pokémon de fato faz, não pedágio de estrada.

**Shiny em 1/100.** `SHINY_ODDS` foi de 8 para 655 — 655/65536 é 1 em 100,1.

> Cuidado se for mexer nisso de novo: três telas passam `SHINY_ODDS` como
> **otId** com personality 0 para forçar um sprite de prévia não-shiny (o
> Pokédex, a escolha de inicial, o Lotad do menu). Continua funcionando com
> qualquer valor, porque `0 ^ n` é `n` e `n < n` é falso — mas o acoplamento é
> real e está documentado aqui porque não é óbvio no código.

## Saves antigos continuam valendo

A única coisa que persiste é o `AUTO RUN`, e ele mora num bit que a
`struct SaveBlock2` **já reservava como padding** dentro da palavra de opções
que já existia. Nada se moveu.

Isso não é afirmação, é verificado de duas formas:

- `STATIC_ASSERT(sizeof(struct SaveBlock2) == 0xF2C)` em `src/save.c` — o
  compilador recusa a build se o struct crescer.
- O gate de layout em `tools/arauna/check_overworld_registry.py`. Ele antes
  comparava `include/global.h` byte a byte contra `c8557cb2`, o que é um *proxy*
  para "o save não se moveu" e acusa qualquer edição, inclusive esta, que não
  move nada. Agora compara **o layout**: cada campo desses headers carrega o
  próprio offset num comentário, e esse mapa de offset para campo é o layout.
  406 offsets conferidos. Testado inserindo um campo de propósito: o gate falha
  e nomeia exatamente quais campos escorregaram.

## O que foi conferido no emulador

Tudo, exceto a taxa de shiny, que é aritmética e não amostra:

- menu ARAUNA abre sobre o campo e volta ao campo;
- LEVEL: equipe de três em nível 5 subiu para 15 com zero insígnias, e a fala
  diz "3 of your POKéMON came up to level 15";
- REMEMBER: abre a equipe, abre a lista, e diz corretamente que não há nada a
  reaprender quando não há;
- LINEAGE: lista exatamente os seis egg moves do Sementim (GRASSWHISTLE, ENCORE,
  LEECH SEED, NATURE POWER, CURSE, HELPING HAND), que é o que
  `src/data/pokemon/egg_moves.h` declara;
- STORAGE: abre o PC com as cinco opções;
- AUTO RUN: 15 tiles sem B contra 7 tiles com B na mesma faixa, em 120 frames;
- ovo: chocou no segundo passo;
- WARD: liga e desliga, com a fala certa dos dois lados;
- POTENTIAL: a página SKILLS mostrou 6 / 0 / 5 / 16 / 7 / 26 contra os IVs lidos
  da RAM na mesma partida — 6, 0, 5, 26, 16, 7 — batendo campo a campo;
- sem HM slave: CUT apareceu no menu de um Sementim cujos movimentos são
  [167, 0, 0, 0], com a primeira insígnia na mão;
- EXP Share: em três partidas seguidas, o lutador ganhou 26 de experiência e o
  Pokémon que ficou no banco ganhou 6, com `gExpShareExp = 6`, sem item nenhum.

**Dois** defeitos foram achados assim, e nenhum dos dois aparecia na compilação.

O primeiro: o menu inicial escurece a tela antes de
qualquer callback, menos os de uma lista curta que ficam no campo. O menu ARAUNA
não estava na lista, então o mapa apagava e nada o trazia de volta. Ele entrou
na lista, ao lado de SAVE e EXIT.

O segundo, mais instrutivo: o EXP Share nativo não funcionava, e o código
*parecia* certo. Eu havia mudado os dois pontos que fazem a conta do rateio,
mas quem não lutou e não segura o item é **descartado antes deles**, numa
terceira condição lá em cima na máquina de estados. As duas mudanças
compilavam, liam bem e não faziam absolutamente nada. Só a medição em batalha
pegou: o banco ganhava zero. Com a terceira condição corrigida, o banco passou
a ganhar 6 por batalha, reproduzível em três partidas.

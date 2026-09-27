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

## Os interiores da Casa da Fogueira

Sete ambientes, do pacote de interiores V2: quatro residências de 12 × 11, o
salão comunal de 18 × 14 com a fogueira central, e os dois andares do Centro
Pokémon. Banco de tiles próprio, 385 tiles e 229 metatiles, dos quais 138 em
uso — bem abaixo do teto de 512.

O instalador desse pacote passou sem nenhum conflito: ele cria sete layouts
novos, com sufixo `_Arauna`, em vez de sobrescrever os herdados, e acrescenta
um bloco isolado às três declarações de tileset.

**A única correção necessária foi de idioma.** O pacote traz o `scripts.inc`
do salão comunal com as falas novas em português — a cena em que as pessoas
contam, ao redor do fogo, cada uma a sua versão da ILHA MIRAGEM. O texto
visível deste repositório é inglês desde a passagem de tradução, e há um gate
de resíduo. As quatro falas foram traduzidas mantendo o conteúdo novo, e o
gate passa com zero candidatos.

### Conferido em jogo

Os sete ambientes percorridos no emulador, 90 a 140 voltas cada, com checagem
de tela parada. Nenhuma assinatura de travamento, e todos renderizam com a
paleta certa: a fogueira no salão, o balcão de cura e o PC no térreo, as mesas
de conexão no andar de cima.

Duas portas foram atravessadas de verdade: sair do salão comunal cai no
exterior novo, e a porta da frente do Centro também.

**A escada para o 2º andar do Centro não disparou no meu teste de caminhada.**
Isso não é defeito do pacote: o mesmo teste, feito num Centro Pokémon que
ninguém tocou, para no mesmo tile. O bloco da escada é idêntico ao da vanilla
— metatile 0x289, colisão 0, elevação 4 — e o 2º andar foi percorrido
entrando nele direto. É o meu método de teste que não serve para escada.

### Observação

A borda dos sete mapas é o metatile `0x201`, o mesmo que `SootopolisCity_House1`
já usava. Como o banco de tiles mudou, a área fora da sala agora aparece como
tábua de madeira em vez de vazio. É coerente com o resto, mas quem preferir o
vazio muda o `border.bin`.

## Os interiores das Águas de M'Boi

Vinte ambientes, em dois pacotes. O primeiro traz onze comuns: sete casas, a
casa dos recordes, a loja e os dois andares do Centro Pokémon. O segundo traz
os quatro especiais: os dois pisos da Casa Dupla, que é o antigo ginásio de
gelo, e os dois do arquivo, com a variante de passagem aberta.

A linguagem é a do exterior: piso de pedra clara, vigas de madeira escura e
janelas de veneziana azul. É de propósito diferente da Casa da Fogueira, que
é tábua escura inteira — são dois assentamentos distintos.

Os dois instaladores passaram sem conflito nenhum, e nenhum dos dois traz uma
única linha de diálogo: são conversão visual pura, ao contrário dos interiores
da Fogueira, que precisaram de tradução.

### A Casa Dupla é o quebra-cabeça do ginásio reskinnado

O antigo ginásio de gelo vira travessia de madeira sobre água, e **a mecânica
é a mesma, não uma reescrita**. Conferido comparando os atributos do banco
novo com os do `sootopolis_gym` da base, metatile a metatile:

| Metatile | Papel | Comportamento | Vanilla |
|---|---|---|---|
| `0x20D` | travessia inteira | `MB_THIN_ICE` (0x26) | igual |
| `0x20E` | travessia marcada | `MB_CRACKED_ICE` (0x27) | igual |
| `0x206` | travessia rompida | `MB_CRACKED_FLOOR_HOLE` (0x66) | igual |
| `0x207` | escada | `MB_NORMAL` (0x00) | igual |

Os quatro batem byte a byte. O `SootopolisGymIcePerStepCallback` continua
achando o que procura; o gelo que racha virou tábua que cede.

### Conferido em jogo

Nove ambientes percorridos no emulador, entre 80 e 200 voltas cada. Todos
renderizam com a paleta certa e ninguém travou.

Dois deles — a Casa Dupla B1F e o arquivo B1F — dispararam o meu detector de
"tela parada". **É falso positivo**: o detector compara o quadro inteiro, e
numa sala pequena com a câmera travada e nada animado em volta o quadro repete
mesmo. Fui conferir lendo a posição do jogador passo a passo, e ele anda nos
dois — 3 posições distintas num caso, 8 no outro, todas dentro da sala.

**O quebra-cabeça em si não foi resolvido de ponta a ponta.** Ele só liga com
o estado de script do ginásio, que um warp frio não monta, e as leituras que
tentei fazer do mapa vivo não ficaram confiáveis o bastante para eu afirmar
qualquer coisa. O que está provado é a equivalência dos atributos acima.

### O que os próprios pacotes deixam pendente

As três confrontações de lore, a cura antes do chefe e a arena dupla da
Bíblia continuam sem implementação narrativa. A Casa da História não está
concluída.

## A Casa da História, rebaseada

O pacote narrativo da Casa Dupla chegou construído sobre uma base muito
antiga, e o instalador dele **recusou-se a escrever** — corretamente. Se
tivesse escrito, teria revertido três trabalhos prontos: `trainers.h` estava
1014 linhas atrás e desfaria 26 `AGENT` → `AGENTE` e **434** movesets
customizados; `trainer_parties.h`, 10000 linhas atrás, levaria junto os times
da Dalva, do Ademar e da Olívia; `match_call.inc`, 990 linhas atrás, a
tradução do Match Call. A Elite Four voltaria a se chamar Drake, Glacia,
Phoebe e Sidney.

O pacote também **substituía a Dona Celina** por "GEMEAS": retrato de Tate e
Liza, que neste jogo é de Cecília e Caetano, batalha dupla e teto 42 — igual
ao 7º ginásio e abaixo dos 46 dela. A raiz está no próprio doc do pacote: a
Bíblia põe a Casa Dupla na 7ª Chancela, mas o slot herdado é o ginásio da 8ª.

Por decisão do autor, **a Celina fica**. Do pacote foi aproveitado só o que é
aditivo, reescrito para ela:

- **A guarda das três testemunhas.** Beatriz, Elena e Cilene já existiam no
  repositório — são `TRAINER_ANDREA`, `TRAINER_DAPHNE` e `TRAINER_BRIANNA`.
  Agora a Celina só aceita o desafio depois das três, usando as flags de
  treinador derrotado que já existem; num save antigo em que as três já
  cairam, o desafio abre direto.
- **A cura antes do chefe**, com `setrespawn` para o Centro da cidade.
- **A passarela de retorno**, que devolve à cidade sem precisar perder.
- **O texto do piso de baixo**, que dá às três testemunhas a margem antiga, a
  margem nova e o arquivo alagado, e reescreve os outros sete treinadores num
  registro mais literário. As cinco menções às Gêmeas voltaram para a Celina.

Ficou de fora tudo que dependia das Gêmeas: `trainerbattle_double`, o segundo
objeto na arena, o texto de "duas criaturas prontas" e as reescritas que
trocavam a Celina por elas.

### Uma correção de posicionamento

O pacote punha a placa da passarela em `(9,3)`, que é **andável**: o jogador
passaria por cima e ela nunca dispararia. No desenho original havia um segundo
objeto ao lado que mudava o acesso; sem ele, a placa é inerte. Movida para
`(9,4)`, que é bloqueado e encosta no corredor, então se lê encarando de
`(9,3)`.

### Conferido em jogo

Falar com a Celina antes das três testemunhas mostra "Hear the three voices
below before you face me" e **não** inicia batalha. A passarela pergunta
"This return bridge leads back to town. Leave now?" com SIM/NÃO. As duas
fotos estão em `docs/arauna/cidades/`.

**O caminho aberto não foi percorrido:** provar a cura e a liberação exigiria
derrotar as três testemunhas dentro do emulador, que é uma sessão longa. O
ramo fechado é o que está fotografado; o aberto é a queda natural para o
`trainerbattle_single` que já existia, mais um `special HealPlayerParty`.

### As comportas

O pacote V2 das comportas troca a lógica reativa que a rodada anterior tinha
deixado por uma mecânica de verdade. Duas passagens centrais do piso inferior
viram comportas fechadas: a primeira abre depois da margem antiga (Beatriz), a
segunda depois da margem nova (Elena). Um nicho a oeste guarda um registro das
duas margens, e a ala leste ganha água rasa que continua sendo chão.

A engenharia é limpa. Um `MAP_SCRIPT_ON_LOAD` reabre as comportas a partir das
flags de derrota guardadas no save, então o estado sobrevive a sair e voltar.
Cada comporta também confere a posição do jogador: quem cair do piso de cima
do lado norte ainda consegue abri-la por dentro e sair pelo warp original, em
vez de ficar preso. Elena e Cilene deixaram de ser treinadoras de linha de
visão e passaram a esperar conversa, para não dispararem fora de ordem quando
alguém cai do andar de cima.

Fechadas, as comportas são colisão 1; abertas, o script escreve `0x20F`, que
é o tile de deslize do quebra-cabeça — coerente com o piso reskinnado.

Como o pacote foi escrito para as Gêmeas, as mesmas cinco menções voltaram
para a Celina antes de entrar.

**Conferido em jogo:** encarar a segunda comporta dá "The second gate is shut.
ELENA's testimony…"; o nicho dá "Names from both banks share the same soaked
page."; e a Beatriz abre com a fala nova da margem antiga. As fotos estão em
`docs/arauna/cidades/`. A abertura depois da vitória não foi percorrida, pelo
mesmo motivo de antes: exigiria vencer as três dentro do emulador.

### O salão das duas margens, e o fim do quebra-cabeça de gelo

O V3 do salão faz uma troca grande, e vale dizer com todas as letras: **o
quebra-cabeça de gelo do piso de cima deixou de existir.** Saíram o contador
de passos (`VAR_ICE_STEP_COUNT`), o `STEP_CB_SOOTOPOLIS_ICE`, a quebra
progressiva das escadas e a queda pelo piso frágil. No lugar entram três
travessias centrais, abertas uma a uma pelos testemunhos de Beatriz, Elena e
Cilene lá embaixo, mais dois murais nas margens.

É uma decisão de desenho, não um conserto. O que se ganha é coerência: o
andar de cima passa a depender da mesma história que o de baixo conta, em vez
de um enigma de gelo reskinnado que já não tinha gelo. O que se perde é uma
mecânica. Os pacotes anteriores tinham preservado o enigma com cuidado —
conferi na época que os quatro atributos batiam byte a byte com a vanilla — e
este o aposenta.

Nada ficou pendurado: nenhum mapa referencia mais `STEP_CB_SOOTOPOLIS_ICE`, e
o `VAR_ICE_STEP_COUNT` continua sendo usado, de forma independente, pelo Sky
Pillar e pelo `cave_hole` — o ginásio simplesmente deixou de ser mais um
usuário de uma variável compartilhada, o que é melhor e não pior.

Como os anteriores, o V3 veio escrito para as Gêmeas. Desta vez não precisei
refazer a troca de texto inteira: o **delta** do V3 sobre a rodada anterior
não tem uma única menção às Gêmeas nem toca na batalha da Celina. Apliquei só
esse delta sobre a minha versão, então o portão das três testemunhas, a cura,
a passarela e a batalha simples continuam como estavam. No piso de baixo
entraram as duas correções de texto que o pacote trazia — as falas que ainda
mandavam "quebrar o gelo" agora falam das comportas.

Os dois murais são o melhor texto do pacote: o da margem antiga lista as
famílias deslocadas pela barragem, com nomes riscados mas ainda legíveis; o da
margem nova registra as casas salvas da cheia, e tem um canto marcado CUSTO
sem nome nenhum ao lado.

**Conferido em jogo:** a travessia diz "The old-bank crossing waits for
BEATRIZ's account."; o mural antigo diz "The old-bank mural lists families
displaced by the dam. Several names were scratched out but can still be
read." As fotos estão em `docs/arauna/cidades/`.

### A arena das duas margens

O V4 abre um canal de água no meio da arena. As duas margens passam a ser
alcançadas por caminhos secos separados, a partir da passarela em `(8,5)`, e a
margem leste fica mais inundada que a oeste. São 22 células trocadas.

O pacote é inteiramente sobre as Gêmeas: ele põe as duas em `(6,2)` e `(10,2)`,
uma de cada lado do canal. **O canal passa exatamente por `x=8`, que é onde a
Celina estava** — sem ajuste, ela ficaria dentro da água.

A geometria vale mesmo com uma líder só: o canal é o rio, que é a história
inteira desta casa. Então o mapa entrou e a Celina foi para a **margem oeste**,
em `(6,2)` — a margem antiga, a que os murais defendem. A margem leste ficou
vaga, e é exatamente onde a segunda figura ficaria se um dia a Casa virar das
Gêmeas ou a Celina ganhar uma parceira.

O V4 também repõe a placa da passarela em `(9,3)`, com o mesmo defeito de
antes: no novo mapa `(9,3)` continua andável e `(9,4)` passou a ser andável
também, então a correção anterior deixou de valer. A placa foi para `(8,4)`,
que é a beira do canal, bloqueada e colada na chegada da passarela — o jogador
sobe pelas travessias, chega em `(8,5)`, encara a água e a ponte oferece a
volta.

**Conferido em jogo:** a Celina é alcançável na margem oeste e o portão das
três vozes continua funcionando; a passarela em `(8,4)` pergunta "Leave now?"
com SIM e NÃO.

### Por que a 7ª Chancela não é uma troca de flag

O V4 explica melhor do que os anteriores: Mossdeep já ocupa a 7ª e libera os
eventos de Missões do Céu, e o slot de Sootopolis não só entrega a 8ª insígnia
como aciona estados ligados ao fim da crise. Mudar uma flag sozinha colide com
esses eventos. A migração teria de realocar a 7ª e a 8ª Casas junto com os
gatilhos das duas.

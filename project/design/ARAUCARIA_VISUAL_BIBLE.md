# Bíblia visual — Vila das Araucárias

## Visão

A Vila das Araucárias é o primeiro contato com Arauna. Ela deve parecer acolhedora
à primeira vista, mas antiga, úmida e ligeiramente inquietante quando observada
com atenção. A natureza não decora a vila: ela determina seus caminhos, crenças
e arquitetura.

A direção combina paisagem serrana do sul do Brasil, fantasia rural e suspense
contido. O resultado deve ser original e legível em uma tela de Game Boy Advance,
sem reproduzir edifícios, árvores ou composições de Hoenn.

## Pilares

### 1. Verticalidade ancestral

A araucária central domina a silhueta. Seu tronco é largo, escuro e marcado por
fitas, placas e pequenas oferendas não religiosas. As copas em camadas criam uma
forma imediatamente reconhecível mesmo em poucos pixels.

### 2. Pedra molhada e madeira envelhecida

Muros e fundações usam basalto cinza-azulado. Paredes e varandas usam madeira
escura, com reboco claro somente em pequenas áreas. Telhados são inclinados,
pesados e avermelhados pelo tempo.

### 3. Calor humano contra o frio

O cenário permanece frio e dessaturado. Janelas, lampiões e interiores recebem
âmbar quente para indicar abrigo. Esse contraste sustenta o tom sombrio sem
tornar a navegação escura demais.

### 4. Névoa como linguagem

A névoa oculta limites distantes e suaviza a vegetação. Ela não deve cobrir
portas, caminhos ou pontos interativos. O jogador sempre reconhece onde pode
andar, mesmo quando não entende o que existe além da vila.

## Paleta conceitual

Esta tabela é uma referência de direção, não a atribuição final de paletas do
motor. As cores serão quantizadas para RGB555 durante a produção.

| Índice | Cor | Uso principal |
| ---: | --- | --- |
| 0 | transparente | recortes de tiles e sprites |
| 1 | `#10181B` | contornos e sombras profundas |
| 2 | `#263438` | madeira escura e pedra em sombra |
| 3 | `#46585A` | basalto molhado |
| 4 | `#71817D` | pedra clara e névoa densa |
| 5 | `#B5C2B8` | reboco, brilho frio e névoa |
| 6 | `#153A2A` | agulhas profundas da araucária |
| 7 | `#28583A` | copa principal |
| 8 | `#4E754A` | musgo e vegetação média |
| 9 | `#82905B` | líquen e folhas iluminadas |
| 10 | `#4A3329` | troncos e vigas |
| 11 | `#75513A` | madeira envelhecida |
| 12 | `#9A684C` | telhas e barro úmido |
| 13 | `#B18755` | pinhão, cordas e detalhes |
| 14 | `#D2A55D` | luz de janela e lampião |
| 15 | `#71333A` | fitas, avisos e acentos narrativos |

## Arquitetura

- telhados inclinados com beirais largos para chuva;
- fundações de basalto visíveis;
- varandas estreitas de madeira;
- janelas pequenas com luz quente;
- cercas irregulares que acompanham a vegetação;
- placas entalhadas, sem sinalização urbana moderna;
- centro comunitário maior, adaptado como posto de pesquisa;
- nenhuma construção perfeitamente simétrica.

## Vegetação e terreno

- araucária ancestral central em conjunto de metatiles grande;
- araucárias menores como limite navegável;
- samambaias, erva-mate, musgo e capim úmido;
- chão de terra escura, sem caminhos amarelos;
- pedras de basalto formando degraus e contenções;
- poças discretas e folhas acumuladas;
- pinhões e pinhas usados apenas como pequenos detalhes.

## Composição da vila

| Zona | Elemento principal | Função narrativa |
| --- | --- | --- |
| Centro | araucária ancestral e clareira | símbolo da comunidade e do juramento |
| Norte | duas casas antigas | família do protagonista e vizinhos |
| Oeste | centro comunitário/pesquisa | introdução aos vínculos e à expedição |
| Leste | caminho entre pedras e mata | saída para a primeira rota |
| Sul | acesso parcialmente interditado | limite do prólogo e tensão futura |

## Legibilidade no GBA

- blocos navegáveis devem ser mais claros que limites e paredes;
- portas precisam de pelo menos dois contrastes de valor;
- contornos importantes usam um único tom profundo;
- detalhes menores que 2 × 2 pixels não são essenciais à leitura;
- a névoa nunca reduz o contraste do personagem com o chão;
- cada paleta prática deve respeitar até 16 entradas;
- o mapa será avaliado sempre em resolução nativa 240 × 160.

## Primeiro pacote de metatiles

### Prioridade A — circulação

- terra escura limpa;
- transições terra/grama nas quatro direções;
- curva interna e externa;
- degrau de basalto;
- borda de mata bloqueada;
- entrada leste e bloqueio sul.

### Prioridade B — identidade

- tronco e copa da araucária ancestral;
- araucária pequena em variações;
- basalto com musgo;
- lampião e janela acesa;
- fitas de juramento na árvore.

### Prioridade C — arquitetura

- casa pequena em madeira e reboco;
- telhado inclinado em três variações;
- fundação de pedra;
- varanda, porta e janela;
- posto de pesquisa comunitário.

### Prioridade D — atmosfera

- samambaia;
- erva-mate;
- poça;
- folhas e pinhões;
- cerca;
- placa entalhada.

## Restrições criativas

- não copiar tiles, edifícios ou árvores oficiais da franquia;
- evitar floresta tropical genérica;
- evitar excesso de preto que prejudique a tela do GBA;
- evitar terror gráfico, símbolos religiosos reais e estereótipos regionais;
- manter a vila habitável e humana, apesar do tom inquietante.

## Plano de produção

1. aprovar o quadro conceitual;
2. quantizar e testar a paleta em RGB555;
3. criar tiles-base de 8 × 8 pixels;
4. montar metatiles de 16 × 16 pixels;
5. cadastrar um tileset secundário próprio;
6. substituir gradualmente os placeholders no greybox;
7. testar colisão, contraste, névoa e leitura no mGBA;
8. iterar antes de criar interiores e a primeira rota.

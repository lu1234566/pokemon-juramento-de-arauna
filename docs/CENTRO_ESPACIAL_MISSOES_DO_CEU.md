# Missões do Céu — o Centro Espacial

Os dois pisos do Centro Espacial, no slot de Mossdeep, ganharam banco de
tiles próprio: piso claro, estrutura azul escura instrumentada, consoles,
guarda-corpo âmbar e, no segundo andar, a janela de observação com o céu.
No lugar do laboratório pálido do Emerald, uma sala de missão.

## O que foi trocado, e o que não foi

Só arte. Os dois registros de layout continuam com os mesmos ids e as mesmas
dimensões, 16 × 10, repontados para os arquivos novos e para
`gTileset_AraunaMissoesCeuSpaceCenterV1`. Nenhum `map.json`, nenhum
`scripts.inc`, nenhum evento.

Isso importa porque o segundo andar tem uma cena coreografada, com movimentos
em coordenadas fixas. **Conferido célula a célula, nas 320 dos dois andares:
zero diferenças de colisão e zero de elevação.** Só o metatile mudou — 157 de
160 no térreo, 159 de 160 em cima. O validador do pacote confirma o mesmo
para os warps das escadas e as duas saídas do térreo, copiados do banco
Facility.

## Uma limpeza na instalação

O instalador deste pacote copia mais que os anteriores: além dos arquivos do
repositório, ele traz `art/`, `review/` e `tools/arauna_maps/`. Isso é útil e
ficou — a fonte de autoria (`art/.../source_atlas.png`), as ferramentas de
reexportação e o manifesto que o próprio instalador relê, na mesma lógica que
`tools/arauna/battle_backgrounds/` já seguia.

Veio junto um `build_casa_fogueira_interiors_v2.py`, sobra do pacote de
interiores da Fogueira, que lê um `art/arauna_casa_fogueira_interiors_v2/`
que não existe aqui. Script que não roda é confusão para quem vier depois:
removido.

## Conferido em jogo

Os dois andares percorridos no emulador, 120 voltas cada, sem assinatura de
travamento e com a paleta certa. A foto do segundo andar está em
`docs/arauna/cidades/centro_espacial_2f.png`: as janelas de céu na parede do
fundo, o guarda-corpo âmbar, os consoles e os personagens da cena nos lugares
de sempre.

A sala é escura — é uma sala de missão à noite, e é essa a intenção do
concept —, mas vale o olho de quem desenhou se o contraste do chão aguenta a
tela do aparelho.

## Pendente

Os demais interiores de Missões do Céu.

## Os sete interiores

Quatro casas, a loja e os dois pisos do Centro Pokémon, em banco próprio:
reboco costeiro claro, madeira verde azulada, tapete geométrico azul e piso
de pedra. É de propósito diferente das outras duas cidades — a Casa da
Fogueira é tábua escura inteira, as Águas de M'Boi são pedra com viga escura,
e Missões do Céu é costeira e clara.

### Layouts próprios, e por que isso importa

Estes sete mapas usavam os layouts **compartilhados** do jogo —
`LAYOUT_HOUSE1`, `LAYOUT_MART`, `LAYOUT_POKEMON_CENTER_1F` e companhia. Se o
pacote tivesse reaproveitado esses registros, toda casa genérica de Arauna
teria virado costeira. Em vez disso ele cria sete layouts novos e repontatoma
só estes sete `map.json`. Conferido: nenhum outro mapa mudou.

### O que foi redesenhado e o que foi congelado

Três casas, a loja e o Centro ganharam ambientes novos, com NPCs e portas
reposicionados — as portas desceram de `y=7` para `y=10`.

**A Casa 2 ficou intocada de propósito**, e é a mais importante: um Wingull
anda por lá em coordenadas fixas, em dois trajetos. Conferido célula a
célula: zero diferenças de colisão, zero de elevação, e nenhum objeto movido.
O validador do pacote também marca `wingull_path_preserved` e
`center_special_metatiles_preserved`.

### Uma limpeza que se repetiu

O instalador deste pacote trouxe de novo o `build_casa_fogueira_interiors_v2.py`,
cuja fonte não está no repositório. Removido outra vez. Se vier um terceiro
pacote desta série, vale conferir de novo.

### Conferido em jogo

Os cinco ambientes percorridos no emulador, 80 a 100 voltas cada, sem
travamento e com a paleta certa. **A porta reposicionada foi atravessada de
verdade**: sair da Casa 1 cai em Missões do Céu. A foto está em
`docs/arauna/cidades/ceu_interiores.png`.

### Pendente

A Casa de Bento, a arena do ginásio e os dois andares da antiga Game Corner
ainda esperam arte própria.

## A Casa de Seu Bento

A casa no slot `MossdeepCity_StevensHouse`, 11 × 8, com banco próprio derivado
da arte costeira dos interiores: mesa com os registros em cima, parede clara e
vitrines na lateral. É o estúdio do guardião de nomes, e a mesa cheia de
papéis é exatamente a fala dele — "quando um nome cai da boca das pessoas, eu
anoto".

### O detalhe que podia quebrar

O script desta casa esconde a carta com
`setmetatile 6, 4, METATILE_GenericBuilding_TableEdge, TRUE`, e esse metatile
é o `0x2F1` do banco `generic_building`. Trocar o banco secundário do mapa sem
esse número no lugar certo deixaria a carta impossível de esconder.

Conferido: o banco novo tem o `0x2F1` com o atributo `0x1000`, **idêntico** ao
do banco antigo. E as 88 células mantêm colisão e elevação sem uma única
diferença, então os dois warps, os três objetos, os quatro pontos de leitura e
o corredor em que Seu Bento anda, de `(9,6)` a `(3,6)`, continuam como estavam.
O validador do pacote marca `script_commands_unchanged` e
`collision_elevation_unchanged`.

### Conferido em jogo

A casa percorrida no emulador, 110 voltas, sem travamento e com a paleta
certa. A foto está em `docs/arauna/cidades/casa_de_bento.png`.

Sobram a arena do ginásio e os dois andares da antiga Game Corner.

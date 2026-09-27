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

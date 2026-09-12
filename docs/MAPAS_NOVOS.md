# Integrar um mapa novo sem quebrar nada

O que já deu errado nas integrações anteriores, e como cada coisa aparece.
Rodar `python3 tools/arauna/audit_map_data.py` pega os quatro primeiros em
alguns segundos.

## Os erros que realmente acontecem

**Evento fora do mapa.** O pior deles, porque o jogo compila e roda. O Porto
do Sal V7 estreitou o mapa de 56 para 52 colunas e deixou o warp de chegada do
barco em x=52. O jogador desembarcava fora do mapa. Sempre que a largura ou a
altura de um mapa mudar, os warps, objetos, placas e gatilhos precisam ser
reconferidos — não só os que você mexeu.

*A vanilla tem dez eventos assim de propósito*, todos dirigidos por script
(Battle Dome, loja de Lilycove, Meteor Falls, porto de Slateport). O auditor
conhece os dez e só reclama dos novos.

**Metatile que o tileset não tem.** Um id dentro de 0–1023 mas além do fim do
array do tileset não é bloqueado pelo `DrawMetatileAt`: ele lê o que estiver
na memória depois — os tiles do desenho e, pior, o *byte de comportamento*, em
que o código de campo dá `switch`. Dá para andar por cima de água, atravessar
parede ou travar.

**Metatile em branco.** O `42` do tileset General tem os oito tiles em zero. Um
mapa que o use mostra um quadrado preto — foi o telhado do mart da Vila da
Passagem. Compila, passa em tudo, e só aparece olhando.

**`map.bin` do tamanho errado.** Precisa ser exatamente `largura × altura × 2`
bytes. Se não for, o mapa inteiro sai deslocado a partir da primeira linha que
faltou.

**Warp apontando para um id que não existe.** O destino é `(mapa, índice do
warp)`. Se o mapa de destino tem 3 warps e você aponta para o 4, o jogo lê
lixo.

## Conferências que o auditor não faz

**O warp cai num tile onde dá para ficar de pé.** Bounds é uma coisa,
caminhabilidade é outra: um warp dentro do mapa mas em cima de água ou parede
deixa o jogador preso. Vale um flood fill a partir do ponto de chegada.

**O metatile de porta combina com a animação.** Porta é um par (moldura +
abertura) mais uma entrada em `data/tilesets/*/anim`. Trocar o desenho da porta
sem trocar a animação faz a porta abrir mostrando outra coisa.

**O tileset secundário cabe.** Primário e secundário somam 1024 metatiles e 16
paletas, das quais o primário usa 6. Um secundário novo que passe disso não
falha no build — ele sobrescreve.

## Se o pacote vier com instalador

Os pacotes de conceito trazem `tools/apply_*.py` + `build_*.py` com um modo
`--check`. Eles guardam um `sha256.json` da árvore no momento em que foram
gerados e **se recusam a rodar numa árvore que divergiu** — o que acontece
sempre, porque a árvore anda entre a geração do pacote e a instalação.

Não desligue a guarda no reflexo. O caminho que funcionou foi: listar cada
divergência que o instalador aponta, confirmar uma a uma que é alteração
nossa e intencional, e só então converter o `raise` em aviso. Uma divergência
que você não reconhece é exatamente o que a guarda existe para pegar.

## Ordem que funciona

1. Copiar layout, `map.bin`, `border.bin`, tilesets e `map.json`.
2. Registrar o mapa em `data/maps/map_groups.json` e o layout em
   `data/layouts/layouts.json`.
3. `python3 tools/arauna/audit_map_data.py` — antes de compilar.
4. `make MODERN=1 -j$(nproc)`.
5. `bash scripts/check_arauna_static.sh`.
6. Andar pelo mapa no emulador, entrando e saindo de cada porta.

O passo 3 é o que economiza tempo: os erros que ele pega são todos do tipo que
compila limpo e só aparece com o jogador em cima.

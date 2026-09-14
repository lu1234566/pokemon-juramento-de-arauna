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

**Warp dentro do mapa mas inalcançável.** Bounds é uma coisa, chegar lá é
outra: um warp em cima de água, atrás de uma parede ou numa ilha sem ponte
compila, roda, e só aparece quando o jogador tenta ir. O auditor faz um flood
fill do ponto de Fly de cada mapa e reclama de warp que não dá para alcançar
nem de barco; os que exigem Surf ele só conta, porque dez deles são de
propósito. Duas conferências que o flood **não** faz: ele lê colisão e
comportamento, não elevação, e não pula ledge de mão única. Por isso dois
platôs da vanilla — o centro de Lavaridge e a entrada da Artisan Cave — estão
numa lista de exceções no próprio arquivo.

**Porta é de dois tipos.** Uma parte delas é tile caminhável e o warp dispara
sob os pés; outra parte é tile de colisão 1 em que você *esbarra*, e o warp
dispara do tile da frente — o portão da Liga é assim. Uma conferência que
exija o tile do warp caminhável marca metade das portas do jogo como quebrada.

## Conferências que o auditor não faz

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

**Desde a tradução, toda divergência de `scripts.inc` é esperada.** Os pacotes
foram gerados antes do inglês, então cada `.inc` que eles protegem por hash
bate diferente. A guarda existe para pegar warp movido, coordenada mudada ou
flag trocada — não texto. A conferência que resolve isso em segundos: apague o
conteúdo de cada `.string` dos dois arquivos, colapse sequências de `.string`
numa só marca, e compare o que sobra. Se o esqueleto for idêntico, só o texto
mudou e a guarda pode passar; se não for, pare e olhe.

**Cuidado com o instalador que reescreve um `scripts.inc` inteiro.** Alguns
pacotes não só protegem o arquivo: eles o substituem, para mexer em duas ou
três linhas. Como o pacote é anterior ao inglês, essa substituição **desfaz a
tradução** do arquivo. O que funcionou foi extrair só as linhas não-`.string`
que o pacote quer mudar e aplicá-las sobre o arquivo traduzido — em Baía das
Luzes eram treze linhas (doze coordenadas de Wailmer e um `setescapewarp`)
dentro de dois arquivos de duzentas falas.

### Conferir se um pacote antigo realmente entrou

Vale refazer de tempos em tempos: comparar cada pacote recebido com a árvore e
ver se o que ele queria escrever está lá. Comparar byte a byte dá **centenas de
falsos positivos**. Cinco regras, cada uma responsável por uma leva deles:

1. **Escopo.** O pacote carrega a árvore inteira (500+ `map.json`), mas só
   declara como sua a parte coberta por `review/*_source` — nos antigos, 10 a 20
   arquivos de 500. Fora dessa lista não dá para saber a intenção; não se cobra.
2. **Supersessão.** Pacotes se sobrepõem. Casa do Uivo V1 reenvia o Rustboro do
   Serra do Uivo V4; Vila Amanhecer V9 move NPCs que a V8 tinha posto em outro
   lugar. O repo bater com o **mais novo** é o resultado certo, não uma falha do
   mais antigo.
3. **Fim de linha.** O repo normaliza texto para CRLF, o pacote traz LF. Todo
   `.pal` acusa diferença com conteúdo idêntico.
4. **Registros que acumulam** — `headers.h`, `graphics.h`, `metatiles.h`,
   `layouts.json`, `heal_locations.json`, `event_scripts.s`. O repo tem a entrada
   de todos os pacotes, o pacote só tem até a dele. O que importa é se **a
   entrada dele** existe, não a igualdade byte a byte.
5. **Tradução.** Depois dos pacotes o jogo virou inglês, então todo `.inc`
   difere dentro de `.string`. Apague o conteúdo das `.string` e compare o
   esqueleto.

Com as cinco, a última varredura dos 19 pacotes recebidos passou de 503
divergências para 11, e as 11 se explicam todas: quatro são a passada de clima
por bioma, quatro são pacote posterior substituindo anterior, uma é a correção
do desembarque do Porto do Sal, uma é a do telhado do mart da Vila da Passagem,
e a última é o repo tendo **mais** do que o pacote — uma placa que um pacote
seguinte acrescentou. Nenhum pacote ficou de fora.

**Pacote gerado sobre pacote tem ordem.** Se a árvore de referência de um
pacote já contém o registro de tileset de outro, ele foi gerado depois daquele
e precisa ser instalado depois. Dá para ver com um `grep` dos marcadores
`// NOME_VERSAO_BEGIN` em `src/data/tilesets/headers.h` de cada pacote: quem
tem menos marcadores vem primeiro.

## Ordem que funciona

1. Copiar layout, `map.bin`, `border.bin`, tilesets e `map.json`.
2. Registrar o mapa em `data/maps/map_groups.json` e o layout em
   `data/layouts/layouts.json`.
3. `python3 tools/arauna/audit_map_data.py` — antes de compilar.
4. `make MODERN=1 -j$(nproc)`.
5. `bash scripts/check_arauna_static.sh` e
   `python3 scripts/check_english_only_policy.py`.
6. Andar pelo mapa no emulador, entrando e saindo de cada porta.

O passo 3 é o que economiza tempo: os erros que ele pega são todos do tipo que
compila limpo e só aparece com o jogador em cima.

O passo 6 dá para automatizar e vale a pena: com o harness local, nascer um
tile ao lado de cada porta, segurar a direção e ler em que mapa o jogador
parou. As três cidades desta rodada foram conferidas assim, 32 portas, uma a
uma. **Um detalhe que custa tempo se você não souber:** o harness pula o
script de novo jogo que devolveria o controle ao jogador, então o campo fica
travado e toda tecla é engolida — o personagem simplesmente não anda. Zere
`sLockFieldControls` (é `static`, sai de `elf_locals()`, não do `.map`) depois
do boot e antes de apertar qualquer coisa.

# Arauna — Anahi e Ciro: overworlds e apresentação inicial

Este pacote contém as duas folhas de overworld e o retrato de corpo inteiro de Anahi para a apresentação inicial, com paletas e binários para GBA. Cada folha tem nove quadros de 16×32 em uma linha de 144×32. Os desenhos foram gerados com a ferramenta integrada de imagens a partir das descrições fornecidas e exportados para a grade e a paleta nativas.

## Arquivos para uso

| Personagem | PNG | Paleta |
| --- | --- | --- |
| Professora Anahi | `characters/anahi/overworld.png` | `characters/anahi/overworld.pal` |
| Ciro | `characters/ciro/overworld.png` | `characters/ciro/overworld.pal` |

Cada pasta também contém `compiled/overworld.4bpp`, `compiled/overworld.gbapal`, `frames.json`, uma prévia ampliada e GIFs de caminhada. Os arquivos com `preview` no nome servem para conferência; o PNG nativo é `overworld.png`.

## Formato e sequência

PNGs indexados de 4 bits; no máximo 16 cores. Índice 0 = magenta sólido `#FF00FF`, tratado como transparente pelo motor. As paletas JASC têm 16 entradas; Anahi usa 15 entradas no PNG e a última entrada de hardware é preenchida, sem alterar os pixels. Anahi tem 14 cores visíveis; Ciro tem 15.

Ordem: frente parada, costas parada, esquerda parada, frente passo A/B, costas passo A/B, esquerda passo A/B. A direita é obtida pelo espelhamento do motor. As coordenadas usam índices a partir de zero.

Em todos os 18 quadros, a figura tem 21 px de altura, topo em y=10, pés em y=30 e largura máxima de 14 px. Nenhuma caminhada repete a parada ou o outro passo; há diferenças nas regiões dos braços e das pernas.

Os binários usam blocos de 2×4 tiles por quadro, equivalentes a `gbagfx -mwidth 2 -mheight 4`. Cada folha compilada tem 2304 bytes e cada paleta de hardware tem 32 bytes. As cores GBAPAL são convertidas para RGB de 5 bits por canal, como exige o GBA.

A paleta sugerida para Ciro somava 18 cores com o fundo. Para atender ao limite de 16, a sombra intermediária do cabelo e o segundo cinza da camiseta foram compartilhados com tons já presentes. Cabelo preto com reflexos azuis, jaqueta verde-acinzentada e bolsa marrom foram mantidos.

## Uso no projeto

Substitua a folha de cada personagem no slot de overworld correspondente e use a paleta fornecida nesse slot. Preserve o ID, a tag e a lógica de animação já existentes. A paleta precisa acompanhar o PNG: uma paleta antiga pode mudar as cores dos mesmos índices.

O pacote não muda o repositório automaticamente. Além dos overworlds, inclui a apresentação inicial de Anahi descrita abaixo. Retratos de batalha não fazem parte desta entrega.

## Conferência

`validation.json` registra dimensões, posição de cada quadro, cores, diferenças entre poses e hashes. A decodificação independente dos binários 4bpp reproduziu todos os índices dos PNGs, e as paletas JASC/GBAPAL foram conferidas. Estas são verificações dos arquivos; não houve teste em uma ROM nesta entrega.


## Anahi na apresentação inicial

O arquivo nativo é `characters/anahi/intro.png`: 64×64, indexado em 4 bits, 16 posições de paleta e índice 0 transparente. A figura completa, incluindo coque e botas, ocupa 42×62 px, de y=2 a y=63. Ela mantém o coque castanho-avermelhado, o jaleco branco, o vestido verde, o cinto marrom com fivela laranja e as botas do overworld. A mão aberta está em gesto de apresentação.

O arquivo pronto para substituir o recurso atual está em `overlay/graphics/birch_speech/birch.png`. Copie-o para esse mesmo caminho no seu projeto e recompile. Em `src/field_effect.c`, tanto `sNewGameBirch_Gfx` quanto `sNewGameBirch_Pal` são gerados desse PNG; não é necessário mudar o código nem copiar a paleta JASC separadamente para esse slot. O recurso usa o objeto 64×64 e a tag de paleta 0x1006 já existentes.

Os arquivos `intro.pal`, `compiled/intro.4bpp` e `compiled/intro.gbapal` são equivalentes nativos para conferência ou integração por outras ferramentas. O retrato tem 2048 bytes em 4bpp e a paleta de hardware tem 32 bytes. O PNG usa transparência real; o RGB do índice transparente é magenta, que não aparece no jogo.

As duas folhas de overworld são cópias idênticas às já entregues. O teste desta apresentação dentro de uma ROM continua não executado; a validação deste pacote confere os arquivos e as referências atuais do código.

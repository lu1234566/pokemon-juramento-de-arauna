# Arauna — Anahi e Ciro: overworlds nativos

Este pacote contém as duas folhas finais solicitadas, com paletas e binários para GBA. Cada folha tem nove quadros de 16×32 em uma linha de 144×32. Os desenhos foram gerados com a ferramenta integrada de imagens a partir das descrições fornecidas e exportados para a grade e a paleta nativas.

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

O pacote não muda o repositório automaticamente. Ele contém somente as superfícies de overworld solicitadas; retratos de batalha e de abertura não fazem parte desta entrega.

## Conferência

`validation.json` registra dimensões, posição de cada quadro, cores, diferenças entre poses e hashes. A decodificação independente dos binários 4bpp reproduziu todos os índices dos PNGs, e as paletas JASC/GBAPAL foram conferidas. Estas são verificações dos arquivos; não houve teste em uma ROM nesta entrega.

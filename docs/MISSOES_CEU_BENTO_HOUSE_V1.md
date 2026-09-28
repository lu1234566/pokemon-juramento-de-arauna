# Missões do Céu — Casa de Seu Bento V1

Adaptação visual nativa da casa no mapa `MossdeepCity_StevensHouse` (11 × 8 blocos). O banco gráfico dedicado deriva da arte costeira dos interiores V1, com mesa e registros sobre a madeira, parede clara e vitrines na lateral. A comparação PNG é renderizada dos tilesets e do `map.bin` reais.

O novo layout preserva os 88 valores originais de colisão e elevação, os dois warps, três objetos e quatro pontos de leitura. A faixa de movimento de Seu Bento entre `(9,6)` e `(3,6)` continua livre. O metatile `0x2F1` tem entrada explícita no banco novo e atributos `0x1000`, para o comando original que esconde a carta em `(6,4)` antes do fim do jogo. Os comandos de entrega de HM Dive, presente de Beldum, carta e flags não foram alterados nesta rodada.

Instale depois dos pacotes Centro Espacial V1 e Interiores V1; o exterior V2 pode precedê-los. `tools/arauna_maps/apply_missoes_ceu_bento_house_v1.py --target CAMINHO` confere conflitos, cria backup e é idempotente. `--check` apenas inspeciona. A validação cobre eventos, geometria, corredor, metatile dinâmico, registradores, instalação limpa e compilação do mapa por `mapjson`. A ROM e as cenas no emulador continuam sem teste.

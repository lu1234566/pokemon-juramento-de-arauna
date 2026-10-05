# Encruzilhada Central — oito interiores V1

A Bíblia, página 7, orienta arquitetura cívica, calçamento e comércio no nó
central de circulação. Não há concept individual identificado para estes
interiores no conjunto recuperado. A Casa da Fogueira já adaptada é separada.

O lote trata duas casas, venda, dois pisos do Centro, oficina de bicicletas,
salão de jogos e Casa elétrica. Pedra clara substitui as superfícies verdes,
vermelhas e amarelas; reboco e carpintaria própria delimitam os ambientes.
As casas usam tábuas, mesas e tecidos azuis. Oficina e jogos têm bancadas próprias.

As dimensões, map.bin e border.bin são idênticos à base. Os 18 warps, 36 objetos,
demais eventos, comandos de script, flags e índices permanecem iguais; somente
o layout selecionado pelo map.json muda. Nenhum diálogo é substituído pelo ZIP.
Os seis bancos dedicados preservam todos os atributos de metatile e os gráficos
originais referenciados, alocando desenhos apenas em slots antes sem referência.

A oficina mantém InitTilesetAnim_BikeShop e a região de animação 1008–1016.
A Casa elétrica mantém InitTilesetAnim_MauvilleGym, os slots 656–671 e suas
paletas 6/7 originais. As barreiras, estados dos botões, portas, PCs, escadas e
comandos de troca de metatile conservam IDs e atributos. A posição dos sprites
e a geometria do quebra-cabeça não mudam. Bancos primários não são modificados.

Construção, renderização, validação e instalador com backup/recusa de conflito
fazem parte do pacote. Instalação isolada, reaplicação, reprodução e conversão
mapjson são verificadas. Compilação de ROM e testes em emulador estão pendentes.

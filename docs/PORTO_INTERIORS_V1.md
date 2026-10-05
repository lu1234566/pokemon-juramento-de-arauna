# Porto do Sal — quatorze interiores V1

O concept 02 de Porto do Sal e a Bíblia, página 6, definem madeira de carga,
cais e edifícios históricos. Não existe prancha individual de cada interior
no conjunto recuperado; a referência externa orienta materiais e atmosfera.

Este lote adapta duas casas, venda, dois pisos do Centro, clube comunitário,
dois pisos do museu, cais, dois pisos do estaleiro e três ambientes do pavilhão.
Pisos de tábuas e reboco substituem superfícies amarelas, verdes e lilases;
mapas marítimos ganham molduras de madeira. Um casco sobre apoios e caixotes
substituem o conjunto metálico na oficina. O clube e a arena recebem tecidos
azuis. Equipamentos e exposições identificáveis continuam nas mesmas posições.

Os 28 warps, 67 objetos, eventos coordenados, flags, índices, recompensas e
comandos de script são preservados. Há 37 definições de movimento idênticas
à base. As dimensões, map.bin e border.bin permanecem byte a byte iguais;
a mudança em map.json é somente o layout dedicado. Nenhum diálogo é substituído.
A geometria das cenas do museu, embarque e pavilhão continua igual à recebida.

Sete bancos secundários próprios conservam todos os atributos de metatile.
Os desenhos adicionais usam apenas slots gráficos originalmente não referenciados,
abaixo de 992; tiles existentes não são sobrescritos. Bancos primários, água,
callbacks, portas, escadas, comportamentos de serviços e referências numéricas
usadas pelos scripts permanecem disponíveis. Os painéis e tecidos são sprites
indexados nativos de 16 cores, não imagens decorativas sobre o render.

O pacote contém construção, renderização, validação e instalador com backup
e recusa de conflitos. São verificadas instalação isolada, reaplicação,
reconstrução dos assets e conversão mapjson dos 14 mapas. Compilação de ROM,
cenas executadas no motor completo e serviços em emulador continuam pendentes.

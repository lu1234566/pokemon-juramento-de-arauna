# Pokémon Juramento de Arauna — checkpoint 07I / Exteriores V1

Base `725f8fe44f427b827221fdbcc3beca70e92e3b72`, checkpoint 07H concluído diretamente sobre a base oficial `531352ce3715e41389382de692e917a32b9e60be`. Três mapas encerram a arte do **Frontier: 47/47**. Nenhum push. Aceitação em ROM e mGBA permanece pendente.

## Referências e ambientação

Master Map Design Bible e concepts recuperados antes de editar. Ever Grande / Liga e Estrada do Juramento orientam o conjunto de terraços, pedra, vegetação e canais. Centro Comunitário e Sede da Liga Interior orientam a recepção e os serviços do 07H. Materiais e texturas foram editados nos bancos 4bpp do jogo, mantendo as silhuetas e máscaras que sustentam as interações.

Praças e passarelas recebem alvenaria de pedra; fachadas ganham terracota, bronze, pedra e verde. A Torre mantém sua silhueta vertical; Dome, Factory, Pike, Pyramid, Arena e Palace conservam entradas legíveis. O pavilhão recebe limiar e balcões de pedra e cobre. Vidro e metal das aberturas animadas continuam como detalhes nativos das fachadas. Insígnias e placas conservam inscrições e máscaras; nomes do motor são mantidos.

## Três mapas

| Mapa | Células | Células com arte alterada | Objetos | Warps |
|---|---:|---:|---:|---:|
| OutsideEast | 5184 | 3195 | 26 | 14 |
| OutsideWest | 4032 | 2479 | 24 | 11 |
| ReceptionGate | 126 | 126 | 5 | 2 |

Três layouts mantêm IDs, ordem, dimensões, grades e bordas. Apenas suas referências de bancos mudam para três pares privados. **9.342 células, 55 objetos e 27 warps ficam exatos**. Colisão, elevação, atributos, máscaras dos dois planos, conexões e posições conservadas. Os exteriores usam todas as 13 paletas originais; só a paleta 12, antes sem uso na recepção, recebe a mesma paleta de materiais dos exteriores. Nenhum layout acrescentado: continuam 754.

## Portas, água e bandeiras

As **16 portas animadas** mantêm os IDs dos dois metatiles, atributos, pixels fechados, paletas e arquivos de animação. C original GetDoorGraphics, BuildDoorTiles, DrawCurrentDoorAnimFrame e DrawClosedDoorTiles executado no host: 80 verificações de desenho/quadros e **128 estados nas duas sequências canônicas**. Oito assets passam pelo empacotamento original de gbagfx: ConvertBitDepth, AdvanceMetatilePosition e ConvertToTiles4Bpp. Isso inclui a PNG do mercado com índices acima de 15, convertidos corretamente para 4bpp; o arquivo original não é editado. Serviços do host são fixtures explícitas. Reprodução de tarefas e display GBA ainda não feita.

Água General conserva seus oito quadros e slots 432–511. Bandeiras East/West conservam quatro quadros e slots **730–735**: callbacks e filas originais executados por 256 ticks, 32 atualizações por lado, com guardas de VRAM. Slots 992–1023 reservados às portas. Alocação estática reaproveita somente tiles sem referências em metatiles preservados e usa flips nativos para deduplicação; nenhuma alocação invade animações.

## Preservação e testes

Contrato congela **23.935 arquivos** da base 07H, incluindo field_door.c, overworld.c, scripts, eventos, warps, condições, preços, registros, saves, progresso, dados do Frontier, objetos de campo, encontros e itens. Sudowoodo, Surf, acesso à Artisan Cave, recepção do passe, dicas e condições de Scott conservam sua lógica. As portas da Torre corrigidas e a água do Palace continuam exatas.

validation.json: PASS em **3.065 atributos**, **6.130 máscaras estáticas**, **15.632 máscaras em oito quadros**, 9.342 seleções C, 15.360 fallbacks, 53.167 células antigas de cavernas/Dive e **1.016 comparações dos materiais compartilhados nas conexões East/West**. Os **44 mapas anteriores** permanecem iguais em 88 renders, além de 14 comparações dos andares gerados da Pyramid e oito quadros da água do Palace. C original dos demais efeitos e do gerador continua passando (1.848 gerações, 1.892.352 células).

Auditoria dos 528 mapas e gates oficiais: PASS, logs em review/frontier_07i. O gate estático omite explicitamente o compile ARM. **Compilação da ROM e mGBA pendentes neste ambiente**, sem compilador ARM/emulador; não houve torneios, batalhas, compras, cura ou passeios jogados nesta ROM.

## Evidências visuais

Três pares de mapas completos, nove pares de câmeras 240×160, exterior conectado West + East, 16 portas com fechamento e três quadros de abertura e quatro quadros das bandeiras por lado. PNGs renderizadas em RGB555 dos bancos 4bpp, sem atores. Composições das portas usam os quadros reais e paletas do código; não são fotos do emulador nem playback de tarefas. Concepts não são evidência do jogo.

## Histórico e entrega

GitHub foi conferido antes e ao fechar o trabalho: autor permanece em 531; main permanece em `979fb6c1b6731561f3c993efd6045a9bbf096c54`, 110 commits atrás de 531 e 111 atrás da base 07H. Checkpoint 07H é `725f8fe44`, com cinco serviços, instalador 44 verificações, cumulativos 42 verificações e ZIP **14.379.785 bytes**. 07I é outro commit e outro pacote, sem depender de sessão de muitas horas para retomar.

Pacote 07I abaixo de **30.000.000 bytes**, com incremento sobre 07H, patch binário, instalador transacional, hashes, documentação e cinco bundles cumulativos desde 07H, 531, 4122, 9f e 989. Bundle `cumulative_from_531_07I.bundle` reúne **07H + 07I** para quem ainda está na base solicitada pelo usuário. Integrações e commits do autor permanecem na ancestralidade.

O main atrasado exige a recuperação anterior entregue com o 07G em quatro volumes; o bundle integral grande é excluído deste ZIP. Incremento sobre a base exata; bases antigas pelos bundles. Em divergência, integrar em branch preservando alterações locais. Nada publicado no GitHub.

INSTALL_TEST.json registra instalação real, rejeições, rollback, repetição e builder determinístico. CUMULATIVE_TEST.json comprova importação, árvore, ancestralidade e hashes dos cinco receptores. SHA256_FILES.json cobre o ZIP. **Frontier encerrado como arte V1: 47/47**, com aceitação em ROM/mGBA como etapa seguinte de integração.

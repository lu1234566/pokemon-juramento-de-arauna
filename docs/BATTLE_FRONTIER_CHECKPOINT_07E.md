# Battle Frontier 07E — Battle Pike V1

Os seis mapas passam a usar um par privado de bancos nativos 4bpp. A ambientação combina piso de pedra escura com pequenos encaixes de cobre, cortinas vinho, tapetes tecidos e figuras serpentinas em metal/pedra. Os equipamentos do saguão têm detalhes jade. A sala final recebe uma espiral serpentina própria no piso, sem criar objeto, trigger ou regra. O desenho conserva as silhuetas dos obstáculos e deixa os caminhos contrastados. Os componentes de piso sob as figuras usam o mesmo material das áreas livres.

Master Map Design Bible, concept da Liga e o último checkpoint 07D foram recuperados antes de editar. A Bible governa escala e materiais, e o concept informa a arquitetura institucional. Não existe um concept específico do Pike na Bible; este desenho é uma interpretação nova, sem acrescentar nome ou acontecimento canônico. Os mapas originais e o atlas nativo foram inspecionados. As imagens de entrega são renders dos bancos reais e do map.bin em RGB555, sem sprites.

## Base e GitHub

Base direta: `38d7879ae14817d242ef07ca4f22fb60d3df96da`, cujo pai é o checkpoint 07D `2a1838d000482773bb25a2faffc291b1c26cb756`, sobre `8d7cafa5d7`. A diferença de 38d para o 07D é apenas docs/INTEGRACAO_07D.md. Os 82 arquivos do pacote 07D coincidem por SHA com essa base. Seu ZIP foi recuperado e conferido por SHA, CRC e 92 hashes internos.

main está em `979fb6c1b6731561f3c993efd6045a9bbf096c54`, 104 commits atrás da base conferida. O novo checkpoint parte do integrador. Cinco bundles atendem às bases 38d, 2a/07D, 8d, 9f e 989/06C2, conservando o histórico e as correções entre elas. O incremento source/, changes.patch e install.py exige 38d. Não houve push.

A nota de integração oficial informa build e fotografias mGBA do 07D pelo integrador. Essa evidência vale para o 07D; o novo 07E ainda exige compilação ARM e teste jogável neste ambiente.

## Escopo e preservação

| Mapa | Dimensões | Células | Objetos | Warps do map.json |
|---|---:|---:|---:|---:|
| BattlePikeLobby | 11×13 | 143 | 4 | 3 |
| BattlePikeCorridor | 14×8 | 112 | 1 | 0 |
| BattlePikeThreePathRoom | 13×11 | 143 | 2 | 0 |
| BattlePikeRoomNormal | 9×8 | 72 | 2 | 0 |
| BattlePikeRoomFinal | 5×8 | 40 | 1 | 0 |
| BattlePikeRoomWildMons | 9×20 | 180 | 0 | 0 |

690 células visuais alteradas, dez objetos e três warps declarados. Os warps silenciosos e movimentos coordenados pelos scripts também ficam exatos. Os 754 layouts mantêm IDs, ordem e compartilhamento: só esses seis mudam as referências dos bancos. O layout BattlePikeRoomUnused, sem mapa associado, conserva seu banco e seus pixels. Nada é acrescentado ao inventário de mapas.

Os únicos quatro arquivos anteriores editados são layouts.json e os três cabeçalhos de tilesets, com bloco FRONTIER_07E isolado. 23.431 dependências anteriores ficam congeladas por SHA-256. Grids, bordas, colisão, elevação, atributos, máscaras, scripts, objetos, movimentos, eventos e warps não mudam. battle_pike.c, field_specials.c, field_door.c, overworld.c, frontier_util.c, saves, labels e constantes ficam intactos. Assim são preservados seleção e dicas de salas, RNG, condições de status/cura, encontros selvagens, seleção do grupo, modos de nível, partidas, Lucy, recompensas e progressão.

A água corrigida 0x226 do Palace, seu gerador e documentação, as portas próprias da Tower, os bancos anteriores da Frontier e INTEGRACAO_07D.md permanecem exatos.

## Cortina e capacidade GBA

O C original CloseBattlePikeCurtain/Task_CloseBattlePikeCurtain escreve uma área 3×4: 12 metatiles por atualização e três quadros nos ticks 4, 8 e 12. São 36 IDs dinâmicos, com três redraws e uma retomada do script. Esses quadros recebem a mesma linguagem das cortinas abertas, mantendo IDs, atributos e máscaras. A união dos IDs dinâmicos e estados nomeados nas constantes contém 43 metatiles, todos redesenhados e validados. A prévia separada mostra a cortina aberta e os três quadros, original em cima e novo embaixo.

151 metatiles usados/dinâmicos são redesenhados. Os 355 atributos e 710 máscaras dos dois planos permanecem exatos. Só a paleta 12, antes vazia, recebe materiais; paletas 0–11 ficam iguais. A alocação estática usa 477 slots e deixa 434 livres, excluindo 432–511 e 992–1023. Os bancos continuam dentro de 512 tiles cada e 16 índices por paleta. O primário mantém InitTilesetAnim_Building e os quadros de TV; o secundário mantém NULL.

## Verificações

- Auditoria oficial de mapas: PASS, oito categorias sem erros.
- Static readiness: PASS, composição oficial English e gates completos. O gate estático omite explicitamente a compilação ARM. Saídas ignoradas de 528 mapas e 551 MIDI foram geradas com as ferramentas originais, sem mudar arquivos distribuídos.
- Seletores C originais: 690 células locais, 30.720 fallbacks e 53.167 células anteriores de cavernas/Dive.
- Atributos, máscaras, IDs, paletas, capacidade e slots reservados: PASS.
- Cortina: 80 combinações de ticks/posições com o C original; footprint e IDs conferidos, três quadros, término no tick 12 e uma retomada do script. Serviços de tarefas, grid e redraw são explícitos no host.
- Building: 16 comparações de metatiles em dois quadros; initializer/dispatch/fila originais, 256 ticks e 32 atualizações com payloads nativos 4bpp.
- Os 20 mapas anteriores da Frontier coincidem em 40 comparações de frames. A água 0x226 do Palace coincide com 0x190 em oito quadros nativos.
- Regressões C anteriores de portas, General (256 ticks/80 atualizações) e Dome (865 casos de luz/fade/transição): PASS.
- Instalador: instalação real, hashes, rejeição de corrupção/edições/bases incorretas, rollback, reaplicação sem escritas, HEAD preservado, validação instalada e reconstrução determinística. Resultado em review/frontier_07e/install_test.json.
- Cinco bundles: importação em receptores independentes com bases e ancestrais requeridos, ancestralidade, pai direto, árvore, checkout SHA incluindo paletas CRLF, dependências protegidas e aplicação real do patch. Resultado em CUMULATIVE_TEST.json do pacote.

Limites: os testes C usam serviços do host para VRAM, filas, tarefas, flags, grid e desenho. A lógica Pike é preservada por hash, sem executar interpretador de scripts/batalhas. Compilação ARM e teste jogável de escolhas, status, cura, encontros, partidas, Lucy, suspensão/retomada, saves e sprites no mGBA ficam pendentes. Nenhuma ROM ou save é distribuído.

## Retomada

LEIA_ME.md documenta os comandos de cada rota. O instalador exige a base atual antes de escrever, mantém HEAD, faz backup/rollback e reaplica sem novas escritas. Nos históricos antigos, usar o bundle cumulativo correspondente antes de conciliar mudanças locais numa branch.

Concluídos **26/47 mapas Frontier**; restam 21. Próximo: **07F, três mapas de Battle Pyramid**, com geração procedural a inventariar antes da arte. Plano completo em review/frontier_07e/checkpoint_plan.json.

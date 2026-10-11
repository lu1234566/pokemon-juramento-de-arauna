# 08F — Salas de conexão V1

Cinco mapas adaptados sobre `f0f08e4ed2edea95963f979fb81a82dbb8b53400`,
a integração do 08E. As salas recebem materiais da Sede da Liga e do Centro
Comunitário, com a tecnologia de comunicação mantida como equipamento público:
madeira, pedra clara, bronze, vidro verde e sinalização legível dos participantes.
Este pacote encerra a fila de mapas ativos em bancos nativos de Hoenn.

## Checkpoints

| Checkpoint | Mapas | Ambientação | Estado |
|---|---|---|---|
| 08F1 | BattleColosseum_2P, BattleColosseum_4P | Quadras de madeira da Liga, molduras de bronze, marcações claras | PASS_STATIC |
| 08F2 | RecordCorner, TradeCenter | Arquivo de registros e terminal de troca, lajes claras e equipamento verde/bronze | PASS_STATIC |
| 08F3 | UnionRoom | Salão comunitário de comunicação, recepção em madeira, círculo central em bronze | PASS_STATIC |

São 740 células: duas arenas de 14×9, RecordCorner de 20×10, TradeCenter de
12×9 e UnionRoom de 15×12. Os dois Colosseums compartilham um par de bancos
privados, mas conservam suas próprias grades, saídas e gatilhos. As outras
três salas têm pares exclusivos; são quatro pares, oito bancos privados.
Os registros estão em `review/connections_08f/08F1.json` a `08F3.json`.
Arte e verificações estáticas estão concluídas. Sessões reais ainda precisam
de aceitação no emulador com participantes compatíveis.

## Recuperação e direção artística

A Master Map Design Bible, os 82 concepts canônicos e a integração mais recente
foram recuperados antes de editar. Seus hashes foram conferidos. Foram vistos
os concepts Centro Comunitário, Sede da Liga — Interior e Arquivo Central /
Horizonte. A Bible estabelece a autoridade de scripts, flags, warps e progressão,
a leitura em 240×160 e, na p.44, o contraste entre ciência pública e tecnologia
apropriada pelo Consórcio. Não há capítulo específico das cinco salas Link;
os materiais são uma interpretação das referências, não uma nova localização
na história. O equipamento do Arquivo inspira a forma dos terminais, sem tornar
estes serviços parte do Consórcio.

As arenas usam tábuas com juntas alternadas, textura discreta e paredes com
detalhes de bronze. O contorno da quadra e os pontos dos participantes continuam
legíveis. Registros e trocas conservam mesas, cadeiras, máquinas e sinais de
cores distintos, sobre lajes grandes. A UnionRoom mantém o salão livre para
os grupos e o círculo de encontro; sua faixa vermelha vira recepção de madeira.
Não foram adicionados obstáculos nem objetos de evento de decoração.

O ZIP 08E anterior, SHA-256
`cf84655bbeacfaf058a6ddf732e8cc13bf3dd1a20aadd7a35b9458bf26d3c866`,
foi conferido por CRC e hashes internos. Os 246 arquivos do manifesto coincidem
com esta base integrada; os três bundles apontam para `76d76ddfe5` e passam
na verificação Git. A integração do 08E não precisou corrigir o pacote.
`review/connections_08f/recovery.json` registra essa conferência.

A branch atualizada do GitHub apontava exatamente para `f0f08e4ed2`.
O main `979fb6c1b6` estava 130 commits atrás desta base. Os novos cumulativos
partem do 08E do autor e de `a594b3e1e6`, preservando o histórico intermediário.
Não são bundles para recuperar diretamente do main. Não houve push desta autoria.

## Preservação funcional

- Os 754 IDs de layout e sua ordem permanecem iguais; somente os bancos dos
  cinco layouts são alterados.
- Todos os arquivos de mapa, grades, bordas, colisões, elevações, eventos,
  scripts, músicas, clima, flags, progressão e dados salvos são idênticos à base.
- Os 14 warps continuam com retorno `MAP_DYNAMIC / WARP_ID_DYNAMIC`; os
  12 gatilhos de batalha, assentos de troca e registros mantêm posição e script.
- O Cable Club mantém as chegadas em 2P `(6,8)`, 4P `(5,8)`, TradeCenter `(5,8)`,
  RecordCorner `(8,9)` e UnionRoom `(7,11)`, além das condições de entrada e saída.
- Seleção de equipe para batalha 4P, início/cancelamento de batalha e troca,
  mistura de registros, presentes, retorno e salvamento permanecem no código original.
- Os oito centros de grupos da UnionRoom e seus cinco offsets continuam no C
  original. As 40 posições foram conferidas, sem novos obstáculos. A criação
  dos avatares, paletas de sessão e ativação/desativação da colisão não mudam.
- As trocas de metatiles do script compartilhado Cable Club acontecem nos
  balcões dos Centros Pokémon e em Mossdeep, que estão congelados. Não são
  transferidas indevidamente para os bancos novos destas salas.
- IDs dos metatiles, todas as tabelas de atributos, máscaras das duas camadas,
  paletas 0–11 e callbacks são preservados. Os metatiles não redesenhados mantêm
  os pixels originais. A paleta 12 estava sem referências no banco original.
- O formato de gráficos continua o original: Building comprimido, CableClub
  sem compressão, UnionRoom comprimido. Os slots de DMA de Building, incluindo
  a TV nos slots 496–499, continuam protegidos.

O contrato congela 24.843 arquivos anteriores, incluindo todo o código e as
correções visuais de Centro 07H, Palace, `field_door.c`, `overworld.c` e todos
os checkpoints já instalados. Os quatro registros controlados ficam fora dessa
lista: `layouts.json`, `graphics.h`, `metatiles.h`, `headers.h`. O validador
restaura as cinco referências antigas e remove somente a seção 08F dos
registros de gráficos para compará-los com a base.

### As sete correções protegidas

| Arquivo | SHA-256 |
|---|---|
| src/party_menu.c | e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f |
| src/field_player_avatar.c | 81ebe4b5761f8992cb459cf37978262358231734a1c56f8b3447346f770db95f |
| src/scrcmd.c | 98cd4b72474c3cc7dfd5dc6cf54a4a96f807733017761a2be58d62b0dcd063a9 |
| data/maps/SlateportCity_Harbor/scripts.inc | fc256e12cb37712c2a2b3e026d442e6baa55ed6560909e7cadecda83c19167ea |
| data/maps/LilycoveCity_Harbor/scripts.inc | 46ab224e74a02b311a9a38b0eb8f940b169e9e5d83844283ccda00be39ebd18c |
| data/maps/FallarborTown_CozmosHouse/scripts.inc | 798dc439a26a33d0845646eab56d599d7712e34414c712304d834ae4eb89f4a6 |
| data/maps/Route116/scripts.inc | cd955b92f802f347645b82cc1bc54aa1715d35097009f7504ec98079c46a62c5 |

Os contratos históricos permanecem intactos, com suas diferenças documentadas:
08B1 sete arquivos, 08B2 seis, 08B3 e 08C quatro scripts cada. 08D e 08E não
têm divergências. O validador 08F verifica exatamente esses conjuntos.

## Verificação concluída

O validador passou: 231 instâncias de metatiles redesenhadas nos quatro pares,
462 máscaras de camada verificadas, 618 metatiles não redesenhados com pixels
idênticos, 26 pontos de evento livres e 40 posições de grupos livres.
Os pares usam 114, 154, 158 e 115 novos slots estáticos respectivamente,
sem ocupar os reservados para DMA. Folhas, referências, compressão e índices
de 4 bits foram conferidos. Os cinco mapas completos e seus comparativos
foram vistos; os renders usam RGB555 sem atores e não são capturas do mGBA.

Os seis gates gerais passaram: dados de mapas, proteção visual, capacidade de
paletas, espécies especiais, identidade das facções e assets de personagens.
O `mapjson` do host compilou e gerou headers de mapas/layouts. Logs, validador
e inventário ficam em `review/connections_08f`.

O instalador verifica todo o payload e o contrato antes de escrever, recusa
versões desconhecidas, gera backup, restaura arquivos se houver falha e escreve
zero ao reaplicar. Os 17 casos incluem preflight, sete versões antigas das
correções, payload corrompido, Centro alterado, código de ocupação Wireless
alterado, registro editado, base obsoleta, falha na segunda escrita, instalação,
reaplicação e rollback manual. O teste preliminar fica no source; o resultado
do payload final fica em `INSTALL_TEST.json`, na raiz do ZIP.

Os três bundles são importados em checkouts de suas respectivas bases,
comparando commit, árvore e hashes de todos os arquivos rastreados, incluindo
as sete correções. `CUMULATIVE_TEST.json` registra o resultado. Os testes usam
worktrees com armazenamento de objetos Git compartilhado; não representam
um clone vazio. O ZIP inclui source, contratos, manifesto, patch binário,
instalador, testes, previews e bundles; tem hashes internos e deve ficar abaixo
de 30.000.000 bytes. Não inclui ROM nem save.

## Aceitação ainda pendente

Não há compilador ARM nem mGBA disponíveis neste ambiente. A ROM nova não foi
compilada aqui, e nenhum teste estático representa uma sessão multiplayer real.
Depois de integrar, conferir com scripts ligados:

1. Entrada pelos Centros Pokémon e retorno ao Centro de origem em cada serviço.
2. Batalhas reais 2P e 4P, escolha de equipe, cancelamento e retorno pós-batalha.
3. Troca real nos dois assentos, animação, dados dos Pokémon e save/reload.
4. Mistura de registros entre participantes, presentes e saída.
5. UnionRoom com grupos RFU, spawn/despawn, colisão, interações, chat, convites
   para batalha/troca, cancelamento, desconexão e retorno dinâmico.

A aceitação real dos concursos do 08E está em `docs/INTEGRACAO_08E.md`.
Ela não incluiu uma sessão Link e não deve ser atribuída a este 08F.

## Fechamento da fila

| Situação no inventário de 528 mapas | Quantidade |
|---|---:|
| Mapas com bancos Arauna | 504 |
| Módulos gerados da Battle Pyramid | 16 |
| Mapas inativos preservados | 8 |
| Mapas ativos ainda em bancos Hoenn | 0 |

Após integrar este checkpoint, a próxima etapa é a aceitação final do ciclo
de mapas, mantendo as sete correções e as proteções visuais. Esse fechamento
da fila de arte não substitui as verificações reais pendentes de multiplayer.

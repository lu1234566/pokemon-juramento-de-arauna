# 08E — Concursos V1

Seis mapas adaptados sobre `e740b80190d1e0a5c18e2536b1705a2795f943a7`,
a integração documentada do 08D. O palco mantém o funcionamento dos concursos
e recebe os materiais do centro comunitário de Arauna: madeira trabalhada,
pedra clara, bronze, tecidos e bandeirinhas. A arte usa metatiles nativos de
16×16, gráficos de 4 bits e paletas compatíveis com RGB555.

## Checkpoints concluídos

| Checkpoint | Mapas | Direção visual | Estado |
|---|---|---|---|
| 08E1 | ContestHall, ContestHallCool | Palco comunitário; tecido urucum em Cool | PASS_STATIC |
| 08E2 | ContestHallBeauty, ContestHallCute | Azul do litoral e tecido rosado | PASS_STATIC |
| 08E3 | ContestHallSmart, ContestHallTough | Verde da mata, ocre e bronze | PASS_STATIC |

Cada sala tem 15×11 células; são 990 células no conjunto. Os seis layouts
usavam General + Contest. Agora usam seis pares privados de bancos, um por
tema, sem tocar no banco do lobby nem nas fachadas dos outros concursos.
Os registros dos checkpoints estão em `review/contests_08e/08E1.json` a
`08E3.json`. São conclusões de arte e verificação estática; concursos reais
no mGBA ainda precisam de aceitação.

## Referências recuperadas antes da edição

A Master Map Design Bible e os 82 concepts canônicos tiveram seus hashes
conferidos. Foram vistos os concepts Centro Comunitário e Bravamar, e lida
a passagem da Casa da Fogueira, p.42, sobre um salão que recebe a comunidade.
A Bible não contém um capítulo específico destes seis concursos. A proposta
de festival é uma interpretação dessas referências, mantendo a função original.

O palco recebeu tábuas com juntas alternadas, veios discretos e pregos;
a plateia fica sobre lajes de pedra. As bordas existentes viraram molduras de
madeira e bronze, e a viga superior carrega bandeirinhas tecidas. As categorias
se distinguem pelo tecido dos degraus e pelo pequeno painel do palco. Os troféus
continuam legíveis em ouro. Não foram acrescentados obstáculos ou objetos de
evento apenas para decorar; os participantes e a plateia conservam seus lugares.

O ZIP 08D anterior, SHA-256
`6060955f88bf2be0926d5e00ffb96325c2f27b165b89ef204ef054bbcd479e83`,
foi recuperado e conferido: CRC, hashes internos, os 215 arquivos do manifesto
contra esta base e os três bundles contra o commit `c6143a5173`.
`review/contests_08e/recovery.json` guarda o resultado. A integração 08D não
alterou esses arquivos; acrescentou seu documento de aceitação.

A branch do projeto foi atualizada do GitHub e apontava exatamente para
`e740b80190`. O main `979fb6c1b6` estava 128 commits atrás desta base.
Os novos cumulativos partem do 08D do autor e de `a594b3e1e6`, e incluem
o histórico das correções. Não são bundles para recuperar diretamente do main.

## O que foi preservado

- Os 754 IDs de layout e sua ordem; apenas os bancos dos seis layouts mudam.
- Todos os `map.json`, `map.bin`, `border.bin`, flags, colisões, elevações,
  objetos, scripts, música, clima, conexões e progressão, byte a byte.
- As cinco categorias continuam compartilhando eventos e scripts de ContestHall.
- Os pontos de chegada das cinco categorias continuam em `(7,5)`; as quatro
  classes retornam ao lobby em `(14,4)` e Link em `(15,4)`.
- As inscrições, escolha do participante, apresentação, movimentos, plateia,
  apelos, pontuação, fitas, Luxury Ball, pinturas, salvamento e sincronização
  Link/Wireless mantêm a lógica original.
- As trocas de metatiles da entrada do lobby continuam no banco já adaptado
  do lobby. Os scripts compartilhados do palco não trocam metatiles.
- Todas as tabelas completas de atributos dos bancos permanecem iguais;
  as máscaras de ambas as camadas, callbacks e áreas de DMA foram preservados.
- As paletas 0–11 e os metatiles que não receberam arte são idênticos. A paleta
  12 estava sem referências ativas no banco original e recebe os materiais novos.

O contrato congela 24.600 arquivos anteriores. Só ficam fora dele os quatro
registros controlados: `layouts.json`, `graphics.h`, `metatiles.h` e `headers.h`.
O validador restaura as seis referências antigas e retira apenas a seção 08E
dos três registros de gráficos para provar a igualdade com a base.

### Sete correções protegidas

| Arquivo | SHA-256 congelado |
|---|---|
| src/party_menu.c | e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f |
| src/field_player_avatar.c | 81ebe4b5761f8992cb459cf37978262358231734a1c56f8b3447346f770db95f |
| src/scrcmd.c | 98cd4b72474c3cc7dfd5dc6cf54a4a96f807733017761a2be58d62b0dcd063a9 |
| data/maps/SlateportCity_Harbor/scripts.inc | fc256e12cb37712c2a2b3e026d442e6baa55ed6560909e7cadecda83c19167ea |
| data/maps/LilycoveCity_Harbor/scripts.inc | 46ab224e74a02b311a9a38b0eb8f940b169e9e5d83844283ccda00be39ebd18c |
| data/maps/FallarborTown_CozmosHouse/scripts.inc | 798dc439a26a33d0845646eab56d599d7712e34414c712304d834ae4eb89f4a6 |
| data/maps/Route116/scripts.inc | cd955b92f802f347645b82cc1bc54aa1715d35097009f7504ec98079c46a62c5 |

Centro 07H, água do Palace, `field_door.c`, `overworld.c`, lógica das ilhas
lendárias e todos os pacotes anteriores também ficam congelados.
Não foram reescritos contratos antigos: 08B1 conserva suas sete divergências
documentadas, 08B2 seis, 08B3 e 08C quatro scripts cada; 08D não tem divergência.
O validador 08E verifica exatamente esses conjuntos.

## Verificações

O validador 08E passou: 204 instâncias de metatiles redesenhadas, 408 máscaras
de camada verificadas, 4.266 metatiles restantes com pixels idênticos, 65 novos
slots estáticos seguros por par de bancos e 79 posições de plateia criadas pelos
scripts conferidas. As folhas mantêm no máximo 512 tiles por banco, índices
de 4 bits e todas as referências válidas. Nenhum slot reservado de DMA foi usado.

Os seis gates gerais passaram: dados de mapa, proteções visuais, capacidade
de paletas, espécies especiais, identidade das facções e assets de personagens.
O `mapjson` do host compilou e gerou os headers de mapas e layouts. Os logs
estão em `review/contests_08e/logs`; os renders completos, individuais e
comparativos foram vistos para os seis mapas. Os PNGs mostram RGB555 sem atores
e não são capturas do emulador.

O pacote inclui instalador que verifica todo o conteúdo antes de escrever,
recusa alterações desconhecidas, faz backup e restaura os arquivos se uma
escrita falhar. O teste exercita 17 casos: preflight, as sete versões antigas
das correções, payload corrompido, Centro alterado, código de concursos alterado,
registro editado, base obsoleta, falha na segunda escrita, instalação efetiva,
reaplicação e rollback manual. Os registros do payload preliminar e do final
são separados; o final fica em `INSTALL_TEST.json` na raiz do ZIP.

Os três bundles são verificados e importados em checkouts das suas respectivas
bases, com comparação da árvore inteira e hashes de todos os arquivos rastreados.
O resultado fica em `CUMULATIVE_TEST.json`. Esses testes usam worktrees com
armazenamento de objetos Git compartilhado; não representam um clone vazio.
O ZIP final inclui manifesto, patch binário, contratos, código, imagens,
instalador, bundles e hashes internos. Não inclui ROM nem save e deve ficar
abaixo de 30.000.000 bytes. Não houve push desta autoria.

## Aceitação ainda pendente

Não há compilador ARM nem mGBA disponíveis neste ambiente. A ROM nova e um
concurso completo por categoria ainda não foram executados. Na integração,
conferir com scripts ligados: inscrição e entrada, apresentação dos quatro
participantes, rodadas de apelos, resultados, vitória e derrota, entrega da fita,
Luxury Ball/pintura quando elegível, retorno ao lobby e save/reload. Testar os
quatro ranks e, em sessão compatível, o fluxo Link/Wireless e suas paletas.
Isso não é substituído pela igualdade dos scripts. A aceitação real do 08D
anterior está em `docs/INTEGRACAO_08D.md` e não deve ser atribuída a este 08E.

## Fila após 08E

O inventário dos 528 mapas registra 499 com bancos Arauna, 16 módulos gerados
da Pyramid, oito mapas inativos preservados e cinco salas de conexão restantes:
BattleColosseum_2P, BattleColosseum_4P, RecordCorner, TradeCenter e UnionRoom.
São o 08F. O próximo pacote deve partir do commit resultante da integração
do 08E e continuar protegendo os sete arquivos e as correções visuais anteriores.

# Arauna — Checkpoint 03B: Sealed Chamber, Ancient Tomb e Island Cave

Base obrigatória: `7cb02987e896535f8b445290883ff0022a989a52`.

Os quatro mapas receberam composição mineral própria por bancos gráficos privados: arquivo de pedra úmida nas duas salas de Sealed Chamber, rocha cinza com veios ocres em Ancient Tomb e pedra fria em Island Cave. As inscrições e as peças que fecham e abrem as portas permanecem exatamente como na base, incluindo pixels, paletas, atributos e referências. A arte mineral nativa já produzida no 03A foi reutilizada; nenhum concept é apresentado como captura do jogo.

## Referências e base instalada

A Master Map Design Bible, os 82 concepts e o pacote 03A foram recuperados antes da edição. Os 83 arquivos de referência conferem por SHA-256. O suplemento desta etapa está em `CAVERNAS_03B_DESIGN.md`.

O GitHub aponta a branch `claude/pokemon-juramento-arauna-fhk6ah` para a base `7cb02987e8`, 83 commits à frente de `main` (`979fb6c1b6`). Dos 94 arquivos do pacote 03A, 93 coincidem com a instalação. A única diferença é o relatório 03A, ampliado pelo integrador com a compilação de ROM e testes em mGBA. O contrato funcional da base anterior `bcd93e980e` continua íntegro. As auditorias anteriores dos cumulativos Sul/Pampa + Uivo e Rota 103 V1.2 foram mantidas; os overlays antigos não foram reaplicados sobre a instalação mais recente.

## Escopo entregue

| Mapa | Dimensão | Células com visual alterado | Warps mantidos |
|---|---:|---:|---:|
| SealedChamber_OuterRoom | 21×23 | 434 | 1 |
| SealedChamber_InnerRoom | 21×23 | 473 | 1 |
| AncientTomb | 17×33 | 544 | 3 |
| IslandCave | 17×33 | 544 | 3 |

São 2.088 células, 8 warps, 2 objetos lendários e 44 eventos de inscrição preservados. Nenhum `map.bin`, `border.bin`, `map.json`, script, encontro, flag ou condição de progressão foi alterado. Entre os 744 layouts, somente o campo `secondary_tileset` desses quatro mudou. As demais alterações em arquivos preexistentes são adições aos registros gráficos e à tabela do seletor visual já instalado; o código do motor permanece intacto.

## Contratos dos puzzles

- Sealed Chamber externa: Dig continua permitido em `(9,3)`, `(10,3)` ou `(11,3)`, antes de `FLAG_SYS_BRAILLE_DIG`. O retorno Dive e Escape continua em `MAP_UNDERWATER_SEALED_CHAMBER, 12, 44`.
- Sealed Chamber interna: Wailord primeiro e Relicanth por último, na ordem herdada de Emerald. Mensagens, tremor e `FLAG_REGI_DOORS_OPENED` permanecem intactos.
- Ancient Tomb: Flash continua condicionado à posição `(8,25)` e à flag original de conclusão. Encontro, captura, fuga e remoção de Registeel estão preservados.
- Island Cave: leitura da inscrição, início/reset/falha temporários, as 36 casas do perímetro, máscaras `FFFF/FFFF/000F` e retorno a `(8,21)` permanecem iguais. A saída em `(8,29)` conserva seu comportamento de warp direcional; ela faz parte do perímetro original. Encontro e resultados de Regice estão preservados.
- Desert Ruins ficou fora da arte, mas seus scripts e a função compartilhada do puzzle de Regirock foram verificados e protegidos.

Os IDs `0x229`, `0x22A–0x22C` e `0x232–0x237` mantêm os dados nativos. Os três conjuntos de porta foram conferidos nos estados fechado e aberto. Quando um script troca um ID, o seletor real retorna esse ID nativo; quando ele coincide com o ID armazenado na base, as casas da porta também não recebem aliases. Isso evita que a arte esconda uma passagem aberta ou restaure visualmente uma porta fechada.

## Verificação concluída

- SHA-256 de **17.785 arquivos de jogo preexistentes** protegidos; 740 layouts alheios intactos. Mais 19 dependências externas de arte/grades visuais nativas conferidas e protegidas no instalador.
- **53 verificações** compilando e executando os corpos reais das funções de `src/braille_puzzles.c` e o escritor de `src/fieldmap.c`. Incluem casos positivos e negativos, volta física contínua de Regice, volta incompleta, flags, ordem da equipe e writes nativos com elevação preservada. Áudio, tarefas e acesso à equipe são stubs de host; o interpretador de scripts não foi emulado. As ramificações dos scripts são preservadas por comparação integral dos arquivos.
- Seletor C de produção: 2.088 células novas, 6.280 casos de fallback/limite e 12.003 células dos 18 casos anteriores, incluindo o 03A.
- 36 verificações de peças de portas nos estados fechado/aberto; Braille gráfico, 22 mensagens e fonte preservados.
- Bancos 4bpp, RGB555, referências aos tiles e paletas 0–12 conferidos; slots de animação excluídos da alocação. Três bancos de 432 tiles gráficos, dentro da capacidade secundária de 512.
- Auditoria oficial: 8/8 checks de mapas em 528 mapas; gates estáticos oficiais completos aprovados, inclusive 189/189 checks de protagonista.
- Prévias reproduzíveis: quatro mapas integrais, 12 pares antes/depois em 240×160 e três pares de portas fechadas/abertas, produzidos pelo seletor C real e tiles nativos. São renders de host sem sprites, não screenshots de emulador.

## Instalação e limite da validação

O ZIP contém instalador com preflight de SHA-256, bloqueio de base/local edits desconhecidos, backup e rollback, reaplicação idempotente, patch binário e bundle Git. **18/18 testes do instalador passaram**, incluindo corrupção do payload, alterações locais em Braille/scripts, dependências do 03A, rejeição do main atrasado, rollback após falha na terceira escrita, instalação e reaplicação. O resultado acompanha o pacote em `INSTALL_TEST.json`. O instalador não faz commit nem push.

Este 03B ainda precisa de **compilação ARM de ROM e validação em mGBA pelo integrador**: a toolchain e o emulador não estão disponíveis neste ambiente. A validação em mGBA do 03A é histórica e não é atribuída ao 03B. A etapa de produção, preservação e entrega do pacote 03B está concluída; sua instalação externa não é presumida.

A próxima etapa é o **03C: Altering Cave + Artisan Cave**, sobre a base resultante da instalação do 03B. Depois vêm os 12 mapas Dive e o Safari, em checkpoints separados.

## Verificação na instalação

- O instalador foi aplicado sobre `7cb02987e8`. A árvore resultante é
  idêntica à do bundle `5e6b18ec20`. `validate_cavernas_03b.py` aprova antes
  e depois da correção abaixo.
- Correção na instalação: as saídas para o sul das salas internas tinham
  sumido.
  - O builder marca os warps com `exit_floor`, mas o 0x207 da casa do warp
    é imutável e não recebe alias. A fileira abaixo, com o buraco oval
    (`0x258–0x25A` no Ancient Tomb e na Island Cave, `0x2E5–0x2E7` na Sealed
    Chamber interna), virou parede lisa.
  - Essas três células voltam ao ID nativo nas três grades visuais, e a
    saída fica visível como no Emerald. Os atributos são os mesmos e o
    seletor C continua coerente.
  - Fica pendente para o autor uma saída desenhada no estilo novo, junto com
    as peças de porta e inscrição, que hoje mantêm a arte marrom original.
- Build `en` ok (ROM em 57,0%). Gates aprovados: 189/189, 95/95, 0
  candidatos de resíduo, as oito verificações de mapas e
  `variantes_troca_layout.py --verificar` 9/9. Nenhum símbolo de harness
  na ROM.
- Legibilidade na visão de câmera: no Ancient Tomb e na Island Cave havia
  16 paredes com desenho de piso e 48 pisos com desenho de parede. Agora são
  0. As salas da Sealed Chamber já eram 0 e continuam 0.
- Emulador:
  - As portas aparecem fechadas no estado padrão e abertas com
    `FLAG_SYS_BRAILLE_DIG`, `FLAG_SYS_REGISTEEL_PUZZLE_COMPLETED` e
    `FLAG_SYS_BRAILLE_REGICE_COMPLETED`.
  - A pé, a porta aberta leva à sala interna e a saída corrigida leva de
    volta, nas três cavernas.

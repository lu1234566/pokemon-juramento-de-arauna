# Battle Frontier 07C — Battle Palace + Battle Arena V1

Seis salas recebem bancos privados. Palace combina terracota, pedra, pátio de água e plataforma de combate; Arena usa madeira, pedra e um tapete de fibra com a marca de combate legível. Referências: Master Map Design Bible, concept da Liga e último checkpoint 07B recuperados e conferidos antes de editar. Novos materiais respeitam as máscaras e o papel de cada superfície.

## Base e conciliação do GitHub

O 07C parte diretamente da base oficial `9f0a056e90fd42fa426030aca2f2e241401c0700`. Ela incorpora o 07B `868226c157fc24b36c24ebfc3ac0c6b83008bae7` por merge e conserva a correção Tower `52e6f87e1b9e0b9452de3c40383440622a30f35a`. O baseline local anterior 8fb e a integração oficial têm código e arte idênticos; só docs/INTEGRACAO_07B.md foi acrescentado na base oficial. Essa documentação também fica protegida por hash. main segue em `979fb6c1b6731561f3c993efd6045a9bbf096c54`, 100 commits atrás de 9f.

A arte 07C não modifica field_door.c ou overworld.c. O primeiro conserva a versão nova do GitHub, com dispatch e imagens próprias das portas Tower; o segundo conserva a correção anterior. As sete alterações Tower e o registro da integração 07B permanecem exatos. O commit original do 07B segue no histórico. Não houve push.

## Escopo

| Mapa | Dimensões | Células | Objetos | Warps |
|---|---:|---:|---:|---:|
| BattlePalaceLobby | 25×12 | 300 | 6 | 3 |
| BattlePalaceCorridor | 17×14 | 238 | 7 | 4 |
| BattlePalaceBattleRoom | 15×10 | 150 | 5 | 2 |
| BattleArenaLobby | 16×13 | 208 | 5 | 1 |
| BattleArenaCorridor | 18×14 | 252 | 1 | 0 |
| BattleArenaBattleRoom | 16×11 | 176 | 9 | 0 |

1.324 células, seis layouts exclusivos, três pares de bancos privados. Todos os IDs e a ordem dos 754 layouts permanecem iguais. Os únicos arquivos anteriores editados pela arte são layouts.json e três cabeçalhos de bancos, com bloco append isolado. Grids, bordas, colisão, atributos e máscaras dos dois planos permanecem iguais. Scripts, objetos, movimentos, eventos, warps, autonomia Palace, julgamento Arena, treinadores, recompensas, saves e progressão são preservados por hash.

284 metatiles recebem arte entre os três pares. Os 1.053 atributos e 2.106 máscaras de planos permanecem exatos. As 12 células dos footprints de portas mantêm pixels originais, paletas e gráficos nativos. Todos os bancos usam 4bpp e no máximo 512 tiles; a alocação estática exclui 432–511 e 992–1023. Apenas a paleta antes não usada 12 recebe materiais; paletas 0–11 permanecem exatas.

## Animação e verificações

- 23.186 dependências anteriores congeladas por SHA-256, incluindo a manutenção GitHub, todos os mapas e checkpoints prévios e as duas engines protegidas.
- Seletores C originais: 1.324 células locais, 30.720 fallbacks e 53.167 células anteriores de cavernas/Dive.
- Os 11 mapas anteriores da Frontier mantêm seus renders em relação ao baseline integrado.
- Portas C originais: 1.028 roteamentos, 16 casos de desenho/flags e dez casos específicos de Dome, Palace e Arena. As rotas próprias da Tower corrigidas pelo GitHub e as portas Trainer Hill são verificadas.
- Nove metatiles animados do General ficam intactos nos oito quadros: 72 casos. C original de InitTilesetAnim_General, dispatch e suas cinco filas: 256 ticks, 80 atualizações, payloads 4bpp completos das imagens nativas, água com oito quadros e flores na sequência 0/1/0/2. O renderer acompanha as tabelas canônicas.
- Regressão do Dome: 865 casos de luz/fade/transição do C original, além dos renders anteriores.
- Auditoria oficial de mapas e static readiness: PASS; logs anexos. O gate estático pula explicitamente a compilação ARM.
- Instalação real, rejeição de corrupção/edições/bases incorretas, rollback, idempotência e reconstrução determinística: resultados em review/frontier_07c/install_test.json.
- Importação dos quatro bundles e patch: CUMULATIVE_TEST.json no pacote final. Cada receptor começa com a base declarada e os requisitos ancestrais do bundle. Como há um merge, ancestrais comuns podem ser requisitos do bundle.

Limites: C executado no host com serviços explícitos para filas/VRAM, tarefas, flags e desenho. Scripts e lógica de combate são preservados por hash, sem executar interpretador de batalhas/scripts, partidas, saves ou uma ROM. Compilação ARM e mGBA continuam pendentes neste ambiente. Prévias são renders RGB555 sem atores, não capturas do emulador.

## Retomada

O bundle checkpoint_BattleFrontier_07C.bundle acrescenta o 07C sobre a base atual 9f0a056e90. Os cumulativos importam o resultado completo sobre 07B/868, GitHub antigo/52e ou 06C2/989, incluindo a integração oficial 9f. O incremento source/, changes.patch e install.py exige 9f0a056e90; não aplicar diretamente às outras bases nem ao antigo baseline 8fb. O instalador verifica toda a base antes de escrever, conserva HEAD, cria backup e rollback e reaplica sem novas escritas. LEIA_ME.md contém os comandos específicos de cada rota.

Concluídos 17/47 mapas Frontier; restam 30. Próximo checkpoint 07D: três mapas de Battle Factory. Plano completo em review/frontier_07c/checkpoint_plan.json.

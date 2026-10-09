# Battle Frontier — checkpoint 07A / Battle Tower V1

Base autoritativa: `7e9d29dc5fdab047ac663dd2953a83ff9a51c0b8`.
Checkpoint recuperado: 06C2 `989c33c94fb89b92c5f608f78233fdd8deded4c4`.

**Sete mapas concluídos, seis layouts existentes, nenhum layout acrescentado.** Lobby, elevador, corredor, arena, sala de parceiros Multi, corredor Multi e arena Multi. Os dois modos continuam compartilhando o layout da arena. A base atual já contém 06A, 06B, 06C1, 06C2 e as correções do integrador.

A Master Map Design Bible, os concepts e o pacote 06C2 foram recuperados antes das edições. ZIP anterior conferido por SHA-256, CRC e 92 hashes internos; seus 83 arquivos de incremento continuam exatos na base GitHub. O ramo integrador está em 7e9; main `979fb6c1b6` está 95 commits atrás. Dados em review/frontier_07a/recovery.json.

## Ambientação e implementação

Pavilhão de provas com tábuas largas, fibras discretas, frisos de bronze, pedra cinza e vegetação verde fria. Referência: linguagem material global da Bíblia e pedra/bronze da prancha da Liga. A Torre mantém sua função de desafio, sem criar nomes, lore ou progressão. O piso sob painéis e mobiliário acompanha o novo material; a arena tem placas de pedra e emblema central legível. 130 metatiles recebem camadas indexadas e texturas nativas.

Um par privado de bancos mantém callbacks `InitTilesetAnim_Building` / `NULL`. IDs, todos os atributos, grids de 16 bits, bordas, colisões, elevações, máscaras das duas camadas, geometria, eventos, scripts, equipes, regras, recompensas, parceiros, câmera Multi e dados de link preservados. Paletas 0–11 ficam exatas; a paleta 12, antes sem referências, contém os materiais novos. Reservas de animação não recebem novos gráficos. Nenhum banco original é alterado.

## Engine e portas

`field_door.c`: SHA-256 `8c44134af9a2b77d2cf03c1cffdf81b6b8015977b1f04d78a8dfb0903758e8da`.
`overworld.c`: SHA-256 `312489b537e07f068952004c23cc503837d547af610354225d7325315d3e18aa`.

Ambos são idênticos a 7e9. As duas imagens e o gerador das portas novas do Trainer Hill também estão preservados. Sem nova migração de layout: saves continuam lendo os mesmos IDs. Portas da Torre, seus metatiles superiores e inferiores, estados de passagem 0x207/0x20F e a paleta 7 mantêm os pixels nativos. O corredor Multi conserva as portas de 32 px e a abertura sincronizada da porta distante via variáveis.

## Verificação

- 23.003 arquivos anteriores preservados por SHA-256, incluindo ferramentas, conceitos e todos os pacotes anteriores.
- 950 células nativas, 517 atributos e 1.018 máscaras de camadas comparados. Contagem de células visualmente alteradas por mapa em validation.json.
- Código C de produção: 950 células e 35.840 fallbacks de selector, além de 53.167 células anteriores de cavernas/Dive.
- Portas C de produção: 1.026 decisões de roteamento e 16 casos de desenho/flag/posição, incluindo dispatch do Trainer Hill e os dois tamanhos de porta. Serviços de host explícitos.
- Auditoria oficial de mapas 8/8 e static readiness oficial English PASS. Fontes restaurados e hashes reconferidos após a composição.
- Instalador: 43/43 testes reais em checkout isolado, cobrindo rollback, corrupção, dependências, bases desconhecidas, idempotência, validação instalada e builder determinístico. Evidência em review/frontier_07a/install_test.json e INSTALL_TEST.json.
- Cumulativos sobre 7e9 e 989: verificações reais de import, árvore, checkout e engine em CUMULATIVE_TEST.json.

Compilação ARM, mGBA, batalhas, sprites e sessões de link continuam pendentes: as ferramentas ARM/mGBA não estão disponíveis. Não há ROM, ELF, save ou biblioteca temporária no pacote. Prévias são renders RGB555 dos grids/bancos nativos sem atores/clima; estados de portas são fixtures de revisão e não são instalados em mapas.

## Etapas dos 47 mapas

| Checkpoint | Mapas | Escopo |
|---|---:|---|
| 07A | 7 | Battle Tower — concluído |
| 07B | 4 | Battle Dome |
| 07C | 6 | Battle Palace + Battle Arena |
| 07D | 3 | Battle Factory |
| 07E | 6 | Battle Pike |
| 07F | 3 | Battle Pyramid, geração procedural |
| 07G | 10 | Nove lounges + casa de Scott |
| 07H | 5 | Ranking, trocas, Center (dois pisos) e Mart |
| 07I | 3 | Dois exteriores + Reception Gate |

Restam 40. Próximo pacote: 07B, Battle Dome, quatro mapas. A Pyramid e os exteriores precisam de revisão própria de geração, animações e warps. O plano completo de nomes está em review/frontier_07a/checkpoint_plan.json.

# Arauna — Battle Frontier 07G: lounges e casa de Bento V1

Base oficial `eb49778fa84f058c496fdcdcdacc4888e3602c97`, posterior ao 07F original `fd298f4467329eddfa8f65f57f9ee88ab365e3e2`. Esta etapa entrega nove lounges e a casa de Bento, ainda `ScottsHouse` nos símbolos técnicos. **39 de 47 mapas Frontier com arte concluída; oito restantes**, em 07H (cinco serviços) e 07I (três exteriores). O pacote permite integrar este checkpoint sem depender da execução dos dois próximos.

## Referências e ambientação

Antes das alterações foram recuperados e lidos a Master Map Design Bible, os conceitos de interiores, o relatório/ZIP do 07F, o plano cumulativo e a nota de integração oficial. A referência funcional é o código da base eb. A Bible orienta arquitetura com materiais reconhecíveis, legibilidade a 240×160, prioridade para NPCs e espaços comunitários de madeira, pedra e tecido. Os conceitos vistos foram Centro Comunitário e Sede da Liga Interior. Não há um conceito específico de lounges do Frontier entre as referências recuperadas; não se inventa uma nova função canônica para os cômodos.

O descanso do circuito agora tem piso de madeira nos sete lounges estreitos, pedra clara nos dois largos e madeira escura na casa. Assentos verdes ou vinho têm trama, madeira nas bordas e silhuetas herdadas. Um friso de folhas tecidas substitui o papel xadrez; plantas ficam em vasos de cobre e as entradas têm tapetes verdes com moldura de latão. A paleta é discreta para os atores continuarem legíveis. A TV mantém seus gráficos nativos, como aparelho reconhecível dentro da nova arquitetura.

## Dez mapas, três layouts compartilhados

| Mapa | Layout original | Função preservada |
|---|---|---|
| Lounge1 | LOUNGE2 — 9×10 | Avaliador de IVs |
| Lounge2 | LOUNGE1 — 13×8 | Notícias das sete instalações |
| Lounge3 | LOUNGE2 — 9×10 | Apostas de Battle Points |
| Lounge4 | LOUNGE2 — 9×10 | Conversas de descanso |
| Lounge5 | LOUNGE1 — 13×8 | Mensagens sobre natureza dos Pokémon |
| Lounge6 | LOUNGE2 — 9×10 | Troca de Pokémon |
| Lounge7 | LOUNGE2 — 9×10 | Dois tutores por Battle Points |
| Lounge8 | LOUNGE2 — 9×10 | Dicas do circuito |
| Lounge9 | LOUNGE2 — 9×10 | Aprendiz atribuído pelo runtime |
| Casa de Bento / ScottsHouse | SCOTTS_HOUSE — 6×8 | Visitas, pontos, berries e escudos do Frontier |

A numeração invertida dos dois layouts é original e continua assim. A arte é aplicada a esses três layouts por três pares privados de tilesets. Os sete lounges estreitos continuam compartilhando a mesma arte; os dois largos também. Nenhum layout extra ou mecanismo de seleção de layout é acrescentado. São 886 células contando os dez mapas, 242 células únicas, 30 objetos e 14 warps.

## Contrato de preservação

`review/frontier_07g/functional_contract.json` congela **23.605 arquivos rastreados** da base, incluindo toda lógica, scripts, eventos, dados de Pokémon, assets anteriores e saves. Apenas `data/layouts/layouts.json` e os três headers de declaração dos bancos recebem mudanças em arquivos existentes.

Os 754 layouts conservam IDs, ordem, dimensões, grids, bordas e compartilhamento. Somente três trocam os campos `primary_tileset` e `secondary_tileset`. Grids e bordas mantêm todos os 16 bits de cada célula: IDs, colisão e elevação. Nenhum script, evento, warp, diálogo, objeto, flag ou movimento é alterado. Os 1.551 atributos e 3.102 máscaras dos dois planos nos três pares são iguais aos bancos originais. Não há metatile novo ou remapeamento de IDs; 72 IDs existentes são redesenhados, somando os três bancos.

As paletas 0–11 são exatas. A paleta 12, comprovadamente sem referências originais nesses pares, recebe os materiais. 133 slots de tiles são alocados sem usar os intervalos dinâmicos reservados 432–511 e 992–1023. O primário conserva todas as entradas de metatiles. Todos os pares mantêm callbacks `InitTilesetAnim_Building` / `NULL`; o metatile 0x002, a sequência da TV e seus slots VRAM 496–499 continuam nativos.

O avaliador usa as mesmas condições e seleção de equipe. O noticiário conserva as sete instalações. Apostas mantêm cálculo, limites e mudanças de BP. Natureza e troca usam as mesmas seleções, espécie requerida, cancelamentos, flags e sequência de troca. Tutores mantêm tabelas e preços 16/24/48 BP, disponibilidade, seleção e pagamento. O Lounge9 mantém script de objeto `0x0` e a atribuição de aprendiz pelo engine; não recebe script substituto.

Bento mantém a ordem de recompensas e as condições: símbolos prata/ouro para as berries, séries de 50/100 na Tower para os escudos, espaço de bolsa/decoração e quantidade inicial de BP conforme visitas. Flags e variáveis só são alteradas pelos scripts originais nos mesmos ramos. Suas mudanças de direção também conservam as coordenadas. Não se mudam os nomes técnicos do Scott.

`src/field_door.c`, `src/overworld.c`, `src/apprentice.c`, `src/field_specials.c`, `src/trade.c`, `src/record_mixing.c`, `src/frontier_util.c`, `src/battle_pyramid.c`, `src/battle_pyramid_bag.c` e o layout dos saves permanecem exatos. A correção das portas da Tower e da água do Palace continua instalada, assim como todos os 29 mapas anteriores e o gerador da Pyramid.

## Conferência do 07F e do GitHub

O 07F recuperado continua V1: `Arauna_Checkpoint_07F_BattleFrontier_Pyramid_V1.zip`, 14.183.626 bytes, SHA256 `03c6eef6b1500794bb451b64f1de2ab583dea192c518e5c6ba9fbac6f4b46f15`. O CRC e os 96 hashes internos passaram; os 84 arquivos do incremento coincidem integralmente com a base eb. Não foi recuperada uma V1.1 corrigida desse ZIP.

A diferença de `fd298f4467` para `eb49778fa8` é somente `docs/INTEGRACAO_07F.md`. A nota do integrador declara fast-forward sem correção de arte necessária e registra compilação/gates e três fotos no mGBA. Isso explica a ausência de mudança no arquivo enviado; não é evidência de compilação desta etapa nova.

As refs remotas foram conferidas. A branch do autor `claude/pokemon-juramento-arauna-fhk6ah` termina na base eb. `main`, em `979fb6c1b6731561f3c993efd6045a9bbf096c54`, está 108 commits atrás de eb. O incremento exige eb. Os seis bundles preservam o histórico e permitem retomar de eb, do 07F original fd, de 9a, de 9f, de 06C2/989 ou desse main. Cada um é importado e conferido em receptor independente antes de fechar a entrega. Nenhum push é feito por esta etapa.

## Validação executada

- Contrato completo: todos os 23.605 hashes protegidos iguais; quatro arquivos existentes restritos aos três campos de bancos e blocos de declaração do 07G.
- Bancos: 4bpp, índices e referências válidos, paletas originais, atributos, máscaras, silhuetas transparentes, metatiles não redesenhados e slots de animação conferidos.
- Selectors C originais: 886 células e 51.200 casos de fallback dos dez mapas, mais 53.167 células dos selectors de cavernas/Dive anteriores.
- TV Building: código C original executado por 256 ticks, 32 atualizações da fila, gráficos e slots nativos conferidos. Renders da TV e máscaras em três quadros iguais aos originais.
- Portas, água/plantas do Palace, luzes do Dome e cortina do Pike: checks anteriores executados no host e preservados.
- Frontier anterior: 29 mapas iguais em 58 renders nativos; mais 14 comparações dos sete pisos gerados da Pyramid em dois quadros.
- Pyramid anterior: 1.848 casos do C original, 1.892.352 células montadas, 15.174 objetos posicionados, 14 casos de tarefa de paleta; 256 ticks/64 atualizações de tochas e sombras. Serviços externos são fixtures explícitas.
- Auditoria de mapas: 528 mapas, gates de dados aprovados. As três notas de Surf herdadas continuam registradas, sem regressão do 07G.
- Static readiness: composição inglesa oficial e todos os gates aprovados; o próprio script omite expressamente a compilação ARM.
- Pacote: instalação real em worktree isolada, dry-run, rejeição de alterações protegidas e bases erradas, corrupção, rollback em dois pontos, reaplicação sem escritas, HEAD intacto e geração determinística. Resultados em `install_test.json` / `INSTALL_TEST.json`.
- Bundles: verify/fetch em receptores independentes, ausência inicial do checkpoint, ancestralidade, pai direto eb, árvore completa, todos os hashes do payload/proteção e aplicação real do patch. Resultados em `CUMULATIVE_TEST.json`.

Os testes de host não executam o interpretador de scripts, batalhas, hardware GBA, saves ou serviços jogáveis completos. Esses sistemas são preservados por hashes. **Compilação da ROM e testes jogáveis no mGBA permanecem pendentes neste ambiente**, onde não foram encontrados compilador ARM ou mGBA. Depois da integração, conferir navegação de todas as entradas, avaliação/troca/tutores/aprendiz e os ramos de recompensas de Bento na ROM real. Fotos e compilação do 07F não substituem essa verificação.

## Arte e reprodução

`review/frontier_07g/` inclui os dez pares de mapas completos, dez pares de quadros 240×160, painéis dos três layouts, antes/depois, dez mapas e animação da TV. São renders dos bancos nativos em RGB555, sem atores; não são fotos do emulador. Salas menores que 240×160 são centralizadas para comparação, sem afirmar o enquadramento do engine.

```sh
python3 tools/arauna_maps/validate_frontier_07g.py --base /checkout-limpo-eb49778fa8
python3 tools/arauna_maps/render_frontier_07g.py --base /checkout-limpo-eb49778fa8
python3 tools/arauna_maps/build_frontier_07g.py --base /checkout-limpo-eb49778fa8
```

O builder é determinístico e não altera os arquivos funcionais. Para instalar, use `LEIA_ME.md`, manifeste e bundles do ZIP. Em histórico divergente, concilie em branch mantendo as manutenções locais. A próxima etapa é **07H, cinco serviços**: ExchangeServiceCorner, Mart, Pokémon Center 1F/2F e RankingHall. O 07I fecha os três exteriores depois.

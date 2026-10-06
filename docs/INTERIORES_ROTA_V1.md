# Interiores de rota V1 — Arauna

Data: 2026-10-06. Base obrigatória: `14e56ecd6e9653c67f2ca8a111c8fabdeddd3e2f`, branch de instalação `claude/pokemon-juramento-arauna-fhk6ah`.

Este lote substitui a arte de **25 mapas ativos de interiores de rota**, incluindo as **11 salas reais da Trick House** (entrada, corredor, sala final e oito desafios). O protótipo não usado da floricultura está fora do escopo. São 23 registros de layout: as duas portarias compartilham um, e Winstrate/Berry Master compartilham outro.

Sobre o placar informado de 315/528, instalar estes 25 mapas leva a **340/528** e deixa 188 pendentes. Isso é uma soma sobre o placar informado, não uma nova classificação global dos 528 mapas.

## Arte e regras de integração

Três atlas novos fornecem paredes de reboco, venezianas de madeira, rede, mobiliário, ferramentas, forno e mostruário de vidro, fósseis, instrumentos, equipamentos de mergulho e módulos de rocha. Foram produzidos com ImageGen, convertidos e quantizados para o formato nativo GBA; o construtor também desenha pisos, placas, trilhos e indicadores em pixels nativos. Nenhum tile gráfico do Emerald foi copiado pelo construtor. Os prompts e os atlas usados na conversão estão em `art/interiores_rota_v1` e no pacote.

Os objetos usam transparência na camada de cima, com um piso opaco independente embaixo. Todas as células das grades têm a camada inferior opaca, evitando o problema das frestas pretas. O primário exclusivo do lote corrige esse requisito também sob o PC/TV. O primário da Campanha V2 e todos os bancos anteriores permanecem idênticos à base.

A geometria deste lote continua igual à base. Nenhum `map.bin`, `border.bin`, `map.json`, evento, warp, encontro, clima, texto, script ou código de save mudou. A única alteração nos registros de layout é a escolha dos bancos. Não se adicionam, removem nem reordenam layouts: os 737 IDs existentes e as variantes acionadas por scripts continuam válidos. A prioridade do Continue Game Warp do pacote Início permanece intacta.

O lote tem 14 bancos secundários e um primário pequeno. Estação do teleférico e túnel mantêm o primário General; suas grades usam os metatiles secundários. Os outros mapas usam `AraunaRotaBaseV1`. Este pacote altera cenários de fundo; os sprites móveis de NPCs, árvores de Cut, pedras e portões giratórios continuam os existentes. A animação da viagem do teleférico não está neste lote.

## Mapas incluídos

| Mapa nativo | Banco novo | Dimensões |
| --- | --- | --- |
| `Route109_SeashoreHouse` | `praia` | 15 × 10 |
| `Route110_SeasideCyclingRoadNorthEntrance` | `ciclovia` | 15 × 6 |
| `Route110_SeasideCyclingRoadSouthEntrance` | `ciclovia` | 15 × 6 |
| `Route110_TrickHouseEntrance` | `oficina` | 12 × 8 |
| `Route110_TrickHouseCorridor` | `oficina` | 15 × 24 |
| `Route110_TrickHouseEnd` | `oficina` | 12 × 8 |
| `Route110_TrickHousePuzzle1` | `enigmas` | 15 × 22 |
| `Route110_TrickHousePuzzle2` | `enigmas` | 15 × 22 |
| `Route110_TrickHousePuzzle3` | `enigmas` | 15 × 22 |
| `Route110_TrickHousePuzzle4` | `enigmas` | 15 × 22 |
| `Route110_TrickHousePuzzle5` | `enigmas` | 15 × 22 |
| `Route110_TrickHousePuzzle6` | `enigmas` | 15 × 22 |
| `Route110_TrickHousePuzzle7` | `enigmas` | 15 × 22 |
| `Route110_TrickHousePuzzle8` | `enigmas` | 15 × 22 |
| `Route111_OldLadysRestStop` | `pouso` | 10 × 8 |
| `Route111_WinstrateFamilysHouse` | `fazenda` | 11 × 8 |
| `Route112_CableCarStation` | `estacao` | 13 × 12 |
| `Route113_GlassWorkshop` | `vidro` | 10 × 9 |
| `Route114_FossilManiacsHouse` | `fosseis` | 10 × 8 |
| `Route114_FossilManiacsTunnel` | `tunel` | 13 × 26 |
| `Route114_LanettesHouse` | `tecnica` | 11 × 8 |
| `Route116_TunnelersRestHouse` | `mineiros` | 10 × 9 |
| `Route121_SafariZoneEntrance` | `safari` | 18 × 14 |
| `Route123_BerryMastersHouse` | `fazenda` | 11 × 8 |
| `Route124_DivingTreasureHuntersHouse` | `mergulho` | 10 × 9 |

## Medida de coincidência com a referência

Compara padrões exatos das classes de cor e transparência de tiles 8×8, inclusive espelhamentos; ignora tiles vazios e preenchimento. Referência: release Expansion 1.16.2, commit `ad0fd4d17f546ca6fd8d785c8724f9382e6e9382`, com 39.376 tiles armazenados, 26.933 não vazios e 16.070 padrões canônicos. Percentuais calculados com outro corpus não são diretamente intercambiáveis. É uma medida de coincidência exata, não uma nota de identidade cultural, autoria ou qualidade artística.

Nos 14 bancos secundários, a coincidência é **0,85% a 5,38%**. O primário tem apenas dez tiles não vazios: três padrões simples coincidem (30%). Ele é apresentado separado para não esconder o tamanho pequeno da amostra. Todos os 15 bancos ficam abaixo de 50% de coincidência exata. A medição por referência superior composta efetivamente usada nas grades também está no JSON, separada da métrica de armazenamento.

| Banco | Tiles não vazios | Coincidências | Percentual |
| --- | ---: | ---: | ---: |
| `arauna_rota_praia_v1` | 110 | 1 | 0.91% |
| `arauna_rota_base_v1` | 10 | 3 | 30.00% |
| `arauna_rota_ciclovia_v1` | 93 | 5 | 5.38% |
| `arauna_rota_oficina_v1` | 161 | 2 | 1.24% |
| `arauna_rota_enigmas_v1` | 235 | 2 | 0.85% |
| `arauna_rota_pouso_v1` | 155 | 2 | 1.29% |
| `arauna_rota_fazenda_v1` | 145 | 2 | 1.38% |
| `arauna_rota_estacao_v1` | 88 | 4 | 4.55% |
| `arauna_rota_vidro_v1` | 170 | 2 | 1.18% |
| `arauna_rota_fosseis_v1` | 165 | 2 | 1.21% |
| `arauna_rota_tunel_v1` | 41 | 1 | 2.44% |
| `arauna_rota_tecnica_v1` | 117 | 3 | 2.56% |
| `arauna_rota_mineiros_v1` | 157 | 2 | 1.27% |
| `arauna_rota_safari_v1` | 96 | 5 | 5.21% |
| `arauna_rota_mergulho_v1` | 160 | 3 | 1.88% |

## Verificação

- Build ARM inglês aprovado: EWRAM 249.708 bytes, IWRAM 30.428 bytes, conteúdo ROM ligado 17.388.212 bytes. Aumento de 154.364 bytes sobre a base. O arquivo GBA é preenchido até 32 MiB e não é distribuído.
- Gates oficiais: 189/189 recursos do protagonista, 95/95 capacidade de paletas, auditoria de mapas com oito verificações aprovadas e zero candidatos de resíduo visível. Os logs completos estão em `review/interiores_rota_v1`.
- Validador independente: 15.320 arquivos existentes protegidos permanecem idênticos; 4.962 células mantêm grade, colisão, elevação e comportamento; 39 IDs únicos dos estados de scripts cobertos e seis pares de estados visualmente distintos. PC e TV desligados/ligados distintos. Slots estáticos e paletas seguros.
- Codificação: os 15 bancos foram comparados à ROM efetivamente ligada — tiles descomprimidos, todas as paletas RGB555, metatiles e atributos são idênticos às fontes nativas.
- Construtor idempotente: nova execução manteve os mesmos 290 arquivos; registro em `idempotence.json`.
- Emulador mGBA 0.10.2: 25 mapas carregados pelo fluxo nativo completo, com grupo, número e posição do jogador confirmados; nenhum opcode ilegal. Capturas usam uma inicialização temporária em RAM, removida antes das interações. A ROM em disco e as fontes entregues não contêm harness de captura.
- Travessias naturais de saída e retorno: Casa da Praia, casa de descanso da Rota 111, oficina de vidro e casa do mergulhador.
- PC do Safari: estado nativo 0x004 → 0x005 confirmado e menu de seleção de PC aberto.
- Trick House 3: pisar no botão executou o script nativo e mudou 0x258 → 0x259, com posição real do jogador e estado da grade confirmados.

SHA-256 da ROM verificada (somente identificação, arquivo não incluído): `b19ca2ff2ad0a5f4163531124999a16de1097bb4642b636b90b6443b813da1d5`.

**Limites:** não houve uma campanha completa nem a solução integral dos oito desafios, e nenhum save histórico foi importado. A segurança dos IDs de layout e do fluxo de Continue foi verificada por identidade dos registros e do código. Os testes de portas cobrem as quatro travessias descritas, não todos os serviços de NPCs. A coincidência baixa de tiles não garante identidade brasileira; as pranchas permitem julgar o resultado visual.

## Auditoria atual das bordas

A ferramenta nova usa o resolvedor de bancos do repositório e os retângulos/aliases do código C real. Foram examinadas **134 conexões direcionadas** de exteriores (Dive/Emerge fora desta medição).

| Critério | Conexões com diferenças | Células |
| --- | ---: | ---: |
| Qualquer diferença RGB exata | 86 | 19.820 |
| Diferença máxima por canal maior que 48 | 56 | 6.023 |

A segunda linha destaca diferenças grandes; não é uma medida universal de desenho errado. Mudanças pequenas de paleta também entram na primeira. As animações aquáticas exclusivas de VRAM não são sintetizadas no render estático. Assim, estes números não devem ser equiparados automaticamente aos 55/6.015 da auditoria externa anterior.

Antes e depois deste lote, todas as 134 entradas do relatório permanecem idênticas: **nenhuma borda melhorou ou piorou**. A correção de bordas continua pendente e não está misturada com este pacote de interiores.

| Mapa que vê a faixa | Vizinho | Células acima de 48 |
| --- | --- | ---: |
| `Route124` | `Route126` | 375 |
| `Route126` | `Route124` | 346 |
| `Route110` | `MauvilleCity` | 325 |
| `Route110` | `SlateportCity` | 310 |
| `MauvilleCity` | `Route110` | 272 |
| `EverGrandeCity` | `Route128` | 268 |
| `SlateportCity` | `Route110` | 259 |
| `Route103` | `Route110` | 233 |
| `Route128` | `EverGrandeCity` | 231 |
| `PetalburgCity` | `Route104` | 224 |
| `Route104` | `RustboroCity` | 224 |
| `Route111` | `MauvilleCity` | 196 |

## Reprodução

A partir de uma cópia instalada e uma worktree limpa da base:

```bash
python3 tools/arauna_maps/build_interiores_rota_v1.py
python3 tools/arauna_maps/validate_interiores_rota_v1.py --base /caminho/base-limpa
python3 tools/arauna_maps/audit_interiores_rota_shapes_v1.py --original /caminho/expansion-original
python3 tools/arauna_maps/audit_borders_rgb_v1.py --output /caminho/bordas.json
bash scripts/build_arauna.sh en -j6
bash scripts/check_arauna_static.sh
python3 tools/arauna/audit_map_data.py
python3 scripts/audit_visible_residue.py
python3 tools/arauna_maps/verify_interiores_rota_rom_v1.py --rom pokemon-juramento-de-arauna-en_modern.gba --elf pokemon-juramento-de-arauna-en_modern.elf
```

Os comandos exigem as dependências já usadas pelo projeto (Pillow, compilador C para a auditoria de bordas, ferramentas ARM para build/encoding). As fontes novas são reproduzíveis a partir dos atlas entregues. Não é necessário restaurar o checkpoint antigo nem instalar a Campanha V1.

As três pranchas mostram os 25 mapas no emulador. A prancha Antes/Depois é um render estático dos dados, sem sprites. A prancha Interações mostra os testes do PC e do botão. PNGs individuais e renders completos acompanham o pacote.

## Próximas etapas do roteiro

1. Victory Road (3 mapas) e Seafloor Cavern (10).
2. Bordas prioritárias, com confirmação no emulador dos pares tratados.
3. Dive (12) e S.S. Tidal (3).
4. Rotas iniciais e cidades recoloridas, permitindo nova geometria com validação de eventos/warps/alcance.

Nada dessas etapas seguintes é declarado concluído neste lote.

## Verificação na instalação

- Aplicado sem conflito sobre `14e56ecd6e`; `make MODERN=1` ok; 189/189,
  95/95, 0 candidatos de resíduo e as oito verificações de mapas aprovadas.
- `validate_interiores_rota_v1.py` aprovado em worktree limpa.
- Os 23 layouts alterados só mudam os bancos. Cada um é usado apenas por
  mapas do lote, inclusive `LAYOUT_HOUSE2/3/4`. Comportamento de metatile
  igual à base nas 4.784 células.
- IDs trocados por script ou código (botões, alavancas e portas da Trick
  House, as 20 setas giratórias do desafio 7, PC e TV) existem nos bancos
  novos, e os pares de estado têm desenhos diferentes.
- Legibilidade (célula de parede quase igual a uma de chão, e o inverso):
  - Túnel do Fossil Maniac: 11 células andáveis parecem rocha, contra 58 na
    versão anterior.
  - Entrada do Safari: 7 células.
  - Labirintos dos desafios 2, 4, 6 e 7: as paredes coincidem com a
    colisão, desenhadas como trilhos baixos. O contraste com o piso é menor
    que no original.
- Emulador: os 25 mapas fotografados sem a sequência do caminhão no
  harness local, sem artefatos.
- Placar de conteúdo: 340 mapas com arte Arauna e 188 iguais ao original.

### Sugestões de arte para uma V1.1

- Dar mais contraste às paredes-trilho dos desafios 2, 4, 6 e 7.
- Uniformizar o piso da casa da Lanette, que alterna ladrilho e madeira
  célula a célula.
- Revisar as 11 células do túnel e as 7 da entrada do Safari.

# Arauna — checkpoint 08A: revisão de ambientação

Revisão concluída em 10/10/2026 sobre `a594b3e1e64517421101d96f5b314df22d47e14f`. **Restam 27 mapas com bancos visuais nativos, além do mapa regional e de refinamentos em espaços que já receberam arte Arauna.** Os 47 mapas do Frontier têm a arte V1 instalada; a aceitação integral com save e batalhas reais continua pendente.

Este checkpoint contém inventário, renders, contrato de proteção e roteiro de aceitação. Não redesenha mapas nem altera scripts, eventos, warps, encontros, progressão ou saves.

## Base e recuperação

- Recuperados a Master Map Design Bible de 55 páginas e os 82 concepts versionados. A Bible prevalece sobre legendas antigas dos concepts.
- A branch integradora no GitHub está em `a594b3e1e6`. O `main`, `979fb6c1b6`, está 113 commits atrás. A revisão usa a branch integradora.
- Recuperados os ZIPs 07H e 07I: CRC íntegro e todos os 184 e 143 hashes internos conferidos, respectivamente. Os cinco bundles de cada pacote passaram em `git bundle verify`; seus checkpoints são ancestrais da base atual. Isso verifica os bundles e sua conciliação; não repete as instalações isoladas dos testes históricos.
- Dos 173 arquivos do manifesto 07H, 168 coincidem com o checkout. `layouts.json` e os três headers de tilesets receberam as adições do 07I; o quinto arquivo diferente é a correção intencional do Centro. Os 132 arquivos do manifesto 07I coincidem.
- Trainer Hill 06A, Navel Rock 06B e Bases Secretas 06C1/06C2 já entraram. Não repetir a antiga lista de 7, 21 e 24 mapas como pendência.

## Cobertura: 528 mapas, 754 layouts

| Situação técnica | Mapas | Interpretação |
|---|---:|---|
| Referência a pelo menos um banco Arauna | 477 | Arte própria presente; não é aprovação estética automática |
| Módulos da Battle Pyramid | 16 | Referências nativas no editor; arte 07F aplicada pelo banco do andar gerado |
| Mapas ainda com os dois bancos nativos | 27 | Fila de adaptação abaixo |
| Protótipos e salas explicitamente não usadas | 8 | Fora da fila de produção |
| **Total** | **528** | Inventário completo em `inventario_528_mapas.csv` |

O inventário consulta também a tabela de aliases de câmera das cavernas e do Dive. Os 27 mapas restantes não possuem esses overrides. A contagem não usa os 754 layouts como se fossem 754 lugares jogáveis.

Os oito inativos são `Route104_Prototype`, sua floricultura protótipo e `UnusedContestHall1–6`. Não removê-los nesta rodada; apagar slots técnicos é manutenção separada.

## O que ainda precisa de adaptação

| Checkpoint proposto | Mapas | Direção visual | Preservação crítica |
|---|---:|---|---|
| 08B — ruínas e cavernas | 7 | Arenito, pedra regional, desgaste e profundidade; integrar interior e boca da ruína ao bioma | Braille e abertura de Regirock; bicicleta e piso rachado; fósseis e colapso da torre; encontros, itens e saídas |
| 08C — navio de transporte | 3 | Embarcação costeira de trabalho e passageiros: madeira gasta, ferragens, cabines e carga legíveis | Bilhetes, seleção de porto, primeira viagem, chegada ao Circuito, retorno, passageiros, cabines e batalhas |
| 08D — ilhas especiais | 6 | Distinguir mata úmida, ilha rochosa e enseada; vegetação e embarcadouros ligados à paisagem | Tickets, barco e retorno; puzzle de Deoxys; perseguição de Mew; Latios/Latias e recompensas |
| 08E — concursos | 6 | Palco de Baía das Luzes, madeira, tecido e cerâmica; cenário coerente com hall e lobby já adaptados | Cinco categorias, jurados, público, NPCs variáveis, placar, retorno, pintura e concursos por link |
| 08F — salas de conexão | 5 | Espaço comunitário de intercâmbio consistente com os Centros | Trocas, link, batalha 2P/4P, record mixing e retornos dinâmicos |

**08B:** `DesertRuins`, `DesertUnderpass`, `ScorchedSlab`, `MirageTower_1F–4F`.

**08C:** `SSTidalCorridor`, `SSTidalLowerDeck`, `SSTidalRooms`.

**08D:** `SouthernIsland_Exterior/Interior`, `BirthIsland_Exterior/Harbor`, `FarawayIsland_Entrance/Interior`.

**08E:** `ContestHall`, `ContestHallBeauty`, `ContestHallCool`, `ContestHallCute`, `ContestHallSmart`, `ContestHallTough`. As cinco variantes são chamadas pelo script do lobby; não confundir com `UnusedContestHall1–6`. Hall e lobby locais de Lilycove já têm bancos Arauna, mas o palco dinâmico ainda não acompanha essa arte.

**08F:** `UnionRoom`, `TradeCenter`, `RecordCorner`, `BattleColosseum_2P/4P`.

Para manter entregas curtas, dividir 08B em: **08B1 DesertRuins (1 mapa)**; **08B2 DesertUnderpass + ScorchedSlab (2)**; **08B3 Mirage Tower (4)**. A fundação externa da Mirage Tower já foi corrigida no Dive 04; isso não adapta seus quatro interiores.

Essas direções são propostas de produção apoiadas no vocabulário de materiais da Bible. A Bible não dá nomes e capítulos específicos para todas essas áreas de pós-jogo. Não inventar nomes canônicos ou modificar sua função narrativa para justificar a arte.

## O que precisa de uma segunda rodada

A Bible pede que a identidade apareça em arquitetura, vegetação, relevo, organização urbana e relação com água. Uma mudança de material mantendo toda a composição anterior não encerra esse trabalho. Foram renderizados os 16 assentamentos atuais e 12 amostras dos mapas nativos; os PNGs usam arquivos reais, sem sprites ou clima do motor.

| Frente | Evidência desta revisão | Próxima intervenção |
|---|---|---|
| Mapa regional | PokéNav/Fly conserva a silhueta de Hoenn; tilesheet, tilemap e zooms urbanos vêm da base vanilla. O Pokédex também mantém seu mapa anterior | Criar cartografia Arauna coerente com seus biomas e cidades; manter coordenadas funcionais, áreas selecionáveis e destinos de Fly na primeira etapa |
| Serra do Uivo | Fachadas, pedra e escarpas foram adaptadas, mas a grande malha reta ainda domina a leitura geral | Reforçar três patamares e ligações por escadas; conferir relevo e percursos no motor, evitando prédios apenas alinhados à avenida |
| Casa da Cinza | Grandes faixas claras retangulares dominam o piso do núcleo | Rever pavimento, relação entre termas e casas e transições de relevo; seguir a Bible de cidade termal rústica, sem copiar a lava abundante do concept antigo |
| Encruzilhada Central | Cruz central legível, com extensas áreas uniformes ao redor | Consolidar praça compacta e quatro bairros; dar função aos espaços e ligar a Casa da Fogueira à circulação |
| Baía das Luzes e Missões do Céu | Arte própria, mas ainda há grandes superfícies uniformes e estruturas dispostas sobre eixos retos | Reforçar orla, marina, bairros e relevo em Baía; aterros, equipamento técnico e caminhos que expliquem o uso do solo em Missões |
| Porto do Sal | Cais, mercado e madeira já comunicam o porto; o desenho geral concentra bastante pavimento regular | Diferenciar Porto, Mercado e Centro com densidade, mercadorias e circulação, sem aumentar o ruído visual |
| Circuito de Batalha | Os 47 mapas têm bancos Arauna; o exterior conserva a organização funcional de Emerald e parte dos equipamentos nativos | Após aceitação, revisar landmarks e fachadas para uma identidade institucional própria; preservar primeiro todas as animações de porta |

Estas são prioridades editoriais, não alegações de colisão quebrada. Não extrapolar o render sem atores para declarar ausentes NPCs, vapor, animações ou props desenhados pelo motor. Amanhecer, Passagem, Porto das Redes, Mata do Meio, Águas de M'Boi e Casa da Fogueira já mostram composições próprias; não recomeçar suas versões instaladas.

**Fundos de batalha:** os 47 cenários principais já estão instalados. `docs/FUNDOS_DE_BATALHA.md` registra 19 variações de terreno que ficaram com ambiente original. O seletor atual confirma fallbacks em Surf incompatível com o cenário terrestre, partes não arenosas da Rota 111, Dive e modos especiais. Frontier, link, bases e encontros especiais têm precedência sobre os cenários Arauna. Uma rodada de variantes e ambientes do Circuito é uma pendência visual distinta dos 27 mapas de campo; não contar tudo como mapas novos nem sobrescrever o seletor indiscriminadamente.

## Aviso para o autor: Centro protegido

Próximo pacote sobre **`a594b3e1e6`**. Congelar:

`data/tilesets/secondary/arauna_frontier07h_clinic/metatiles.bin`

SHA-256 atual:

`aa2ce0422b3b25572bf3afcb9b521a75f2259f2d6be0268b522f83d0321b3e4b`

Hash do arquivo original do 07H:

`f3c4ca040633bd1ca6bb80ffcc449778c7b3d1fa653a50f21501b6c487d039fe`

A alteração é no **secundário**: quadrantes 0, 1, 4 e 5 de `0x25C`, levando a faixa superior da parede `0x20B` sobre as portas do Cable Club. A metade inferior conserva a moldura. Não restaurar esse arquivo do ZIP 07H nem executar seu builder antigo sobre a base nova. Não modificar o manifesto histórico para esconder a correção: registrar a exceção e gerar o contrato do próximo pacote a partir da base atual.

`protected_files.json` congela o Centro e seus atributos, a água corrigida do Palace e seus atributos, `field_door.c`, `overworld.c` e os dois seletores visuais de campo. O autor deve incluir esses arquivos entre as dependências protegidas do próximo pacote, junto de todos os scripts, eventos, grids funcionais e encontros que estiverem fora de seu escopo.

```sh
python3 tools/arauna_maps/check_visual_protection_08.py
```

O aviso está pronto neste documento. Não houve envio externo: não foi encontrado PR aberto da branch integradora nem issue de Frontier que identificasse um canal direto do autor. Não mencionar contas presumidas nem abrir uma discussão pública por inferência.

## Aceitação do Frontier: próxima verificação de jogo

`aceitacao_frontier_47_mapas.csv` contém exatamente os 47 mapas, agrupados por 07A–07I. Todas as verificações desta nova sessão estão marcadas como pendentes. Os relatos de integração anteriores registram builds e fotografias no mGBA, mas algumas arenas foram fotografadas com scripts de entrada desligados; isso não comprova seus desafios reais.

Executar em sessões curtas, mantendo a mesma ROM e registrando seu commit/hash, versão do mGBA e identidade do save privado:

| Sessão | Cobertura | Fluxos reais a registrar |
|---|---|---|
| A | Torre, 7 mapas | Inscrição, elevador, combate Single/Double, circuito Multi, derrota, saída e retomada |
| B | Dome, 4 mapas | Inscrição, chaveamento, corredor, preparação, torneio, luzes e retorno |
| C | Palace + Arena, 6 mapas | Combate sob regras de cada instalação, julgamento, água animada e retorno |
| D | Factory + Pike, 9 mapas | Aluguel e troca, batalhas; salas aleatórias, cura/status, encontros e desistência |
| E | Pyramid, 3 mapas | Andares gerados, luz, itens, mochila, avanço, topo, saída e retomada |
| F | Lounges, casa de Bento, serviços e exteriores, 18 mapas | Todas as entradas/saídas, Oeste–Leste, portas e escadas animadas, compras, cura, pontos e recompensas |

Não desligar scripts nem substituir batalhas por fotografias. Usar os modos disponíveis no save; funcionalidades que exigem link precisam de sessão própria e não recebem aprovação com um único jogador. Recompensas/streaks, derrota e retorno devem ser observados no jogo, não apenas inferidos de hashes iguais.

Neste ambiente não há mGBA, compilador ARM nem ROM/save final disponíveis. **Não foi executada nem aprovada a aceitação do Frontier.** O checkpoint entregue é a auditoria 08A e seu roteiro, sem alegar uma ROM final testada.

## Verificações desta entrega

- Inventário completo: 528 mapas e 754 layouts; classificação da Pyramid conferida com o gerador e a integração 07F.
- Auditoria oficial `audit_map_data.py`: oito gates passam. As três notas de Surf em Ever Grande/Lilycove são preexistentes.
- Conferência dos ZIPs e bundles 07H/07I contra a base oficial.
- Guardas dos oito arquivos protegidos passam. Diferença do Centro conferida palavra por palavra.
- Renders de 16 assentamentos, 12 amostras nativas e cartografia real do PokéNav. Não são screenshots do emulador.
- Nenhum arquivo de jogo mudou neste checkpoint; apenas documentação, evidências e ferramentas de leitura/validação foram acrescentadas.

Reprodução:

```sh
python3 tools/arauna_maps/audit_brazil_08.py
python3 tools/arauna_maps/check_visual_protection_08.py
python3 tools/arauna/audit_map_data.py
```

No clone limpo, gerar antes os headers de grupos/layouts com o `mapjson`, conforme o build do projeto. Os registros e recibos desta auditoria estão em `review/aceitacao_08_auditoria/`.

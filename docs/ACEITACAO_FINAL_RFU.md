# Aceitação final do ciclo de mapas: sessão sem fio da Union Room

O checkpoint 01 da aceitação final foi conferido, e a sessão RFU real do
checkpoint 02 foi executada com scripts ligados. As cinco partes passaram. A
última pendência do ciclo de mapas está encerrada. Nenhum arquivo do jogo
mudou nesta etapa.

## Checkpoint 01: conferência

- **Pacote de evidências.**
  - O ZIP tem SHA-256
    `4911700a67648ae1ecaf59d87cf80a08fbb0b6b4ee44803f18b080dcf325a632`.
  - Os 19 arquivos batem com `SHA256_FILES.json`.
  - A base citada, `dcde4be8de`, é a ponta da branch.
- **Inventário.** O CSV dos 528 mapas é idêntico ao
  `review/connections_08f/inventario_528_mapas.csv`. São 504 mapas com bancos
  Arauna, 16 módulos da Pyramid, 8 inativos e nenhum mapa ativo em banco
  nativo.
- **Proteções.** Os hashes das sete correções conferem com o checkout.

## Checkpoint 02: sessão sem fio real

O mGBA não emula o Wireless Adapter; o gpSP emula. Ambiente:

- **Núcleo.** gpSP (libretro), commit `5819380c2f` de 19/09/2026, compilado
  localmente. Opções: `gpsp_serial = "rfu"`, BIOS embutida e RTC
  determinístico.
- **Frontend.** Um frontend libretro local roda duas instâncias, cada uma com
  sua cópia do núcleo. O netpacket das duas foi ligado como no netplay do
  RetroArch: a primeira é o host, a segunda o cliente. Os pacotes do
  adaptador passam de uma para a outra.
- **ROMs.** A ROM oficial compilada destes fontes tem SHA-256
  `b380e501e21e4078830e9f8727cfe7fd206a167b111913ac59bda08e44eee284`.
  O teste usou a ROM de harness dos mesmos fontes. A única diferença é o
  `new_game.c` local, que põe cada jogo no 2F do Centro de Lilycove com
  nome, ID e equipe de teste.
- **Jogadores.**
  - IARA (ID `0x1A2F3E4D`) leva Guaraná nv. 25 e Pimpau nv. 22.
  - TOBIAS (ID `0x2B67A1C3`) leva Sagüim nv. 25 e Botim nv. 22.
  - Os dois têm a Pokédex, sem a nacional.
- **Harness.** Fica fora do repositório.

| Parte da sessão | Resultado |
|---|---|
| Entrada e descoberta | Os dois entram pelo atendente sem fio: "Welcome to the POKéMON WIRELESS CLUB UNION ROOM", save, "I hope you enjoy your time in the UNION ROOM". Na sala, cada jogo mostra o outro jogador no lugar de líder (4,6). IARA vê TOBIAS como YOUNGSTER, e TOBIAS vê IARA como BUG CATCHER |
| Contato e atividade | IARA fala com o avatar: "Is there something that you wanted to do?" (GREETINGS, BATTLE, CHAT, EXIT). TOBIAS recebe "Somebody has contacted you". **GREETINGS:** os dois cartões abrem, até "TOBIAS: Glad to have met you!". **BATTLE:** TOBIAS aceita, cada um escolhe dois Pokémon e a batalha vai até o fim. **Troca:** IARA registra Guaraná no quadro com a atendente, pedindo tipo NORMAL. TOBIAS consulta o quadro na parede, em (2,1), e oferece Sagüim. IARA aceita, a animação roda e o jogo salva. Na memória, cada Pokémon está do outro lado com o ID do dono original |
| Colisão dos avatares | Empurrando o avatar de TOBIAS, IARA não sai do lugar. Depois que TOBIAS sai, ele para de transmitir e o avatar some do mundo de IARA em 13 s. IARA pisa na casa onde ele estava |
| Encerramento e retorno | Os dois saem pela porta (7,11) e voltam ao 2F do Centro de Lilycove. A equipe trocada continua lá |
| Persistência e reconexão | Os dois consoles foram reiniciados. O save carrega no Centro, com o Pokémon recebido na equipe. Numa nova entrada pelo atendente, os dois se veem de novo em 2 s |

A arte nova não atrapalha nenhuma função da sala: o quadro de trocas, a
atendente e a porta estão nas casas que o código espera.

### Notas do ambiente de teste

- O gpSP gera o ID do adaptador a partir do relógio de ciclos. Duas
  instâncias idênticas, ligadas no mesmo quadro, gerariam o mesmo ID, o que
  não acontece com dois consoles. O segundo jogo rodou 97 quadros a mais
  antes da ligação.
- Na batalha, o cursor de golpe ficou no ataque de baixo à esquerda (Vine
  Whip, Headbutt). Os golpes de cima são de status, e repetir só eles não
  acaba a batalha.

## Dex regional com as 386 espécies

Numa tentativa anterior, TOBIAS ofereceu Folião (#278) e o jogo respondeu
"That POKéMON can't be traded now." A dex regional era #001–#202
(`HOENN_DEX_COUNT` 202). Mas 143 das 295 espécies selvagens têm número acima
de 202, já a partir da Rota 101. Antes da Pokédex nacional, que só chega
depois do Hall da Fama, o corte tinha três efeitos:

- a Pokédex escondia essas capturas;
- o resumo mostrava o número como desconhecido;
- o cabo e a Union Room recusavam a troca.

Também havia um efeito sobre a classificação: ANAHI declarava a dex completa
com 200 espécies.

Agora a dex regional é a dex inteira: `HOENN_DEX_COUNT` passa a ser
`NATIONAL_DEX_COUNT`, 386. A ordem continua terminando em Sacinho (#385) e
Arauá (#386), as posições de Jirachi e Deoxys. A checagem de dex completa
continua deixando as duas de fora. O que ela conta está na seção seguinte.

Mudanças:

- **Classificação de ANAHI.** As faixas de `GetPokedexRatingText` passam a
  ser distribuídas sobre o total. Com a dex de 202, o resultado é igual ao
  original.
- **Texto.** "hundred mark" vira "halfway mark".
- **Gerador e documento.** `build_species.py` e `docs/arauna/DEX_PORT.md`
  registram a decisão.

No mGBA, comparando a ROM anterior com a nova, com scripts ligados:

| Verificação | Antes | Depois |
|---|---|---|
| Pokédex sem a nacional, com Pomba-Gira (#263) e Folião (#278) | SEEN 0, OWN 0, lista vazia | SEEN 2, OWN 2, Nº278 Folião na lista |
| Resumo de Folião | sem número | Nº278 |
| ANAHI com 200 capturados | "The ARAUNA POKéDEX is complete!" | "You've passed the halfway mark." |
| ANAHI com #001–#384 capturados | contagem parada em 202 | "complete!" |
| Union Room sem a nacional, TOBIAS oferece Folião (#278) | recusada | troca concluída; IARA fica com Folião, com o ID de TOBIAS |

A ROM compila e os gates passam. `build_species.py --check` também passa.

### Dex completa sem as especiais sem casa

A primeira versão dessa mudança pedia #001–#384 para a dex completa. Isso inclui
19 lendárias e míticas que o gate de disponibilidade segura sem encontro
(#329–#344, #346, #348 e #376), e ninguém consegue capturá-las. Com o corte
antigo, de #001–#200, o diploma era alcançável; com o novo, tinha ficado
impossível.

Agora a dex completa pula as especiais seguradas. Elas são lidas de
`src/data/pokemon/dex_completion_held_back.h`, gerado por
`check_availability.py --write` a partir de `ESPECIAIS_ESTATICOS.csv`. O gate
falha se o cabeçalho não bater com o CSV. Hoje a dex completa pede 365
espécies. Quando uma especial ganhar casa, a linha dela sai do CSV e ela volta
a contar.

Há uma regra só, `GetPokedexCompletionCount`, usada por:

- o diploma;
- a estrela do cartão;
- o presente do laboratório;
- a classificação de ANAHI, no PC e no PokéNav.

A classificação pelo PokéNav tinha faixas próprias. Elas ainda declaravam a dex
completa com 200 capturas, e a mudança anterior não tinha pego isso. Agora o
PokéNav usa a mesma classificação do PC.

A dex nacional de Arauna tem as mesmas espécies. `HasAllMons` ainda pulava os
números de Mew, Lugia, Ho-Oh e Celebi, que em Arauna são criaturas comuns
(Marimbondão, Jenipapo, Urucum e Caipora). Agora ela é a dex completa com a
dex nacional ligada, e o diploma diz NATIONAL nesse caso.

No mGBA, com scripts ligados, comparando o commit anterior (`89591d2fd8`) com
este. "Tudo o que dá para pegar" são #001–#384 capturados sem as 19 seguradas,
ou seja, 365 capturas.

| Verificação | Antes | Depois |
|---|---|---|
| ANAHI no laboratório, tudo o que dá para pegar | "very close to complete. Keep going!" | "The ARAUNA POKéDEX is complete!" |
| Mesmo caso, faltando #001 | — | "very close to complete" |
| Designer do Motel de Lilycove, tudo o que dá para pegar | "If you do complete it, please come show me." | fanfarra e diploma "completed your ARAUNA POKéDEX" |
| Mesmo caso, com a dex nacional | — | diploma "NATIONAL POKéDEX", na moldura dourada |
| Mesmo caso, faltando #001 | — | sem diploma |
| Cartão de treinador, tudo o que dá para pegar | cartão verde, sem estrela | cartão bronze, com estrela |
| Entrar no laboratório depois do Hall da Fama, tudo o que dá para pegar | nada acontece | a mesa com as três Poké Balls aparece e ANAHI chama o jogador |
| ANAHI pelo PokéNav, 200 capturados | "The ARAUNA POKéDEX is complete!" | "You've passed the halfway mark." |
| ANAHI pelo PokéNav, tudo o que dá para pegar | — | "complete!" |

A ROM compila sem avisos novos e os gates passam. A ROM oficial destes fontes
tem SHA-256 `df26159126ec16af56a402bb78291728e338113708c7bb98400a5ba8313c99ed`.

### Aviso ao autor

Nove arquivos que os contratos congelam mudaram, e um arquivo novo entrou.
`validate_connections_08f.py` agora para em `data/text/pokedex_rating.inc`, o
primeiro deles que ele confere.

| Arquivo | SHA-256 |
|---|---|
| `include/constants/pokedex.h` | `33c16378e34a9ac56c5a11cef64086d5dfc3a90958276ed272ca430c6f624ec4` |
| `include/pokedex.h` | `9d0801044e51c454c7057f5c13c59997090fd26fedd4193cb8ef4e653c2a246e` |
| `src/pokedex.c` | `0b25c87aa8317814d2a7e463849c85cea83268ed616f5900491d4c7efcf4335d` |
| `src/birch_pc.c` | `bd776a21a118c2020d543c83f985bf001c5d7503c244ce82efac594f2c27b7f4` |
| `src/match_call.c` | `e23f827ec677860cd31fafcdc5e77a8e5d8b4b51e15eacf5a6772e319ecf71ed` |
| `data/text/pokedex_rating.inc` | `9e7e058be6d1a54d2752a463c0e5d79f79bc67814cc6cbb66ac2541359ce0e98` |
| `tools/arauna/build_species.py` | `262ec1cdbd1dfb668d322ae82f46c1ff6fa9732ecd32e9a407f6048d48cb4242` |
| `tools/arauna/check_availability.py` | `05f457f6281166fd2609d29d596ccf6f53106a438e501ebe0bd224ef4b366fc1` |
| `docs/arauna/DEX_PORT.md` | `5818103d70eb0b34a20133ab1191223329e91c5b24ff3ed6fa55017468a93f81` |
| `src/data/pokemon/dex_completion_held_back.h` (novo) | `ad3f8d994d721b50e37873ecc24a8a074edcf7ff66586115e2877101d0acb04d` |

Os próximos pacotes devem partir deste commit e proteger esses dez arquivos,
junto das sete correções anteriores.

## Estado

Cobertura, integridade e sessão sem fio aprovadas. O ciclo de mapas está
encerrado, com as sete correções protegidas e a dex regional de 386. A dex
completa pede as 365 espécies que dá para capturar hoje.

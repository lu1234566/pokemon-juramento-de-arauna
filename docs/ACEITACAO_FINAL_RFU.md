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
continua deixando as duas de fora. Assim, o diploma, a estrela do cartão de
treinador, o presente do laboratório e a classificação de ANAHI contam
#001–#384.

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
| ANAHI com 384 capturados | contagem parada em 202 | "complete!" |
| Union Room sem a nacional, TOBIAS oferece Folião (#278) | recusada | troca concluída; IARA fica com Folião, com o ID de TOBIAS |

A ROM compila e os gates passam. `build_species.py --check` também passa.

### Aviso ao autor

Cinco arquivos que os contratos congelam mudaram.
`validate_connections_08f.py` agora para em `data/text/pokedex_rating.inc`.

| Arquivo | SHA-256 |
|---|---|
| `include/constants/pokedex.h` | `33c16378e34a9ac56c5a11cef64086d5dfc3a90958276ed272ca430c6f624ec4` |
| `src/birch_pc.c` | `87d7800c864b64ac923ef741e437721a8411bbafa6010e3d35b0b8ee908b3b78` |
| `data/text/pokedex_rating.inc` | `9e7e058be6d1a54d2752a463c0e5d79f79bc67814cc6cbb66ac2541359ce0e98` |
| `tools/arauna/build_species.py` | `262ec1cdbd1dfb668d322ae82f46c1ff6fa9732ecd32e9a407f6048d48cb4242` |
| `docs/arauna/DEX_PORT.md` | `6737cdd4c25c04ed36230c29dd6dbc3f3a4220ba01287e431b251c5b610ba992` |

Os próximos pacotes devem partir deste commit e proteger esses cinco arquivos,
junto das sete correções anteriores.

## Estado

Cobertura, integridade e sessão sem fio aprovadas. O ciclo de mapas está
encerrado, com as sete correções protegidas e a dex regional de 386.

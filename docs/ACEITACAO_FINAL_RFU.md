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

### Observação: troca de espécies fora da dex regional

Numa tentativa anterior, TOBIAS ofereceu Folião (#278) e o jogo respondeu
"That POKéMON can't be traded now." Isso segue o
`docs/arauna/DEX_PORT.md`: a dex regional é #001–#202, e as espécies
#203–#386 seguem a regra das espécies de fora da região. Sem a Pokédex
nacional, a Union Room não as troca, como no original com as espécies de fora
de Hoenn. Não é defeito, mas são 184 das 386 espécies. Se a intenção for
liberar a troca delas sem a dex nacional, é uma decisão de projeto à parte.

## Estado

Cobertura, integridade e sessão sem fio aprovadas. O ciclo de mapas está
encerrado, com as sete correções protegidas.

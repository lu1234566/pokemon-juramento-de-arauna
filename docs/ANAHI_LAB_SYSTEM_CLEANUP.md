# Limpeza sistêmica do laboratório de Anahi

## Escopo

Este lote cobre somente seis blocos de texto em `data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc`:

- upgrade da Pokédex para o Modo NACIONAL;
- recebimento do starter pós-game;
- prompt legado de apelido;
- aviso após o starter já ter sido escolhido;
- aviso de falta de espaço para o Pokémon;
- ligação pós-game herdada de Scott.

Labels, scripts executáveis, flags, vars, estado da National Dex, escolha de starter, objetos, movimentos, save e progressão permanecem intactos.

## Ligação pós-game

A função estrutural da ligação de Scott é atribuída a **Seu Bento**. A escolha reaproveita um personagem que já assumiu na `main` superfícies de orientação de campo e Match Call, evitando criar um novo anfitrião apenas para este evento.

O destino técnico herdado não é renomeado neste lote. A fala o apresenta genericamente como um circuito de batalha após a Liga e mantém os dois pontos de embarque, usando os nomes de Arauna já aplicados ao mapa regional:

- `MAPSEC_SLATEPORT_CITY` → **PORTO DO SAL**;
- `MAPSEC_LILYCOVE_CITY` → **BAIA DAS LUZES**.

## Validação

`tools/cleanup_anahi_lab_system_residue.py`:

- substitui apenas os seis labels delimitados;
- é idempotente;
- possui modo `--check`;
- rejeita tokens vanilla relevantes (`SCOTT`, `S.S. TIDAL`, `SLATEPORT`, `LILYCOVE` e frases inglesas dos demais blocos);
- exige os termos canônicos da ligação;
- valida segmentos visíveis com limite de 32 caracteres, usando larguras conservadoras para `{PLAYER}` e `{STR_VAR_1}`.

O check faz parte tanto do workflow gerador de resíduos quanto da CI normal.

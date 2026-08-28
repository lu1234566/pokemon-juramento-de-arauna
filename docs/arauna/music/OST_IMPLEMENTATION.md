# Arauna OST — implementação

21 faixas originais implementadas como **novos slots `MUS_ARAUNA_*`**
(índices 610–630). Nenhum ID vanilla foi reescrito: os dados de música do
Emerald continuam intactos e apenas os *contextos* foram redirecionados. Isso
mantém o esqueleto do Emerald estável e evita que um slot compartilhado leve
música nova para um contexto que não deveria recebê-la.

## ⚠️ Ressalva essencial sobre os arranjos

As MIDI foram geradas por **transcrição automática por DSP** das masters
(`tools/arauna/transcribe_ost.py`), sem que ninguém as tenha escutado no
processo. O pipeline extrai andamento, um contorno de melodia monofônico, o
baixo, um acorde por tempo e percussão de onset.

Isso significa, honestamente:

- o **andamento, a estrutura, a tonalidade geral e a densidade rítmica** de cada
  faixa tendem a estar próximos da master;
- a **melodia é aproximada**: em trechos densos o extrator segue o parcial mais
  forte, que nem sempre é a linha principal;
- **contramelodias, ornamentação e timbres específicos não são reproduzidos**;
- os **leitmotifs pedidos na seção 29 do briefing não estão garantidos** — eles
  dependem de decisões musicais que exigem escuta.

Portanto: as versões atuais **tocam, dão loop e ocupam o contexto certo**, mas
devem ser tratadas como *base editável*, não como arranjo final. O caminho de
melhoria é abrir os `.mid` num editor e corrigir as linhas à mão — toda a
fiação (slot, voicegroup, loop, roteamento) já está pronta e não precisa mudar.

## Pipeline

`master .mp3` → `tools/arauna/transcribe_ost.py` (DSP) → `sound/songs/midi/mus_arauna_*.mid`
→ `mid2agb` (via `sound/songs/midi/midi.cfg`) → `.s` → ROM.

- **Voicegroup:** `voicegroup_arauna_ost` (`sound/voicegroups/arauna_ost.inc`),
  derivado de `littleroot` — base PSG (square) barata em CPU, com drumset e
  piano nos índices 0 e 1. Uma única voicegroup compartilhada por todas as 21
  faixas mantém o custo de ROM baixo e o timbre coeso.
- **Instrumentação por faixa:** 4 tracks — melodia (square), baixo (square
  grave), harmonia (piano) e percussão. Bem abaixo do limite prático do mixer;
  não usa DirectSound novo nem samples novos, então não há risco de estourar
  CPU em batalha.
- **Volume:** normalizado perceptualmente. O RMS de cada master foi medido e
  convertido para o parâmetro `-V` do `mid2agb` (faixa 66–110, mediana 80), para
  que nenhuma faixa fique muito acima ou abaixo das outras.

## Loop

Todas as 21 faixas dão loop (verificado: cada `.s` gerado emite `GOTO` em todas
as 4 tracks, nenhuma termina em `FINE` isolado). Os marcadores são eventos de
texto `[` e `]` na **track condutora** do MIDI — o `mid2agb` lê essa track uma
única vez e propaga os eventos para todas as demais.

- **Loops curtos de gameplay** (`< 45 s`): loop do início, sem intro artificial e
  sem silêncio — Instinto Selvagem, Rival à Altura, Prova de Arauna.
- **Faixas longas:** mantêm o início como intro tocada uma vez e depois repetem
  o corpo. O ponto de loop é alinhado ao compasso (4/4) para a emenda cair no
  tempo forte.

| MUS_* | BPM | Loop início (tempo) | Loop fim (tempo) |
|---|---:|---:|---:|
| `MUS_ARAUNA_MAIN` | 68 | 32 | 132 |
| `MUS_ARAUNA_VILA_AMANHECER` | 64 | 40 | 160 |
| `MUS_ARAUNA_ROUTE` | 127 | 40 | 164 |
| `MUS_ARAUNA_WILD_BATTLE` | 140 | 0 | 48 |
| `MUS_ARAUNA_TRAINER_BATTLE` | 98 | 44 | 188 |
| `MUS_ARAUNA_CIRO` | 140 | 60 | 248 |
| `MUS_ARAUNA_CIRO_BATTLE` | 148 | 0 | 68 |
| `MUS_ARAUNA_CIRO_FINAL` | 140 | 88 | 352 |
| `MUS_ARAUNA_HORIZON` | 98 | 76 | 316 |
| `MUS_ARAUNA_HORIZON_BATTLE` | 78 | 44 | 188 |
| `MUS_ARAUNA_GYM_BATTLE` | 106 | 0 | 24 |
| `MUS_ARAUNA_STORY_BOSS` | 148 | 88 | 352 |
| `MUS_ARAUNA_LEGEND_ENCOUNTER` | 115 | 56 | 236 |
| `MUS_ARAUNA_LEGEND_BATTLE` | 83 | 64 | 256 |
| `MUS_ARAUNA_ARAUA_ENCOUNTER` | 73 | 32 | 140 |
| `MUS_ARAUNA_ARAUA_BATTLE` | 167 | 100 | 408 |
| `MUS_ARAUNA_OATH_ROAD` | 127 | 96 | 388 |
| `MUS_ARAUNA_ELITE_BATTLE` | 85 | 52 | 208 |
| `MUS_ARAUNA_CHAMPION_BATTLE` | 179 | 108 | 440 |
| `MUS_ARAUNA_CREDITS` | 157 | 60 | 244 |
| `MUS_ARAUNA_SAPPHIRE_CRYPT` | 71 | 44 | 176 |

## Tabela de implementação

| Faixa | MUS ID | MIDI | Voicegroup | Loop | Mapa / evento | Substitui | Status |
|---|---|---|---|---|---|---|---|
| Juramento de Arauna | `MUS_ARAUNA_MAIN` | `mus_arauna_main.mid` | `arauna_ost` | sim | Tela de título | `MUS_TITLE` (só em `title_screen.c`) | IMPLEMENTADA |
| Onde a Jornada Nasce | `MUS_ARAUNA_VILA_AMANHECER` | `mus_arauna_vila_amanhecer.mid` | `arauna_ost` | sim | Vila Amanhecer + casas (5 mapas, ex-`MUS_LITTLEROOT`) | `MUS_LITTLEROOT` | IMPLEMENTADA |
| Terra de Arauna | `MUS_ARAUNA_ROUTE` | `mus_arauna_route.mid` | `arauna_ost` | sim | Rotas iniciais 101/102/103 (ex-`MUS_ROUTE101`) | `MUS_ROUTE101` | IMPLEMENTADA |
| Instinto Selvagem | `MUS_ARAUNA_WILD_BATTLE` | `mus_arauna_wild_battle.mid` | `arauna_ost` | sim | Batalha selvagem (não-Kanto) | `MUS_VS_WILD` | IMPLEMENTADA |
| Um Desafio à Frente | `MUS_ARAUNA_TRAINER_BATTLE` | `mus_arauna_trainer_battle.mid` | `arauna_ost` | sim | Treinador comum (não-Kanto) | `MUS_VS_TRAINER` | IMPLEMENTADA |
| Sempre Um Passo à Frente | `MUS_ARAUNA_CIRO` | `mus_arauna_ciro.mid` | `arauna_ost` | sim | 20 cenas de encontro de rival (12 mapas) | `MUS_ENCOUNTER_MAY` / `_BRENDAN` | IMPLEMENTADA |
| Rival à Altura | `MUS_ARAUNA_CIRO_BATTLE` | `mus_arauna_ciro_battle.mid` | `arauna_ost` | sim | Ciro (`TRAINER_CLASS_RIVAL`) | `MUS_VS_RIVAL` | IMPLEMENTADA |
| O Preço de Vencer | `MUS_ARAUNA_CIRO_FINAL` | `mus_arauna_ciro_final.mid` | `arauna_ost` | sim | Ciro estágio final (6 IDs Lilycove) | — (novo) | IMPLEMENTADA |
| Progresso a Qualquer Custo | `MUS_ARAUNA_HORIZON` | `mus_arauna_horizon.mid` | `arauna_ost` | sim | Encontro de agente Aqua/Horizonte (tema de campo) | `MUS_ENCOUNTER_AQUA` | IMPLEMENTADA |
| Máquina de Controle | `MUS_ARAUNA_HORIZON_BATTLE` | `mus_arauna_horizon_battle.mid` | `arauna_ost` | sim | Agentes/admins/líder **Aqua** (Horizonte) | `MUS_VS_AQUA_MAGMA` (**só o lado Aqua**) | IMPLEMENTADA |
| Prova de Arauna | `MUS_ARAUNA_GYM_BATTLE` | `mus_arauna_gym_battle.mid` | `arauna_ost` | sim | `TRAINER_CLASS_LEADER` (8 ginásios) | `MUS_VS_GYM_LEADER` | IMPLEMENTADA |
| Algo Não Deveria Estar Aqui | `MUS_ARAUNA_STORY_BOSS` | `mus_arauna_story_boss.mid` | `arauna_ost` | sim | Líder dos Lembrantes (`TRAINER_CLASS_MAGMA_LEADER`) | — (novo) | IMPLEMENTADA |
| Vozes Antes dos Homens | `MUS_ARAUNA_LEGEND_ENCOUNTER` | `mus_arauna_legend_encounter.mid` | `arauna_ost` | sim | Santuários lendários: Desert Ruins, Island Cave, Ancient Tomb | `MUS_SEALED_CHAMBER` | IMPLEMENTADA |
| Força Primordial | `MUS_ARAUNA_LEGEND_BATTLE` | `mus_arauna_legend_battle.mid` | `arauna_ost` | sim | Todo lendário exceto Arauá | `MUS_VS_KYOGRE_GROUDON`, `MUS_VS_REGI`, `MUS_VS_MEW`, `MUS_RG_VS_LEGEND` | IMPLEMENTADA |
| Aquele Que Lembra | `MUS_ARAUNA_ARAUA_ENCOUNTER` | `mus_arauna_araua_encounter.mid` | `arauna_ost` | sim | `SkyPillar_Top` (cena de Arauá) | `MUS_MT_CHIMNEY` | IMPLEMENTADA |
| O Primeiro Juramento | `MUS_ARAUNA_ARAUA_BATTLE` | `mus_arauna_araua_battle.mid` | `arauna_ost` | sim | Batalha vs `SPECIES_RAYQUAZA` (#386 Arauá) | `MUS_VS_RAYQUAZA` | IMPLEMENTADA |
| O Peso do Juramento | `MUS_ARAUNA_OATH_ROAD` | `mus_arauna_oath_road.mid` | `arauna_ost` | sim | 13 mapas (Victory Road + salas Ever Grande) | `MUS_VICTORY_ROAD` | IMPLEMENTADA |
| Os Que Permaneceram de Pé | `MUS_ARAUNA_ELITE_BATTLE` | `mus_arauna_elite_battle.mid` | `arauna_ost` | sim | `TRAINER_CLASS_ELITE_FOUR` (Lázaro, Rosa, Clara, Tibúrcio) | `MUS_VS_ELITE_FOUR` | IMPLEMENTADA |
| Até Onde Você Chegou | `MUS_ARAUNA_CHAMPION_BATTLE` | `mus_arauna_champion_battle.mid` | `arauna_ost` | sim | `TRAINER_CLASS_CHAMPION` (Amália) | `MUS_VS_CHAMPION` | IMPLEMENTADA |
| Depois do Juramento | `MUS_ARAUNA_CREDITS` | `mus_arauna_credits.mid` | `arauna_ost` | sim | Créditos (`credits.c`) | `MUS_CREDITS` | IMPLEMENTADA |
| The Sapphire Crypt | `MUS_ARAUNA_SAPPHIRE_CRYPT` | `mus_arauna_sapphire_crypt.mid` | `arauna_ost` | sim | `SealedChamber` (externo + interno) | `MUS_SEALED_CHAMBER` | IMPLEMENTADA |

### Decisão documentada — The Sapphire Crypt

O briefing pediu escolha narrativa, não pelo título. A faixa é a mais lenta do
pacote (71 BPM) e a de textura mais escura e estática.

Cinco mapas compartilhavam `MUS_SEALED_CHAMBER`. Eles se dividem naturalmente em
dois grupos, e a divisão aproveita duas faixas em vez de uma:

- **`SealedChamber` (externo + interno)** → *The Sapphire Crypt*. É a câmara
  selada alcançada por baixo d'água, com escrita antiga — literalmente a cripta
  do jogo, e o lugar cuja atmosfera casa com a faixa.
- **Desert Ruins, Island Cave, Ancient Tomb** → *Vozes Antes dos Homens*. São os
  santuários onde o lendário (Muiraquitã) aparece, ou seja, exatamente o
  contexto de "aproximação/aparição" que a seção 20 descreve.

**Alternativa considerada:** usar a faixa em Cave of Origin (o coração da crise
de M'Boi). Foi descartada porque aquele mapa já tem tema próprio e forte
identidade, enquanto os cinco mapas de `MUS_SEALED_CHAMBER` estavam
compartilhando um único tema genérico.

### Decisão documentada — separação Horizonte × Lembrantes

`MUS_VS_AQUA_MAGMA` é **um único slot compartilhado** por Aqua e Magma no
Emerald, e `GetBattleBGM()` decidia pela classe do treinador. Como em Arauna
Aqua ≈ Horizonte e Magma ≈ Lembrantes, trocar o slot contaminaria os dois lados.
A implementação separa os `case` do `switch`: `TEAM_AQUA` / `AQUA_ADMIN` /
`AQUA_LEADER` passam a tocar *Máquina de Controle*, enquanto `TEAM_MAGMA` /
`MAGMA_ADMIN` / `MAGMA_LEADER` **continuam no slot vanilla**. O mesmo vale para
o tema de campo: só `TRAINER_ENCOUNTER_MUSIC_AQUA` virou *Progresso a Qualquer
Custo*; o caso `_MAGMA` ficou intacto.

### Decisão documentada — roteamento por ID, não por classe

Em `main` os confrontos de Ciro usam `TRAINER_CLASS_RIVAL`, então o roteamento
por classe é seguro para ele. O caso que **exige** ID é o Ciro final: os seis IDs
de Lilycove são testados dentro do `case TRAINER_CLASS_RIVAL`, e todos os demais
encontros caem no padrão. Se no futuro forem criados IDs `TRAINER_ARAUNA_*` com
classes genéricas compartilhadas, o roteamento deles precisa ser por ID, antes do
`switch` por classe.

### Decisão documentada — Story Boss (Algo Não Deveria Estar Aqui)

Este é o ponto com mais margem de interpretação, e a seção 19 pede que a decisão
seja documentada. A faixa é de **batalha**, e não pode ser lendário (esses têm
*Força Primordial*) nem treinador comum.

A escolha foi o **líder dos Lembrantes** (`TRAINER_CLASS_MAGMA_LEADER`): é o
boss de campanha não-lendário do jogo, e os Lembrantes são justamente a facção
que o Desencanto produziu — "algo não deveria estar aqui" descreve o confronto.
Como bônus, isso mantém os Lembrantes musicalmente separados do Horizonte sem
reutilizar o tema do Consórcio, respeitando a restrição da seção 17.

**Alternativa considerada:** um encontro roteirizado ligado a M'Boi / Arquivo
Vivo. Foi descartada porque em `main` esses momentos ainda não têm um ID de
treinador dedicado — quando existir, basta apontá-lo para `MUS_ARAUNA_STORY_BOSS`
sem tocar em mais nada.

### Decisão documentada — Ciro normal × Ciro final

A progressão de rival do Emerald é Route 103 → 110 → 119 → Rustboro →
**Lilycove**. Os 6 IDs de Lilycove (`TRAINER_{BRENDAN,MAY}_LILYCOVE_{MUDKIP,
TREECKO,TORCHIC}`) são o último e mais forte confronto, e recebem *O Preço de
Vencer*; todos os encontros anteriores mantêm *Rival à Altura*.

## Auditoria final (seção 42)

Ocorrências de música de Hoenn ainda presentes, classificadas:

- **A — corretas e intencionais:**
  `MUS_VS_AQUA_MAGMA` / `MUS_VS_AQUA_MAGMA_LEADER` no ramo Magma (Lembrantes —
  separação exigida pelo briefing); `MUS_VS_GYM_LEADER` / `MUS_VS_TRAINER` em
  `cable_club.c` e no ramo de link de `GetBattleBGM()` (batalhas de link, fora
  da campanha); `MUS_TITLE` em `title_screen_frlg.c` (tela de título FRLG, não a
  de Arauna).
- **B — contexto ainda sem OST Arauna:** a maioria dos mapas herdados de Hoenn
  continua com música vanilla. Isso é **intencional**: o pacote tem 21 faixas e
  o briefing pede explicitamente para não forçar uma delas em todo mapa.
- **C — resíduo a corrigir:** nenhum encontrado.
- **D — fanfares/SFX:** intocados, conforme a seção 33.

**Não** se pode dizer que "a OST foi totalmente substituída". O correto é: *as
21 faixas do pacote foram integralmente implementadas nos contextos definidos.*

## Estado de build e teste

- `mid2agb` converte as 21 MIDI sem erro; cada `.s` exporta o símbolo que
  `sound/song_table.inc` referencia e aponta para `voicegroup_arauna_ost`.
- `song_table.inc` (631 entradas, índices 0–630), `include/constants/songs.h` e
  `midi.cfg` estão consistentes entre si; todas as 21 constantes definidas são
  usadas e nenhuma constante usada está indefinida.
- Toda a suíte `repository-safety` passa, incluindo
  `validate_map_symbol_references.py` (que valida cada constante de música dos
  `map.json`).
- **A ROM compila com as 21 faixas.** Verificado na CI (`Project CI`, run
  33179807346): os passos *Build English Emerald* e *Confirm English ROM exists*
  passaram, e o job `repository-safety` ficou verde nos 38 passos. Isso prova que
  as MIDI convertem, entram na song table e linkam numa ROM real.
- **Nada foi ouvido.** Ver pendências.

## Pendências reais

1. **Qualidade musical dos arranjos** — a transcrição é automática e não
   verificada de ouvido. É a pendência principal (ver ressalva no topo).
2. **Teste in-game** — a ROM compila, mas falta rodar e validar de ouvido os 21
   contextos da seção 39 e os 2 loops completos da seção 40.
3. **Leitmotifs (seção 29)** — não garantidos pela transcrição automática.
4. **Fade/transições (seção 34)** — a fiação usa os mesmos mecanismos do vanilla
   (`playbgm`, `PlayBattleBGM`, música de mapa), então o comportamento de fade
   deve ser o do Emerald, mas isso não foi observado em execução.

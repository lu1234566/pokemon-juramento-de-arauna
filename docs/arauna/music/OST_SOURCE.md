# Arauna OST — masters de referência

As masters são **externas ao repositório**. Os MP3 (61 MB no total) não são
versionados aqui: eles são a referência artística, não o dado que entra na ROM.
A ROM carrega apenas as sequências MIDI convertidas pelo `mid2agb`.

- **Pacote oficial (master externa):**
  `https://drive.google.com/file/d/1UXbUkWeD1u94i9PWhkYGr3S6kAx7BUET/view`
  (ZIP, 21 faixas MP3, entregue em 2026-08-27)
- **Formato das masters:** MP3 estéreo, instrumental (sem voz).
- **BPM / duração:** medidos por DSP a partir da própria master (tabela abaixo).
  O BPM detectado é o que foi gravado no MIDI; onde a master tem rubato ou
  mudança de andamento, esse valor é uma média e pode precisar de ajuste manual.

| # | Master (MP3) | Função | BPM | Dur. (s) | Loop | MUS_* | MIDI |
|---|---|---|---|---:|---|---|---|
| 01 | Juramento de Arauna | Tema principal / título | 68 | 118.6 | sim | `MUS_ARAUNA_MAIN` | `mus_arauna_main.mid` |
| 02 | Onde a Jornada Nasce | Vila Amanhecer | 64 | 151.9 | sim | `MUS_ARAUNA_VILA_AMANHECER` | `mus_arauna_vila_amanhecer.mid` |
| 03 | Terra de Arauna | Rotas iniciais | 127 | 78.1 | sim | `MUS_ARAUNA_ROUTE` | `mus_arauna_route.mid` |
| 04 | Instinto Selvagem | Batalha selvagem | 140 | 21.6 | sim (curto) | `MUS_ARAUNA_WILD_BATTLE` | `mus_arauna_wild_battle.mid` |
| 05 | Um Desafio à Frente | Batalha de treinador | 98 | 116.3 | sim | `MUS_ARAUNA_TRAINER_BATTLE` | `mus_arauna_trainer_battle.mid` |
| 06 | Sempre Um Passo à Frente | Tema de Ciro (cena) | 140 | 107.2 | sim | `MUS_ARAUNA_CIRO` | `mus_arauna_ciro.mid` |
| 07 | Rival à Altura | Batalha de Ciro | 148 | 28.3 | sim (curto) | `MUS_ARAUNA_CIRO_BATTLE` | `mus_arauna_ciro_battle.mid` |
| 08 | O Preço de Vencer | Ciro final | 140 | 151.8 | sim | `MUS_ARAUNA_CIRO_FINAL` | `mus_arauna_ciro_final.mid` |
| 09 | Progresso a Qualquer Custo | Consórcio Horizonte | 98 | 193.5 | sim | `MUS_ARAUNA_HORIZON` | `mus_arauna_horizon.mid` |
| 10 | Máquina de Controle | Batalha Horizonte | 78 | 146.5 | sim | `MUS_ARAUNA_HORIZON_BATTLE` | `mus_arauna_horizon_battle.mid` |
| 11 | Prova de Arauna | Líder de Ginásio | 106 | 14.6 | sim (curto) | `MUS_ARAUNA_GYM_BATTLE` | `mus_arauna_gym_battle.mid` |
| 12 | Algo Não Deveria Estar Aqui | Boss de campanha | 148 | 143.4 | sim | `MUS_ARAUNA_STORY_BOSS` | `mus_arauna_story_boss.mid` |
| 13 | Vozes Antes dos Homens | Encontro lendário | 115 | 123.5 | sim | `MUS_ARAUNA_LEGEND_ENCOUNTER` | `mus_arauna_legend_encounter.mid` |
| 14 | Força Primordial | Batalha lendária | 83 | 186.6 | sim | `MUS_ARAUNA_LEGEND_BATTLE` | `mus_arauna_legend_battle.mid` |
| 15 | Aquele Que Lembra | Encontro com Arauá | 73 | 115.8 | sim | `MUS_ARAUNA_ARAUA_ENCOUNTER` | `mus_arauna_araua_encounter.mid` |
| 16 | O Primeiro Juramento | Batalha contra Arauá | 167 | 147.5 | sim | `MUS_ARAUNA_ARAUA_BATTLE` | `mus_arauna_araua_battle.mid` |
| 17 | O Peso do Juramento | Estrada do Juramento | 127 | 183.6 | sim | `MUS_ARAUNA_OATH_ROAD` | `mus_arauna_oath_road.mid` |
| 18 | Os Que Permaneceram de Pé | Elite Four | 85 | 147.5 | sim | `MUS_ARAUNA_ELITE_BATTLE` | `mus_arauna_elite_battle.mid` |
| 19 | Até Onde Você Chegou | Campeã Amália | 179 | 148.4 | sim | `MUS_ARAUNA_CHAMPION_BATTLE` | `mus_arauna_champion_battle.mid` |
| 20 | Depois do Juramento | Créditos | 157 | 93.7 | sim | `MUS_ARAUNA_CREDITS` | `mus_arauna_credits.mid` |
| 21 | The Sapphire Crypt | Ruína / cripta | 71 | 149.4 | sim | `MUS_ARAUNA_SAPPHIRE_CRYPT` | `mus_arauna_sapphire_crypt.mid` |

## Como as MIDI foram geradas

`tools/arauna/transcribe_ost.py` faz uma transcrição **automática por DSP** de
cada master: detecta o andamento por autocorrelação do fluxo espectral, extrai o
contorno de pitch dominante na banda média (melodia) e o fundamental na banda
grave (baixo), estima um acorde por tempo via chroma, e deriva percussão dos
picos de onset. O resultado é quantizado numa grade de semicolcheia e escrito
como MIDI multi-track.

**Isto é um ponto de partida, não um arranjo fiel.** Ver as ressalvas em
`OST_IMPLEMENTATION.md`.

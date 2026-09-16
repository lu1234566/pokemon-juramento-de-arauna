# Dossie da beta — o que faltava

Complemento de `docs/DOSSIE_BETA.md`, com o que aquele documento nao
trazia: o que cada habilidade e cada golpe novo **faz**, a tabela de
encontros mapa a mapa, e a arte das 386 criaturas.

Gerado por `tools/arauna/build_dossier_extras.py`, do proprio
repositorio: as descricoes sao as que o jogador le na tela do jogo.

## A arte

`docs/arauna/sprites/` tem tres coisas:

| pasta | o que e |
|---|---|
| `frente/` | 386 PNG de 64x64, o retrato de batalha, fundo transparente |
| `icone/` | 386 PNG de 32x32, o icone de menu, fundo transparente |
| `folha_de_contato.png` | os 386 icones numa grade de 20 colunas |

Os arquivos sao nomeados `NNN_Nome.png`, entao ordenar por nome e
ordenar por numero da dex.

## As 35 habilidades novas

A descricao e exatamente a que aparece na tela de resumo do jogo.

| # | habilidade | o que faz |
|---:|---|---|
| 78 | **LOYAL FLAME** |  |
| 79 | **WINGED WATCH** | Ups water, bug if faster. |
| 80 | **GRANITE BEAK** |  |
| 81 | **SERPENT COIL** | Tough while at full HP. |
| 82 | **SUN CROWN** | Summons sunlight in battle. |
| 83 | **MOON VEIL** | Blunts special hits in calm. |
| 84 | **TUPA VOICE** | Electric and dragon numb. |
| 85 | **RIVER SONG** | Sound moves never miss. |
| 86 | **FIRST SUN** | Ups fire and psychic in sun. |
| 87 | **FIRST MOON** | Ups SP. DEF in calm air. |
| 88 | **ETERNAL BOND** | Guards the team's stats. |
| 89 | **MANY RIVERS** | Water moves heal the user. |
| 90 | **GUARDIAN** | Softens weakness hits. |
| 91 | **FOREST RENEW** | Heals a little each turn. |
| 92 | **STORMCALL** | Summons rain in battle. |
| 93 | **DRY SPELL** | Halves damage from water. |
| 94 | **SOUTH WIND** | Lowers the foes' SPEED. |
| 95 | **LIVING SOIL** | Heals in a sandstorm. |
| 96 | **ANCIENT FIRE** | Ups fire, even in rain. |
| 97 | **MASTER TIDE** | Ups water, dragon in rain. |
| 98 | **FIRST LIGHT** | Arrives cured of all ills. |
| 99 | **LAST LIGHT** | Ups dark, fire when hurt. |
| 100 | **LIVING WISH** | Heals itself and its ally. |
| 101 | **OATH** | Raises SP. DEF on entry. |
| 102 | **WATCHFIRE** | Burns on contact. |
| 103 | **RIVER KING** |  |
| 104 | **OLD CARAPACE** | Its shell blunts weakness. |
| 105 | **ABSOLUTE SUN** | Calls the sun on entry. |
| 106 | **LONG NIGHT** | Lowers the foes' SP. ATK. |
| 107 | **ENDURANCE** |  |
| 108 | **SACRED SEA** |  |
| 109 | **RAINBOW ARC** | SPEED rises when hit hard. |
| 110 | **TURNED FEET** | Status moves go first. |
| 111 | **WHIRLWIND** | Confuses on contact. |
| 112 | **ESSENCE** |  |

## Os 27 golpes exclusivos

O nome em jogo cabe em doze caracteres; o inteiro esta ao lado, para
usar em titulo.

| golpe | em jogo | tipo | poder | precisao | PP | o que faz |
|---|---|---|---:|---:|---:|---|
| **Fairy Wind** | `FAIRY WIND` | Fairy | 40 | 100% | 30 | A gentle fairy wind that strikes the foe. |
| **Disarming Voice** | `DISARM VOICE` | Fairy | 40 | sempre | 15 | A charming cry that never misses its targets. |
| **Draining Kiss** | `DRAIN KISS` | Fairy | 50 | 100% | 10 | A life-stealing kiss that restores the user's HP. |
| **Dazzling Gleam** | `DAZZLE GLEAM` | Fairy | 80 | 100% | 10 | A brilliant fairy flash that hits opposing POKeMON. |
| **Moonblast** | `MOONBLAST` | Fairy | 95 | 100% | 10 | Moonlight strikes the foe. It may lower SP. ATK. |
| **Luar De Jaci** | `JACI MOON` | Fairy | 100 | 90% | 5 | Jaci's moonlight falls hard. It may lower SP. ATK. |
| **Juramento De Arauana** | `ARAUANA OATH` | Fairy | 105 | 90% | 5 | A regional oath strikes and raises the user's SP. DEF. |
| **Eclipse Divino** | `ECLIPSE` | Fairy | 110 | 85% | 5 | A divine eclipse erupts, but lowers the user's SP. ATK. |
| **Vira Lata Celeste** | `CELESTIAL ST` | Fire | 90 | 100% | 10 | A stray's starlit charge. It may inflict a burn. |
| **Rajada Do Banhado** | `WETLAND BURS` | Water | 90 | 95% | 10 | A burst of marsh water that may reduce SPEED. |
| **Martelo De Granito** | `GRANITE HAMM` | Rock | 95 | 90% | 10 | A hammering stone blow that may lower DEFENSE. |
| **Fogo Fatuo Ancestral** | `ANCESTRAL WI` | Fire | 85 | 100% | 10 | An old wisp-fire that may inflict a burn. |
| **Passo Ao Contrario** | `BACKWARD STE` | Grass | 80 | 100% | 15 | A backward step so quick it always strikes first. |
| **Canto Da Iara** | `IARA SONG` | Water | 75 | 100% | 10 | A luring song that may leave the foe confused. |
| **Redemoinho Do Saci** | `SACI WHIRLWI` | Flying | 80 | 95% | 10 | A sudden whirlwind that always strikes first. |
| **Encanto Do Boto** | `RIVER ENCHAN` | Psychic | 85 | 100% | 10 | A river charm that may leave the foe confused. |
| **Abraco Da Boiuna** | `BOIUNA EMBRA` | Dragon | 95 | 90% | 10 | A crushing coil that traps the foe for 2 to 5 turns. |
| **Galope Sem Cabeca** | `HEADLESS GAL` | Fire | 90 | 100% | 10 | A headlong charge that also hurts the user. |
| **Mare Da Mae** | `MOTHER TIDE` | Water | 90 | 100% | 10 | A mothering tide that restores the user's HP. |
| **Forja De Ogum** | `OGUN FORGE` | Steel | 90 | 100% | 10 | A forged strike that raises the user's DEFENSE. |
| **Olhar Da Cobra Grande** | `GREAT SERPEN` | Ghost | — | 90% | 10 | A serpent's stare that paralyzes the foe. |
| **Aurora De Guaraci** | `GUARACI DAWN` | Fire | — | sempre | 5 | A dawn that calls harsh sunlight for five turns. |
| **Trovao De Tupa** | `TUPA THUNDER` | Electric | 105 | 85% | 5 | A thunderclap that may leave the foe paralyzed. |
| **Correnteza Suprema** | `SUPREME CURR` | Water | 100 | 95% | 5 | An overwhelming current that may reduce SPEED. |
| **Incendio Primordial** | `PRIMORDIAL B` | Fire | 110 | 85% | 5 | A first fire so fierce it also hurts the user. |
| **Marulho Atlantico** | `ATLANTIC SUR` | Water | 105 | 90% | 5 | An ocean swell that may make the foe flinch. |
| **Essencia Primordial** | `PRIMORDIAL E` | Dragon | 110 | 90% | 5 | A first-born surge that lowers the user's SP. ATK. |

## Onde cada criatura aparece

116 mapas com encontro. A taxa e a chance de o mapa gerar um encontro
a cada passo; quanto maior, mais frequente.

### ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS

- **surfe** (taxa 4): #226 Golfinho (5-35), #233 Pescadão (30-35), #306 Perereca (5-35), #325 Bueiro (5-35)
- **pesca** (taxa 20): #223 Cavalim-Marinho (30-35), #226 Golfinho (5-30), #231 Peixe-Espada (25-35), #233 Pescadão (5-30), #256 Iemanjá-Pequena (25-30), #306 Perereca (20-25), #325 Bueiro (10-30)

### ABANDONED_SHIP_ROOMS_B1F

- **surfe** (taxa 4): #223 Cavalim-Marinho (30-35), #226 Golfinho (5-35), #233 Pescadão (5-35), #267 Marinheiro (5-35)
- **pesca** (taxa 20): #223 Cavalim-Marinho (25-30), #226 Golfinho (5-30), #231 Peixe-Espada (30-35), #233 Pescadão (5-30), #256 Iemanjá-Pequena (20-25), #267 Marinheiro (10-30), #325 Bueiro (25-35)

### ALTERING_CAVE

- **grama** (taxa 7): #011 Saúvarco (22-24), #016 Boitatá (20-28), #178 Jequitibá (18), #195 Mandioca (26), #358 Tamanduão (20-26), #360 Preguiçoso (20), #362 Beija-Luz (26), #371 Zabumba (24)

### ARTISAN_CAVE_1F

- **grama** (taxa 10): #016 Boitatá (40-46), #093 Vampiro (45), #197 Rochão (43-48), #199 Ametista (41-44), #200 Ouríço (49), #211 Fóssil (50), #213 Vulcanite (50), #214 Marmim (47)

### ARTISAN_CAVE_B1F

- **grama** (taxa 10): #016 Boitatá (40-46), #093 Vampiro (45), #197 Rochão (43-48), #199 Ametista (41-44), #200 Ouríço (49), #211 Fóssil (50), #213 Vulcanite (50), #214 Marmim (47)

### CAVE_OF_ORIGIN_1F

- **grama** (taxa 4): #123 Piranha (30-32), #127 Curimbatá (34), #128 Traíra (30-34), #130 Tucunaré (34), #131 Pacu (36), #134 Cascudo (31-32), #209 Estalactite (35), #252 Anhangá-Pitã (33), #255 Zumbi (33)

### CAVE_OF_ORIGIN_ENTRANCE

- **grama** (taxa 4): #123 Piranha (30-32), #127 Curimbatá (35), #128 Traíra (33-34), #130 Tucunaré (29), #131 Pacu (36), #134 Cascudo (28-31), #209 Estalactite (35), #279 Onçuma (33), #350 Bugio (34)

### CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP1

- **grama** (taxa 4): #123 Piranha (30-33), #127 Curimbatá (34), #128 Traíra (30-34), #130 Tucunaré (34), #131 Pacu (36), #134 Cascudo (31-32), #181 Vitóriarégia (33), #209 Estalactite (35)

### CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP2

- **grama** (taxa 4): #123 Piranha (30-33), #127 Curimbatá (34), #128 Traíra (30-34), #130 Tucunaré (34), #131 Pacu (36), #134 Cascudo (31-32), #181 Vitóriarégia (33), #209 Estalactite (35)

### CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP3

- **grama** (taxa 4): #123 Piranha (30-33), #127 Curimbatá (34), #128 Traíra (30-34), #130 Tucunaré (34), #131 Pacu (36), #134 Cascudo (31-32), #181 Vitóriarégia (33), #209 Estalactite (35)

### DESERT_UNDERPASS

- **grama** (taxa 10): #016 Boitatá (35-41), #030 Tatuçu (40), #078 Coati (43), #116 Cabrita (42), #185 Babaçu (36), #369 Sanfoninha (45), #370 Violeiro (44), #371 Zabumba (38-40), #372 Cordelim (38)

### DEWFORD_TOWN

- **surfe** (taxa 4): #012 Capivim (5-35), #085 Sapim (15-25), #216 Caranguim (25-30), #224 Tartaruguim (25-30)
- **pesca** (taxa 10): #012 Capivim (30-35), #055 Peixim (20-30), #058 Mandim (10-30), #085 Sapim (35-40), #104 Cabocim (5-30), #216 Caranguim (40-45), #228 Tubarim (5-30)

### EVER_GRANDE_CITY

- **surfe** (taxa 4): #130 Tucunaré (15-25), #181 Vitóriarégia (25-30), #186 Buriti (25-30), #209 Estalactite (5-35)
- **pesca** (taxa 10): #057 Mãe-d'Água (30-35), #122 Pirarucu (10-30), #125 Aruanã (40-45), #126 Poraquê (30-35), #130 Tucunaré (5-30), #131 Pacu (35-40), #209 Estalactite (5-30)

### FIERY_PATH

- **grama** (taxa 10): #028 Tatuim (16), #029 Tatubola (16), #078 Coati (16), #101 Cerválo (15), #116 Cabrita (14), #117 Chocalhão (15), #185 Babaçu (14), #198 Cristalim (15), #201 Ferrolho (15), #209 Estalactite (15), #210 Estalagmite (14), #215 Granito (16)

### GRANITE_CAVE_1F

- **grama** (taxa 10): #078 Coati (6), #091 Morcim (7), #198 Cristalim (7-10), #201 Ferrolho (6), #204 Manganim (8), #209 Estalactite (8), #210 Estalagmite (9), #211 Fóssil (7-8), #215 Granito (8-9)

### GRANITE_CAVE_B1F

- **grama** (taxa 10): #078 Coati (11), #091 Morcim (10), #198 Cristalim (9-10), #201 Ferrolho (10), #204 Manganim (9), #209 Estalactite (11), #211 Fóssil (9), #215 Granito (10-11)

### GRANITE_CAVE_B2F

- **grama** (taxa 10): #078 Coati (10), #091 Morcim (11-12), #198 Cristalim (10), #201 Ferrolho (10), #204 Manganim (12), #209 Estalactite (11), #211 Fóssil (10), #215 Granito (11-12)
- **pedra** (taxa 20): #198 Cristalim (10-20), #209 Estalactite (15-20), #211 Fóssil (15-20), #215 Granito (5-10)

### GRANITE_CAVE_STEVENS_ROOM

- **grama** (taxa 10): #078 Coati (8), #091 Morcim (8-9), #198 Cristalim (7-10), #201 Ferrolho (8), #204 Manganim (7), #209 Estalactite (6), #211 Fóssil (8), #215 Granito (7-8)

### JAGGED_PASS

- **grama** (taxa 20): #021 Cactula (22), #029 Tatubola (21), #116 Cabrita (20), #185 Babaçu (22), #201 Ferrolho (22), #211 Fóssil (20-22), #213 Vulcanite (22), #215 Granito (20-21)

### LILYCOVE_CITY

- **surfe** (taxa 4): #226 Golfinho (5-35), #306 Perereca (25-30), #310 Ferrugem (15-25), #325 Bueiro (25-30)
- **pesca** (taxa 10): #226 Golfinho (10-30), #227 Baleia (40-45), #231 Peixe-Espada (5-30), #233 Pescadão (5-30), #267 Marinheiro (25-30), #306 Perereca (35-40), #325 Bueiro (30-35)

### MAGMA_HIDEOUT_1F

- **grama** (taxa 10): #110 Ogum (33), #116 Cabrita (28-29), #185 Babaçu (31), #201 Ferrolho (30), #209 Estalactite (27-28), #213 Vulcanite (30), #215 Granito (30), #274 Reisado (30), #285 Boitatá-Puro (32)

### MAGMA_HIDEOUT_2F_1R

- **grama** (taxa 10): #078 Coati (30), #116 Cabrita (28-29), #201 Ferrolho (30), #209 Estalactite (27-28), #210 Estalagmite (31), #215 Granito (30), #246 Guaraci (32), #277 Congada (30), #297 Corcovado-Ancião (33)

### MAGMA_HIDEOUT_2F_2R

- **grama** (taxa 10): #106 Cangaço (30), #116 Cabrita (28-29), #185 Babaçu (30), #201 Ferrolho (30), #209 Estalactite (27-28), #210 Estalagmite (31), #215 Granito (30), #282 Draguará-Alfa (32), #371 Zabumba (33)

### MAGMA_HIDEOUT_2F_3R

- **grama** (taxa 10): #016 Boitatá (32), #116 Cabrita (28), #160 Carcará (30), #185 Babaçu (31), #195 Mandioca (30), #201 Ferrolho (30), #209 Estalactite (27-28), #210 Estalagmite (29), #211 Fóssil (33), #215 Granito (30)

### MAGMA_HIDEOUT_3F_1R

- **grama** (taxa 10): #107 Xangô (30), #116 Cabrita (30), #201 Ferrolho (28), #209 Estalactite (27-28), #210 Estalagmite (31), #211 Fóssil (33), #213 Vulcanite (32), #214 Marmim (29), #215 Granito (30), #270 Beata (30)

### MAGMA_HIDEOUT_3F_2R

- **grama** (taxa 10): #078 Coati (30), #116 Cabrita (28), #153 Corupião (30), #201 Ferrolho (29), #202 Diamantina (32), #206 Enxofrino (30), #209 Estalactite (27-28), #210 Estalagmite (31), #211 Fóssil (33), #215 Granito (30)

### MAGMA_HIDEOUT_3F_3R

- **grama** (taxa 10): #078 Coati (30), #100 Corcovado (32), #116 Cabrita (28), #175 João-de-Barro (30), #201 Ferrolho (30), #209 Estalactite (27-28), #210 Estalagmite (31), #211 Fóssil (33), #215 Granito (29), #269 Cangaceiro (30)

### MAGMA_HIDEOUT_4F

- **grama** (taxa 10): #054 Guaraflama (30), #116 Cabrita (28-29), #185 Babaçu (31), #201 Ferrolho (30), #209 Estalactite (27-28), #211 Fóssil (30), #213 Vulcanite (33), #215 Granito (30), #284 Petropico-Ancião (32)

### METEOR_FALLS_1F_1R

- **grama** (taxa 10): #123 Piranha (16-18), #127 Curimbatá (14), #128 Traíra (15-19), #130 Tucunaré (16), #131 Pacu (20), #134 Cascudo (14-17), #181 Vitóriarégia (19), #209 Estalactite (20), #273 Bumba-Meu-Boi (18)
- **surfe** (taxa 4): #123 Piranha (5-35), #128 Traíra (5-15), #134 Cascudo (15-25), #209 Estalactite (25-35)
- **pesca** (taxa 30): #125 Aruanã (30-35), #126 Poraquê (40-45), #128 Traíra (5-30), #130 Tucunaré (5-30), #131 Pacu (20-30), #134 Cascudo (10-30), #165 Jaburu (35-40)

### METEOR_FALLS_1F_2R

- **grama** (taxa 10): #123 Piranha (33), #127 Curimbatá (39), #128 Traíra (35-38), #130 Tucunaré (37), #131 Pacu (40), #134 Cascudo (33-35), #181 Vitóriarégia (38), #203 Bauxito (35), #209 Estalactite (40)
- **surfe** (taxa 4): #123 Piranha (30-35), #128 Traíra (5-15), #134 Cascudo (15-25), #209 Estalactite (25-35)
- **pesca** (taxa 30): #125 Aruanã (30-35), #126 Poraquê (40-45), #127 Curimbatá (10-30), #128 Traíra (5-30), #131 Pacu (25-35), #134 Cascudo (5-30), #165 Jaburu (35-40)

### METEOR_FALLS_B1F_1R

- **grama** (taxa 10): #123 Piranha (33), #127 Curimbatá (39), #128 Traíra (35-38), #130 Tucunaré (37), #131 Pacu (40), #134 Cascudo (33-35), #181 Vitóriarégia (38), #200 Ouríço (35), #209 Estalactite (40)
- **surfe** (taxa 4): #123 Piranha (30-35), #128 Traíra (5-15), #134 Cascudo (15-25), #209 Estalactite (25-35)
- **pesca** (taxa 30): #125 Aruanã (35-40), #127 Curimbatá (25-35), #128 Traíra (5-30), #130 Tucunaré (10-30), #131 Pacu (30-35), #134 Cascudo (5-30), #165 Jaburu (40-45)

### METEOR_FALLS_B1F_2R

- **grama** (taxa 10): #123 Piranha (30-33), #127 Curimbatá (39), #128 Traíra (35-38), #130 Tucunaré (37), #131 Pacu (40), #134 Cascudo (35), #181 Vitóriarégia (38), #204 Manganim (25), #209 Estalactite (40)
- **surfe** (taxa 4): #123 Piranha (30-35), #128 Traíra (5-15), #134 Cascudo (15-25), #209 Estalactite (25-35)
- **pesca** (taxa 30): #125 Aruanã (35-40), #127 Curimbatá (25-35), #128 Traíra (5-30), #130 Tucunaré (10-30), #131 Pacu (30-35), #134 Cascudo (5-30), #165 Jaburu (40-45)

### METEOR_FALLS_STEVENS_CAVE

- **grama** (taxa 10): #123 Piranha (33-35), #127 Curimbatá (39), #128 Traíra (35-38), #130 Tucunaré (37), #131 Pacu (40), #134 Cascudo (33-35), #181 Vitóriarégia (38), #209 Estalactite (40)

### MIRAGE_TOWER_1F

- **grama** (taxa 10): #021 Cactula (22), #029 Tatubola (20-21), #106 Cangaço (24), #116 Cabrita (20-21), #118 Cascavelim (23), #160 Carcará (24), #185 Babaçu (20-23), #211 Fóssil (22), #215 Granito (20)

### MIRAGE_TOWER_2F

- **grama** (taxa 10): #021 Cactula (20), #029 Tatubola (20-22), #116 Cabrita (20-21), #118 Cascavelim (24), #160 Carcará (24), #185 Babaçu (20-23), #211 Fóssil (23), #215 Granito (22)

### MIRAGE_TOWER_3F

- **grama** (taxa 10): #021 Cactula (20), #029 Tatubola (20-22), #116 Cabrita (20-21), #118 Cascavelim (24), #160 Carcará (24), #185 Babaçu (20-23), #211 Fóssil (23), #215 Granito (22)

### MIRAGE_TOWER_4F

- **grama** (taxa 10): #021 Cactula (20), #029 Tatubola (20-22), #116 Cabrita (20-21), #118 Cascavelim (24), #160 Carcará (24), #185 Babaçu (20-23), #211 Fóssil (23), #215 Granito (22)

### MOSSDEEP_CITY

- **surfe** (taxa 4): #223 Cavalim-Marinho (15-25), #226 Golfinho (5-35), #267 Marinheiro (25-30), #364 Sarará (25-30)
- **pesca** (taxa 10): #223 Cavalim-Marinho (25-35), #226 Golfinho (5-30), #231 Peixe-Espada (5-30), #233 Pescadão (10-30), #256 Iemanjá-Pequena (30-35), #267 Marinheiro (40-45), #364 Sarará (35-40)

### MT_PYRE_1F

- **grama** (taxa 10): #038 Preguicão (24), #159 Urutau (24), #171 Sanhaço (22), #172 Papa-Formiga (23), #189 Açaí (25-29), #242 Anhangá (26-27), #249 Jenipapo (28-29), #253 Yara-Pindá (24), #296 Amazona (29)

### MT_PYRE_2F

- **grama** (taxa 10): #017 Curupim (24), #041 Papagaio (24), #159 Urutau (25-29), #180 Orquidina (23), #189 Açaí (28-29), #214 Marmim (24), #242 Anhangá (22), #249 Jenipapo (26-27), #287 Curupira-Rei (29)

### MT_PYRE_3F

- **grama** (taxa 10): #017 Curupim (29), #038 Preguicão (24), #159 Urutau (23), #171 Sanhaço (24), #189 Açaí (28-29), #214 Marmim (25-29), #242 Anhangá (26-27), #249 Jenipapo (22), #253 Yara-Pindá (24)

### MT_PYRE_4F

- **grama** (taxa 10): #038 Preguicão (27), #041 Papagaio (25), #159 Urutau (24), #189 Açaí (25-27), #242 Anhangá (26-27), #249 Jenipapo (28-29), #253 Yara-Pindá (29), #257 Ossanha (22), #261 Curupira-Ancião (23)

### MT_PYRE_5F

- **grama** (taxa 10): #017 Curupim (22), #038 Preguicão (27), #041 Papagaio (25), #120 Jararaca (23), #159 Urutau (24), #189 Açaí (25-27), #242 Anhangá (26-27), #249 Jenipapo (28-29), #253 Yara-Pindá (29)

### MT_PYRE_6F

- **grama** (taxa 10): #038 Preguicão (27), #041 Papagaio (25), #069 Jaguatirica (22), #145 Piolhão (23), #159 Urutau (24), #189 Açaí (25-27), #242 Anhangá (26-27), #249 Jenipapo (28-29), #253 Yara-Pindá (29)

### MT_PYRE_EXTERIOR

- **grama** (taxa 10): #038 Preguicão (27), #041 Papagaio (26), #072 Paca (25), #156 Beija-flor (29), #159 Urutau (27), #189 Açaí (27-29), #242 Anhangá (27-28), #249 Jenipapo (27-29), #253 Yara-Pindá (28)

### MT_PYRE_SUMMIT

- **grama** (taxa 10): #017 Curupim (28), #041 Papagaio (30), #149 Aranhão (28), #159 Urutau (26), #189 Açaí (24), #214 Marmim (25), #242 Anhangá (27-28), #249 Jenipapo (29-30), #253 Yara-Pindá (28)

### NEW_MAUVILLE_ENTRANCE

- **grama** (taxa 10): #146 Barata (22), #264 Exu (22), #272 Rei-Momo (26), #307 Lagartixa (26), #310 Ferrugem (25), #316 Latinha (23), #320 Pilhoso (24-25), #323 Aluminio (24), #326 Sinal (23), #327 Poste (22), #365 Cambota (22)

### NEW_MAUVILLE_INSIDE

- **grama** (taxa 10): #146 Barata (26), #236 Bicho-Papão (26), #299 Ratão (26), #308 Traça-Papel (26), #310 Ferrugem (25), #315 Bituca (23), #320 Pilhoso (23), #321 Cabofio (22), #323 Aluminio (24-25), #324 Concretim (22), #326 Sinal (24)

### PACIFIDLOG_TOWN

- **surfe** (taxa 4): #144 Caramulão (5-35), #165 Jaburu (25-30), #181 Vitóriarégia (15-25), #253 Yara-Pindá (25-30)
- **pesca** (taxa 10): #124 Tambaqui (35-40), #125 Aruanã (5-30), #127 Curimbatá (40-45), #131 Pacu (10-30), #132 Matrinxã (25-35), #165 Jaburu (5-30), #231 Peixe-Espada (30-35)

### PETALBURG_CITY

- **surfe** (taxa 1): #035 Jacarão (10-30), #193 Mate (30-35), #248 Aluá (5-10), #325 Bueiro (5-10)
- **pesca** (taxa 10): #046 Sucurim (40-45), #059 Mandí (10-30), #124 Tambaqui (5-30), #128 Traíra (35-40), #130 Tucunaré (20-30), #132 Matrinxã (5-30), #133 Piau (30-35)

### PETALBURG_WOODS

- **grama** (taxa 20): #014 Sagüim (5), #037 Preguicim (6), #049 Borbolim (5), #067 Gatim (5), #070 Cutim (5), #076 Quatim (5), #136 Vagalumim (6), #138 Cigarrinho (6), #163 Corurupim (6), #190 Cacauim (6), #228 Tubarim (5), #359 Preguicinha (5)

### ROUTE101

- **grama** (taxa 20): #010 Formilim (3), #052 Guaracim (2), #064 Aranin (2), #088 Teiuzim (2), #097 Mulinha (2), #111 Cavalim (3), #113 Zebuim (3), #140 Louvadinha (3), #176 Sementim (3), #207 Argilim (3), #351 Tuim (3), #354 Preazinho (2)

### ROUTE102

- **grama** (taxa 20): #022 Muriçoco (3), #031 Ararinha (4), #052 Guaracim (3), #064 Aranin (3), #094 Piuiuim (4), #113 Zebuim (4), #140 Louvadinha (3), #147 Grilim (4), #176 Sementim (4), #190 Cacauim (3), #351 Tuim (3), #359 Preguicinha (4)
- **surfe** (taxa 4): #025 Botim (30-35), #034 Jacarim (10-20), #058 Mandim (20-30), #085 Sapim (20-30), #104 Cabocim (5-10)
- **pesca** (taxa 30): #012 Capivim (35-40), #025 Botim (20-30), #034 Jacarim (10-30), #055 Peixim (10-30), #058 Mandim (5-10), #085 Sapim (10-30), #104 Cabocim (5-10), #216 Caranguim (40-45), #228 Tubarim (30-35)

### ROUTE103

- **grama** (taxa 20): #012 Capivim (3), #022 Muriçoco (3), #031 Ararinha (3), #043 Antinha (2), #094 Piuiuim (4), #111 Cavalim (3), #113 Zebuim (4), #190 Cacauim (3), #196 Pedrinha (2), #228 Tubarim (4), #354 Preazinho (2), #359 Preguicinha (3)
- **surfe** (taxa 4): #025 Botim (15-25), #034 Jacarim (5-35), #058 Mandim (25-30), #085 Sapim (10-30), #104 Cabocim (25-30)
- **pesca** (taxa 30): #012 Capivim (35-40), #025 Botim (5-10), #034 Jacarim (10-30), #055 Peixim (5-10), #058 Mandim (10-30), #085 Sapim (25-35), #104 Cabocim (10-30), #165 Jaburu (40-45), #228 Tubarim (30-35)

### ROUTE104

- **grama** (taxa 20): #022 Muriçoco (4), #037 Preguicim (4), #040 Papaguim (5), #043 Antinha (5), #049 Borbolim (4), #079 Gambá (5), #082 Tuquinho (4), #136 Vagalumim (4), #138 Cigarrinho (5), #163 Corurupim (5), #190 Cacauim (4), #220 Polvim (3)
- **surfe** (taxa 4): #055 Peixim (25-30), #085 Sapim (25-30), #216 Caranguim (10-30), #220 Polvim (15-25), #228 Tubarim (15-25)
- **pesca** (taxa 30): #055 Peixim (5-30), #058 Mandim (35-40), #104 Cabocim (30-35), #125 Aruanã (40-45), #216 Caranguim (10-30), #220 Polvim (20-30), #224 Tartaruguim (5-10), #228 Tubarim (10-30)

### ROUTE105

- **surfe** (taxa 4): #012 Capivim (5-35), #085 Sapim (15-25), #216 Caranguim (25-30), #224 Tartaruguim (25-30)
- **pesca** (taxa 30): #012 Capivim (30-35), #055 Peixim (20-30), #058 Mandim (10-30), #085 Sapim (35-40), #104 Cabocim (5-30), #216 Caranguim (40-45), #228 Tubarim (5-30)

### ROUTE106

- **surfe** (taxa 4): #012 Capivim (5-35), #085 Sapim (15-25), #216 Caranguim (25-30), #224 Tartaruguim (25-30)
- **pesca** (taxa 30): #012 Capivim (30-35), #055 Peixim (20-30), #058 Mandim (10-30), #085 Sapim (35-40), #104 Cabocim (5-30), #216 Caranguim (40-45), #228 Tubarim (5-30)

### ROUTE107

- **surfe** (taxa 4): #012 Capivim (5-35), #085 Sapim (15-25), #216 Caranguim (25-30), #224 Tartaruguim (25-30)
- **pesca** (taxa 30): #012 Capivim (30-35), #055 Peixim (20-30), #058 Mandim (10-30), #085 Sapim (35-40), #104 Cabocim (5-30), #216 Caranguim (40-45), #228 Tubarim (5-30)

### ROUTE108

- **surfe** (taxa 4): #012 Capivim (5-35), #085 Sapim (15-25), #216 Caranguim (25-30), #224 Tartaruguim (25-30)
- **pesca** (taxa 30): #012 Capivim (30-35), #055 Peixim (20-30), #058 Mandim (10-30), #085 Sapim (35-40), #104 Cabocim (5-30), #216 Caranguim (40-45), #228 Tubarim (5-30)

### ROUTE109

- **surfe** (taxa 4): #012 Capivim (5-35), #085 Sapim (15-25), #216 Caranguim (25-30), #224 Tartaruguim (25-30)
- **pesca** (taxa 30): #012 Capivim (30-35), #055 Peixim (20-30), #058 Mandim (10-30), #085 Sapim (35-40), #104 Cabocim (5-30), #216 Caranguim (40-45), #228 Tubarim (5-30)

### ROUTE110

- **grama** (taxa 20): #086 Sapão (13), #220 Polvim (12-13), #226 Golfinho (13), #228 Tubarim (12), #231 Peixe-Espada (12), #300 Pombim (12), #308 Traça-Papel (13), #313 Lixão (12), #317 Sacolim (13), #351 Tuim (12), #356 Tamanduí (13)
- **surfe** (taxa 4): #086 Sapão (5-35), #216 Caranguim (25-30), #220 Polvim (15-25), #228 Tubarim (25-30)
- **pesca** (taxa 30): #086 Sapão (10-30), #216 Caranguim (35-40), #220 Polvim (20-30), #224 Tartaruguim (40-45), #228 Tubarim (5-30), #231 Peixe-Espada (5-30), #233 Pescadão (30-35)

### ROUTE111

- **grama** (taxa 10): #021 Cactula (21), #029 Tatubola (20-21), #081 Sarué (19), #116 Cabrita (19-20), #154 Cupinzim (22), #185 Babaçu (20-21), #215 Granito (22), #237 Lobisomem (19), #357 Tamanduá (20)
- **surfe** (taxa 4): #035 Jacarão (5-10), #086 Sapão (10-30), #186 Buriti (30-35), #209 Estalactite (20-30)
- **pedra** (taxa 20): #024 Tamanduá (15-20), #029 Tatubola (5-15), #154 Cupinzim (15-20), #357 Tamanduá (15-20)
- **pesca** (taxa 30): #035 Jacarão (30-35), #086 Sapão (5-30), #126 Poraquê (10-30), #130 Tucunaré (20-30), #165 Jaburu (40-45), #186 Buriti (5-30), #209 Estalactite (35-40)

### ROUTE112

- **grama** (taxa 20): #021 Cactula (16), #028 Tatuim (14), #029 Tatubola (15-16), #116 Cabrita (14-16), #142 Escorpim (15), #185 Babaçu (16), #187 Cajuzim (15), #201 Ferrolho (14), #213 Vulcanite (16), #215 Granito (16)

### ROUTE113

- **grama** (taxa 20): #028 Tatuim (14-16), #029 Tatubola (15), #098 Mula (14-15), #116 Cabrita (16), #154 Cupinzim (16), #201 Ferrolho (16), #207 Argilim (15), #238 Corpo-Seco (16), #357 Tamanduá (14), #361 Beija-Flor (16)

### ROUTE114

- **grama** (taxa 20): #012 Capivim (15-17), #035 Jacarão (16), #059 Mandí (15), #086 Sapão (16), #127 Curimbatá (17), #130 Tucunaré (15), #174 Bacurau (18), #235 Cuca (16), #361 Beija-Flor (15), #375 Piranhita (16-17)
- **surfe** (taxa 4): #012 Capivim (5-10), #035 Jacarão (30-35), #086 Sapão (20-30), #375 Piranhita (10-30)
- **pedra** (taxa 20): #127 Curimbatá (5-15), #134 Cascudo (15-20), #154 Cupinzim (15-20), #357 Tamanduá (15-20)
- **pesca** (taxa 30): #035 Jacarão (35-40), #059 Mandí (5-30), #127 Curimbatá (10-30), #128 Traíra (30-35), #130 Tucunaré (20-30), #134 Cascudo (40-45), #375 Piranhita (5-30)

### ROUTE115

- **grama** (taxa 20): #038 Preguicão (24), #041 Papagaio (26), #103 Suçuapara (24), #125 Aruanã (24), #131 Pacu (25), #144 Caramulão (23-25), #157 Sabiá (25), #179 Bromelinha (23-25), #253 Yara-Pindá (25)
- **surfe** (taxa 4): #144 Caramulão (15-25), #179 Bromelinha (5-35), #181 Vitóriarégia (25-30), #253 Yara-Pindá (25-30)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (30-35), #131 Pacu (5-30), #179 Bromelinha (40-45), #231 Peixe-Espada (20-30), #233 Pescadão (35-40)

### ROUTE116

- **grama** (taxa 20): #010 Formilim (7), #052 Guaracim (7), #064 Aranin (6), #088 Teiuzim (6), #097 Mulinha (8), #140 Louvadinha (6), #147 Grilim (8), #176 Sementim (7), #207 Argilim (7), #351 Tuim (7), #356 Tamanduí (6), #361 Beija-Flor (8)

### ROUTE117

- **grama** (taxa 20): #038 Preguicão (13), #041 Papagaio (14), #065 Caraninha (13-14), #086 Sapão (14), #098 Mula (13), #152 Traça (13), #259 Saciamigo (13), #263 Pomba-Gira (13), #361 Beija-Flor (13), #366 Berimbau (13)
- **surfe** (taxa 4): #086 Sapão (10-30), #144 Caramulão (20-30), #179 Bromelinha (5-10), #253 Yara-Pindá (30-35)
- **pesca** (taxa 30): #057 Mãe-d'Água (5-30), #086 Sapão (30-35), #124 Tambaqui (20-30), #125 Aruanã (5-30), #126 Poraquê (40-45), #130 Tucunaré (35-40), #131 Pacu (10-30)

### ROUTE118

- **grama** (taxa 20): #057 Mãe-d'Água (26), #074 Marimbondo (25), #125 Aruanã (24), #131 Pacu (26), #144 Caramulão (24-26), #165 Jaburu (27), #179 Bromelinha (25), #262 Caipora-Fêmea (26), #271 Menino-Deus (26), #349 Aracuã (25)
- **surfe** (taxa 4): #125 Aruanã (25-30), #144 Caramulão (5-35), #181 Vitóriarégia (15-25), #253 Yara-Pindá (25-30)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #059 Mandí (30-35), #124 Tambaqui (40-45), #125 Aruanã (5-30), #131 Pacu (5-30), #144 Caramulão (35-40), #165 Jaburu (20-35)

### ROUTE119

- **grama** (taxa 15): #057 Mãe-d'Água (26), #073 Formigão (24), #125 Aruanã (25), #131 Pacu (25), #144 Caramulão (25-27), #165 Jaburu (27), #179 Bromelinha (25), #181 Vitóriarégia (26), #183 Cipó (27), #184 Palmito (27)
- **surfe** (taxa 4): #125 Aruanã (25-30), #144 Caramulão (5-35), #179 Bromelinha (15-25), #253 Yara-Pindá (25-30)
- **pesca** (taxa 30): #124 Tambaqui (10-30), #125 Aruanã (5-30), #130 Tucunaré (35-40), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (20-30), #181 Vitóriarégia (40-45)

### ROUTE120

- **grama** (taxa 20): #153 Corupião (25), #154 Cupinzim (25), #155 Formigão-Preto (25), #168 Anú (26), #169 Trinca-Ferro (27), #170 Curió (27), #241 Comadre (27), #242 Anhangá (25), #288 Saci-Rei (25), #357 Tamanduá (25-27)
- **surfe** (taxa 4): #144 Caramulão (5-10), #179 Bromelinha (30-35), #186 Buriti (20-30), #253 Yara-Pindá (10-30)
- **pesca** (taxa 30): #057 Mãe-d'Água (5-30), #124 Tambaqui (30-35), #125 Aruanã (5-30), #126 Poraquê (35-40), #130 Tucunaré (20-30), #131 Pacu (10-30), #253 Yara-Pindá (40-45)

### ROUTE121

- **grama** (taxa 20): #125 Aruanã (26-28), #144 Caramulão (26), #158 Bem-te-vi (28), #162 Urubu (25), #179 Bromelinha (26), #253 Yara-Pindá (27), #265 Preto-Velho (28), #278 Folião (26), #302 Baratão (28), #368 Pandeirim (28)
- **surfe** (taxa 4): #144 Caramulão (15-25), #179 Bromelinha (5-35), #181 Vitóriarégia (25-30), #253 Yara-Pindá (25-30)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #124 Tambaqui (30-35), #125 Aruanã (5-30), #130 Tucunaré (35-40), #131 Pacu (5-30), #231 Peixe-Espada (20-30), #233 Pescadão (40-45)

### ROUTE122

- **surfe** (taxa 4): #135 Acará (15-25), #223 Cavalim-Marinho (25-30), #226 Golfinho (25-30), #253 Yara-Pindá (5-35)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (35-40), #128 Traíra (5-30), #130 Tucunaré (5-30), #131 Pacu (40-45), #165 Jaburu (30-35), #233 Pescadão (25-35)

### ROUTE123

- **grama** (taxa 20): #057 Mãe-d'Água (27), #075 Abelhinha (28), #125 Aruanã (26), #131 Pacu (26-28), #144 Caramulão (26), #151 Marimbondão (28), #167 Seriema (28), #179 Bromelinha (25), #182 Ipê (26), #251 Caipora (28)
- **surfe** (taxa 4): #125 Aruanã (25-30), #144 Caramulão (5-35), #186 Buriti (15-25), #253 Yara-Pindá (25-30)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #124 Tambaqui (35-40), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (20-30)

### ROUTE124

- **surfe** (taxa 4): #019 Iaraço (25-30), #125 Aruanã (25-30), #144 Caramulão (5-35), #181 Vitóriarégia (15-25)
- **pesca** (taxa 30): #057 Mãe-d'Água (5-30), #124 Tambaqui (40-45), #125 Aruanã (5-30), #130 Tucunaré (35-40), #131 Pacu (10-30), #144 Caramulão (25-35), #181 Vitóriarégia (30-35)

### ROUTE125

- **surfe** (taxa 4): #131 Pacu (25-30), #144 Caramulão (5-35), #181 Vitóriarégia (15-25), #253 Yara-Pindá (25-30)
- **pesca** (taxa 30): #057 Mãe-d'Água (5-30), #124 Tambaqui (40-45), #125 Aruanã (10-30), #130 Tucunaré (35-40), #131 Pacu (5-30), #144 Caramulão (25-35), #181 Vitóriarégia (30-35)

### ROUTE126

- **surfe** (taxa 4): #045 Antaraú (15-25), #125 Aruanã (25-30), #131 Pacu (25-30), #144 Caramulão (5-35)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (25-35), #181 Vitóriarégia (35-40)

### ROUTE127

- **surfe** (taxa 4): #131 Pacu (25-30), #144 Caramulão (15-25), #181 Vitóriarégia (5-35), #253 Yara-Pindá (25-30)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (25-35), #181 Vitóriarégia (35-40)

### ROUTE128

- **surfe** (taxa 4): #125 Aruanã (25-30), #131 Pacu (25-30), #144 Caramulão (5-35), #248 Aluá (15-25)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (30-35), #181 Vitóriarégia (35-40)

### ROUTE129

- **surfe** (taxa 4): #125 Aruanã (25-30), #131 Pacu (25-30), #144 Caramulão (5-35), #256 Iemanjá-Pequena (15-25)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (25-35), #181 Vitóriarégia (35-40)

### ROUTE130

- **grama** (taxa 20): #125 Aruanã (25-30), #131 Pacu (20-35), #144 Caramulão (10-40), #161 Gavião (50), #181 Vitóriarégia (45), #223 Cavalim-Marinho (5), #250 Urucum (15), #253 Yara-Pindá (5), #290 Muirá-Kytã (10)
- **surfe** (taxa 4): #125 Aruanã (25-30), #131 Pacu (25-30), #144 Caramulão (5-35), #253 Yara-Pindá (15-25)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (25-35), #181 Vitóriarégia (35-40)

### ROUTE131

- **surfe** (taxa 4): #125 Aruanã (25-30), #131 Pacu (25-30), #144 Caramulão (5-35), #181 Vitóriarégia (15-25)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (25-35), #181 Vitóriarégia (35-40)

### ROUTE132

- **surfe** (taxa 4): #125 Aruanã (25-30), #131 Pacu (25-30), #144 Caramulão (5-35), #181 Vitóriarégia (15-25)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (25-35), #181 Vitóriarégia (35-40)

### ROUTE133

- **surfe** (taxa 4): #125 Aruanã (25-30), #131 Pacu (25-30), #144 Caramulão (5-35), #181 Vitóriarégia (15-25)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (25-35), #181 Vitóriarégia (35-40)

### ROUTE134

- **surfe** (taxa 4): #125 Aruanã (25-30), #131 Pacu (25-30), #144 Caramulão (5-35), #181 Vitóriarégia (15-25)
- **pesca** (taxa 30): #057 Mãe-d'Água (10-30), #125 Aruanã (5-30), #130 Tucunaré (40-45), #131 Pacu (5-30), #144 Caramulão (30-35), #165 Jaburu (25-35), #181 Vitóriarégia (35-40)

### RUSTURF_TUNNEL

- **grama** (taxa 10): #014 Sagüim (7), #028 Tatuim (5-6), #061 Preguim (6), #091 Morcim (7), #198 Cristalim (5-6), #201 Ferrolho (8), #204 Manganim (5), #209 Estalactite (8), #215 Granito (8)

### SAFARI_ZONE_NORTH

- **grama** (taxa 25): #013 Tucanhão (27), #073 Formigão (31), #125 Aruanã (29), #169 Trinca-Ferro (29), #173 Choca (31), #189 Açaí (27), #214 Marmim (27), #242 Anhangá (29), #249 Jenipapo (27-29), #266 Caboclo-Guerreiro (29)
- **pedra** (taxa 25): #169 Trinca-Ferro (15-20), #213 Vulcanite (20-25), #214 Marmim (5-15), #295 Muiraquitã (25-30)

### SAFARI_ZONE_NORTHEAST

- **grama** (taxa 25): #159 Urutau (33-35), #169 Trinca-Ferro (33), #189 Açaí (36), #211 Fóssil (39), #214 Marmim (34), #215 Granito (40), #242 Anhangá (37), #249 Jenipapo (34)
- **pedra** (taxa 25): #169 Trinca-Ferro (30-35), #211 Fóssil (30-35), #214 Marmim (20-30), #215 Granito (35-40)

### SAFARI_ZONE_NORTHWEST

- **grama** (taxa 25): #125 Aruanã (27-29), #131 Pacu (27), #144 Caramulão (29), #150 Vespão (29), #179 Bromelinha (29), #181 Vitóriarégia (29), #192 Guaraná (31), #253 Yara-Pindá (27), #294 Uirapuru (31)
- **surfe** (taxa 9): #125 Aruanã (30-35), #144 Caramulão (20-30), #181 Vitóriarégia (30-35), #286 Iara-Mãe (25-40)
- **pesca** (taxa 35): #057 Mãe-d'Água (10-25), #124 Tambaqui (25-30), #125 Aruanã (5-30), #130 Tucunaré (35-40), #131 Pacu (5-30), #144 Caramulão (25-35), #181 Vitóriarégia (30-35)

### SAFARI_ZONE_SOUTH

- **grama** (taxa 25): #020 Sacizinho (25), #115 Ovelhinha (27), #153 Corupião (27), #155 Formigão-Preto (27), #165 Jaburu (25-27), #166 Ema (25), #167 Seriema (29), #186 Buriti (25), #193 Mate (27), #194 Milho (25)

### SAFARI_ZONE_SOUTHEAST

- **grama** (taxa 25): #001 Caramelo (34), #007 Pimpau (33), #011 Saúvarco (34), #024 Tamanduá (36), #054 Guaraflama (34), #153 Corupião (37), #175 João-de-Barro (39), #195 Mandioca (33), #277 Congada (40), #362 Beija-Luz (35)
- **surfe** (taxa 9): #004 Querô (25-30), #086 Sapão (30-35), #126 Poraquê (35-40), #186 Buriti (25-30), #193 Mate (25-30)
- **pesca** (taxa 35): #057 Mãe-d'Água (25-30), #086 Sapão (25-35), #125 Aruanã (35-40), #126 Poraquê (25-30), #131 Pacu (30-35), #186 Buriti (25-30), #193 Mate (25-35)

### SAFARI_ZONE_SOUTHWEST

- **grama** (taxa 25): #057 Mãe-d'Água (27), #084 Curicaca (27), #096 Colhereiro (25), #125 Aruanã (25-27), #131 Pacu (25-27), #144 Caramulão (27), #165 Jaburu (25), #179 Bromelinha (29), #292 Mapinguari (27)
- **surfe** (taxa 9): #144 Caramulão (30-35), #165 Jaburu (20-30), #181 Vitóriarégia (30-35), #283 Terolibra-Rainha (30-35)
- **pesca** (taxa 35): #124 Tambaqui (25-30), #125 Aruanã (5-30), #130 Tucunaré (35-40), #131 Pacu (5-30), #144 Caramulão (25-35), #165 Jaburu (10-25), #181 Vitóriarégia (30-35)

### SEAFLOOR_CAVERN_ENTRANCE

- **surfe** (taxa 4): #123 Piranha (5-35), #267 Marinheiro (30-35), #280 Sucuriaçu (30-35), #318 Garrafão (30-35)
- **pesca** (taxa 10): #127 Curimbatá (20-30), #128 Traíra (10-30), #131 Pacu (35-40), #134 Cascudo (5-30), #231 Peixe-Espada (30-35), #233 Pescadão (5-30), #281 Pirarumbá (40-45)

### SEAFLOOR_CAVERN_ROOM1

- **grama** (taxa 4): #123 Piranha (30-32), #128 Traíra (29), #130 Tucunaré (35), #134 Cascudo (28-31), #233 Pescadão (33-34), #243 Jurupari (33), #267 Marinheiro (36), #304 Cão-Bravo (34), #309 Poeirão (35)

### SEAFLOOR_CAVERN_ROOM2

- **grama** (taxa 4): #123 Piranha (30-32), #128 Traíra (29), #130 Tucunaré (35), #134 Cascudo (28-31), #205 Salitre (35), #233 Pescadão (33-34), #240 Perna-Cabeluda (34), #267 Marinheiro (36), #289 Anhangaú (33)

### SEAFLOOR_CAVERN_ROOM3

- **grama** (taxa 4): #023 Onçaléu (33), #123 Piranha (30-32), #128 Traíra (29), #130 Tucunaré (35), #134 Cascudo (28-31), #205 Salitre (35), #233 Pescadão (33-34), #254 Pisadeira (34), #267 Marinheiro (36)

### SEAFLOOR_CAVERN_ROOM4

- **grama** (taxa 4): #123 Piranha (30-32), #128 Traíra (29), #130 Tucunaré (35), #134 Cascudo (28-31), #205 Salitre (35), #233 Pescadão (33-34), #267 Marinheiro (36), #276 Maracatu (34), #373 Rendeira (33)

### SEAFLOOR_CAVERN_ROOM5

- **grama** (taxa 4): #123 Piranha (30-32), #127 Curimbatá (33), #128 Traíra (29), #130 Tucunaré (35), #134 Cascudo (28-31), #233 Pescadão (33-34), #239 Mão-Peluda (34), #267 Marinheiro (36), #328 Grafiteiro (35)

### SEAFLOOR_CAVERN_ROOM6

- **grama** (taxa 4): #123 Piranha (30-32), #127 Curimbatá (33), #128 Traíra (29), #130 Tucunaré (35), #134 Cascudo (28-31), #146 Barata (35), #233 Pescadão (33-34), #247 Rudá (34), #267 Marinheiro (36)
- **surfe** (taxa 4): #123 Piranha (5-35), #205 Salitre (30-35), #267 Marinheiro (30-35), #291 Cobra-Norato (30-35)
- **pesca** (taxa 10): #127 Curimbatá (20-30), #130 Tucunaré (10-30), #131 Pacu (35-40), #134 Cascudo (5-30), #231 Peixe-Espada (30-35), #233 Pescadão (5-30), #374 Escamoso (40-45)

### SEAFLOOR_CAVERN_ROOM7

- **grama** (taxa 4): #123 Piranha (30-32), #127 Curimbatá (33), #128 Traíra (29), #130 Tucunaré (35), #134 Cascudo (28-31), #233 Pescadão (33-34), #234 Loirinha (35), #267 Marinheiro (36), #305 Gato-Preto (34)
- **surfe** (taxa 4): #109 Oxum (30-35), #123 Piranha (5-35), #205 Salitre (30-35), #267 Marinheiro (30-35)
- **pesca** (taxa 10): #126 Poraquê (10-30), #127 Curimbatá (30-35), #130 Tucunaré (20-30), #131 Pacu (40-45), #133 Piau (10-30), #134 Cascudo (5-30), #231 Peixe-Espada (35-40), #233 Pescadão (5-10)

### SEAFLOOR_CAVERN_ROOM8

- **grama** (taxa 4): #090 Camaleão (34), #123 Piranha (30-32), #127 Curimbatá (33), #128 Traíra (29), #130 Tucunaré (35), #134 Cascudo (28-31), #233 Pescadão (33-34), #267 Marinheiro (36), #322 Bugão (35)

### SHOAL_CAVE_LOW_TIDE_ENTRANCE_ROOM

- **grama** (taxa 10): #205 Salitre (30), #209 Estalactite (28-32), #218 Siri (32), #222 Águaviva (32), #231 Peixe-Espada (30), #233 Pescadão (26-28), #267 Marinheiro (26), #268 Baiano (32), #312 Óleoso (32), #319 Netzero (32)
- **surfe** (taxa 4): #205 Salitre (5-35), #219 Camarão (25-30), #222 Águaviva (25-30), #232 Pargo (5-35), #233 Pescadão (25-35)
- **pesca** (taxa 10): #205 Salitre (5-30), #218 Siri (35-40), #227 Baleia (20-30), #231 Peixe-Espada (10-30), #233 Pescadão (10-30), #267 Marinheiro (5-10), #293 Ipupiara (40-45), #312 Óleoso (30-35)

### SHOAL_CAVE_LOW_TIDE_ICE_ROOM

- **grama** (taxa 10): #205 Salitre (26-28), #209 Estalactite (32), #222 Águaviva (30), #231 Peixe-Espada (30), #233 Pescadão (26-30), #267 Marinheiro (28-30), #303 Mosquim (26), #312 Óleoso (28), #367 Atabaque (32)

### SHOAL_CAVE_LOW_TIDE_INNER_ROOM

- **grama** (taxa 10): #205 Salitre (26-28), #209 Estalactite (30), #218 Siri (32), #227 Baleia (32), #233 Pescadão (26-30), #267 Marinheiro (28-32), #311 Fumacento (32), #312 Óleoso (32), #323 Aluminio (32)
- **surfe** (taxa 4): #205 Salitre (5-35), #230 Arraia (25-30), #231 Peixe-Espada (25-35), #267 Marinheiro (5-35), #364 Sarará (25-30)
- **pesca** (taxa 10): #108 Iemanjá (40-45), #209 Estalactite (30-35), #218 Siri (10-30), #227 Baleia (35-40), #231 Peixe-Espada (5-30), #233 Pescadão (5-30), #267 Marinheiro (20-30)

### SHOAL_CAVE_LOW_TIDE_LOWER_ROOM

- **grama** (taxa 10): #205 Salitre (26-28), #209 Estalactite (30), #218 Siri (32), #222 Águaviva (32), #227 Baleia (32), #233 Pescadão (26-30), #264 Exu (32), #267 Marinheiro (28-32), #312 Óleoso (32)

### SHOAL_CAVE_LOW_TIDE_STAIRS_ROOM

- **grama** (taxa 10): #205 Salitre (26-28), #209 Estalactite (30), #218 Siri (32), #222 Águaviva (32), #227 Baleia (32), #233 Pescadão (26-30), #267 Marinheiro (28-32), #275 Frevinho (32), #312 Óleoso (32)

### SKY_PILLAR_1F

- **grama** (taxa 10): #016 Boitatá (37), #199 Ametista (34-37), #200 Ouríço (38), #211 Fóssil (33-38), #214 Marmim (34-36), #215 Granito (36), #258 Oxalá (37), #298 Cristo (38)

### SKY_PILLAR_3F

- **grama** (taxa 10): #016 Boitatá (37), #199 Ametista (34-37), #200 Ouríço (38), #211 Fóssil (33-38), #214 Marmim (34-36), #215 Granito (36), #244 Tupã (37), #245 Jaci (38)

### SKY_PILLAR_5F

- **grama** (taxa 10): #016 Boitatá (37), #199 Ametista (34-37), #200 Ouríço (38), #211 Fóssil (33-38), #212 Meteorito (39), #214 Marmim (34-36), #215 Granito (36), #260 Sacipererê (39)

### SLATEPORT_CITY

- **surfe** (taxa 4): #012 Capivim (15-25), #085 Sapim (25-30), #220 Polvim (5-35), #375 Piranhita (25-30)
- **pesca** (taxa 10): #012 Capivim (5-30), #055 Peixim (20-30), #058 Mandim (10-30), #085 Sapim (40-45), #104 Cabocim (10-30), #220 Polvim (30-35), #228 Tubarim (5-10), #375 Piranhita (35-40)

### SOOTOPOLIS_CITY

- **surfe** (taxa 1): #123 Piranha (15-25), #130 Tucunaré (25-30), #209 Estalactite (5-35), #375 Piranhita (25-30)
- **pesca** (taxa 10): #125 Aruanã (35-45), #127 Curimbatá (5-30), #129 Dourado (10-30), #130 Tucunaré (5-10), #131 Pacu (5-45), #132 Matrinxã (10-30), #134 Cascudo (30-40), #165 Jaburu (30-35)

### UNDERWATER_ROUTE124

- **surfe** (taxa 4): #123 Piranha (30-35), #205 Salitre (20-30), #209 Estalactite (30-35), #267 Marinheiro (30-35)

### UNDERWATER_ROUTE126

- **surfe** (taxa 4): #123 Piranha (30-35), #205 Salitre (20-30), #209 Estalactite (30-35), #267 Marinheiro (30-35)

### VICTORY_ROAD_1F

- **grama** (taxa 10): #016 Boitatá (38-40), #078 Coati (36), #197 Rochão (36), #200 Ouríço (36), #211 Fóssil (36-40), #213 Vulcanite (36), #214 Marmim (38), #215 Granito (36-40)

### VICTORY_ROAD_B1F

- **grama** (taxa 10): #016 Boitatá (40-42), #078 Coati (38), #197 Rochão (38), #200 Ouríço (38), #211 Fóssil (38-40), #213 Vulcanite (42), #214 Marmim (42), #215 Granito (40-42)
- **pedra** (taxa 20): #197 Rochão (35-40), #211 Fóssil (30-40), #214 Marmim (35-40), #215 Granito (35-40)

### VICTORY_ROAD_B2F

- **grama** (taxa 10): #016 Boitatá (40-44), #078 Coati (44), #197 Rochão (42), #200 Ouríço (42), #211 Fóssil (40-42), #213 Vulcanite (44), #214 Marmim (44), #215 Granito (40-42)
- **surfe** (taxa 4): #122 Pirarucu (35-40), #130 Tucunaré (35-40), #181 Vitóriarégia (35-40), #209 Estalactite (25-35)
- **pesca** (taxa 30): #057 Mãe-d'Água (30-35), #122 Pirarucu (10-30), #125 Aruanã (40-45), #126 Poraquê (25-35), #130 Tucunaré (5-30), #131 Pacu (35-40), #209 Estalactite (5-30)


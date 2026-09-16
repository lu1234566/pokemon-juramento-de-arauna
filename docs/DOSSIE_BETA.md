# Pokemon Juramento de Arauana — dossie da beta

Gerado por `tools/arauna/build_beta_dossier.py` a partir do proprio
repositorio. Nenhum numero aqui foi digitado a mao.

## A historia

O canone abaixo nao e resumo escrito para o dossie: sao os pontos que
`docs/ARAUANA_STORY_IMPLEMENTATION.md` declara e que o texto do jogo
implementa, em 647 blocos de dialogo e 103 arquivos de script.

| | |
|---|---|
| **Core theme** | memory, grief, erasure and consent. |
| **Phenomenon** | Desencanto. |
| **Technology** | Arquivo Vivo. |
| **Corporate force** | Consorcio Horizonte, led by Dr. Otacilio Meira. |
| **Radical opposition** | Lembrantes, led by Luzia Ferraz. |
| **Mentor** | Professora Anahi, who helped create the first Vinculo sensors. |
| **Oral-memory keeper** | Dona Zila. |
| **Rival** | Ciro, initially sponsored by Horizonte. |
| **Father** | Elias, connected to the approvals behind the M'Boi disaster. |
| **Final thesis** | nobody has the right to decide for someone else what deserves to be remembered. |

A regra da adaptacao esta escrita no mesmo documento e vale para tudo
que segue: **nenhuma ordem de rota, ordem de insignia, warp, flag de
progressao ou gatilho de evento do Emerald foi mudada.** O que mudou foi
a superficie -- quem fala, o que diz, e o que o mundo se chama.

## Os nomes do mundo

43 lugares do mapa da regiao. Nome fica em portugues, prosa vai para o
ingles -- e a regra que `docs/GLOSSARIO_EN.md` fixa.

| Hoenn | Arauana |
|---|---|
| ABANDONED SHIP | **NAVIO PERDIDO** |
| ANCIENT TOMB | **TUMBA ANTIGA** |
| ARTISAN CAVE | **GRUTA DO OFICIO** |
| CAVE OF ORIGIN | **GRUTA DA ORIGEM** |
| DESERT RUINS | **RUINAS DA AREIA** |
| DESERT UNDERPASS | **PASSAGEM SECA** |
| DEWFORD | **PORTO DAS REDES** |
| EVER GRANDE | **ESTR. JURAMENTO** |
| FALLARBOR | **CAMPO DAS CINZAS** |
| FIERY PATH | **TRILHA DE BRASA** |
| FORTREE | **MATA DO MEIO** |
| GRANITE CAVE | **GRUTA DAS VOZES** |
| ISLAND CAVE | **GRUTA DA ILHA** |
| JAGGED PASS | **PASSO CORTADO** |
| LAVARIDGE | **SERTAO DE DENTRO** |
| LILYCOVE | **BAIA DAS LUZES** |
| LITTLEROOT | **VILA AMANHECER** |
| MARINE CAVE | **GRUTA DAS MARES** |
| MAUVILLE | **ENCRUZILHADA** |
| METEOR FALLS | **RUINAS DA QUEDA** |
| MIRAGE ISLAND | **ILHA MIRAGEM** |
| MIRAGE TOWER | **TORRE MIRAGEM** |
| MOSSDEEP | **MISSOES DO CEU** |
| MT. CHIMNEY | **SERRA DA CINZA** |
| MT. PYRE | **MEMORIAL DOS NOMES** |
| NEW MAUVILLE | **USINA VELHA** |
| OLDALE | **VILA DA PASSAGEM** |
| PACIFIDLOG | **CASA DA FOGUEIRA** |
| PETALBURG | **PAMPA DA ESPERA** |
| PETALBURG WOODS | **MATA DA ESPERA** |
| RUSTBORO | **SERRA DO UIVO** |
| RUSTURF TUNNEL | **GALERIAS SERRA** |
| SAFARI ZONE | **RESERVA ARAUNA** |
| SCORCHED SLAB | **LAJE QUEIMADA** |
| SEAFLOOR CAVERN | **CAVERNAS M'BOI** |
| SEALED CHAMBER | **CAMARA SELADA** |
| SHOAL CAVE | **GRUTA DA MARE** |
| SKY PILLAR | **TORRE JURAMENTO** |
| SLATEPORT | **PORTO DO SAL** |
| SOOTOPOLIS | **AGUAS DE M'BOI** |
| SOUTHERN ISLAND | **ILHA DO SUL** |
| TERRA CAVE | **GRUTA DA TERRA** |
| VERDANTURF | **VALE DO SILENCIO** |

## O jogo em numeros

| | |
|---|---:|
| criaturas na dex | 386 |
| capturaveis na natureza | 293 |
| mapas com encontro | 116 |
| learnsets proprios | 412 |
| golpes ensinados por nivel | 5260 |
| relacoes evolutivas | 81 |
| habilidades novas | 35 |
| golpes exclusivos | 27 |
| treinadores no jogo | 855 |

## O caminho do jogo

Oito insignias, quatro da Elite e a Campea. O teto de nivel sobe com a
insignia, e e o mesmo numero que `sLevelCapByBadges` usa em
`src/arauna_qol.c`.

| ordem | casa | chefe | tipo | teto |
|---:|---|---|---|---:|
| 1 | Serra do Uivo | **Dalva** | Rock | 15 |
| 2 | Casa da Mare | **Ademar** | Fighting | 19 |
| 3 | Encruzilhada | **Olivia** | Electric | 24 |
| 4 | Casa da Cinza | **Nara** | Fire | 29 |
| 5 | Pampa da Espera | **Elias** | Normal | 31 |
| 6 | Mata do Meio | **Lidia** | Flying | 33 |
| 7 | Missoes do Ceu | **Cec&Caet** | Psychic | 42 |
| 8 | Aguas M'Boi | **Celina** | Water | 46 |
| 9 | Elite dos Quatro | **Lazaro** | Dark | 49 |
| 10 | Elite dos Quatro | **Rosa** | Ghost | 51 |
| 11 | Elite dos Quatro | **Clara** | Steel | 53 |
| 12 | Elite dos Quatro | **Tiburcio** | Dragon | 55 |
| 13 | Campea | **Amalia** | Campea | 58 |

## Os times dos chefes

### 1. Dalva — Rock, Serra do Uivo (teto Nv. 15)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #196 Pedrinha | Rock | 284 | Nv. 13 | 10/31 | Shell Bell | Defense Curl · Rollout (30) · Sandstorm · Tackle (35) |
| #134 Cascudo | Water/Rock | 448 | Nv. 14 | 15/31 | Kings Rock | Surf (95) · Tackle (35) · Withdraw · Rollout (30) |
| #198 Cristalim | Rock/Fairy | 282 | Nv. 14 | 18/31 | Sitrus Berry | Confusion (50) · Ancient Power (60) · Rock Slide (75) · Charm |
| #211 Fóssil | Rock/Dragon | 448 | Nv. 14 | 20/31 | Sitrus Berry | Dragon Rage (1) · Harden · Ancient Power (60) · Dragon Dance |
| #215 Granito | Rock/Fighting | 445 | Nv. 15 | 31/31 | Sitrus Berry | Karate Chop (50) · Ancient Power (60) · Mach Punch (40) · Tackle (35) |

### 2. Ademar — Fighting, Casa da Mare (teto Nv. 19)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #062 Prego | Fighting/Normal | 404 | Nv. 17 | 12/31 | Sitrus Berry | Double Edge (120) · Cross Chop (100) · Headbutt (70) · Focus Energy |
| #105 Caboclo | Water/Fighting | 551 | Nv. 17 | 13/31 | Sitrus Berry | Rain Dance · Surf (95) · Mach Punch (40) · Karate Chop (50) |
| #161 Gavião | Flying/Fighting | 447 | Nv. 17 | 14/31 | Black Belt | Brick Break (75) · Mach Punch (40) · Wing Attack (60) · Whirlwind |
| #239 Mão-Peluda | Ghost/Fighting | 449 | Nv. 17 | 16/31 | Sitrus Berry | Confuse Ray · Sing · Low Kick (1) · Mach Punch (40) |
| #255 Zumbi | Ghost/Fighting | 606 | Nv. 19 | 31/31 | Rawst Berry | Destiny Bond · Shadow Ball (80) · Mach Punch (40) · Sky Uppercut (85) |

### 3. Olivia — Electric, Encruzilhada (teto Nv. 24)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #200 Ouríço | Steel/Electric | 448 | Nv. 22 | 10/31 | Sitrus Berry | Steel Wing (70) · Agility · Thunderbolt (95) · Thunder Wave |
| #321 Cabofio | Electric/Steel | 448 | Nv. 23 | 12/31 | Sitrus Berry | Metal Claw (50) · Shock Wave (60) · Water Pulse (60) · Iron Defense |
| #230 Arraia | Water/Electric | 448 | Nv. 24 | 13/31 | Sitrus Berry | Faint Attack (60) · Spark (65) · Water Pulse (60) · Withdraw |
| #137 Vagalume | Bug/Electric | 555 | Nv. 24 | 17/31 | Sitrus Berry | Shock Wave (60) · Signal Beam (75) · Thunder Wave · Agility |
| #244 Tupã | Electric/Dragon | 606 | Nv. 24 | 31/31 | Scope Lens | Spark (65) · Dragon Breath (60) · Scary Face · Thunderbolt (95) |

### 4. Nara — Fire, Casa da Cinza (teto Nv. 29)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #232 Pargo | Water/Fire | 446 | Nv. 24 | 24/31 | None | Overheat (140) · Take Down (90) · Magnitude (1) · Sunny Day |
| #052 Guaracim | Fire | 287 | Nv. 24 | 24/31 | None | Overheat (140) · Smog (20) · Light Screen · Sunny Day |
| #206 Enxofrino | Fire/Poison | 449 | Nv. 26 | 30/31 | None | Overheat (140) · Tackle (35) · Sunny Day · Attract |
| #016 Boitatá | Fire/Ghost | 514 | Nv. 29 | 30/31 | White Herb | Overheat (140) · Sunny Day · Body Slam (85) · Attract |

### 5. Elias — Normal, Pampa da Espera (teto Nv. 31)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #084 Curicaca | Flying/Normal | 447 | Nv. 27 | 24/31 | None | Teeter Dance · Psybeam (65) · Facade (70) · Encore |
| #115 Ovelhinha | Normal/Fairy | 449 | Nv. 27 | 24/31 | None | Slash (70) · Facade (70) · Encore · Faint Attack (60) |
| #103 Suçuapara | Normal/Fighting | 447 | Nv. 29 | 24/31 | None | Slash (70) · Belly Drum · Facade (70) · Headbutt (70) |
| #071 Cutia | Normal | 555 | Nv. 31 | 30/31 | Sitrus Berry | Counter (1) · Yawn · Facade (70) · Faint Attack (60) |

### 6. Lidia — Flying, Mata do Meio (teto Nv. 33)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #157 Sabiá | Flying/Normal | 445 | Nv. 29 | 25/31 | None | Perish Song · Mirror Move · Safeguard · Aerial Ace (60) |
| #033 Araracanga | Flying/Fire | 550 | Nv. 29 | 25/31 | None | Sunny Day · Aerial Ace (60) · Solar Beam (120) · Synthesis |
| #156 Beija-flor | Flying/Fairy | 448 | Nv. 30 | 25/31 | None | Water Gun (40) · Supersonic · Protect · Aerial Ace (60) |
| #020 Sacizinho | Dark/Flying | 461 | Nv. 31 | 26/31 | None | Sand Attack · Fury Attack (15) · Steel Wing (70) · Aerial Ace (60) |
| #083 Aracari | Flying/Grass | 551 | Nv. 33 | 31/31 | Oran Berry | Earthquake (100) · Dragon Breath (60) · Dragon Dance · Aerial Ace (60) |

### 7. Cec&Caet — Psychic, Missoes do Ceu (teto Nv. 42)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #265 Preto-Velho | Ghost/Psychic | 604 | Nv. 41 | 30/31 | None | Earthquake (100) · Ancient Power (60) · Psychic (90) · Light Screen |
| #039 Bicho-Preguiça | Grass/Psychic | 551 | Nv. 41 | 30/31 | None | Psychic (90) · Sunny Day · Confuse Ray · Calm Mind |
| #247 Rudá | Fairy/Psychic | 449 | Nv. 42 | 30/31 | Sitrus Berry | Light Screen · Psychic (90) · Hypnosis · Calm Mind |
| #305 Gato-Preto | Dark/Psychic | 449 | Nv. 42 | 30/31 | Sitrus Berry | Sunny Day · Solar Beam (120) · Psychic (90) · Flamethrower (95) |

### 8. Celina — Water, Aguas M'Boi (teto Nv. 46)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #124 Tambaqui | Water/Normal | 445 | Nv. 41 | 24/31 | None | Water Pulse (60) · Attract · Sweet Kiss · Flail (1) |
| #364 Sarará | Fairy/Water | 472 | Nv. 41 | 24/31 | None | Rain Dance · Water Pulse (60) · Amnesia · Earthquake (100) |
| #132 Matrinxã | Water/Normal | 444 | Nv. 43 | 24/31 | None | Encore · Body Slam (85) · Aurora Beam (65) · Water Pulse (60) |
| #047 Sucuri | Water/Poison | 480 | Nv. 43 | 24/31 | None | Water Pulse (60) · Crabhammer (90) · Taunt · Leer |
| #280 Sucuriaçu | Water/Dragon | 607 | Nv. 46 | 30/31 | Chesto Berry | Water Pulse (60) · Double Team · Ice Beam (95) · Rest |

### Lazaro — Dark (teto Nv. 49)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #123 Piranha | Water/Dark | 448 | Nv. 46 | 30/31 | None | Roar · Double Edge (120) · Sand Attack · Crunch (80) |
| #068 Gato-do-mato | Normal/Dark | 554 | Nv. 48 | 30/31 | None | Torment · Double Team · Swagger · Extrasensory (80) |
| #023 Onçaléu | Dark | 524 | Nv. 46 | 30/31 | None | Leech Seed · Faint Attack (60) · Needle Arm (60) · Cotton Spore |
| #374 Escamoso | Water/Dark | 498 | Nv. 48 | 30/31 | None | Surf (95) · Swords Dance · Strength (80) · Facade (70) |
| #077 Quati | Normal/Dark | 550 | Nv. 49 | 31/31 | Sitrus Berry | Aerial Ace (60) · Rock Slide (75) · Swords Dance · Slash (70) |

### Rosa — Ghost (teto Nv. 51)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #236 Bicho-Papão | Dark/Ghost | 449 | Nv. 48 | 30/31 | None | Shadow Punch (60) · Confuse Ray · Curse · Protect |
| #239 Mão-Peluda | Ghost/Fighting | 449 | Nv. 49 | 30/31 | None | Shadow Ball (80) · Grudge · Will O Wisp · Faint Attack (60) |
| #240 Perna-Cabeluda | Ghost/Normal | 446 | Nv. 50 | 30/31 | None | Shadow Ball (80) · Double Team · Night Shade (1) · Faint Attack (60) |
| #054 Guaraflama | Fire/Ghost | 448 | Nv. 49 | 30/31 | None | Shadow Ball (80) · Psychic (90) · Thunderbolt (95) · Facade (70) |
| #241 Comadre | Ghost/Fairy | 448 | Nv. 51 | 31/31 | Sitrus Berry | Shadow Ball (80) · Ice Beam (95) · Rock Slide (75) · Earthquake (100) |

### Clara — Steel (teto Nv. 53)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #231 Peixe-Espada | Water/Steel | 444 | Nv. 50 | 30/31 | None | Encore · Body Slam (85) · Hail · Ice Ball (30) |
| #030 Tatuçu | Ground/Steel | 555 | Nv. 50 | 30/31 | None | Light Screen · Crunch (80) · Icy Wind (55) · Ice Beam (95) |
| #201 Ferrolho | Steel/Ground | 445 | Nv. 52 | 30/31 | None | Attract · Double Edge (120) · Hail · Blizzard (120) |
| #110 Ogum | Steel/Fire | 602 | Nv. 52 | 30/31 | None | Shadow Ball (80) · Explosion (250) · Hail · Ice Beam (95) |
| #024 Tamanduá | Ground/Steel | 470 | Nv. 53 | 31/31 | Sitrus Berry | Surf (95) · Body Slam (85) · Ice Beam (95) · Sheer Cold (1) |

### Tiburcio — Dragon (teto Nv. 55)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #211 Fóssil | Rock/Dragon | 448 | Nv. 52 | 30/31 | None | Rock Tomb (50) · Dragon Claw (80) · Protect · Double Edge (120) |
| #036 Jacarodon | Water/Dragon | 551 | Nv. 54 | 30/31 | None | Double Edge (120) · Dragon Breath (60) · Dragon Dance · Aerial Ace (60) |
| #280 Sucuriaçu | Water/Dragon | 607 | Nv. 53 | 30/31 | None | Smokescreen · Dragon Dance · Surf (95) · Body Slam (85) |
| #122 Pirarucu | Water/Dragon | 552 | Nv. 53 | 30/31 | None | Flamethrower (95) · Crunch (80) · Dragon Breath (60) · Earthquake (100) |
| #348 Arauanamon | Dragon/Fairy | 650 | Nv. 55 | 31/31 | Sitrus Berry | Flamethrower (95) · Dragon Claw (80) · Rock Slide (75) · Crunch (80) |

### Amalia — Campea (teto Nv. 58)

| criatura | tipos | BST | nivel | IV | item | golpes |
|---|---|---:|---:|---:|---|---|
| #286 Iara-Mãe | Water/Fairy | 602 | Nv. 57 | 31/31 | None | Rain Dance · Water Spout (150) · Double Edge (120) · Blizzard (120) |
| #280 Sucuriaçu | Water/Dragon | 607 | Nv. 55 | 31/31 | None | Toxic · Hydro Pump (120) · Sludge Bomb (90) · Ice Beam (95) |
| #048 Boiuna | Water/Dragon | 600 | Nv. 56 | 31/31 | None | Giga Drain (60) · Surf (95) · Leech Seed · Double Team |
| #364 Sarará | Fairy/Water | 472 | Nv. 56 | 31/31 | None | Earthquake (100) · Surf (95) · Amnesia · Hyper Beam (150) |
| #027 Botogaláu | Water/Psychic | 555 | Nv. 56 | 31/31 | None | Dragon Dance · Earthquake (100) · Hyper Beam (150) · Surf (95) |
| #109 Oxum | Water/Fairy | 606 | Nv. 58 | 31/31 | Sitrus Berry | Recover · Surf (95) · Ice Beam (95) · Toxic |

## Como os mapas se ligam

64 mapas de superficie tem vizinho. E o grafo do Emerald, intacto: e
por ele que se anda de uma casa a outra.

| mapa | vizinhos |
|---|---|
| PetalburgCity | left: ROUTE104, right: ROUTE102 |
| SlateportCity | up: ROUTE110, down: ROUTE109, right: ROUTE134 |
| MauvilleCity | up: ROUTE111, down: ROUTE110, left: ROUTE117, right: ROUTE118 |
| RustboroCity | up: ROUTE115, down: ROUTE104, right: ROUTE116 |
| FortreeCity | left: ROUTE119, right: ROUTE120 |
| LilycoveCity | left: ROUTE121, right: ROUTE124 |
| MossdeepCity | up: ROUTE125, down: ROUTE127, left: ROUTE124 |
| EverGrandeCity | left: ROUTE128 |
| LittlerootTown | up: ROUTE101 |
| OldaleTown | up: ROUTE103, down: ROUTE101, left: ROUTE102 |
| DewfordTown | up: ROUTE106, right: ROUTE107 |
| LavaridgeTown | right: ROUTE112 |
| FallarborTown | left: ROUTE114, right: ROUTE113 |
| VerdanturfTown | up: ROUTE116, right: ROUTE117 |
| PacifidlogTown | left: ROUTE132, right: ROUTE131 |
| Route101 | up: OLDALE_TOWN, down: LITTLEROOT_TOWN |
| Route102 | left: PETALBURG_CITY, right: OLDALE_TOWN |
| Route103 | down: OLDALE_TOWN, right: ROUTE110 |
| Route104 | up: RUSTBORO_CITY, down: ROUTE105, right: PETALBURG_CITY |
| Route105 | up: ROUTE104, down: ROUTE106, dive: UNDERWATER_ROUTE105 |
| Route106 | up: ROUTE105, down: DEWFORD_TOWN |
| Route107 | left: DEWFORD_TOWN, right: ROUTE108 |
| Route108 | left: ROUTE107, right: ROUTE109 |
| Route109 | up: SLATEPORT_CITY, left: ROUTE108 |
| Route110 | up: MAUVILLE_CITY, down: SLATEPORT_CITY, left: ROUTE103 |
| Route111 | down: MAUVILLE_CITY, left: ROUTE113, left: ROUTE112 |
| Route112 | up: ROUTE113, left: LAVARIDGE_TOWN, right: ROUTE111 |
| Route113 | down: ROUTE112, left: FALLARBOR_TOWN, right: ROUTE111 |
| Route114 | left: ROUTE115, right: FALLARBOR_TOWN |
| Route115 | down: RUSTBORO_CITY, right: ROUTE114 |
| Route116 | down: VERDANTURF_TOWN, left: RUSTBORO_CITY |
| Route117 | left: VERDANTURF_TOWN, right: MAUVILLE_CITY |
| Route118 | up: ROUTE119, left: MAUVILLE_CITY, right: ROUTE123 |
| Route119 | down: ROUTE118, right: FORTREE_CITY |
| Route120 | left: FORTREE_CITY, right: ROUTE121 |
| Route121 | down: ROUTE122, left: ROUTE120, right: LILYCOVE_CITY |
| Route122 | up: ROUTE121, down: ROUTE123 |
| Route123 | up: ROUTE122, left: ROUTE118 |
| Route124 | down: ROUTE126, left: LILYCOVE_CITY, right: ROUTE125, right: MOSSDEEP_CITY, dive: UNDERWATER_ROUTE124 |
| Route125 | down: MOSSDEEP_CITY, left: ROUTE124, dive: UNDERWATER_ROUTE125 |
| Route126 | up: ROUTE124, right: ROUTE127, dive: UNDERWATER_ROUTE126 |
| Route127 | up: MOSSDEEP_CITY, down: ROUTE128, left: ROUTE126, dive: UNDERWATER_ROUTE127 |
| Route128 | up: ROUTE127, down: ROUTE129, right: EVER_GRANDE_CITY, dive: UNDERWATER_ROUTE128 |
| Route129 | up: ROUTE128, left: ROUTE130, dive: UNDERWATER_ROUTE129 |
| Route130 | left: ROUTE131, right: ROUTE129 |
| Route131 | left: PACIFIDLOG_TOWN, right: ROUTE130 |
| Route132 | left: ROUTE133, right: PACIFIDLOG_TOWN |
| Route133 | left: ROUTE134, right: ROUTE132 |
| Route134 | left: SLATEPORT_CITY, right: ROUTE133 |
| Underwater_Route124 | down: UNDERWATER_ROUTE126, emerge: ROUTE124 |
| Underwater_Route126 | up: UNDERWATER_ROUTE124, right: UNDERWATER_ROUTE127, emerge: ROUTE126 |
| Underwater_Route127 | emerge: ROUTE127, left: UNDERWATER_ROUTE126, down: UNDERWATER_ROUTE128 |
| Underwater_Route128 | up: UNDERWATER_ROUTE127, emerge: ROUTE128 |
| Underwater_Route129 | emerge: ROUTE129 |
| Underwater_Route105 | emerge: ROUTE105 |
| Underwater_Route125 | emerge: ROUTE125 |
| SafariZone_Northwest | right: SAFARI_ZONE_NORTH, down: SAFARI_ZONE_SOUTHWEST |
| SafariZone_North | left: SAFARI_ZONE_NORTHWEST, down: SAFARI_ZONE_SOUTH, right: SAFARI_ZONE_NORTHEAST |
| SafariZone_Southwest | up: SAFARI_ZONE_NORTHWEST, right: SAFARI_ZONE_SOUTH |
| SafariZone_South | up: SAFARI_ZONE_NORTH, left: SAFARI_ZONE_SOUTHWEST, right: SAFARI_ZONE_SOUTHEAST |
| BattleFrontier_OutsideWest | right: BATTLE_FRONTIER_OUTSIDE_EAST |
| SafariZone_Northeast | left: SAFARI_ZONE_NORTH, down: SAFARI_ZONE_SOUTHEAST |
| SafariZone_Southeast | left: SAFARI_ZONE_SOUTH, up: SAFARI_ZONE_NORTHEAST |
| BattleFrontier_OutsideEast | left: BATTLE_FRONTIER_OUTSIDE_WEST |

## As 35 habilidades novas

Fogo Leal · Vigia Alado · Bico Granito · Cobra Grande · Coroa Solar · Veu Lunar · Voz De Tupa · Canto Rio · Sol Primeiro · Lua Primeva · Laco Eterno · Mil Rios · Guardiao · Mata Renova · Tempestade · Seca Brava · Vento Sul · Solo Vivo · Fogo Antigo · Mare Mestra · Primeira Luz · Ultima Luz · Desejo Vivo · Juramento · Fogo Vigia · Rei Do Rio · Casco Antigo · Sol Absoluto · Noite Eterna · Resistencia · Mar Sagrado · Arco Vivo · Pe Inverso · Redemoinho · Essencia

## Os 27 golpes exclusivos

| golpe | tipo | poder |
|---|---|---:|
| Fairy Wind | Fairy | 40 |
| Disarming Voice | Fairy | 40 |
| Draining Kiss | Fairy | 50 |
| Dazzling Gleam | Fairy | 80 |
| Moonblast | Fairy | 95 |
| Luar De Jaci | Fairy | 100 |
| Juramento De Arauana | Fairy | 105 |
| Eclipse Divino | Fairy | 110 |
| Vira Lata Celeste | Fire | 90 |
| Rajada Do Banhado | Water | 90 |
| Martelo De Granito | Rock | 95 |
| Fogo Fatuo Ancestral | Fire | 85 |
| Passo Ao Contrario | Grass | 80 |
| Canto Da Iara | Water | 75 |
| Redemoinho Do Saci | Flying | 80 |
| Encanto Do Boto | Psychic | 85 |
| Abraco Da Boiuna | Dragon | 95 |
| Galope Sem Cabeca | Fire | 90 |
| Mare Da Mae | Water | 90 |
| Forja De Ogum | Steel | 90 |
| Olhar Da Cobra Grande | Ghost | — |
| Aurora De Guaraci | Fire | — |
| Trovao De Tupa | Electric | 105 |
| Correnteza Suprema | Water | 100 |
| Incendio Primordial | Fire | 110 |
| Marulho Atlantico | Water | 105 |
| Essencia Primordial | Dragon | 110 |

## O elenco

Ninguem no jogo responde mais por um nome de Hoenn.

| Hoenn | Arauana |
|---|---|
| ARCHIE | **OTACILIO** |
| BRAWLY | **ADEMAR** |
| BRENDAN | **CIRO** |
| FLANNERY | **NARA** |
| JUAN | **CELINA** |
| LIZA | **CAETANO** |
| MATT | **BRENO** |
| MAXIE | **LUZIA** |
| MAY | **CIRO** |
| NORMAN | **ELIAS** |
| ROXANNE | **DALVA** |
| SHELLY | **MARTA** |
| STEVEN | **BENTO** |
| TABITHA | **RAUL** |
| TATE | **CECILIA** |
| WALLACE | **AMALIA** |
| WALLY | **VAL** |
| WATTSON | **OLIVIA** |
| WINONA | **LIDIA** |
| RYDEL | **ZEFERINO** |
| SCOTT | **BENTO** |
| CAPT. STERN | **NUNES** |
| MR. BRINEY | **HONORIO** |
| PEEKO | **PEROLA** |
| MR. STONE | **AMARAL** |
| LANETTE | **LENITA** |
| COZMO | **SALUSTIO** |
| WINSTRATE | **QUEIROZ** |
| BILL | **ELCIO** |
| SIDNEY | **LAZARO** |
| PHOEBE | **ROSA** |
| GLACIA | **CLARA** |
| DRAKE | **TIBURCIO** |

## Como isto foi verificado

Nada aqui foi so compilado. Cada linha abaixo foi provada com a ROM rodando num emulador, lendo a memoria do jogo -- equipe, niveis, IVs, golpes, HP turno a turno -- e nao olhando o codigo-fonte.

| o que | resultado |
|---|---|
| Varredura de mapas | 403 mapas visitados com o jogador andando 5s em cada um, checando a cada segundo se o ponteiro do save saiu da EWRAM, se o id do mapa deixou de existir, se a tela congelou com input aceito ou se o jogo voltou para a tela de copyright. **Zero achados.** |
| Times dos tres chefes novos | Dalva, Ademar e Olivia lidos de gEnemyParty dentro da batalha: as cinco vagas de cada um chegam com especie, nivel, item, os seis IVs e os quatro golpes customizados exatos. |
| Dificuldade medida | Seis partidas completas. Contra a Dalva, um inicial de nv15 com o golpe certo derruba 4 de 5. Contra o Ademar, 2 de 5. Contra a Olivia, um Ground derruba 2 e trava na dupla Water/Electric. |
| Learnsets dos 386 | Lidos de volta da ROM linkada, decodificando gLevelUpLearnsets. Criaturas criadas em quatro niveis diferentes recebem exatamente os golpes que a tabela promete. |
| Portugues residual | 37418 strings visiveis varridas contra um lexico portugues. Nenhuma passa. |
| Largura de texto | 575 arquivos de script medidos como o motor mede, a partir de charmap.txt e gFontNormalLatinGlyphWidths. Nada acima dos 208px da caixa de fala. |
| Disponibilidade | 293 criaturas capturaveis na natureza, 366 de 386 obteniveis contando evolucao e presentes. |
| ROM limpa | Nenhum simbolo do harness de teste sobrevive na ROM final; a arvore fica limpa depois de cada prova. |

**O que isto nao prova.** Ninguem jogou esta beta do inicio ao fim. A varredura prova que os mapas carregam e que da para andar neles, e as partidas provam que os chefes funcionam -- mas nenhum teste automatico seguiu a cadeia de flags da historia da Vila do Amanhecer ate a Campea. Esse e o teste que a beta publica existe para fazer. Os seis mapas UnusedContestHall* ficaram de fora da varredura: sao conteudo morto do Emerald, inalcancavel em jogo, e o harness trava ao entrar neles justamente por isso.

## A dex completa — as 386 criaturas

Uma marca na coluna *selvagem* quer dizer que ela aparece em alguma
grama, agua ou pesca. As outras vem por evolucao, presente ou evento.

| # | nome | tipos | BST | selvagem | golpes por nivel |
|---:|---|---|---:|:---:|---:|
| 001 | Caramelo | Fire | 325 | sim | 10 |
| 002 | Caramelão | Fire | 425 | — | 12 |
| 003 | Draguará | Fire/Dragon | 595 | — | 15 |
| 004 | Querô | Water | 340 | sim | 10 |
| 005 | Queribela | Water/Bug | 434 | — | 12 |
| 006 | Terolibra | Water/Bug | 595 | — | 15 |
| 007 | Pimpau | Grass | 332 | sim | 10 |
| 008 | Bicopau | Grass | 432 | — | 12 |
| 009 | Petropico | Grass/Rock | 574 | — | 15 |
| 010 | Formilim | Bug | 248 | sim | 10 |
| 011 | Saúvarco | Bug/Ground | 473 | sim | 15 |
| 012 | Capivim | Water/Normal | 360 | sim | 12 |
| 013 | Tucanhão | Flying/Grass | 437 | sim | 13 |
| 014 | Sagüim | Normal | 308 | sim | 9 |
| 015 | Micuiras | Normal/Psychic | 468 | — | 15 |
| 016 | Boitatá | Fire/Ghost | 514 | sim | 13 |
| 017 | Curupim | Grass/Fairy | 445 | sim | 12 |
| 018 | Curupira | Grass/Fairy | 603 | — | 18 |
| 019 | Iaraço | Water/Fairy | 548 | sim | 17 |
| 020 | Sacizinho | Dark/Flying | 461 | sim | 13 |
| 021 | Cactula | Grass/Poison | 382 | sim | 13 |
| 022 | Muriçoco | Bug/Poison | 287 | sim | 13 |
| 023 | Onçaléu | Dark | 524 | sim | 13 |
| 024 | Tamanduá | Ground/Steel | 470 | sim | 13 |
| 025 | Botim | Water | 283 | sim | 10 |
| 026 | Botão | Water/Psychic | 404 | — | 12 |
| 027 | Botogaláu | Water/Psychic | 555 | — | 15 |
| 028 | Tatuim | Ground | 283 | sim | 10 |
| 029 | Tatubola | Ground/Steel | 404 | sim | 12 |
| 030 | Tatuçu | Ground/Steel | 555 | sim | 15 |
| 031 | Ararinha | Flying | 284 | sim | 10 |
| 032 | Arará | Flying/Fire | 405 | — | 12 |
| 033 | Araracanga | Flying/Fire | 550 | — | 15 |
| 034 | Jacarim | Water | 284 | sim | 10 |
| 035 | Jacarão | Water/Dark | 405 | sim | 12 |
| 036 | Jacarodon | Water/Dragon | 551 | — | 15 |
| 037 | Preguicim | Grass | 285 | sim | 10 |
| 038 | Preguicão | Grass/Psychic | 406 | sim | 12 |
| 039 | Bicho-Preguiça | Grass/Psychic | 551 | — | 15 |
| 040 | Papaguim | Flying | 285 | sim | 10 |
| 041 | Papagaio | Flying/Psychic | 406 | sim | 12 |
| 042 | Papagaião | Flying/Psychic | 552 | — | 15 |
| 043 | Antinha | Normal | 286 | sim | 9 |
| 044 | Anta | Normal/Water | 550 | — | 15 |
| 045 | Antaraú | Normal/Water | 446 | sim | 12 |
| 046 | Sucurim | Water/Poison | 286 | sim | 10 |
| 047 | Sucuri | Water/Poison | 480 | — | 12 |
| 048 | Boiuna | Water/Dragon | 600 | — | 15 |
| 049 | Borbolim | Bug | 287 | sim | 10 |
| 050 | Casulete | Bug | 283 | — | 12 |
| 051 | Morphália | Bug/Fairy | 553 | — | 18 |
| 052 | Guaracim | Fire | 287 | sim | 10 |
| 053 | Guará | Fire/Normal | 552 | — | 15 |
| 054 | Guaraflama | Fire/Ghost | 448 | sim | 13 |
| 055 | Peixim | Water | 282 | sim | 10 |
| 056 | Peixeboi | Water | 552 | — | 15 |
| 057 | Mãe-d'Água | Water/Fairy | 448 | sim | 17 |
| 058 | Mandim | Water | 283 | sim | 10 |
| 059 | Mandí | Water/Poison | 404 | sim | 12 |
| 060 | Mandubé | Water/Dark | 555 | — | 15 |
| 061 | Preguim | Normal | 283 | sim | 9 |
| 062 | Prego | Fighting/Normal | 404 | — | 12 |
| 063 | Pregarcanjo | Fighting/Psychic | 555 | — | 15 |
| 064 | Aranin | Bug | 284 | sim | 10 |
| 065 | Caraninha | Bug/Poison | 405 | sim | 12 |
| 066 | Caranga | Bug/Poison | 550 | — | 15 |
| 067 | Gatim | Normal | 284 | sim | 9 |
| 068 | Gato-do-mato | Normal/Dark | 554 | — | 15 |
| 069 | Jaguatirica | Dark/Normal | 445 | sim | 12 |
| 070 | Cutim | Normal | 285 | sim | 9 |
| 071 | Cutia | Normal | 555 | — | 15 |
| 072 | Paca | Normal/Dark | 445 | sim | 12 |
| 073 | Formigão | Bug/Fighting | 447 | sim | 13 |
| 074 | Marimbondo | Bug/Poison | 449 | sim | 13 |
| 075 | Abelhinha | Bug/Flying | 446 | sim | 13 |
| 076 | Quatim | Normal | 286 | sim | 9 |
| 077 | Quati | Normal/Dark | 550 | — | 15 |
| 078 | Coati | Dark/Ground | 446 | sim | 13 |
| 079 | Gambá | Poison/Normal | 286 | sim | 9 |
| 080 | Cangambá | Poison/Dark | 551 | — | 15 |
| 081 | Sarué | Poison/Ghost | 447 | sim | 13 |
| 082 | Tuquinho | Flying | 287 | sim | 10 |
| 083 | Aracari | Flying/Grass | 551 | — | 15 |
| 084 | Curicaca | Flying/Normal | 447 | sim | 12 |
| 085 | Sapim | Water | 287 | sim | 10 |
| 086 | Sapão | Water/Poison | 403 | sim | 12 |
| 087 | Cururu | Poison/Ground | 554 | — | 15 |
| 088 | Teiuzim | Normal | 282 | sim | 9 |
| 089 | Teiú | Normal/Dark | 552 | — | 15 |
| 090 | Camaleão | Normal/Psychic | 448 | sim | 12 |
| 091 | Morcim | Flying | 283 | sim | 10 |
| 092 | Morcego | Flying/Psychic | 404 | — | 12 |
| 093 | Vampiro | Flying/Dark | 555 | sim | 15 |
| 094 | Piuiuim | Flying | 283 | sim | 10 |
| 095 | Tuiuiú | Flying/Water | 553 | — | 15 |
| 096 | Colhereiro | Flying/Fairy | 449 | sim | 17 |
| 097 | Mulinha | Normal | 284 | sim | 9 |
| 098 | Mula | Normal/Fire | 405 | sim | 11 |
| 099 | Mula-sem-Cabeça | Fire/Ghost | 550 | — | 15 |
| 100 | Corcovado | Rock/Dragon | 604 | sim | 13 |
| 101 | Cerválo | Normal | 286 | sim | 9 |
| 102 | Catingueiro | Normal/Grass | 551 | — | 15 |
| 103 | Suçuapara | Normal/Fighting | 447 | sim | 12 |
| 104 | Cabocim | Water | 287 | sim | 10 |
| 105 | Caboclo | Water/Fighting | 551 | — | 15 |
| 106 | Cangaço | Dark/Flying | 447 | sim | 13 |
| 107 | Xangô | Electric/Fighting | 449 | sim | 13 |
| 108 | Iemanjá | Water/Fairy | 604 | sim | 17 |
| 109 | Oxum | Water/Fairy | 606 | sim | 17 |
| 110 | Ogum | Steel/Fire | 602 | sim | 13 |
| 111 | Cavalim | Normal | 284 | sim | 9 |
| 112 | Cavalgado | Normal/Fighting | 554 | — | 15 |
| 113 | Zebuim | Normal | 283 | sim | 9 |
| 114 | Zebu | Normal/Fighting | 553 | — | 15 |
| 115 | Ovelhinha | Normal/Fairy | 449 | sim | 16 |
| 116 | Cabrita | Normal/Rock | 445 | sim | 12 |
| 117 | Chocalhão | Poison | 285 | sim | 10 |
| 118 | Cascavelim | Poison | 406 | sim | 12 |
| 119 | Cascavão | Poison/Dark | 552 | — | 15 |
| 120 | Jararaca | Poison/Grass | 448 | sim | 13 |
| 121 | Pirarim | Water | 282 | — | 10 |
| 122 | Pirarucu | Water/Dragon | 552 | sim | 15 |
| 123 | Piranha | Water/Dark | 448 | sim | 13 |
| 124 | Tambaqui | Water/Normal | 445 | sim | 12 |
| 125 | Aruanã | Water/Flying | 447 | sim | 13 |
| 126 | Poraquê | Electric/Water | 449 | sim | 13 |
| 127 | Curimbatá | Water/Ground | 445 | sim | 13 |
| 128 | Traíra | Water/Dark | 447 | sim | 13 |
| 129 | Dourado | Water/Fighting | 449 | sim | 13 |
| 130 | Tucunaré | Water/Dark | 446 | sim | 13 |
| 131 | Pacu | Water/Grass | 448 | sim | 13 |
| 132 | Matrinxã | Water/Normal | 444 | sim | 13 |
| 133 | Piau | Water/Normal | 446 | sim | 12 |
| 134 | Cascudo | Water/Rock | 448 | sim | 13 |
| 135 | Acará | Water/Psychic | 445 | sim | 13 |
| 136 | Vagalumim | Bug/Electric | 285 | sim | 10 |
| 137 | Vagalume | Bug/Electric | 555 | — | 15 |
| 138 | Cigarrinho | Bug | 283 | sim | 10 |
| 139 | Cigarrão | Bug/Flying | 553 | — | 15 |
| 140 | Louvadinha | Bug | 287 | sim | 10 |
| 141 | Louvadeus | Bug/Psychic | 552 | — | 15 |
| 142 | Escorpim | Poison | 286 | sim | 10 |
| 143 | Escorpião | Poison/Dark | 550 | sim | 15 |
| 144 | Caramulão | Bug/Water | 446 | sim | 13 |
| 145 | Piolhão | Bug/Poison | 448 | sim | 13 |
| 146 | Barata | Bug/Dark | 445 | sim | 13 |
| 147 | Grilim | Bug | 285 | sim | 10 |
| 148 | Grilão | Bug/Normal | 555 | — | 15 |
| 149 | Aranhão | Bug/Poison | 445 | sim | 13 |
| 150 | Vespão | Bug/Flying | 447 | sim | 13 |
| 151 | Marimbondão | Bug/Poison | 449 | sim | 13 |
| 152 | Traça | Bug/Normal | 446 | sim | 12 |
| 153 | Corupião | Bug/Ground | 448 | sim | 13 |
| 154 | Cupinzim | Bug/Ground | 444 | sim | 13 |
| 155 | Formigão-Preto | Bug/Dark | 446 | sim | 13 |
| 156 | Beija-flor | Flying/Fairy | 448 | sim | 17 |
| 157 | Sabiá | Flying/Normal | 445 | sim | 13 |
| 158 | Bem-te-vi | Flying/Normal | 447 | sim | 13 |
| 159 | Urutau | Flying/Ghost | 449 | sim | 13 |
| 160 | Carcará | Flying/Dark | 445 | sim | 13 |
| 161 | Gavião | Flying/Fighting | 447 | sim | 13 |
| 162 | Urubu | Flying/Dark | 555 | sim | 13 |
| 163 | Corurupim | Flying/Psychic | 284 | sim | 12 |
| 164 | Coruja | Flying/Psychic | 554 | — | 13 |
| 165 | Jaburu | Flying/Water | 444 | sim | 13 |
| 166 | Ema | Normal/Flying | 446 | sim | 12 |
| 167 | Seriema | Flying/Fighting | 448 | sim | 13 |
| 168 | Anú | Flying/Dark | 445 | sim | 13 |
| 169 | Trinca-Ferro | Flying/Steel | 447 | sim | 13 |
| 170 | Curió | Flying/Normal | 449 | sim | 13 |
| 171 | Sanhaço | Flying/Fairy | 445 | sim | 17 |
| 172 | Papa-Formiga | Flying/Bug | 447 | sim | 13 |
| 173 | Choca | Flying/Normal | 449 | sim | 13 |
| 174 | Bacurau | Flying/Dark | 446 | sim | 13 |
| 175 | João-de-Barro | Flying/Ground | 448 | sim | 13 |
| 176 | Sementim | Grass | 282 | sim | 10 |
| 177 | Muda | Grass | 403 | — | 12 |
| 178 | Jequitibá | Grass/Rock | 554 | sim | 15 |
| 179 | Bromelinha | Grass/Water | 445 | sim | 13 |
| 180 | Orquidina | Grass/Fairy | 447 | sim | 16 |
| 181 | Vitóriarégia | Grass/Water | 449 | sim | 13 |
| 182 | Ipê | Grass/Fairy | 445 | sim | 16 |
| 183 | Cipó | Grass/Poison | 447 | sim | 13 |
| 184 | Palmito | Grass/Fighting | 449 | sim | 13 |
| 185 | Babaçu | Grass/Ground | 446 | sim | 13 |
| 186 | Buriti | Grass/Water | 448 | sim | 13 |
| 187 | Cajuzim | Grass | 282 | sim | 10 |
| 188 | Cajueiro | Grass/Fire | 552 | — | 15 |
| 189 | Açaí | Grass/Dark | 448 | sim | 13 |
| 190 | Cacauim | Grass | 283 | sim | 10 |
| 191 | Cacaueiro | Grass/Normal | 553 | — | 15 |
| 192 | Guaraná | Grass/Electric | 449 | sim | 13 |
| 193 | Mate | Grass/Water | 445 | sim | 13 |
| 194 | Milho | Grass/Normal | 447 | sim | 12 |
| 195 | Mandioca | Grass/Ground | 449 | sim | 13 |
| 196 | Pedrinha | Rock | 284 | sim | 10 |
| 197 | Rochão | Rock | 554 | sim | 15 |
| 198 | Cristalim | Rock/Fairy | 282 | sim | 12 |
| 199 | Ametista | Rock/Psychic | 552 | sim | 15 |
| 200 | Ouríço | Steel/Electric | 448 | sim | 13 |
| 201 | Ferrolho | Steel/Ground | 445 | sim | 13 |
| 202 | Diamantina | Rock/Fairy | 605 | sim | 16 |
| 203 | Bauxito | Steel/Ground | 449 | sim | 13 |
| 204 | Manganim | Steel/Dark | 445 | sim | 13 |
| 205 | Salitre | Rock/Water | 447 | sim | 13 |
| 206 | Enxofrino | Fire/Poison | 449 | sim | 13 |
| 207 | Argilim | Ground | 284 | sim | 10 |
| 208 | Boneco | Ground/Psychic | 554 | — | 15 |
| 209 | Estalactite | Rock/Water | 444 | sim | 13 |
| 210 | Estalagmite | Rock/Ground | 446 | sim | 13 |
| 211 | Fóssil | Rock/Dragon | 448 | sim | 13 |
| 212 | Meteorito | Rock/Psychic | 603 | sim | 13 |
| 213 | Vulcanite | Fire/Rock | 447 | sim | 13 |
| 214 | Marmim | Rock/Fairy | 449 | sim | 16 |
| 215 | Granito | Rock/Fighting | 445 | sim | 13 |
| 216 | Caranguim | Water | 285 | sim | 10 |
| 217 | Guaiamum | Water/Ground | 555 | — | 15 |
| 218 | Siri | Water/Fighting | 446 | sim | 13 |
| 219 | Camarão | Water | 448 | sim | 13 |
| 220 | Polvim | Water/Psychic | 282 | sim | 10 |
| 221 | Polvão | Water/Psychic | 552 | — | 13 |
| 222 | Águaviva | Water/Poison | 448 | sim | 15 |
| 223 | Cavalim-Marinho | Water/Fairy | 445 | sim | 17 |
| 224 | Tartaruguim | Water | 285 | sim | 10 |
| 225 | Tartaruga | Water/Rock | 555 | — | 13 |
| 226 | Golfinho | Water/Psychic | 445 | sim | 15 |
| 227 | Baleia | Water/Normal | 447 | sim | 12 |
| 228 | Tubarim | Water/Dark | 287 | sim | 10 |
| 229 | Tubarão | Water/Dark | 552 | — | 13 |
| 230 | Arraia | Water/Electric | 448 | sim | 15 |
| 231 | Peixe-Espada | Water/Steel | 444 | sim | 13 |
| 232 | Pargo | Water/Fire | 446 | sim | 13 |
| 233 | Pescadão | Water/Dark | 448 | sim | 13 |
| 234 | Loirinha | Ghost/Fairy | 445 | sim | 17 |
| 235 | Cuca | Dark/Psychic | 447 | sim | 13 |
| 236 | Bicho-Papão | Dark/Ghost | 449 | sim | 13 |
| 237 | Lobisomem | Dark/Normal | 445 | sim | 13 |
| 238 | Corpo-Seco | Ghost/Dark | 447 | sim | 13 |
| 239 | Mão-Peluda | Ghost/Fighting | 449 | sim | 13 |
| 240 | Perna-Cabeluda | Ghost/Normal | 446 | sim | 12 |
| 241 | Comadre | Ghost/Fairy | 448 | sim | 17 |
| 242 | Anhangá | Ghost/Grass | 444 | sim | 13 |
| 243 | Jurupari | Dark/Fairy | 604 | sim | 16 |
| 244 | Tupã | Electric/Dragon | 606 | sim | 13 |
| 245 | Jaci | Fairy/Psychic | 603 | sim | 18 |
| 246 | Guaraci | Fire/Fairy | 605 | sim | 16 |
| 247 | Rudá | Fairy/Psychic | 449 | sim | 18 |
| 248 | Aluá | Water/Poison | 445 | sim | 13 |
| 249 | Jenipapo | Dark/Grass | 447 | sim | 13 |
| 250 | Urucum | Fire/Grass | 449 | sim | 13 |
| 251 | Caipora | Grass/Fighting | 552 | sim | 13 |
| 252 | Anhangá-Pitã | Ghost/Fire | 448 | sim | 13 |
| 253 | Yara-Pindá | Water/Fairy | 444 | sim | 17 |
| 254 | Pisadeira | Ghost/Fighting | 446 | sim | 13 |
| 255 | Zumbi | Ghost/Fighting | 606 | sim | 13 |
| 256 | Iemanjá-Pequena | Water/Fairy | 445 | sim | 17 |
| 257 | Ossanha | Grass/Fairy | 447 | sim | 16 |
| 258 | Oxalá | Normal/Fairy | 607 | sim | 15 |
| 259 | Saciamigo | Dark/Fairy | 445 | sim | 16 |
| 260 | Sacipererê | Dark/Fairy | 605 | sim | 16 |
| 261 | Curupira-Ancião | Grass/Fairy | 449 | sim | 16 |
| 262 | Caipora-Fêmea | Grass/Fighting | 446 | sim | 13 |
| 263 | Pomba-Gira | Dark/Fairy | 448 | sim | 16 |
| 264 | Exu | Dark/Fighting | 444 | sim | 13 |
| 265 | Preto-Velho | Ghost/Psychic | 604 | sim | 13 |
| 266 | Caboclo-Guerreiro | Grass/Fighting | 448 | sim | 13 |
| 267 | Marinheiro | Water/Dark | 445 | sim | 13 |
| 268 | Baiano | Fire/Fighting | 447 | sim | 13 |
| 269 | Cangaceiro | Dark/Fighting | 449 | sim | 13 |
| 270 | Beata | Fairy/Psychic | 445 | sim | 18 |
| 271 | Menino-Deus | Fairy/Normal | 447 | sim | 17 |
| 272 | Rei-Momo | Normal/Fire | 449 | sim | 12 |
| 273 | Bumba-Meu-Boi | Normal/Fire | 446 | sim | 12 |
| 274 | Reisado | Fairy/Normal | 448 | sim | 17 |
| 275 | Frevinho | Fighting/Fire | 444 | sim | 13 |
| 276 | Maracatu | Dark/Fairy | 446 | sim | 17 |
| 277 | Congada | Fighting/Fire | 448 | sim | 13 |
| 278 | Folião | Normal/Fairy | 445 | sim | 16 |
| 279 | Onçuma | Dark/Ghost | 605 | sim | 13 |
| 280 | Sucuriaçu | Water/Dragon | 607 | sim | 13 |
| 281 | Pirarumbá | Water/Dragon | 603 | sim | 13 |
| 282 | Draguará-Alfa | Fire/Dragon | 605 | sim | 16 |
| 283 | Terolibra-Rainha | Water/Bug | 607 | sim | 13 |
| 284 | Petropico-Ancião | Grass/Rock | 604 | sim | 13 |
| 285 | Boitatá-Puro | Fire/Dragon | 606 | sim | 13 |
| 286 | Iara-Mãe | Water/Fairy | 602 | sim | 17 |
| 287 | Curupira-Rei | Grass/Fairy | 604 | sim | 16 |
| 288 | Saci-Rei | Dark/Fairy | 606 | sim | 16 |
| 289 | Anhangaú | Ghost/Grass | 603 | sim | 13 |
| 290 | Muirá-Kytã | Grass/Fairy | 605 | sim | 16 |
| 291 | Cobra-Norato | Water/Dragon | 607 | sim | 13 |
| 292 | Mapinguari | Grass/Fighting | 603 | sim | 13 |
| 293 | Ipupiara | Water/Dark | 605 | sim | 13 |
| 294 | Uirapuru | Flying/Fairy | 607 | sim | 17 |
| 295 | Muiraquitã | Rock/Fairy | 604 | sim | 16 |
| 296 | Amazona | Fighting/Fairy | 606 | sim | 16 |
| 297 | Corcovado-Ancião | Rock/Dragon | 602 | sim | 13 |
| 298 | Cristo | Fairy/Psychic | 604 | sim | 18 |
| 299 | Ratão | Dark/Poison | 448 | sim | 13 |
| 300 | Pombim | Flying/Normal | 283 | sim | 9 |
| 301 | Pombão | Flying/Poison | 553 | — | 13 |
| 302 | Baratão | Bug/Flying | 449 | sim | 15 |
| 303 | Mosquim | Bug/Poison | 445 | sim | 13 |
| 304 | Cão-Bravo | Dark/Normal | 447 | sim | 13 |
| 305 | Gato-Preto | Dark/Psychic | 449 | sim | 13 |
| 306 | Perereca | Water/Poison | 446 | sim | 13 |
| 307 | Lagartixa | Normal/Psychic | 448 | sim | 12 |
| 308 | Traça-Papel | Bug/Psychic | 444 | sim | 13 |
| 309 | Poeirão | Ground/Dark | 446 | sim | 13 |
| 310 | Ferrugem | Steel/Water | 448 | sim | 13 |
| 311 | Fumacento | Poison/Flying | 445 | sim | 13 |
| 312 | Óleoso | Poison/Water | 447 | sim | 13 |
| 313 | Lixão | Poison/Ground | 287 | sim | 10 |
| 314 | Chorume | Poison/Dark | 551 | — | 13 |
| 315 | Bituca | Fire/Poison | 447 | sim | 13 |
| 316 | Latinha | Steel/Normal | 449 | sim | 15 |
| 317 | Sacolim | Poison/Flying | 446 | sim | 13 |
| 318 | Garrafão | Water/Poison | 448 | sim | 13 |
| 319 | Netzero | Flying/Poison | 444 | sim | 13 |
| 320 | Pilhoso | Electric/Poison | 446 | sim | 13 |
| 321 | Cabofio | Electric/Steel | 448 | sim | 13 |
| 322 | Bugão | Bug/Dark | 445 | sim | 13 |
| 323 | Aluminio | Steel/Flying | 447 | sim | 13 |
| 324 | Concretim | Rock/Steel | 449 | sim | 13 |
| 325 | Bueiro | Water/Dark | 445 | sim | 13 |
| 326 | Sinal | Electric/Psychic | 447 | sim | 13 |
| 327 | Poste | Steel/Electric | 449 | sim | 13 |
| 328 | Grafiteiro | Dark/Fairy | 446 | sim | 16 |
| 329 | Guaraciana | Fire/Fairy | 606 | — | 18 |
| 330 | Jaciana | Fairy/Water | 602 | — | 20 |
| 331 | Tupanaú | Electric/Dragon | 604 | — | 15 |
| 332 | Iaraú | Water/Fairy | 606 | sim | 19 |
| 333 | Kuarahy | Fire/Psychic | 603 | — | 15 |
| 334 | Yasy | Fairy/Dark | 605 | — | 20 |
| 335 | Rudarauna | Fairy/Psychic | 607 | — | 20 |
| 336 | Perybé | Water/Psychic | 603 | — | 15 |
| 337 | Arauanaú | Fairy/Dragon | 605 | — | 20 |
| 338 | Verdejante | Grass/Dragon | 607 | — | 15 |
| 339 | Chuvão | Water/Electric | 604 | — | 15 |
| 340 | Solzão | Fire/Ground | 606 | — | 15 |
| 341 | Ventania | Flying/Dragon | 602 | — | 15 |
| 342 | Terraão | Ground/Rock | 604 | — | 15 |
| 343 | Fogaréu | Fire/Dragon | 606 | — | 15 |
| 344 | Marulho | Water/Dragon | 603 | — | 15 |
| 345 | Alvorecer | Fairy/Fire | 605 | — | 20 |
| 346 | Poente | Dark/Fire | 607 | — | 15 |
| 347 | Estrelinha | Fairy/Psychic | 648 | — | 20 |
| 348 | Arauanamon | Dragon/Fairy | 650 | — | 19 |
| 349 | Aracuã | Flying/Normal | 449 | sim | 13 |
| 350 | Bugio | Normal/Dark | 446 | sim | 13 |
| 351 | Tuim | Grass | 305 | sim | 10 |
| 352 | Periquitão | Grass/Flying | 439 | — | 12 |
| 353 | Ararunão | Grass/Flying | 598 | — | 15 |
| 354 | Preazinho | Normal | 328 | sim | 9 |
| 355 | Capivarão | Normal/Water | 510 | — | 15 |
| 356 | Tamanduí | Bug | 320 | sim | 10 |
| 357 | Tamanduá | Bug/Ground | 440 | sim | 12 |
| 358 | Tamanduão | Bug/Ground | 545 | sim | 15 |
| 359 | Preguicinha | Grass | 285 | sim | 10 |
| 360 | Preguiçoso | Grass/Psychic | 520 | sim | 15 |
| 361 | Beija-Flor | Fairy/Flying | 377 | sim | 14 |
| 362 | Beija-Luz | Fairy/Fire | 482 | sim | 16 |
| 363 | Beija-Sol | Fairy/Fire | 610 | — | 20 |
| 364 | Sarará | Fairy/Water | 472 | sim | 18 |
| 365 | Cambota | Fighting/Normal | 485 | sim | 12 |
| 366 | Berimbau | Fairy/Fighting | 505 | sim | 18 |
| 367 | Atabaque | Fighting/Ground | 495 | sim | 13 |
| 368 | Pandeirim | Fairy/Normal | 460 | sim | 18 |
| 369 | Sanfoninha | Normal/Fairy | 510 | sim | 16 |
| 370 | Violeiro | Grass/Fairy | 523 | sim | 17 |
| 371 | Zabumba | Ground/Fighting | 515 | sim | 13 |
| 372 | Cordelim | Psychic/Fairy | 485 | sim | 18 |
| 373 | Rendeira | Fairy/Bug | 515 | sim | 18 |
| 374 | Escamoso | Water/Dark | 498 | sim | 13 |
| 375 | Piranhita | Water/Dark | 395 | sim | 13 |
| 376 | Boitatã | Fire/Dragon | 650 | — | 15 |
| 377 | Piraruaçu | Water/Dragon | 630 | — | 15 |
| 378 | Mata-Mata | Grass/Dragon | 640 | — | 15 |
| 379 | Solaris | Fire/Psychic | 670 | — | 15 |
| 380 | Selenê | Dark/Psychic | 670 | — | 15 |
| 381 | Zumbi-Rei | Fighting/Dark | 655 | — | 15 |
| 382 | Iemanjã | Water/Fairy | 695 | — | 19 |
| 383 | Oxumará | Dragon/Fairy | 695 | — | 18 |
| 384 | Curupixel | Grass/Fairy | 645 | — | 18 |
| 385 | Sacinho | Dark/Fairy | 650 | — | 18 |
| 386 | Arauá | Dragon/Psychic | 720 | — | 15 |

## O que a beta ainda nao tem

O plano dos especiais tem 31 lendarios e miticos. **11 ja estao no jogo**,
nos encontros estaticos herdados do Emerald. Os outros **20 nao tem lugar
no mapa** -- a dex nao fecha nesta beta, e isso e conhecido.

### Os 20 que ainda esperam lugar

| dex | nome | tipos | nivel previsto | lugar previsto |
|---:|---|---|---:|---|
| 329 | Guaraciana | fire/fairy | 60 | SERRA DO UIVO / TORRE JURAMENTO - santuario dedicado |
| 330 | Jaciana | fairy/water | 60 | BAIA DAS LUZES / aguas costeiras - encontro estatico |
| 331 | Tupanaú | electric/dragon | 60 | SERRA DO UIVO / TORRE JURAMENTO - santuario dedicado |
| 332 | Iaraú | water/fairy | 60 | MATA DO MEIO / CAVERNAS M'BOI - encontro estatico |
| 333 | Kuarahy | fire/psychic | 60 | SERRA DO UIVO / TORRE JURAMENTO - santuario dedicado |
| 334 | Yasy | fairy/dark | 60 | SERRA DO UIVO / TORRE JURAMENTO - santuario dedicado |
| 335 | Rudarauna | fairy/psychic | 60 | BAIA DAS LUZES / aguas costeiras - encontro estatico |
| 336 | Perybé | water/psychic | 60 | MATA DO MEIO / CAVERNAS M'BOI - encontro estatico |
| 337 | Arauanaú | fairy/dragon | 62 | TORRE JURAMENTO / ESTR. JURAMENTO |
| 338 | Verdejante | grass/dragon | 60 | MATA DO MEIO / CAVERNAS M'BOI - encontro estatico |
| 339 | Chuvão | water/electric | 60 | BAIA DAS LUZES / aguas costeiras - encontro estatico |
| 340 | Solzão | fire/ground | 58 | SERRA DA CINZA / torre ou ruina dedicada |
| 341 | Ventania | flying/dragon | 58 | Cerrado tardio / santuario dedicado |
| 342 | Terraão | ground/rock | 62 | RUINAS DA QUEDA / ESTR. JURAMENTO |
| 343 | Fogaréu | fire/dragon | 60 | SERRA DO UIVO / TORRE JURAMENTO - santuario dedicado |
| 344 | Marulho | water/dragon | 60 | BAIA DAS LUZES / aguas costeiras - encontro estatico |
| 346 | Poente | dark/fire | 60 | BAIA DAS LUZES / aguas costeiras - encontro estatico |
| 348 | Arauanamon | dragon/fairy | 68 | TORRE JURAMENTO / ESTR. JURAMENTO |
| 376 | Boitatã | fire/dragon | 65 | Cerrado tardio / santuario dedicado |
| 385 | Sacinho | dark/fairy | 65 | Cerrado tardio / santuario dedicado |

### Os 11 que ja podem ser encontrados

| dex | nome | tipos |
|---:|---|---|
| 345 | Alvorecer | fairy/fire |
| 347 | Estrelinha | fairy/psychic |
| 377 | Piraruaçu | water/dragon |
| 378 | Mata-Mata | grass/dragon |
| 379 | Solaris | fire/psychic |
| 380 | Selenê | dark/psychic |
| 381 | Zumbi-Rei | fighting/dark |
| 382 | Iemanjã | water/fairy |
| 383 | Oxumará | dragon/fairy |
| 384 | Curupixel | grass/fairy |
| 386 | Arauá | dragon/psychic |


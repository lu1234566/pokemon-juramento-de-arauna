# Quem ja tem STAB dentro do teto de cada chefe

Gerado por `tools/arauna/build_stab_pool.py` a partir do repositorio.
Nao edite a mao: rode `python3 tools/arauna/build_stab_pool.py --write`.

A pergunta e uma so: **para o time deste chefe, quem eu posso escolher sem
inventar TM, sem subir o nivel e sem golpe fora do learnset?** Uma especie so
entra aqui se o tipo do chefe e um dos seus dois tipos **e** ela aprende, por
nivel, um golpe ofensivo daquele tipo ate o teto de nivel do chefe.

Fora da conta: os 31 lendarios/miticos de `docs/arauna/ESPECIAIS_ESTATICOS.csv`,
as tres linhas iniciais (#001-#009) e a familia pseudo #046-#048.

## Resumo

| chefe | tipo | teto | do tipo | com STAB no teto |
|---|---|---:|---:|---:|
| Dalva | ROCK | 15 | 22 | **15** |
| Ademar | FIGHTING | 19 | 31 | **19** |
| Olivia | ELECTRIC | 24 | 12 | **7** |
| Nara | FIRE | 29 | 26 | **24** |
| Elias | NORMAL | 31 | 65 | **65** |
| Lidia | FLYING | 33 | 54 | **53** |
| Cec&Caet | PSYCHIC | 42 | 32 | **29** |
| Celina | WATER | 46 | 83 | **82** |
| Sidney | DARK | 49 | 56 | **56** |
| Phoebe | GHOST | 51 | 18 | **18** |
| Glacia | STEEL | 53 | 16 | **16** |
| Drake | DRAGON | 55 | 11 | **10** |

## Dalva — ROCK, ate nv15

15 das 22 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 284 | Petropico-Ancião | Grass/Rock | 604 | ROCK_THROW (50) | 15 |
| 212 | Meteorito | Rock/Psychic | 603 | ROCK_THROW (50) | 10 |
| 297 | Corcovado-Ancião | Rock/Dragon | 602 | ROCK_THROW (50) | 10 |
| 225 | Tartaruga | Water/Rock | 555 | ROCK_THROW (50) | 15 |
| 197 | Rochão | Rock | 554 | ROCK_THROW (50) | 9 |
| 199 | Ametista | Rock/Psychic | 552 | ANCIENT_POWER (60) | 13 |
| 214 | Marmim | Rock/Fairy | 449 | ROCK_THROW (50) | 10 |
| 324 | Concretim | Rock/Steel | 449 | ROCK_THROW (50) | 10 |
| 134 | Cascudo | Water/Rock | 448 | ROCK_THROW (50) | 15 |
| 205 | Salitre | Rock/Water | 447 | ROCK_THROW (50) | 10 |
| 213 | Vulcanite | Fire/Rock | 447 | ROCK_THROW (50) | 15 |
| 116 | Cabrita | Normal/Rock | 445 | ROCK_THROW (50) | 10 |
| 215 | Granito | Rock/Fighting | 445 | ROCK_THROW (50) | 10 |
| 209 | Estalactite | Rock/Water | 444 | ROCK_THROW (50) | 10 |
| 196 | Pedrinha | Rock | 284 | ROCK_THROW (50) | 10 |

Fora por pouco — sao do tipo, mas o primeiro golpe ofensivo
daquele tipo so chega depois do teto:

| dex | nome | tipos | BST | primeiro STAB ofensivo |
|---:|---|---|---:|---|
| 202 | Diamantina | Rock/Fairy | 605 | ANCIENT_POWER no nv34 |
| 100 | Corcovado | Rock/Dragon | 604 | ANCIENT_POWER no nv34 |
| 295 | Muiraquitã | Rock/Fairy | 604 | ANCIENT_POWER no nv34 |
| 178 | Jequitibá | Grass/Rock | 554 | ROLLOUT no nv46 |
| 211 | Fóssil | Rock/Dragon | 448 | ANCIENT_POWER no nv34 |
| 210 | Estalagmite | Rock/Ground | 446 | ROLLOUT no nv24 |
| 198 | Cristalim | Rock/Fairy | 282 | ANCIENT_POWER no nv24 |

## Ademar — FIGHTING, ate nv19

19 das 31 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 255 | Zumbi | Ghost/Fighting | 606 | KARATE_CHOP (50) | 19 |
| 292 | Mapinguari | Grass/Fighting | 603 | KARATE_CHOP (50) | 19 |
| 63 | Pregarcanjo | Fighting/Psychic | 555 | LOW_KICK (variavel) | 17 |
| 251 | Caipora | Grass/Fighting | 552 | KARATE_CHOP (50) | 19 |
| 366 | Berimbau | Fairy/Fighting | 505 | KARATE_CHOP (50) | 19 |
| 367 | Atabaque | Fighting/Ground | 495 | KARATE_CHOP (50) | 15 |
| 129 | Dourado | Water/Fighting | 449 | KARATE_CHOP (50) | 19 |
| 239 | Mão-Peluda | Ghost/Fighting | 449 | KARATE_CHOP (50) | 19 |
| 269 | Cangaceiro | Dark/Fighting | 449 | KARATE_CHOP (50) | 19 |
| 266 | Caboclo-Guerreiro | Grass/Fighting | 448 | KARATE_CHOP (50) | 19 |
| 277 | Congada | Fighting/Fire | 448 | KARATE_CHOP (50) | 15 |
| 103 | Suçuapara | Normal/Fighting | 447 | KARATE_CHOP (50) | 16 |
| 268 | Baiano | Fire/Fighting | 447 | KARATE_CHOP (50) | 19 |
| 218 | Siri | Water/Fighting | 446 | KARATE_CHOP (50) | 19 |
| 254 | Pisadeira | Ghost/Fighting | 446 | KARATE_CHOP (50) | 19 |
| 262 | Caipora-Fêmea | Grass/Fighting | 446 | KARATE_CHOP (50) | 19 |
| 215 | Granito | Rock/Fighting | 445 | KARATE_CHOP (50) | 19 |
| 264 | Exu | Dark/Fighting | 444 | KARATE_CHOP (50) | 19 |
| 275 | Frevinho | Fighting/Fire | 444 | KARATE_CHOP (50) | 15 |

Fora por pouco — sao do tipo, mas o primeiro golpe ofensivo
daquele tipo so chega depois do teto:

| dex | nome | tipos | BST | primeiro STAB ofensivo |
|---:|---|---|---:|---|
| 296 | Amazona | Fighting/Fairy | 606 | LOW_KICK no nv24 |
| 112 | Cavalgado | Normal/Fighting | 554 | KARATE_CHOP no nv34 |
| 114 | Zebu | Normal/Fighting | 553 | KARATE_CHOP no nv34 |
| 105 | Caboclo | Water/Fighting | 551 | KARATE_CHOP no nv38 |
| 371 | Zabumba | Ground/Fighting | 515 | LOW_KICK no nv24 |
| 365 | Cambota | Fighting/Normal | 485 | MACH_PUNCH no nv26 |
| 107 | Xangô | Electric/Fighting | 449 | LOW_KICK no nv24 |
| 184 | Palmito | Grass/Fighting | 449 | LOW_KICK no nv24 |
| 167 | Seriema | Flying/Fighting | 448 | MACH_PUNCH no nv29 |
| 73 | Formigão | Bug/Fighting | 447 | MACH_PUNCH no nv29 |
| 161 | Gavião | Flying/Fighting | 447 | MACH_PUNCH no nv29 |
| 62 | Prego | Fighting/Normal | 404 | LOW_KICK no nv31 |

## Olivia — ELECTRIC, ate nv24

7 das 12 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 244 | Tupã | Electric/Dragon | 606 | SPARK (65) | 24 |
| 137 | Vagalume | Bug/Electric | 555 | SHOCK_WAVE (60) | 17 |
| 107 | Xangô | Electric/Fighting | 449 | SPARK (65) | 19 |
| 327 | Poste | Steel/Electric | 449 | THUNDER_SHOCK (40) | 10 |
| 200 | Ouríço | Steel/Electric | 448 | THUNDER_SHOCK (40) | 10 |
| 320 | Pilhoso | Electric/Poison | 446 | SPARK (65) | 24 |
| 136 | Vagalumim | Bug/Electric | 285 | SPARK (65) | 19 |

Fora por pouco — sao do tipo, mas o primeiro golpe ofensivo
daquele tipo so chega depois do teto:

| dex | nome | tipos | BST | primeiro STAB ofensivo |
|---:|---|---|---:|---|
| 126 | Poraquê | Electric/Water | 449 | SHOCK_WAVE no nv29 |
| 192 | Guaraná | Grass/Electric | 449 | SPARK no nv29 |
| 230 | Arraia | Water/Electric | 448 | THUNDER_SHOCK no nv34 |
| 321 | Cabofio | Electric/Steel | 448 | SHOCK_WAVE no nv29 |
| 326 | Sinal | Electric/Psychic | 447 | SHOCK_WAVE no nv29 |

## Nara — FIRE, ate nv29

24 das 26 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 363 | Beija-Sol | Fairy/Fire | 610 | HEAT_WAVE (100) | 25 |
| 285 | Boitatá-Puro | Fire/Dragon | 606 | FLAMETHROWER (95) | 29 |
| 246 | Guaraci | Fire/Fairy | 605 | EMBER (40) | 2 |
| 282 | Draguará-Alfa | Fire/Dragon | 605 | FLAME_WHEEL (60) | 19 |
| 110 | Ogum | Steel/Fire | 602 | FLAME_WHEEL (60) | 26 |
| 53 | Guará | Fire/Normal | 552 | HEAT_WAVE (100) | 29 |
| 188 | Cajueiro | Grass/Fire | 552 | EMBER (40) | 29 |
| 33 | Araracanga | Flying/Fire | 550 | FLAMETHROWER (95) | 21 |
| 99 | Mula-sem-Cabeça | Fire/Ghost | 550 | HEAT_WAVE (100) | 27 |
| 16 | Boitatá | Fire/Ghost | 514 | FIRE_SPIN (15) | 26 |
| 206 | Enxofrino | Fire/Poison | 449 | FLAME_WHEEL (60) | 15 |
| 250 | Urucum | Fire/Grass | 449 | EMBER (40) | 2 |
| 272 | Rei-Momo | Normal/Fire | 449 | EMBER (40) | 2 |
| 54 | Guaraflama | Fire/Ghost | 448 | FLAME_WHEEL (60) | 15 |
| 277 | Congada | Fighting/Fire | 448 | FLAME_WHEEL (60) | 19 |
| 213 | Vulcanite | Fire/Rock | 447 | EMBER (40) | 2 |
| 268 | Baiano | Fire/Fighting | 447 | FLAME_WHEEL (60) | 15 |
| 315 | Bituca | Fire/Poison | 447 | EMBER (40) | 2 |
| 232 | Pargo | Water/Fire | 446 | FLAME_WHEEL (60) | 19 |
| 273 | Bumba-Meu-Boi | Normal/Fire | 446 | FLAME_WHEEL (60) | 21 |
| 275 | Frevinho | Fighting/Fire | 444 | FLAME_WHEEL (60) | 19 |
| 32 | Arará | Flying/Fire | 405 | FLAME_WHEEL (60) | 26 |
| 98 | Mula | Normal/Fire | 405 | EMBER (40) | 24 |
| 52 | Guaracim | Fire | 287 | FLAMETHROWER (95) | 28 |

Fora por pouco — sao do tipo, mas o primeiro golpe ofensivo
daquele tipo so chega depois do teto:

| dex | nome | tipos | BST | primeiro STAB ofensivo |
|---:|---|---|---:|---|
| 362 | Beija-Luz | Fairy/Fire | 482 | FIRE_SPIN no nv35 |
| 252 | Anhangá-Pitã | Ghost/Fire | 448 | FLAMETHROWER no nv44 |

## Elias — NORMAL, ate nv31

65 das 65 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 258 | Oxalá | Normal/Fairy | 607 | HEADBUTT (70) | 26 |
| 71 | Cutia | Normal | 555 | DOUBLE_EDGE (120) | 25 |
| 148 | Grilão | Bug/Normal | 555 | SCRATCH (40) | 1 |
| 68 | Gato-do-mato | Normal/Dark | 554 | DOUBLE_EDGE (120) | 25 |
| 112 | Cavalgado | Normal/Fighting | 554 | DOUBLE_EDGE (120) | 17 |
| 114 | Zebu | Normal/Fighting | 553 | DOUBLE_EDGE (120) | 21 |
| 191 | Cacaueiro | Grass/Normal | 553 | TACKLE (35) | 1 |
| 53 | Guará | Fire/Normal | 552 | TACKLE (35) | 1 |
| 89 | Teiú | Normal/Dark | 552 | TAKE_DOWN (90) | 13 |
| 102 | Catingueiro | Normal/Grass | 551 | DOUBLE_EDGE (120) | 21 |
| 44 | Anta | Normal/Water | 550 | DOUBLE_EDGE (120) | 21 |
| 77 | Quati | Normal/Dark | 550 | DOUBLE_EDGE (120) | 25 |
| 355 | Capivarão | Normal/Water | 510 | DOUBLE_EDGE (120) | 25 |
| 369 | Sanfoninha | Normal/Fairy | 510 | HEADBUTT (70) | 26 |
| 365 | Cambota | Fighting/Normal | 485 | HEADBUTT (70) | 21 |
| 15 | Micuiras | Normal/Psychic | 468 | DOUBLE_EDGE (120) | 21 |
| 368 | Pandeirim | Fairy/Normal | 460 | HEADBUTT (70) | 24 |
| 115 | Ovelhinha | Normal/Fairy | 449 | TAKE_DOWN (90) | 29 |
| 170 | Curió | Flying/Normal | 449 | TAKE_DOWN (90) | 19 |
| 173 | Choca | Flying/Normal | 449 | HEADBUTT (70) | 15 |
| 272 | Rei-Momo | Normal/Fire | 449 | HEADBUTT (70) | 21 |
| 316 | Latinha | Steel/Normal | 449 | TACKLE (35) | 1 |
| 349 | Aracuã | Flying/Normal | 449 | TAKE_DOWN (90) | 19 |
| 90 | Camaleão | Normal/Psychic | 448 | HEADBUTT (70) | 26 |
| 274 | Reisado | Fairy/Normal | 448 | QUICK_ATTACK (40) | 21 |
| 307 | Lagartixa | Normal/Psychic | 448 | QUICK_ATTACK (40) | 16 |
| 84 | Curicaca | Flying/Normal | 447 | HEADBUTT (70) | 16 |
| 103 | Suçuapara | Normal/Fighting | 447 | TAKE_DOWN (90) | 26 |
| 158 | Bem-te-vi | Flying/Normal | 447 | HEADBUTT (70) | 15 |
| 194 | Milho | Grass/Normal | 447 | TACKLE (35) | 1 |
| 227 | Baleia | Water/Normal | 447 | HEADBUTT (70) | 26 |
| 271 | Menino-Deus | Fairy/Normal | 447 | QUICK_ATTACK (40) | 21 |
| 304 | Cão-Bravo | Dark/Normal | 447 | HEADBUTT (70) | 24 |
| 45 | Antaraú | Normal/Water | 446 | HEADBUTT (70) | 26 |
| 133 | Piau | Water/Normal | 446 | HEADBUTT (70) | 26 |
| 152 | Traça | Bug/Normal | 446 | QUICK_ATTACK (40) | 16 |
| 166 | Ema | Normal/Flying | 446 | TAKE_DOWN (90) | 21 |
| 240 | Perna-Cabeluda | Ghost/Normal | 446 | SCRATCH (40) | 1 |
| 273 | Bumba-Meu-Boi | Normal/Fire | 446 | SCRATCH (40) | 1 |
| 350 | Bugio | Normal/Dark | 446 | TAKE_DOWN (90) | 29 |
| 69 | Jaguatirica | Dark/Normal | 445 | SCRATCH (40) | 1 |
| 72 | Paca | Normal/Dark | 445 | SCRATCH (40) | 1 |
| 116 | Cabrita | Normal/Rock | 445 | QUICK_ATTACK (40) | 16 |
| 124 | Tambaqui | Water/Normal | 445 | HEADBUTT (70) | 26 |
| 157 | Sabiá | Flying/Normal | 445 | HEADBUTT (70) | 15 |
| 237 | Lobisomem | Dark/Normal | 445 | TAKE_DOWN (90) | 29 |
| 278 | Folião | Normal/Fairy | 445 | HEADBUTT (70) | 26 |
| 132 | Matrinxã | Water/Normal | 444 | HEADBUTT (70) | 24 |
| 98 | Mula | Normal/Fire | 405 | DOUBLE_EDGE (120) | 19 |
| 62 | Prego | Fighting/Normal | 404 | DOUBLE_EDGE (120) | 18 |
| 12 | Capivim | Water/Normal | 360 | HEADBUTT (70) | 26 |
| 354 | Preazinho | Normal | 328 | TAKE_DOWN (90) | 26 |
| 14 | Sagüim | Normal | 308 | TAKE_DOWN (90) | 21 |
| 43 | Antinha | Normal | 286 | TAKE_DOWN (90) | 21 |
| 76 | Quatim | Normal | 286 | TAKE_DOWN (90) | 21 |
| 79 | Gambá | Poison/Normal | 286 | TACKLE (35) | 1 |
| 101 | Cerválo | Normal | 286 | TAKE_DOWN (90) | 21 |
| 70 | Cutim | Normal | 285 | DOUBLE_EDGE (120) | 31 |
| 67 | Gatim | Normal | 284 | TAKE_DOWN (90) | 21 |
| 97 | Mulinha | Normal | 284 | TAKE_DOWN (90) | 21 |
| 111 | Cavalim | Normal | 284 | DOUBLE_EDGE (120) | 31 |
| 61 | Preguim | Normal | 283 | TAKE_DOWN (90) | 21 |
| 113 | Zebuim | Normal | 283 | TAKE_DOWN (90) | 21 |
| 300 | Pombim | Flying/Normal | 283 | TAKE_DOWN (90) | 21 |
| 88 | Teiuzim | Normal | 282 | TAKE_DOWN (90) | 21 |

## Lidia — FLYING, ate nv33

53 das 54 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 294 | Uirapuru | Flying/Fairy | 607 | GUST (40) | 15 |
| 353 | Ararunão | Grass/Flying | 598 | DRILL_PECK (80) | 29 |
| 93 | Vampiro | Flying/Dark | 555 | DRILL_PECK (80) | 25 |
| 162 | Urubu | Flying/Dark | 555 | GUST (40) | 19 |
| 164 | Coruja | Flying/Psychic | 554 | WING_ATTACK (60) | 24 |
| 95 | Tuiuiú | Flying/Water | 553 | DRILL_PECK (80) | 21 |
| 301 | Pombão | Flying/Poison | 553 | PECK (35) | 2 |
| 42 | Papagaião | Flying/Psychic | 552 | DRILL_PECK (80) | 13 |
| 83 | Aracari | Flying/Grass | 551 | DRILL_PECK (80) | 21 |
| 33 | Araracanga | Flying/Fire | 550 | DRILL_PECK (80) | 9 |
| 20 | Sacizinho | Dark/Flying | 461 | GUST (40) | 21 |
| 96 | Colhereiro | Flying/Fairy | 449 | GUST (40) | 19 |
| 159 | Urutau | Flying/Ghost | 449 | WING_ATTACK (60) | 29 |
| 170 | Curió | Flying/Normal | 449 | AERIAL_ACE (60) | 29 |
| 173 | Choca | Flying/Normal | 449 | WING_ATTACK (60) | 19 |
| 302 | Baratão | Bug/Flying | 449 | GUST (40) | 2 |
| 349 | Aracuã | Flying/Normal | 449 | AERIAL_ACE (60) | 29 |
| 156 | Beija-flor | Flying/Fairy | 448 | WING_ATTACK (60) | 29 |
| 167 | Seriema | Flying/Fighting | 448 | WING_ATTACK (60) | 24 |
| 175 | João-de-Barro | Flying/Ground | 448 | GUST (40) | 19 |
| 84 | Curicaca | Flying/Normal | 447 | WING_ATTACK (60) | 21 |
| 106 | Cangaço | Dark/Flying | 447 | GUST (40) | 19 |
| 125 | Aruanã | Water/Flying | 447 | GUST (40) | 19 |
| 150 | Vespão | Bug/Flying | 447 | WING_ATTACK (60) | 29 |
| 158 | Bem-te-vi | Flying/Normal | 447 | WING_ATTACK (60) | 19 |
| 161 | Gavião | Flying/Fighting | 447 | WING_ATTACK (60) | 24 |
| 169 | Trinca-Ferro | Flying/Steel | 447 | PECK (35) | 2 |
| 172 | Papa-Formiga | Flying/Bug | 447 | WING_ATTACK (60) | 29 |
| 323 | Aluminio | Steel/Flying | 447 | GUST (40) | 19 |
| 75 | Abelhinha | Bug/Flying | 446 | GUST (40) | 19 |
| 166 | Ema | Normal/Flying | 446 | WING_ATTACK (60) | 26 |
| 174 | Bacurau | Flying/Dark | 446 | GUST (40) | 15 |
| 317 | Sacolim | Poison/Flying | 446 | WING_ATTACK (60) | 29 |
| 157 | Sabiá | Flying/Normal | 445 | WING_ATTACK (60) | 19 |
| 160 | Carcará | Flying/Dark | 445 | GUST (40) | 15 |
| 168 | Anú | Flying/Dark | 445 | GUST (40) | 19 |
| 171 | Sanhaço | Flying/Fairy | 445 | WING_ATTACK (60) | 29 |
| 311 | Fumacento | Poison/Flying | 445 | GUST (40) | 19 |
| 165 | Jaburu | Flying/Water | 444 | GUST (40) | 15 |
| 319 | Netzero | Flying/Poison | 444 | GUST (40) | 15 |
| 352 | Periquitão | Grass/Flying | 439 | PECK (35) | 22 |
| 13 | Tucanhão | Flying/Grass | 437 | GUST (40) | 15 |
| 41 | Papagaio | Flying/Psychic | 406 | DRILL_PECK (80) | 18 |
| 32 | Arará | Flying/Fire | 405 | DRILL_PECK (80) | 14 |
| 92 | Morcego | Flying/Psychic | 404 | GUST (40) | 2 |
| 361 | Beija-Flor | Fairy/Flying | 377 | WING_ATTACK (60) | 24 |
| 82 | Tuquinho | Flying | 287 | DRILL_PECK (80) | 33 |
| 40 | Papaguim | Flying | 285 | DRILL_PECK (80) | 33 |
| 31 | Ararinha | Flying | 284 | DRILL_PECK (80) | 28 |
| 163 | Corurupim | Flying/Psychic | 284 | WING_ATTACK (60) | 26 |
| 91 | Morcim | Flying | 283 | WING_ATTACK (60) | 14 |
| 94 | Piuiuim | Flying | 283 | DRILL_PECK (80) | 33 |
| 300 | Pombim | Flying/Normal | 283 | GUST (40) | 10 |

Fora por pouco — sao do tipo, mas o primeiro golpe ofensivo
daquele tipo so chega depois do teto:

| dex | nome | tipos | BST | primeiro STAB ofensivo |
|---:|---|---|---:|---|
| 139 | Cigarrão | Bug/Flying | 553 | GUST no nv34 |

## Cec&Caet — PSYCHIC, ate nv42

29 das 32 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 265 | Preto-Velho | Ghost/Psychic | 604 | PSYBEAM (65) | 39 |
| 298 | Cristo | Fairy/Psychic | 604 | PSYCHIC (90) | 39 |
| 245 | Jaci | Fairy/Psychic | 603 | PSYBEAM (65) | 39 |
| 27 | Botogaláu | Water/Psychic | 555 | CONFUSION (50) | 36 |
| 63 | Pregarcanjo | Fighting/Psychic | 555 | CONFUSION (50) | 29 |
| 164 | Coruja | Flying/Psychic | 554 | PSYCHIC (90) | 39 |
| 208 | Boneco | Ground/Psychic | 554 | CONFUSION (50) | 34 |
| 42 | Papagaião | Flying/Psychic | 552 | PSYCHIC (90) | 29 |
| 141 | Louvadeus | Bug/Psychic | 552 | PSYBEAM (65) | 42 |
| 199 | Ametista | Rock/Psychic | 552 | CONFUSION (50) | 9 |
| 221 | Polvão | Water/Psychic | 552 | PSYBEAM (65) | 34 |
| 39 | Bicho-Preguiça | Grass/Psychic | 551 | DREAM_EATER (100) | 34 |
| 360 | Preguiçoso | Grass/Psychic | 520 | CONFUSION (50) | 29 |
| 372 | Cordelim | Psychic/Fairy | 485 | PSYBEAM (65) | 34 |
| 247 | Rudá | Fairy/Psychic | 449 | PSYBEAM (65) | 39 |
| 305 | Gato-Preto | Dark/Psychic | 449 | PSYBEAM (65) | 34 |
| 90 | Camaleão | Normal/Psychic | 448 | PSYBEAM (65) | 37 |
| 307 | Lagartixa | Normal/Psychic | 448 | PSYBEAM (65) | 37 |
| 235 | Cuca | Dark/Psychic | 447 | PSYBEAM (65) | 39 |
| 326 | Sinal | Electric/Psychic | 447 | PSYBEAM (65) | 34 |
| 226 | Golfinho | Water/Psychic | 445 | CONFUSION (50) | 34 |
| 270 | Beata | Fairy/Psychic | 445 | PSYBEAM (65) | 39 |
| 308 | Traça-Papel | Bug/Psychic | 444 | PSYBEAM (65) | 34 |
| 38 | Preguicão | Grass/Psychic | 406 | PSYBEAM (65) | 35 |
| 41 | Papagaio | Flying/Psychic | 406 | CONFUSION (50) | 26 |
| 26 | Botão | Water/Psychic | 404 | PSYBEAM (65) | 39 |
| 92 | Morcego | Flying/Psychic | 404 | PSYCHIC (90) | 35 |
| 163 | Corurupim | Flying/Psychic | 284 | PSYCHIC (90) | 39 |
| 220 | Polvim | Water/Psychic | 282 | PSYCHIC (90) | 33 |

Fora por pouco — sao do tipo, mas o primeiro golpe ofensivo
daquele tipo so chega depois do teto:

| dex | nome | tipos | BST | primeiro STAB ofensivo |
|---:|---|---|---:|---|
| 212 | Meteorito | Rock/Psychic | 603 | FUTURE_SIGHT no nv58 |
| 15 | Micuiras | Normal/Psychic | 468 | PSYCHIC no nv46 |
| 135 | Acará | Water/Psychic | 445 | FUTURE_SIGHT no nv58 |

## Celina — WATER, ate nv46

82 das 83 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 280 | Sucuriaçu | Water/Dragon | 607 | SURF (95) | 44 |
| 283 | Terolibra-Rainha | Water/Bug | 607 | SURF (95) | 44 |
| 291 | Cobra-Norato | Water/Dragon | 607 | SURF (95) | 42 |
| 109 | Oxum | Water/Fairy | 606 | WATER_PULSE (60) | 44 |
| 293 | Ipupiara | Water/Dark | 605 | WATER_PULSE (60) | 44 |
| 108 | Iemanjá | Water/Fairy | 604 | BUBBLE (20) | 2 |
| 281 | Pirarumbá | Water/Dragon | 603 | SURF (95) | 44 |
| 286 | Iara-Mãe | Water/Fairy | 602 | SURF (95) | 44 |
| 27 | Botogaláu | Water/Psychic | 555 | HYDRO_PUMP (120) | 14 |
| 60 | Mandubé | Water/Dark | 555 | BUBBLE_BEAM (65) | 2 |
| 217 | Guaiamum | Water/Ground | 555 | HYDRO_PUMP (120) | 29 |
| 225 | Tartaruga | Water/Rock | 555 | BUBBLE_BEAM (65) | 24 |
| 95 | Tuiuiú | Flying/Water | 553 | BUBBLE_BEAM (65) | 42 |
| 56 | Peixeboi | Water | 552 | HYDRO_PUMP (120) | 29 |
| 122 | Pirarucu | Water/Dragon | 552 | HYDRO_PUMP (120) | 29 |
| 221 | Polvão | Water/Psychic | 552 | WATER_GUN (40) | 10 |
| 229 | Tubarão | Water/Dark | 552 | WATER_PULSE (60) | 44 |
| 36 | Jacarodon | Water/Dragon | 551 | BUBBLE_BEAM (65) | 42 |
| 105 | Caboclo | Water/Fighting | 551 | HYDRO_PUMP (120) | 25 |
| 44 | Anta | Normal/Water | 550 | SURF (95) | 46 |
| 19 | Iaraço | Water/Fairy | 548 | SURF (95) | 42 |
| 355 | Capivarão | Normal/Water | 510 | SURF (95) | 46 |
| 374 | Escamoso | Water/Dark | 498 | SURF (95) | 39 |
| 364 | Sarará | Fairy/Water | 472 | SURF (95) | 44 |
| 126 | Poraquê | Electric/Water | 449 | SURF (95) | 44 |
| 129 | Dourado | Water/Fighting | 449 | WATER_GUN (40) | 10 |
| 181 | Vitóriarégia | Grass/Water | 449 | SURF (95) | 44 |
| 57 | Mãe-d'Água | Water/Fairy | 448 | SURF (95) | 44 |
| 123 | Piranha | Water/Dark | 448 | WATER_PULSE (60) | 44 |
| 131 | Pacu | Water/Grass | 448 | BUBBLE_BEAM (65) | 24 |
| 134 | Cascudo | Water/Rock | 448 | BUBBLE_BEAM (65) | 24 |
| 186 | Buriti | Grass/Water | 448 | BUBBLE_BEAM (65) | 29 |
| 219 | Camarão | Water | 448 | HYDRO_PUMP (120) | 39 |
| 222 | Águaviva | Water/Poison | 448 | BUBBLE_BEAM (65) | 38 |
| 230 | Arraia | Water/Electric | 448 | HYDRO_PUMP (120) | 25 |
| 233 | Pescadão | Water/Dark | 448 | WATER_PULSE (60) | 44 |
| 310 | Ferrugem | Steel/Water | 448 | BUBBLE_BEAM (65) | 34 |
| 318 | Garrafão | Water/Poison | 448 | BUBBLE_BEAM (65) | 19 |
| 125 | Aruanã | Water/Flying | 447 | SURF (95) | 44 |
| 128 | Traíra | Water/Dark | 447 | WATER_PULSE (60) | 44 |
| 205 | Salitre | Rock/Water | 447 | BUBBLE_BEAM (65) | 29 |
| 227 | Baleia | Water/Normal | 447 | BUBBLE (20) | 2 |
| 312 | Óleoso | Poison/Water | 447 | BUBBLE_BEAM (65) | 29 |
| 45 | Antaraú | Normal/Water | 446 | BUBBLE_BEAM (65) | 32 |
| 130 | Tucunaré | Water/Dark | 446 | WATER_PULSE (60) | 44 |
| 133 | Piau | Water/Normal | 446 | BUBBLE (20) | 2 |
| 144 | Caramulão | Bug/Water | 446 | BUBBLE_BEAM (65) | 29 |
| 218 | Siri | Water/Fighting | 446 | WATER_GUN (40) | 10 |
| 232 | Pargo | Water/Fire | 446 | WATER_GUN (40) | 10 |
| 306 | Perereca | Water/Poison | 446 | BUBBLE_BEAM (65) | 24 |
| 124 | Tambaqui | Water/Normal | 445 | BUBBLE (20) | 2 |
| 127 | Curimbatá | Water/Ground | 445 | WATER_PULSE (60) | 44 |
| 135 | Acará | Water/Psychic | 445 | BUBBLE_BEAM (65) | 24 |
| 179 | Bromelinha | Grass/Water | 445 | SURF (95) | 44 |
| 193 | Mate | Grass/Water | 445 | BUBBLE_BEAM (65) | 29 |
| 223 | Cavalim-Marinho | Water/Fairy | 445 | WATER_PULSE (60) | 44 |
| 226 | Golfinho | Water/Psychic | 445 | HYDRO_PUMP (120) | 29 |
| 248 | Aluá | Water/Poison | 445 | WATER_GUN (40) | 10 |
| 256 | Iemanjá-Pequena | Water/Fairy | 445 | WATER_PULSE (60) | 44 |
| 267 | Marinheiro | Water/Dark | 445 | WATER_PULSE (60) | 44 |
| 325 | Bueiro | Water/Dark | 445 | WATER_PULSE (60) | 44 |
| 132 | Matrinxã | Water/Normal | 444 | WATER_GUN (40) | 10 |
| 165 | Jaburu | Flying/Water | 444 | SURF (95) | 44 |
| 209 | Estalactite | Rock/Water | 444 | SURF (95) | 44 |
| 231 | Peixe-Espada | Water/Steel | 444 | BUBBLE_BEAM (65) | 29 |
| 253 | Yara-Pindá | Water/Fairy | 444 | WATER_PULSE (60) | 44 |
| 35 | Jacarão | Water/Dark | 405 | SURF (95) | 18 |
| 26 | Botão | Water/Psychic | 404 | HYDRO_PUMP (120) | 22 |
| 59 | Mandí | Water/Poison | 404 | SURF (95) | 18 |
| 86 | Sapão | Water/Poison | 403 | HYDRO_PUMP (120) | 18 |
| 375 | Piranhita | Water/Dark | 395 | SURF (95) | 44 |
| 12 | Capivim | Water/Normal | 360 | SURF (95) | 42 |
| 85 | Sapim | Water | 287 | HYDRO_PUMP (120) | 33 |
| 104 | Cabocim | Water | 287 | HYDRO_PUMP (120) | 37 |
| 228 | Tubarim | Water/Dark | 287 | HYDRO_PUMP (120) | 42 |
| 216 | Caranguim | Water | 285 | HYDRO_PUMP (120) | 37 |
| 224 | Tartaruguim | Water | 285 | HYDRO_PUMP (120) | 37 |
| 34 | Jacarim | Water | 284 | HYDRO_PUMP (120) | 33 |
| 25 | Botim | Water | 283 | HYDRO_PUMP (120) | 37 |
| 58 | Mandim | Water | 283 | HYDRO_PUMP (120) | 37 |
| 55 | Peixim | Water | 282 | HYDRO_PUMP (120) | 33 |
| 121 | Pirarim | Water | 282 | HYDRO_PUMP (120) | 37 |

Fora por pouco — sao do tipo, mas o primeiro golpe ofensivo
daquele tipo so chega depois do teto:

| dex | nome | tipos | BST | primeiro STAB ofensivo |
|---:|---|---|---:|---|
| 220 | Polvim | Water/Psychic | 282 | **nunca — nao existe no learnset** |

## Sidney — DARK, ate nv49

56 das 56 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 288 | Saci-Rei | Dark/Fairy | 606 | CRUNCH (80) | 48 |
| 260 | Sacipererê | Dark/Fairy | 605 | FAINT_ATTACK (60) | 29 |
| 279 | Onçuma | Dark/Ghost | 605 | BITE (60) | 19 |
| 293 | Ipupiara | Water/Dark | 605 | BITE (60) | 24 |
| 243 | Jurupari | Dark/Fairy | 604 | BITE (60) | 19 |
| 60 | Mandubé | Water/Dark | 555 | BITE (60) | 38 |
| 93 | Vampiro | Flying/Dark | 555 | BITE (60) | 42 |
| 162 | Urubu | Flying/Dark | 555 | PURSUIT (40) | 15 |
| 68 | Gato-do-mato | Normal/Dark | 554 | BITE (60) | 42 |
| 89 | Teiú | Normal/Dark | 552 | FAINT_ATTACK (60) | 42 |
| 119 | Cascavão | Poison/Dark | 552 | BITE (60) | 42 |
| 229 | Tubarão | Water/Dark | 552 | BITE (60) | 24 |
| 80 | Cangambá | Poison/Dark | 551 | BITE (60) | 42 |
| 314 | Chorume | Poison/Dark | 551 | BITE (60) | 19 |
| 77 | Quati | Normal/Dark | 550 | BITE (60) | 42 |
| 143 | Escorpião | Poison/Dark | 550 | BITE (60) | 42 |
| 23 | Onçaléu | Dark | 524 | CRUNCH (80) | 34 |
| 374 | Escamoso | Water/Dark | 498 | CRUNCH (80) | 44 |
| 20 | Sacizinho | Dark/Flying | 461 | FAINT_ATTACK (60) | 32 |
| 236 | Bicho-Papão | Dark/Ghost | 449 | BITE (60) | 19 |
| 269 | Cangaceiro | Dark/Fighting | 449 | CRUNCH (80) | 44 |
| 305 | Gato-Preto | Dark/Psychic | 449 | CRUNCH (80) | 44 |
| 123 | Piranha | Water/Dark | 448 | BITE (60) | 24 |
| 189 | Açaí | Grass/Dark | 448 | BITE (60) | 24 |
| 233 | Pescadão | Water/Dark | 448 | BITE (60) | 24 |
| 263 | Pomba-Gira | Dark/Fairy | 448 | CRUNCH (80) | 48 |
| 299 | Ratão | Dark/Poison | 448 | CRUNCH (80) | 48 |
| 106 | Cangaço | Dark/Flying | 447 | FAINT_ATTACK (60) | 29 |
| 128 | Traíra | Water/Dark | 447 | BITE (60) | 24 |
| 235 | Cuca | Dark/Psychic | 447 | BITE (60) | 19 |
| 238 | Corpo-Seco | Ghost/Dark | 447 | PURSUIT (40) | 15 |
| 249 | Jenipapo | Dark/Grass | 447 | BITE (60) | 19 |
| 304 | Cão-Bravo | Dark/Normal | 447 | BITE (60) | 15 |
| 78 | Coati | Dark/Ground | 446 | CRUNCH (80) | 48 |
| 130 | Tucunaré | Water/Dark | 446 | BITE (60) | 24 |
| 155 | Formigão-Preto | Bug/Dark | 446 | CRUNCH (80) | 44 |
| 174 | Bacurau | Flying/Dark | 446 | FAINT_ATTACK (60) | 29 |
| 276 | Maracatu | Dark/Fairy | 446 | CRUNCH (80) | 48 |
| 309 | Poeirão | Ground/Dark | 446 | BITE (60) | 24 |
| 328 | Grafiteiro | Dark/Fairy | 446 | BITE (60) | 19 |
| 350 | Bugio | Normal/Dark | 446 | CRUNCH (80) | 44 |
| 69 | Jaguatirica | Dark/Normal | 445 | BITE (60) | 21 |
| 72 | Paca | Normal/Dark | 445 | CRUNCH (80) | 47 |
| 146 | Barata | Bug/Dark | 445 | BITE (60) | 19 |
| 160 | Carcará | Flying/Dark | 445 | FAINT_ATTACK (60) | 29 |
| 168 | Anú | Flying/Dark | 445 | PURSUIT (40) | 15 |
| 204 | Manganim | Steel/Dark | 445 | BITE (60) | 24 |
| 237 | Lobisomem | Dark/Normal | 445 | CRUNCH (80) | 39 |
| 259 | Saciamigo | Dark/Fairy | 445 | BITE (60) | 19 |
| 267 | Marinheiro | Water/Dark | 445 | BITE (60) | 24 |
| 322 | Bugão | Bug/Dark | 445 | BITE (60) | 19 |
| 325 | Bueiro | Water/Dark | 445 | BITE (60) | 24 |
| 264 | Exu | Dark/Fighting | 444 | CRUNCH (80) | 44 |
| 35 | Jacarão | Water/Dark | 405 | CRUNCH (80) | 48 |
| 375 | Piranhita | Water/Dark | 395 | CRUNCH (80) | 48 |
| 228 | Tubarim | Water/Dark | 287 | FAINT_ATTACK (60) | 28 |

## Phoebe — GHOST, ate nv51

18 das 18 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 255 | Zumbi | Ghost/Fighting | 606 | SHADOW_BALL (80) | 39 |
| 279 | Onçuma | Dark/Ghost | 605 | SHADOW_BALL (80) | 48 |
| 265 | Preto-Velho | Ghost/Psychic | 604 | SHADOW_BALL (80) | 44 |
| 289 | Anhangaú | Ghost/Grass | 603 | SHADOW_BALL (80) | 44 |
| 99 | Mula-sem-Cabeça | Fire/Ghost | 550 | LICK (20) | 32 |
| 16 | Boitatá | Fire/Ghost | 514 | LICK (20) | 2 |
| 159 | Urutau | Flying/Ghost | 449 | SHADOW_BALL (80) | 39 |
| 236 | Bicho-Papão | Dark/Ghost | 449 | SHADOW_BALL (80) | 48 |
| 239 | Mão-Peluda | Ghost/Fighting | 449 | SHADOW_BALL (80) | 34 |
| 54 | Guaraflama | Fire/Ghost | 448 | NIGHT_SHADE (variavel) | 24 |
| 241 | Comadre | Ghost/Fairy | 448 | NIGHT_SHADE (variavel) | 29 |
| 252 | Anhangá-Pitã | Ghost/Fire | 448 | SHADOW_BALL (80) | 39 |
| 81 | Sarué | Poison/Ghost | 447 | SHADOW_BALL (80) | 48 |
| 238 | Corpo-Seco | Ghost/Dark | 447 | SHADOW_BALL (80) | 39 |
| 240 | Perna-Cabeluda | Ghost/Normal | 446 | SHADOW_BALL (80) | 32 |
| 254 | Pisadeira | Ghost/Fighting | 446 | SHADOW_BALL (80) | 34 |
| 234 | Loirinha | Ghost/Fairy | 445 | NIGHT_SHADE (variavel) | 29 |
| 242 | Anhangá | Ghost/Grass | 444 | SHADOW_BALL (80) | 44 |

## Glacia — STEEL, ate nv53

16 das 16 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 110 | Ogum | Steel/Fire | 602 | IRON_TAIL (100) | 37 |
| 30 | Tatuçu | Ground/Steel | 555 | METEOR_MASH (100) | 38 |
| 24 | Tamanduá | Ground/Steel | 470 | METEOR_MASH (100) | 44 |
| 203 | Bauxito | Steel/Ground | 449 | IRON_TAIL (100) | 34 |
| 316 | Latinha | Steel/Normal | 449 | STEEL_WING (70) | 38 |
| 324 | Concretim | Rock/Steel | 449 | IRON_TAIL (100) | 39 |
| 327 | Poste | Steel/Electric | 449 | IRON_TAIL (100) | 39 |
| 200 | Ouríço | Steel/Electric | 448 | IRON_TAIL (100) | 39 |
| 310 | Ferrugem | Steel/Water | 448 | IRON_TAIL (100) | 39 |
| 321 | Cabofio | Electric/Steel | 448 | IRON_TAIL (100) | 34 |
| 169 | Trinca-Ferro | Flying/Steel | 447 | IRON_TAIL (100) | 34 |
| 323 | Aluminio | Steel/Flying | 447 | METEOR_MASH (100) | 39 |
| 201 | Ferrolho | Steel/Ground | 445 | IRON_TAIL (100) | 34 |
| 204 | Manganim | Steel/Dark | 445 | IRON_TAIL (100) | 34 |
| 231 | Peixe-Espada | Water/Steel | 444 | IRON_TAIL (100) | 44 |
| 29 | Tatubola | Ground/Steel | 404 | METEOR_MASH (100) | 44 |

## Drake — DRAGON, ate nv55

10 das 11 especies do tipo. Ordenado por BST.

| dex | nome | tipos | BST | melhor golpe STAB no teto | nv |
|---:|---|---|---:|---|---:|
| 280 | Sucuriaçu | Water/Dragon | 607 | OUTRAGE (90) | 48 |
| 291 | Cobra-Norato | Water/Dragon | 607 | OUTRAGE (90) | 47 |
| 244 | Tupã | Electric/Dragon | 606 | OUTRAGE (90) | 48 |
| 285 | Boitatá-Puro | Fire/Dragon | 606 | TWISTER (40) | 2 |
| 100 | Corcovado | Rock/Dragon | 604 | OUTRAGE (90) | 53 |
| 281 | Pirarumbá | Water/Dragon | 603 | OUTRAGE (90) | 48 |
| 297 | Corcovado-Ancião | Rock/Dragon | 602 | OUTRAGE (90) | 48 |
| 122 | Pirarucu | Water/Dragon | 552 | DRAGON_BREATH (60) | 50 |
| 36 | Jacarodon | Water/Dragon | 551 | OUTRAGE (90) | 50 |
| 211 | Fóssil | Rock/Dragon | 448 | OUTRAGE (90) | 53 |

Fora por pouco — sao do tipo, mas o primeiro golpe ofensivo
daquele tipo so chega depois do teto:

| dex | nome | tipos | BST | primeiro STAB ofensivo |
|---:|---|---|---:|---|
| 282 | Draguará-Alfa | Fire/Dragon | 605 | **nunca — nao existe no learnset** |


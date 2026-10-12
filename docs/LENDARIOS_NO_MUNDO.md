# Os 20 lendários e míticos no mundo

Os 20 especiais que `docs/arauna/ESPECIAIS_ESTATICOS.csv` segurava sem encontro
agora estão no mundo, cada um com um encontro estático. O gate de
disponibilidade passa a contar 386 de 386, e a dex completa volta a pedir
#001–#384.

## Onde cada um está

A decisão de cada linha está em `docs/arauna/ARAUNA_LEGENDS.csv`. Os lugares
seguem a coluna `placement` do plano de especiais e o texto de dex de cada
criatura.

| Lugar | Dex | Nível | Mapa (x,y) |
|---|---|---|---|
| Torre Juramento, 1º andar | #329 Guaraciana | 60 | SkyPillar_1F (11,6) |
| Torre Juramento, 2º andar | #331 Tupanaú | 60 | SkyPillar_2F (11,9) |
| Torre Juramento, 3º andar | #343 Fogaréu | 60 | SkyPillar_3F (11,7) |
| Torre Juramento, 4º andar | #334 Yasy | 60 | SkyPillar_4F (11,9) |
| Torre Juramento, 5º andar | #333 Kuarahy | 60 | SkyPillar_5F (1,9) |
| Torre Juramento, praia da entrada | #348 Arauanamon | 68 | SkyPillar_Outside (10,10) |
| Estr. Juramento, B2F, à beira do lago | #337 Arauanaú | 62 | VictoryRoad_B2F (21,7) |
| Ruínas da Queda, gruta do fundo | #342 Terraão | 62 | MeteorFalls_StevensCave (15,23) |
| Serra da Cinza, beira da cratera | #340 Solzão | 58 | MtChimney (30,9) |
| Cavernas M'Boi, lago da última câmara | #336 Perybé | 60 | SeafloorCavern_Room9 (17,36) |
| Rota 120, lago sob a ponte | #332 Iaraú | 60 | Route120 (28,73) |
| Rota 120, clareira da mata | #338 Verdejante | 60 | Route120 (6,30) |
| Rota 124, banco de areia | #346 Poente | 60 | Route124 (60,40) |
| Rota 124, mar junto à casa da ilha | #344 Marulho | 60 | Route124 (66,47) |
| Rota 125, ilhota de pedra | #330 Jaciana | 60 | Route125 (48,28) |
| Rota 125, ilhota de areia | #339 Chuvão | 60 | Route125 (10,22) |
| Rota 122, mar diante da Memorial | #335 Rudarauna | 60 | Route122 (24,34) |
| Rota 113, campo de cinzas | #376 Boitatã | 65 | Route113 (35,9) |
| Rota 113, campo aberto a leste | #341 Ventania | 58 | Route113 (89,10) |
| Passagem Seca, câmara de areia | #385 Sacinho | 65 | DesertUnderpass (132,12) |

Os cinco celestes (sol, lua, trovão, fogo e a consorte de Guaraci) sobem a
Torre Juramento um andar por vez. Arauanamon, "a região inteira feita carne",
espera na praia da torre, e Curupixel continua no topo. Os espíritos da água
ficam onde há água: Perybé nas Cavernas M'Boi, Iaraú no lago da Rota 120,
Marulho, Chuvão, Jaciana, Poente e Rudarauna nas águas da Baía das Luzes.

Nenhuma casa é gargalo. Cada lugar foi escolhido fora de corredores, longe de
warps e fora de piso rachado, e o gate `check_overworld_registry.py` confere
isso a cada build, como já fazia com as 46 criaturas que andam pelo mapa.

## Quando aparecem

- **Antes do primeiro Hall da Fama** todos dormem. Na entrada de cada mapa,
  `AraunaLegends_OnTransition` marca a flag do lendário, e o objeto não aparece.
  Isso mantém níveis de 58 a 68 fora da campanha principal; o Campeão tem 58.
- **No Hall da Fama** `AraunaLegends_Reawaken` acorda todos os que o jogador
  ainda não capturou.
- **Fugir** deixa o lendário onde está.
- **Capturar** tira o objeto antes de a tela voltar, como nas câmaras dos Regis.
- **Derrotar** faz a presença sumir com a mensagem "Perhaps it will return
  after another victory at the LEAGUE." Ela volta no Hall da Fama seguinte.
  Nenhuma espécie se perde.

As 20 flags são `FLAG_UNUSED_0x020`–`0x033`, que o vanilla nunca usou. O save
não muda de forma.

## Como o jogador descobre

Depois do Hall da Fama, na cena em que recebe a dex nacional, ANAHI comenta
que o sensor de Vínculo da bancada "went wild" e que são vinte sinais. O
sensor, ao lado dela, passa a ler quantos lendários ainda estão no mundo,
agrupados pelo nome do lugar no mapa da região:

> It counts 20 BOND signals still out in ARAUNA: TORRE JURAMENTO: 6,
> ESTR. JURAMENTO: 1, RUINAS DA QUEDA: 1…

Com todos capturados, ele diz que todos os sinais foram respondidos. Antes do
Hall da Fama ele mostra só o texto de sempre.

## A arte

Cada lendário usa o próprio sprite de batalha, parado, em 64×64: o mesmo tamanho
dos lendários grandes do Emerald e a mesma figura que aparece na batalha.
Nenhum desenho novo foi inventado. O registry de overworlds ganhou o formato
`64s` (parado, uma pose) ao lado de `64` (anda) e `32` (Regis). As 20 folhas
ficam em `graphics/object_events/pics/pokemon/arauna/<dex>_<slug>.png`; uma
arte dedicada pode substituir qualquer uma com o mesmo nome.

Um lendário parado sobre a água não ganha reflexo. O reflexo de um sprite de
64 px aparecia quatro casas abaixo, como uma segunda criatura.

A batalha usa `StartRegiBattle`: a transição de lendário e a música "Força
Primordial" (`MUS_ARAUNA_LEGEND_BATTLE`), como os outros encontros estáticos.

## Ferramentas

- `tools/arauna/build_legends.py --write` gera tudo a partir do CSV: folhas e
  paletas, linhas do registry, tags de paleta, flags, objetos nos mapas (sempre
  acrescentados no fim), a tabela `src/data/arauna_legends.h` e os scripts em
  `data/scripts/arauna_legends.inc`. Depois dele, rode
  `tools/arauna/build_overworld_registry.py --write`.
- `src/arauna_legends.c` lê a tabela: dormir, acordar, sumir na captura, sensor.
- O gate do registry agora conta as 66 linhas do manifesto, em vez de 46 fixas,
  e passa os 20 lendários pelos mesmos testes de casa das outras criaturas.
- O gate de disponibilidade encontra os `setwildbattle` novos sozinho.

## Testes no mGBA

Com scripts ligados, numa ROM de harness destes fontes:

| Verificação | Resultado |
|---|---|
| Os 20 depois do Hall da Fama | todos visíveis no lugar (prancha de imagens) |
| Guaraciana antes do Hall da Fama | não aparece; flag marcada |
| Tupanaú contra Quati nv. 100 | texto, grito, transição, batalha, "Wild Tupanaú fainted!", "The presence faded away…"; some do mapa |
| Yasy com Master Ball | "Gotcha!", página da Pokédex, apelido recusado; de volta ao mapa, Yasy já não está |
| Guaraciana, fugir | "Got away safely!"; continua no lugar |
| Flag marcada e Hall da Fama | acorda de novo |
| Tudo capturado e Hall da Fama | continua fora |
| Sensor depois do Hall da Fama | 20 sinais por lugar; com tudo capturado, "Every BOND signal it ever caught has been answered." |
| Cena da dex nacional | a fala nova de ANAHI aparece depois do upgrade |
| ANAHI com #001–#384 | "complete!"; faltando #329, "very close to complete" |
| Iaraú no lago | um só, sem reflexo duplicado |
| Arauanaú no B2F escuro | visível com Flash |

A ROM compila sem avisos novos e os gates passam.

## Aviso ao autor

33 arquivos que os contratos congelam mudaram, e 46 arquivos novos
entraram. `validate_connections_08f.py` agora para em `data/event_scripts.s`,
o primeiro deles que ele confere. As folhas e paletas novas vêm do sprite de
batalha de cada criatura; os mapas só ganharam objetos no fim da lista de
`object_events`, sem renumerar nenhum.

| Arquivo | SHA-256 |
|---|---|
| `data/event_scripts.s` | `a328a46d8aabdf5f3be5bc97018b2dcbee718b5d0253d563596118078f361067` |
| `data/maps/DesertUnderpass/map.json` | `14a3f870c031d5fc2fe1dfc319e2355d21a5f3b31b93512ab0429d5f9ab4b202` |
| `data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc` | `8ceffbacefd19041d4576532c2c88f1a8b560b3db40a90824eeded2554a6b5f3` |
| `data/maps/MeteorFalls_StevensCave/map.json` | `15ad579cc64f6c845e2502d883c97cf0b2fd768de990d4e5d460544e6b245c77` |
| `data/maps/MtChimney/map.json` | `e52ee77acfbb40c5e4d79c2e75cb955a8c798b6e2e1a8b79b9bbd006c3717ec6` |
| `data/maps/Route113/map.json` | `9f1ea0c4e3b9996f086acea2a42027276b400246db912a48c2656d4553cb6688` |
| `data/maps/Route120/map.json` | `a8f4214face696bb7af6484cd33ff45600a5531339cb5abffd0666596e9d45c6` |
| `data/maps/Route122/map.json` | `c430e6fbe9de813db93fda3351306df20593f1e22f0637946fb4822b21f6e757` |
| `data/maps/Route124/map.json` | `9fc70d6de99db5baf859a032dada36e6144119aa198972b30bb2c8243fab663d` |
| `data/maps/Route125/map.json` | `351d408b7eea157696aaf061280f641065c47d9823118bb2b336fc5220780e7d` |
| `data/maps/SeafloorCavern_Room9/map.json` | `8a235f5bc7c2a92546121e71dc54bdc9b1615a151ee1bd4704f1159acb9c6074` |
| `data/maps/SkyPillar_1F/map.json` | `0fc4ee9e79c1203616e7ce172e739123c4f21bf719d03144178bca46e72dfe13` |
| `data/maps/SkyPillar_2F/map.json` | `a2c645234c4af18a1d4bf654d33b5aea6a7b90e4f3a79425a4cefe652f4ae81b` |
| `data/maps/SkyPillar_3F/map.json` | `a30d76aba150ce0db16adfcce63e40c33ad69e06d70af0c97ea60d2806eaac3f` |
| `data/maps/SkyPillar_4F/map.json` | `d67c81ab558a1fae5d2860e6d2788a212f460d7c793f848dfee05944259a01e1` |
| `data/maps/SkyPillar_5F/map.json` | `31b119a26260a30daac1d72a448b5a8872d179022a168ccdb20bbbe2ad731c1c` |
| `data/maps/SkyPillar_Outside/map.json` | `a34dcd0e901bc6300eb7e06b35e98de6b99ad308407bca600b962213a2bd5eb7` |
| `data/maps/VictoryRoad_B2F/map.json` | `e0198361e2c75a1976c73d81cc44ab4b80a7bc6c4763c045880c2054a880e4f9` |
| `data/scripts/hall_of_fame.inc` | `20f5ce6567889ab49b446a16115830be81fe7c8f379cf08514b34f47356acd6c` |
| `data/specials.inc` | `41731674fb7aec8251ebb482279ec7e38aecc1e1f2952ef794112c4910b3d373` |
| `docs/EVENTOS_LENDARIOS.md` | `12213cfbb7120dd7134541b36b35bcd79842996b226783c1da60560337540051` |
| `docs/arauna/ARAUNA_OVERWORLD_46.csv` | `c5ab1a73c774966e2bdf6a172dd01baeb2789fbb8d58db71d1f700da0a460cfe` |
| `docs/arauna/DEX_PORT.md` | `ba04ec73425e7486983db5dd778f6e7864770c1ec1a1c69e91977fcd0ab7ba3e` |
| `docs/arauna/OVERWORLD_REGISTRY.md` | `2c01ab628663f703be697002e918e0980fea8c617296e722a7646eb987d7b816` |
| `include/constants/arauna_overworld.h` | `d5d615d24f1d5e3554610610e9c07fdeefc392670df808b4347178895911704b` |
| `include/constants/flags.h` | `d50b71d5b9d655d499e680f45e458c90f7ecd4e2d8142399fb147aa99b0530ea` |
| `src/data/object_events/arauna_overworld.h` | `b37e30343f6ce7f95d144753a9494d2135b4a1363d8d9c757b0158a3b51fc089` |
| `src/data/object_events/object_event_graphics.h` | `6b114d986e090c614bde01590c4cf999b3bdd1a338c525e0b457049e47a3ffa3` |
| `src/data/object_events/object_event_pic_tables.h` | `751152bfc1887c037a47556828e1bad254eb29f80c6e391ed26e84759dfbba9c` |
| `src/event_object_movement.c` | `8c96760a8f413e9b9b10a6f34032ef285d529154792deb48f8153deec629ca2d` |
| `src/script.c` | `9467a089e2839b407272e626478b587f1c90ffa820069b3e4fabd4c455aeffca` |
| `tools/arauna/build_overworld_registry.py` | `9253a055ac6c3093a30a08f401ba70c1c465b7bb310e7a1a364aa4cb7f2ca941` |
| `tools/arauna/check_overworld_registry.py` | `0161fa5cee7acdf409b78ffec84c0cb52d9e4a7bc904a1a014ba5c057cfd41ac` |
| `src/data/pokemon/dex_completion_held_back.h` | `a59ca785f82362612ae9ce9c0fd22d59078bba736968436fd27f8c9e96c237ff` |
| `data/scripts/arauna_legends.inc` (novo) | `26dd6dfee1cbcd0af09b304c47b44f5c942415523d1e508c7da732c40797c8fe` |
| `docs/arauna/ARAUNA_LEGENDS.csv` (novo) | `792cabec770bcd4ed627f62be2858d023038ecdf8c08ad91314d5634dd325f04` |
| `graphics/object_events/palettes/arauna_329_guaraciana.pal` (novo) | `2398cadc2e2f4f308210e23e5a0f3fa3497e4681d4c5e42a46a7d6f1ab919898` |
| `graphics/object_events/palettes/arauna_330_jaciana.pal` (novo) | `4c0276652c56d91ebbdc4be82c2172036693a3f87915d4f59e8a7e60d0de1ce0` |
| `graphics/object_events/palettes/arauna_331_tupanau.pal` (novo) | `58fd8671a56940a49542b05d53c9c71350418b66348fb6179d42e93e5f4d2855` |
| `graphics/object_events/palettes/arauna_332_iarau.pal` (novo) | `59b5055a98952db72e7dee020f4a898bb3bb1aff446aff1a9f24000b95b301f9` |
| `graphics/object_events/palettes/arauna_333_kuarahy.pal` (novo) | `dd5b5c1a2d942da8560148405cfef8174b15bd8f19f5b6c8511c81da62b6c45f` |
| `graphics/object_events/palettes/arauna_334_yasy.pal` (novo) | `889ce7bdb85cd8065292dc02bb8bc01608f518f3c4f971bda59d1b74d6a2aab5` |
| `graphics/object_events/palettes/arauna_335_rudarauna.pal` (novo) | `bc3854ebb690fe4334ba833ae66176ce3a10d1d40d250f699b83356167218bf5` |
| `graphics/object_events/palettes/arauna_336_perybe.pal` (novo) | `9e1bf836ace4773f24cc24b6b8e2cada21c320b86dccd4128ea77dcb0f9ba141` |
| `graphics/object_events/palettes/arauna_337_arauanau.pal` (novo) | `6648c724ec96485c6cb2aa7999ffd06736a12a915c92119096eceba5dd3fd066` |
| `graphics/object_events/palettes/arauna_338_verdejante.pal` (novo) | `f1af807715e53d27e8bc36090e4825f100d2a7d616c24fbf1136cbc7aa5d5bb2` |
| `graphics/object_events/palettes/arauna_339_chuvao.pal` (novo) | `fd88428696ff2216c98d77d043157451e7f43120d7c9eccd6b7faa9ab5c23602` |
| `graphics/object_events/palettes/arauna_340_solzao.pal` (novo) | `94f17c7ba260d2dc7a142d187fddfeec20f08f75c7e1b6520c62bd0e03a59ac4` |
| `graphics/object_events/palettes/arauna_341_ventania.pal` (novo) | `92c6c397e9e108c7c93f84f2e2b664c341694cc0865933a4a003db923679876f` |
| `graphics/object_events/palettes/arauna_342_terraao.pal` (novo) | `0387b0fdad5362031f8e8204d33e25ea90d615561e430e05ecf471dfc8d78843` |
| `graphics/object_events/palettes/arauna_343_fogareu.pal` (novo) | `e34eb2c5e8b2cfccd526a6a915084b659e9949a834f898fd51d6d92d1769d5d4` |
| `graphics/object_events/palettes/arauna_344_marulho.pal` (novo) | `0b329544538e6cb31c511775e7dd5047eb0dfc03a5cb955241e4b436a82ac835` |
| `graphics/object_events/palettes/arauna_346_poente.pal` (novo) | `aef888892d85de84ee77a2714c573e3e4b2fb32df200194f5a195f5761ca9e28` |
| `graphics/object_events/palettes/arauna_348_arauanamon.pal` (novo) | `5338f8e50277227e7c2e3423a7295fb7e9bd2df96ded78c8adad39395f2741d7` |
| `graphics/object_events/palettes/arauna_376_boitata.pal` (novo) | `f9356f294ed1cc10b973bc13739c78e6c3a494c1a4981d1040550aacd3e9cb11` |
| `graphics/object_events/palettes/arauna_385_sacinho.pal` (novo) | `426c751cf8991742969dfa0b742755431046d1952276b3aff4fb91ec447d72e6` |
| `graphics/object_events/pics/pokemon/arauna/329_guaraciana.png` (novo) | `5981f8ab77b6f5f2b405f665e57cf64044cd46cb86eb608d125047f918ac0929` |
| `graphics/object_events/pics/pokemon/arauna/330_jaciana.png` (novo) | `e40417562b952dcf827b9c0944c2e07b0ecbfb2ba7e0ae9a4607e27661695924` |
| `graphics/object_events/pics/pokemon/arauna/331_tupanau.png` (novo) | `96f7f63621a9e11915215430036926fc502276d94fd441f530288631f341e5ec` |
| `graphics/object_events/pics/pokemon/arauna/332_iarau.png` (novo) | `0cca5851efad4f1b6b3279a41ff25ccf611679205f13f3cebcceb6e25e8a78ec` |
| `graphics/object_events/pics/pokemon/arauna/333_kuarahy.png` (novo) | `ca77f7942f813b78802ace86334ce5ac58dde0309a3c832e37739f1eea878d04` |
| `graphics/object_events/pics/pokemon/arauna/334_yasy.png` (novo) | `b13f1a4ccd8d13109e089e02d1b2297906109d45621f7095d22707e523741ab8` |
| `graphics/object_events/pics/pokemon/arauna/335_rudarauna.png` (novo) | `f8d40387eb8006a75ae678a3b15f47f49bbfae8cb1dc128a5539f3e849b93488` |
| `graphics/object_events/pics/pokemon/arauna/336_perybe.png` (novo) | `d9b9ed6a080273da40c9f842b57293182df2334cd151350f18550fbbb6a51f91` |
| `graphics/object_events/pics/pokemon/arauna/337_arauanau.png` (novo) | `28da525c7e2deb1f511f4686ee0ec0e40684233214b8c052b382ab43480a714f` |
| `graphics/object_events/pics/pokemon/arauna/338_verdejante.png` (novo) | `357427ea9ef11b28ce7040d0cc085020c33aa76d5d62a0f1f79c3ee73a7e3453` |
| `graphics/object_events/pics/pokemon/arauna/339_chuvao.png` (novo) | `2312e0fee37c5a91462812790a7bc57aebbc6ce5c2f8b0d181e4bb2a3d2d6535` |
| `graphics/object_events/pics/pokemon/arauna/340_solzao.png` (novo) | `6b65513cc80ea42d22644fb6d0c1f82ddd8b622a08f8d332c9d65225e4db9a8a` |
| `graphics/object_events/pics/pokemon/arauna/341_ventania.png` (novo) | `c3d8dfdde8bc4e2dd3cd4e1b3e510f5cf7b34bdfa6127a31e717bb8843f97731` |
| `graphics/object_events/pics/pokemon/arauna/342_terraao.png` (novo) | `e84dfa9fd6842541e0a2ec70159851e766f7b4395088b361fb501062baca8d74` |
| `graphics/object_events/pics/pokemon/arauna/343_fogareu.png` (novo) | `2b66785f19bbf4bec01c75572a16141063c742dbf5baa332bd2009e356a4d26c` |
| `graphics/object_events/pics/pokemon/arauna/344_marulho.png` (novo) | `53a3c6a97c1cdc672b190323d0cc6ad44b044e5e015db6cb4bdf3389bb97da49` |
| `graphics/object_events/pics/pokemon/arauna/346_poente.png` (novo) | `2fec55b87bb24832b76bf731650758bb860f9c16b87d4fb51df0b9f58f5d18b8` |
| `graphics/object_events/pics/pokemon/arauna/348_arauanamon.png` (novo) | `7b31476945ceb83ed300b19d03410e9263b77560adc0bdbb3746267b23f90e81` |
| `graphics/object_events/pics/pokemon/arauna/376_boitata.png` (novo) | `c1cb4cbe8a00dcce2847a4970f2f2c4d005d92159b15abf2debc51a8b4573129` |
| `graphics/object_events/pics/pokemon/arauna/385_sacinho.png` (novo) | `216724c784d166bfe213e55d2029fbad710a4fb2e2183dd16b21b721066f5260` |
| `include/arauna_legends.h` (novo) | `1aaeffe7f595de9aeb4c34ea049972f4a60c12eddb2d11ff94e4f004841c0878` |
| `src/arauna_legends.c` (novo) | `22d585db4ca3c8f1e01689b6078ab6bb968cbc9d7357ea7af7630a1b1a3cee45` |
| `src/data/arauna_legends.h` (novo) | `24fd3d30ab473f065ec62761c1c54db1b7d53f2619aa6a2844168035efc70954` |
| `tools/arauna/build_legends.py` (novo) | `dd5bbf003191221aa63ee41b120d6f1c671534e001088820f7616ad6bd14b632` |

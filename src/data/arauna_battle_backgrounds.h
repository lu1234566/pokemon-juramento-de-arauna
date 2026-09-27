// Native Arauna backgrounds. IDs match concepts.json.
//
// Declarado com INCGFX e nao com INCBIN de binario pronto, como o resto
// do repositorio: .gitignore ignora *.4bpp, *.gbapal e *.lz, e o alvo
// clean-assets do Makefile apaga esses tres em toda a arvore. Um pacote
// que trouxesse o binario compilado compilaria aqui e falharia em qualquer
// clone novo, e sumiria no primeiro make clean. As fontes versionadas sao
// tiles.png, map.bin e palette.pal; o build refaz o resto.
static const u32 sAraunaEntryTiles[] = INCGFX_U32("graphics/battle_environment/arauna/common/entry.png", ".4bpp.lz");
static const u32 sAraunaEntryMap[] = INCGFX_U32("graphics/battle_environment/arauna/common/entry_map.bin", ".lz");
static const u32 sAraunaTiles_R101[] = INCGFX_U32("graphics/battle_environment/arauna/r101/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R101[] = INCGFX_U32("graphics/battle_environment/arauna/r101/map.bin", ".lz");
static const u32 sAraunaPalette_R101[] = INCGFX_U32("graphics/battle_environment/arauna/r101/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R101 = {sAraunaTiles_R101, sAraunaMap_R101, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R101};
static const u32 sAraunaTiles_R102[] = INCGFX_U32("graphics/battle_environment/arauna/r102/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R102[] = INCGFX_U32("graphics/battle_environment/arauna/r102/map.bin", ".lz");
static const u32 sAraunaPalette_R102[] = INCGFX_U32("graphics/battle_environment/arauna/r102/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R102 = {sAraunaTiles_R102, sAraunaMap_R102, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R102};
static const u32 sAraunaTiles_R103[] = INCGFX_U32("graphics/battle_environment/arauna/r103/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R103[] = INCGFX_U32("graphics/battle_environment/arauna/r103/map.bin", ".lz");
static const u32 sAraunaPalette_R103[] = INCGFX_U32("graphics/battle_environment/arauna/r103/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R103 = {sAraunaTiles_R103, sAraunaMap_R103, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R103};
static const u32 sAraunaTiles_R104[] = INCGFX_U32("graphics/battle_environment/arauna/r104/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R104[] = INCGFX_U32("graphics/battle_environment/arauna/r104/map.bin", ".lz");
static const u32 sAraunaPalette_R104[] = INCGFX_U32("graphics/battle_environment/arauna/r104/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R104 = {sAraunaTiles_R104, sAraunaMap_R104, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R104};
static const u32 sAraunaTiles_R105[] = INCGFX_U32("graphics/battle_environment/arauna/r105/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R105[] = INCGFX_U32("graphics/battle_environment/arauna/r105/map.bin", ".lz");
static const u32 sAraunaPalette_R105[] = INCGFX_U32("graphics/battle_environment/arauna/r105/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R105 = {sAraunaTiles_R105, sAraunaMap_R105, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R105};
static const u32 sAraunaTiles_R106[] = INCGFX_U32("graphics/battle_environment/arauna/r106/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R106[] = INCGFX_U32("graphics/battle_environment/arauna/r106/map.bin", ".lz");
static const u32 sAraunaPalette_R106[] = INCGFX_U32("graphics/battle_environment/arauna/r106/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R106 = {sAraunaTiles_R106, sAraunaMap_R106, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R106};
static const u32 sAraunaTiles_R107[] = INCGFX_U32("graphics/battle_environment/arauna/r107/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R107[] = INCGFX_U32("graphics/battle_environment/arauna/r107/map.bin", ".lz");
static const u32 sAraunaPalette_R107[] = INCGFX_U32("graphics/battle_environment/arauna/r107/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R107 = {sAraunaTiles_R107, sAraunaMap_R107, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R107};
static const u32 sAraunaTiles_R108[] = INCGFX_U32("graphics/battle_environment/arauna/r108/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R108[] = INCGFX_U32("graphics/battle_environment/arauna/r108/map.bin", ".lz");
static const u32 sAraunaPalette_R108[] = INCGFX_U32("graphics/battle_environment/arauna/r108/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R108 = {sAraunaTiles_R108, sAraunaMap_R108, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R108};
static const u32 sAraunaTiles_R109[] = INCGFX_U32("graphics/battle_environment/arauna/r109/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R109[] = INCGFX_U32("graphics/battle_environment/arauna/r109/map.bin", ".lz");
static const u32 sAraunaPalette_R109[] = INCGFX_U32("graphics/battle_environment/arauna/r109/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R109 = {sAraunaTiles_R109, sAraunaMap_R109, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R109};
static const u32 sAraunaTiles_R110[] = INCGFX_U32("graphics/battle_environment/arauna/r110/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R110[] = INCGFX_U32("graphics/battle_environment/arauna/r110/map.bin", ".lz");
static const u32 sAraunaPalette_R110[] = INCGFX_U32("graphics/battle_environment/arauna/r110/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R110 = {sAraunaTiles_R110, sAraunaMap_R110, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R110};
static const u32 sAraunaTiles_R111[] = INCGFX_U32("graphics/battle_environment/arauna/r111/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R111[] = INCGFX_U32("graphics/battle_environment/arauna/r111/map.bin", ".lz");
static const u32 sAraunaPalette_R111[] = INCGFX_U32("graphics/battle_environment/arauna/r111/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R111 = {sAraunaTiles_R111, sAraunaMap_R111, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R111};
static const u32 sAraunaTiles_R112[] = INCGFX_U32("graphics/battle_environment/arauna/r112/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R112[] = INCGFX_U32("graphics/battle_environment/arauna/r112/map.bin", ".lz");
static const u32 sAraunaPalette_R112[] = INCGFX_U32("graphics/battle_environment/arauna/r112/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R112 = {sAraunaTiles_R112, sAraunaMap_R112, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R112};
static const u32 sAraunaTiles_R113[] = INCGFX_U32("graphics/battle_environment/arauna/r113/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R113[] = INCGFX_U32("graphics/battle_environment/arauna/r113/map.bin", ".lz");
static const u32 sAraunaPalette_R113[] = INCGFX_U32("graphics/battle_environment/arauna/r113/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R113 = {sAraunaTiles_R113, sAraunaMap_R113, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R113};
static const u32 sAraunaTiles_R114[] = INCGFX_U32("graphics/battle_environment/arauna/r114/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R114[] = INCGFX_U32("graphics/battle_environment/arauna/r114/map.bin", ".lz");
static const u32 sAraunaPalette_R114[] = INCGFX_U32("graphics/battle_environment/arauna/r114/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R114 = {sAraunaTiles_R114, sAraunaMap_R114, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R114};
static const u32 sAraunaTiles_R115[] = INCGFX_U32("graphics/battle_environment/arauna/r115/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R115[] = INCGFX_U32("graphics/battle_environment/arauna/r115/map.bin", ".lz");
static const u32 sAraunaPalette_R115[] = INCGFX_U32("graphics/battle_environment/arauna/r115/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R115 = {sAraunaTiles_R115, sAraunaMap_R115, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R115};
static const u32 sAraunaTiles_R116[] = INCGFX_U32("graphics/battle_environment/arauna/r116/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R116[] = INCGFX_U32("graphics/battle_environment/arauna/r116/map.bin", ".lz");
static const u32 sAraunaPalette_R116[] = INCGFX_U32("graphics/battle_environment/arauna/r116/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R116 = {sAraunaTiles_R116, sAraunaMap_R116, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R116};
static const u32 sAraunaTiles_R117[] = INCGFX_U32("graphics/battle_environment/arauna/r117/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R117[] = INCGFX_U32("graphics/battle_environment/arauna/r117/map.bin", ".lz");
static const u32 sAraunaPalette_R117[] = INCGFX_U32("graphics/battle_environment/arauna/r117/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R117 = {sAraunaTiles_R117, sAraunaMap_R117, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R117};
static const u32 sAraunaTiles_R118[] = INCGFX_U32("graphics/battle_environment/arauna/r118/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R118[] = INCGFX_U32("graphics/battle_environment/arauna/r118/map.bin", ".lz");
static const u32 sAraunaPalette_R118[] = INCGFX_U32("graphics/battle_environment/arauna/r118/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R118 = {sAraunaTiles_R118, sAraunaMap_R118, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R118};
static const u32 sAraunaTiles_R119[] = INCGFX_U32("graphics/battle_environment/arauna/r119/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R119[] = INCGFX_U32("graphics/battle_environment/arauna/r119/map.bin", ".lz");
static const u32 sAraunaPalette_R119[] = INCGFX_U32("graphics/battle_environment/arauna/r119/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R119 = {sAraunaTiles_R119, sAraunaMap_R119, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R119};
static const u32 sAraunaTiles_R120[] = INCGFX_U32("graphics/battle_environment/arauna/r120/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R120[] = INCGFX_U32("graphics/battle_environment/arauna/r120/map.bin", ".lz");
static const u32 sAraunaPalette_R120[] = INCGFX_U32("graphics/battle_environment/arauna/r120/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R120 = {sAraunaTiles_R120, sAraunaMap_R120, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R120};
static const u32 sAraunaTiles_R121[] = INCGFX_U32("graphics/battle_environment/arauna/r121/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R121[] = INCGFX_U32("graphics/battle_environment/arauna/r121/map.bin", ".lz");
static const u32 sAraunaPalette_R121[] = INCGFX_U32("graphics/battle_environment/arauna/r121/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R121 = {sAraunaTiles_R121, sAraunaMap_R121, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R121};
static const u32 sAraunaTiles_R122[] = INCGFX_U32("graphics/battle_environment/arauna/r122/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R122[] = INCGFX_U32("graphics/battle_environment/arauna/r122/map.bin", ".lz");
static const u32 sAraunaPalette_R122[] = INCGFX_U32("graphics/battle_environment/arauna/r122/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R122 = {sAraunaTiles_R122, sAraunaMap_R122, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R122};
static const u32 sAraunaTiles_R123[] = INCGFX_U32("graphics/battle_environment/arauna/r123/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R123[] = INCGFX_U32("graphics/battle_environment/arauna/r123/map.bin", ".lz");
static const u32 sAraunaPalette_R123[] = INCGFX_U32("graphics/battle_environment/arauna/r123/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R123 = {sAraunaTiles_R123, sAraunaMap_R123, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R123};
static const u32 sAraunaTiles_R124[] = INCGFX_U32("graphics/battle_environment/arauna/r124/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R124[] = INCGFX_U32("graphics/battle_environment/arauna/r124/map.bin", ".lz");
static const u32 sAraunaPalette_R124[] = INCGFX_U32("graphics/battle_environment/arauna/r124/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R124 = {sAraunaTiles_R124, sAraunaMap_R124, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R124};
static const u32 sAraunaTiles_R125[] = INCGFX_U32("graphics/battle_environment/arauna/r125/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R125[] = INCGFX_U32("graphics/battle_environment/arauna/r125/map.bin", ".lz");
static const u32 sAraunaPalette_R125[] = INCGFX_U32("graphics/battle_environment/arauna/r125/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R125 = {sAraunaTiles_R125, sAraunaMap_R125, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R125};
static const u32 sAraunaTiles_R126[] = INCGFX_U32("graphics/battle_environment/arauna/r126/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R126[] = INCGFX_U32("graphics/battle_environment/arauna/r126/map.bin", ".lz");
static const u32 sAraunaPalette_R126[] = INCGFX_U32("graphics/battle_environment/arauna/r126/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R126 = {sAraunaTiles_R126, sAraunaMap_R126, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R126};
static const u32 sAraunaTiles_R127[] = INCGFX_U32("graphics/battle_environment/arauna/r127/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R127[] = INCGFX_U32("graphics/battle_environment/arauna/r127/map.bin", ".lz");
static const u32 sAraunaPalette_R127[] = INCGFX_U32("graphics/battle_environment/arauna/r127/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R127 = {sAraunaTiles_R127, sAraunaMap_R127, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R127};
static const u32 sAraunaTiles_R128[] = INCGFX_U32("graphics/battle_environment/arauna/r128/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R128[] = INCGFX_U32("graphics/battle_environment/arauna/r128/map.bin", ".lz");
static const u32 sAraunaPalette_R128[] = INCGFX_U32("graphics/battle_environment/arauna/r128/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R128 = {sAraunaTiles_R128, sAraunaMap_R128, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R128};
static const u32 sAraunaTiles_R129[] = INCGFX_U32("graphics/battle_environment/arauna/r129/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R129[] = INCGFX_U32("graphics/battle_environment/arauna/r129/map.bin", ".lz");
static const u32 sAraunaPalette_R129[] = INCGFX_U32("graphics/battle_environment/arauna/r129/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R129 = {sAraunaTiles_R129, sAraunaMap_R129, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R129};
static const u32 sAraunaTiles_R130[] = INCGFX_U32("graphics/battle_environment/arauna/r130/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R130[] = INCGFX_U32("graphics/battle_environment/arauna/r130/map.bin", ".lz");
static const u32 sAraunaPalette_R130[] = INCGFX_U32("graphics/battle_environment/arauna/r130/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R130 = {sAraunaTiles_R130, sAraunaMap_R130, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R130};
static const u32 sAraunaTiles_R131[] = INCGFX_U32("graphics/battle_environment/arauna/r131/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R131[] = INCGFX_U32("graphics/battle_environment/arauna/r131/map.bin", ".lz");
static const u32 sAraunaPalette_R131[] = INCGFX_U32("graphics/battle_environment/arauna/r131/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R131 = {sAraunaTiles_R131, sAraunaMap_R131, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R131};
static const u32 sAraunaTiles_R132[] = INCGFX_U32("graphics/battle_environment/arauna/r132/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R132[] = INCGFX_U32("graphics/battle_environment/arauna/r132/map.bin", ".lz");
static const u32 sAraunaPalette_R132[] = INCGFX_U32("graphics/battle_environment/arauna/r132/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R132 = {sAraunaTiles_R132, sAraunaMap_R132, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R132};
static const u32 sAraunaTiles_R133[] = INCGFX_U32("graphics/battle_environment/arauna/r133/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R133[] = INCGFX_U32("graphics/battle_environment/arauna/r133/map.bin", ".lz");
static const u32 sAraunaPalette_R133[] = INCGFX_U32("graphics/battle_environment/arauna/r133/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R133 = {sAraunaTiles_R133, sAraunaMap_R133, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R133};
static const u32 sAraunaTiles_R134[] = INCGFX_U32("graphics/battle_environment/arauna/r134/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_R134[] = INCGFX_U32("graphics/battle_environment/arauna/r134/map.bin", ".lz");
static const u32 sAraunaPalette_R134[] = INCGFX_U32("graphics/battle_environment/arauna/r134/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_R134 = {sAraunaTiles_R134, sAraunaMap_R134, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_R134};
static const u32 sAraunaTiles_G01[] = INCGFX_U32("graphics/battle_environment/arauna/g01/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_G01[] = INCGFX_U32("graphics/battle_environment/arauna/g01/map.bin", ".lz");
static const u32 sAraunaPalette_G01[] = INCGFX_U32("graphics/battle_environment/arauna/g01/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_G01 = {sAraunaTiles_G01, sAraunaMap_G01, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_G01};
static const u32 sAraunaTiles_G02[] = INCGFX_U32("graphics/battle_environment/arauna/g02/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_G02[] = INCGFX_U32("graphics/battle_environment/arauna/g02/map.bin", ".lz");
static const u32 sAraunaPalette_G02[] = INCGFX_U32("graphics/battle_environment/arauna/g02/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_G02 = {sAraunaTiles_G02, sAraunaMap_G02, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_G02};
static const u32 sAraunaTiles_G03[] = INCGFX_U32("graphics/battle_environment/arauna/g03/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_G03[] = INCGFX_U32("graphics/battle_environment/arauna/g03/map.bin", ".lz");
static const u32 sAraunaPalette_G03[] = INCGFX_U32("graphics/battle_environment/arauna/g03/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_G03 = {sAraunaTiles_G03, sAraunaMap_G03, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_G03};
static const u32 sAraunaTiles_G04[] = INCGFX_U32("graphics/battle_environment/arauna/g04/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_G04[] = INCGFX_U32("graphics/battle_environment/arauna/g04/map.bin", ".lz");
static const u32 sAraunaPalette_G04[] = INCGFX_U32("graphics/battle_environment/arauna/g04/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_G04 = {sAraunaTiles_G04, sAraunaMap_G04, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_G04};
static const u32 sAraunaTiles_G05[] = INCGFX_U32("graphics/battle_environment/arauna/g05/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_G05[] = INCGFX_U32("graphics/battle_environment/arauna/g05/map.bin", ".lz");
static const u32 sAraunaPalette_G05[] = INCGFX_U32("graphics/battle_environment/arauna/g05/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_G05 = {sAraunaTiles_G05, sAraunaMap_G05, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_G05};
static const u32 sAraunaTiles_G06[] = INCGFX_U32("graphics/battle_environment/arauna/g06/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_G06[] = INCGFX_U32("graphics/battle_environment/arauna/g06/map.bin", ".lz");
static const u32 sAraunaPalette_G06[] = INCGFX_U32("graphics/battle_environment/arauna/g06/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_G06 = {sAraunaTiles_G06, sAraunaMap_G06, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_G06};
static const u32 sAraunaTiles_G07[] = INCGFX_U32("graphics/battle_environment/arauna/g07/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_G07[] = INCGFX_U32("graphics/battle_environment/arauna/g07/map.bin", ".lz");
static const u32 sAraunaPalette_G07[] = INCGFX_U32("graphics/battle_environment/arauna/g07/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_G07 = {sAraunaTiles_G07, sAraunaMap_G07, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_G07};
static const u32 sAraunaTiles_G08[] = INCGFX_U32("graphics/battle_environment/arauna/g08/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_G08[] = INCGFX_U32("graphics/battle_environment/arauna/g08/map.bin", ".lz");
static const u32 sAraunaPalette_G08[] = INCGFX_U32("graphics/battle_environment/arauna/g08/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_G08 = {sAraunaTiles_G08, sAraunaMap_G08, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_G08};
static const u32 sAraunaTiles_E01[] = INCGFX_U32("graphics/battle_environment/arauna/e01/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_E01[] = INCGFX_U32("graphics/battle_environment/arauna/e01/map.bin", ".lz");
static const u32 sAraunaPalette_E01[] = INCGFX_U32("graphics/battle_environment/arauna/e01/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_E01 = {sAraunaTiles_E01, sAraunaMap_E01, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_E01};
static const u32 sAraunaTiles_E02[] = INCGFX_U32("graphics/battle_environment/arauna/e02/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_E02[] = INCGFX_U32("graphics/battle_environment/arauna/e02/map.bin", ".lz");
static const u32 sAraunaPalette_E02[] = INCGFX_U32("graphics/battle_environment/arauna/e02/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_E02 = {sAraunaTiles_E02, sAraunaMap_E02, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_E02};
static const u32 sAraunaTiles_E03[] = INCGFX_U32("graphics/battle_environment/arauna/e03/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_E03[] = INCGFX_U32("graphics/battle_environment/arauna/e03/map.bin", ".lz");
static const u32 sAraunaPalette_E03[] = INCGFX_U32("graphics/battle_environment/arauna/e03/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_E03 = {sAraunaTiles_E03, sAraunaMap_E03, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_E03};
static const u32 sAraunaTiles_E04[] = INCGFX_U32("graphics/battle_environment/arauna/e04/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_E04[] = INCGFX_U32("graphics/battle_environment/arauna/e04/map.bin", ".lz");
static const u32 sAraunaPalette_E04[] = INCGFX_U32("graphics/battle_environment/arauna/e04/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_E04 = {sAraunaTiles_E04, sAraunaMap_E04, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_E04};
static const u32 sAraunaTiles_C01[] = INCGFX_U32("graphics/battle_environment/arauna/c01/tiles.png", ".4bpp.lz");
static const u32 sAraunaMap_C01[] = INCGFX_U32("graphics/battle_environment/arauna/c01/map.bin", ".lz");
static const u32 sAraunaPalette_C01[] = INCGFX_U32("graphics/battle_environment/arauna/c01/palette.pal", ".gbapal.lz");
static const struct BattleBackground sAraunaBg_C01 = {sAraunaTiles_C01, sAraunaMap_C01, sAraunaEntryTiles, sAraunaEntryMap, sAraunaPalette_C01};

static const struct BattleBackground *GetAraunaBattleBackground(void)
{
    u16 map;
    bool8 water;
    // Recorded/link/facility and special legendary backgrounds have precedence.
    if (gBattleTypeFlags & (BATTLE_TYPE_LINK | BATTLE_TYPE_FRONTIER | BATTLE_TYPE_RECORDED | BATTLE_TYPE_RECORDED_LINK | BATTLE_TYPE_EREADER_TRAINER | BATTLE_TYPE_TRAINER_HILL | BATTLE_TYPE_SECRET_BASE | BATTLE_TYPE_GROUDON | BATTLE_TYPE_KYOGRE | BATTLE_TYPE_KYOGRE_GROUDON | BATTLE_TYPE_RAYQUAZA | BATTLE_TYPE_INGAME_PARTNER))
        return NULL;
    if (gBattleTypeFlags & BATTLE_TYPE_TRAINER)
    {
        switch (gTrainerBattleOpponent_A)
        {
        case TRAINER_ROXANNE_1:
        case TRAINER_ROXANNE_2:
        case TRAINER_ROXANNE_3:
        case TRAINER_ROXANNE_4:
        case TRAINER_ROXANNE_5:
            return &sAraunaBg_G01;
        case TRAINER_BRAWLY_1:
        case TRAINER_BRAWLY_2:
        case TRAINER_BRAWLY_3:
        case TRAINER_BRAWLY_4:
        case TRAINER_BRAWLY_5:
            return &sAraunaBg_G02;
        case TRAINER_WATTSON_1:
        case TRAINER_WATTSON_2:
        case TRAINER_WATTSON_3:
        case TRAINER_WATTSON_4:
        case TRAINER_WATTSON_5:
            return &sAraunaBg_G03;
        case TRAINER_FLANNERY_1:
        case TRAINER_FLANNERY_2:
        case TRAINER_FLANNERY_3:
        case TRAINER_FLANNERY_4:
        case TRAINER_FLANNERY_5:
            return &sAraunaBg_G04;
        case TRAINER_NORMAN_1:
        case TRAINER_NORMAN_2:
        case TRAINER_NORMAN_3:
        case TRAINER_NORMAN_4:
        case TRAINER_NORMAN_5:
            return &sAraunaBg_G05;
        case TRAINER_WINONA_1:
        case TRAINER_WINONA_2:
        case TRAINER_WINONA_3:
        case TRAINER_WINONA_4:
        case TRAINER_WINONA_5:
            return &sAraunaBg_G06;
        case TRAINER_TATE_AND_LIZA_1:
        case TRAINER_TATE_AND_LIZA_2:
        case TRAINER_TATE_AND_LIZA_3:
        case TRAINER_TATE_AND_LIZA_4:
        case TRAINER_TATE_AND_LIZA_5:
            return &sAraunaBg_G07;
        case TRAINER_JUAN_1:
        case TRAINER_JUAN_2:
        case TRAINER_JUAN_3:
        case TRAINER_JUAN_4:
        case TRAINER_JUAN_5:
            return &sAraunaBg_G08;
        case TRAINER_SIDNEY: return &sAraunaBg_E01;
        case TRAINER_PHOEBE: return &sAraunaBg_E02;
        case TRAINER_GLACIA: return &sAraunaBg_E03;
        case TRAINER_DRAKE: return &sAraunaBg_E04;
        case TRAINER_WALLACE: return &sAraunaBg_C01;
        }
    }
    map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    water = gBattleEnvironment == BATTLE_ENVIRONMENT_WATER || gBattleEnvironment == BATTLE_ENVIRONMENT_POND;
    switch (map)
    {
    case MAP_ROUTE101:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R101;
    case MAP_ROUTE102:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R102;
    case MAP_ROUTE103:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R103;
    case MAP_ROUTE104:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R104;
    case MAP_ROUTE105:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R105;
    case MAP_ROUTE106:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R106;
    case MAP_ROUTE107:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R107;
    case MAP_ROUTE108:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R108;
    case MAP_ROUTE109:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R109;
    case MAP_ROUTE110:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R110;
    case MAP_ROUTE111:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        if (gBattleEnvironment != BATTLE_ENVIRONMENT_SAND)
            return NULL;
        return &sAraunaBg_R111;
    case MAP_ROUTE112:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R112;
    case MAP_ROUTE113:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R113;
    case MAP_ROUTE114:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R114;
    case MAP_ROUTE115:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R115;
    case MAP_ROUTE116:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R116;
    case MAP_ROUTE117:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R117;
    case MAP_ROUTE118:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R118;
    case MAP_ROUTE119:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R119;
    case MAP_ROUTE120:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R120;
    case MAP_ROUTE121:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R121;
    case MAP_ROUTE122:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R122;
    case MAP_ROUTE123:
        if (water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R123;
    case MAP_ROUTE124:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R124;
    case MAP_ROUTE125:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R125;
    case MAP_ROUTE126:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R126;
    case MAP_ROUTE127:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R127;
    case MAP_ROUTE128:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R128;
    case MAP_ROUTE129:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R129;
    case MAP_ROUTE130:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R130;
    case MAP_ROUTE131:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R131;
    case MAP_ROUTE132:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R132;
    case MAP_ROUTE133:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R133;
    case MAP_ROUTE134:
        if (!water || gBattleEnvironment == BATTLE_ENVIRONMENT_UNDERWATER)
            return NULL;
        return &sAraunaBg_R134;
    case MAP_RUSTBORO_CITY_GYM: return &sAraunaBg_G01;
    case MAP_DEWFORD_TOWN_GYM: return &sAraunaBg_G02;
    case MAP_MAUVILLE_CITY_GYM: return &sAraunaBg_G03;
    case MAP_LAVARIDGE_TOWN_GYM_1F: return &sAraunaBg_G04;
    case MAP_LAVARIDGE_TOWN_GYM_B1F: return &sAraunaBg_G04;
    case MAP_PETALBURG_CITY_GYM: return &sAraunaBg_G05;
    case MAP_FORTREE_CITY_GYM: return &sAraunaBg_G06;
    case MAP_MOSSDEEP_CITY_GYM: return &sAraunaBg_G07;
    case MAP_SOOTOPOLIS_CITY_GYM_1F: return &sAraunaBg_G08;
    case MAP_SOOTOPOLIS_CITY_GYM_B1F: return &sAraunaBg_G08;
    case MAP_EVER_GRANDE_CITY_SIDNEYS_ROOM: return &sAraunaBg_E01;
    case MAP_EVER_GRANDE_CITY_PHOEBES_ROOM: return &sAraunaBg_E02;
    case MAP_EVER_GRANDE_CITY_GLACIAS_ROOM: return &sAraunaBg_E03;
    case MAP_EVER_GRANDE_CITY_DRAKES_ROOM: return &sAraunaBg_E04;
    case MAP_EVER_GRANDE_CITY_CHAMPIONS_ROOM: return &sAraunaBg_C01;
    }
    return NULL;
}

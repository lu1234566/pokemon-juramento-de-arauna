# Arauna — Bases Secretas em cavernas, checkpoint 06C1 V1

16 interiores redesenhados sobre o 06B `2449e12b0645f9aa37ef261ba2d3ce71df93254a`: quatro Red Cave, quatro Brown Cave, quatro Blue Cave e quatro Yellow Cave. Escopo fechado antes das oito bases em árvores/arbustos e dos 47 mapas da Battle Frontier.

## Referências e ambientação

A Master Map Design Bible e os 82 concepts recuperados estão em `docs/referencias/bible_concepts_recuperados`. O 06B foi recuperado do pacote salvo e conferido pelo bundle e pelos hashes antes das edições. A Bible descreve mineralogia nas Galerias da Serra e Gruta das Vozes (p.25–26), terreno vulcânico na Serra da Cinza (p.27), pedra fria na Gruta da Maré (p.29) e arenito do semiarido/deserto (p.16). Não contém uma direção dedicada às Bases Secretas; esta proposta adapta esses materiais sem acrescentar lore ou mudar nomes do jogo.

| Família nativa | Material | Direção |
|---|---|---|
| Red Cave 1–4 | Laterita | Solo ferruginoso, luz quente, juntas escuras |
| Brown Cave 1–4 | Arenito | Estratos castanhos, piso seco e pouca textura |
| Blue Cave 1–4 | Basalto | Pedra fria cinza azulada, contraste com o computador |
| Yellow Cave 1–4 | Calcário ocre | Tom mineral claro, fraturas esparsas |

Os contornos originais, obstáculos, portas e áreas decoráveis permanecem. O piso usa fraturas curtas e lascas claras; não recebe objetos cenográficos que bloqueiem a decoração.

## Implementação e preservação

Quatro bancos secundários privados `gTileset_AraunaSecret06C1{Red,Brown,Blue,Yellow}`. Apenas os campos secondary_tileset dos 16 layouts e três headers aditivos mudam entre os arquivos existentes. Os 754 IDs e sua ordem são os mesmos, sem layouts acrescentados.

Cada banco retém os 83 gráficos nativos e acrescenta 65 subtiles de ambiente, com preenchimento até 160. A paleta 12, sem referências no banco original, recebe o material. As 12 paletas anteriores e todos os metatile entries que referenciam o banco primário continuam byte a byte iguais. Compressão LZ nativa, callback NULL. Nenhuma animação em slots compartilhados foi criada.

O banco primário `gTileset_SecretBase` e os ponteiros `gTilesetPointer_SecretBase`/`gTilesetPointer_SecretBaseRedCave`, que o menu das decorações lê diretamente, permanecem intactos. Piso e parede sob PC e móveis remapeiam o mesmo material, incluindo os estados Register PC, chão sob PC oculto e passagens de decoração.

Grids, bordas, map.json, scripts, eventos, computador, treinador, 14 placeholders de sprites por mapa, catálogo, inventário, permissões, saves, link/record mixing e 75 entradas exteriores são protegidos por hashes. Os 16 exits continuam `MAP_DYNAMIC / WARP_ID_SECRET_BASE`. Nenhum script de progressão muda. Record mixing tem preservação de código, sem alegação de sessão link executada.

## Evidências

`validation.json`: 22.787 dependências preservadas (18.426 de gameplay + 4.361 outras), 2.090 células, 1.296 atributos de metatiles, 2.592 máscaras de camadas, 5.504 referências primárias, 48 arquivos de paleta e 332 gráficos originais. As oito bases Tree/Shrub têm renders idênticos ao 06B. O selector C também verifica as 53.167 células anteriores de cavernas/Dive.

`native_c.log` e `validation.json`: catálogo nativo de 120 decorações válidas, 501.600 decisões de posicionamento comparadas antes/depois, 1.200 escritas de decorações não sprite 196 casos de PC/entrada/retorno e 256 casos das 16 posições salvas de decoração. O harness compila as funções C reais com serviços explícitos para grid, variáveis, saves, objetos, fade, tasks e callbacks. Não representa execução integral do motor.

`install_test.json`: instalador real em checkout isolado, preflight, corrupção, mudanças locais, base atrasada, rollback, idempotência, hashes completos e reprodução pelo builder. `CUMULATIVE_TEST.json` no pacote: importação real em repositório que começa somente no integrador d665, igualdade da árvore completa e checkout dos hashes, incluindo CRLF de paletas; aplicação real do patch incremental.

Três montagens e 16 pares de mapas completos são renderizados com RGB555. Os exemplos decorados usam CanPlaceDecoration/ShowDecorationOnMap; são fixtures de revisão, nunca escritas nos saves ou grids instalados. Não mostram atores, dolls, clima ou capturas de emulador.

A auditoria oficial de mapas passou 8/8 e a composição oficial English passou o static readiness. Os fontes foram restaurados e todos os hashes congelados conferidos após essa composição. Compilação ARM e revisão mGBA pendentes por ausência dessas ferramentas. Revisão de sprites e record mixing em link pendentes. O pacote não contém ROM, ELF ou saves.

## GitHub e integração

Integrador conferido: `d665dc34ddea776c06c85981653a9f62aa1e19d6`, ainda sem 06A/06B. Main `979fb6c1b6731561f3c993efd6045a9bbf096c54`, 88 commits atrás. Entrega cumulativa inclui 06A + 06B + 06C1 sobre d665; incremento exige o 06B 2449. Não publica ou envia mensagens ao autor.

Próximo checkpoint: 06C2, oito bases Tree/Shrub. Battle Frontier depois. Manutenção geral e remoção de bancos antigos ficam para a rodada do usuário.

# Battle Frontier 07D — Battle Factory V1

Três mapas recebem um par privado de bancos nativos 4bpp. A Factory assume a linguagem de uma oficina técnica em funcionamento: placas de pedra escura, perfis de cobre, painéis verde-jade, prateleiras de cápsulas e uma marca de calibração na arena. A construção preserva as silhuetas dos equipamentos e distingue a circulação das bancadas. Os componentes nativos de piso sob os móveis recebem o mesmo material, evitando emendas claras. A engrenagem é arte do piso, sem acrescentar evento ou regra de combate.

Master Map Design Bible, concepts da Liga e da Usina e o último pacote 07C foram recuperados antes de editar. A Bible governa escala e materiais; a Usina serve de referência para a infraestrutura técnica, sem transformar esta instalação ativa em local abandonado nem criar nome canônico. O ZIP 07C foi conferido por CRC e 178 hashes internos. As prévias vêm dos bancos reais e do map.bin, sem sprites.

## Base e manutenção do GitHub

Base direta: `8d7cafa5d7eef106eea69bc1ad18e3097d7e343b`. Ela incorpora o 07C `638d523c088ddc9991617031e07808119712caf7` e corrige a água 0x226 no Palace. As três alterações dessa integração — metatiles do garden, docs/INTEGRACAO_07C.md e corrige_agua_palace_07c.py — ficam exatas. field_door.c e overworld.c conservam as correções anteriores, incluindo as portas próprias da Tower.

main permanece em `979fb6c1b6731561f3c993efd6045a9bbf096c54`, 102 commits atrás da base conferida. O 07D parte do integrador, com bundles cumulativos para os históricos anteriores. Não houve push.

## Escopo e preservação

| Mapa | Dimensões | Células | Objetos | Warps do map.json |
|---|---:|---:|---:|---:|
| BattleFactoryLobby | 19×12 | 228 | 6 | 2 |
| BattleFactoryPreBattleRoom | 17×14 | 238 | 1 | 0 |
| BattleFactoryBattleRoom | 13×12 | 156 | 8 | 0 |

622 células, 15 objetos e dois warps declarados. As transições coordenadas por scripts também ficam exatas. Os 754 layouts mantêm IDs, ordem e compartilhamento; só os três da Factory mudam as referências dos bancos. Não se acrescenta layout. Os únicos arquivos anteriores editados são layouts.json e três cabeçalhos de tilesets, com bloco FRONTIER_07D isolado.

311 metatiles usados recebem arte, sem trocar IDs. Os 362 atributos e 724 máscaras dos dois planos permanecem exatos. Os grids, bordas, colisão, elevação, scripts, objetos, movimentos, eventos e warps são preservados por bytes, assim como aluguel e escolha de Pokémon, trocas, modos de nível, geração de adversários, Noland, batalhas, recompensas, saves e progressão. O desenho da arena usa apenas metatiles exclusivos desse mapa, conferidos contra Lobby e PreBattleRoom.

23.352 dependências anteriores congeladas por SHA-256. Paletas 0–11 mantêm as cores originais; apenas a paleta 12, antes vazia, recebe os materiais. A alocação estática exclui 432–511 e 992–1023, reservados a animações e portas. Cada banco continua com no máximo 512 tiles. O primário conserva InitTilesetAnim_Building e seus quadros; o secundário conserva NULL. As passagens da Factory usam os scripts de movimento/fade originais, sem comandos de portas animadas. O roteador e todos os gráficos anteriores de portas continuam protegidos.

## Verificações

- Auditoria oficial de mapas: PASS, sem novos eventos fora do mapa, IDs inválidos, tamanhos incorretos, warps/conexões inválidos ou saídas inalcançáveis.
- Static readiness: PASS, com composição oficial e gates completos. Compilação ARM explicitamente omitida pelo gate estático. Os arquivos ignorados de 528 mapas e 551 MIDI foram gerados pelas ferramentas originais para os verificadores.
- Seletores C originais: 622 células locais, 15.360 fallbacks e 53.167 células anteriores de cavernas/Dive.
- 362 atributos, 724 máscaras e 16 comparações dos oito metatiles Building em dois quadros; IDs, paletas, capacidades e slots reservados: PASS.
- InitTilesetAnim_Building, dispatch e fila TV no C original: 256 ticks, 32 atualizações e os dois payloads 4bpp nativos.
- Os 17 mapas anteriores da Frontier ficam idênticos em 34 comparações de frames. A água corrigida 0x226 do Palace coincide com 0x190 nos oito quadros.
- Regressões C anteriores: roteador de portas e desenho/flags, General com 256 ticks/80 atualizações e Dome com 865 casos de luz/fade/transição.
- Instalador: instalação real, hashes, rejeição de corrupção/edições/bases incorretas, rollback, reaplicação sem escritas, HEAD preservado e reconstrução determinística. Resultados em review/frontier_07d/install_test.json.
- Quatro bundles importados em receptores independentes: base/ancestrais, commit, árvore, checkout SHA incluindo paletas CRLF, dependências protegidas e aplicação real do patch. Resultados em CUMULATIVE_TEST.json do pacote.

Limites: os testes C usam serviços explícitos do host para VRAM, filas, tarefas, flags e desenho. Scripts e a lógica Factory ficam preservados por hash, sem executar interpretador de batalhas/scripts. Compilação ARM e teste de aluguel, troca, partidas, Noland, saves, sprites e execução completa no mGBA permanecem pendentes neste ambiente. As imagens são renders RGB555, não capturas de emulador.

## Retomada

checkpoint_BattleFrontier_07D.bundle acrescenta o 07D à base atual 8d. Os cumulativos do 07C/638, GitHub/9f e 06C2/989 incluem a manutenção necessária e o resultado completo. O incremento source/, changes.patch e install.py exige 8d; não aplicar diretamente às bases antigas ou main. O instalador verifica a base inteira antes de escrever, mantém HEAD, cria backup/rollback e reaplica sem novas escritas. LEIA_ME.md contém os comandos de cada rota.

Concluídos **20/47 mapas Frontier**; restam 27. Próximo checkpoint: **07E, seis mapas de Battle Pike**. Inventário em review/frontier_07d/checkpoint_plan.json.

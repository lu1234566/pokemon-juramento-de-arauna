# Battle Frontier — checkpoint 07F / Battle Pyramid V1

Base autoritativa: `9a3f9464ea6ba1e30b599c76648e4eb0e1a49405`, integração oficial do 07E. O checkpoint acrescenta três mapas: **29/47 Frontier concluídos**, restam 18. Arte e verificação no host estão concluídas; build ARM e testes jogáveis no mGBA ficam pendentes neste ambiente. Nenhum push foi feito.

## Recuperação e ambientação

A Master Map Design Bible, o concept da Liga/Caminho das Quatro Vozes e o relatório/pacote 07E foram recuperados antes da arte. A Bible orienta materiais, identidade arquitetônica, leitura em 240×160 e preservação da autoridade funcional dos scripts. Não existe um concept dedicado à Pyramid recuperado nesta etapa; a aplicação é uma interpretação artística desses princípios, sem acrescentar cânone.

Os 96 arquivos do incremento 07E conferem por SHA-256 contra a base 9a. Entre o 07E do autor (`a679c20843`) e 9a muda apenas `docs/INTEGRACAO_07E.md`. O branch de autoria no remoto foi conferido em 9a; main está em `979fb6c1b6`, 106 commits atrás da base. Não usar main para aplicar o incremento. Evidências em `review/frontier_07f/recovery.json`.

O saguão recebe piso de pedra escura, juntas de cobre, bancadas verdes e luz das tochas. Os andares recebem alvenaria modular e uma saída azul com sinal de ascensão. O topo mostra uma rosa dos ventos acima da massa da pirâmide, em céu de crepúsculo. A grande área navegável fica tranquila para leitura dos atores. As estátuas, chamas e sombras conservam os quadrantes usados pela animação original. A porta de entrada e o sinal de ascensão permanecem reconhecíveis.

## Três mapas e os módulos do gerador

| Mapa contado no Frontier | Layout | Células de origem | Eventos de objeto | Warps declarados |
|---|---|---:|---:|---:|
| BattleFrontier_BattlePyramidLobby | Original, índice 359 | 270 | 4 | 1 |
| BattleFrontier_BattlePyramidFloor | Original, índice 360 | 64, stub 8×8 | 16 | 0 |
| BattleFrontier_BattlePyramidTop | Original, índice 377 | 782 | 2 | 0 |

O Floor de 8×8 **não é o andar jogado**. O C monta 16 módulos de 8×8 numa área de 32×32, inserida em buffer de 47×46 com as margens do engine. Square01–Square16 ocupam índices 361–376 da tabela original. O acesso `offset + LAYOUT_BATTLE_FRONTIER_BATTLE_PYRAMID_FLOOR` é intencional: o valor da constante é baseado em 1 e aponta para Square01 quando o offset é zero. Nenhum ID ou ordem foi alterado.

Os módulos somam 1.024 células de origem e 112 objetos. Seus map.json, scripts, grids, bordas e referências aos bancos originais do editor permanecem exatos. O gerador copia apenas os dados dos grids para o Floor ativo; é o par gráfico privado desse Floor que desenha os IDs em runtime. As provas dos módulos os renderizam com esse par, como o jogo. Eles não acrescentam 16 ao contador dos 47 mapas Frontier.

Há um marcador 0x28E por módulo. O gerador conserva um no módulo de saída e transforma os demais em 0x28D, copiando colisão e elevação. A posição inicial usa o marcador do módulo de entrada. O teste executa os dois valores de `setPlayerPosition`, inclusive o ramo FALSE que calcula a posição. Warps por script, retorno ao saguão, subida ao topo e progresso ficam intocados.

## Bancos, paletas e animação

Só os três layouts contados no checkpoint trocam referências para um par privado. Os 754 layouts mantêm IDs, ordem, dimensões, paths, compartilhamento e demais campos. Os quatro arquivos preexistentes editáveis são layouts.json e as três tabelas de declaração de tilesets. As declarações antigas permanecem iguais após remover o bloco FRONTIER_07F.

132 IDs usados são redesenhados. Os 229 atributos dos dois bancos e as 458 máscaras dos planos permanecem exatos. Há mais 792 comparações de máscaras sob os três quadros animados. Os bancos seguem 4bpp, até 512 tiles cada, até 16 índices por paleta. A arte aloca 266 slots e deixa 438 livres. A alocação exclui as reservas gerais e os slots específicos da Pyramid.

**A paleta dos andares é BG6**, trocada pela tarefa original conforme `curChallengeBattleNum`. Os sete conjuntos de 16 cores de `graphics/battle_frontier/pyramid_floor.pal` continuam exatos, bem como `src/graphics.c` e o callback da tarefa. Todos os IDs dos módulos usam BG6. Não foi substituída por uma cor fixa: a variação entre pisos foi preservada. Paletas 0–11 ficam iguais; só BG12, antes vazia, recebe os materiais do Lobby/Top.

O primário conserva InitTilesetAnim_Building/TV. O secundário conserva InitTilesetAnim_BattlePyramid. A animação original escreve oito tiles da sombra em 647–654 e oito da tocha em 663–670, a cada oito ticks. Esses destinos foram reservados antes de alocar arte; 22 entradas animadas de metatiles mantêm gráficos, paletas, flips e quadrantes. O teste executa initializer, dispatcher e queues originais por 256 ticks, com 64 updates e sentinelas ao redor dos destinos.

## Preservação e provas

O contrato anterior à edição congela **23.524 arquivos rastreados**. Inclui field_door.c, overworld.c, battle_pyramid.c, battle_pyramid_bag.c, fieldmap.c, frontier_util.c, tileset_anims.c, constantes, paletas, encontros, objetos, scripts, grids e toda a progressão. Sementes, RNG, níveis 50/aberto, elenco, itens no chão, bolsa da Pyramid, luz, dicas, Brandon, batalhas, saves e recompensas não mudam. Isso é proteção por hash, não afirmação de desafio jogado.

O C original de seleção de modelos/módulos, montagem de grids, entrada/saída, posição inicial, todos os modos de distribuição de objetos e tarefa de paleta foi extraído sem editar suas funções e compilado no host. Os dados de origem vêm dos grids e eventos reais. São **1.848 casos**, cobrindo todos os 16 módulos e 16 modelos, **1.892.352 células montadas**, **2.103.024 células de margem intocadas**, **15.174 objetos colocados** e 14 casos da tarefa de paleta. Cada grid e posição coincide com a base. Os objetos conferem tipo, coordenadas, unicidade, chão acessível e dados de origem; nenhuma colisão ou elevação foi relaxada.

Serviços de memória, map-header lookup, callback on-load e escolha de IDs/gráficos de treinadores são fixtures explícitas. O teste de distribuição não testa o RNG real do elenco. O interpretador de scripts, batalhas, bolsa, saves e hardware de luz não foram executados. O harness respeita os ramos BUGFIX do código original; a limpeza das alocações remanescentes é apenas do host.

Os seletores C do jogo conferem as 1.116 células dos três grids de origem, 15.360 fallbacks e 53.167 células anteriores de cavernas/Dive. Os 26 mapas Frontier anteriores mantêm pixels em 52 casos de quadro. Portas da Tower, cortina do Pike, animação do Dome, Building/General e os oito quadros da borda d'água corrigida do Palace também passam. Todos os arquivos originais dos bancos dessas etapas estão congelados.

A auditoria oficial percorreu 528 mapas e passou seus oito gates; três notas de Surf são preexistentes. O static readiness passou todos os gates oficiais após gerar os outputs ignorados com mapjson e mid2agb originais. **O gate estático omite explicitamente o compile ARM.** Nenhuma ROM 07F foi compilada ou jogada neste ambiente, que não dispõe de toolchain ARM/mGBA. A nota de integração 07E relata testes do integrador na etapa anterior; esses testes não validam a arte 07F.

## Instalação, históricos e retomada

O ZIP contém incremento completo, patch binário, instalador, provas e cinco bundles de histórico, para 9a, a679/07E, 38d, 9f e 989/06C2. Esses históricos conservam as correções de engine e as integrações intermediárias. O instalador valida pacote e dependências antes de escrever, rejeita bases antigas e edições desconhecidas, conserva HEAD, cria backup e faz rollback em falhas. Reinstalação não produz novas escritas.

`install_test.json` registra instalações reais em worktree isolado, corrupção, edições de dependências, bases erradas, falhas de escrita, rollback e geração determinística. Os bundles são importados em receptores independentes; `CUMULATIVE_TEST.json`, no ZIP, comprova árvore, ancestralidade, checkout completo, hashes e patch. O hash externo do ZIP fica no relatório de entrega.

As imagens são renders RGB555 de arte nativa, sem sprites, luz simulada ou capturas do mGBA. Há mapas completos antes/depois, câmeras 240×160, sete andares realmente montados pelo C, todos os módulos e os três quadros animados.

Reprodução com Python 3, Pillow e compilador C do host:

```sh
python3 tools/arauna_maps/validate_frontier_07f.py --base /checkout-limpo-9a3f9464ea
python3 tools/arauna_maps/render_frontier_07f.py --base /checkout-limpo-9a3f9464ea
```

Próximo checkpoint: **07G — nove lounges e casa de Scott, dez mapas**. Plano atualizado em review/frontier_07f/checkpoint_plan.json. O 07F é uma etapa fechada e retomável; a próxima autoria pode começar da revisão registrada no manifesto, após a integração testar a ROM e o desafio no emulador.

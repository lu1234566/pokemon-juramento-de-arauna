# 08B2 — DesertUnderpass + ScorchedSlab V1

Dois mapas concluídos sobre `0434665c07f2598f43bc399da4e8a7ce44e02979`.
São 3.497 células: Underpass 139 × 23 e ScorchedSlab 15 × 20.

## Ambientação

**DesertUnderpass:** galeria sedimentar com faixas horizontais de arenito,
chão compactado e depósitos mais claros perto do fóssil. A textura substitui
a hachura diagonal herdada; as faces e os degraus continuam delimitando os
mesmos volumes. As referências são a Rota 114 (vale, pedra e paredões) e a
transição semiarida da Rota 111 da Master Map Design Bible.

**ScorchedSlab:** rocha escura com fraturas, líquen discreto e um patamar de
pedra acima do espelho d'água. A referência da Rota 120 é mata e ruínas;
não foram acrescentadas lava, calor, personagens ou história. O patamar do
TM contrasta com a massa rochosa bloqueada, e a margem mantém a forma nativa.

A arte foi desenhada diretamente na grade de pixels nativa. Há quatro bancos
exclusivos, primário e secundário para cada mapa. No Underpass foram
redesenhados 34 IDs com 92 slots gráficos novos; em ScorchedSlab, 23 IDs
com 53 slots. Não há aliases de câmera nem novas rotinas C.

## Base, correção do menu e histórico

O último commit da branch `claude/pokemon-juramento-arauna-fhk6ah`, conferido
no GitHub, é a base solicitada. Ela contém o 08B1 `5e51e3b2ba`, a correção
do menu de HMs `b4d5f73ec` e `docs/INTEGRACAO_08B1.md`.

O novo contrato congela **24.167 arquivos** anteriores. Inclui
`src/party_menu.c` com SHA-256:

`e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f`

O contrato e o validador históricos do 08B1 não foram regenerados. O hash
anterior continua registrado naquele contrato; por isso ele não valida uma
base posterior com a correção. O validador 08B2 usa o contrato da base 043,
exige o hash novo e confere as dependências históricas do 08B1, com essa
única diferença documentada. Não restaura party_menu.c para fazer testes passar.

A integração 08B1 registra percurso no mGBA com scripts ativos, Rock Smash
e três resultados da batalha de Piraruaçu. Essas evidências pertencem ao
08B1; não são apresentadas como uma sessão nova do 08B2.

O ZIP 08B1 recuperado tem SHA-256
`74546587cc9b672574398ee9694b47435a0c5acb39a25995741cc3486e83136d`.
O `main` está em `979fb6c1b6`, 118 commits atrás da base 043. O pacote traz
incremento desde 043 e cumulativos desde 08B1 e a594; os mais antigos incluem
a correção do menu, a revisão 08A e as integrações correspondentes. Nenhum é
recuperação direta do main. Não houve push.

## Preservação e testes concluídos

| Elemento | Resultado |
|---|---|
| 754 layouts | IDs, ordem, dimensões e caminhos iguais; só dois pares de bancos mudam |
| Grade, borda e mapas | Todos os map.bin, border.bin e map.json byte a byte iguais |
| Scripts e progressão | Scripts, eventos, flags, encontros, conexões e warps intactos |
| Fóssil | O fóssil restante depende das flags de escolha originais; coleta e remoção intactas |
| Sunny Day | Evento em (7,5), finditem, item, flag de coleta e comum de itens preservados |
| Menu do Pokémon | Hash novo de party_menu.c protegido; nenhum trecho alterado pelo 08B2 |
| Metatiles | Os atributos completos dos dois pares iguais aos nativos; IDs mantidos |
| Silhuetas | 118 máscaras de camada comparadas, todas iguais às nativas |
| Água | 11.600 pixels comparados em oito quadros RGB555; todos iguais |
| Animações | 38 palavras de tiles animados no mapa e slots de DMA conservados |
| Demais gráficos do par | 892 IDs do Underpass e 903 do Slab visualmente idênticos |
| Correções anteriores | Centro 07H, água Palace, field_door.c e overworld.c preservados |

O flood de colisão/comportamento alcança as vizinhanças dos dois itens.
Underpass conserva 659 células acessíveis; ScorchedSlab conserva 111 com Surf
e somente a célula de entrada sem Surf. O teste ignora elevação e atores;
ele não substitui o percurso no emulador. A elevação foi conservada por bytes.

A varredura dos 528 mapas passa nos oito gates. Os três avisos de Surf em
EverGrande/Lilycove são anteriores. Também passam as proteções 08A e os gates
de paletas de atores, espécies especiais, facções e assets de personagens.
Logs, inventário, contrato e resultados estão em `review/desert_08b2`.

O instalador verifica hashes antes de escrever, protege a correção do menu,
recusa edições desconhecidas, faz backup, restaura em caso de interrupção e
reaplica sem novas escritas. Os testes de instalação e transporte seguem no
ZIP como INSTALL_TEST.json e CUMULATIVE_TEST.json.

## Aceitação pendente e reprodução

Este ambiente não possui compilador ARM nem mGBA. Os PNGs e o GIF são renders
dos assets nativos em RGB555, sem atores; não são capturas do emulador.
Compilar a ROM e conferir no mGBA:

- entrada/retorno pelo túnel da Rota 114, encontros e coleta do fóssil restante;
- entrada/retorno pela Rota 120, Surf, desembarque no patamar e coleta do TM;
- retorno após a coleta, sem reaparecimento dos objetos;
- continuidade do menu de HMs corrigido, inclusive Rock Smash no puzzle 08B1.

Preparação dos cabeçalhos e verificação sem ARM:

```sh
make -C tools/mapjson
tools/mapjson/mapjson groups emerald data/maps/map_groups.json data/maps include/constants
tools/mapjson/mapjson layouts emerald data/layouts/layouts.json data/layouts include/constants
python3 tools/arauna_maps/validate_desert_08b2.py
python3 tools/arauna_maps/desert_08b2.py render
python3 tools/arauna/audit_map_data.py
python3 tools/arauna_maps/check_visual_protection_08.py
```

São necessários Python 3, Pillow, fontes DejaVu e o compilador C++ do host.
O relatório histórico 08A permanece intacto. O inventário atualizado tem
480 mapas com banco Arauna, 16 módulos da Pyramid, 8 inativos e **24 nativos**.

Próximo pacote: **08B3 — Mirage Tower 1F–4F**, partindo do commit 08B2
registrado no manifesto, conservando party_menu.c e as correções anteriores.

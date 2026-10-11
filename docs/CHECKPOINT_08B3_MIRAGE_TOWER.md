# 08B3 — Mirage Tower 1F–4F V1

Quatro mapas concluídos sobre `a862cdee1d7e2c910abae6122b45951ea1690198`:
1F, 2F e 3F têm 21 × 17 células; 4F tem 13 × 10. Total: **1.201 células**.

## Ambientação e referências recuperadas

A Master Map Design Bible define a Rota 111 como semiárido, deserto e serra,
e pede que a Mirage Tower nasça do relevo desértico. Foi recuperado e lido
o PDF em `docs/referencias/bible_concepts_recuperados`, com o concept
`05_Rota_111_Semiarido_Deserto_Serra.png`. A torre interior segue o deserto,
sem importar o tema da Torre do Ruído ou da Torre Juramento, que são locais diferentes.

As paredes agora têm arenito avermelhado em camadas, faces escuras e bordas
gastas; a areia clara acumula nos percursos. Os maciços bloqueados recebem
estratos horizontais, substituindo a hachura diagonal herdada. Escadas e
saídas têm contraste mais claro. As rachaduras usam fraturas escuras; o
buraco tem um interior escuro e borda quebrada. O desenho foi feito na grade
nativa de pixels, preservando a forma das camadas e a leitura da colisão.

Um par exclusivo `arauna_mirage08b3` serve aos quatro andares: 41 IDs
redesenhados e 119 slots gráficos seguros. A paleta nova ocupa apenas a
linha 12 do par privado e usa valores representáveis em RGB555. Não há
aliases de câmera, novas rotinas C ou mudanças nos bancos compartilhados.

## Base e correções protegidas

O ZIP 08B2 recuperado tem 10.028.733 bytes e SHA-256
`a09ab2e29d94a554d0537607643e6eb27e25fa363f5878e5540c5d51e9c904d4`;
é o pacote já instalado, sem conteúdo novo. A branch do GitHub foi conferida
em `a862cdee1d`; `main`, em `979fb6c1b6`, está **121 commits atrás da base**.
O 08B3 parte da integração atual, incluindo `c01d55ba6`, e não de `646a270fdf`.

O contrato novo congela **24.258 arquivos anteriores**. Só os quatro registros
de gráficos permitem acréscimos controlados; em layouts.json, só os bancos
dos quatro andares mudam. Os hashes exigidos são:

| Arquivo protegido | SHA-256 |
|---|---|
| src/party_menu.c | e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f |
| src/field_player_avatar.c | 81ebe4b5761f8992cb459cf37978262358231734a1c56f8b3447346f770db95f |
| src/scrcmd.c | 98cd4b72474c3cc7dfd5dc6cf54a4a96f807733017761a2be58d62b0dcd063a9 |

Os contratos e validadores históricos 08B1 e 08B2 permanecem intactos. O
validador novo exige os hashes corrigidos e reconhece somente as diferenças
documentadas: três arquivos contra o contrato 08B1; dois contra o 08B2.
Não restaura versões antigas para fazer os validadores históricos passar.
Centro 07H, água do Palace, field_door.c, overworld.c e todos os pacotes
anteriores também ficam protegidos.

## Preservação e verificações concluídas

| Elemento | Resultado |
|---|---|
| 754 layouts | Mesmos IDs, ordem, dimensões e caminhos; quatro pares de referências mudam |
| Grade e bordas | Todos os map.bin e border.bin anteriores iguais por bytes |
| Eventos e progressão | map.json, scripts, objetos, encontros, flags e sete warps intactos |
| Piso frágil | 0x22F, atributo 0x10D2, nas mesmas 11 células do 2F e três do 3F |
| Buraco após quebrar | 0x206, atributo 0x0066, também redesenhado, embora ausente da grade inicial |
| Bicicleta, quedas e retornos | field_tasks.c, cave_hole.inc, callbacks e holewarps preservados |
| Rock Smash | Duas pedras no 3F e uma no 4F, scripts e flags temporárias intactos |
| Fósseis | Objetos, confirmação, escolha Root/Claw, ocultação e entrega preservados |
| Colapso e exterior | mirage_tower.c, sprites, tilemap, animação exterior e base da Rota 111 intactos |
| Atributos e callbacks | Arrays completos iguais; General / NULL preservados |
| Silhuetas | 82 máscaras de camada iguais, incluindo os estados de piso e buraco |
| Outros metatiles do par | 885 IDs visualmente idênticos aos nativos |
| Animações e gráficos | Alocação fora dos slots de DMA; tiles animados anteriores intactos |

A validação detectou e corrigiu uma reutilização indevida no cache de slots
livres durante a autoria. O construtor local exclui os slots que serão
sobrescritos do cache inicial; a verificação final compara todas as máscaras.
O editor compartilhado dos pacotes anteriores não foi alterado.

Passam a varredura dos 528 mapas nos oito gates e os gates de proteções 08A,
paletas de atores, espécies especiais, facções e assets de personagens.
Os três avisos de Surf de EverGrande/Lilycove são anteriores. Contrato,
resultados, logs e inventário atualizado estão em `review/mirage_08b3`.

O inventário agora tem 484 mapas com banco Arauna, 16 módulos gerados da
Pyramid, oito inativos e **20 mapas nativos restantes**. É cobertura dos
bancos, não aprovação artística nem aceitação completa de gameplay.

## Instalação e histórico

O ZIP contém o incremento sobre a862, o cumulativo desde o 08B2 do autor
(`646a270fdf`) e o cumulativo desde `a594b3e1e6`. Os cumulativos incluem as
correções e integrações intermediárias. Nenhum é recuperação direta de main.

O instalador confere o pacote e toda a base protegida antes de escrever,
recusa conteúdo corrompido e edições locais desconhecidas, faz backup,
restaura os arquivos em caso de falha e reaplica sem novas escritas.
INSTALL_TEST.json e CUMULATIVE_TEST.json no ZIP registram os resultados,
bases e limites dos testes de instalação e transporte. Não houve push.

## Aceitação de runtime ainda necessária para o novo 08B3

Este ambiente não tem compilador ARM nem mGBA. PNGs e GIF são renders dos
assets nativos sem atores; os dois estados do piso foram renderizados, mas
isso não executa o puzzle. A aceitação do 08B2 e do menu de HMs com o puzzle
08B1 foi concluída pelo integrador na base a862, conforme seu relato; ela
não é apresentada como um novo teste de gameplay dos quatro andares.

Após compilar a ROM, conferir no mGBA com scripts ativos e save carregado:

1. Entrar pela Rota 111, subir e retornar pelos sete warps dos quatro andares.
2. Cruzar o piso do 2F com Mach Bike; parar ou perder velocidade, ver a
   rachadura virar buraco e cair no andar inferior. Conferir os três pisos do 3F.
3. Usar Rock Smash pelo menu nas pedras do 3F e 4F, inclusive com um Pokémon
   que não conheça o golpe e com a insígnia exigida pela função atual.
4. Em saves separados, recusar e aceitar cada fóssil. Conferir item e flag
   correspondentes, desaparecimento dos objetos, colapso, queda na Rota 111
   e remoção da torre. Conferir a liberação do fóssil restante no Underpass
   no momento previsto pela progressão original.
5. Sair e voltar, conferir encontros selvagens e continuidade do menu de HMs.

## Reproduzir verificações no host

```sh
make -C tools/mapjson
tools/mapjson/mapjson groups emerald data/maps/map_groups.json data/maps include/constants
tools/mapjson/mapjson layouts emerald data/layouts/layouts.json data/layouts include/constants
python3 tools/arauna_maps/validate_mirage_08b3.py
python3 tools/arauna_maps/mirage_08b3.py render
python3 tools/arauna_maps/mirage_08b3.py gates
```

Python 3, Pillow, fontes DejaVu e compilador C++ do host são suficientes
para estas verificações. freeze exige a base a862 antes de instalar; build
usa o contrato congelado e os bancos nativos protegidos, sendo reexecutável.

Próximo checkpoint da fila: **08C — SSTidalCorridor, SSTidalLowerDeck e
SSTidalRooms** (três mapas), após integrar e aceitar o 08B3 sobre a base atual.

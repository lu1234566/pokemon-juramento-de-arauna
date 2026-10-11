# 08C — SS Tidal V1

Três mapas concluídos sobre `54c82e4430fcc3673afc3686db07fcb26ce755c8`:

| Mapa | Dimensões | Células |
|---|---|---|
| SSTidalCorridor | 18 × 13 | 234 |
| SSTidalLowerDeck | 17 × 13 | 221 |
| SSTidalRooms | 36 × 18 | 648 |
| Total | | **1.103** |

## Ambientação e referências recuperadas

A Master Map Design Bible e o concept `02_Porto_do_Sal.png` foram lidos antes
de editar. Porto do Sal é uma cidade portuária brasileira histórica, com
docas, armazéns e madeira de carga. Não há concept específico do SS Tidal
entre os arquivos recuperados. O Navio Perdido é outro local e não foi
usado como referência de abandono ou ruína para esta balsa em operação.

Os diálogos atuais já chamam o navio de ferry de Arauna, ligando Porto do Sal
e Baía das Luzes, com acesso ao Circuito após o convite de Bento. A direção
visual parte dessa função: corredor com pintura naval azul esverdeada,
chapa clara sobre o volume das cabines e piso de circulação fosco; cabines
com tábuas, mobiliário de madeira e tecidos listrados; porão com chapas
rebitadas, cargas de madeira e travessas diagonais nos caixotes.

Os materiais foram desenhados na grade nativa de pixels. Não são apenas
trocas de paleta: juntas, grãos, rebites, reforços e tecidos têm novos padrões.
O contorno das peças e a leitura dos volumes acompanham a colisão original.
Escadas, portas, escotilhas, camas e sinais continuam nas posições previstas.

Um par exclusivo `arauna_sstidal08c` serve aos três mapas. São **125 IDs
redesenhados e 207 slots gráficos seguros**. A linha 12 contém a paleta nova
em RGB555. As linhas 0–11 permanecem iguais; não há aliases de câmera nem
novas rotinas C. Bancos compartilhados e outros mapas permanecem protegidos.

## Portas animadas

As oito portas animadas usam quatro IDs fechados: `0x223`, `0x22B`,
`0x263` e `0x297`. Foram preservados os metatiles completos, incluindo
as vergas, seus gráficos e a paleta 7. O dourado fica como ferragem e moldura
sobre a madeira; não há restauração de um trecho com cores novas durante a
abertura. Os arquivos de animação e `field_door.c` são exatamente os da base.

Os IDs de porta continuam levando às entradas originais da tabela de
animações, que não depende do banco InsideShip neste caso. Nenhum ID novo
foi introduzido e os slots 1016–1023 usados pelas animações ficam reservados.
Os GIFs mostram os quadros originais nas molduras atuais, mais lentamente
para inspeção; não são execução do motor nem medição do tempo da animação.

## Base, integração e arquivos protegidos

O checkpoint 08B3 foi recuperado antes de editar. Seu ZIP tem SHA-256
`851b7655aeabb66983a4a45c07e9e0e51a13a64ccb044922c826baaeb13671f5`.
`docs/INTEGRACAO_08B3.md` registra o fast-forward do autor `062b84e92f`,
build e gates aprovados e percurso real no mGBA, inclusive quedas, bicicleta,
Rock Smash, ambos os fósseis, colapso e encontros. Não houve correção adicional.
Essas são evidências da integração anterior, não testes novos do 08C.

A branch do GitHub foi conferida em `54c82e4430`; `main`, em `979fb6c1b6`,
está **123 commits atrás da base solicitada**. O 08C parte de 54c, não apenas
do commit de autoria 062. Nenhum push foi feito.

O contrato novo congela **24.325 arquivos anteriores**. Só os quatro
registros de gráficos aceitam alterações controladas: acréscimos nos três
headers e troca dos bancos dos três mapas em layouts.json. Os hashes são:

| Arquivo protegido | SHA-256 |
|---|---|
| src/party_menu.c | e05f9efb61cfd652e56a361ba1e8b826f614abc0e684438a0b031b036679d08f |
| src/field_player_avatar.c | 81ebe4b5761f8992cb459cf37978262358231734a1c56f8b3447346f770db95f |
| src/scrcmd.c | 98cd4b72474c3cc7dfd5dc6cf54a4a96f807733017761a2be58d62b0dcd063a9 |

Os contratos históricos não foram regenerados. A validação reconhece as
três diferenças de integração contra o 08B1 e as duas contra o 08B2; contra
o contrato 08B3, todas as dependências conferem. Centro 07H, água do Palace,
field_door.c, overworld.c e todas as outras correções também ficam protegidos.

## Preservação e verificações concluídas

| Elemento | Resultado |
|---|---|
| 754 layouts | IDs, ordem, dimensões e caminhos iguais; somente os três pares de bancos mudam |
| Grade e bordas | Todos os map.bin e border.bin anteriores iguais por bytes |
| Eventos e warps | 15 objetos, 15 eventos de fundo e 22 warps do navio intactos |
| Colisão e comportamento | Arrays completos dos dois bancos iguais aos nativos |
| Silhuetas | 260 máscaras de camada verificadas, todas iguais |
| Outros metatiles do par | 639 IDs visualmente idênticos, incluindo os quatro IDs das portas |
| Animações | Callbacks General / NULL e gráficos animados anteriores preservados; alocação fora de DMA |
| Viagens | Estados, contador de passos, embarque, desembarque, destinos e warps dinâmicos intactos |
| Escotilhas | Oito sinais e a rotina de visão externa e retorno preservados |
| Cama | Interação em (15,11)/(15,12), cura e avanço da viagem intactos |
| Recompensas | TM Snatch, tratamento de bolsa cheia, flag e ocultação do doador preservados; Leftovers em (0,2) intacto |
| Batalhas e Circuito | Treinadores, flags de derrota, batalha dupla e convite de Bento preservados |

A varredura dos 528 mapas passa nos oito gates. Passam também as proteções
08A e os gates de paletas de atores, espécies especiais, facções e assets de
personagens. Os três avisos de Surf em EverGrande/Lilycove são anteriores.
Logs, contrato, resultados e inventário atualizado estão em `review/sstidal_08c`.

Agora há **487 mapas com banco Arauna**, 16 módulos gerados da Pyramid,
oito inativos e **17 mapas nativos restantes**: seis ilhas especiais, seis
Concursos e cinco mapas de conexão. A contagem mede cobertura dos bancos;
não representa aceitação completa da arte ou do gameplay.

## Instalação e cumulativos

O ZIP traz o incremento sobre 54c, um cumulativo desde o 08B3 do autor
(`062b84e92f`) e outro desde `a594b3e1e6`. Os cumulativos conservam as
integrações e correções intermediárias. Nenhum recupera diretamente main.

O instalador faz verificação completa dos hashes antes de escrever, exige
a base indicada ou o próprio checkpoint, recusa conteúdo corrompido e
edições locais desconhecidas, mantém backup, restaura após falha e reaplica
sem novas escritas. INSTALL_TEST.json e CUMULATIVE_TEST.json no ZIP registram
as instalações e importações efetivamente testadas, com os respectivos limites.

## Aceitação de runtime pendente para o novo 08C

Este ambiente não tem compilador ARM nem mGBA. PNGs e GIFs são renders dos
assets nativos sem atores. A preservação da lógica foi comprovada por hashes
e dados estáticos; não se apresenta uma viagem ou batalha simulada como gameplay.

Após compilar a ROM, conferir com save carregado e todos os scripts ativos:

1. Embarcar em Porto do Sal e Baía das Luzes, viajar nos dois sentidos e
   desembarcar nos portos corretos. Testar o convite de Bento e o acesso ao Circuito.
2. Entrar e sair das oito cabines e do porão, conferindo portas ao abrir e fechar.
3. Interagir com as escotilhas nos estados que mostram a viagem: vista externa,
   deslocamento, saída com B e retorno ao corredor.
4. Descansar na cama da cabine 2, conferir cura e avanço/chegada da viagem.
5. Jogar batalhas dos dois marinheiros e das cabines, incluindo a dupla;
   voltar depois de derrotar os treinadores, sem reiniciar flags.
6. Coletar TM Snatch e Leftovers, sair e voltar sem duplicação; conferir o
   doador após receber o TM e depois de desembarcar.
7. Salvar/carregar durante a viagem e conferir o menu de HMs corrigido ao
   retornar ao continente.

## Reproduzir verificações no host

```sh
make -C tools/mapjson
tools/mapjson/mapjson groups emerald data/maps/map_groups.json data/maps include/constants
tools/mapjson/mapjson layouts emerald data/layouts/layouts.json data/layouts include/constants
python3 tools/arauna_maps/validate_sstidal_08c.py
python3 tools/arauna_maps/sstidal_08c.py render
python3 tools/arauna_maps/sstidal_08c.py gates
```

Python 3, Pillow, fontes DejaVu e compilador C++ do host são suficientes
para estas verificações. freeze exige a base 54c antes de instalar; build
usa o contrato congelado e os bancos nativos protegidos, sendo reexecutável.

Próxima etapa: **08D — ilhas especiais** (seis mapas, em checkpoints),
após integrar e aceitar o 08C sobre a base atual.

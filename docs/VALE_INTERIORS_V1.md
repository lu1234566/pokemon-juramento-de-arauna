# Vale do Silêncio — nove interiores V1

A Bíblia, página 7, descreve um assentamento pequeno entre serras, jardins,
flores e pausa contemplativa. Não há concept interno próprio do Vale nos ZIPs
recuperados. Esta adaptação usa essa direção espacial e os módulos domésticos
nativos de Arauna já produzidos, sem apresentar outra casa como concept do Vale.

Três casas, uma venda, dois pisos do Centro e três ambientes do pavilhão de
batalha receberam madeira quente, paredes claras, janelas, mobiliário, plantas
e tecidos. O piso tem juntas discretas; as paredes combinam reboco e carpintaria.
A casa de Wanda tem espaço para os cinco moradores e o passeio de Val, sem
interferir em suas flags de presença. O balcão da venda usa MB_COUNTER.

As quatro salas domésticas/comerciais foram ampliadas: duas casas 12×11,
casa de Wanda 18×12 e venda 14×11. NPCs e portas foram reposicionados com
índices, destinos, scripts, itens, estoque e flags preservados. Os Centros
mantêm as dimensões; PC, escadas e portas de conexão conservam seus atributos
funcionais. Alguns NPCs do térreo foram deslocados para evitar os móveis.

O pavilhão mantém dimensões, eventos, colisões, elevações e atributos de cada
célula. Os sete percursos de entrada/saída verificados permanecem livres. Os
IDs da porta animada e sua paleta 9 foram mantidos. O banco adicional conserva
as definições originais e acrescenta os módulos visuais. O pavilhão continua
com suas regras de batalha herdadas; esta rodada não cria uma Casa da História.

São nove mapas, dezesseis warps e trinta e um objetos. O exterior já existente
não é reimplantado por este ZIP. Os scripts não são substituídos, permitindo
manter revisões de diálogo feitas em outra etapa. A validação compara os
comandos de roteiro e a identidade dos eventos, testa acesso aos NPCs e serviços,
o passeio de Val, os percursos do pavilhão e as portas abertas do andar de conexão.

O instalador verifica conflitos e guarda backup. O pacote é testado em checkout
limpo, reaplicado, reconstruído do atlas e passado pelo conversor mapjson.
Compilação de ROM, batalha real e conexão de cabo em emulador continuam pendentes.

## Instalação no repositório

- `VerdanturfTown_BattleTentLobby`: o pacote partia de uma base anterior ao
  lote 06 e traria de volta `OBJ_EVENT_GFX_SCOTT`. Entrou só o layout novo; o
  objeto continua `OBJ_EVENT_GFX_STEVEN`.
- Pavilhão (lobby, corredor, sala de batalha): mesmas dimensões, colisão,
  elevação e comportamento do layout antigo, tile a tile. A porta animada
  `METATILE_BattleTent_Door` mantém ID e comportamento.
- Warps: todos continuam sobre tiles de warp (tapete de saída, escada rolante,
  portas animadas do Cable Club). Todos os NPCs e eventos de texto ficam
  alcançáveis a partir da entrada.
- Metatiles trocados por código ou script (barreiras do Cable Club, porta do
  Cable Club, escada rolante) mantêm IDs e comportamento; o desenho é outro
  (escada de madeira, porta de madeira).
- Diferente do que diz o texto acima, os Centros não preservam todos os
  atributos. Interações que dependiam de comportamento de metatile e saíram
  com os móveis antigos:
  - Centro 1F: estante (`MB_POKEMON_CENTER_BOOKSHELF`) e mapa da região
    (`MB_REGION_MAP`); o PC mudou de lugar e continua funcionando.
  - Centro 2F: PC do balcão (`MB_PC`) e quadros de recordes de conexão
    (`MB_WIRELESS_BOX_RESULTS`, `MB_CABLE_BOX_RESULTS_2`).
  - Venda: prateleiras (`MB_SHOP_SHELF`). Casa da avaliadora: TV. Casa de
    Wanda: estante.
  - Devolvido depois: as prateleiras de potes e livros (metatiles
    0x226–0x227, presentes na venda, no Centro 1F e nas casas da avaliadora
    e de Wanda) respondem como estante (`MB_BOOKSHELF`).
- A enfermeira passou de (7,2) para (7,3), sem balcão entre ela e o jogador.
  A cura funciona no emulador; a Pokébola e o monitor da animação são sprites
  de posição fixa e caem sobre o móvel atrás dela.
- Build ARM, gates e emulador (nove mapas e uma cura completa) verificados.

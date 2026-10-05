# Quatro cidades — 48 interiores V1

| Cidade | Mapas | Warps | Objetos |
| --- | ---: | ---: | ---: |
| Campo das Cinzas | 8 | 14 | 25 |
| Casa da Cinza | 7 | 63 | 27 |
| Mata do Meio | 10 | 22 | 37 |
| Baía das Luzes | 23 | 57 | 147 |
| Total | 48 | 156 | 236 |

A Bíblia, páginas 8 e 9, e o concept 05 de Casa da Cinza orientam os materiais.
Não há concept individual dos interiores no conjunto recuperado. Os novos
sprites indexados são tiles nativos, não imagens decorativas sobre os renders.
Campo conserva vegetação e tecidos verdes junto da pedra clara; a cidade não
é reduzida a uma paleta marrom. Casa da Cinza combina pedra escura, madeira,
reboco quente e tecidos terracota. Mata usa tábuas e carpintaria verde. Baía
recebe calçamento e reboco claros, cores costeiras, tecidos azuis e madeira.

Os 48 layouts dedicados mantêm dimensões, map.bin e border.bin byte a byte
iguais à base. A única mudança em map.json é o layout. Eventos, flags, índices,
comandos de cena, movimentos e recompensas permanecem iguais. Diálogos não
são incluídos nem substituídos por este ZIP. Todos os atributos dos 19 bancos
secundários são idênticos às origens. Bancos primários não são modificados.

Novos desenhos ocupam somente slots gráficos não referenciados na base e
abaixo de 992. Nos bancos de museu, concurso e elevador, toda a faixa gráfica
original é reservada. Paletas de museu/elevador, alçapões termais e obstáculos
giratórios são preservadas. Quadros ativados por flags (metatiles 0x25A–0x263)
e as duas portinholas de concurso (0x2D1/0x2D9) conservam metadata exata.
Os 50 warps internos da Casa termal, barreiras giratórias, escadas, portas,
PCs e balcões seguem nos mesmos lugares, com os mesmos comportamentos.

As pranchas mostram todos os ambientes antes/depois. A contagem inclui o
UnusedMart legado e o terraço da loja; não equivale a esforço ou a todo o jogo.
Construção, renderização, validação e instalador com backup/recusa de conflitos
acompanham o pacote. Instalação, reaplicação, reprodução e conversão mapjson são
verificadas. Compilação de ROM e cenas executadas em emulador estão pendentes.

# Pokémon Juramento de Arauna — checkpoint 07H / Serviços V1

Base oficial `531352ce3715e41389382de692e917a32b9e60be`. Cinco serviços encerrados como arte nativa. **Frontier: 44/47; faltam os três exteriores do 07I.** Sem push.

## Referências e base

Master Map Design Bible recuperada em docs/referencias/bible_concepts_recuperados/Arauna_Master_Map_Design_Bible.pdf; conceitos Centro Comunitário e Sede da Liga Interior examinados. Pedra clara, madeira, cerâmica verde e bronze derivam dessa linguagem; os concepts não são evidência do jogo.

GitHub foi conferido antes das edições: branch do autor em 531; main em `979fb6c1b6731561f3c993efd6045a9bbf096c54`, 110 commits atrás da base. A base 531 acrescenta somente docs/INTEGRACAO_07G.md ao checkpoint `4122b9fa98db5604cb302468ff89dfc0145865a0`. O ZIP compacto 07G recuperado tem SHA256 `d13742675b2868fc4930c059b136e7f453cabb47c80247776f520d57e3b5f43c`; seus 164 arquivos fonte coincidem com 531. A integração registra compilação e fotos no mGBA do 07G, sem validar a nova ROM do 07H.

## Cinco mapas

| Mapa | Células | Células com arte alterada | Objetos | Warps |
|---|---:|---:|---:|---:|
| ExchangeServiceCorner | 165 | 158 | 9 | 3 |
| Mart | 88 | 88 | 4 | 2 |
| PokemonCenter_1F | 126 | 100 | 5 | 3 |
| PokemonCenter_2F | 140 | 97 | 4 | 3 |
| RankingHall | 795 | 469 | 3 | 2 |

Troca por BP: madeira e balcão de bronze. Mercado: cerâmica verde, estantes e limiar de cobre. Centro: pedra clara, equipamentos originais de cura, PC, escadas e comunicação. Galeria de recordes: pedra solene, placas verdes e frisos em bronze. Silhuetas funcionais e máscaras originais foram conservadas; a arte ocupa os mesmos metatiles.

## Preservação

1.314 células e bordas idênticas; 754 layouts conservam IDs, ordem e dimensões. Só cinco referências de bancos mudam; quatro pares privados atendem os mapas (o Centro compartilha o mesmo par nos dois pisos). Não há layouts acrescentados. Colisão, elevação, atributos, máscaras dos dois planos, paletas 0–11 e callbacks ficam exatos. A paleta 12 fornece os materiais.

25 objetos e 13 warps mantêm posições, movimentos, flags, scripts e destinos. O contrato congela **23.766 arquivos** da base, incluindo src/field_door.c e src/overworld.c. Trocas, preços e limites de BP, estoque do mercado, dinheiro, cura, PC, comunicação por link/wireless, condições de atendimento, placas de recordes, mistura de recordes, saves e progressão ficam byte a byte preservados. Os pisos substituídos por cable_club.inc (0x21E/0x25D e 0x2DC/0x2E4) são conferidos em dois estados; escadas, estação de cura e porta Cable Club conservam os pixels nativos.

## Evidências e limites

validation.json: PASS em 1.156 atributos, 2.312 máscaras estáticas e 1.428 máscaras em três quadros; 1.314 seleções C, 25.600 fallbacks e 53.167 células antigas de cavernas/Dive. Os **39 mapas anteriores** continuam visualmente iguais em 78 comparações, além de 14 comparações dos pisos gerados da Pyramid e oito quadros da água corrigida do Palace. Portas, TV, General, Dome, Pike e Pyramid usam verificações anteriores do C original no host; gerador da Pyramid passa 1.848 casos e 1.892.352 células.

Previews completos antes/depois e cinco câmeras 240×160 são renders RGB555 dos bancos 4bpp, sem atores. Nenhuma imagem é apresentada como foto do mGBA. Auditoria dos mapas e gates oficiais são registrados em audit_map_data.log e static_readiness.log. O gate estático omite expressamente a compilação ARM. **ROM e execução no mGBA pendentes: compilador ARM e emulador indisponíveis neste ambiente.** Scripts de serviços, compras, cura e recordes foram protegidos por hash, não jogados.

## Entrega e continuidade

ZIP com incremento/patch, instalador transacional, hashes e cinco bundles cumulativos desde 531, 4122, eb, 9f e 989. Cada ZIP fica estritamente abaixo de 30.000.000 bytes. O bundle integral de main foi excluído; a recuperação anterior entregue com o 07G continua em quatro volumes separados. Não sobreponha este incremento diretamente em main ou histórico divergente.

install_test.json comprova instalação real, rejeição de corrupção/edições, rollback, repetição e reprodução pelo builder. CUMULATIVE_TEST.json comprova importação real nos cinco receptores. Próximo: **07I — Outside East, Outside West e Reception Gate**, preservando animação de portas, bandeiras, água e conexões.

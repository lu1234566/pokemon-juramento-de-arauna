# Serra do Uivo V4 — blueprint de implementação

Referência: `review/serra_v4_concepts/Serra_do_Uivo.png`, recorte 04 do pacote de cidades fornecido pelo usuário. A Bíblia de produção define Serra do Mar, núcleo serrano e três patamares urbanos ligados por escadas. A Casa do Uivo é a etapa narrativa seguinte.

A paisagem combina rocha exposta, cascata principal com bacia, queda lateral, vegetação de altitude, pedra cinzenta e fachadas claras com madeira e telhados de ardósia/verde escuro. Tochas marcam as escadarias; um pequeno mirante e um trecho de trilho reforçam a identidade serrana.

- Patamar baixo: chegada, comércio, alojamentos, oficina e encontro com Ciro.
- Patamar médio: Casa da Terra, Centro, moradias, casa do Cortador e escola.
- Patamar alto: cascatas, centro técnico Horizonte, moradia, mirante e acesso às rotas 115/116.

Os 40×60 metatiles acomodam os onze edifícios e as doze entradas já existentes. A miniatura conceitual foi expandida para atender esse inventário; ela não representa todas as funções do mapa. Os sete tiles junto às conexões conservam IDs do General, e o contato aquático noroeste permanece compatível com a Rota 115.

A arquitetura é um banco secundário local em 4bpp. Os módulos minerais/folhagem partem de metatiles nativos e paletas locais; fachadas, pisos, cascatas e objetos são peças indexadas determinísticas. O General compartilhado permanece byte-idêntico. As quedas são cenário bloqueado, estático: não acrescentam exigência de Surf ou Waterfall.

As alturas físicas usam elevações 3, 5 e 7, com transições 0 nas escadas. Só duas passagens conectam os três bairros. As bordas norte e leste têm transições próprias para as rotas, ambas em elevação 3.

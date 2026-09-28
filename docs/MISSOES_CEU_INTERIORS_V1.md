# Missões do Céu — moradias e serviços V1

Sete interiores nativos 4bpp: quatro casas, loja e dois pisos do Centro Pokémon. O atlas deriva do concept visual fornecido para a cidade, com reboco costeiro, madeira verde azulada, telha terracota, piso de pedra, mapas de observação e mobiliário doméstico. Os layouts são próprios destes sete mapas; outros mapas que usam `HOUSE1`, `MART` e `POKEMON_CENTER` não mudam.

Instalação após o pacote do Centro Espacial V1: extraia o ZIP e execute `python3 tools/arauna_maps/apply_missoes_ceu_interiors_v1.py --target /caminho/do/repo`. `--check` verifica dependências. O instalador mescla os sete registros adicionais de layout e o banco de tiles ao projeto, guarda backup e aceita reaplicação. O exterior V2 pode ser aplicado antes sem conflito.

Três casas e a loja receberam ambientes novos, com NPCs e portas reposicionados. A Casa 2 preserva exatamente a colisão, elevação e os pontos de interação: o Wingull caminha por coordenadas fixas em dois trajetos. Nos Centros, os IDs e atributos de escada, Cable Club, portas e PC funcional são mantidos. Nenhum script de história foi substituído.

Os validadores conferem os sete acessos, NPCs, a abertura das duas passagens do Cable Club, o percurso do Wingull, metatiles especiais, orçamento 4bpp e registros. Os renders são dos dados nativos, sem sprites. ROM e emulador continuam pendentes; Casa de Bento, arena e dois andares da antiga Game Corner ainda necessitam arte própria.

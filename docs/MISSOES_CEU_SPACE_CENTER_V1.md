# Missões do Céu — Centro Espacial V1

Dois pisos visuais nativos 4bpp a partir do concept `10_Centro_Espacial_Missoes_do_Ceu.png` e da Bíblia de mapas, p. 48: hall científico público, observação, sala de preparo e plataforma. O banco novo usa piso claro, estrutura azul escura, consoles e luz âmbar. O atlas de produção está incluído para reprodução.

Instale o ZIP extraído com `python3 tools/arauna_maps/apply_missoes_ceu_space_center_v1.py --target /caminho/do/repo`. `--check` verifica conflitos. O instalador mescla apenas os dois registros de layout e os três blocos de declaração do tileset, de modo que também aceita a camada de exterior `Missoes_do_Ceu_V2`. Cria backup e aceita reaplicação. Os mapas e scripts de eventos são mantidos. As 320 células retêm os bits de colisão e elevação originais; o comportamento dos dois warps de escada e das duas saídas do térreo também foi copiado do banco Facility. Isso preserva a coreografia fixa do confronto no segundo andar.

O validador confere entradas, saídas, personagens, movimentos com coordenadas explícitas, orçamento de tiles, atributos de warp e registros. `mapjson` analisa ambos os mapas. Os renders são produzidos dos metatiles nativos, sem sprites. A ROM e as cenas em emulador ainda precisam ser verificadas. Demais interiores de Missões do Céu seguem pendentes.

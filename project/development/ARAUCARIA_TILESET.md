# Primeiro tileset autoral da Vila das Araucárias

Este pacote substitui os placeholders de Hoenn no `AraunaMapLab` por arte
original preparada para as limitações do Game Boy Advance.

## Estrutura

- 297 tiles únicos de 8 × 8 pixels em PNG indexado de 4 bits;
- 144 metatiles de 16 × 16 pixels;
- paleta conceitual quantizada para RGB555;
- uso do slot global 6, o primeiro slot do tileset secundário de Emerald;
- layout 20 × 20 com casas, posto de pesquisa, araucária ancestral e mata;
- colisões preservadas para a entrada, guia, Nilo e item de teste.

Os binários e o PNG estão versionados para que possam ser editados normalmente
no Porymap. O gerador reproduz somente a primeira revisão aprovada.

## Regeneração intencional

A regeneração sobrescreve o tileset e o layout atuais. Use-a apenas quando quiser
voltar à revisão-base:

```sh
python3 scripts/generate_arauna_tileset.py \
  --tileset-output data/tilesets/secondary/araucaria_village \
  --layout-output data/layouts/AraunaMapLab \
  --preview /tmp/araucaria-village-preview.png
```

O gerador usa apenas a biblioteca padrão do Python, verifica a contagem esperada
de tiles e produz bytes idênticos em execuções repetidas.

## Edição diária

Para alterações normais, abra o projeto no Porymap, selecione
`AraunaMapLab` e salve o mapa ou o tileset. Depois valide ambos os idiomas:

```sh
make ARAUNA_LANGUAGE=PORTUGUESE -j$(nproc)
make ARAUNA_LANGUAGE=ENGLISH -j$(nproc)
```

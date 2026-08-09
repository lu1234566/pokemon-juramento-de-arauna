# Integração integral da Dex de Arauna

- 386 entradas substituem, uma a uma, os slots nacionais 001–386.
- Slots de batalha dos iniciais: Torchic/Combusken/Blaziken, Mudkip/Marshtomp/Swampert e Treecko/Grovyle/Sceptile.
- 314 referências fornecidas foram convertidas para o formato do GBA.
- 72 entradas sem imagem receberam conceitos procedurais originais e reproduzíveis.
- Cada entrada tem frontal animada em dois quadros, traseira, ícone, paleta normal e paleta shiny.
- Nomes, tipos, atributos, altura, peso, descrição e evoluções por nível vêm de `pokedex.json`.
- Quinze nomes acima do limite técnico de 12 caracteres usam abreviação apenas dentro do motor; os nomes integrais permanecem no manifesto e no mapeamento.

A arte fonte de 010–314 só possui vista frontal. As traseiras desses números são reconstruções técnicas da silhueta para batalha; podem ser refinadas individualmente no mesmo slot sem alterar dados ou scripts.

## Formato de edição

O motor usa `src/data/graphics/arauna_fakemon_graphics.h`, um pacote C compacto com sprites de batalha em LZ77 padrão do GBA. Isso evita milhares de arquivos gerados no histórico do Git.

As versões editáveis estão em `graphics/arauna/arauna_editable_fakemon_assets.zip`. Cada pasta numerada contém `anim_front.png`, `back.png`, `icon.png`, `normal.pal`, `shiny.pal` e o perfil de produção. Extraia o ZIP em `graphics/arauna/editable`, altere o pacote desejado e execute `python tools/arauna/repack_arauna_graphics.py` na raiz do projeto para reconstruir o cabeçalho compacto.

As folhas de contato ficam em `docs/arauna/previews`, e o mapeamento exato entre número, nome e slot de batalha está em `ARAUNA_DEX_ENGINE_MAPPING.csv`.

## Limites conhecidos desta entrega

- Os 72 conceitos de 315–386 foram criados a partir de nome, tipos, categoria e inspiração porque não havia imagem de referência no pacote recebido.
- As traseiras de 010–314 são reconstruções de produção; podem ser trocadas uma a uma sem alterar a Pokédex.
- Golpes, habilidades e cries continuam herdados dos Pokémon usados como slots de batalha. Nomes, tipos, atributos, dimensões, textos e evoluções já são de Arauna.

# A dex de Arauna dentro do engine

As 386 espécies de Arauna estão instaladas. Este documento diz o que foi feito,
por qual regra, e onde mudar cada decisão.

## Os cinco geradores

Rodam nesta ordem. Todos aceitam `--check` (não escreve nada) e `--write`.

| Ferramenta | O que faz |
|---|---|
| `tools/arauna/build_species.py` | nomes, tipos, stats, habilidades, categorias, altura, peso, texto da dex, ordem da dex |
| `tools/arauna/build_evolutions.py` | as 81 evoluções aprovadas |
| `tools/arauna/build_sprites.py` | front, still, back, `normal.pal`, `shiny.pal` |
| `tools/arauna/build_icons.py` | ícones de party/box e as seis paletas compartilhadas |
| `tools/arauna/build_placement.py` | onde cada criatura aparece: encontros selvagens e times de treinador |
| `tools/arauna/build_movesets.py` | level-up, TM/HM, tutores e egg moves |

A fonte de tudo é `graphics/arauna/arauna_sprites_gba_export.zip`. O
`pokedex.json` dentro dele já trazia nome, tipos, stats, habilidades, categoria,
altura, peso e texto de dex das 386.

## Onde mudar as decisões

Cada julgamento que tive de fazer virou uma linha de CSV em `docs/arauna/`:

| Arquivo | Decisão |
|---|---|
| `ARAUNA_DEX_ENGINE_MAPPING.csv` | qual slot do engine cada número da dex ocupa |
| `ARAUNA_ABILITIES.csv` | habilidade de Arauna -> habilidade do engine, com o grau de fidelidade |
| `ARAUNA_NAMES_SHORT.csv` | forma de 10 caracteres dos 38 nomes que não cabem |
| `ARAUNA_CATEGORIES_SHORT.csv` | forma de 11 caracteres das 6 categorias que não cabem |
| `ARAUNA_EVOLUTIONS.csv` | as 81 relações |
| `ARAUNA_PLACEMENT.csv` | qual criatura responde por cada slot nos encontros e times |

Editar uma linha e rodar o gerador de novo é a forma de discordar de qualquer
escolha. Os geradores de placement e movesets leem sempre a última versão
commitada dos arquivos que alteram, então rodar `--write` duas vezes não empilha.

## Dois limites do engine que moldaram o resto

**Nomes têm 10 caracteres.** Não é só o campo de exibição: `SetBoxMonData`
copia `POKEMON_NAME_LENGTH` bytes para `BoxPokemon.nickname`, que tem 10 bytes e
faz parte do layout do save. Aumentar a constante não dá um nome maior — dá uma
escrita fora do campo, em cima de `language` e dos bits de bad egg. Por isso os
38 nomes longos têm forma curta explícita em vez de corte silencioso.

**O charmap não tem `ã` nem `õ`.** O resto do projeto já escreve português sem
eles. Toda string passa por transliteração antes de ser emitida e é conferida
contra `charmap.txt`. Um `ã` no fim da palavra vira `an`, o que mantém a leitura
nasal e, na prática, separa Boitatã de Boitatá e Iemanjã de Iemanjá.

## Campos derivados

O `pokedex.json` não traz catch rate, exp yield, EVs, egg groups, growth rate,
gender ratio nem body color. Nenhum foi inventado espécie por espécie; todos
saem de regra:

- **catch rate** pela posição na cadeia de evolução (lendário 3, final de cadeia
  de três 45, final de duas 60, meio 120, básico com evolução 190, isolado 90);
- **exp yield** = total de base stats / 3;
- **EVs** no stat mais alto, 2+1 para finais de cadeia e lendários;
- **egg groups** pelos dois tipos; lendário não bota ovo;
- **growth rate** lendário devagar, família de três médio-devagar, resto médio;
- **body color** medida da cor dominante do próprio sprite.

## Dex regional

A dex de Arauna é uma só, lida numa ordem só, então o número regional é igual ao
nacional. `HOENN_DEX_COUNT` continua 202, o que faz a dex regional ser
exatamente #001–#202 e deixa intacta a checagem de dex completa que a campanha
já usa.

## O que ainda é vanilla

- **Gritos.** Cada espécie usa o grito de quem morava no slot.
- **Footprints.** São pegadas 16×16 de duas cores e não há nada no export que
  corresponda a elas.
- **Texto da dex em inglês.** O texto está em português, como o resto dos dados
  do projeto; o build em inglês mostra português até existir um renderer.
- **20 das 46 habilidades** são aproximações de coisas que a terceira geração não
  tem (Harvest, Motor Drive, Prankster, Leaf Guard). Estão marcadas como
  `approximated` no CSV.

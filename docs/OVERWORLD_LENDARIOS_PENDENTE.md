# As quatro artes que faltam para o swap dos lendários

Este documento existe para que o próximo pacote de arte caia pronto. O registry
já aceita o formato; o que falta são quatro folhas.

## Correção ao que eu disse antes

Eu relatei que `OBJ_EVENT_GFX_ARAUNA_POKEMON_A/B` apontavam para o NinjaBoy e
concluí daí que não havia arte disponível. **Estava errado** — li a tabela
estática e parei nela. Os dois ids são **despachantes**: quem decide o gráfico é
`VAR_ARAUNA_OW_A`/`_B` em tempo de execução, e
`GetObjectEventGraphicsInfo` desvia para `gAraunaOverworldGraphicsInfo[canal][seleção]`,
que é o registry próprio de Arauana. O NinjaBoy é só o que sobra na tabela
estática para um id que nunca é lido por ela.

O problema que eu apontei continua de pé, mas pela razão que você deu: as quatro
criaturas do swap **não estão entre as 46 do registry**, e é isso que impede
selecioná-las hoje.

## O que já está pronto

O gerador `tools/arauna/build_overworld_registry.py` só sabia fazer 64×64 com
animação de caminhada. Agora ele aceita **um tamanho por criatura**, lido da
coluna `ow_size` de `docs/arauna/ARAUNA_OVERWORLD_46.csv`:

| `ow_size` | o que sai |
|---|---|
| 64 (padrão) | `.size = 2048`, 64×64, `inanimate = FALSE`, OAM 64×64, três poses |
| **32** | `.size = 512`, 32×32, `inanimate = TRUE`, OAM 32×32, **uma pose repetida nove vezes** |

A forma 32×32 é exatamente a que os Regis já usam neste repositório — um desenho
só, parado, metade dos tiles.

Isto foi provado das duas pontas:

- **as 46 existentes saem byte a byte idênticas** depois da mudança, nos quatro
  arquivos gerados. O refactor não move nada do que já funciona;
- a forma 32×32 foi exercitada com um manifesto sintético e emite
  `.size = 512`, `.width = 32`, `.inanimate = TRUE`,
  `&gObjectEventBaseOam_32x32`, `sOamTables_32x32`, os nove quadros apontando
  para o quadro 0, e a folha declarada com `-mwidth 4 -mheight 4`.

## O que o pacote de arte precisa trazer

Quatro criaturas, uma pose cada:

| dex | nome | espécie de engine | onde vai ficar |
|---|---|---|---|
| 338 | Verdejante | `SPECIES_SOLROCK` | Ancient Tomb |
| 342 | Terraão | `SPECIES_CRAWDAUNT` | Desert Ruins |
| 344 | Marulho | `SPECIES_CLAYDOL` | Island Cave |
| 347 | Estrelinha | `SPECIES_ANORITH` | Birth Island |

Para cada uma, dois arquivos com estes nomes exatos:

```
graphics/object_events/pics/pokemon/arauna/338_verdejante.png
graphics/object_events/palettes/arauna_338_verdejante.pal
```

**A folha:**

- **32×32 pixels**, uma pose só — não 96×32, não três poses;
- PNG **indexado**, 4 bits, **16 cores**, com o índice 0 transparente;
- olhando para o jogador (a pose "sul"), que é a única que o motor vai pedir.

Se alguma delas ficar melhor em 16×32, dá para acrescentar essa terceira forma
ao gerador — mas aí é preciso `gObjectEventBaseOam_16x32` e a tabela de
subsprites correspondente, então diga antes.

**A paleta:** `.pal` no formato JASC que o resto do diretório usa, 16 cores, a
primeira sendo a transparente.

## Como entra depois que a arte chegar

Quatro linhas no fim de `docs/arauna/ARAUNA_OVERWORLD_46.csv`, com `ow_size` 32,
e `python3 tools/arauna/build_overworld_registry.py --write`. O gerador cuida
das constantes, das duas cópias por canal, das pic tables e das declarações de
gráfico. `ARAUNA_OW_COUNT` passa de 47 para 51.

Uma etiqueta de paleta nova por criatura entra junto. Isso não disputa banco de
hardware: o despachante mantém só duas criaturas residentes por vez, uma por
canal, então crescer o registry custa espaço de tabela e não banco.

## E só então o swap

Com as quatro no registry, cada câmara troca o seu `object_event` para
`OBJ_EVENT_GFX_ARAUNA_POKEMON_A` e ganha um `setvar VAR_ARAUNA_OW_A, ARAUNA_OW_…`
no `ON_TRANSITION` do mapa, e o `setwildbattle` passa a nomear a criatura e o
nível novos. Aí a arte e a batalha voltam a concordar, que é a condição que fez
eu segurar o swap.

## Uma nota sobre o encontro sem overworld

Você tem razão de que ele é possível: o motor não exige que `setwildbattle`
venha de um `object_event` — um `coord_event` serve. O que eu disse e que estava
certo é que **não existe exemplo pronto disso no repositório**: a Marine Cave,
que o desenho cita como ambiental, tem `OBJ_EVENT_GFX_KYOGRE_FRONT` no chão. É
um caminho a construir, não a copiar — e, como você diz, não é o caminho destes
quatro, que são criaturas presentes na câmara.

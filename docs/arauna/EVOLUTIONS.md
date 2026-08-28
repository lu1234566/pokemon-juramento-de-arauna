# Evoluções de Arauna — design aprovado e como aplicar

O design está fechado e validado. **Ainda não foi aplicado**, por um motivo
técnico concreto explicado abaixo.

## O que está versionado

| Arquivo | Conteúdo |
|---|---|
| `docs/arauna/ARAUNA_EVOLUTIONS.csv` | as 81 relações aprovadas (origem, alvo, nível, decisão) |
| `docs/arauna/ARAUNA_DEX_ENGINE_MAPPING.csv` | qual espécie do engine cada número da dex de Arauna ocupa |
| `tools/arauna/build_evolutions.py` | valida o design e gera `src/data/pokemon/evolution.h` |

Fonte: planilha `Arauna_Evolucoes_e_Overworld_PreLancamento.xlsx`, aba
`Evolucoes_386`. Todas as 81 usam `EVO_LEVEL` — sem troca, pedra, amizade ou
horário — o que era o objetivo declarado para reduzir risco antes do playtest.

## Validação

`python3 tools/arauna/build_evolutions.py --check` confere e hoje passa limpo:

- nenhuma espécie evolui para si mesma;
- nenhum alvo recebe duas espécies diferentes;
- nenhum ciclo;
- níveis entre 2 e 80;
- em cadeias de 3 estágios, o nível **sempre cresce**.

São 81 relações, 22 delas no meio de uma cadeia, formando 59 famílias.

A planilha também corrige 6 alvos que estavam errados no manifesto anterior — o
mais grave sendo **#163 Corurupim, que apontava para si mesmo** e agora aponta
para #164 Coruja. Os outros cinco (#220, #224, #228, #300, #313) apontavam para
espécies fora da própria família.

## Aplicado

A dex de Arauna entrou (`tools/arauna/build_species.py`), entao
`species_names.h` deixou de dizer BULBASAUR e o gerador passou a escrever
sozinho. `src/data/pokemon/evolution.h` agora tem as 81 relacoes aprovadas:

    [SPECIES_TORCHIC]   = {{EVO_LEVEL, 17, SPECIES_COMBUSKEN}}, // #001 Caramelo -> #002 Caramelao

As 172 relacoes vanilla sairam: 130 evolucoes por pedra, troca e amizade
deixaram de existir e 39 novas entraram. Isso e o desenho aprovado -- toda
evolucao de Arauna e por nivel.

Para regenerar depois de mexer nos CSVs:

```
python3 tools/arauna/build_evolutions.py --check
python3 tools/arauna/build_evolutions.py --write
```

## Observação sobre a aba `Overworld_23`

Essa aba descreve o formato-alvo dos 23 overworlds como
`16×32 por frame • 9 frames • 144×32` para **todos**. Isso não corresponde ao
engine: os slots têm formatos diferentes — 16×16 (Caramelo, Capivim, Botim,
Camaleão, Tuiuiú, Preazinho, Beija-Flor), 16×32 (Morphália, Jequitibá,
Corpo-Seco, Curupixel), 32×32 (a maioria dos lendários e médios) e 64×64
(Arauá). A integração já feita usa o formato real de cada slot; a linha da
planilha é uma simplificação e não deve ser usada como especificação.

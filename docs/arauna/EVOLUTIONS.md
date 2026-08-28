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

## Por que ainda não foi aplicado

Um número da dex de Arauna **não é** um id de espécie do engine. Pelo mapeamento
oficial, #001 Caramelo mora em `SPECIES_TORCHIC` e #007 Pimpau em
`SPECIES_TREECKO`. As relações só fazem sentido depois de traduzidas por esse
mapeamento.

O ponto é que **`main` ainda carrega a dex vanilla**: `species_names.h` continua
dizendo BULBASAUR, IVYSAUR, KINGLER. A tabela de espécies de Arauna
(`species_info/arauna_dex.h`) nunca chegou aqui.

Aplicar as relações agora escreveria, em constantes do engine, coisas como:

    [SPECIES_RATICATE] = {{EVO_LEVEL, 34, SPECIES_SPEAROW}}
    [SPECIES_FEAROW]   = {{EVO_LEVEL, 18, SPECIES_EKANS}}

Correto para Arauna, sem sentido para a dex que está compilada de fato. Além
disso, as 81 relações substituiriam as 172 atuais: **130 evoluções vanilla
seriam removidas** (pedras, Eevee, trocas) e 39 novas adicionadas. O gerador se
recusa a escrever enquanto detectar a dex vanilla instalada.

## Como aplicar quando a dex de Arauna entrar

```
python3 tools/arauna/build_evolutions.py --check    # confere o design e o impacto
python3 tools/arauna/build_evolutions.py --write    # gera evolution.h
```

O `--write` passa a funcionar sozinho assim que `species_names.h` deixar de
conter os nomes vanilla. Existe `--force` para casos excepcionais, mas ele
contorna exatamente a proteção descrita acima.

## Observação sobre a aba `Overworld_23`

Essa aba descreve o formato-alvo dos 23 overworlds como
`16×32 por frame • 9 frames • 144×32` para **todos**. Isso não corresponde ao
engine: os slots têm formatos diferentes — 16×16 (Caramelo, Capivim, Botim,
Camaleão, Tuiuiú, Preazinho, Beija-Flor), 16×32 (Morphália, Jequitibá,
Corpo-Seco, Curupixel), 32×32 (a maioria dos lendários e médios) e 64×64
(Arauá). A integração já feita usa o formato real de cada slot; a linha da
planilha é uma simplificação e não deve ser usada como especificação.

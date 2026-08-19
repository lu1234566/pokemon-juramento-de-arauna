# Localização — estado atual em 2026-08-19

## Escopo deste protótipo

A localização bilíngue foi reconstruída sobre a `main` atual apenas para a introdução de Professora Anahi. O objetivo é restaurar uma prova técnica segura de que duas variantes de texto podem ser compiladas a partir do mesmo commit sem criar branches permanentes por idioma.

Este trabalho NÃO significa que o jogo inteiro esteja traduzido para inglês.

## Fontes

A introdução usa os mesmos nove labels internos nas duas variantes:

- `data/text/arauna/pt_br/birch_speech.inc`;
- `data/text/arauna/en/birch_speech.inc`.

`data/text/birch_speech.inc` funciona somente como seletor e preserva os labels/fluxo que a engine do Emerald já usa.

## Seleção e pipeline

A macro de pré-processador `ARAUNA_LANGUAGE` define a variante:

- `0` = inglês;
- `1` = português brasileiro.

Se a macro não for informada, o seletor define `1`, preservando o comportamento atual da `main` em português.

A seleção precisa acontecer na etapa do `cpp`, não no GNU assembler. A regra de dados do Makefile executa uma primeira passagem do `preproc` do pokeemerald, depois o `cpp`, depois uma segunda passagem do `preproc` antes do assembler. Como o primeiro `preproc` expande diretivas `.include` de forma imediata, o seletor usa `#include`: assim o `cpp` elimina o idioma não selecionado antes que a segunda passagem converta as `.string` em bytes do charmap.

## Builds isoladas

Use:

```bash
bash scripts/build_arauna.sh ptbr -j2 all
bash scripts/build_arauna.sh en -j2 all
```

O wrapper injeta `ARAUNA_LANGUAGE` no comando do `cpp`, usa diretórios de build separados e nomes de ROM distintos para evitar reutilização acidental de objetos entre as duas variantes.

Como a build é moderna (`MODERN=1`), os nomes resultantes seguem o padrão do Makefile e incluem `_modern`.

## Validação

`scripts/check_localization.py` verifica:

- a mesma ordem de labels nos dois idiomas;
- equivalência dos placeholders;
- limite máximo de 32 caracteres visíveis por linha;
- caracteres disponíveis no `charmap.txt`.

O limpador `tools/cleanup_intro_speech_residue.py` foi adaptado para validar a fonte pt-BR e o seletor bilíngue sem reintroduzir Birch/Littleroot na superfície visível.

A CI executa o contrato de localização e tenta compilar as duas variantes de introdução de forma independente.

## Limitações conhecidas

- o restante do jogo ainda mistura grande volume de texto autoral pt-BR com superfícies sistêmicas herdadas em inglês;
- não existe seleção de idioma em runtime neste protótipo;
- `ã`, `õ`, `Ã` e `Õ` continuam dependentes da etapa de fonte/pixel art registrada na issue #9;
- por isso, o pt-BR provisório evita esses glifos quando necessário;
- nomes próprios de Arauna, como `VILA AMANHECER`, permanecem iguais na variante inglesa neste estágio para não criar um segundo cânone de nomes de lugares.

## Próximo passo técnico

Expandir a mesma arquitetura de maneira incremental para superfícies alcançáveis do jogo, começando por textos sistêmicos e pós-game que ainda aparecem em inglês, sempre preservando labels, fluxo de eventos, flags, warps e formato de save.

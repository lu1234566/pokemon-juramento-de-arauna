# Localização — inventário técnico inicial

Estado: 2026-08-19

Este inventário fecha o escopo técnico inicial da issue #5. Ele descreve o sistema realmente presente na `main` atual; não tenta reconstruir a arquitetura antiga de branches históricas.

## Onde o texto aparece

A base `pokeemerald` usada por Arauna concentra texto visível principalmente em:

- `data/maps/**/scripts.inc` — diálogos, placas, eventos de mapa e mensagens ligadas à campanha;
- `data/text/*.inc` — textos compartilhados e superfícies sistêmicas;
- `src/strings.c` e tabelas C relacionadas — strings de engine/UI que não vivem em scripts de mapa;
- arquivos de dados específicos de subsistemas, quando a própria engine os referencia diretamente.

A passagem narrativa de Arauna já reescreveu uma grande quantidade de `data/maps/**/scripts.inc`, enquanto partes sistêmicas herdadas do Emerald ainda precisam de migração incremental.

## Charmap e pré-processamento

- `charmap.txt` define os caracteres e tokens reconhecidos pela pipeline de texto do GBA.
- Strings `.string` não vão diretamente para o GNU assembler: o `tools/preproc` do projeto converte o texto usando o charmap.
- Para unidades de dados `.s`, a regra relevante do Makefile segue a ordem:

  `preproc -> cpp -> preproc -> assembler`

- A primeira passagem expande diretivas assembler `.include`.
- A seleção da introdução bilíngue, portanto, usa `#include` controlado pelo `cpp`; isso impede que os dois idiomas sejam incluídos antes da seleção.

## Protótipo bilíngue atual

A introdução de Professora Anahi usa duas fontes equivalentes:

- `data/text/arauna/pt_br/birch_speech.inc`
- `data/text/arauna/en/birch_speech.inc`

O seletor está em `data/text/birch_speech.inc` e usa `ARAUNA_LANGUAGE`:

- `0` — inglês;
- `1` — português brasileiro;
- ausência da macro — português brasileiro por padrão.

O wrapper `scripts/build_arauna.sh` cria builds isoladas para cada variante da introdução, evitando reaproveitamento acidental dos mesmos objetos.

## Validação existente

`scripts/check_localization.py` verifica no protótipo:

- mesma ordem de labels;
- placeholders equivalentes;
- largura máxima de 32 caracteres visíveis por linha;
- disponibilidade dos caracteres no charmap.

Os validadores de resíduos também cobrem várias superfícies de Arauna para impedir reintrodução de nomes/falas antigas do Emerald.

## Limitações conhecidas do inventário

- a introdução é a única superfície com fonte pt-BR/en paralela formal neste estágio;
- grande parte da campanha autoral está em pt-BR, enquanto várias mensagens sistêmicas herdadas continuam em inglês;
- `ã`, `õ`, `Ã` e `Õ` dependem da issue #9 porque exigem desenho/validação das fontes;
- ainda não há seleção de idioma em runtime, e isso não é requisito do protótipo M1;
- a expansão futura deve ser feita por superfícies alcançáveis, preservando labels e fluxo, em vez de duplicar branches por idioma.

## Decisão sobre Poryscript

**Decisão do M1: Poryscript não é dependência do protótipo de localização.**

Razões:

1. o projeto atual já possui grande volume de scripts ASM `.inc` integrados e funcionando sobre o grafo do Emerald;
2. introduzir Poryscript apenas para provar duas fontes de idioma aumentaria o escopo sem resolver um problema necessário do protótipo;
3. a seleção pt-BR/en acontece antes do assembler e funciona independentemente da linguagem usada para escrever os eventos;
4. migrar eventos para Poryscript pode ser avaliado separadamente se trouxer ganho de manutenção para scripts novos, mas não deve ser condição para localizar conteúdo existente.

Assim, o M1 mantém os scripts atuais e trata localização como uma camada de fontes/seleção/validação, não como uma migração de linguagem de scripting.

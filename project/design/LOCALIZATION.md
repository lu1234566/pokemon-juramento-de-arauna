# Arquitetura de localização

## Decisão

A primeira demo terá dois patches, `pt-BR` e `en`, gerados do mesmo código-fonte. Mapas, eventos, dados e mecânicas serão compartilhados; apenas textos e recursos explicitamente localizados poderão variar.

Não serão mantidas branches permanentes por idioma.

## Princípios

- Português brasileiro é o idioma autoral.
- Inglês é uma adaptação natural, não tradução palavra por palavra.
- Toda fala possui uma identidade estável independente do idioma.
- O comprimento dos textos não pode alterar lógica, flags ou sequência de eventos.
- Nomes, termos e pronomes são registrados no glossário.
- Uma mudança narrativa não é concluída até existir nos dois idiomas ou estar marcada explicitamente como pendente.

## Estrutura implementada no primeiro protótipo

O idioma é escolhido em tempo de compilação. As duas builds usam o mesmo commit, lógica e dados compartilhados:

```bash
make ARAUNA_LANGUAGE=PORTUGUESE -j$(nproc)
make ARAUNA_LANGUAGE=ENGLISH -j$(nproc)
```

Os resultados são `pokeemerald-ptbr.gba` e `pokeemerald-en.gba`. Cada idioma possui seu próprio diretório de objetos para impedir que arquivos compilados de uma língua sejam reutilizados pela outra.

Os primeiros textos autorais estão organizados assim:

```text
data/text/arauna/
  en/
    birch_speech.inc
  pt_br/
    birch_speech.inc
```

`data/text/birch_speech.inc` seleciona exatamente uma fonte durante o build. O script `scripts/check_localization.py` confirma que os idiomas possuem os mesmos identificadores e placeholders e rejeita linhas acima do limite conservador do protótipo.

O nome interno `Birch` e o sprite original permanecem placeholders técnicos. Eles não definem o pesquisador final de Arauna.

### Limitação tipográfica conhecida

O charmap herdado contém vários acentos latinos, mas ainda não possui glifos para `ã`, `õ` e suas formas maiúsculas. O protótipo usa redação natural que evita temporariamente esses caracteres; a versão pública deverá implementar e testar os glifos em vez de remover acentos corretos do português.

## Identificadores

Exemplo conceitual:

```text
INTRO_RESEARCHER_GREETING
STARTER_GRASS_DESCRIPTION
BOND_RUINS_COURAGE_CHOICE
```

Os identificadores não devem conter o texto traduzido. Uma ferramenta de validação futura verificará chaves ausentes, duplicadas e conteúdo provisório.

## Glossário mínimo

| Conceito | pt-BR | en | Observação |
|---|---|---|---|
| Região | Arauna | Arauna | Não traduzir |
| Juramentos | Juramentos | Oaths | Nome do sistema histórico |
| Vínculos | Vínculos | Bonds | Consequências narrativas |
| Coragem | Coragem | Courage | Tendência |
| Sabedoria | Sabedoria | Wisdom | Tendência |
| Compaixão | Compaixão | Compassion | Tendência |
| Noite Sem Estrelas | Noite Sem Estrelas | Starless Night | Evento histórico |
| Vila das Araucárias | A definir | To be defined | Nome precisa funcionar nos dois idiomas |
| Rota da Neblina | A definir | To be defined | Nome precisa funcionar nos dois idiomas |

## Fases

### Fase 1 — Fundação

- [x] inventariar o fluxo da introdução e o charmap;
- [x] escolher organização compatível com o build;
- [x] criar glossário inicial;
- [x] implementar um diálogo de teste em cada idioma;
- [ ] compilar as duas builds na CI;
- [ ] medir diferença de tamanho e comportamento no emulador.

### Fase 2 — Vertical slice

- localizar todos os textos autorais;
- gerar duas builds do mesmo commit;
- testar caixas, variáveis e nomes;
- gerar patches separados.

### Fase 3 — Seleção em runtime

Somente após o vertical slice, avaliar:

- armazenar os dois bancos de texto na mesma ROM;
- tela antes do primeiro save;
- preferência registrada no save;
- troca posterior nas opções;
- impacto em memória e tamanho;
- migração de saves.

Se qualquer requisito ameaçar o cronograma, os dois patches continuam sendo a solução oficial.

## Definition of done de uma fala

- texto `pt-BR` revisado;
- texto `en` revisado;
- terminologia consistente;
- variáveis e nome do jogador preservados;
- quebra de linha testada no jogo;
- nenhum corte ou overflow;
- contexto e emoção equivalentes.

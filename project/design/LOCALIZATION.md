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

## Estrutura pretendida

A estrutura final será definida depois de mapear o sistema de textos do motor. O objetivo conceitual é equivalente a:

```text
project/localization/
  glossary.csv
  pt-BR/
  en/
```

Arquivos compilados pelo motor poderão permanecer nas pastas nativas. A organização acima representa a fonte autoral, não uma alteração antecipada do pipeline.

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

- inventariar textos e charmap;
- escolher organização compatível com Poryscript e o build;
- criar glossário;
- compilar um diálogo de teste em cada idioma;
- medir diferença de tamanho e comportamento.

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

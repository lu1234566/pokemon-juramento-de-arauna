# Plano da Pokédex de Arauna — 386 espécies

## Objetivo

Substituir integralmente os 386 slots da Pokédex do Emerald por espécies que pareçam pertencer à mesma região, tenham funções ecológicas reconhecíveis e ofereçam variedade real de equipes durante a campanha.

`386` significa espécies individuais, contando cada estágio evolutivo. A meta de produção inicial é aproximadamente 186 famílias:

| Estrutura | Famílias-alvo | Espécies |
|---|---:|---:|
| Linhas de três estágios | 60 | 180 |
| Linhas de dois estágios | 80 | 160 |
| Espécies de estágio único | 46 | 46 |
| **Total** | **186** | **386** |

Essa distribuição é um orçamento de design, não uma obrigação imutável. Qualquer mudança precisa preservar o total de 386 e ser registrada.

## Slots confirmados

| Slots | Linha | Tipos ao final | Estado |
|---|---|---|---|
| 001–003 | Projeto Pica-pau | Grass/Rock | conceito confirmado; arte pendente |
| 004–006 | Projeto Caramelo | Fire/Dragon | conceito confirmado; arte pendente |
| 007–009 | Projeto Quero-quero | Water/Bug | conceito confirmado; arte pendente |
| 010–386 | a definir em lotes | diversos | reservado |

## Orçamento por habitat primário

Cada espécie recebe um habitat primário para impedir que a Pokédex seja preenchida sem planejamento. Uma espécie pode aparecer em zonas de transição ou outros biomas quando houver justificativa ecológica.

| Habitat primário | Slots-alvo |
|---|---:|
| Mata das Araucárias e Mata Atlântica | 54 |
| Floresta Amazônica e grandes rios | 52 |
| Cerrado e veredas | 42 |
| Caatinga, cânions e sertões | 36 |
| Pantanal e planícies alagáveis | 36 |
| Pampas e campos | 28 |
| Litoral, manguezais e ilhas | 38 |
| Serras, cavernas, minerais e fósseis | 34 |
| Ambientes urbanos, rurais e industriais | 28 |
| Ruínas, espécies antigas, guardiões e míticos | 38 |
| **Total** | **386** |

## Regras de composição

- Todos os 18 tipos precisam de representação durante a campanha, não apenas no pós-jogo.
- Nenhum bioma pode ser dominado por um único tipo.
- Cada terço do jogo oferece pelo menos uma família viável para funções comuns: atacante físico, atacante especial, parede, suporte, controle de velocidade e utilidade de campo.
- Espécies de início de jogo não serão tratadas como descartáveis; algumas devem continuar competitivas até a Liga.
- Tipos raros recebem disponibilidade planejada, mas não artificialmente tardia.
- Evoluções por troca terão alternativa acessível sem depender de outro jogador.
- Diferenças entre versões não bloquearão a conclusão da Pokédex em um único patch.
- Nenhuma família será desenhada apenas para preencher número.

## Ficha obrigatória de cada família

Antes de qualquer sprite, a família precisa ter:

1. número e codinome;
2. inspirações biológicas, culturais ou materiais;
3. habitat e nicho ecológico;
4. silhueta e arco evolutivo descritos;
5. tipos e justificativa;
6. função de batalha e faixa de stats;
7. habilidades e assinatura, se houver;
8. método e nível de evolução;
9. ponto de obtenção na campanha;
10. riscos de semelhança excessiva com designs oficiais ou de terceiros;
11. aprovação conceitual.

Somente depois dessa aprovação começa o fluxo de concept art e sprites.

## Estados de produção

`reservado` → `pitch escrito` → `conceito aprovado` → `silhueta aprovada` → `sprite frontal aprovado` → `pacote gráfico aprovado` → `dados integrados` → `QA completo`

O status será rastreado por slot. Nenhuma coluna pode ser pulada silenciosamente.

## Lotes de produção

### Lote 0 — Trio inicial

- slots 001–009;
- valida toda a cadeia de conceito, sprite, animação, ícone, dados, evolução, Pokédex e save;
- somente depois de concluído autoriza produção paralela de famílias comuns.

### Lote 1 — Ecossistema inicial

- 12 a 18 espécies da Mata das Araucárias e Rota da Neblina;
- inclui mamífero inicial, ave comum, inseto, espécie noturna, espécie de água doce e encontro raro;
- serve ao vertical slice definitivo.

### Lotes seguintes

- lotes de 12 a 24 espécies organizados por habitat e ponto da campanha;
- cada lote precisa compilar nos dois idiomas e passar por teste de Pokédex, evolução, batalha e save;
- arte rejeitada permanece fora do jogo, usando placeholder técnico identificado quando necessário.

## Balanceamento e dados

- O orçamento total de BST será comparado por estágio evolutivo e momento de obtenção.
- Habilidades exclusivas serão exceções; primeiro reutilizar comportamentos estáveis do motor.
- Golpes autorais entrarão somente quando o conceito não puder ser expresso com o conjunto existente.
- Learnsets devem refletir anatomia, ecologia e progressão, não apenas cobertura competitiva.
- Formas shiny precisam continuar legíveis nas paletas e telas do GBA.

## Compatibilidade técnica

- Os IDs internos serão mapeados com cuidado para não quebrar saves, espécies de scripts ou tabelas do motor.
- A migração dos 386 slots ocorrerá em uma branch dedicada e por lotes testáveis.
- Placeholders nunca serão apresentados como arte final.
- Sprites, ícones, footprints, cries e dados relacionados serão auditados por tamanho e formato.
- Builds `pt-BR` e `en` precisam manter paridade de espécies e textos.

## Critério de conclusão

Uma espécie só é considerada concluída quando possui pacote gráfico aprovado, dados balanceados, localização nos dois idiomas, habitat válido, evolução testada, entrada de Pokédex, cry autorizado e testes de save sem regressão.

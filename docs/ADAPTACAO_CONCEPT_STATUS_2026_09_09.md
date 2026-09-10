# Adaptação às concept arts — situação em 9 de setembro de 2026

A contagem abaixo trata da **adaptação visual/espacial ao padrão reforçado pelo usuário**, com dados nativos revisáveis. Não é uma porcentagem de conclusão do jogo: o código existente já contém progressão, traduções e versões anteriores de muitos mapas, enquanto a nova narrativa descrita na Bíblia ainda tem lacunas.

## Quanto falta

| Frente do Design Bible | Escopo espacial adaptado | Ainda exige trabalho |
|---|---:|---:|
| Cidades e assentamentos — exterior | 6 de 16 | 10 |
| Rotas 101–134 | 1 de 34 | 33 |
| Dungeons e áreas especiais | 0 de 15 | 15 conjuntos |
| Casas da História | 2 de 8 | 6 |
| Locais narrativos dedicados | 6 de 13 | 7, incluindo os interiores da Liga |

**Nos exteriores das cidades, 37,5% passaram por esta nova rodada; faltam 62,5%.** As dez restantes já possuem trabalhos anteriores de reconstrução, que precisam de revisão de fidelidade às referências. Não devem ser descartadas automaticamente nem contadas como concluídas no novo padrão.

Vila Amanhecer e Pampa da Espera tiveram o lote completo de vila e interiores fechado nesta rodada. Pampa inclui sete mapas internos e quinze salas, com o Ginásio/Casa do Pampa, três casas, venda e dois andares do Centro. As outras 14 cidades ainda têm interiores a adaptar/revisar, embora alguns ambientes específicos já estejam prontos, como Casa da Terra, Casa da Maré e Casa do Uivo. Esses interiores não estão integralmente quantificados nas categorias da Bíblia.

As cinco categorias somam 86 **entradas de planejamento**, das quais 15 têm o escopo espacial correspondente adaptado e 71 ainda exigem trabalho. **Isso não representa 86 mapas independentes nem uma porcentagem do esforço total.** A própria Bíblia repete lugares sob funções diferentes: Arquivo Central e Memorial, por exemplo, aparecem em dungeons e locais narrativos. Há conjuntos com vários andares/estados, além dos interiores comuns. Por isso não há uma porcentagem global de esforço nem prazo em dias confiável neste momento.

## Exteriores já adaptados nesta rodada

Vila Amanhecer V9; Vila da Passagem V1; Pampa da Espera V1; Serra do Uivo V4; Porto das Redes V1; Liga/Ever Grande V2.

## Exteriores ainda a revisar pelas referências

Porto do Sal; Encruzilhada Central; Vale do Silêncio; Campo das Cinzas; Casa da Cinza; Mata do Meio; Baía das Luzes; Missões do Céu; Águas de M’Boi; Casa da Fogueira no slot de Pacifidlog.

## O que a palavra “adaptado” não inclui

- A visita espacial à Casa do Uivo está implementada, mas o arco U03–U11, batalha, Selo e Libras ainda estão pendentes.
- Casa da Terra e Casa da Maré preservam Dalva/Ademar e a progressão atual; os novos arcos da Bíblia não estão certificados como implementados.
- Primeira Câmara tem portão/altar funcionais, mas não o Sistema de Vínculos completo.
- Pampa V1 e Interiores V1 fecham o lote espacial da cidade. Elias, os sete treinadores e as recompensas existentes foram preservados; a nova narrativa/chancela da Casa do Pampa na Bíblia permanece pendente.
- Build ARM completo e teste em emulador continuam pendentes para a cadeia de mapas. Renders, conversão `mapjson` e fixtures C não substituem esses testes.

## Base da auditoria

Índice e seções I–V do Master Map Design Bible fornecido (16 cidades, 34 rotas, 15 áreas, 8 Casas, 13 locais). Referências antigas conflitantes são explicitadas; o código atual governa responsáveis, IDs, flags e recompensas. O texto da Bíblia e a lista completa com evidências estão no pacote: `review/pampa_v1_references/design_bible_full_text.txt` e `review/arauna_adaptacao_concepts_2026_09_09.csv`.

Foram conferidos os commits locais da rodada de concepts (`926f201` até `55fd170`, mais Pampa Interiores V1) e os relatórios/pacotes existentes da cópia cumulativa. A contagem diferencia exterior de interior e adaptação espacial de narrativa nova. Não presume que o nome de um ZIP ou uma revisão textual certifique a arte.

Próxima prioridade natural: continuar a revisão das dez cidades externas restantes, começando por Porto do Sal, e fechar os lotes de interiores das cidades já adaptadas. Os trajetos e o código atual devem permanecer preservados.

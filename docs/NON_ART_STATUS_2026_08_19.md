# Status técnico sem arte — 2026-08-19

Este documento registra o estado da `main` após o ataque técnico de 19/08/2026 e separa trabalho técnico/narrativo de dependências visuais.

## Arquitetura vigente

A referência técnica atual é `docs/ARAUANA_STORY_IMPLEMENTATION.md`:

- preservar o grafo de eventos do Pokémon Emerald;
- preservar ordem de progressão, warps, flags e identificadores internos;
- reutilizar os slots funcionais do Emerald;
- substituir a superfície visível por Arauna;
- evitar alterações de save quando a mudança é apenas narrativa/visual.

A antiga estratégia de criar seis mapas dedicados ao vertical slice foi supersedida pela arquitetura atual.

## Implementado sem depender de arte nova

### Superfície narrativa

- passagem narrativa de Arauna aplicada a mais de uma centena de arquivos de scripts de mapas;
- Ciro ocupa a função narrativa do rival;
- Professora Anahi ocupa a função narrativa de Birch;
- Consórcio Horizonte e Lembrantes substituem as facções relevantes na superfície visível;
- Serra do Uivo, Porto das Redes, Encruzilhada Central, Casa da Cinza, Pampa da Espera, Mata do Meio, Missões do Céu e M'Boi possuem correspondência de ginásio/localidade em limpadores dedicados;
- Seu Bento substitui resíduos visíveis ligados a Steven nos alvos cobertos e, no pós-game do laboratório, assume a função visível da ligação herdada de Scott;
- protagonista e Ciro possuem cânone/voz consolidados e a antiga issue #2 está concluída.

### Limpeza de resíduos do Emerald

A `main` possui treze validadores/aplicadores incrementais:

1. placas e identidades centrais;
2. Match Call;
3. Ciro em rotas;
4. residência inicial;
5. mensagens de batalha;
6. Vila Amanhecer;
7. introdução;
8. nomes do mapa regional;
9. identidade de UI/sistema;
10. Route 119;
11. núcleo doméstico de Val;
12. avaliação da Pokédex;
13. fluxos sistêmicos/pós-game do laboratório de Anahi.

O lote #13 removeu os seis resíduos rastreados pela issue #123 sem alterar comandos de evento, labels, flags, vars, progressão ou save.

### Localização

- a introdução de Anahi possui fontes pt-BR/en paralelas e seleção por `ARAUNA_LANGUAGE` no estágio correto do `cpp`;
- `scripts/build_arauna.sh` isola as duas variantes de build;
- `scripts/check_localization.py` verifica labels, placeholders, largura e charmap;
- o inventário técnico e glossário-base concluíram o protótipo M1 da antiga issue #5;
- o restante do jogo ainda requer expansão incremental por superfície alcançável, não tradução global cega.

### CI e proteção da `main`

A proteção da `main` exige os contextos `repository-safety` e `build-and-test`. A CI foi alinhada a esses nomes:

- `repository-safety` executa os treze checks de resíduos e o contrato bilíngue;
- a matriz compila pt-BR e inglês;
- `build-and-test` agrega o resultado e só passa quando a validação e ambas as builds passam.

## Pendências técnicas que não exigem arte

### P0 — execução real da CI

Os runners observados em 19/08/2026 continuam encerrando jobs antes do primeiro step (`steps: null`), inclusive antes do Checkout. Quando o serviço voltar a aceitar jobs:

- confirmar `repository-safety`;
- confirmar as builds pt-BR/en;
- confirmar `build-and-test`;
- tratar apenas logs produzidos depois do Checkout como evidência de falha do código.

### P1 — expansão incremental da localização/resíduos

Ainda existe conteúdo sistêmico e secundário herdado do Emerald fora dos alvos protegidos. A regra é expandir a cobertura por superfícies realmente alcançáveis e canonicamente definidas, preservando labels, fluxo, flags, warps e formato de save.

Não há issue não-art aberta para um próximo lote específico neste momento; um novo lote deve nascer de resíduo confirmado, com escopo delimitado antes da edição.

### P2 — manutenção de documentação

Documentos históricos de plano devem permanecer como histórico, mas documentos de estado precisam ser atualizados quando uma issue é concluída para não reabrir trabalho já integrado.

## Fora deste ataque porque depende de arte

- issue #3 — concept art dos iniciais;
- issue #9 — glifos `ã/õ/Ã/Õ` nas fontes;
- issue #31 — direção visual/tileset da Vila das Araucárias;
- sprites finais, portraits, tilesets, ícones e conversões que exijam conferência pixel a pixel.

## Regra para próximas tarefas

Antes de implementar uma issue antiga, conferir se seus caminhos, mapas, documentos e arquitetura ainda existem na `main`. Se não existirem, classificar a issue como supersedida ou reescrevê-la para o estado atual antes de produzir código. O PR legado #58 permanece fora de escopo.

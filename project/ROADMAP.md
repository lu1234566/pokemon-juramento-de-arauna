# Roadmap da versão definitiva

Este roadmap parte de uma decisão de produção: Arauna terá mapas, nomes, eventos, encontros e história próprios, mas reutilizará prioritariamente os gráficos de cenário do Emerald. O esforço autoral de arte será concentrado nos Pokémon.

## M0 — Escopo definitivo

**Estado:** concluído na documentação; aguardando integração do PR de escopo.

- [x] Confirmar *Pokémon: Juramento de Arauna* como projeto definitivo.
- [x] Confirmar português brasileiro e inglês.
- [x] Confirmar tom maduro, protagonista falante e Sistema de Vínculos.
- [x] Expandir a inspiração para todo o Brasil dividido em macrobiomas ficcionais.
- [x] Confirmar substituição dos 386 slots da Pokédex do Emerald.
- [x] Confirmar pica-pau Grass/Rock, caramelo Fire/Dragon e quero-quero Water/Bug.
- [x] Formalizar aprovação obrigatória de sprites.
- [x] Confirmar mapas novos com reutilização prioritária dos gráficos do Emerald.
- [x] Aprovar a proposta B como silhueta-base do Projeto Caramelo.

## M1 — Base limpa para a nova direção

**Objetivo:** remover o cenário autoral como bloqueador sem desfazer a fundação técnica existente.

- [ ] Integrar o PR de escopo depois da revisão de Lucas.
- [ ] Marcar o passe visual autoral anterior como substituído, preservando seu histórico.
- [ ] Criar branch limpa para a Vila das Araucárias com tilesets originais do Emerald.
- [ ] Manter o tileset autoral antigo fora dos mapas ativos, sem exclusão destrutiva inicial.
- [ ] Corrigir entrada da casa, entrada do laboratório, saída da vila e retorno da rota.
- [ ] Validar colisões, warps, save/reload e retorno entre os seis mapas existentes.
- [ ] Compilar `pt-BR` e `en` e testar no mGBA.

**Saída:** Vila das Araucárias navegável, reconhecível como jogo de GBA e sem depender de novos gráficos de cenário.

## M2 — Vertical slice funcional

**Objetivo:** concluir a primeira hora usando placeholders claramente identificados.

- [ ] Fechar o fluxo casa–vila–centro de pesquisa–rota–ruína–câmara.
- [ ] Implementar introdução, escolha do inicial, tutorial e rival Nilo.
- [ ] Implementar primeira decisão de Vínculo e suas três consequências.
- [ ] Implementar miniboss, revelação do guardião e encerramento do slice.
- [ ] Definir encontros provisórios e curva de níveis.
- [ ] Escrever primeiro em `pt-BR` e localizar para `en` após o fluxo estabilizar.
- [ ] Terminar o slice sem comandos de debug.

**Saída:** história jogável de 30 a 60 minutos nos dois idiomas, ainda sem exigir arte final das 386 espécies.

## M3 — Lote 0 da Pokédex: trio inicial

**Objetivo:** validar a cadeia completa de produção de Fakemon antes da escala industrial.

- [x] Aprovar a silhueta-base B do Projeto Caramelo.
- [ ] Aprovar folha refinada e sprite frontal 64 × 64 do Caramelo.
- [ ] Aprovar silhuetas e sprite frontal do Pica-pau.
- [ ] Aprovar silhuetas e sprite frontal do Quero-quero.
- [ ] Definir nomes, habilidades, stats, evoluções e learnsets das três linhas.
- [ ] Aprovar formas intermediárias e finais.
- [ ] Aprovar sprites traseiros, ícones, animações e shinies.
- [ ] Integrar slots 001–009 em branch isolada.
- [ ] Testar escolha, batalha, evolução, Pokédex e save.

**Saída:** nove espécies concluídas e um processo repetível para os demais lotes.

## M4 — Planta completa da Pokédex

**Objetivo:** fechar os 386 conceitos antes de produzir centenas de imagens.

- [ ] Criar registro estruturado dos slots 001–386.
- [ ] Distribuir aproximadamente 186 famílias evolutivas.
- [ ] Definir habitat, tipos, função de batalha e ponto de obtenção de cada família.
- [ ] Auditar representação dos 18 tipos e funções de equipe por trecho da campanha.
- [ ] Marcar espécies originais e eventuais formas regionais que exigem aprovação específica.
- [ ] Reservar guardiões, míticos, fósseis, pseudo-lendários e encontros especiais.
- [ ] Validar que a soma final permanece exatamente 386.

**Saída:** Pokédex inteira planejada em texto e dados, sem exigir que todos os sprites já existam.

## M5 — Vertical slice apresentável

**Objetivo:** substituir os placeholders do primeiro bioma por conteúdo aprovado.

- [ ] Concluir 12 a 18 espécies da Mata das Araucárias e Rota da Neblina.
- [ ] Integrar somente pacotes gráficos aprovados.
- [ ] Finalizar encontros, treinadores e balanceamento do primeiro arco.
- [ ] Revisar textos `pt-BR` e `en`.
- [ ] Realizar teste com cinco pessoas.
- [ ] Gerar patches privados reproduzíveis.

**Saída:** primeiro pacote realmente apresentável de Arauna.

## M6 — Esqueleto da região completa

**Objetivo:** construir toda a geografia jogável antes de polir cada cidade.

- [ ] Definir ordem dos macrobiomas e dos oito Selos.
- [ ] Criar mapas greybox com tilesets do Emerald.
- [ ] Implementar conexões, retornos, habilidades de campo e atalhos.
- [ ] Distribuir cidades, rotas, cavernas, ruínas e áreas opcionais.
- [ ] Implementar a campanha principal com placeholders de conteúdo.
- [ ] Validar que o jogo pode ser concluído do início à Liga.

**Saída:** campanha completa em greybox, sem depender de 386 sprites finalizados.

## M7 — Produção da Pokédex e dos capítulos

**Objetivo:** substituir placeholders em lotes de 20 a 24 espécies.

- [ ] Produzir cada lote por habitat e momento de obtenção.
- [ ] Separar aprovação de conceito, sprite frontal e pacote gráfico.
- [ ] Integrar dados, encontros, treinadores e textos após aprovação.
- [ ] Compilar e testar os dois idiomas a cada lote.
- [ ] Fechar cada capítulo somente quando seus encontros essenciais estiverem prontos.

**Marcos internos:**

- 60–80 espécies: Demo pública 1 e dois Selos;
- aproximadamente 193 espécies: alpha regional e quatro Selos;
- 300 espécies: campanha completa em beta interno;
- 386 espécies: Pokédex e pós-jogo completos.

## M8 — Beta

- [ ] Oito Selos, Liga, finais e pós-jogo essencial.
- [ ] 386 espécies obtíveis ou registráveis.
- [ ] Auditoria de encontros, evoluções, tipos e balanceamento.
- [ ] Auditoria de textos, fontes, créditos e aprovações de arte.
- [ ] Testes em mGBA, outros emuladores e hardware quando possível.
- [ ] Compatibilidade de saves congelada.
- [ ] Zero bloqueadores conhecidos.

## M9 — Versão 1.0

- [ ] Localização `pt-BR` e `en` revisada integralmente.
- [ ] Patches públicos reproduzíveis, sem ROM completa.
- [ ] Guia de aplicação, créditos e documentação final.
- [ ] Repositório preparado para correções pós-lançamento.

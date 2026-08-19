# Status técnico sem arte — 2026-08-19

Este documento registra uma auditoria da `main` atual e separa trabalho técnico/narrativo de dependências visuais. A intenção é impedir que backlog histórico seja confundido com a arquitetura realmente usada pelo jogo hoje.

## Arquitetura vigente

A referência técnica atual é `docs/ARAUANA_STORY_IMPLEMENTATION.md`:

- preservar o grafo de eventos do Pokémon Emerald;
- preservar ordem de progressão, warps, flags e identificadores internos;
- reutilizar os slots funcionais do Emerald;
- substituir a superfície visível por Arauna;
- evitar alterações de save quando a mudança é apenas narrativa/visual.

A antiga estratégia de criar seis mapas dedicados ao vertical slice não está presente na `main` atual e foi tratada como supersedida.

## Implementado sem depender de arte nova

### Superfície narrativa

- passagem narrativa de Arauna aplicada a mais de uma centena de arquivos de scripts de mapas;
- Ciro ocupa a função narrativa do rival;
- Professora Anahi ocupa a função narrativa de Birch;
- Consórcio Horizonte e Lembrantes substituem as facções relevantes na superfície visível;
- Serra do Uivo, Porto das Redes, Encruzilhada Central, Casa da Cinza, Pampa da Espera, Mata do Meio, Missões do Céu e M'Boi já possuem correspondência de ginásio/localidade em limpadores dedicados;
- Seu Bento substitui resíduos visíveis ligados a Steven nos alvos já cobertos.

### Limpeza de resíduos do Emerald

O repositório já possui validadores/aplicadores para:

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
12. avaliação da Pokédex.

A CI principal passa a executar esses doze validadores em modo `--check` para prevenir regressões.

### Documentação e manutenção

- README voltou a descrever Pokémon Juramento de Arauna em vez do README puro do `pokeemerald`;
- CI ganhou `workflow_dispatch`, concorrência controlada e job independente de validação estática;
- issue #28 foi encerrada como arquitetura supersedida;
- issue #5 foi mantida aberta porque a estratégia bilíngue histórica não está mais integrada na `main` atual;
- issue #9 foi explicitamente mantida fora deste lote porque seus critérios dependem de glifos/fontes em pixel art;
- issue #2 permanece aberta: Ciro e parte do cânone estão integrados, mas os critérios completos de protagonista/voz/documentação ainda não estão satisfeitos.

## Pendências técnicas que não exigem arte

### P0 — validar o estado atual quando o runner do Actions voltar a aceitar jobs

- executar `Arauna static validation`;
- executar `Build Emerald base`;
- revisar qualquer falha real de script/compilação;
- não confundir falha anterior à criação de steps com falha de código.

### P1 — localização bilíngue

A `main` atual não possui mais a antiga camada `ARAUNA_LANGUAGE`/build dupla. O trabalho correto é redesenhar a localização a partir do estado atual, levando em conta que muitos scripts autorais já estão em pt-BR e grande parte da base sistêmica do Emerald continua em inglês.

Evitar simplesmente restaurar o PR histórico: ele foi criado para uma estrutura de projeto que já mudou.

### P1 — cobertura de resíduos fora dos alvos atuais

Os validadores existentes protegem superfícies selecionadas, não todo o texto do Emerald. Ainda existe grande volume de texto genérico em inglês em módulos de sistema, Match Call genérico, pós-game e conteúdo secundário. A expansão deve ser incremental e orientada por superfícies realmente alcançáveis no jogo.

### P1 — laboratório inicial / pós-game

O laboratório de Anahi já tem grande parte dos blocos autorais convertidos, mas ainda há mensagens sistêmicas herdadas em inglês em fluxos como upgrade da Pokédex/National Dex e nickname de presentes. Esses resíduos devem ser tratados em um lote técnico próprio, preservando labels e fluxo.

### P2 — documentação de cânone

Consolidar documentos antigos de planos/lotes em uma referência de estado evita repetir trabalho já aplicado. Não apagar histórico útil; marcar claramente o que é plano, implementação concluída ou arquitetura supersedida.

## Fora deste ataque porque depende de arte

- sprites finais de personagens;
- tilesets autorais novos;
- revisão visual final de cidades quando exige novos tiles;
- glifos `ã/õ/Ã/Õ` nas fontes;
- retratos, ícones e demais GFX;
- qualquer conversão final de sprite/fonte que exija conferência pixel a pixel.

## Regra para próximas tarefas

Antes de implementar uma issue antiga, conferir primeiro se seus caminhos, mapas, documentos e arquitetura ainda existem na `main`. Se não existirem, classificar a issue como supersedida ou reescrevê-la para o estado atual antes de produzir código.

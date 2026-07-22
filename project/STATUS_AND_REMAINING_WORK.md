# Estado do projeto e trabalho restante

Atualizado em 22 de julho de 2026. Este documento distingue implementação em
branches de trabalho de conteúdo realmente compilado, testado e aprovado.

> Nota de revisão (22/07): a suíte `repository-safety` do CI, que antes reprovava
> em pelo menos dez passos, está **19/19 verde** (18 validadores Python + o check
> de arquivos proprietários). Os oito chefes de ginásio, os quatro da Elite e o
> Campeão já foram reskinados como chefes de Arauna preservando os level caps. O
> único bloqueio remanescente é de infraestrutura: o GitHub Actions não aloca
> runner (billing/minutos), o que impede o build real e a geração do
> `pokeemerald-en.gba` para teste.

## Estado atual

| Área | Estado | Observação |
| --- | --- | --- |
| Escopo e direção | Definido | Brasil por biomas, 386 slots e Sistema de Vínculos; primeira versão jogável em inglês |
| Vila e mapas do slice técnico | Implementado em PRs | Gráficos do Emerald; falta teste integrado no mGBA |
| Ambientação e clima dos mapas | Passe aplicado | Música/clima recanonizados (tom mais sombrio) na vila, laboratório, Rota da Neblina, Porto, Centro de Pesquisa e rotas reutilizadas |
| História técnica inicial | Implementado em PRs | Estágios 0–8, Nilo, Rota da Neblina, Ruína e Câmara do Primeiro Elo |
| Bíblia narrativa canônica | Dois arcos em greybox | Porto reutiliza Route 109/Slateport; Serra reutiliza Fallarbor/Route 114/Meteor Falls |
| Pokédex de Arauna | Integrada na PR #47 | 386 nomes, dados, evoluções, learnsets, perfis e slots próprios |
| Ecologia e treinadores | Integrado na PR #47 | Encontros, espécies protegidas, dificuldade e equipes possuem auditorias reproduzíveis |
| Chefes (ginásios + Elite + Campeão) | Reskinados | 13 chefes de Arauna sobre os slots de líder/Elite/Campeão; level caps, tamanhos de time e tiers de IA preservados; nenhuma espécie protegida em treinador |
| Level cap por campanha | Implementado | Curva completa de 8 insígnias (`GetFullCampaignLevelCap`) mais os caps de história do prólogo |
| Sensibilidade cultural | Corrigido | Orixá (Oxum, #109) removido de dado de batalha do Agente; validadores reconciliados |
| Artes dos Fakemon | Integradas tecnicamente na PR #47 | Aprovação visual por lotes ainda é necessária; nenhuma nova arte deve entrar sem aprovação |
| Sprites de NPC personalizados | Prontos, não integrados | 16 assets validados em `.integration/npc_v3/`; integração aguarda aprovação (ADR-024) e runner |
| QoL básica | Ativa na PR #47 | Apenas recursos sem efeito relevante sobre progressão ou formato do save |
| QoL intermediária | Bloqueada por marco | EXP Share global, DexNav e serviços aguardam a segunda insígnia jogável |
| Segundo teste da ROM | Preparado em branch | Save novo, percurso até a Uivo Badge e 999 Rare Candies de teste entregues uma única vez no laboratório |
| Suíte `repository-safety` do CI | Verde (19/19) | Todos os validadores e o check de arquivos proprietários passam no head atual |
| Build e teste do head atual | Bloqueado por infraestrutura | Primeira versão força inglês e gera `pokeemerald-en.gba`; Actions não aloca runner (billing/minutos) |

## Roster de chefes (level caps inalterados)

Cada chefe reutiliza o slot de treinador do líder/Elite/Campeão original,
mantendo classe, tamanho de time, tiers de IA e o ás segurando item. Só mudam
nome, apresentação e a equipe (espécies não protegidas de Arauna).

| Slot original | Chefe de Arauna | Classe | Ás (segura item) |
| --- | --- | --- | --- |
| Roxanne | Bento | Hiker | Jumpluff @ Oran (15) |
| Brawly | Nabor | Bird Keeper | Dodrio @ Sitrus (19) |
| Wattson | Ivo | Ruin Maniac | Wailord @ Sitrus (24) |
| Flannery | Brás | Kindler | Glalie @ Sitrus (29) |
| Norman | Tião | Fisherman | Duskull @ Sitrus (31) |
| Winona | Iracema | Aroma Lady | Wynaut @ Sitrus (33) |
| Tate & Liza | Gêmeas | Twins (duplo) | Cyndaquil @ Sitrus (42) |
| Juan | Severino | Expert | Swinub @ Sitrus (46) |
| Sidney | Lázaro | Elite Four | Vigoroth @ Sitrus (49) |
| Phoebe | Rosa | Elite Four | Exploud @ Sitrus (51) |
| Glacia | Clara | Elite Four | Yanma @ Sitrus (53) |
| Drake | Tibúrcio | Elite Four | Gardevoir @ Sitrus (55) |
| Wallace | Augusto | Campeão | Ralts @ Sitrus (58) |

## Pacote do segundo teste

- A versão de teste continua exclusivamente em inglês e deve gerar
  `pokeemerald-en.gba`.
- Ao confirmar o inicial no Centro de Pesquisa, Dr. Maia entrega 999 Rare
  Candies como suprimento temporário de teste.
- A entrega usa uma flag exclusiva, não pode ser duplicada e volta a ser
  oferecida ao falar com Maia somente se a mochila estava sem espaço.
- O teste deve usar um save novo e seguir
  `docs/arauna/SECOND_ROM_TEST_CHECKLIST.md`.
- EXP Share global, DexNav e serviços de natureza/habilidade continuam
  desativados até o percurso ser compilado e validado no mGBA.
- As Rare Candies são instrumentação da segunda build e devem ser removidas
  ou condicionadas antes de uma versão pública.
- O passo de upload do artefato já existe em `build.yml`: um `workflow_dispatch`
  manual publica o `pokeemerald-en.gba` como artefato `pokeemerald-en-gba`
  (retenção de 7 dias) assim que houver runner.

## O que falta para estabilizar a PR #47

- [x] Deixar a suíte `repository-safety` verde (19/19) no head atual.
- [x] Executar todas as auditorias e validadores do repositório localmente.
- [ ] Restaurar um runner capaz de iniciar o checkout ou compilar no Codespaces.
      **Bloqueio de conta:** depende de Settings → Billing → Actions do dono do
      repositório; não é resolúvel por código.
- [ ] Fazer um build limpo da versão inglesa ativa (depende do runner).
- [ ] Testar no mGBA: save novo, escolha, captura, whiteout, save/reload, três
      Vínculos, miniboss, Pokédex no Centro de Pesquisa e epílogo.
- [ ] Corrigir qualquer falha encontrada no teste real.
- [ ] Revisar o lote visual completo; sprites não aprovados continuam candidatos.
- [ ] Aprovar e integrar os 16 sprites de NPC de `.integration/npc_v3/` (ADR-024).
- [ ] Integrar a pilha de PRs na ordem correta.
- [ ] Gerar apenas patch privado de teste, nunca uma ROM completa no repositório.

## Próximo marco de campanha

A Bíblia Narrativa v1.3 define a sequência canônica que deve substituir o slice
técnico atual:

1. Prólogo na Vila Amanhecer, com escolha segura entre Caramelo, Querô e Pimpau.
2. Ciro recebe o inicial de vantagem primária e Anahí recebe o terceiro.
3. Arco 1, Porto das Redes: Iaraço, Iara-Mãe e Insígnia da Maré.
4. Arco 2, Serra do Uivo: Lobisomem desbotado, comunicação em Libras e Insígnia do Uivo.

A QoL intermediária só pode ser ativada depois que esse percurso estiver
implementado, compilado e testado com save novo.

## O que falta da Pokédex e da arte

- [ ] Revisar os 386 pacotes visuais em lotes aprováveis.
- [ ] Aprovar e integrar os 16 sprites de NPC (10 overworld + 6 retratos de
      treinador), já prontos e validados em `.integration/npc_v3/`.
- [ ] Substituir os 386 cries herdados, que continuam como placeholders de áudio.
- [ ] Fazer revisão final de habitats, capturas especiais e Testemunhos contra a
      Bíblia Narrativa v1.3.
- [ ] Validar o conjunto completo em build real e em hardware/emulador.

## O que falta da campanha completa

- [x] Definir oito Insígnias/Casas de História e os biomas principais.
- [x] Definir o eixo narrativo e os cinco Testemunhos.
- [x] Reskinar os oito chefes de ginásio, os quatro da Elite e o Campeão como
      chefes de Arauna, mantendo os level caps do Emerald.
- [x] Aplicar o passe de ambientação/clima nas localidades do slice.
- [ ] Converter a Bíblia v1.3 em mapa de cenas, diálogos, flags e objetivos.
- [ ] Consolidar o Prólogo canônico sobre os blocos existentes de Emerald.
- [x] Construir a primeira passagem de Porto das Redes reutilizando Route 109 e Slateport.
- [ ] Implementar encontros, chefe e balanceamento final da Insígnia da Maré.
- [x] Construir Serra do Uivo reutilizando Route 114, Fallarbor e Meteor Falls.
- [ ] Remodelar o layout e a posição das interações dos mapas reutilizados do
      Emerald (mudança de layout, não de tileset).
- [ ] Compilar e testar o percurso completo até a Uivo Badge antes de liberar QoL intermediária.
- [ ] Construir os Arcos 3–8, Liga, finais e pós-jogo.
- [ ] Distribuir encontros, treinadores, itens, lojas e economia por arco.
- [ ] Balancear progressão, níveis, evoluções, habilidades e learnsets.
- [ ] Produzir música, efeitos e identidade sonora distribuíveis.
- [ ] Revisar integralmente português e inglês.
- [ ] Testar em mGBA, outros emuladores e hardware quando possível.
- [ ] Preparar patches reproduzíveis, créditos e guia de instalação.

## Dependências do autor

1. Aprovação visual dos Fakemon por lotes antes de considerar as artes definitivas.
2. Aprovação da integração dos 16 sprites de NPC (ADR-024).
3. Restaurar os minutos/billing do GitHub Actions para destravar o build e a
   geração da ROM de teste.
4. Teste manual das entradas, colisões, Pokédex, save/reload e fluxo de derrota.
5. Decisões narrativas ou visuais somente quando surgirem alternativas que
   mudem materialmente o jogo.

Enquanto o runner não inicia, o desenvolvimento pode avançar em especificação,
greybox, scripts, dados provisórios, validadores e infraestrutura sem ativar
recursos que escondam problemas de progressão.

# Estado do projeto e trabalho restante

Atualizado em 18 de julho de 2026. Este documento distingue implementação em
branches de trabalho de conteúdo realmente compilado, testado e aprovado.

## Estado atual

| Área | Estado | Observação |
| --- | --- | --- |
| Escopo e direção | Definido | Brasil por biomas, 386 slots e Sistema de Vínculos; primeira versão jogável em inglês |
| Vila e mapas do slice técnico | Implementado em PRs | Gráficos do Emerald; falta teste integrado no mGBA |
| História técnica inicial | Implementado em PRs | Estágios 0–8, Nilo, Rota da Neblina, Ruína e Câmara do Primeiro Elo |
| Bíblia narrativa canônica | Dois arcos em greybox | Porto reutiliza Route 109/Slateport; Serra reutiliza Fallarbor/Route 114/Meteor Falls |
| Pokédex de Arauna | Integrada na PR #47 | 386 nomes, dados, evoluções, learnsets, perfis e slots próprios |
| Ecologia e treinadores | Integrado na PR #47 | Encontros, espécies protegidas, dificuldade e equipes possuem auditorias reproduzíveis |
| Artes dos Fakemon | Integradas tecnicamente na PR #47 | Aprovação visual por lotes ainda é necessária; nenhuma nova arte deve entrar sem aprovação |
| QoL básica | Ativa na PR #47 | Apenas recursos sem efeito relevante sobre progressão ou formato do save |
| QoL intermediária | Bloqueada por marco | EXP Share global, DexNav e serviços aguardam a segunda insígnia jogável |
| Build e teste do head atual | Bloqueado por infraestrutura | Primeira versão força inglês e gera `pokeemerald-en.gba`; Actions ainda encerra antes do checkout |

## O que falta para estabilizar a PR #47

- [ ] Restaurar um runner capaz de iniciar o checkout ou compilar no Codespaces.
- [ ] Executar todas as auditorias e validadores do repositório.
- [ ] Fazer um build limpo da versão inglesa ativa.
- [ ] Testar no mGBA: save novo, escolha, captura, whiteout, save/reload, três
      Vínculos, miniboss, Pokédex no Centro de Pesquisa e epílogo.
- [ ] Corrigir qualquer falha encontrada no teste real.
- [ ] Revisar o lote visual completo; sprites não aprovados continuam candidatos.
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
- [ ] Substituir os 386 cries herdados, que continuam como placeholders de áudio.
- [ ] Fazer revisão final de habitats, capturas especiais e Testemunhos contra a
      Bíblia Narrativa v1.3.
- [ ] Validar o conjunto completo em build real e em hardware/emulador.

## O que falta da campanha completa

- [x] Definir oito Insígnias/Casas de História e os biomas principais.
- [x] Definir o eixo narrativo e os cinco Testemunhos.
- [ ] Converter a Bíblia v1.3 em mapa de cenas, diálogos, flags e objetivos.
- [ ] Consolidar o Prólogo canônico sobre os blocos existentes de Emerald.
- [x] Construir a primeira passagem de Porto das Redes reutilizando Route 109 e Slateport.
- [ ] Implementar encontros, chefe e balanceamento final da Insígnia da Maré.
- [x] Construir Serra do Uivo reutilizando Route 114, Fallarbor e Meteor Falls.
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
2. Teste manual das entradas, colisões, Pokédex, save/reload e fluxo de derrota.
3. Decisões narrativas ou visuais somente quando surgirem alternativas que
   mudem materialmente o jogo.

Enquanto o runner não inicia, o desenvolvimento pode avançar em especificação,
greybox, scripts, dados provisórios, validadores e infraestrutura sem ativar
recursos que escondam problemas de progressão.

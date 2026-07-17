# Estado do projeto e trabalho restante

Atualizado em 17 de julho de 2026. Este documento distingue implementação em
branches de trabalho de conteúdo realmente compilado, testado e aprovado.

## Estado atual

| Área | Estado | Observação |
| --- | --- | --- |
| Escopo e direção | Definido | Brasil por biomas, 386 slots, dois idiomas e Sistema de Vínculos |
| Vila e seis mapas do slice | Implementado em PRs | Casco gráfico do Emerald; falta teste integrado no mGBA |
| História inicial, Nilo e rota | Implementado em PRs | Estágios 0–5 e encontros provisórios |
| Ruína, escolha de Vínculo e câmara | Implementado em PRs | Três escolhas, miniboss e memória do Campeão |
| Encerramento do slice | Implementado em PR | Retorno a Nilo e estágio 8 |
| Pokédex técnica | Parcial | Registro 001–386 existe; só 001–020 vieram do spoiler estruturado manualmente |
| Captura e cura | Implementado em PRs | Kit, Dex provisória, checkpoint e cura repetível |
| Sprites de Arauna | Aguardando aprovação | Nenhum pacote gráfico de fakemon foi integrado |
| Build e teste | Bloqueado | GitHub Actions termina antes do checkout, sem passos ou logs |

## O que falta para fechar o vertical slice

- [ ] Reparar ou substituir o runner do GitHub Actions.
- [ ] Compilar as versões portuguesa e inglesa.
- [ ] Testar no mGBA: save novo, escolha, captura, whiteout, save/reload, três
      Vínculos, miniboss e epílogo.
- [ ] Corrigir qualquer falha encontrada no teste real.
- [ ] Integrar a pilha de PRs na ordem correta e reconciliar o PR separado da Dex.
- [ ] Fazer uma revisão final de texto e balanceamento da primeira rota.
- [ ] Gerar um patch privado de teste, nunca uma ROM completa no repositório.

## O que falta da Pokédex

- [ ] Receber exportação estruturada dos slots 021–386 em CSV, JSON ou código do
      projeto da Pokédex; hoje 366 slots ainda estão reservados sem dados finais.
- [ ] Para cada slot: nome, tipos, inspiração, bioma, família, evolução, método
      de evolução, stats, habilidades, learnset, descrição e raridade.
- [ ] Fechar os dados de batalha das nove formas dos iniciais.
- [ ] Aprovar, por lote, sprite frontal, traseiro, ícone, shiny e animações.
- [ ] Definir cries e footprints quando aplicável.
- [ ] Integrar e testar os 386 slots sem alterar a numeração dos saves.

## O que falta da campanha completa

- [ ] Definir o mapa-múndi e a ordem dos biomas brasileiros ficcionais.
- [ ] Planejar oito Selos, cidades, rotas, cavernas, ruínas e atalhos.
- [ ] Escrever os capítulos posteriores, antagonistas, Liga, finais e pós-jogo.
- [ ] Construir toda a campanha em greybox com gráficos do Emerald.
- [ ] Distribuir encontros, treinadores, itens, lojas e economia.
- [ ] Balancear progressão, níveis, evoluções, habilidades e learnsets.
- [ ] Produzir música, efeitos e identidade sonora que puderem ser distribuídos.
- [ ] Revisar integralmente português e inglês.
- [ ] Testar em mGBA, outros emuladores e hardware quando possível.
- [ ] Preparar patches reproduzíveis, créditos e guia de instalação.

## Dependências do autor

1. Exportação completa e editável da Pokédex, para evitar transcrever 366 slots
   a partir de imagens.
2. Entrega dos sprites em lotes numerados; cada lote será apresentado para
   aprovação antes da integração.
3. Decisões narrativas ou visuais somente quando surgirem alternativas que
   mudem materialmente o jogo.

Enquanto essas dependências não chegam, o desenvolvimento técnico pode avançar
na campanha greybox, ferramentas, dados provisórios, testes e infraestrutura.

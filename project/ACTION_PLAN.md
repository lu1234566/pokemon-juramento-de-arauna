# Plano de ação — versão definitiva de Arauna

## Resultado pretendido

Entregar um ROM hack bilíngue de Pokémon Emerald com:

- região, mapas, conexões, nomes e história próprios;
- identidade brasileira distribuída entre macrobiomas ficcionais;
- 386 espécies de Arauna substituindo a Pokédex do Emerald;
- oito Selos, Liga, Sistema de Vínculos, finais e pós-jogo;
- patches `pt-BR` e `en` gerados da mesma fonte;
- aparência consistente com o Emerald por reutilizar seus gráficos de cenário.

## Decisão que simplifica o projeto

Não será necessário redesenhar árvores, casas, água, cavernas, interiores, interface ou a maior parte dos objetos do mundo. Arauna será construída com novos layouts usando prioritariamente os tilesets originais do Emerald.

Isso reduz o risco artístico e técnico, mas não elimina o trabalho de mapas: coordenadas, conexões, colisões, warps, eventos, encontros e progressão continuarão sendo autorais.

O principal volume de arte nova passa a ser:

1. sprites das 386 espécies;
2. ícones, costas, animações e shinies correspondentes;
3. treinadores ou elementos de história realmente indispensáveis;
4. raríssimos tiles de cenário que não possam ser substituídos por recursos existentes.

## Regras de execução

1. `main` deve permanecer compilável.
2. Mudanças entram por branches e PRs pequenos.
3. Nenhuma ROM, save, credencial ou build `.gba` entra no Git.
4. Nenhum sprite entra em diretório compilado sem aprovação explícita.
5. Placeholders precisam ser identificados como temporários.
6. Todo lote compila em português e inglês.
7. Mapas novos reutilizam assets por referência; arquivos upstream não serão alterados sem necessidade.
8. Primeiro provar o fluxo completo com poucas espécies, depois escalar para 386.

## Organização das branches

| Prefixo | Uso |
|---|---|
| `docs/*` ou `agent/*` | decisões, planos e documentação |
| `feature/map-*` | um mapa ou conjunto pequeno de conexões |
| `feature/story-*` | uma sequência narrativa ou capítulo |
| `feature/dex-batch-*` | dados e integração de um lote aprovado |
| `art/proposal-*` | propostas fora dos diretórios compilados |
| `fix/*` | correções isoladas de colisão, warp, idioma ou build |

Branches de arte não devem misturar grandes alterações de história ou mapas. Branches de mapas não devem aproveitar para substituir sprites.

## Sequência imediata

### Passo 1 — Fechar a nova fundação documental

- revisar e integrar o PR de escopo definitivo;
- registrar que o passe de tiles autorais anterior foi substituído;
- preservar seu histórico sem usá-lo como base ativa.

### Passo 2 — Recuperar a Vila das Araucárias

- criar uma branch nova a partir da `main` estável;
- apontar a vila para uma combinação confiável de tilesets do Emerald;
- remontar casas, centro de pesquisa, caminhos, vegetação e saída;
- corrigir as quatro transições reportadas pelo teste manual;
- testar colisões e retornos no mGBA com save novo.

O objetivo não é copiar Littleroot. A vila terá layout, nomes, eventos e ritmo próprios, apenas usando a mesma linguagem gráfica.

### Passo 3 — Concluir a história do vertical slice

- casa do protagonista;
- apresentação da Vila das Araucárias;
- centro de pesquisa e escolha do inicial;
- primeiro confronto com Nilo;
- Rota da Neblina e tutorial;
- Ruína do Primeiro Elo;
- escolha de Coragem, Sabedoria ou Compaixão;
- miniboss, memória do guardião e encerramento.

O roteiro entra primeiro em `pt-BR`. A localização inglesa acontece depois que cada cena estiver estável para evitar retrabalho duplicado.

### Passo 4 — Finalizar o primeiro inicial

- refinar a proposta B do cachorro caramelo;
- enviar a folha refinada para aprovação;
- produzir o sprite frontal 64 × 64 somente após aprovação do refinamento;
- enviar o sprite frontal para nova aprovação;
- produzir costas, ícone, animação e shiny somente depois;
- integrar em branch isolada e testar escolha, batalha e save.

O mesmo fluxo será repetido para Pica-pau e Quero-quero.

### Passo 5 — Planejar os 386 slots

Antes de produzir centenas de sprites, criar um registro estruturado com:

- slot e codinome;
- família evolutiva;
- bioma e nicho;
- tipos;
- função de batalha;
- ponto de obtenção;
- método de evolução;
- estado de conceito, arte, integração e QA.

O registro textual completo reduz duplicações de conceito e impede que tipos ou funções importantes fiquem concentrados no fim do jogo.

### Passo 6 — Primeiro ecossistema jogável

Definir 12 a 18 espécies para a Mata das Araucárias e Rota da Neblina. O conjunto deve incluir:

- trio inicial;
- ave comum;
- mamífero inicial;
- inseto de dois ou três estágios;
- espécie noturna;
- espécie de água doce;
- encontro raro;
- pelo menos uma opção defensiva e uma de suporte.

Cada família passa por aprovação antes da arte e por nova aprovação antes da integração.

## Fluxo de uma espécie

```text
slot reservado
→ pitch escrito
→ conceito aprovado
→ silhueta aprovada
→ concept art aprovado
→ sprite frontal aprovado
→ pacote gráfico aprovado
→ dados integrados
→ encontros e treinadores
→ QA nos dois idiomas
```

Nenhuma etapa de aprovação artística será presumida.

## Fluxo de um mapa

```text
função narrativa
→ diagrama de conexões
→ layout com tiles do Emerald
→ colisões e warps
→ eventos e encontros
→ teste de navegação
→ texto pt-BR
→ localização en
→ teste no mGBA
```

Um tileset autoral só será considerado se o layout aprovado não conseguir comunicar o bioma com os recursos existentes.

## Fluxo de um capítulo

1. objetivo dramático e revelação;
2. cidades, rotas e áreas especiais envolvidas;
3. espécies necessárias para a ecologia e os treinadores;
4. greybox jogável com placeholders;
5. textos e escolhas em `pt-BR`;
6. balanceamento;
7. localização `en`;
8. substituição gradual dos placeholders por assets aprovados;
9. teste de início ao fim com save novo.

## Validação obrigatória por PR

- `git diff --check`;
- proteção contra arquivos proprietários;
- validação de localização;
- build `pt-BR`;
- build `en`;
- testes oficiais do motor quando aplicáveis;
- validadores específicos de mapas ou espécies;
- teste manual no mGBA para mudanças visuais, navegação, batalha ou save.

## Pontos de aprovação de Lucas

| Marco | O que será apresentado | O que a aprovação autoriza |
|---|---|---|
| Mapa inicial | vídeo ou capturas da vila com tiles do Emerald | continuar eventos e polimento, não criar novos tiles |
| Conceito de espécie | referências, tipos e silhuetas | produzir concept art |
| Concept art | forma e paleta propostas | produzir sprite frontal |
| Sprite frontal | escala nativa e ampliada | produzir pacote gráfico restante |
| Pacote gráfico | frente, costas, ícone, animação e shiny | integrar a espécie |
| Vertical slice | patch privado e checklist | avançar para demo pública |

## O que não faremos agora

- redesenhar todos os cenários do Emerald;
- criar tilesets exclusivos para cada bioma;
- produzir 386 sprites antes de testar o trio;
- integrar imagens apenas porque foram geradas;
- manter os mapas de Hoenn e apenas trocar seus nomes;
- escrever português e inglês simultaneamente enquanto a cena ainda muda;
- publicar ou versionar a ROM comercial.

## Próximos três entregáveis

1. Vila das Araucárias remontada com gráficos do Emerald e transições corrigidas.
2. Folha refinada da proposta B do cachorro caramelo para aprovação.
3. Registro dos slots 001–386 e ficha textual do primeiro ecossistema.

# Sistema de Vínculos

## Propósito

Transformar o modo como o jogador responde ao mundo em consequências narrativas legíveis, sem criar três campanhas separadas.

## Tendências

- **Coragem:** ação, risco e enfrentamento.
- **Sabedoria:** investigação, planejamento e conhecimento.
- **Compaixão:** cuidado, diálogo e proteção.

Nenhuma tendência representa bem ou mal. Cada uma pode resolver problemas ou criar novos conflitos.

## Versão 0 — Vertical slice

- uma decisão com três respostas;
- uma variável ou conjunto pequeno de flags;
- três resoluções curtas da mesma cena;
- recompensa diferente;
- diálogo posterior reconhecendo a escolha;
- nenhuma alteração no motor de batalha.

## Versão 1 — Demo pública

- pontuação acumulada nas três tendências;
- respostas e reações condicionais;
- pequenas rotas ou objetivos alternativos;
- itens ou missões exclusivas;
- mudança perceptível na relação com o rival;
- painel de depuração para testar valores.

## Versão 2 — Após a demo

Avaliar bênção, item ou golpe limitado associado à tendência dominante. A implementação em batalha só entra no roadmap se não comprometer memória, balanceamento, saves ou localização.

## Regras de design

- O jogador deve entender por que uma consequência aconteceu.
- Escolhas importantes não podem ser apenas cosméticas.
- O jogo não exibirá uma barra moral simplista.
- Recompensas diferentes precisam ter valor comparável.
- O caminho dominante não elimina todas as opções das outras tendências.
- O inicial escolhido não bloqueia nenhuma tendência.
- Flags narrativas e progressão obrigatória devem permanecer separadas.

## Primeira cena de teste

Um Pokémon afetado pela energia dos Juramentos está preso em uma ruína instável:

- Coragem: entrar imediatamente e removê-lo do perigo;
- Sabedoria: desativar o mecanismo antes da aproximação;
- Compaixão: acalmá-lo e permitir que indique uma passagem segura.

Todas as rotas salvam o Pokémon e mantêm a história principal, mas mudam o dano ambiental, a recompensa e a reação do rival.

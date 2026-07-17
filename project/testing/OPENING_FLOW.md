# Roteiro de teste — abertura jogável de Arauna

Este roteiro valida somente a progressão da casa até a entrada da Rota da Neblina. Os Pokémon de Emerald usados nas batalhas são placeholders técnicos; nenhum sprite de Arauna foi integrado.

## Preparação

1. Compile uma build `pt-BR` a partir da branch da abertura.
2. Use save novo ou zere as variáveis de teste de Arauna.
3. Entre na Vila das Araucárias pelo acesso técnico e siga primeiro para a casa no noroeste.

## Casa e objetivo

- [ ] A primeira entrada exibe o chamado da Dra. Maia uma única vez.
- [ ] `VAR_ARAUNA_STORY_STAGE` muda de 0 para 1.
- [ ] O responsável do protagonista reforça o objetivo do Centro de Pesquisa.
- [ ] Sair e entrar novamente não repete automaticamente a abertura.

## Centro de Pesquisa

- [ ] Dra. Maia apresenta os três projetos.
- [ ] Cada esfera mostra conceito, tipo inicial e confirmação `sim/não`.
- [ ] Recusar não altera a equipe nem as variáveis.
- [ ] Confirmar concede somente um placeholder no nível 5.
- [ ] Pica-pau usa TREECKO, Caramelo usa TORCHIC e Quero-quero usa MUDKIP apenas como placeholders.
- [ ] A mensagem informa claramente que nenhum sprite de Arauna foi integrado.
- [ ] As outras esferas não concedem um segundo parceiro.
- [ ] `VAR_ARAUNA_STARTER_CHOICE` registra 1, 2 ou 3 e o estágio muda para 2.

## Nilo e a saída leste

- [ ] Antes da escolha, Nilo não inicia batalha.
- [ ] Depois da escolha, Nilo inicia sua batalha existente.
- [ ] A vitória muda o estágio para 3 e não é repetida ao conversar novamente.
- [ ] Antes do estágio 3, a borda leste mostra a mensagem de bloqueio e recua o jogador um passo.
- [ ] Depois do estágio 3, a borda leste entra na Rota da Neblina.
- [ ] Ao entrar na rota, o estágio muda uma única vez para 4.
- [ ] O retorno posiciona o jogador na estrada, sem loop imediato.

## Persistência e segurança

- [ ] Save/reload preserva objetivo, escolha, batalha e liberação da rota.
- [ ] O mesmo fluxo funciona na build inglesa.
- [ ] Nenhuma fala autoral mistura idiomas ou ultrapassa a caixa de texto.
- [ ] Nenhum sprite, ícone, paleta ou dado definitivo de espécie foi adicionado.

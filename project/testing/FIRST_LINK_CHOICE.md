# Roteiro de teste — escolha do Primeiro Elo

Este trecho começa no estágio 5, depois que o Poochyena afetado foge da Rota da Neblina para a ruína.

## Resgate e escolha

- [ ] O Poochyena aparece diante da entrada e usa somente o sprite vanilla.
- [ ] A cena descreve a estrutura instável antes de oferecer as escolhas.
- [ ] Recusar as três opções devolve o controle e permite tentar novamente.
- [ ] Coragem registra `VAR_ARAUNA_BOND_CHOICE = 1`.
- [ ] Sabedoria registra `VAR_ARAUNA_BOND_CHOICE = 2`.
- [ ] Compaixão registra `VAR_ARAUNA_BOND_CHOICE = 3`.
- [ ] Cada escolha possui uma resolução textual diferente.
- [ ] As três escolhas removem o Poochyena, marcam o resgate e avançam a história para 6.
- [ ] Reentrar na ruína não repete a escolha nem recria o Pokémon.

## Câmara

- [ ] Antes da escolha, aproximar-se da escada mostra o bloqueio e recua o jogador.
- [ ] Depois da escolha, a mesma aproximação entra na Câmara do Primeiro Elo.
- [ ] O retorno da câmara continua apontando para a ruína.

## Persistência e segurança

- [ ] Save/reload preserva a tendência escolhida, o resgate e o estágio 6.
- [ ] Português e inglês executam exatamente o mesmo fluxo.
- [ ] Nenhum sprite novo ou dado definitivo de espécie foi integrado.

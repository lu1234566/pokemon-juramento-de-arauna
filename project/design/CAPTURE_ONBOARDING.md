# Pokédex e kit de captura

Este passo torna a abertura funcional como um jogo de Pokémon: depois de
escolher o inicial, o jogador recebe acesso à Pokédex provisória de 386 slots e
pode obter material para capturar os encontros da Rota da Neblina.

## Fluxo

1. Antes da escolha do inicial, o kit da praça permanece selado.
2. Ao registrar Caramelo, Querô ou Pimpau, a Dra. Maia ativa a Pokédex e o modo
   nacional para disponibilizar os 386 números usados por Arauna.
3. O texto informa claramente que os nomes e espécies oficiais ainda são
   substitutos técnicos associados aos mesmos números.
4. O kit da praça libera 5 Poké Balls e 3 Potions de uma só vez.
5. O objeto desaparece e a flag existente impede um segundo recebimento.

## Decisões técnicas

- O protótipo usa `FLAG_SYS_POKEDEX_GET` e `EnableNationalPokedex`; nenhuma
  interface gráfica nova é necessária nesta etapa.
- O kit verifica espaço para os dois itens antes de alterar a mochila, evitando
  recebimento parcial e duplicação por nova tentativa.
- A Pokédex oficial é deliberadamente tratada como provisória. A substituição
  futura será feita pelo número do slot, preservando saves e tabelas.
- Nenhum sprite, ícone, retrato ou tileset é criado ou modificado.

# Servicos compartilhados: Centro POKéMON e POKé MART

## Objetivo

Localizar a camada de atendimento compartilhada por Centros POKéMON e POKé MARTS de toda a regiao, evitando repetir a mesma correcao cidade por cidade.

## Centro POKéMON

O renderer cobre 10 blocos em:

`data/text/pkmn_center_nurse.inc`

Inclui:

- boas-vindas;
- pergunta de descanso;
- recebimento da equipe;
- confirmacao de recuperacao;
- despedida;
- variante interrompida pelo Cartao Dourado;
- reconhecimento do Cartao Dourado de quatro estrelas;
- atendimento habitual apos o reconhecimento;
- variantes de recebimento/espera.

## POKé MART

O renderer cobre 3 blocos em:

`data/text/mart_clerk.inc`

Inclui:

- boas-vindas;
- pergunta de atendimento;
- despedida;
- variante que usa o nome do jogador.

## Preservado

Centro POKéMON:

- `Common_EventScript_PkmnCenterNurse`;
- `HealPlayerParty`;
- `GAME_STAT_USED_POKECENTER`;
- Trainer Stars;
- Cartao Dourado/Prateado como estados internos;
- Pokérus e sua verificacao;
- Union Room;
- Trainer Hill;
- movimentos e efeitos de cura;
- flags, vars e save.

POKé MART:

- estoques;
- precos;
- `pokemart`;
- compra/venda;
- inventario;
- dinheiro;
- IDs de item;
- flags, vars e save.

Este lote altera somente as mensagens universais de atendimento. Interfaces maiores de compra/venda e Cable Club podem ser localizadas em lotes sistemicos posteriores.

## Impacto

Como esses textos sao compartilhados, uma unica camada melhora todos os mapas que chamam a enfermeira padrao ou os textos padrao de atendente de Mart.

Porto do Sal passa a permanecer em PT-BR mesmo ao entrar nesses servicos, sem criar forks de script por cidade.

## Seguranca

- 13 blocos exatos;
- no maximo duas linhas por pagina;
- no maximo 32 caracteres por segmento;
- comparacao estrutural mascarando `.string`;
- build transacional;
- auditor renderizado;
- gate CI dedicado.

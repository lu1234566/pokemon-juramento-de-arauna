# Vila da Passagem V1 — blueprint

A Master Map Design Bible, página 4, define Oldale como uma vila de estrada em Y/T: terra batida, madeira, casas junto ao entroncamento, venda, Center, bancos e árvores antigas. Os arquivos recebidos não contêm um PNG dedicado a Vila da Passagem. As referências visuais usadas são a Vila Amanhecer e o conjunto Sul de Arauna; não serão apresentadas como um concept dedicado a esta cidade.

- Composição: 30×26 metatiles, ajustando os 28×22 propostos para os edifícios completos e as cenas existentes. Entrada sul, braço oeste e saída nordeste formam um Y irregular.
- Arquitetura: duas casas de telha cerâmica do banco aprovado de Amanhecer, desencontradas; Center e Mart reconstruídos com módulos nativos completos. Fachadas inteiras, jardins pequenos e bancos junto à estrada.
- Posições: casa de estrada a noroeste, Center a sudoeste, Mart a nordeste e segunda casa a sudeste. Um bosque pequeno ocupa a parte interna da bifurcação, sem praça pavimentada.
- Saídas: 101 ao sul em x=8..11; 102 a oeste em y=10/11; 103 ao norte em x=18..21. A conexão norte usa offset +10, com -10 na volta pela Rota 103.
- Ciro: preservar os três gatilhos e a entrada por conversa; mover somente a linha de chegada para y=25. Sua saída continua pela Rota 101 nas colunas 9, 10 e 11 já validadas.
- Funcionário do Mart: encontro em (24,13), destino em (24,7). Reescrever os trajetos para a nova loja e acrescentar a abordagem pelo quarto lado, agora acessível. Preservar o brinde, a capacidade da mochila, as flags e os diálogos.
- Bloqueio oeste: conservar a passagem em (0,10)/(1,11), com o NPC contornando o jogador ao recuar. A guarda deve voltar à posição inicial em tentativas repetidas.
- Fly: migrar para o piso imediatamente abaixo da nova porta do Center.
- Banco gráfico: reutilizar AraunaAmanhecer; reservar apenas clones dos metatiles nativos de serviços que precisam do fundo de grama local. Não criar gráficos ou animações adicionais. Portas nativas do Center/Mart e porta já aprovada das casas.
- Conexões visuais: Route102 e Route103 passam a usar o mesmo banco. Os renders das rotas e das bordas de Petalburg/Route110 devem permanecer iguais.
- Entrega: mapa real, comparação com a direção de referência, viewports 240×160, conexões, simulação de cenas, validador e instalador reproduzível. ROM/emulador permanecem pendentes.

Inventário: 4 warps, 4 objetos, 4 gatilhos e 5 eventos de placa; quatro desses eventos pertencem às duas metades dos letreiros integrados do Center e do Mart. Não serão criadas cinco placas soltas.

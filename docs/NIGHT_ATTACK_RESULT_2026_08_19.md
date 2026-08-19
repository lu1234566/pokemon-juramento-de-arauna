# Ataque técnico sem arte — resultado de 19/08/2026

## Integrado na `main`

### PR #119 — Vila Amanhecer V3

- redesenho do blockdata 20×20 com tiles já existentes do Emerald;
- `map.bin` validado com 800 bytes;
- portas, placas e corredor norte preservados nas coordenadas funcionais;
- sem alteração de warps, eventos, flags, conexões ou save.

### PR #120 — manutenção/CI/backlog

- README voltou a representar Pokémon Juramento de Arauna;
- CI ganhou validação estática dos limpadores de resíduos;
- arquitetura atual e estado técnico sem arte foram documentados;
- issue #28 encerrada como arquitetura supersedida.

### PR #121 — introdução bilíngue atual

- introdução de Anahi separada em pt-BR/en com os mesmos nove labels;
- seleção no estágio correto do `cpp` da pipeline do pokeemerald;
- pt-BR preservado como padrão;
- builds isoladas `intro-ptbr`/`intro-en`;
- validação de labels, placeholders, charmap e largura de linha;
- documentação explícita de que o protótipo ainda não representa tradução integral do jogo.

### PR #122 — protagonista e Ciro

- identidade narrativa do protagonista fechada;
- idade, origem, motivação, conflito e limites de interpretação definidos;
- dois slots de apresentação de gênero preservam o mesmo cânone;
- relação inicial e arco do primeiro capítulo de Ciro definidos;
- vozes pt-BR/en registradas;
- GDD narrativo e sinopse atualizados;
- issue #2 concluída.

### PR #124 — fechamento do M1 de localização

- inventário atual de textos/charmap;
- decisão: Poryscript não é dependência do protótipo M1;
- glossário-base pt-BR/en versionado;
- issue #5 concluída.

## Backlog revisado

- issue #2 — concluída;
- issue #5 — concluída como protótipo M1;
- issue #28 — encerrada como supersedida pela arquitetura atual;
- issue #9 — depende de glifos/fontes em pixel art;
- issue #31 — direção visual/tileset, depende de arte;
- issue #3 — concept art dos iniciais, depende de arte;
- issue #123 — novo lote técnico delimitado para resíduos sistêmicos do laboratório de Anahi.

O PR legado #58 não foi alterado.

## Resíduo técnico ainda confirmado

`data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc` ainda contém seis blocos de superfície em inglês/vanilla, agora rastreados pela issue #123:

1. upgrade para National Dex;
2. recebimento do starter de Johto;
3. prompt legado de apelido;
4. aviso para deixar os outros starters;
5. mensagem de falta de espaço para Pokémon;
6. ligação pós-game completa de Scott/S.S. Tidal/Slateport/Lilycove.

A substituição direta desse arquivo grande não foi feita de forma cega: o conector disponível exige substituição integral do texto e o Actions não chegou a executar Checkout, então não havia um mecanismo seguro para aplicar/revalidar automaticamente esse patch durante a sessão.

## GitHub Actions

Foram disparados runs e rerun em branches diferentes. O padrão observado foi consistente: os jobs encerraram em falha antes de registrar qualquer step (`steps: null`), inclusive antes do Checkout. Portanto não houve log de compilação ou de comando do repositório que permitisse atribuir essas falhas ao código.

A CI foi preparada para, quando o runner efetivamente executar jobs, separar validação estática e builds de introdução pt-BR/en.

## Restrições respeitadas

- nenhum Codespaces usado;
- nenhuma arte nova criada ou exigida para os lotes integrados;
- nenhuma mudança intencional de save, flags, warps ou ordem de progressão;
- PR #58 preservado sem alterações.

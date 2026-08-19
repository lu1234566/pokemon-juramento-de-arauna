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
- builds isoladas para pt-BR/en;
- validação de labels, placeholders, charmap e largura de linha.

### PR #122 — protagonista e Ciro

- identidade narrativa do protagonista fechada;
- relação inicial e arco do primeiro capítulo de Ciro definidos;
- vozes pt-BR/en registradas;
- GDD narrativo e sinopse atualizados;
- issue #2 concluída.

### PR #124 — fechamento do M1 de localização

- inventário atual de textos/charmap;
- decisão: Poryscript não é dependência do protótipo M1;
- glossário-base pt-BR/en versionado;
- issue #5 concluída.

### PR #125 — laboratório de Anahi / pós-game

- seis resíduos sistêmicos em inglês/vanilla removidos;
- upgrade da National Dex, recebimento/nickname do starter e avisos auxiliares localizados;
- ligação de Scott reatribuída visualmente a Seu Bento;
- `SLATEPORT`/`LILYCOVE` substituídos por `PORTO DO SAL`/`BAIA DAS LUZES` na superfície visível;
- nenhum comando executável, label, flag, var, movimento, progressão ou save foi alterado;
- novo validador dedicado com `--check` e limite conservador de 32 caracteres;
- issue #123 concluída.

## Auditoria do backlog

Issues abertas após o ataque:

- #3 — concept art dos iniciais; depende de arte;
- #9 — glifos/fontes; depende de pixel art;
- #31 — tileset/direção visual da vila; depende de arte.

Não restou issue aberta totalmente não-art. O PR legado #58 permaneceu intocado.

## CI / runner

Os runs observados durante a sessão, inclusive rerun, encerraram antes de registrar qualquer step (`steps: null`). O padrão ocorreu antes do Checkout, portanto não há log de compilação nem evidência de falha do código.

A proteção da `main` foi auditada e exige os contextos históricos `repository-safety` e `build-and-test`. A CI atual foi preparada para voltar a publicar exatamente esses nomes quando os runners iniciarem normalmente: o primeiro protege os validadores/contrato de localização e o segundo agrega a validação com as duas builds de idioma.

## Restrições respeitadas

- nenhum Codespaces usado;
- nenhuma arte nova criada ou exigida;
- nenhuma mudança intencional de save, flags, warps ou ordem de progressão;
- nenhuma edição no PR #58.

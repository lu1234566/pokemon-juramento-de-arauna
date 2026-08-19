# Avaliador de Nomes de Porto do Sal

## Objetivo

Localizar a casa do Avaliador de Nomes sem alterar nenhuma das regras herdadas de renomeacao de POKéMON.

## Escopo

Nove blocos foram curados:

- apresentacao do AVALIADOR;
- escolha do POKéMON;
- avaliacao do apelido atual;
- pedido de novo apelido;
- confirmacao do novo nome;
- despedida;
- caso em que o jogador escolhe o mesmo nome;
- POKéMON cujo treinador original nao e o jogador;
- OVO.

## Comportamento preservado

Permanecem intactos:

- `ChoosePartyMon`;
- `ScriptGetPartyMonSpecies`;
- verificacao de OVO;
- `IsMonOTIDNotPlayers`;
- `MonOTNameNotPlayer`;
- `Common_EventScript_NameReceivedPartyMon`;
- `TryPutNameRaterShowOnTheAir`;
- buffers de nickname;
- YES/NO;
- flags, vars e saves.

Assim, POKéMON recebidos de outro treinador continuam sem poder ser renomeados e OVO continua bloqueado.

## Seguranca

`scripts/render_porto_sal_name_rater.py` valida:

- 9 labels exatos;
- marcadores da superficie inglesa anterior;
- segmentos visiveis de no maximo 32 caracteres;
- comparacao estrutural mascarada;
- ausencia de `NAME RATER`, `fortune-teller`, `magnificent nickname` e outros residuos nos blocos alvo.

O `scripts.inc` da casa foi adicionado ao backup transacional do build e ao auditor renderizado.

Sem arte, sem Codespaces e PR #58 intocado.

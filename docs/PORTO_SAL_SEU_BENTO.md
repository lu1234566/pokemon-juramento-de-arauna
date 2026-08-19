# Seu Bento em Porto do Sal

## Objetivo

Fechar a superficie visivel herdada de Scott em Porto do Sal sem alterar nenhum identificador ou estado interno de Emerald.

## Cenas curadas

Seis blocos:

1. Seu Bento reconhece que o jogador barrou a equipe do Horizonte no Museu;
2. apresenta seu habito de acompanhar treinadores e manter um caderno de campo;
3. registra contato pelo POKéNAV;
4. mensagem de registro mostra `SEU BENTO`;
5. explica que vai circular por outras cidades e registrar pistas;
6. comenta a participacao do jogador na TENDA DE BATALHA.

## Coerencia canonica

Esta camada nao cria uma nova equivalencia. O projeto ja usa Seu Bento como equivalente visivel do slot Scott em:

- Match Call;
- convite ao circuito de batalha;
- pos-game;
- outras superficies narrativas recentes.

Porto do Sal agora passa a apresentar esse papel antes do pos-game.

A caracterizacao escolhida conecta as duas fases: Seu Bento observa jornadas, registra pistas e usa o POKéNAV para avisar quando encontra algo que justifique uma viagem.

## Identificadores internos preservados

Continuam intactos, entre outros:

- `LOCALID_SLATEPORT_SCOTT`;
- `VAR_SCOTT_STATE`;
- `FLAG_ENABLE_SCOTT_MATCH_CALL`;
- scripts `ScottScene` / `ScottBattleTentScene`;
- movimentos e remocao/adicao do objeto;
- musica/fanfare de registro;
- estados de Slateport;
- saves e progressao.

## Seguranca

`scripts/render_porto_sal_seu_bento.py` valida:

- seis labels exatos;
- marcadores da superficie anterior;
- largura maxima de 32 caracteres;
- comparacao estrutural mascarada;
- ausencia de `SCOTT`, `CIRO:`, `BATTLE TENT` e residuos em ingles nos blocos alvo;
- presenca visivel de `SEU BENTO`.

O renderer roda depois das camadas de fila, placas civicas e vida cotidiana, sem sobreposicao de labels.

Sem arte, sem Codespaces e PR #58 intocado.

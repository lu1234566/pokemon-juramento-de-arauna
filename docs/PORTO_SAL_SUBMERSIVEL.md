# Porto do Sal — submersivel e rota para M'Boi

Este lote cura a sequencia plot-critical de `SlateportCity` + `SlateportCity_Harbor` sem alterar nenhuma flag, movimento, warp ou estado herdado do Emerald.

## Entrevista publica

O slot interno de CAPT. STERN nao recebe um novo personagem canonico inventado. Na superficie ele e tratado como `ENGENHEIRO` / `ENGENHEIRO DO PORTO`.

A entrevista deixa de falar genericamente em uma especie extinta na Route 128 e passa a comunicar que:

- novos mapas confirmam cavernas sob M'BOI;
- o submersivel do porto consegue alcanca-las;
- leituras de VINCULO em M'BOI subiram junto dos ultimos tremores;
- uma corrente anomala esta se movendo pelas cavernas.

A reporter permanece apenas como `REPORTER`, sem depender dos nomes vanilla Gabby/Ty na superficie.

## Requisicao do submersivel

O anuncio herdado de Team Aqua passa a ser um comunicado do HORIZONTE:

- protocolo de emergencia;
- o submersivel sera requisitado para responder a anomalia de M'BOI;
- a equipe civil do porto e instruida a nao interferir.

Isso deixa explicito que a tomada do veiculo nao e consensual, mesmo que OTACILIO acredite estar evitando outro desastre.

## Hangar

OTACILIO explica que:

- o submersivel e o unico veiculo capaz de alcancar as CAVERNAS DE M'BOI;
- primeiro ele seguira ao ARQUIVO CENTRAL para concluir a carga/preparacao;
- depois partira para M'BOI;
- ele conscientemente esta agindo sem esperar permissao.

Isso conecta diretamente esta cena a `ARQUIVO_CENTRAL_DEPTH.md`, onde o submersivel parte do B2F depois do carregamento.

O ENGENHEIRO reage dizendo que o veiculo foi construido para pesquisa, nao para uma faccao, e que OTACILIO poderia ter pedido autorizacao.

## Pista posterior

Depois que o submersivel deixa o ARQUIVO CENTRAL, as falas do engenheiro deixam de repetir slogans do HORIZONTE e passam a informar:

- o veiculo mergulhou em mar aberto;
- a rota segue para M'BOI;
- o jogador precisara usar DIVE para chegar as cavernas.

## Estrutura preservada

Permanecem intactos:

- `VAR_SLATEPORT_CITY_STATE`;
- `VAR_SLATEPORT_HARBOR_STATE`;
- `FLAG_MET_TEAM_AQUA_HARBOR`;
- flags que liberam a entrada do ARQUIVO CENTRAL;
- `FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE`;
- `FLAG_EVIL_TEAM_ESCAPED_STERN_SPOKE`;
- todos os `LOCALID_*`;
- movimentos de civis, engenheiro, OTACILIO, agente e submersivel;
- musica da cena;
- warp da cidade para o porto;
- ferry/postgame;
- scanner trade;
- DIVE e requisitos posteriores;
- saves e progressao.

Nenhum `scripts.inc` e commitado modificado. `SlateportCity/scripts.inc` e `SlateportCity_Harbor/scripts.inc` entram no backup transacional do build e sao restaurados no `EXIT`.

## Validacao

`scripts/render_porto_sal_submersivel.py` cobre:

- 8 blocos na cidade;
- 5 blocos no porto;
- 13 blocos plot-critical no total.

Todas as 50 linhas visiveis novas foram auditadas e respeitam o limite de 32 caracteres.

O renderer usa labels exatos, assinatura conhecida da superficie anterior, comparacao estrutural mascarada e rejeita residuos centrais de CAPT. STERN, GABBY, LILYCOVE e os parágrafos genericos anteriores.

Entrada:

`python3 scripts/render_porto_sal_submersivel.py --check`

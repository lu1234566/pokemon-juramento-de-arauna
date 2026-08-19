# Cais e Barco de Linha de Porto do Sal

## Objetivo

Fechar a superficie cotidiana e de pos-game do antigo Slateport Harbor sem alterar a perseguicao plot-critical do submersivel, que permanece em uma camada separada.

## Escopo

`scripts/render_porto_sal_harbor_service.py` cura 21 blocos do Cais:

### Atendimento e ferry

- servico ainda indisponivel;
- pedido e verificacao do BILHETE;
- escolha de destino;
- confirmacao de BAIA DAS LUZES;
- confirmacao do CIRCUITO DE BATALHA;
- embarque e cancelamento;
- pergunta de novo destino.

### Vida portuaria

- marinheiro interessado em descida submarina;
- comentario sobre clima/correntes anormais;
- homem que nao cabe no submersivel.

### Construcao do barco

- progresso com ajuda do VETERANO;
- conclusao do BARCO DE LINHA;
- convite para viajar.

### Scanner

- proposta de troca do SCANNER;
- recusa e retorno posterior;
- DEEPSEATOOTH / DEEPSEASCALE;
- escolha do premio;
- entrega ao ENGENHEIRO;
- agradecimento pela ajuda a pesquisa.

## Menus de destino

Dois literais globais de `src/strings.c` tambem sao renderizados:

- `gText_LilycoveCity` -> `BAIA DAS LUZES`;
- `gText_SlateportCity` -> `PORTO DO SAL`.

`gText_BattleFrontier` ja e renderizado pela camada do Circuito como `CIRCUITO DE BATALHA`, portanto o menu do ferry fica coerente sem duplicar essa responsabilidade.

## Fora do escopo

As cinco falas da requisicao/perseguicao do submersivel continuam sob `render_porto_sal_submersivel.py`:

- reconhecimento da equipe;
- fala de Otacilio;
- protesto do engenheiro;
- partida do Arquivo Central;
- orientacao para DIVE/M'Boi.

## Preservado

Permanecem intactos:

- `MULTI_SSTIDAL_*`;
- `VAR_SS_TIDAL_STATE`;
- mapas/warps do barco;
- bilhete e flags;
- `ITEM_SCANNER`;
- `ITEM_DEEP_SEA_TOOTH`;
- `ITEM_DEEP_SEA_SCALE`;
- `FLAG_EXCHANGED_SCANNER`;
- verificacao de clima/lendarios;
- movimentos e objetos;
- estados do Cais;
- saves e progressao.

## Seguranca

O renderer exige:

- 21 labels exatos;
- marcadores da superficie anterior;
- largura maxima de 32 caracteres;
- comparacao estrutural mascarada;
- dois anchors unicos para nomes de cidade em `strings.c`;
- ausencia dos principais nomes vanilla nos blocos alvo.

O build aplica esta camada depois das demais superficies de Porto do Sal. O auditor renderizado compoe a camada plot-critical do submersivel primeiro e o servico do Cais depois, mantendo os escopos independentes.

Sem arte, sem Codespaces e PR #58 intocado.

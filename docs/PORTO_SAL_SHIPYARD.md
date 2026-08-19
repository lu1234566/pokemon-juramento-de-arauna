# Estaleiro de Porto do Sal

## Objetivo

Curar a superficie visivel do antigo `SternsShipyard` sem alterar nenhuma logica herdada de Emerald.

## Identidade visivel

Os IDs internos continuam intactos, mas a superficie deixa de depender de nomes vanilla:

- `Dock` -> MESTRE / mestre do estaleiro;
- `Mr. Briney` -> MARINHEIRO VETERANO / VETERANO;
- `S.S. Tidal` -> BARCO DE LINHA;
- `Capt. Stern` -> ENGENHEIRO DO PORTO.

Nenhum novo personagem canonico foi inventado apenas para preencher um slot de Emerald.

## 1F

Nove blocos foram curados:

- dificuldade real de montar um projeto novo;
- encaminhamento das PECAS OCEANICAS ao ENGENHEIRO no MUSEU;
- necessidade de experiencia pratica no mar;
- chegada de um marinheiro veterano;
- conclusao do BARCO DE LINHA no pos-game;
- fala do veterano sobre combinar projeto e experiencia;
- duas falas tecnicas sobre o comportamento do mar e trabalho em terra.

## 2F

Duas falas tecnicas foram localizadas:

- projeto de navio como estrutura de grande porte;
- principio de flutuacao.

## Coerencia com Porto do Sal

O Estaleiro agora se encaixa no arco ja implementado:

1. as PECAS OCEANICAS pertencem ao trabalho oceanografico do ENGENHEIRO;
2. o MUSEU recebe/calibra os componentes;
3. o Estaleiro cuida de casco, estrutura e construcao naval;
4. o BARCO DE LINHA surge como projeto civil posterior, sem depender do nome S.S. Tidal.

## Preservado

Permanecem intactos:

- `FLAG_SYS_GAME_CLEAR`;
- `FLAG_BADGE07_GET`;
- `FLAG_DELIVERED_DEVON_GOODS`;
- `FLAG_DOCK_REJECTED_DEVON_GOODS`;
- todos os `LOCALID_*`;
- movimentos;
- objetos;
- estados do estaleiro;
- ferry/post-game;
- saves e progressao.

## Seguranca

`scripts/render_porto_sal_shipyard.py` valida:

- labels exatos;
- marcadores da superficie anterior;
- largura maxima de 32 caracteres;
- comparacao estrutural mascarada;
- ausencia dos tokens visiveis `CAPT. STERN`, `MR. BRINEY` e `S.S. TIDAL` nos blocos alvo.

O build faz backup transacional dos dois `scripts.inc`, aplica a camada e restaura os arquivos-fonte apos a compilacao.

Sem arte, sem Codespaces e PR #58 intocado.

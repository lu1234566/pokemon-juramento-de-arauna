# Vida cotidiana de Porto do Sal

## Objetivo

Fechar as falas humanas cotidianas ainda visivelmente herdadas de Slateport sem misturar este escopo com Berry Powder ou com a cena de Seu Bento/Scott.

## Escopo

`scripts/render_porto_sal_daily_life.py` cura 29 blocos em `data/maps/SlateportCity/scripts.inc`.

### Comercio e cidade

- vendedor de vitaminas/itens de treino;
- mercado e compras;
- farol;
- algas e culinaria;
- crescimento historico da cidade;
- Porto do Sal como cidade costeira;
- decoracoes;
- Tenda de Batalha;
- viajante vindo do interior.

### POKéMON e sistemas herdados

- avaliacao de esforco;
- recebimento e aplicacao da FITA DE ESFORCO;
- dica para continuar treinando;
- Avaliador de Nomes;
- apelidos de POKéMON recebidos em troca.

### Vida maritima

- marinheiros e o tamanho do mar;
- navios antigos transformados em habitat;
- referencia civil ao ENGENHEIRO DO PORTO e suas expedicoes.

### Entrevista

Os espectadores da entrevista deixam de usar Stern/Gabby/Ty na superficie:

- CAPT. STERN -> ENGENHEIRO DO PORTO;
- GABBY -> REPORTER;
- TY -> CAMERAMAN.

Os eventos, movimentos e a sequencia plot-critical da entrevista continuam nos mesmos slots internos. A parte que leva ao submersivel permanece sob `render_porto_sal_submersivel.py`.

## Fora do escopo

Este lote nao altera:

- sistema de Berry Powder;
- menus/loja de Berry Powder;
- cena de Scott/Seu Bento e Match Call;
- logica da Tenda de Batalha;
- mecanismos de Name Rater;
- qualquer mapa ou arte.

## Preservado

Permanecem intactos:

- `LeadMonHasEffortRibbon`;
- `Special_AreLeadMonEVsMaxedOut`;
- `GiveLeadMonEffortRibbon`;
- marts e inventarios;
- flags de Ribbon;
- Tenda de Batalha;
- Name Rater;
- estados da entrevista;
- movimentos;
- objetos;
- flags/vars;
- warps e saves.

## Seguranca

O renderer valida:

- 29 labels exatos;
- marcadores da superficie anterior;
- largura maxima de 32 caracteres;
- comparacao estrutural mascarada;
- ausencia de tokens visiveis como `ENERGY GURU`, `EFFORT RIBBON`, `MAUVILLE CITY`, `CAPT. STERN`, `GABBY:` e `TY:` nos blocos alvo.

O build aplica esta camada depois da fila do Museu e das placas civicas. O auditor renderizado usa a mesma composicao.

Sem arte, sem Codespaces e PR #58 intocado.

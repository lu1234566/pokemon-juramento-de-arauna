# Porto do Sal — fila, 1F do Museu e pessoas

Esta camada complementa `PORTO_SAL_MUSEUM_CONFRONTATION.md`. O confronto do 2F permanece separado; aqui o escopo e a superficie humana da fila externa e do 1F.

## Fila externa

Quinze falas de `SlateportCity` deixam de funcionar como dialogo vanilla de Team Aqua.

A fila agora mostra:

- moradores curiosos com o movimento no MUSEU;
- agentes do HORIZONTE instruidos a entrar sem chamar atencao;
- agentes que aceitam pagar o ingresso por ser um MUSEU civil;
- outros que ja defendem requisitar equipamentos considerados essenciais;
- duvidas sobre uma ordem vaga de `inspecao de campo`;
- pequenas falas cotidianas que fazem os agentes parecerem pessoas diferentes, nao um unico slogan repetido.

A fila, movimentos, objetos e estado da cidade permanecem intactos.

## Bilheteria

O fluxo de entrada continua exatamente o mesmo:

- ingresso de ¥50;
- verificacao de dinheiro;
- `removemoney`;
- entrada gratuita no caso especial em que o jogo entende que o jogador esta acompanhando o grupo;
- flag de entrada paga;
- todos os estados do Museu.

Apenas os quatro textos da recepcao passam para PT-BR.

## Agentes no 1F

Seis agentes do HORIZONTE recebem falas distintas:

- tecnico de campo que aproveita a visita;
- equipe que deveria apenas observar antes da chegada de OTACILIO;
- comentario sobre equipamento caro sem motivacao de roubo;
- interesse nos modelos de correntes e pressao;
- referencia a uma operacao anterior que falhou;
- agente que reclama de ter pago ingresso como qualquer visitante.

Isso prepara o confronto do 2F sem antecipar que a requisicao das PECAS OCEANICAS necessariamente tera sucesso.

## Visitantes

Quatro visitantes passam a falar em PT-BR sobre:

- aprender sobre o mar e seus POKéMON;
- o ENGENHEIRO DO PORTO como inspiracao;
- especies ainda desconhecidas em regioes profundas;
- desejo de conviver com um POKéMON marinho.

## TM do agente conhecido

O agente familiar continua usando exatamente o evento original de `ITEM_TM_THIEF`.

Na superficie:

- ele reconhece que o jogador o derrotou anteriormente;
- entrega a TM como forma de encerrar a divida;
- se a bolsa estiver cheia, pede que o jogador volte com espaco;
- depois da entrega, espera que o proximo encontro nao seja em lados opostos.

`FLAG_RECEIVED_TM46` e todos os comandos de entrega permanecem intactos.

## Estrutura preservada

Permanecem intactos:

- valor de entrada ¥50 e `checkmoney`/`removemoney`;
- `FLAG_PAID_TO_ENTER_MUSEUM`;
- `VAR_SLATEPORT_MUSEUM_1F_STATE`;
- `ITEM_TM_THIEF` e `FLAG_RECEIVED_TM46`;
- objetos, movimentos, coordenadas e warps;
- todos os scripts de exposicao/painel cientifico, que ficam fora deste lote;
- saves e progressao.

## Validacao

A camada base cobre 15 falas da fila e 17 falas humanas do 1F. Um wrapper de validacao corrige as que ficariam acima do teto e mantem todo o conjunto em no maximo 32 caracteres visiveis por segmento.

Entrada oficial:

`python3 scripts/render_porto_sal_museum_people_checked.py --check`

O build aplica a sequencia:

1. submersivel de Porto do Sal;
2. pessoas/fila do Museu;
3. confronto do 2F e PECAS OCEANICAS.

Os alvos sao disjuntos e o backup transacional restaura os fontes no `EXIT`.

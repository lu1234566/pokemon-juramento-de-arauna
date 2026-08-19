# Base dos Lembrantes — andares inferiores

Esta camada complementa `LEMBRANTES_BASE_CORE.md` e cura `MagmaHideout_1F`, `MagmaHideout_2F_1R` e `MagmaHideout_2F_2R`.

O objetivo e substituir a repeticao de slogans por pessoas com motivos, metodos e divergencias diferentes, sem alterar nenhuma batalha ou logica de progressao.

## 1F — entrada e motivos

A entrada da base estabelece que:

- os LEMBRANTES preservam copias de materiais que o HORIZONTE tentou retirar de circulacao;
- alguns membros entraram na faccao porque acreditam que perdas documentais nao foram acidentais;
- o MEMORIAL DOS NOMES guarda nomes, enquanto a base guarda provas sobre tentativas de apagamento;
- devolver historias nao deve significar invadir a mente de alguem;
- nem todos na faccao concordam integralmente com LUZIA;
- o REGISTRO-MATRIZ ja aparece como decisao controversa antes de o jogador chegar ao nucleo.

## 2F_1R — arquivo de provas

Este andar funciona como arquivo material:

- cadernos de familias atingidas em M'BOI;
- documentos classificados como `material terapeutico` pelo HORIZONTE;
- depoimentos com trechos cobertos;
- lotes retirados de deposito antes de incineracao;
- documentos com assinaturas da LIGA e do HORIZONTE;
- ELIAS aparece em aprovacoes, mas o texto tambem reconhece ressalvas;
- os LEMBRANTES cruzam nomes, datas e testemunhos;
- documentos sao explicitamente tratados como evidencia incompleta, nao como verdade automatica.

A camada evita afirmar quem ordenou cada ocultacao quando o repositorio nao fornece prova canonica para isso.

## 2F_2R — dissenso interno

O segundo setor transforma a divergencia interna em tema jogavel:

- quem pode devolver uma memoria;
- o que fazer quando alguem escolheu esquecer;
- diferenca entre combater apagamento e impor restauracao;
- membros que seguem LUZIA sem considera-la infalivel;
- critica a linguagem de `instabilidade` usada pelo HORIZONTE;
- reconhecimento de que uma pessoa nao e um arquivo restauravel sem consentimento;
- preparacao do andar superior por RAUL;
- medo real sobre como a corrente reagira ao REGISTRO.

O ultimo membro pede ao jogador que nao entregue o REGISTRO ao HORIZONTE, mas tambem que impeça seu uso sem limite. Isso prepara diretamente `LEMBRANTES_BASE_CORE.md`.

## Estrutura preservada

Permanecem intactos:

- `TRAINER_GRUNT_MAGMA_HIDEOUT_*`;
- parties, IA, classes e sprites;
- scripts de batalha;
- `VAR_JAGGED_PASS_ASH_WEATHER`;
- objetos, movimentos, coordenadas e warps;
- itens de mapa;
- saves e progressao.

## Validacao

`scripts/render_lembrantes_lower_surface.py` cobre 30 blocos:

- 6 no 1F;
- 12 no 2F_1R;
- 12 no 2F_2R.

O renderer usa labels exatos, assinaturas conhecidas da superficie anterior, limite de 32 caracteres visiveis e comparacao estrutural mascarada.

Entrada:

`python3 scripts/render_lembrantes_lower_surface.py --check`

Os tres arquivos entram no backup transacional do build. O auditor global analisa a versao renderizada, e a CI mantem gates independentes para os andares inferiores e para o nucleo superior.

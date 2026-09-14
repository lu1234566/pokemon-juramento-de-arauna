# Os encontros selvagens

O pacote `Arauna_Encounter_Table_v2` entrou inteiro, mais um remendo em C que ele
traz junto e sem o qual uma espécie fica sem casa.

## O que ele mexe, e o que ele não mexe

A tabela nova foi comparada com a antiga antes de entrar, tabela a tabela:

| | |
|---|---:|
| tabelas de encontro, antes e depois | 220 e 220 |
| tabelas só de um lado | 0 |
| **taxas de encontro alteradas** | **0** |
| **tamanhos de tabela alterados** | **0** |
| **faixas de nível alteradas** | **0** |
| tabelas em que alguma espécie muda | 209 |

Só muda **qual espécie cada slot nomeia** — a mesma disciplina que o repositório
já exigia de si mesmo. Nenhuma constante de espécie e nenhum nome de mapa que o
pacote usa é desconhecido do repositório.

## As afirmações do pacote, conferidas por fora

Não bastam os relatórios dele; refiz cada conta com a ferramenta do repo:

| afirmação | conferido |
|---|---|
| 0 lendários/míticos em grama, água ou pesca | **0**, confirmado |
| 293 espécies capturáveis no wild | **293** |
| iniciais só no Safari pós-game | Safari Zone Southeast, #1 e #7 na grama, #4 na água |
| nenhum comum impossível de obter | **uma exceção**, abaixo |

### A exceção: #121 Pirarim

Ele não aparece em tabela nenhuma. Existe só na vaga rara de pesca da Route 119,
que o Emerald codifica em C, fora das tabelas — o `sWildFeebas` de
`src/wild_encounter.c`. Sem o remendo que o pacote traz, o Pirarim é
inalcançável. O nome do próprio campo no relatório do pacote já avisa disso
(`non_special_reachable_with_evolution_and_pirarim`), e a auditoria chegou nisso
por conta própria.

O remendo também conserta um defeito de verdade herdado do Emerald: `SPECIES_FEEBAS`
é o **#349 Aracuã**, que é **Flying/Normal**. Deixar como estava faria o sistema
secreto de pesca da Route 119 tirar um pássaro da água. O `SPECIES_RHYDON` que
entra no lugar é o #121 Pirarim, Water/Water. Conferido nos dois sentidos.

## Os 21 lendários que ficaram sem casa

Aqui está o custo real de instalar este pacote hoje, e ele não foi escondido.

O pacote tira os 31 especiais das tabelas aleatórias de propósito, e o plano de
encontros estáticos ainda não existe. Oito deles já têm encontro por script
herdado do Emerald e dois são os errantes — sobram **21 sem nenhuma forma de
serem obtidos**. Antes deste pacote eles estavam espalhados na grama; depois
dele, não estão em lugar nenhum.

O gate de disponibilidade reprovou, e com razão. A resposta não foi desligá-lo:

- ele **falha** se qualquer Pokémon **comum** ficar inalcançável, que é o que ele
  sempre existiu para impedir;
- um especial inalcançável só passa se estiver nomeado em
  `docs/arauna/ESPECIAIS_ESTATICOS.csv`, que é o plano do pacote trazido para
  dentro do repositório, com os 31 e o lugar que cada um espera;
- o gate imprime os 21 e onde cada um deveria ficar, toda vez que roda.

Assim o buraco tem exatamente o tamanho que o arquivo diz, não pode crescer em
silêncio, e fechar um deles é apagar uma linha. Testado de propósito: tirando a
linha do #329 do plano, o gate reprova e nomeia "#329 Guaraciana".

> **Conflito a resolver junto com o plano estático:** #380 Selenê e #381
> Zumbi-Rei estão no plano como santuário, mas hoje são os **errantes** do
> Emerald — `src/roamer.c` os solta pelo mapa. São obtíveis por isso, e é por
> isso que sobram 21 e não 23. Quando o santuário existir, é preciso decidir se
> eles continuam errando ou não.

## Um ponto cego do gate, fechado

O gate lia as tabelas e os scripts, e só. O Pirarim mostrou que isso não basta:
espécie que o motor produz de dentro do C — a vaga rara de pesca, os errantes —
era invisível para ele. Agora `build_availability.py` também lê
`src/wild_encounter.c` e `src/roamer.c`.

## Conferido no emulador

Duas amostras, de dois pontos diferentes da Route 101, em partidas separadas:

| encontro | espécie | estava na tabela antiga? |
|---|---|---|
| 1 | #104 Zebuim | **não** |
| 2 | #378 Preazinho | **não** |

As duas são espécies que **só** existem na tabela nova naquele mapa — a antiga
tinha Casulete, Preguim, Aranin, Teiuzim, Mulinha, Cavalim e Pedrinha. O jogo
está lendo a tabela instalada, e não uma cópia velha em cache.

## Se for mexer nisso

`tools/arauna/build_availability.py --write` **planta espécies em slots
sobrando** para tapar buracos de disponibilidade. Rodá-lo agora passaria por
cima da ecologia deste pacote. Ele continua útil como diagnóstico (`--check`),
mas a fonte da tabela passou a ser o pacote, não ele.

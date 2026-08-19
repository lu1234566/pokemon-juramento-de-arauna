# Missoes do Ceu — confronto pelo uplink regional

Este lote cura `MossdeepCity_SpaceCenter_2F` como o confronto principal em MISSOES DO CEU sem alterar a batalha dupla, a selecao de equipe ou a progressao herdada do Emerald.

O nome regional ja e canonico no repositorio: `MAPSEC_MOSSDEEP_CITY` -> `MISSOES DO CEU`.

## Premissa

A infraestrutura de MISSOES DO CEU possui antenas e um uplink capaz de cobrir grande parte de Arauna.

Na superficie narrativa, isso cria um risco coerente com o ARQUIVO VIVO: a mesma rede pode permitir sincronizacao remota de sensores de VINCULO em escala regional.

Os LEMBRANTES ocupam o andar para impedir que essa capacidade fique disponivel ao HORIZONTE.

## Objetivo de Luzia

LUZIA pretende:

- usar o transmissor para circular os registros/provas de M'BOI;
- destruir a chave de sincronismo que permitiria acionar sensores remotamente;
- devolver a infraestrutura civil depois disso.

A intencao continua distinta da politica do HORIZONTE, mas o metodo repete o problema central de Arauna: decidir por toda uma populacao sem consentimento.

## Seu Bento

O slot interno de Steven e preservado.

SEU BENTO confronta a tomada da rede porque:

- o uplink e infraestrutura civil, nao apenas equipamento do HORIZONTE;
- impedir uma faccao de controlar a rede tomando-a para outra faccao ainda e controle;
- pessoas sem participacao no conflito dependem dessa infraestrutura.

Por isso ele pede ajuda ao jogador e a batalha dupla herdada passa a funcionar como defesa da autonomia da rede, nao como defesa de combustivel de foguete.

## Raul e os Lembrantes

RAUL continua usando os slots internos de Tabitha ja existentes.

Os tres LEMBRANTES que enfrentam o jogador no corredor deixam de repetir paragrafo generico. Eles comunicam:

- o risco de sincronizacao regional;
- a ordem de RAUL para segurar o andar;
- a existencia da chave de sincronismo;
- o plano de LUZIA de transmitir provas antes de destruir a chave;
- duvidas sobre atingir uma infraestrutura usada por civis.

## Desfecho

Depois da batalha dupla, LUZIA reconhece que tomar a rede para impedir que outros a controlem ainda significa tomar a rede.

Ela retira os LEMBRANTES e decide buscar outra forma de fazer as provas de M'BOI circularem.

SEU BENTO informa que a rede ficou livre dos dois lados e mantem o convite original para o jogador visita-lo em casa.

## Estrutura preservada

Permanecem intactos:

- `TRAINER_MAXIE_MOSSDEEP`;
- `TRAINER_TABITHA_MOSSDEEP`;
- `TRAINER_GRUNT_SPACE_CENTER_5/6/7`;
- parties, IA, classes e sprites;
- `SPECIAL_BATTLE_STEVEN`;
- `SavePlayerParty`, `ChooseHalfPartyForBattle`, `ReducePlayerPartyToSelectedMons`, `LoadPlayerParty`;
- `FRONTIER_DATA_SELECTED_MON_ORDER`;
- tratamento de derrota/whiteout;
- `VAR_MOSSDEEP_CITY_STATE`;
- `VAR_MOSSDEEP_SPACE_CENTER_STATE`;
- `FLAG_DEFEATED_MAGMA_SPACE_CENTER`;
- flags de objetos e nota;
- movimentos, coordenadas, warps, saves e progressao;
- sequencia posterior na casa de SEU BENTO.

Nenhum `scripts.inc` e commitado modificado; a camada e aplicada apenas durante o build transacional.

## Validacao

`scripts/render_missoes_ceu_confrontation.py` cobre 28 blocos visiveis.

Ele exige:

- labels exatos;
- assinatura reconhecida da superficie anterior;
- maximo conservador de 32 caracteres visiveis por segmento;
- igualdade estrutural fora dos corpos de dialogo mascarados;
- ausencia de residuos centrais como `expand the land mass`, `I'm with our leader` e a fala vanilla sobre roubo de combustivel.

Entrada:

`python3 scripts/render_missoes_ceu_confrontation.py --check`

`MossdeepCity_SpaceCenter_2F/scripts.inc` entra no backup de `scripts/build_arauna.sh`, e o auditor global analisa a superficie renderizada.

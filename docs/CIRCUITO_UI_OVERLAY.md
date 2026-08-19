# Circuito de Batalha: camada global de UI

Este lote converte a superficie textual global herdada da Battle Frontier sem alterar identificadores, saves, flags, mapas ou graficos.

## Estrategia

`src/strings.c` permanece intacto no repositorio. Durante `scripts/build_arauna.sh`:

1. o arquivo e copiado para um backup temporario;
2. `scripts/render_arauna_frontier_ui.py` aplica 27 substituicoes exatas e auditaveis;
3. a ROM e compilada normalmente;
4. um `trap EXIT` restaura o `strings.c`, inclusive se o build falhar ou for interrompido.

Isso evita uma reescrita de um arquivo C muito grande pelo conector e mantem a alteracao reversivel.

## Superficie convertida

- `BATTLE FRONTIER` visivel -> `CIRCUITO DE BATALHA`;
- `Battle Points` -> `PONTOS DE BATALHA` e abreviacao `PB`;
- titulos curtos do Passe: `SIMBOLOS`, `REG. BATALHA`, `PONTOS DE BATALHA`;
- acoes do Passe e mapa;
- mensagens de batalha registrada;
- nomes dos sete simbolos;
- descricoes das sete instalacoes;
- textos de Pontos de Batalha exibidos no Trainer Card/records quando usam os mesmos `gText_*` globais.

## Nomes das instalacoes

Os nomes proprios `BATTLE TOWER`, `BATTLE DOME`, `BATTLE PALACE`, `BATTLE ARENA`, `BATTLE FACTORY`, `BATTLE PIKE` e `BATTLE PYRAMID` continuam inalterados neste lote. Eles sao tratados como nomes proprios provisoriamente para nao inventar uma traducao isolada para `BATTLE PIKE` e para permitir uma futura decisao unica para as sete instalacoes.

## Validacao

`python3 scripts/render_arauna_frontier_ui.py --check`

O comando exige que cada um dos 27 anchors originais exista exatamente uma vez e confirma que todos os alvos renderizados substituem a superficie antiga.

`scripts/audit_visible_residue.py` audita a versao renderizada de `src/strings.c`, portanto nao conta como pendencia um texto legado que so existe como fonte de entrada para esta camada.

## Fora de escopo

Qualquer texto incorporado diretamente em PNG/tilemap do Frontier Pass ou de outras telas continua sendo divida de arte e nao e alterado aqui.

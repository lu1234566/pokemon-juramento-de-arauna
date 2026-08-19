# Aguas de M'Boi — vida cotidiana e Kiri

Esta camada complementa `AGUAS_MBOI_TORRE_BRIDGE.md`. A crise principal continua pertencendo a `render_aguas_mboi_surface.py`; este lote cuida apenas da superficie cotidiana que permanece visivel antes/depois da crise.

## Cidade

Oito blocos adicionais deixam de exibir texto vanilla ou repeticoes genericas:

- um morador descreve a geografia vertical e aquatica de AGUAS DE M'BOI;
- um garoto fala sobre nunca ter visto o ceu sem a borda da cratera;
- o comentario de turista deixa de citar SOOTOPOLIS;
- duas falas descrevem a cratera e o ceu noturno como parte da identidade local;
- dois dialogos pos-crise registram o habito de conferir nomes e o aparecimento das primeiras memorias alheias;
- a explicacao de WATERFALL usa `HM`, `INSIGNIA NASCENTE` e `GINASIO de AGUAS DE M'BOI`, sem `HIDDEN MACHINE` ou nome vanilla.

Nenhuma coordenada, evento, warp ou comportamento de NPC e alterado.

## Kiri

Os seis textos de KIRI vivem em `data/text/berries.inc`, mas os labels sao exclusivos de Sootopolis/AGUAS DE M'BOI. Por isso eles podem ser localizados sem tocar nos NPCs de berries das outras rotas.

A nova superficie preserva a ideia original de nomes como desejos familiares, o que combina com o tema de memoria e identidade de Arauna:

- KIRI pergunta o nome do jogador;
- explica que os pais escolheram o nome como desejo de saude e gentileza;
- entrega as berries normalmente;
- pergunta que desejo existe no nome do jogador;
- mantem a conversa sobre estacoes e o outono.

## Estrutura preservada

Continuam exatamente como estavam:

- `FLAG_DAILY_SOOTOPOLIS_RECEIVED_BERRY`;
- `dotimebasedevents`;
- o sorteio da primeira berry;
- a escolha Figy/Iapapa da segunda berry;
- todos os `giveitem` e tratamentos de bolsa cheia;
- o `MSGBOX_YESNO` sobre a estacao;
- entrega da HM, flags e requisitos de WATERFALL;
- Ginasio, insignia, saves e progressao.

## Arquitetura

`scripts/render_aguas_mboi_daily_surface.py` importa a camada de crise ja aprovada, aplica-a primeiro e depois adiciona somente os oito blocos cotidianos e seis blocos de KIRI.

O build chama apenas esta camada encadeada para AGUAS DE M'BOI, evitando aplicar o mesmo renderer duas vezes sobre o mesmo fonte.

`data/text/berries.inc` foi adicionado ao backup transacional de `scripts/build_arauna.sh`, portanto o fonte e restaurado no `EXIT` mesmo em falha/interrupcao.

O auditor global tambem renderiza esta versao final antes de procurar residuos.

## Validacao

- crise principal: `python3 scripts/render_aguas_mboi_surface.py --check`
- cotidiano/Kiri: `python3 scripts/render_aguas_mboi_daily_surface.py --check`

As duas camadas usam anchors exatos, limite conservador de 32 caracteres visiveis por segmento e comparacao estrutural mascarada.

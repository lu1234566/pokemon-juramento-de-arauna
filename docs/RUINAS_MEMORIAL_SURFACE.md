# Ruinas da Queda + Memorial dos Nomes

Este lote continua a limpeza narrativa de Arauna sem alterar a estrutura interna herdada do Pokemon Emerald.

## Ruinas da Queda

O slot `MeteorFalls_1F_1R` passa a apresentar de forma consistente o encontro que antecede a Serra da Cinza:

- os personagens dos slots Magma sao LEMBRANTES;
- os personagens dos slots Aqua sao agentes do HORIZONTE;
- Archie permanece internamente Archie, mas fala como OTACILIO;
- o METEORITE continua sendo `ITEM_METEORITE`, mas a narrativa o trata como componente capaz de alimentar o amplificador de VINCULO da Serra da Cinza;
- `METEOR FALLS`, `MT. CHIMNEY`, `TEAM AQUA`, `COZMO` e dialogo ingles deixam de aparecer nos dez blocos plot-critical renderizados;
- o pesquisador permanece no mesmo objeto/evento, mas deixa de depender da identidade vanilla de Prof. Cozmo.

Nenhum movimento, flag, `LOCALID_*`, musica, `VAR_METEOR_FALLS_STATE`, objeto ou gatilho e alterado.

## Memorial dos Nomes

O slot `MtPyre_Summit` deixa de misturar o canon de Arauna com repeticoes automaticas e restos da lenda de Hoenn.

### Ocupacao do Horizonte

Os quatro treinadores herdados de Team Aqua agora falam consistentemente como agentes do HORIZONTE. Eles recolhem e digitalizam placas do memorial, e alguns demonstram desconforto com a propria ordem.

Isso corrige o estado anterior em que esses agentes chegavam a repetir falas atribuidas a DONA ZILA ou descricoes ambientais sem relacao com a batalha.

### Registros-matriz

Os antigos orbes sao reinterpretados apenas na superficie narrativa como `REGISTROS-MATRIZ` do Memorial. Os IDs, flags e scripts de Red/Blue Orb continuam exatamente os mesmos internamente.

OTACILIO/Horizonte leva um registro; os LEMBRANTES ja haviam retirado o outro. No retorno pos-climax, OTACILIO e LUZIA devolvem os registros.

### Tradicao oral

O guardiao do Memorial passa a contar uma versao de Arauna sobre:

- as duas correntes antigas ligadas a memoria e encerramento de vinculos;
- a origem etica do JURAMENTO;
- a crise de M'BOI;
- o principio de que lembrar tudo e apagar a dor a qualquer custo podem se tornar violencia quando uma pessoa decide pelos demais.

Os prompts YES/NO e todos os scripts que os consomem permanecem intactos.

## Emblema Lembrante

O identificador interno `ITEM_MAGMA_EMBLEM` permanece intocado, assim como sua funcao de progressao. Apenas a superficie visivel muda:

- `MAGMA EMBLEM` -> `EMBLEMA LEMB.`;
- descricao -> emblema usado pelos LEMBRANTES que abre sua base.

Isso preserva saves e scripts que dependem de `ITEM_MAGMA_EMBLEM` sem mostrar uma identidade de Team Magma ao jogador.

## Validacao

A entrada oficial e:

`python3 scripts/render_ruinas_memorial_surface_checked.py --check`

O renderer valida:

- 10 blocos das Ruinas da Queda;
- 24 blocos do Memorial dos Nomes;
- um unico anchor de nome para `ITEM_MAGMA_EMBLEM`;
- um unico bloco `sMagmaEmblemDesc`;
- largura visivel maxima de 32 caracteres;
- marcadores exatos do fonte atual;
- ausencia de mudanca estrutural fora dos corpos de dialogo selecionados.

`scripts/build_arauna.sh` inclui os quatro fontes em seu backup temporario e restaura todos no `EXIT`, inclusive em falha ou interrupcao.

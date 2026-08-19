# Arquivo Central — B1F e B2F

Este lote aprofunda a superficie narrativa dos andares herdados `AquaHideout_B1F` e `AquaHideout_B2F` sem alterar a estrutura de progressao do Emerald.

## B1F — arquivos de M'Boi

Os doze dialogos dos quatro agentes deixam de repetir frases genericas sobre o HORIZONTE e passam a formar uma descoberta progressiva dos documentos de M'BOI.

A superficie confirma apenas fatos ja estabelecidos pelo canon do repositorio:

- ANAHI participou da criacao dos primeiros sensores de VINCULO;
- o pai de CIRO morreu no desastre de M'BOI;
- CIRO recebeu apoio do HORIZONTE anos depois, sem afirmar que ele conhece todos os arquivos;
- ELIAS aprovou parte dos protocolos ligados a M'BOI;
- OTACILIO perdeu familia no desastre;
- depois de M'BOI, o ARQUIVO VIVO se tornou o projeto central de OTACILIO;
- compreender a dor de OTACILIO nao torna todas as ordens do HORIZONTE justificaveis.

O texto evita inventar uma ligacao causal nao confirmada entre a morte do pai de Ciro e o patrocinio posterior do HORIZONTE.

Os encontros estaticos com `SPECIES_ELECTRODE`, seus niveis, flags e comportamento ficam completamente fora deste lote.

## B2F — evacuacao do Arquivo

`TRAINER_MATT` ja possui a identidade visivel `BRENO` no repositorio. O identificador interno e preservado, mas os quatro dialogos centrais passam a usar Breno de forma consistente.

A cena agora comunica que:

- o embarque de dados ja comecou;
- Breno esta atrasando o jogador para permitir a retirada;
- OTACILIO concluiu a carga e partiu para M'BOI;
- a rota do submersivel termina nas CAVERNAS DE M'BOI;
- copias locais e chaves de acesso estao sendo apagadas durante a evacuacao;
- servidores ligados a M'BOI foram priorizados;
- OTACILIO levou uma copia integral dos registros de VINCULO;
- nem todos os funcionarios conhecem a historia completa de M'BOI.

Isso substitui o restante visivel de `BOSS`, `LILYCOVE`, ingles e referencias genericas a uma caverna sob o mar.

## Estrutura preservada

Continuam intactos, entre outros:

- `TRAINER_MATT` e todos os `TRAINER_GRUNT_AQUA_HIDEOUT_*`;
- `FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE`;
- objeto e movimento do submersivel;
- `VAR_TEMP_1`, `VAR_0x8008`, `VAR_0x8009`;
- `LOCALID_*`;
- encontros com Electrode;
- batalhas, parties, IA, coordenadas, warps, saves e progressao.

## Validacao

`python3 scripts/render_arquivo_central_surface.py --check`

O renderer valida:

- 12 blocos no B1F;
- 13 blocos no B2F;
- marcadores exatos do fonte atual;
- limite conservador de 32 caracteres visiveis por segmento;
- ausencia de alteracoes fora dos corpos de dialogo selecionados.

`scripts/build_arauna.sh` inclui os dois arquivos no backup temporario, aplica a camada e restaura os fontes no `EXIT`, inclusive em falha ou interrupcao.

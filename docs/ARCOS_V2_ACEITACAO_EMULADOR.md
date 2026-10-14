# Arcos V2 — aceitação técnica no emulador

**Registro histórico de 12/10/2026.** A continuação de 14/10 fechou a captura
e o CONTINUE final do Uivo na ROM corrigida; ver
[REMAINING_RUNTIME_QA_20261014.md](REMAINING_RUNTIME_QA_20261014.md).
Os demais cenários abaixo continuam identificados pela ROM histórica.

Data: 12/10/2026. Commit da ROM testada: `5c59b75ca91a6bedb212f788f5d1291aa1ed33ab`.
SHA-256: `556aa2ad960cfe16664f66e80699c9c7df15bb2c6b69d5ed7e9e8eb6922790eb`.
Origem: artefato oficial do CI 1423. Engine: mGBA 0.10.2.

## Método e alcance

A ROM foi executada sem patch. Condições de entrada dos casos isolados
(Liga, insígnias, estados anteriores, posição, mochila e equipe) foram
preparadas em RAM. Depois disso, os eventos compilados, opções, ataques,
derrotas, retornos e recompensas rodaram no engine. A jornada da Torre
percorreu seus eventos de 0 a 9 sem escrever estados intermediários;
deslocamentos entre interações foram preparados em RAM.

Derrotas usaram uma criatura de nível 1. Casos de vitória usaram uma criatura
de nível 100, com HP e atributos reforçados para 999 para testar os eventos
de forma determinística. Não houve escrita do resultado da batalha, da vida
dos adversários ou da conclusão para forçar vitória. Isso não avalia
balanceamento e não equivale a uma campanha natural desde NEW GAME.

Os quatro checkpoints confirmados de persistência foram gravados pelo
diálogo de SAVE do jogo, usando o comando normal SaveGame, no flash de
128 KiB, e abertos por CONTINUE em novos processos do mGBA. Não se usou
savestate nessas provas. Um savestate temporário criado depois do
carregamento a frio permitiu comparar as três custódias.

## Resultados confirmados

| Caso | Resultado observado |
|---|---|
| Meira: derrota | Resultado 2; recuperação em Petalburg; estado 6; conclusão ausente; script encerrado e controle liberado. |
| Recepção e registros | Recusa mantém estado 0; evacuação, lotes 3→1→2, Zila, Ciro e documentos em ordem alternativa levam ao estado 6. |
| Meira: vitória e adiamento | Resultado 1 e flag do treinador; estado 8; recusar todas as custódias deixa a conclusão pendente. |
| Custódia após CONTINUE | As três opções levam a estado 9 e guardam valores 1/2/3; resultado de batalha permanece 0 na nova sessão, sem repetir Meira. |
| Fogueira: derrotas | Perder no primeiro agente, no segundo ou em Breno mantém estado 1 e flags dos treinadores anteriores. |
| Fogueira: retomada | O guardião retoma a defesa; agentes vencidos são pulados; vitória em Breno chega ao presságio, estado 3. |
| Retorno pós-Torre | Liga e Torre permitem despertar e uma SACRED ASH; repetição não acrescenta outro item. |
| Mochila cheia | SACRED ASH mantém estado 3; SOOTHE BELL mantém estado 7 do Uivo. Liberar espaço permite concluir. |
| Save legado da Fogueira | Estado 4 sem flag de despertar recebe a nova cena depois da Torre sem outra SACRED ASH. |
| Uivo: consentimento | Recusar o relato mantém estado 0. |
| Uivo: compromisso | Recusar as três alternativas mantém estado 6; as alternativas aceitas guardam valores 1/2/3. |
| Uivo: replay | Nos ramos devolvido/capturado, mantém estado 8, compromisso e quantidade de SOOTHE BELL. |
| Filhote: derrota | Resultado 2; mantém estado 4 e permite voltar. |
| Filhote: vitória | Resultado 1; desfecho de retorno à família; estado 5. |
| Filhote: fuga | Resultado 4; mantém estado 4 e filhote disponível. |
| Filhote: captura real | MASTER BALL pelo menu normal da mochila; resultado 7, estado 5, flag de captura e equipe com duas criaturas. |

Os testes do segundo e terceiro oponentes da Fogueira foram isolados com
flags dos anteriores como condições de entrada. A retomada do primeiro
percorreu as três vitórias consecutivas no engine. Os ramos de replay foram
preparados por flag; a captura real foi testada separadamente.

## Persistência confirmada

| Momento gravado | Estado após abrir CONTINUE em novo processo |
|---|---|
| Torre antes de Meira | Estado 6; escolhas, lotes e documentos preservados. |
| Meira vencida; custódia adiada | Estado 8; treinador vencido; conclusão ausente. |
| Torre concluída | Estado 9; custódia 1; conclusão presente. |
| Fogueira após recompensa | Estado 4; despertar presente; uma SACRED ASH. |

Os quatro carregamentos chegaram a CB2_Overworld, com contexto de script
[2, 0] e controles liberados. O resumo legível por máquina está em
[emulator_acceptance_summary.json](../review/arcos_v2/emulator_acceptance_summary.json).

## Evidências e interrupção do ambiente

Esses resultados foram observados nos retornos do mGBA durante a sessão.
O ambiente reiniciou no intervalo antes do commit: os logs completos,
capturas de tela, scripts de diagnóstico e arquivos de save locais não
ficaram disponíveis para esta publicação. Por isso o JSON contém um
resumo reconstruído das observações confirmadas, não os recibos brutos.

O teste seguinte pretendia concluir Uivo depois da captura e abrir seu
save em novo processo; não houve retorno confirmado dessa execução antes
do reinício. Esse quinto carregamento permanece pendente. A captura real
em si já teve seu resultado confirmado antes da interrupção.

ROM, harness, saves e savestates não são incluídos no repositório.

## Validação de fonte e limites restantes

O validador atual voltou a passar: 2.240 cenários da roda, 30 de Fogueira,
1.728 da Torre, sete de Uivo e 33 de ticket; 501 linhas medidas, máximo
190/208 px. O checker dos assets e do status de Libras também passou.
Essas contagens são do modelo, não do emulador.

Os sprites e as dez saídas da Torre foram aceitos na rodada anterior,
na mesma ROM. Permanecem pendentes a campanha natural completa,
balanceamento, carregamento final do Uivo capturado, aprovação autoral,
tradução/revisão qualificadas de Libras e os eixos/finais canônicos completos.
Não houve merge para main.

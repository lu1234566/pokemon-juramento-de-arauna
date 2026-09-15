# Os eventos dos lendários e míticos

O pacote `Arauna_Eventos_Lendarios_Miticos_31` foi auditado e **não foi
instalado**, porque não há nele o que instalar. Isto não é crítica ao pacote: é
o que o próprio README dele diz.

## O que o ZIP contém

> "Pacote de desenvolvimento para revisão. **Não altera o Git e não implementa
> automaticamente no ROM.**" — `README.md` do pacote

Trinta e um arquivos de design, um CSV/JSON com os 31, um checklist, e trinta e
um `scripts_referencia/*.inc`. Os trinta e um scripts foram comparados entre si
depois de normalizar espécie, nível e nome: **é uma forma só**, o mesmo modelo
repetido trinta e uma vezes. Cada um abre com

> `@ NÃO integrar sem revisão de flags/local.`

e traz, em vez de lógica, comentários do que falta: `@ validar desbloqueio`,
`@ captura -> marcar CAUGHT`, `@ derrota -> regra de respawn aprovada`.

Nenhum dos treze comportamentos concretos descritos na mensagem está no pacote:
não há a escolha na TV, o sistema de roaming, o puzzle do triângulo, o santuário
novo da Route 119, a troca de local dos Regis, nem a remoção de sprite nenhuma.

A única coisa do pacote que o repositório já tinha pronta é a música:
`MUS_ARAUNA_LEGEND_ENCOUNTER` existe, é a 622.

## O que o jogo já faz hoje

Os encontros herdados do Emerald estão todos vivos e **coerentes**: em cada um
deles, a criatura que aparece no mapa é a mesma que você enfrenta.

| lugar | quem está lá hoje | nível | sprite no mapa |
|---|---|---:|---|
| Ancient Tomb | **#379 Solaris** | 40 | Registeel |
| Desert Ruins | **#377 Piraruaçu** | 40 | Regirock |
| Island Cave | **#378 Mata-Mata** | 40 | Regice |
| Sky Pillar Top | **#384 Curupixel** | 70 | Rayquaza |
| Birth Island | **#386 Arauá** | 30 | Deoxys |
| Navel Rock, fundo | #258 Oxalá | 70 | Lugia |
| Navel Rock, topo | #259 Saciamigo | 70 | Ho-Oh |
| Faraway Island | #160 Carcará | 30 | Mew |
| Southern Island | #380 Selenê / #381 Zumbi-Rei | 50 | Latias / Latios |
| Marine Cave | **#382 Iemanjã** | 70 | — |
| Terra Cave | **#383 Oxumará** | 70 | — |

Duas das treze linhas da mensagem **já são verdade**: Iemanjã na Marine Cave e
Oxumará na Terra Cave. As outras onze descrevem uma **troca de lugar** em
relação ao que existe — o design quer Verdejante no Ancient Tomb no lugar do
Solaris, Arauá no Sky Pillar no lugar do Curupixel, e assim por diante.

## Por que não implementei a troca por conta própria

Três razões, e a terceira é a que pesa.

**Deslocamento.** Tirar Piraruaçu, Mata-Mata e Solaris das câmaras dos Regis
para levá-los a Navel Rock e a um santuário novo é seguro do lado de quem sai —
#160, #258 e #259 são capturáveis na natureza, conferido. Mas é uma cadeia de
mudanças que precisa acontecer inteira ou nenhuma, senão sobra criatura sem casa.

**Níveis.** O design pede 60 onde hoje é 40, e 75 onde hoje é 70. Isso muda o
ritmo do pós-jogo, e o teto de nível do jogo hoje é 58 para o Campeão.

**Os sprites.** Este é o ponto. Cada um desses oito lugares coloca no mapa o
boneco da criatura do Emerald: `OBJ_EVENT_GFX_REGISTEEL` no Ancient Tomb,
`OBJ_EVENT_GFX_LUGIA` em Navel Rock, `OBJ_EVENT_GFX_DEOXYS` na Ilha do
Nascimento. Hoje o boneco e a batalha **combinam**. Trocar só a espécie da
batalha faria o jogador andar até um Registeel e lutar contra um Verdejante.

> **Correção:** numa primeira leitura eu disse que não havia arte própria
> disponível porque `OBJ_EVENT_GFX_ARAUNA_POKEMON_A/B` apontam para o NinjaBoy.
> Os dois ids são **despachantes** — `VAR_ARAUNA_OW_A`/`_B` escolhe o gráfico em
> tempo de execução no registry próprio de Arauana, e o NinjaBoy é só o resto da
> tabela estática, que nunca é lida para eles. O impedimento real é outro e
> continua valendo: **Verdejante, Terraão, Marulho e Estrelinha não estão entre
> as 46 do registry**. O caminho para resolver isso está em
> `docs/OVERWORLD_LENDARIOS_PENDENTE.md`.

## O que foi feito

Achei um terceiro ponto cego no gate de disponibilidade, procurando por estes
eventos. Ele varria `givemon`, `setwildbattle` e `createmon`, mas **não**
`seteventmon` — que é como **todas** as ilhas de evento entregam o seu lendário.
Seis espécies eram invisíveis para ele por isso.

Uma delas é o **#386 Arauá**, que está na Ilha do Nascimento desde sempre e que
eu listei como "sem casa" no commit anterior. Era erro meu, herdado do gate.
Corrigido: são **20** esperando lugar, não 21.

## O caminho mais curto para fechar os 20

Sem inventar mapa nenhum, o repositório tem onze pontos de encontro estático já
funcionando. Se a troca for aprovada como está desenhada, ela libera três casas
(as câmaras dos Regis, com Piraruaçu, Mata-Mata e Solaris indo para Navel Rock e
para o santuário novo) e fecha três dos 20: **#338 Verdejante, #342 Terraão e
#344 Marulho**.

Os outros dezessete pedem lugares que ainda não existem, e a coluna `placement`
de `docs/arauna/ESPECIAIS_ESTATICOS.csv` já diz onde cada um deveria ficar.

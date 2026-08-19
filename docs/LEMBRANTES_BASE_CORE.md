# Base dos Lembrantes — nucleo superior

Este lote cura os andares `MagmaHideout_3F_1R`, `MagmaHideout_3F_2R` e `MagmaHideout_4F` como o nucleo superior da BASE DOS LEMBRANTES.

Ele nao altera o labirinto, batalhas ou progressao herdados do Emerald. A mudanca e exclusivamente na superficie narrativa visivel.

## Problema anterior

A base ja usava nomes e conceitos de Arauna, mas quase todos os NPCs repetiam quatro paragrafos genericos:

- guardar um nome como resistencia;
- HORIZONTE querendo uma Arauna estavel;
- historia inconveniente virando `ruido` e desaparecendo;
- divergencia interna sobre devolver memorias sem permissao.

No 4F, a repeticao atingia a propria cena de LUZIA. RAUL ainda tinha uma fala de derrota em ingles (`Taken down again`).

## 3F — preparacao do Registro-Matriz

O 3F agora explica progressivamente que:

- o REGISTRO-MATRIZ responde a VINCULOS antigos;
- ele nao e um recipiente de memoria;
- ele indica para onde memorias foram empurradas;
- LUZIA pretende usar o registro para abrir a corrente e permitir o retorno;
- os sensores ja estao fora da escala antes da ativacao;
- parte dos LEMBRANTES percebe que o procedimento deixou de parecer controlado;
- RAUL fechou o acesso ao nucleo;
- um dos membros pede ao jogador que nao entregue o registro ao HORIZONTE, mas tambem nao permita que LUZIA o use sem limite.

Assim a faccao continua moralmente distinta do HORIZONTE sem ser tratada como automaticamente correta.

## 4F — Raul e Luzia

`TRAINER_TABITHA_MAGMA_HIDEOUT` continua internamente intacto. O nome visivel ja existente `RAUL` e usado nos dialogos.

RAUL:

- bloqueia o acesso ao nucleo;
- admite que segue LUZIA porque viu familias apagadas dos registros;
- reconhece que isso nao elimina o medo do que a ativacao pode causar.

LUZIA:

- usa o REGISTRO-MATRIZ para localizar o que o ARQUIVO arrancou;
- tenta devolver essas memorias a Arauna;
- percebe que a corrente nao esta obedecendo ao registro e esta puxando em escala muito maior;
- enfrenta o jogador sem aceitar que isso torne o HORIZONTE correto;
- depois da derrota, reconhece o aviso do jogador;
- constata que a corrente deixou a base e segue os sinais para o litoral/PORTO DO SAL.

O texto nao define equivalencia tecnica entre a corrente e uma especie lendaria especifica. `SPECIES_GROUDON` permanece como mecanismo interno herdado.

## Estrutura preservada

Permanecem intactos:

- `TRAINER_MAXIE_MAGMA_HIDEOUT`;
- `TRAINER_TABITHA_MAGMA_HIDEOUT`;
- todos os `TRAINER_GRUNT_MAGMA_HIDEOUT_*` envolvidos;
- parties, IA e itens dos treinadores;
- `SPECIES_GROUDON` e objetos correspondentes;
- musica, orb effect, tremores e movimentos;
- `VAR_SLATEPORT_CITY_STATE`;
- `VAR_SLATEPORT_HARBOR_STATE`;
- `FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT`;
- flags de objetos e grunts;
- coordenadas, warps, saves e progressao.

## Validacao

`scripts/render_lembrantes_core_surface.py` cobre 26 blocos:

- 6 em `3F_1R`;
- 3 em `3F_2R`;
- 17 em `4F`.

O renderer exige labels exatos, uma assinatura reconhecida da superficie anterior, limite conservador de 32 caracteres visiveis por segmento e igualdade estrutural fora dos corpos de texto mascarados.

Entrada de validacao:

`python3 scripts/render_lembrantes_core_surface.py --check`

Os tres fontes entram no backup transacional de `scripts/build_arauna.sh` e sao restaurados no `EXIT`.

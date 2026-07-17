# Estratégia de placeholders — Pokédex de Arauna

## Decisão

Durante o desenvolvimento, batalhas, eventos, encontros e testes podem usar
Pokémon oficiais disponíveis no motor. Cada espécie definitiva de Arauna terá um
número fixo na Pokédex e, quando necessário, um `SPECIES_*` oficial reservado
como casca técnica temporária.

O número da Pokédex de Arauna e o ID interno do motor são conceitos separados.
Por exemplo, **Caramelo é #001 em Arauna**, embora sua casca atual seja
`SPECIES_TORCHIC`. A ordem regional exibida no jogo será definida pela coluna
`arauna_slot`, não pelo número nacional original do placeholder.

## Vantagens

- scripts e equipes podem ser escritos antes da arte final;
- evoluções e saves continuam apontando para um ID interno estável;
- a troca futura não exige refazer cada treinador ou evento;
- os placeholders mantêm o vertical slice jogável;
- sprites externas continuam fora do jogo até aprovação explícita.

## Substituição futura

Quando uma espécie estiver aprovada, o registro reservado receberá:

1. nome e textos nos dois idiomas;
2. tipos, atributos, habilidades, evoluções e learnset;
3. sprite frontal, costas, ícone, animação, shiny e paletas aprovados;
4. número regional definido por `arauna_slot`;
5. testes de batalha, evolução, Pokédex e compatibilidade de save.

O Pokémon oficial deixa de aparecer quando todos esses dados forem substituídos.
Nenhuma ROM final deverá misturar silenciosamente espécies oficiais com a Dex de
Arauna.

## Regras

- cada slot de Arauna recebe no máximo um placeholder estável;
- o mesmo `SPECIES_*` não pode representar dois slots de Arauna;
- placeholders usados apenas em batalhas precisam constar no inventário técnico;
- usar um placeholder não aprova o conceito nem a sprite definitiva;
- mudanças em sprites continuam exigindo prévia e aprovação antes da integração;
- a planilha externa da Dex é a fonte criativa; os CSVs do repositório são a
  cópia estruturada usada por código e validação.

## Importação da Dex externa

O spoiler recebido confirma visualmente os slots #001–020. Eles podem ser
registrados por nome e tipos, mas fichas completas, famílias, biomas, habilidades
e artes devem ser importadas de um export estruturado da Dex externa quando ele
estiver disponível. Isso evita transcrição manual dos 386 registros.

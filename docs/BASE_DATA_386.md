# Os dados de base das 386

O pacote `Arauna_Base_Data_386_v2` entrou. Ele redefine **oito campos** de cada
espécie e deixa o resto exatamente como estava.

## O que mudou e o que não mudou

Antes de instalar, o pacote foi conferido campo a campo contra a tabela do repo.
O resultado é a razão pela qual dava para instalar sem medo:

| | |
|---|---:|
| espécies do pacote que o repo conhece | 386 de 386 |
| **diferenças nos seis base stats** | **0** |
| **diferenças de tipo** | **0** |
| constantes que o repo não conhece | 0 |

O pacote promete preservar os seis stats, os tipos, as habilidades, a cor e o
`noFlip`. Os stats e os tipos ele preserva de fato — conferido, não confiado.

Os outros três a instalação preservou **mecanicamente**, e não por confiança: o
arquivo foi fotografado antes da edição, editado campo a campo, e fotografado de
novo; os onze campos da lista protegida foram comparados espécie por espécie e
**nenhum escorregou**.

> Isso não é zelo teórico. O `species_info_base_data_preview.h` do pacote traz
> `.abilities` em cada bloco, com os valores de **antes** das 35 habilidades
> Arauna. Aplicar esse arquivo inteiro, como ele convida a fazer, apagaria as 35
> em silêncio e o build continuaria passando. A instalação nunca o usou.

### Os oito campos que mudaram

| campo | quantas espécies | como |
|---|---:|---|
| `expYield` | 386 | média +4,5; de −19 a +32; sobe em 305, desce em 81 |
| `catchRate` | 297 | média +4,3; de −145 a +110; sobe em 195, desce em 102 |
| `eggGroups` | 252 | 207 mudam de grupo; **45 são só troca de ordem** |
| `evYield` | 140 | |
| `itemRare` | 109 | espécies que agora carregam item raro; nenhuma carregava |
| `eggCycles` | 102 | |
| `growthRate` | 68 | |
| `friendship` | 34 | |
| `genderRatio` | 9 | os iniciais viraram 12,5% fêmea, como manda a convenção |

As 45 trocas de ordem de `eggGroups` não mudam nada em jogo — a checagem de
compatibilidade olha os dois grupos dos dois lados — mas estão contadas à parte
para o número 252 não assustar mais do que deve.

## Conferido no emulador

Não basta a tabela bater com o JSON; o jogo tem que ler a tabela. A curva de
crescimento é o melhor teste disso, porque ela decide sozinha a experiência de um
Pokémon num dado nível:

| espécie | o pacote diz | lido da RAM no nível 30 | confere? |
|---|---|---|---|
| #010 Formilim | `GROWTH_FAST` | exp 21600 = 4·30³/5 | sim |
| (vizinha, curva diferente) | `GROWTH_MEDIUM_FAST` | exp 27000 = 30³ | sim |
| #046–048 família pseudo | `GROWTH_SLOW`, amizade 35 | exp 33750 = 5·30³/4, amizade 35 | sim |

A vizinha com outra curva na mesma leitura importa: mostra que a mudança é por
espécie, e não um valor global que por acaso deu certo.

## Os 76 achados, que continuam abertos

O pacote **não** corrigiu os seis base stats, e fez bem: metade do balanceamento
do jogo não deve virar de lado por uma fórmula. Ele listou os problemas em
`reports/AUDIT_FINDINGS.md`. Estão repetidos aqui porque são decisões suas, não
do código:

| o quê | quantos |
|---|---:|
| BST acima de 600 sem ser lendário nem mítico | 36 |
| *spreads* exatamente repetidos entre espécies | 34 |
| iniciais finais acima do padrão (595, 595, 574 contra ~525–535) | 3 |
| evolução que **não** aumenta o BST | 2 |
| BST baixo demais | 1 |

Os *spreads* repetidos são o achado mais pesado. Há grupos de **17 espécies**
com os seis stats idênticos — por exemplo `75, 72, 78` nas três últimas colunas
aparece em dezenas de criaturas, com só as três primeiras variando. Isso é
assinatura de preenchimento procedural, não de design.

Dois achados o relatório chama de erro objetivo, e os dois merecem uma correção:

- **#049 Borbolim → #050 Casulete**, BST caindo de 287 para 283;
- **#163 Corurupim**, "evolui para o próprio #163".

**Nenhum dos dois é o que parece.** Fui conferir no repo antes de repetir:
`src/data/pokemon/evolution.h` **não declara uma única evolução** — nem para
essas duas espécies, nem para nenhuma das 386. Não existe autoevolução no
arquivo, existe arquivo vazio.

O que o relatório está descrevendo é o modelo de família do **próprio pacote**,
que infere parentesco por número de Pokédex consecutivo. Conferido: das 81
espécies que o pacote trata como tendo evolução, o repo confirma **zero**, e o
#163 é um caso de `family_length = 2` numa família que só tem um membro — daí a
comparação dele consigo mesmo.

Ou seja: o achado verdadeiro é maior e mais simples do que os dois listados —
**o jogo não tem tabela de evoluções**. Isso não se conserta em dados de base;
é o assunto do pacote de evoluções.

## Se for mexer nisso

A fonte é `master/base_data_386.json`. A instalação é uma edição em cima do
`species_info.h` existente, campo a campo, **nunca** a substituição do arquivo
pelo preview do pacote — pelo motivo do aviso lá em cima.

# As evoluções

O pacote `Arauna_Evolutions_v2` entrou. **Ele mexe em cinco linhas**, e essa é a
notícia mais importante da auditoria.

## O que já estava certo

A expectativa era instalar uma tabela nova. Conferido antes de mexer, o repo já
tinha as 81 relações — e as 81 batem, uma a uma, com as do pacote:

| | |
|---|---:|
| relações no repo | 81 |
| relações no pacote | 81 |
| só no repo | 0 |
| só no pacote | 0 |
| **relações em que o método muda** | **5** |
| autoevoluções | 0 |
| ciclos | 0 |
| alvos com mais de uma origem | 0 |

O mapeamento também foi conferido contra a autoridade do próprio repositório: o
comentário `// #NNN Nome` que cada bloco de `species_info.h` carrega. As 81
origens e os 81 destinos caem no número de Pokédex certo, **sem exceção**.

Sete nomes do pacote não batem letra a letra com os do repo — "Bicho-Preguiça"
contra "Preguiça", "Mula-sem-Cabeça" contra "Mula-sem". Todos os sete são nomes
de mais de dez caracteres, e dez é o limite do `POKEMON_NAME_LENGTH`. São a mesma
criatura com a grafia curta que cabe na tela, não um erro de mapeamento.

## As cinco que mudaram

De nível para um método com intenção:

| espécie | era | virou |
|---|---|---|
| #017 Curupim → #018 Curupira | nível 34 | **amizade** |
| #092 Morcego → #093 Vampiro | nível 32 | **MOON STONE** |
| #098 Mula → #099 Mula-sem-Cabeça | nível 34 | **FIRE STONE** |
| #163 Corurupim → #164 Coruja | nível 24 | **amizade, de noite** |
| #362 Beija-Luz → #363 Beija-Sol | nível 40 | **SUN STONE** |

As outras 76 continuam por nível, iniciais em 17/36 e a família pseudo por nível.

### As três pedras existem e são achá­veis

Uma evolução presa atrás de um item que o jogo não dá é um beco sem saída, então
isso foi conferido no mundo, não só na tabela de itens:

| pedra | onde |
|---|---|
| MOON STONE | bola de item em Meteor Falls 1F/1R |
| FIRE STONE | bola de item em Fiery Path, e o trocador de cacos da Route 124 |
| SUN STONE | dada por um NPC no Centro Espacial (Missões do Céu) |

**Um alerta de ritmo:** a SUN STONE vem de Missões do Céu, que é a cidade da
sétima insígnia — o teto de nível ali é 42. O pacote quer o Beija-Sol disponível
"por volta do nível 40". Cabe, mas por pouco. Se a Beija-Luz for pensada para
entrar na equipe antes disso, a pedra precisa aparecer mais cedo.

### "De noite" aqui é de madrugada

O `EVO_FRIENDSHIP_NIGHT` do Emerald é `hora >= 0 && hora < 12`. Ou seja: o
Corurupim evolui **da meia-noite ao meio-dia**, não ao anoitecer. É a definição
do motor, não uma escolha deste pacote, e está escrita aqui porque o nome da
constante sugere o contrário.

As duas por amizade precisam de 220, e as duas espécies têm amizade base 70 —
alcançável. Se alguma delas fosse para o balde de amizade 35 que os lendários
usam, o caminho ficaria bem mais longo.

## Conferido no emulador

A prova mais forte disponível sem uma partida inteira: usar a pedra de verdade.

Com uma SUN STONE na bolsa e uma equipe de três, o menu da equipe marcou
**"No use." nos outros dois** e só a Beija-Luz como alvo válido — isto é, o jogo
leu a tabela para decidir quem responde à pedra. Usando nela: *"Beija-Luz is
evolving!"*, a animação inteira, e a espécie na RAM passou de **347 para 341**,
que é exatamente o `SPECIES_GLALIE -> SPECIES_SPHEAL` que a tabela declara.

## Um defeito que a troca destapou

O gate de disponibilidade **reprovou** a instalação: "3 unobtainable — #018
Curupira, #099 Mula-sem-Cabeça, #363 Beija-Sol". Exatamente três das cinco que
mudaram de método.

Não era um beco sem saída de verdade: `check_availability.py` só entendia
`EVO_LEVEL`. A expressão que ele usava para ler a tabela era literalmente
`\{\{EVO_LEVEL, \d+, ...\}\}`, então qualquer espécie cuja evolução deixasse de
ser por nível virava inalcançável aos olhos dele, mesmo estando a um passo de
distância. O defeito estava lá desde sempre, esperando alguém mudar um método.

Agora ele lê **todos** os métodos, e trata o único que pode de fato falhar — a
pedra — conferindo se o mundo entrega aquele item. Essa conferência lê só quem
**dá** um item (`finditem`, `giveitem`, o estoque das lojas, o trocador de
cacos) e **não** lê `src/data/items.h`, que declara todos os 388 e faria a
checagem passar para qualquer coisa. Dos 388 itens do jogo, 218 são entregues
em algum lugar e 228 não.

Testado de propósito: apontando a evolução do Beija-Luz para um item que ninguém
entrega, o gate reprova e nomeia "#363 Beija-Sol"; desfazendo, passa.

## O arquivo de sincronia da Pokédex

O pacote traz `generated/pokedex_evolution_sync.json` para acertar as 69
divergências do `pokedex.ts` do Lovable. **Ele não foi usado aqui, e não deve
ser**: a Pokédex do Emerald não mostra linha evolutiva, e o repositório não tem
nenhuma tabela que dependa desses dados. Esse arquivo é para o aplicativo
externo, não para a ROM.

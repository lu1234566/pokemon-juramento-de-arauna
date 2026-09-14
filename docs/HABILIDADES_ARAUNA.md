# As 35 habilidades

Uma habilidade exclusiva para cada forma final de inicial, para o pseudo-lendário
e para cada lendário e mítico. Ids 78 a 112, `ABILITIES_COUNT` 113 — o Emerald
parava em 77, então nada foi renumerado.

## Duas decisões que valem explicar

**A mesma habilidade nos dois slots.** É a recomendação do pacote e ela está
certa pela razão que ele dá: o Gen III não guarda *qual* habilidade o Pokémon
tem, guarda **um bit** dizendo se é a primeira ou a segunda, sorteado quando o
Pokémon nasce. Uma espécie com duas habilidades diferentes não pode garantir
nenhuma das duas. Pôr a mesma nos dois slots é a única forma de a identidade ser
sempre a planejada. As 35 estão assim, conferido: 35 pares, todos iguais.

**A constante fica em português, o nome na tela fica em inglês.** É a mesma
divisão que os golpes assinatura já usam — `MOVE_LUAR_DE_JACI` aparece como
"JACI MOON". Assim os ids e os *assignments* do pacote continuam batendo com o
código, e o gate de inglês continua passando. Dez dos nomes do pacote
(`FOGO LEAL`, `TEMPESTADE`, `NOITE ETERNA`...) estão no léxico português que o
gate recusa, então a alternativa seria quebrar o jogo inteiro em duas línguas.

## O que cada uma faz

| dono | nome na tela | o que faz |
|---|---|---|
| Draguará | LOYAL FLAME | golpes fire e dragon +15%; não pode ser queimado |
| Terolibra | WINGED WATCH | golpes water e bug +20% quando é o mais rápido |
| Petropico | GRANITE BEAK | golpes rock +20%; DEFENSE não cai |
| Boiuna | SERPENT COIL | com HP cheio, recebe 25% menos |
| Guaraciana | SUN CROWN | sol por cinco turnos ao entrar |
| Jaciana | MOON VEIL | sem clima, recebe 20% menos de golpes especiais |
| Tupanaú | TUPA VOICE | golpes electric e dragon paralisam em 1 de 5 |
| Iaraú | RIVER SONG | golpes sonoros +30% e não erram |
| Kuarahy | FIRST SUN | sob sol, golpes fire e psychic +20% |
| Yasy | FIRST MOON | sem clima, SP. DEF efetiva +25% |
| Rudarauna | ETERNAL BOND | o lado inteiro recusa quedas de atributo |
| Perybé | MANY RIVERS | ao acertar golpe water, recupera 1/16 |
| Arauanaú | GUARDIAN | golpes super efetivos causam 25% menos |
| Verdejante | FOREST RENEW | 1/16 por turno; 1/8 sob sol |
| Chuvão | STORMCALL | chuva por cinco turnos ao entrar |
| Solzão | DRY SPELL | golpes water recebidos pela metade |
| Ventania | SOUTH WIND | ao entrar, SPEED dos oponentes −1 |
| Terraão | LIVING SOIL | 1/16 por turno em tempestade de areia |
| Fogaréu | ANCIENT FIRE | golpes fire +20% e sem a penalidade da chuva |
| Marulho | MASTER TIDE | sob chuva, golpes water e dragon +20% |
| Alvorecer | FIRST LIGHT | entra curado de status e de confusão |
| Poente | LAST LIGHT | abaixo de metade do HP, dark e fire +25% |
| Estrelinha | LIVING WISH | 1/16 por turno para si e para o parceiro |
| Arauanamon | OATH | ao entrar, SP. DEF +1 |
| Boitatã | WATCHFIRE | 30% de queimar quem toca |
| Piraruaçu | RIVER KING | water e dragon +15%; não hesita |
| Mata-Mata | OLD CARAPACE | golpes super efetivos causam 20% menos |
| Solaris | ABSOLUTE SUN | sol por cinco turnos ao entrar |
| Selenê | LONG NIGHT | ao entrar, SP. ATK dos oponentes −1 |
| Zumbi-Rei | ENDURANCE | atributos não caem; não hesita |
| Iemanjã | SACRED SEA | bebe golpes water (1/4 do HP); sob chuva, fairy +20% |
| Oxumará | RAINBOW ARC | ao sobreviver a um golpe super efetivo, SPEED +1 |
| Curupixel | TURNED FEET | golpes de status ganham +1 de prioridade |
| Sacinho | WHIRLWIND | 30% de confundir quem toca |
| Arauá | ESSENCE | atributos não caem; dragon e psychic +10% |

## Onde isso mora no motor

As decisões puras ficam todas em `src/arauna_abilities.c` — quanto multiplicar,
quem recusa uma queda, o que é golpe sonoro. Os pontos que precisam empurrar um
*battle script* ficam onde o motor já guarda esse tipo de código, ao lado da
habilidade vanilla com que cada uma se parece:

| mecanismo | onde | de quem herda a forma |
|---|---|---|
| clima na entrada | `ABILITYEFFECT_ON_SWITCHIN` | Drought / Drizzle, mas com o contador de cinco turnos da Sunny Day |
| queda no lado inimigo | o mesmo bit adiado do Intimidate | Intimidate |
| cura na entrada | `ABILITYEFFECT_ON_SWITCHIN` | Shed Skin, sem o dado |
| cura por turno | `ABILITYEFFECT_ENDTURN` | Rain Dish |
| efeito de contato | `ABILITYEFFECT_ON_DAMAGE` | Flame Body |
| absorver água | `ABILITYEFFECT_ABSORBING` | Water Absorb |
| depois de acertar | `ABILITYEFFECT_ARAUNA_ATTACKER` (novo) | não havia: tudo que o motor roda no fim do golpe lê a habilidade do **alvo** |
| multiplicador de dano | fim de `CalculateBaseDamage` | Blaze / Torrent |
| super efetivo −% | fim de `Cmd_typecalc` | não havia |
| queda de atributo | `ChangeStatBuffs` | Clear Body |
| queimadura / hesitar | `Cmd_setmoveeffect` | Water Veil / Inner Focus |
| nunca errar | `AccuracyCalcHelper` | Lock-On |
| prioridade | `GetWhoStrikesFirst` | não havia |

O corte de super efetivo **tem** que ser lido no `Cmd_typecalc` e em nenhum outro
lugar: quando a fórmula de dano roda, a tabela de tipos ainda não falou; quando o
dano é aplicado, o multiplicador já está embutido e não dá mais para separar.

## As nove ressalvas

Nada aqui foi encoberto:

1. **RIVER SONG está quase sem uso.** Ela vale para golpes sonoros, e o learnset
   do Iaraú tem **um só**, UPROAR, no nível 70. Acrescentei DISARMING VOICE e
   IARA SONG à lista de golpes sonoros (são sonoros por qualquer leitura, e a
   Soundproof também deveria barrá-los), mas o Iaraú não aprende nenhum dos dois.
   **Ou o learnset dele ganha um golpe sonoro cedo, ou a habilidade fica morta.**
   É uma decisão de design, não de código, então está aqui e não foi resolvida
   por conta própria.
2. **SUN CROWN e ABSOLUTE SUN são a mesma coisa.** Vem assim do pacote: as duas
   pedem "sol forte por 5 turnos".
3. **A mensagem da queda é a genérica.** "{PKMN}'s SPEED fell!", sem citar a
   habilidade, porque a linha que o Emerald usa para o Intimidate tem a palavra
   ATTACK dentro da própria string.
4. **LIVING WISH cura o parceiro em silêncio.** Um battle script só consegue
   confirmar o HP de um battler por execução, então o parceiro é curado direto e
   só a barra dele se mexe; a fala é sobre o dono.
5. **ANCIENT FIRE desfaz a penalidade da chuva dobrando o dano**, porque a
   penalidade é uma divisão inteira que já aconteceu. É exato a menos de uma
   unidade de arredondamento.
6. **WINGED WATCH compara a velocidade com os estágios, mas ignora paralisia.**
   Ela pergunta quem é mais rápido por natureza, não quem está mancando.
7. **ETERNAL BOND só protege o parceiro em doubles.** Em singles é igual à
   ENDURANCE.
8. **"Sem clima" quer dizer sem clima em efeito** — Cloud Nine e Air Lock contam
   como sem clima para a MOON VEIL e a FIRST MOON.
9. **A IA só aprendeu duas.** Ela evita jogar água na SACRED SEA e desconta a
   DRY SPELL, e sabe procurar uma SACRED SEA no banco para receber um golpe de
   água. As outras 33 ela não conhece — é a mesma cegueira que ela já tem para
   metade das habilidades vanilla.

## O que foi conferido no emulador

Batalha selvagem de verdade, lendo a RAM de batalha:

| habilidade | medido | controle |
|---|---|---|
| SUN CROWN | `gBattleWeather = 0x0020` (sol temporário) na entrada | — |
| SOUTH WIND | estágio de SPEED do selvagem = 5 | 6 sem a habilidade |
| OATH | estágio de SP. DEF próprio = 7 | 6 |
| FIRST LIGHT | queimadura posta na equipe some ao entrar (`status1 = 0`) | a mesma queimadura sobrevive em quem não tem a habilidade (`0x10`) |
| ENDURANCE | recusou a queda do SOUTH WIND: estágio 6 | 5 quando o selvagem não a tem |
| FOREST RENEW | 50 → 53 → 56 → 59 de HP, subindo a cada turno **enquanto apanhava** | controle não ganhou um ponto em quatro turnos |

A prova da ENDURANCE precisou de uma janela estreita: `gBattleMons` só é
preenchido depois que a batalha começa, e a queda do SOUTH WIND é adiada até os
dois lados estarem em campo. A habilidade do selvagem é escrita no quadro exato
em que a espécie dele aparece — entre as duas coisas.

## Se for mexer nisso

`IS_ARAUNA_ABILITY(x)` em `include/arauna_abilities.h` separa as 35 das 78 do
Emerald sem listar nada de novo. `ABILITIES_COUNT` dimensiona as duas tabelas de
texto e nada mais — não há tabela indexada por habilidade fora de
`src/data/text/abilities.h`.

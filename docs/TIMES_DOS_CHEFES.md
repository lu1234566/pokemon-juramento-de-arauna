# Os treze times de chefe

Cada chefe tem o seu time em `docs/arauna/times/<NOME>.json`, no formato do
editor (`arauana-team` v4), e o array correspondente em
`src/data/trainer_parties.h`, com um comentário que aponta para o JSON. As
tabelas completas, com golpes, estão em `docs/DOSSIE_BETA.md`.

Dalva, Ademar e Olivia vieram do editor. As outras dez foram montadas no mesmo
padrão, a partir do learnset de cada criatura.

## O padrão

- **Cinco criaturas**, seis na dupla de Cec&Caet e na Campeã.
- **Nível escalonado** até o teto do chefe: a primeira vaga dois níveis
  abaixo (três na Campeã), a última no teto.
- **IV escalonado**: a primeira vaga começa baixa e a última tem 31.
- **Item em todas**: a da última vaga reforça o tipo do chefe (Charcoal,
  Silk Scarf, Sharp Beak, Twisted Spoon, Mystic Water, Black Glasses, Spell
  Tag, Metal Coat, Dragon Fang); as outras levam Sitrus, Lum, Leftovers,
  White Herb, Quick Claw, Scope Lens, King's Rock ou Bright Powder.
- **Golpes só do learnset da própria criatura**: por nível, TM ou golpe de
  ovo. Nenhum tutor. Um golpe de nível acima do nível da criatura é permitido,
  porque o moveset é customizado, e o `check_boss_team.py` avisa sobre ele.
- **Pelo menos um golpe do tipo do chefe** em cada criatura dos líderes e da
  Liga, mais o segundo STAB dela e cobertura contra quem bate no tipo do
  chefe. A Campeã mistura tipos.
- **Poder de TM e golpe de ovo limitado pelo ponto do jogo**: até 80 no
  quarto, quinto e sexto ginásio, até 95 no sétimo e oitavo, livre na Liga.
  Golpe de nível não tem limite. A única exceção é o Overheat, que a Nara usa
  em duas criaturas porque é o golpe do tema dela.

## Os golpes exclusivos

Cinco criaturas de chefe levam o golpe exclusivo da espécie:

| chefe | criatura | golpe |
|---|---|---|
| Nara | #016 Boitatá | Fogo-Fátuo Ancestral |
| Clara | #110 Ogum | Forja de Ogum |
| Tibúrcio | #291 Cobra-Norato | Olhar da Cobra Grande |
| Amália | #027 Botogaláu | Encanto do Boto |
| Amália | #048 Boiuna | Abraço da Boiuna |

## O que mudou de espécie

- **Tibúrcio** tinha o lendário #348 Arauanamon na última vaga. Ele agora
  espera ao pé da torre, em `SkyPillar_Outside`, junto dos outros dezenove
  de `docs/arauna/ARAUNA_LEGENDS.csv`. Em seu lugar entra #291 Cobra-Norato.
  Saem também #211 Fóssil (que já está no time da Dalva) e #280 Sucuriaçu
  (no da Celina); entram #297 Corcovado-Ancião e #282 Draguará-Alfa.
- **Rosa** troca #239 Mão-Peluda (que já está no time do Ademar), #054
  Guaraflama e #241 Comadre por #254 Pisadeira, #234 Loirinha e #289
  Anhangaú. A última vaga passa de BST 448 para 603.
- **Nara** tinha quatro criaturas: troca #052 Guaracim (BST 287) por #053
  Guará e ganha #099 Mula-sem-Cabeça.
- **Elias** tinha quatro e ganha #114 Zebu.
- **Cec&Caet** tinham quatro e ganham #164 Coruja e #199 Ametista.
- **Lídia, Celina, Lázaro e Clara** mantêm as espécies; os golpes, itens,
  IVs e níveis são novos.
- **Amália** troca #280 Sucuriaçu e #364 Sarará (que já estão no time da
  Celina) por #246 Guaraci e #294 Uirapuru.

Dois times usam a família pseudo, que o `check_boss_team.py` aponta como
ATENÇÃO: #047 Sucuri na Celina e #048 Boiuna na Amália. As duas já estavam
nesses times antes e continuam.

## Como foi conferido

- `python3 tools/arauna/check_boss_team.py docs/arauna/times/<NOME>.json --cap N`
  sem erro para os dez.
- No mGBA, as treze batalhas foram abertas e o `gEnemyParty` foi lido de
  dentro da batalha: as 52 vagas dos dez times novos chegam com espécie,
  nível, item, IV e os quatro golpes iguais ao JSON.
- A batalha da Nara foi jogada inteira contra o kit de teste de nível 100:
  cinco turnos, insígnia e flag de vitória gravadas. A da Amália também foi
  até o fim: o Guaraci (Fire/Fairy) segurou o mesmo kit — Dragon Claw não
  pega em Fairy — e venceu.

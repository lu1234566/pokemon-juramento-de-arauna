# Como publicar a beta

## O que se publica é o patch, não a ROM

A ROM montada carrega o Pokémon Emerald inteiro dentro dela — as músicas, os
tilesets, os sprites, o motor. Distribuir esse arquivo é distribuir o jogo da
Nintendo com umas alterações, e é assim que uma hack sai do ar.

O que a comunidade publica, e o que este repositório já estava preparado para
publicar, é o **patch**: só a diferença. Cada jogador aplica na cópia legítima
que ele já tem. O `scripts/check_no_proprietary_files.sh` recusa `.gba`,
`.bps`, `.ips`, `.ups` e `.xdelta` no Git desde antes desta nota — a regra não
é nova, só não estava escrita num lugar só.

## Fazendo o patch

```bash
bash scripts/build_arauna.sh en
python3 tools/arauna/make_patch.py SUA_EMERALD.gba \
    --saida juramento-de-arauana-beta.bps
```

A sua cópia é lida e nunca copiada para lugar nenhum. O que sai é a diferença
mais três checksums.

**O gerador se prova antes de escrever.** Ele aplica o patch de volta na
origem e confere byte a byte contra o alvo; se não bater, ele não escreve nada
e sai com erro. Publicar um patch que não aplica é o tipo de erro que só
aparece depois que mil pessoas baixaram.

## Por que BPS e não IPS

O BPS grava o CRC32 da origem, do alvo e do próprio patch. O aplicador
**recusa sozinho** uma ROM base errada, que é o erro número um de quem instala
hack — e diz qual é o problema em vez de gerar um jogo quebrado que trava na
terceira cidade.

O IPS não tem checksum nenhum e o formato nem endereça 16 MB.

## O tamanho do patch

Espere algo entre 11 e 16 MB. Isto é um build *modern* do pokeemerald: o
compilador não é o mesmo da ROM original, então o binário inteiro fica
deslocado em relação a ela, e o patch acaba carregando quase tudo. Não é
defeito, é o preço do build moderno — e é por isso que hacks feitas em
pokeemerald costumam ter patches grandes.

Um `.zip` do `.bps` derruba bastante.

## A ROM que o patch produz

Confira estes números depois de aplicar. Se o seu aplicador mostrar outra
coisa, a base estava errada.

| | |
|---|---|
| arquivo | `pokemon-juramento-de-arauna-en_modern.gba` |
| tamanho | 33 554 432 bytes |
| CRC32 | `CFEBD897` |
| MD5 | `fc49992e9dd0d5aabe9c2f53c90333f0` |
| SHA-1 | `e466b5a65d0be007e0aa9cc8588ee93ff68f4334` |
| SHA-256 | `0cc8a741b0c5af840c45e21d362eccd7577dcead6c52d2af876f15ceb48e4d23` |

Build da continuação de QA em 14/10/2026, GCC ARM 13.2.1.
Detalhes e limites da campanha em `docs/CAMPAIGN_JOURNEY_QA_20261014.md`.
Os testes dirigidos anteriores estão em `docs/REMAINING_RUNTIME_QA_20261014.md`.

Estes valores são desta build. Qualquer commit novo muda os três — regere a
tabela antes de publicar.

## O que dizer no anúncio

Duas coisas que é melhor você dizer antes que alguém reporte:

- **A dex só fecha depois do Hall da Fama.** Vinte lendários e míticos esperam
  no mapa, mas dormem até o primeiro Hall da Fama — antes disso nenhum deles
  aparece, de propósito. Depois, o sensor de VÍNCULO do laboratório da Anahi
  diz onde ainda há sinal. A lista com mapa e nível está em
  `docs/DOSSIE_BETA.md`.

- **Três arcos são rascunho.** Casa do Uivo (depois da segunda insígnia),
  o primeiro vínculo da Primeira Câmara e a Noite de História da Casa da
  Fogueira (depois da sétima) foram escritos a partir da sinopse e podem
  mudar. O Eremita fala por escrito; a cena em Libras ainda não existe.
  Detalhes em `docs/ARCOS_RASCUNHO.md`.

Os treze times de chefe já estão no padrão novo — cinco criaturas com item e
IV escalonado, seis na dupla e na Campeã — e foram lidos de dentro da batalha.
Cada um está em `docs/arauna/times/`.

E outra, que é o motivo de existir uma beta: **ninguém jogou esta versão
do início ao fim.** Os 528 mapas foram varridos e carregam; as batalhas de
chefe foram medidas. Mas a cadeia de flags da história, da Vila do Amanhecer
até a Campeã, nunca foi percorrida inteira por ninguém.

## O manual

`docs/DOSSIE_BETA.md` é o documento para acompanhar o lançamento: a história,
os nomes do mundo, as treze casas, os treze times com moveset completo, o grafo
de mapas, as 35 habilidades, os 27 golpes exclusivos, o elenco, a dex dos 386 e
o que falta. Ele é gerado por `tools/arauna/build_beta_dossier.py --write`, do
próprio repositório, então regere junto com a build.

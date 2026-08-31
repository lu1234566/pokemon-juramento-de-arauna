# Os nomes de Arauna

Cinco passes, na ordem em que devem rodar. Todos aceitam `--check` e `--write`,
e todos decidem o que renomear comparando com a árvore vanilla — rodar duas
vezes não empilha.

| Ferramenta | O que renomeia |
|---|---|
| `tools/arauna/build_trainer_names.py` | os 434 treinadores de rota em `src/data/trainers.h` |
| `tools/arauna/build_facility_names.py` | os 526 do Frontier, das Tendas, do Trainer Hill e dos concursos |
| `tools/arauna/build_apprentice_names.py` | os 16 aprendizes do Battle Tower |
| `tools/arauna/build_place_names.py` | os lugares, no texto, a partir do mapa |
| `tools/arauna/build_character_names.py` | as pessoas, no texto, a partir de `trainers.h` |
| `tools/arauna/build_species_mentions.py` | as criaturas, no texto, a partir da dex |

**Depois de qualquer um dos três últimos, rode `tools/arauna/rewrap_text.py
--write`.** Nome novo é quase sempre nome maior, e uma linha que passa da caixa
de mensagem não dá erro nenhum: ela é simplesmente cortada na tela. O
`tools/arauna/check_text_width.py` é o gate que não deixa isso passar — mede
como o engine mede, a partir de `charmap.txt` e de
`gFontNormalLatinGlyphWidths`, com o teto medido do próprio Emerald: 208px na
caixa de fala, 102px na descrição de item da mochila.

## A parte difícil não é a substituição

Está toda em `tools/arauna/rename.py`, compartilhada pelos três passes de texto.

**Só o que é exibido.** Um `.string` num script, um `_("")` numa tabela, os
literais adjacentes de uma descrição sob `src/data/text`, e os bancos JSON em
`data/text/arauna/en` — que é onde mora o texto inglês que um renderer escreve,
e que os dois primeiros passes esqueceram até serem corrigidos. Nomes de
símbolo sobrevivem porque são maiúsculas-e-minúsculas (`SlateportCity_Text_…`)
ou colados por sublinhado (`MAPSEC_SLATEPORT_CITY`), e a fronteira de palavra
recusa os dois.

**Os renderers ingleses andam junto.** Um renderer acha o bloco que reescreve
procurando uma frase no texto base, então um nome renomeado tem de ser
renomeado nas âncoras dele também — senão o renderer procura algo que não
existe mais. Mas **não** nas listas de tokens que ele afirma terem sumido: ali
`"MT. CHIMNEY"` quer dizer "o nome de Hoenn tem de ter ido embora", e virar
`"SERRA DA CINZA"` proibiria justamente o nome que o renderer escreve. O mesmo
arquivo usa `"MT. CHIMNEY"` nos dois papéis, então o texto não decide isso — a
árvore sintática do próprio Python decide, e a diferença entre as duas é uma
palavra: um laço de resíduo estoura quando o token **está** lá, um laço de
âncora estoura quando a frase **não está**.

## O que ainda é de Hoenn, e por quê

**81 menções a espécies, todas em bonecos.** São 35 decorações de boneco, as
lojas que os vendem e o minigame do Dodrio, e a arte de todos eles continua
sendo o Pokémon do Emerald: o boneco na prateleira é um Pikachu. Trocar o
rótulo por uma criatura de Arauna pioraria a incoerência em vez de resolvê-la,
porque o boneco está à vista. Essa espera arte, não tabela.

**36 menções a pessoas que o projeto nunca batizou:** RYDEL, SCOTT,
CAPT. STERN, MR. BRINEY, PEEKO, MR. STONE, LANETTE, PROF. COZMO, WINSTRATE,
BILL — mais os quatro trocadores de decoração e o juiz de tamanho em
`src/strings.c` (`gText_Tristan`, `gText_Philip`, `gText_Dennis`,
`gText_Roberto`, `gText_Marco`). Escolher um nome é decisão de história; a
lista está em `ARAUNA_CHARACTER_NAMES.csv` com a coluna vazia.

**BATTLE FRONTIER e TRAINER HILL.** O Frontier já é BATTLE CIRCUIT nos
renderers ingleses, então mover o nome pertence a eles e não a este passe.

**GRUNT.** Virou AGENTE numa facção e ATIVISTA na outra, e qual das duas uma
fala quer depende de quem está falando. Isso é leitura, não tabela.

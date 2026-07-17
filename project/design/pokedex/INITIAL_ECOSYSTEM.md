# Primeiros registros visíveis da Pokédex externa

**Estado:** alinhamento com o spoiler da Dex de Arauna  
**Escopo:** slots #001–020 visíveis na captura recebida  
**Arte:** nenhuma imagem da captura está aprovada ou integrada pelo repositório

O catálogo externo substitui as propostas provisórias que ocupavam #010–018 no
primeiro rascunho. O repositório registra agora apenas o que pode ser lido com
segurança na captura: número, nome e tipos. Famílias, biomas, habilidades, stats,
evoluções e fichas completas aguardam importação estruturada.

## Trio inicial

| Slots | Linha | Tipagem conhecida | Placeholder de desenvolvimento |
|---|---|---|---|
| #001–003 | Caramelo → Caramelão → Dragauará | Fire → Fire → Fire/Dragon | Torchic → Combusken → Blaziken |
| #004–006 | Querô → Queribela → Terólibra | Water → Water/Bug → Water/Bug | Mudkip → Marshtomp → Swampert |
| #007–009 | Pimpau → Bicopau → Petronico | Grass → Grass → Grass/Rock | Treecko → Grovyle → Sceptile |

Os placeholders preservam tipagem e progressão aproximadas para teste. O número
de Arauna não precisa coincidir com o número nacional do Pokémon temporário.

## Outros registros visíveis

| Slot | Nome | Tipos mostrados |
|---:|---|---|
| #010 | Formilim | Bug |
| #011 | Saúvarco | Bug/Ground |
| #012 | Capivim | Water/Normal |
| #013 | Tucanhão | Flying/Grass |
| #014 | Sagüim | Normal |
| #015 | Micuías | Normal/Psychic |
| #016 | Boitatá | Fire/Ghost |
| #017 | Curupim | Grass/Fairy |
| #018 | Curupira | Grass/Fairy |
| #019 | Iaraço | Water/Fairy |
| #020 | Sacizinho | Dark/Flying |

Essas onze entradas permanecem como `external-preview`: o spoiler confirma que
existem no catálogo, mas não fornece dados suficientes para inferir famílias ou
mecânicas. Nenhuma delas recebe placeholder estável antes da ficha estruturada.

## Uso imediato em batalhas

Poochyena, Voltorb e outros Pokémon oficiais podem continuar aparecendo nas
batalhas do protótipo. Eles ficam declarados em `battle_placeholders.csv` e serão
substituídos por slots de Arauna quando a distribuição completa estiver
disponível.

## Próximo passo de dados

Importar um arquivo JSON ou CSV exportado da Dex externa com os 386 registros.
Esse arquivo deve conter, quando disponível: número, nome, família, estágio,
tipos, inspiração, bioma, descrição e estado da arte. A importação estruturada é
preferível a transcrever centenas de cartões por capturas de tela.

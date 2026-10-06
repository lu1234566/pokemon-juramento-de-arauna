# Mata da Espera V1 e borda Rota 119–118

Base: `b3fceb65b071b468e21075f11fa311c8a381e910`, branch
`claude/pokemon-juramento-arauna-fhk6ah`.

Esta rodada adapta o visual da Mata da Espera e fecha os quatro grupos de
cache pendentes no tileset compartilhado por Fortree e pelas rotas 119/120.

## Mata da Espera

A direção vem da página 25 do Master Map Design Bible: Mata Atlântica
fechada, trilhas curvas, raízes e clareira narrativa. O novo chão delineia
a trilha com contornos em pixels; árvores de raízes largas, troncos caídos
e samambaias acrescentam marcos. A vegetação e as paletas da Rota 104
fazem a transição entre rota e dungeon.

É uma primeira adaptação visual sobre a geometria existente, de 48×44.
Os seis acessos, dois gatilhos, treze objetos e cinco eventos de fundo
ficam nas posições atuais. A proposta de 34×28 da Bíblia foi subordinada
a esse inventário, conforme a regra de preservar eventos e progressão.

- 199 células recebem novo desenho; as 2.112 conservam colisão, elevação e
  atributos de comportamento idênticos aos da base.
- As árvores maiores, troncos e samambaias ocupam vegetação já bloqueada.
  As raízes nas trilhas continuam transitáveis.
- A grama mantém seus IDs nativos e o comportamento de encontro em todas
  as suas posições. Isso preserva também Cut, que seleciona a troca de
  grama por ID fixo. O novo chão é aplicado às áreas livres.
  A tabela de encontros, clima, música, flags, objetos e scripts permanecem
  iguais; no `map.json`, só muda o layout.
- Banco secundário próprio: 229 tiles novos e 434/512 metatiles. Usa
  paletas 9 e 10; nenhum metatile usa paletas 13–15 ou slots de portas.
- O fundo sob a arte transparente é opaco, evitando os vãos pretos
  encontrados nos pisos do lote anterior.

## Borda com o tileset de Fortree

A conexão é a Rota 118 vista ao sul da **Rota 119**, que compartilha o
tileset de Fortree; não há conexão direta de Fortree com a Rota 118.

A compactação reaproveita oito tiles estáticos duplicados, incluindo
versões espelhadas, sem mudar nenhuma camada dos 392 metatiles existentes.
O callback desse banco não anima o secundário. Referências vindas dos
primários são protegidas pelo compactador.

Quatro grupos, abrangendo 22 células que referiam metatiles indefinidos
no banco receptor, passam a ter definições corretas no cache. O ajuste de IDs cobre 24 células,
incluindo duas cópias de compatibilidade. O banco da Rota 123 recebe as
definições compartilhadas necessárias para a outra vista de três células.

Os cinco layouts que usam os bancos alterados permanecem idênticos em
RGB, colisão, elevação e comportamento. Na faixa completa, nenhuma célula
aumentou seu indicador de erro; o agregado caiu de 8.194,54 para 2.897,96.
Esse indicador soma diferenças médias RGB por célula e atribui penalidade
255 a IDs indefinidos; não mede uma captura da ROM anterior. Os renders
diagnósticos mostram esses IDs em preto. As definições válidas mantêm os
tons próprios de cada bioma, sem exigir identidade de paletas entre mapas.

O corretor agora inclui suas dependências no repositório, aceita filtro
por receptor e reconhece o remapeamento de índices de cor. Um segundo
dry run nesse receptor não propõe alterações. O dry run na base detecta
os quatro grupos e esbarra na falta de slots em três deles.

## Validação

- Build ARM local: `bash scripts/build_arauna.sh en -j6`, aprovado.
- Três gates do build: English-only, cobertura narrativa e largura de texto,
  aprovados; 37.537 strings visíveis verificadas.
- Auditoria de dados de mapas: oito verificações aprovadas, sem erros.
  A leitura dos limites de metatiles também foi corrigida para consultar
  `metatiles.h`, onde estão os registros nativos.
- Validador da mata: comportamento de todas as células, seis pares de
  warps e alcance antes/depois de Cut aprovados. Acessibilidade comparada
  em três entradas: 501 células antes de Cut, 660 depois, como na base.
- mGBA: seis saídas **e seis retornos** atravessados, com mapa e índice de
  warp conferidos em RAM; os dois gatilhos iniciam o diálogo do pesquisador.
- mGBA: aproximação e travessia Rota 119 → Rota 118 conferidas na base e
  na versão final, além dos três pontos acessíveis da mata nas imagens.
- Reprodução do construtor: 21 arquivos de assets/layout repetidos com
  hashes idênticos.

As capturas usam inicialização de teste temporária em memória para chegar
aos mapas. Os ajustes de entrada foram restaurados antes de enviar os
comandos de movimento. A ROM final vem das fontes normais; nenhuma ROM,
save ou modificação de entrada de depuração integra o pacote.

O combate completo do pesquisador e uma campanha integral não foram
reexecutados. Scripts e todos os dados de movimento/terreno que essa cena
recebe permaneceram iguais. As imagens da faixa de cache são identificadas
como renders estáticos; as demais capturas são do emulador.

## Correção do panorama anterior

Ever Grande já tem o exterior V2 com fachada de pedra e vidro, brasão,
escadarias e cachoeiras. O símbolo legado `gTileset_EverGrande` causou a
classificação incorreta como Hoenn original. Essa implementação foi
preservada. Uma nova porcentagem global exige auditar o conteúdo dos
bancos, não apenas os seus nomes.

## Reprodução

```sh
python3 tools/arauna_maps/build_mata_espera_v1.py
bash scripts/build_arauna.sh en -j6
python3 tools/arauna_maps/validate_mata_espera_v1.py
python3 tools/arauna/audit_map_data.py
```

O construtor requer Pillow, NumPy e SciPy. Os assets finais já estão no
pacote e o build não depende dessas bibliotecas. Não houve GitHub Actions.
O build gera os headers de mapas que a auditoria usa em uma cópia limpa.
As evidências ficam em `review/mata_espera_v1_*` e `review/bordas_fortree_*`.

## Verificação na instalação

- Aplicado sem conflito sobre `b3fceb65b0`; `make MODERN=1` ok.
- `check_arauna_static.sh` 189/189, `check_overworld_palette_capacity.py`
  95/95, `audit_visible_residue.py` 0 candidatos, `audit_map_data.py` com
  as oito verificações aprovadas.
- `build_mata_espera_v1.py` rodado de novo reproduz byte a byte os arquivos
  do pacote; `validate_mata_espera_v1.py` aprovado.
- Os cinco layouts dos bancos alterados renderizam idênticos à base. A
  Rota 118 muda 24 IDs no `map.bin`, sem mudar colisão nem elevação.
- Bordas por cor, rede inteira: só duas conexões mudam, as duas para
  melhor (Rota 119 ← 118: 109 → 87 células erradas; Rota 123 ← 118:
  3 → 0). Nenhuma piora.
- Animações gerais, comportamentos de metatile da rede inteira e os
  metatiles de Cut: sem diferença.
- Emulador: seis pontos da mata e a travessia Rota 119 → Rota 118 a pé,
  da linha 132 até (58, 0) da Rota 118.

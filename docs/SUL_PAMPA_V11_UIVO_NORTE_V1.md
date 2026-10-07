# Sul/Pampa V1.1 + Uivo Norte V1

Base exata: `59f4c6eea2a7aa033bb10ca4e6074a0a2ec3883c`, branch `claude/pokemon-juramento-arauna-fhk6ah`. Pacote incremental com patch Git binário, arquivos nativos, construtor, validadores e evidências. A variante sem Mirage Tower da Rota 111 já instalada nessa base foi preservada.

## O que foi entregue

- **Rota 102:** as 104 células bloqueadas que usavam o desenho de grama de encontro passam a ter moitas densas. A grama transitável de encontro conserva seu desenho e função.
- **Rota 103:** a mesma correção em 588 células bloqueadas, com moitas distintas do capim onde se pode andar.
- **Rota 104:** 688 células antes desenhadas como arbusto seco passam a compor uma copa contínua de mata fechada, incluindo os dois acessos da Mata da Espera. Objetos de raízes que usam outros metatiles continuam sendo objetos separados.
- **Rustboro / Serra do Uivo:** fachadas novas de pedra, madeira e telha cerâmica, ginásio, escola e grêmio de pesquisa; ruas de pedra, escadas e patamares com faces de basalto. 2.325 células redesenhadas.
- **Rota 115:** vegetação costeira, moitas, araucárias, piso e escarpas de basalto, com a entrada de Meteor Falls e os dois pontos temporários da Terra Cave funcionais. 2.606 células redesenhadas.
- **Rota 116:** caminho de terra de mineração, casa dos trabalhadores, entradas de túnel, pedra e araucárias; dois pontos temporários da Terra Cave funcionais. 1.949 células redesenhadas.

As dimensões são 50×20, 80×22 e 40×80 nas Rotas 102–104; 40×60 em Rustboro, 40×80 na Rota 115 e 100×20 na Rota 116. **Nenhuma célula mudou colisão, elevação ou comportamento nativo.** A geometria transitável permaneceu igual à base. Eventos, warps, encontros, climas, flags e scripts de história foram preservados. Os objetos novos têm desenho na camada superior e piso opaco embaixo.

Somente os três mapas redesenhados ganham IDs de layout novos, acrescentados ao fim do registro. Os três mapas da V1.1 mantêm seus IDs de layout. A migração de saves usa o C real do motor, reconhece os layouts anteriores e mantém as coordenadas, pois a área de passagem não mudou. A prioridade do continue-game warp original é preservada.

## Fontes e bancos nativos

Atlas de desenhos novos fixo em `art/uivo_norte_v1/source_atlas.png`, acompanhado do prompt, regiões de recorte e plano de paletas. A conversão é determinística; reproduzir o pacote não depende de gerar novamente a imagem. Fachadas maiores são montadas por repetição de tiles 8×8 inteiros, mantendo os detalhes de pedra e madeira.

São 12 bancos intermediários de arte e 48 bancos ativos privados de borda (24 primários e 24 secundários). Os intermediários ficam fora das declarações carregadas pela ROM e servem à construção e à auditoria. Cada banco contém `tiles.png` indexado, `palettes/*.pal` JASC-PAL em CRLF, `metatiles.bin` e `metatile_attributes.bin`.

Só são usadas paletas **0–12**, pixels 0–15 e 16 cores por linha. Os slots gráficos 432–511 e 992–1023 e as demais faixas ocupadas pelos callbacks específicos ficam reservados para animações. Água e seus callbacks foram mantidos, e a comparação das bordas inclui oito quadros animados.

Os IDs reservados incluem grades próprias, cache de borda, grades dos vizinhos, metatiles de Cut, famílias produzidas pelo motor e dependências transitivas dos scripts compartilhados. Isso inclui os metatiles que o script da Terra Cave desenha nas Rotas 115 e 116. Os resultados de scripts conservam desenho e atributos da base.

## Bordas com aliases do V2

O mecanismo existente em `src/arauna_border_visuals.c` recebe tabelas específicas deste lote; os seletores anteriores continuam disponíveis para layouts alternativos. As grades de colisão da faixa do vizinho permanecem intactas. Os aliases recompõem a cor do vizinho sem substituí-la pela cor do receptor.

Foram recompostas **40 direções / 20 pares**, incluindo as ligações anteriores afetadas pela troca dos bancos. As três ligações acrescentadas são Rustboro↔Rota 116, Rota 115↔114 e Rota 116↔Verdanturf. Todas as 40 direções terminam com zero diferenças de desenho. As outras **94 direções auditadas não mudam**. Os 18 mapas recompostos fora dos seis alvos mantêm seu desenho próprio igual em RGB555.

Contagem por célula da faixa inteira do vizinho, na precisão RGB555 do GBA e com o seletor C e a cópia de conexões reais:

| Receptor ← vizinho | Antes | Depois |
| --- | ---: | ---: |
| Rota 111 ← Mauville | 0 | 0 |
| Lavaridge ← Rota 112 | 0 | 0 |
| Rota 116 ← Verdanturf | 167 | 0 |
| Rota 116 ← Rustboro | 140 | 0 |
| Rota 110 ← Mauville | 0 | 0 |
| Rota 110 ← Slateport | 0 | 0 |
| Rota 110 ← Rota 103 | 0 | 0 |
| Rota 118 ← Rota 119 | 0 | 0 |
| Rota 118 ← Mauville | 0 | 0 |
| Rota 117 ← Mauville | 0 | 0 |
| Rota 102 ← Petalburg | 0 | 0 |
| Rota 102 ← Oldale | 0 | 0 |
| Petalburg ← Rota 104 | 0 | 0 |
| Petalburg ← Rota 102 | 0 | 0 |
| Rota 105 ← Rota 104 | 0 | 0 |
| Ever Grande ← Rota 128 | 0 | 0 |
| Rota 126 ← Rota 124 | 0 | 0 |
| Verdanturf ← Rota 116 | 189 | 0 |
| Mauville ← Rota 111 | 0 | 0 |
| Mauville ← Rota 110 | 0 | 0 |
| Mauville ← Rota 117 | 0 | 0 |
| Mauville ← Rota 118 | 0 | 0 |
| Rota 103 ← Oldale | 0 | 0 |
| Rota 103 ← Rota 110 | 0 | 0 |
| Rota 128 ← Ever Grande | 0 | 0 |
| Rota 114 ← Rota 115 | 315 | 0 |
| Slateport ← Rota 110 | 0 | 0 |
| Rustboro ← Rota 115 | 0 | 0 |
| Rustboro ← Rota 104 | 0 | 0 |
| Rustboro ← Rota 116 | 159 | 0 |
| Rota 112 ← Lavaridge | 0 | 0 |
| Rota 124 ← Rota 126 | 0 | 0 |
| Rota 104 ← Rustboro | 0 | 0 |
| Rota 104 ← Rota 105 | 0 | 0 |
| Rota 104 ← Petalburg | 0 | 0 |
| Rota 115 ← Rustboro | 0 | 0 |
| Rota 115 ← Rota 114 | 361 | 0 |
| Rota 119 ← Rota 118 | 0 | 0 |
| Oldale ← Rota 103 | 0 | 0 |
| Oldale ← Rota 102 | 0 | 0 |

As conexões Rota 115↔114 e Rota 116↔Verdanturf não têm passagem atravessável nas grades nativas da base. Seus aliases foram verificados, mas não foram criadas travessias novas nem fotos apresentadas como prova de travessia nesses quatro sentidos.

## Desenho novo: medida de originalidade

Comparação exata da estrutura de classes de cor e transparência dos tiles 8×8, também espelhados, contra 38.800 gráficos armazenados no Emerald original. A tabela mede somente os tiles de arte nova; água, portas e ledges funcionais e desenhos importados dos vizinhos ficam fora da medida. Tiles simples podem coincidir por acaso. Esta medida não avalia identidade cultural percebida nem o percentual de pixels de toda a tela.

| Mapa | Tiles de arte nova não vazios | Iguais ao original | Percentual igual |
| --- | ---: | ---: | ---: |
| Rota 102 | 11 | 1 | 9.09% |
| Rota 103 | 11 | 1 | 9.09% |
| Rota 104 | 7 | 1 | 14.29% |
| Rustboro | 478 | 10 | 2.09% |
| Rota 115 | 68 | 7 | 10.29% |
| Rota 116 | 224 | 8 | 3.57% |

## Verificação e capturas

- Build inglês moderno aprovado com GCC ARM 13.2.1. Gates: 189/189 checks do protagonista, 95/95 de capacidade de paletas; auditoria de resíduos com zero candidatos críticos/globais. Auditoria oficial de mapas: oito verificações aprovadas.
- 1.003 arquivos de mapas, scripts e animações protegidos; 717 registros de layout preexistentes fora dos registros principais recompostos preservados; três novos IDs acrescentados. Os 717 registros incluem layouts sem uso e não representam 717 mapas ativos.
- 67.796 atributos de células nativas comparados; colisão, elevação, eventos, warps e alcance aprovados. Na V1.1, todos os pixels fora das células indicadas permanecem iguais à base.
- Bordas: 84.384 comparações de células em oito quadros e 73.728 verificações de fallback do seletor C. Zero diferenças nas 40 direções tratadas e zero regressões nas outras 94.
- Migração: 2.984 posições antigas executadas com o C real no host; zero posições realocadas. As mesmas 2.984 posições nos layouts atuais não remigram. Nove IDs de Cut verificados no C real. **Não foi testado um arquivo de save antigo real no emulador.**
- Reprodução a partir de uma worktree limpa da base: 979 arquivos gerados iguais byte a byte, usando apenas ferramentas e entradas de arte/plano fixas.
- ROM compilada: 48 bancos, 40 tabelas de aliases e 13 linhas de paleta conferidos contra as fontes. Nenhum símbolo de harness na ROM final. SHA-256: `1b7bace62390a0fcd7e44e946b57cb6ed9492c264aa962f845def9c321912f90`. Arquivo de ROM de 33554432 bytes; não distribuído.
- **mGBA 0.10.2: 62 execuções nativas e fotos, 31 antes e 31 depois.** Portas e conexões foram usadas para recarregar os mapas antes de fotografar. Foram testadas as duas entradas da Mata da Espera, portas do Centro e dos trabalhadores, entrada de Meteor Falls, quatro entradas temporárias da Terra Cave e 16 direções de borda atravessáveis, com ida, retorno e nova travessia. Grupo/mapa e coordenadas foram conferidos. A variante sem Mirage Tower foi confirmada pelo ID 712 no motor, antes e depois. Zero opcodes ilegais.

As capturas executam o código GBA da ROM em libmgba. A posição inicial, equipe e estados de teste são preparados temporariamente na memória do emulador; a ROM em disco conserva seu hash. As fotos são quadros reais 240×160; oito pranchas foram ampliadas com nearest-neighbor. Não há render estático ou imagem de conceito apresentado como captura do emulador. Os estados da Terra Cave e da Mirage Tower constam dos recibos.

Evidências: `review/uivo_norte_v1/`, com JSONs, logs, 62 fotos e oito pranchas. ROM, ELF, saves, estados e o harness privado de captura não fazem parte do ZIP.

## Construção reproduzível

Pré-requisitos: Git, Python 3.10+, Pillow e compilador C do host. Para build e checagem da ROM, toolchain ARM suportada pelo projeto e seus utilitários. Executar a partir do checkout com o pacote aplicado:

```sh
git worktree add --detach ../arauna-base 59f4c6eea2a7aa033bb10ca4e6074a0a2ec3883c
python tools/arauna_maps/build_uivo_norte_v1.py --base ../arauna-base
python tools/arauna_maps/validate_uivo_norte_v1.py --base ../arauna-base
python tools/arauna_maps/validate_uivo_migration_v1.py --base ../arauna-base
bash scripts/check_arauna_static.sh
python tools/arauna/audit_map_data.py
bash scripts/build_arauna.sh en -j6
python tools/arauna_maps/verify_uivo_rom_v1.py --rom pokemon-juramento-de-arauna-en_modern.gba --elf pokemon-juramento-de-arauna-en_modern.elf
```

A auditoria opcional de originalidade usa uma cópia do commit `ad0fd4d17f546ca6fd8d785c8724f9382e6e9382` e `python tools/arauna_maps/audit_uivo_originality_v1.py --original ../emerald-original`.

O instalador do ZIP verifica a base, os SHA-256 e a árvore Git final, aplica o patch incremental e mantém paletas CRLF. As alterações ficam staged para revisão. Não faz commit nem push no repositório de destino. Uma segunda execução, com os arquivos já instalados, é uma operação sem mudanças.

## Verificação na instalação

- O instalador foi aplicado sobre `59f4c6eea2` e chegou à árvore revisada.
  `validate_uivo_norte_v1.py` e `validate_uivo_migration_v1.py` aprovaram
  numa worktree limpa.
- Build `en` ok (ROM em 56,7%). Gates aprovados: 189/189, 95/95, 0
  candidatos de resíduo, as oito verificações de mapas e
  `verify_uivo_rom_v1.py`. Nenhum símbolo de harness na ROM.
- Correção 1, variante sem Mirage Tower da Rota 111:
  - `LAYOUT_ARAUNA_ROUTE111_THREE_ACTS_NO_TOWER_V1` tinha ficado nos
    bancos Sul, enquanto a Rota 111 base passou para os bancos Uivo.
  - A variante foi regenerada com `variantes_troca_layout.py`, que volta a
    dar 9/9. O render em RGB555 e os atributos são idênticos.
  - Com isso, a asserção de `validate_uivo_norte_v1.py` que exige esse
    registro inalterado deixa de valer. Todo o resto do validador continua
    aprovado (716 layouts preservados mais a variante, 40 direções, 0
    erros).
- Correção 2, borda fora do mapa de Rustboro e da Rota 116:
  - O `border.bin` copiado dos layouts anteriores apontava para os IDs
    `0x1D4/0x1D5/0x1DC/0x1DD`, árvores do banco General, que nos bancos Uivo
    estão vazios. Fora do mapa aparecia preto.
  - A borda agora usa o padrão 2×2 de árvore que o próprio mapa repete sem
    emenda: `2E0 2E1 / 32E 32F` em Rustboro e as araucárias
    `2D0 2D1 / 2E4 2E5` na Rota 116.
  - Nos outros 23 layouts com bancos trocados, a borda continua idêntica
    em RGB555.
- Render próprio: os 22 layouts com bancos trocados ficam idênticos em
  RGB555. Só mudam as células anunciadas: 104 na Rota 102, 588 na Rota 103
  e 688 na Rota 104. Nos três mapas novos, colisão, elevação, comportamento
  e camada são iguais célula a célula aos layouts anteriores.
- Terra Cave: as quatro entradas temporárias e a limpeza das Rotas 115 e
  116 mantêm o comportamento da base. A entrada aparece como boca de
  caverna. A parede da limpeza é a do banco novo.
- Emulador:
  - 45 de 45 travessias a pé chegam com VRAM e paletas iguais ao
    carregamento direto, incluindo Rustboro↔104/115/116 e as chegadas à
    Rota 111 vindas das Rotas 112 e 113 (variante sem torre).
  - Petalburg não pode ser carregada diretamente pelo harness. As duas
    chegadas a pé (das Rotas 102 e 104) diferem dessa referência
    exatamente nos mesmos tiles e cores, como no Sul V1.
- Pendência de legibilidade:
  - Na Rota 103 ainda há 111 células bloqueadas com o mesmo desenho de chão
    andável. A maior parte está na faixa leste de terra com tufos (x 59–74,
    y 15–18) e nas ilhotas de juncos do rio.
  - Na Rota 102 há 10 células, que são troncos de árvore.

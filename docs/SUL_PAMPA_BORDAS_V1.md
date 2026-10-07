# Sul/Pampa V1 — Rotas 102, 103, 104 e Petalburg; bordas prioritárias

Base exata: `591aeb24973622bda8d12cce60b3560cef938c00`, da branch `claude/pokemon-juramento-arauna-fhk6ah`. Entrega incremental; aplicação não altera o histórico anterior. Pacote contém fontes, patch Git binário e evidências. ROM, ELF, saves, estados e harness privado de captura ficam fora da entrega.

## Resultado visual e escopo

Arte nova de araucárias, campos de capim, cercas, cultivo, fachadas de telhado cerâmico, floricultura, casa do Briney, praça e fonte. A referência fixa é `art/sul_pampa_v1/source_atlas.png`; prompt e retângulos de recorte estão junto dela. A conversão para os bancos nativos é determinística e não depende de repetir a geração da imagem.

Rotas 102 (50×20), 103 (80×22), 104 (40×80) e Petalburg (38×30) conservam dimensões, eventos, warps e cenas. Os caminhos de terra e as composições de fachadas são novos. A geometria transitável muda em oito células de cerca na Rota 102: (11–15,3) e (26–28,15). Não se trata de uma alteração completa da geografia dos quatro mapas. As demais colisões e todas as elevações e propriedades nativas foram preservadas. No total foram redesenhadas 953, 1.318, 2.139 e 1.090 células, respectivamente.

Objetos novos usam a camada de cima com quatro tiles opacos de grama/piso embaixo. Água, animações, portas, ledges, metatiles de scripts e famílias de metatiles produzidos pelo motor permanecem funcionais. O Cut reconhece os seis IDs de capim novos e usa o piso correspondente.

## Bordas

Usa o seletor existente em `src/arauna_border_visuals.c`, sem mudar a grade de colisão da faixa do vizinho. São 21 pares de bancos privados (42 bancos ativos) e 34 direções: as 14 direções pedidas, as correções anteriores da V2, a ligação 119/118 e outras conexões afetadas pelos quatro mapas novos. IDs reservados incluem grades próprias, grades dos vizinhos, scripts, Cut e metatiles produzidos pelo motor.

Erros de desenho medidos em células da faixa completa, usando o C real do seletor e as funções reais de cópia das conexões. Comparação na precisão RGB555 do GBA, incluindo oito quadros da animação da água.

| Direção | Antes | Depois |
| --- | ---: | ---: |
| Rota 111 ← Mauville | 340 | 0 |
| Lavaridge ← Rota 112 | 215 | 0 |
| Rota 118 ← Mauville | 211 | 0 |
| Rota 117 ← Mauville | 247 | 0 |
| Petalburg ← Rota 104 | 258 | 0 |
| Mauville ← Rota 111 | 193 | 0 |
| Mauville ← Rota 117 | 135 | 0 |
| Mauville ← Rota 118 | 129 | 0 |
| Rustboro ← Rota 115 | 197 | 0 |
| Rustboro ← Rota 104 | 263 | 0 |
| Rota 112 ← Lavaridge | 93 | 0 |
| Rota 104 ← Rustboro | 280 | 0 |
| Rota 104 ← Petalburg | 221 | 0 |
| Rota 115 ← Rustboro | 207 | 0 |

As 14 direções pedidas somavam 2989 células diferentes; agora somam zero. As 34 direções tratadas somam zero erros. As outras 100 direções auditadas não mudaram. Os outros 17 mapas com bancos recompostos mantêm seu desenho próprio igual, em RGB555, em todas as células.

As paletas foram recompostas para acomodar cores dos vizinhos sem recolori-los com a paleta do receptor. O plano exato de Mauville é um arquivo de entrada fixo, verificado pelo construtor; executar o construtor não exige solver. Só há linhas 0–12. PNGs indexados com valores de pixel 0–15 e paletas JASC-PAL em CRLF. Slots 432–511 e 992–1023, mais slots específicos dos callbacks, ficam reservados para animação.

## Originalidade

Comparação de igualdade exata da estrutura de classes de cor e transparência de tiles 8×8 contra todos os bancos originais, também espelhados. Mede somente a arte nova; água, portas, ledges funcionais e arte importada dos vizinhos são excluídos. Igualdade de um tile simples pode ocorrer por coincidência. Este número não mede identidade cultural percebida.

| Mapa | Tiles novos não vazios | Iguais ao original | Percentual igual |
| --- | ---: | ---: | ---: |
| Rota 102 | 109 | 1 | 0.92% |
| Rota 103 | 68 | 2 | 2.94% |
| Rota 104 | 325 | 5 | 1.54% |
| Petalburg | 616 | 13 | 2.11% |

## Verificação

- Build inglês moderno aprovado; prontidão estática aprovada, incluindo 189/189 checks do protagonista e 95/95 de capacidade de paleta; auditoria oficial de resíduos sem candidatos críticos/globais.
- Auditoria de mapas: oito verificações aprovadas; 1.005 arquivos de mapas/scripts/animações protegidos e 61.876 atributos de células comparados.
- Bordas: 72.872 comparações de células com animação em oito quadros, 64.512 verificações de fallback do seletor C, zero regressões nas conexões fora do lote.
- Migração: C real executado no host em 3.905 posições antigas; oito posições de cerca realocadas; 3.905 posições dos layouts atuais não remigradas. Prioridade do continue-game warp original preservada. Não foi usado save antigo real no emulador.
- Reprodução: 822 arquivos de dados e C gerados iguais byte a byte a partir de uma cópia limpa da base e das entradas fixas.
- ROM compilada: 42 bancos e 34 tabelas de aliases conferidos contra os arquivos nativos, 13 linhas de paleta e nenhum símbolo do harness. SHA-256: `8b0a40bc260720ee94b11b68276cf2770d498c07a72bbce61e3439ddc7143d04`. Arquivo de ROM de 33554432 bytes; não incluído no ZIP.
- mGBA 0.10.2: 42 execuções nativas, 21 fotos antes e 21 depois. Fotos dos mapas após entrada/saída natural por porta ou conexão. Cada uma das 14 direções de borda foi cruzada, retornada, fotografada e cruzada novamente; grupo/mapa e coordenadas conferidos. Surf ativo e alteração da VRAM da água confirmados nas duas ROMs. Zero opcodes ilegais. ROM em disco permaneceu intacta; o ponto de partida das capturas foi preparado temporariamente na memória do emulador.

Evidências em `review/sul_pampa_v1/`: JSONs de validação, recibos e logs do mGBA, fotos 240×160 originais e cinco pranchas ampliadas por nearest-neighbor. As pranchas não usam renders estáticos nem imagens geradas como prova de emulação.

## Reprodução das fontes e validadores

Pré-requisitos: Git, Python 3.10+, Pillow, compilador C do host; para build/validação da ROM, toolchain ARM suportada pelo projeto (build verificado com GCC 13.2.1) e utilitários do projeto.

A partir do checkout com o pacote aplicado:

```sh
git worktree add --detach ../arauna-base 591aeb24973622bda8d12cce60b3560cef938c00
python tools/arauna_maps/build_sul_pampa_v1.py --base ../arauna-base
python tools/arauna_maps/validate_sul_pampa_v1.py --base ../arauna-base
python tools/arauna_maps/validate_sul_migration_v1.py --base ../arauna-base
bash scripts/check_arauna_static.sh
python tools/arauna/audit_map_data.py
bash scripts/build_arauna.sh en -j6
python tools/arauna_maps/verify_sul_rom_v1.py --rom pokemon-juramento-de-arauna-en_modern.gba --elf pokemon-juramento-de-arauna-en_modern.elf
```

A auditoria opcional de originalidade usa uma worktree do commit `ad0fd4d17f546ca6fd8d785c8724f9382e6e9382` e `python tools/arauna_maps/audit_sul_originality_v1.py --original ../emerald-original`.

Os oito bancos intermediários `arauna_sul_*` são saída reproduzível da etapa de arte e servem à auditoria; não estão declarados como bancos carregados na ROM. Os 42 bancos ativos são `arauna_border_*_sul_v1`. Nenhuma implementação das Grutas V2 ou dos Interiores V1.1 é revertida.

## Verificação na instalação

- Aplicado sem conflito sobre `591aeb2497`; `make MODERN=1` ok; 189/189,
  95/95, 0 candidatos de resíduo e as oito verificações de mapas aprovadas.
- `validate_sul_pampa_v1.py` e `validate_sul_migration_v1.py` aprovados em
  worktree limpa.
- `validate_border_visuals_119_118.py` ficou obsoleto. Ele simula a tabela
  de aliases da V1, presa aos bancos `AraunaRoute119BorderV1/118BorderV1`,
  que deixaram de ser usados. A faixa 119/118 agora é coberta pelo
  validador desta entrega e foi conferida no mGBA: nas linhas em que as
  vistas da Rota 119 e da Rota 118 se sobrepõem, há 0 pixels diferentes.
- Correção na instalação: `LAYOUT_ARAUNA_ROUTE111_THREE_ACTS_NO_TOWER_V1`
  (Mirage Tower oculta, o estado mais comum) continuava nos bancos
  antigos, então a borda Rota 111 ← Mauville não seria corrigida na maior
  parte do tempo. A variante foi regenerada com
  `variantes_troca_layout.py` nos bancos novos; o render em RGB555 e os
  atributos são idênticos.
- Os 17 mapas com bancos recompostos, mais a variante da Rota 111, têm render
  próprio em RGB555, atributos e callbacks idênticos aos anteriores,
  inclusive nos IDs usados por scripts.
- Emulador:
  - 45 travessias a pé chegam com VRAM e paletas iguais ao carregamento
    direto.
  - Petalburg (que o harness não carrega diretamente) foi conferida pela
    chegada a pé: as cenas de Bento e do ginásio, e as portas do Centro e
    da loja.
- Pendência de legibilidade: na Rota 103, 588 células bloqueadas têm o
  mesmo desenho do capim de encontro; na Rota 102, 104. O capim decorativo
  bloqueado precisa de outro desenho (moita, cerca, árvore). Na Rota 104, a
  mata fechada em volta das entradas da Mata da Espera virou arbusto seco
  de pampa.

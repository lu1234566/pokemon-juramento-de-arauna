# Vila Amanhecer V9 — vila e interiores

Entrega local sobre `bf387be` (Primeira Câmara V1), com 91 arquivos de integração. Os IDs existentes, recompensas, diálogos do prólogo e implementação da Dalva foram preservados.

## O que está implementado

- Exterior de 30×26: fachadas próprias da V8, jardins mais densos, árvores completas e banco na clareira. A placa do laboratório saiu da última célula da trilha e foi para o canteiro lateral, tornando o acesso direto utilizável.
- Duas casas com térreo e quarto: cozinha, madeira quente, janela, mapa, mesa xadrez, cadeiras, banco, cama, livros, console, relógio e PC nativo. Tecidos verdes para o protagonista, azuis para Ciro. O papel de cada casa acompanha a escolha do personagem.
- Laboratório normal e com bancada de recompensa: nova arte clara e verde-azulada, vitrines, mapa e bancada de trabalho. As três Pokébolas de recompensa mantêm os objetos e posições originais no estado pós-jogo; sua faixa de aproximação está livre.
- Sala de pesquisa e sala de equipamentos, ligadas por duas portas novas. Seis interações ambientais em PT-BR/EN. Esses anexos não introduzem recompensas ou flags de história.

São oito mapas externos/internos: vila, quatro andares domésticos, laboratório e dois anexos. Treze layouts contemplam as quatro variantes de papel doméstico e o segundo estado do laboratório.

## Relação com as referências

Os arquivos de `review/amanhecer_v9_concepts` são as referências fornecidas. Os comparativos `amanhecer_v9_concept_*.png` mostram, separadamente, referência e render nativo. A escala e o detalhamento foram adaptados à grade de 16×16, às paletas de 16 cores e à tela de 240×160.

A planta doméstica mantém a geometria de navegação que sustenta o prólogo, os encontros e as posições salvas das decorações. A reconstrução visual aproxima materiais e móveis das referências dentro desse contrato. A bancada principal do laboratório aparece com suportes vazios; a escolha inicial continua no resgate da Rota 101. A bancada pós-jogo utiliza os eventos reais existentes.

As imagens foram renderizadas de `map.bin`, gráficos indexados e paletas do jogo. Não são capturas de emulador. Os enquadramentos pequenos incluem margem preta onde a câmera ultrapassa o limite do mapa.

## Validação executada

- 342 células domésticas preservam exatamente colisão, elevação e comportamento; dimensões e eventos também foram preservados.
- Áreas de decoração dos dois quartos, coordenadas de PC/relógio/console e IDs de caixa/manual conservados nos dois bancos domésticos.
- 14 trajetos de laboratório verificados sobre os dois estados; retorno do resgate, entrada, Pokédex, assistente e recompensa acessíveis.
- Duas conexões recíprocas entre laboratório e anexos, seis interações ambientais alcançáveis, caminhos e eventos externos preservados.
- Código C real do motor testado em fixtures locais: 24 atualizações de PC, seis combinações de posição/direção, três regras de chegada e dois comportamentos de decoração.
- Seleção de papel doméstico executada para as oito combinações de mapa e personagem.
- Conversão nativa `mapjson`: 32 arquivos gerados; IDs anteriores preservados.
- ZIP reproduzido em pasta limpa: 91 arquivos do jogo e 46 imagens idênticos, instalação repetível, alteração não relacionada preservada e três conflitos recusados antes de qualquer escrita.
- PNGs 4bpp e orçamento verificados: 266 tiles de hardware no banco doméstico, 265 no laboratório; abaixo dos 496 slots estáticos disponíveis. O banco de Ciro compartilha a mesma geometria e arte, com paleta de tecidos própria.

O build completo da ROM e a execução em emulador não foram realizados neste ambiente. A integração é revisável e reproduzível, mas esses testes continuam necessários no ambiente de execução do jogo.

## Como integrar

Este ZIP é uma revisão incremental da cadeia local, após a Primeira Câmara V1. Não substitui a árvore inteira do repositório e não foi enviado para a `main` remota.

```sh
python3 tools/apply_amanhecer_v9.py --target /caminho/do/projeto --check
python3 tools/apply_amanhecer_v9.py --target /caminho/do/projeto
```

O instalador compara os pré-requisitos antes de escrever, preserva alterações não relacionadas em registros compartilhados e guarda cópia dos arquivos substituídos. Interrompe sem alterações se detectar conflito nos arquivos desta entrega.

Para reproduzir os dados e evidências em uma cópia extraída:

```sh
python3 tools/build_amanhecer_v9.py
python3 tools/validate_amanhecer_v9.py
python3 tools/probe_amanhecer_v9_native.py
python3 tools/build_amanhecer_v9_review.py
python3 scripts/render_anahi_annexes_en_checked.py --check
```

Dependências de revisão: Python com Pillow, fonte DejaVu Sans, compilador C/C++, make. Os demais `map.json` do ZIP são dependências do gerador nativo de IDs; somente os 91 arquivos declarados em `apply_amanhecer_v9.py` são aplicados.

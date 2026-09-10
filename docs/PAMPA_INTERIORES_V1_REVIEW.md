# Pampa da Espera — interiores V1, revisão

Sete mapas e quinze salas adaptados em tiles nativos: nove salas da Casa do Pampa/Ginásio de Elias, três casas, venda e dois andares do Centro. O exterior Pampa V1 continua intacto. A direção visual e os conflitos entre referências estão descritos em `PAMPA_INTERIORES_V1_BLUEPRINT.md` e no painel `review/pampa_interiores_v1_design_reference.png`.

## Evidência

- 52 warps, 30 objetos e 14 eventos de fundo conferidos. Não há gatilhos por coordenada nesses mapas.
- As sete rotinas `scripts.inc` permanecem byte-idênticas; também são preservados os scripts externos do tutorial, do pai de Val e dos serviços. Nenhuma fala, batalha, estoque, flag ou recompensa foi reescrita.
- Quatro bancos 4bpp: galpão 355 metatiles/280 tiles gráficos; casas 122/195; venda 42/92; Centro 287/219. Limites: 512 metatiles secundários e 496 tiles gráficos utilizáveis antes da área reservada.
- 59 metatiles de dispositivos copiados foram comparados pixel a pixel com os originais. Os demais dispositivos em slots fixos recebem decoração própria conservando seus atributos e coordenadas.
- Todos os acessos de sala, portas e interações foram percorridos pelo auditor. A modelagem do grafo do Ginásio cobre as 128 combinações dos sete treinadores nos estados anterior ao desafio, desafio, pós-vitória e revanche. Isso é auditoria estática do grafo, não execução do interpretador de scripts.
- As funções C reais da engine passaram em fixtures locais: oito grupos de portas nos cinco quadros, oito animações completas e oito aberturas diretas; 42 casos de etapa de escada e dois ciclos completos; PC em três direções; âncoras de cura para grupos de zero a seis Pokémon. Serviços e callbacks externos são controlados nesses testes.
- Os três renderizadores ingleses verificados passaram em `--check`. A política de build exclusivamente em inglês também passou na cópia completa do projeto.
- Quinze vistas completas de 240 × 160 e comparativos são renders dos `map.bin`; a moldura preta apenas acomoda salas menores. Nenhuma imagem é apresentada como captura de emulador.
- Conversão nativa `mapjson`: sete mapas, grupos e layouts compilados. O pacote inclui reprodução limpa dos builders, renders e validadores, com manifesto de hashes.

## Revisão e aplicação

Base local: `55fd170`, exterior Pampa V1. Aplicar apenas pelo instalador, que verifica conflitos antes de escrever. Não copiar todo o ZIP sobre outra versão do projeto: ele contém referências e dependências para reprodução.

```sh
python3 tools/apply_pampa_interiores_v1.py --target /seu/projeto --check
python3 tools/apply_pampa_interiores_v1.py --target /seu/projeto
```

O delta tem 101 arquivos de jogo: sete map.json, uma tabela de layouts, três registros de tilesets, quatorze binários de layouts privados e 76 arquivos dos quatro bancos. O instalador guarda backup, é idempotente e preserva os registros alheios de layouts e pontos de cura. Apenas o ponto de cura de Pampa é uma pré-condição desta entrega. Os sprites e paletas de Elias e Dalva constam entre as dependências protegidas.

Reprodução (Python 3, Pillow, DejaVu Sans, C/C++ e make):

```sh
python3 tools/build_pampa_interiores_v1.py
python3 tools/validate_pampa_interiores_v1.py
python3 tools/probe_pampa_interiores_v1_native.py
python3 tools/build_pampa_interiores_v1_review.py
```

O build ARM completo e o teste em emulador continuam pendentes, pois essas ferramentas não estão disponíveis neste ambiente. Os testes acima não certificam timing, sobreposição dinâmica de sprites ou comunicação entre instâncias da ROM. A adaptação espacial está concluída para este lote; a nova narrativa/chancela descrita na Bíblia permanece pendente. O andamento geral acompanha a entrega no relatório e inventário de 9 de setembro de 2026.

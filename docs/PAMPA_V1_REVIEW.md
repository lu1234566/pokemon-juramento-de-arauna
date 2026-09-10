# Pampa da Espera V1 — revisão e integração

Exterior nativo de 38 × 30, seis fachadas completas, galpão e sino, praça do fundador, cercados e dois lagos. O desenho segue a direção rural do Design Bible; a prancha fornecida para a Casa do Pampa é documentada como referência divergente. Os interiores ainda não foram adaptados neste lote.

## Integração

Base local: `884a255` (Casa do Uivo V1). São 28 arquivos de jogo: mapa, borda, eventos e script da cidade; layout e ponto de cura; três registros gráficos e banco secundário próprio. Os outros arquivos do ZIP são dependências e evidências. Não copiar o ZIP inteiro sobre o projeto.

```sh
python3 tools/apply_pampa_v1.py --target /caminho/do/jogo --check
python3 tools/apply_pampa_v1.py --target /caminho/do/jogo
```

O instalador verifica todos os conflitos antes de escrever, cria backup recuperável e preserva entradas não relacionadas dos registros compartilhados. Reaplicar a mesma versão não escreve novamente. Nenhum push, merge, Actions ou mudança no PR legado faz parte da entrega.

## Verificação

- Seis warps e seus retornos, nove objetos, oito gatilhos e oito eventos de fundo preservam identidade e ordem.
- Todos os prédios e módulos conferidos célula por célula; portas, aproximações e faixas de caminhada dos NPCs livres.
- 25 percursos geométricos verificados, incluindo as quatro variantes do guia, quatro de Bento, ida à Rota 102 e retorno à casa de Val. A checagem cobre colisão/elevação e interferência com moradores; não simula o agendamento da engine quadro a quadro.
- Três recompensas continuam inacessíveis a pé e alcançáveis com Surf. O menino olha para água reflexiva real.
- Oito funções reais da engine executadas em fixtures C: alcance de 675 células a pé, 36 transições de margem com 144 verificações e seis portas sem tarefa de animação indevida. Dependências da engine são controladas no teste; isso não é emulação da ROM.
- 204 dependências protegidas, incluindo rotas, interiores, flags, código nativo e renderizadores. O restante do script da cidade permanece byte-idêntico depois de normalizar os quatro movimentos e duas coordenadas declarados.
- Política English-only aprovada e renderizador inglês de Pampa/Rota 102 compatível. Não se pré-aplica a tradução sobre a fonte, pois o build oficial faz a composição transacional.
- Banco indexado 4bpp com 115 metatiles e 191/496 tiles estáticos de hardware, preservando slots reservados. Conversão de mapa, layouts e grupos por `mapjson` aprovada.
- Oito recortes de 240 × 160, mapa de eventos, antes/depois e prancha de direção artística. São renders dos arquivos nativos, não capturas de emulador.

O pacote inclui o teste de reprodução após extração e o teste de integração idempotente, com conflitos recusados antes de escrever. Os resultados estão em `review/pampa_v1_*_check.json` e demais relatórios JSON.

## Reprodução

Requisitos: Python 3, Pillow, fonte DejaVu Sans, compiladores C/C++ e make.

```sh
python3 tools/build_pampa_v1.py
python3 tools/validate_pampa_v1.py
python3 tools/probe_pampa_v1_native.py
python3 tools/build_pampa_v1_review.py
python3 tools/package_pampa_v1.py
python3 tools/check_pampa_v1_package.py
```

O build ARM completo e a execução em emulador continuam pendentes por indisponibilidade dessas ferramentas no ambiente. Também continuam pendentes os interiores de Pampa e a adaptação narrativa específica da Casa do Pampa. O inventário do restante do projeto acompanha esta entrega em `docs/ADAPTACAO_CONCEPT_STATUS_2026_09_09.md`.

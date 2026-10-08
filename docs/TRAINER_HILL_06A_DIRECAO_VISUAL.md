# Direção visual — Trainer Hill 06A

Trainer Hill é um equipamento de desafios próximo à Rota 111, onde a Bible passa do semiárido à serra. Sua nova aparência usa essa transição: arenito ocre, juntas irregulares de pedra, madeira escura, tecido oliva e ardósia. O projeto mantém a geometria original para que escadas, portas, posições dos treinadores e trajetos cronometrados continuem correspondendo aos scripts.

A recepção é clara e legível, com faixa de tecido no balcão e piso contínuo. Nos desafios, barreiras têm topo claro, face sombreada e base escura: a silhueta deve comunicar bloqueio. Os pisos livres usam juntas discretas, sem a mesma sombra das barreiras. Setas, notas, placas, painéis e outros pictogramas originais ficam visíveis para não esconder as regras dos puzzles. A cobertura ganha uma massa de ardósia escura sobre pedra clara; o terraço permanece aberto e suas saídas ficam legíveis. A cabine do elevador usa painéis de madeira e piso de pedra.

## Referências e proveniência

- `Arauna_Master_Map_Design_Bible.pdf`, p. 16, Rota 111: semiárido → deserto → serra, rochas, caatinga e areia. O mesmo material também foi recuperado em texto antes da edição.
- Concept original: `concepts/Arauna_Rotas_e_Cavernas_Conceituais/01_Rotas_de_Superficie/05_Rota_111_Semiarido_Deserto_Serra.png`, em `docs/referencias/bible_concepts_recuperados`.
- Pacote recuperado de Bible/concepts: SHA-256 `ecf381db95864a61e191a9fcf2525e3f892a1dd934e5aaca7c43344f5e6e19e3`.
- Não há concept próprio de Trainer Hill no conjunto recuperado. Esta adaptação é um suplemento visual, sem renomear a localização ou acrescentar história/progressão.
- Concept desta etapa: `review/trainer_hill_06a/concept/TrainerHill_06A_Direcao.png`, criado com a ferramenta integrada de geração de imagens. Brief: prancha de pixel art vista de cima para um pavilhão de desafios GBA na serra/semiárido de Arauna, com recepção, piso de desafios, cobertura e amostras de material; arenito ocre, madeira escura, tecido oliva, ardósia cinza azulada; escala e legibilidade de Pokémon de terceira geração; sem texto narrativo nem alterações de jogabilidade. A prancha orienta materiais e atmosfera; suas formas não são blockdata nem geometria de ROM.

## Arte instalada

A arte de produção foi feita como pixels indexados nativos por `trainer_hill_06a_art.py` e instalada por `build_trainer_hill_06a.py`. Não é um recorte/redimensionamento da prancha gerada. Cada tile tem 8×8 pixels e 4bpp; cada metatile tem 16×16 pixels. As cores são quantizadas para RGB555. A paleta de materiais usa 16 entradas; as paletas das duas portas animadas permanecem intactas.

São dois pares privados de bancos: pavilhão (recepção, andares e cobertura) e elevador. Os metatiles preservam IDs e atributos. Planos arquitetônicos mantêm as máscaras de transparência de ambas as camadas; os pixels de fundo foram convertidos em pedra ou ardósia. Os bancos originais continuam na base, sem limpeza de materiais nesta etapa.

Limite artístico deliberado do V1: os dois modelos de porta animada do elevador e os pictogramas funcionais mantêm seus desenhos nativos. A prancheta conceitual não promete portas ou geometrias que este pacote não instalou. A adaptação dessas animações pode ser feita em uma manutenção posterior com revisão no emulador.

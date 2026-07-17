# Game Design Document

## Pokémon: Juramento de Arauna

- **Status:** pré-produção da versão definitiva
- **Versão do GDD:** 0.2
- **Direção criativa:** Lucas Barcelar
- **Plataforma:** Game Boy Advance
- **Base:** pokeemerald-expansion 1.16.2

## High concept

Uma jornada Pokémon bilíngue de fantasia sombria em Arauna, uma região ficcional inspirada em todo o Brasil e dividida em grandes biomas. O protagonista investiga o desaparecimento do antigo Campeão enquanto a Liga, uma organização tecnológica e guardiões tradicionais disputam o controle dos Juramentos: vínculos antigos capazes de despertar os protetores da região.

O jogo substitui os 386 slots da Pokédex do Emerald por uma Pokédex própria de Arauna. Ecologia, progressão, tipos e identidade visual serão concebidos como um conjunto único, e não como uma simples troca de nomes.

## Fantasia do jogador

O jogador atravessa uma versão fantástica e viva do Brasil, forma uma equipe inteiramente ligada a Arauna, conquista Selos e descobre como cada bioma foi afetado pela Noite Sem Estrelas. Suas respostas representam Coragem, Sabedoria ou Compaixão e alteram relações, recompensas, cenas e partes do desfecho.

## Pilares

1. **Brasil fantástico, não caricatural:** referências aparecem na fauna, flora, arquitetura, clima, cultura material e conflitos locais.
2. **Pokédex com função ecológica:** cada uma das 386 espécies possui habitat, nicho, curva de disponibilidade e função de batalha.
3. **Exploração com identidade:** mapas, encontros e personagens contam a história de Arauna.
4. **Vínculos com consequências:** escolhas são lembradas e produzem mudanças visíveis.
5. **Batalhas planejadas:** líderes e chefes utilizam estratégias, não apenas níveis maiores.
6. **Leitura autêntica de GBA:** cenários e sprites respeitam limites, contraste e linguagem visual de Pokémon Emerald.
7. **Produção em etapas:** nenhum lote grande de arte entra no jogo antes de um pequeno lote provar o fluxo completo.

## Tom e limites

- Maduro e sombrio, com perdas, segredos, corrupção institucional e conflitos morais.
- Esperança, amizade e descoberta continuam centrais.
- Sem violência gráfica, crueldade gratuita ou choque usado como substituto de narrativa.
- O antagonista deve possuir uma crença defensável, mesmo quando seus métodos são inaceitáveis.

## Idiomas

- Português brasileiro: texto autoral principal.
- Inglês: localização adaptada.
- Builds e patches separados a partir da mesma versão.
- A seleção interna de idioma continua sendo uma decisão técnica posterior.

## Protagonista

O protagonista fala, possui personalidade reconhecível e participa das cenas. O jogador escolhe respostas importantes, mas não controla cada frase.

- **voz fixa:** curiosidade, iniciativa e ligação pessoal com o mistério;
- **voz variável:** Coragem, Sabedoria ou Compaixão determinam como reage;
- **agência real:** escolhas destacadas precisam produzir ao menos uma consequência observável.

Para o greybox, o protagonista tem 16 anos, vive na Vila das Araucárias e mantém nome e aparência selecionáveis. A direção visual final ainda depende de aprovação.

## Mundo

Arauna não reproduz o mapa político do Brasil. Ela reorganiza referências brasileiras em macrobiomas ficcionais conectados por rotas, rios, serras, litoral e infraestrutura urbana. Cada área precisa funcionar como lugar vivido e cumprir uma função ecológica, econômica ou histórica.

O percurso começa na Mata das Araucárias e se expande para Mata Atlântica, Pampas, litoral e manguezais, Cerrado, Pantanal, Caatinga, Floresta Amazônica, serras, cavernas e grandes centros urbanos.

## Facções

| Facção | Crença | Papel |
|---|---|---|
| Liga de Arauna | O conhecimento dos Juramentos precisa ser controlado | Autoridade ambígua |
| Organização tecnológica | Dominar os Vínculos evitará uma nova catástrofe | Antagonista compreensível |
| Guardiões tradicionais | Os Juramentos precisam ser restaurados | Preservação e memória |
| Protagonista e aliados | O futuro não precisa repetir nenhuma das soluções antigas | Transformação |

## Loop principal

1. Chegar a uma nova área e compreender seu conflito.
2. Explorar, capturar e montar respostas para a ecologia local.
3. Encontrar uma pista sobre os Juramentos ou a Noite Sem Estrelas.
4. Tomar uma decisão ou completar uma missão.
5. Enfrentar um treinador principal com estratégia ligada ao bioma.
6. Obter um Selo, acesso ou nova informação.
7. Observar consequências em personagens, encontros ou no ambiente.

## Estrutura de lançamento

### Vertical slice definitivo

30 a 60 minutos:

- Vila das Araucárias reconstruída com linguagem visual de GBA;
- centro de pesquisa e escolha do inicial;
- rival Nilo;
- Rota da Neblina;
- Ruína do Primeiro Elo;
- uma decisão de Vínculo;
- miniboss e aparição parcial de um guardião;
- 12 a 18 espécies jogáveis, usando somente sprites aprovados ou placeholders declarados.

### Demo pública 1

2 a 4 horas, três assentamentos, dois Selos, duas áreas especiais, primeiro arco completo e 60 a 80 espécies disponíveis.

### Campanha pretendida

Oito Selos, Liga, três variações de desfecho, pós-jogo e 386 entradas obtíveis ou registráveis. A duração final será recalculada após o vertical slice e a primeira demo.

## Pokédex de Arauna

- 386 slots substituem integralmente a Pokédex do Emerald.
- Os nove primeiros slots pertencem às três linhas de iniciais.
- Cada espécie recebe conceito, tipo, habilidades, stats, evolução, learnset, habitat, sprite e textos `pt-BR`/`en`.
- Espécies oficiais só podem aparecer como referências temporárias de desenvolvimento e nunca como conteúdo final silencioso.
- Formas regionais ou releituras de Pokémon oficiais são exceções e dependem de decisão explícita.
- A produção ocorre por lotes pequenos com aprovação de conceito e de sprite separadas.

## Trio de iniciais

| Slots | Inspiração | Tipagem final | Identidade de batalha |
|---|---|---|---|
| 001–003 | pica-pau brasileiro | Grass/Rock | pressão física, defesa e controle de campo |
| 004–006 | vira-lata caramelo | Fire/Dragon | versatilidade, coragem e ofensiva equilibrada |
| 007–009 | quero-quero | Water/Bug | velocidade, interrupção e utilidade |

O ciclo secundário cria respostas cruzadas: Rock ameaça Fire, Fire ameaça Bug e Bug ameaça Grass. Isso reduz confrontos totalmente previsíveis sem apagar o triângulo clássico dos tipos primários.

## Sistemas modernos

Mega Evolução, Z-Moves, Dynamax e Terastal não serão ativados apenas por existirem no motor. A mecânica principal deve servir à história, ao balanceamento e aos limites de memória do GBA.

## Critério do primeiro sucesso

Cinco pessoas recebem o patch correto, iniciam um save novo e terminam o vertical slice. Pelo menos quatro concluem sem bloqueadores, reconhecem a identidade brasileira sem perceber caricatura, entendem o conflito central e descrevem uma consequência de sua escolha de Vínculo.

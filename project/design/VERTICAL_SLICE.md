# Greybox do vertical slice

## Estado e objetivo

Este documento fixa a menor versão jogável do primeiro arco de *Pokémon:
Juramento de Arauna*. O greybox deve durar entre 30 e 60 minutos, usar arte
provisória quando necessário e provar o fluxo completo sem comandos de debug.

O slice começa na Vila das Araucárias, apresenta os três iniciais, atravessa a
Rota da Neblina e termina na Ruína do Primeiro Elo após uma decisão de Vínculo,
um miniboss e uma breve manifestação de um guardião.

O greybox estará concluído quando um save novo puder chegar à tela final sem
ficar preso, perder um item obrigatório ou repetir um evento essencial.

## Decisões de trabalho

As definições abaixo são válidas para o greybox. Aparência final, textos finais
e detalhes biográficos ainda podem ser refinados no Marco 4.

### Protagonista

- tem 16 anos e vive na Vila das Araucárias;
- participa de um programa local de iniciação à pesquisa de campo;
- mantém nome e aparência selecionáveis com os recursos provisórios do motor;
- possui a mesma personalidade e função narrativa em todas as aparências;
- demonstra curiosidade, iniciativa e ligação pessoal com o mistério;
- expressa Coragem, Sabedoria ou Compaixão apenas nas decisões destacadas.

### Rival

Nilo deixa de ser apenas o treinador técnico do mapa-laboratório e passa a ser
o rival provisório do vertical slice.

- tem 17 anos e é aprendiz de guarda-florestal;
- cresceu ao lado do protagonista e conhece as trilhas da região;
- é competitivo, observador e genuinamente protetor;
- acredita que agir sem compreender o terreno coloca outras pessoas em risco;
- reage de modo diferente à primeira decisão de Vínculo, sem representar uma
  tendência moralmente superior;
- usa o inicial com vantagem de tipo contra a escolha do jogador.

### Elenco funcional

| Papel | Função no slice | Estado do nome |
|---|---|---|
| Responsável do protagonista | Apresenta rotina, afeto e urgência inicial | Não definido |
| Pesquisadora-chefe | Conduz o programa e guarda os três iniciais | Dra. Maia, provisório |
| Assistente de pesquisa | Tutorial de cura, Poké Bolas e registros | Não definido |
| Nilo | Rival, guia de campo e espelho da decisão | Definido para o greybox |
| Morador da missão opcional | Procura um caderno perdido na neblina | Não definido |
| Agente da organização | Miniboss e primeira face do conflito | Codinome provisório |

## Limites do conteúdo

- aventura sombria sem violência gráfica, crueldade gratuita ou sustos de
  choque;
- nenhuma evolução dos iniciais precisa aparecer;
- nenhuma mecânica de batalha própria dos Vínculos será implementada;
- sprites, música e interiores podem usar placeholders documentados;
- a seleção de idioma continua no momento da compilação;
- o slice não entrega Selo, ginásio, Liga nem acesso ao restante de Arauna;
- nenhum item obtido por uma escolha pode ser obrigatório para progredir.

## Mapas

O limite do greybox é de seis mapas jogáveis. A Vila das Araucárias reaproveita
o layout e o tileset já validados no `AraunaMapLab`, removendo gradualmente os
elementos de laboratório técnico.

| Ordem | Mapa de trabalho | Função | Entrada e saída |
|---:|---|---|---|
| 1 | Casa do Protagonista | Abertura, nome e primeiro objetivo | Sai para a vila; retorno sempre permitido |
| 2 | Vila das Araucárias | Hub, apresentação de Nilo e acesso à rota | Casa, centro e rota possuem destinos válidos |
| 3 | Centro de Pesquisa | Incidente, escolha do inicial e preparação | Retorna à vila após concluir a escolha |
| 4 | Rota da Neblina | Captura, treinadores e missão opcional | Liga a vila à ruína; atalhos não são obrigatórios |
| 5 | Ruína do Primeiro Elo | Exploração curta e decisão de Vínculo | Permite recuar até a luta do miniboss |
| 6 | Câmara do Primeiro Elo | Miniboss, guardião, revelação e encerramento | Termina em tela final; não libera área inexistente |

## Fluxo principal

1. Uma abertura curta mostra fragmentos da Noite Sem Estrelas sem explicar sua
   causa.
2. O protagonista desperta e recebe o objetivo de comparecer ao Centro de
   Pesquisa.
3. A vila apresenta Nilo, o centro, a saída bloqueada e dois moradores.
4. No centro, uma reação energética assusta os três Pokémon raros mantidos em
   observação.
5. O jogador inspeciona cada inicial e confirma uma escolha; cancelar retorna à
   seleção sem conceder Pokémon.
6. Um Pokémon selvagem afetado invade a área e cria o combate tutorial.
7. Nilo testa o protagonista em uma batalha curta e recebe o inicial com
   vantagem de tipo.
8. A pesquisadora entrega Poké Bolas, cura a equipe e libera a Rota da Neblina.
9. Na rota, o jogador encontra espécies selvagens, três treinadores e a missão
   opcional do caderno de campo.
10. Um Pokémon afetado foge em direção à ruína interditada; Nilo acompanha o
    protagonista.
11. Na ruína, um mecanismo instável prende o Pokémon e apresenta as respostas
    de Coragem, Sabedoria e Compaixão.
12. As três respostas salvam o Pokémon, registram uma consequência e convergem
    para a câmara interior.
13. Um agente da organização tenta recolher a energia liberada e atua como
    miniboss.
14. Após a vitória, uma presença colossal projeta uma memória do antigo Campeão
    e a demo termina com o juramento registrado no save.

## Estado de progressão

Os nomes abaixo descrevem a intenção. Os IDs reais de constantes serão alocados
em uma tarefa de implementação, depois de verificar os intervalos livres.

### Variáveis

| Variável lógica | Valores | Uso |
|---|---|---|
| `VAR_ARAUNA_STORY_STAGE` | 0–8 | Controla a progressão obrigatória |
| `VAR_ARAUNA_STARTER_CHOICE` | 0, Grass, Fire, Water | Evita conceder mais de um inicial |
| `VAR_ARAUNA_BOND_CHOICE` | 0, Courage, Wisdom, Compassion | Registra a primeira decisão |
| `VAR_ARAUNA_OPTIONAL_MISSION` | 0–3 | Separa a missão secundária da trama |

### Estágios obrigatórios

| Estágio | Estado alcançado | Próxima transição válida |
|---:|---|---|
| 0 | Novo jogo na casa | Receber chamado para o centro |
| 1 | Centro liberado | Confirmar um inicial |
| 2 | Inicial obtido | Vencer ou perder o tutorial sem duplicar concessões |
| 3 | Batalha com Nilo concluída | Liberar a rota |
| 4 | Rota em exploração | Encontrar o Pokémon afetado |
| 5 | Ruína aberta | Registrar uma decisão de Vínculo |
| 6 | Decisão registrada | Enfrentar o agente |
| 7 | Miniboss derrotado | Executar a cena do guardião |
| 8 | Vertical slice concluído | Exibir encerramento repetível e seguro |

Flags de objetos devem esconder itens coletados, controlar treinadores
derrotados, impedir a repetição da abertura e preservar atalhos. Nenhuma flag
opcional poderá substituir `VAR_ARAUNA_STORY_STAGE`.

## Escolha dos iniciais

As primeiras formas entram com dados de batalha próprios e sprites placeholder.
Os codinomes de desenvolvimento podem ser exibidos apenas enquanto os nomes
finais não forem aprovados.

| Projeto | Tipo inicial | Papel no começo | Oponente de Nilo |
|---|---|---|---|
| Capivara | Grass | Resistência, recuperação e suporte | Projeto Gato-do-mato |
| Gato-do-mato | Fire | Velocidade e pressão | Projeto Lontra |
| Lontra | Water | Controle e adaptação | Projeto Capivara |

Regras:

- todos começam no nível 5 e chegam com golpes funcionais;
- a tela exige confirmação antes de gravar escolha e espécie;
- o Pokémon não pode ser entregue novamente após derrota ou recarga;
- a escolha do inicial não altera nem limita a tendência de Vínculo;
- Pokédex, resumo, cura, depósito e save precisam aceitar as três espécies.

## Primeira decisão de Vínculo

Um Pokémon afetado está preso junto a um mecanismo antigo. A cena possui uma
entrada e uma saída comuns, mas três resoluções legíveis.

| Tendência | Ação | Consequência imediata | Reconhecimento posterior |
|---|---|---|---|
| Coragem | Entrar antes que a estrutura ceda | O Pokémon sai rápido, mas parte da passagem desaba | Nilo reconhece iniciativa e questiona o risco |
| Sabedoria | Desativar o mecanismo pelas inscrições | A sala permanece estável e revela um registro extra | Nilo admite que o plano evitou danos |
| Compaixão | Acalmar o Pokémon e seguir seus sinais | O Pokémon revela uma passagem lateral segura | Nilo percebe que a criatura compreendeu o jogador |

Cada resolução concede uma recompensa opcional de valor semelhante. O item
exato será escolhido durante o balanceamento, e nenhuma rota será tratada como
resposta correta.

## Encontros e batalhas provisórios

### Faixa de níveis

| Conteúdo | Nível esperado |
|---|---:|
| Combate tutorial | 3 |
| Primeira batalha com Nilo | 5 |
| Encontros no começo da rota | 2–4 |
| Encontros perto da ruína | 4–6 |
| Treinadores comuns | 4–7 |
| Miniboss | equipe de 2 Pokémon nos níveis 7–8 |

### Conjunto ecológico inicial

As espécies abaixo são candidatas provisórias e serão verificadas contra dados,
curva de evolução e disponibilidade técnica antes da implementação:

- Rota da Neblina: Poochyena, Zigzagoon, Taillow, Hoothoot, Seedot, Shroomish,
  Wurmple, Budew, Lotad, Wooper, Nincada e Rookidee;
- proximidade e interior da ruína: Duskull, Baltoy, Roggenrola, Phantump,
  Morelull e Unown.

O conjunto total possui 18 espécies e fica dentro da meta de 15 a 25. Espécies
raras não podem ser necessárias para concluir a demo.

### Treinadores

O greybox prevê seis batalhas de treinador:

1. Nilo após a escolha do inicial;
2. estudante de campo na primeira metade da rota;
3. coletora de ervas na área de vegetação;
4. aprendiz de guarda-florestal perto da neblina densa;
5. explorador opcional ligado ao caderno perdido;
6. agente da organização como miniboss.

## Missão secundária

Um morador perdeu um caderno de observação na Rota da Neblina. O jogador pode
recuperá-lo antes de entrar na ruína.

- aceitar, encontrar e entregar usam estados separados;
- o caderno não ocupa um espaço capaz de bloquear a missão principal;
- a recompensa é útil, mas não exclusiva a ponto de punir quem ignorar a missão;
- Nilo possui uma fala curta reconhecendo a devolução;
- a missão continua concluível antes do miniboss e expira apenas na tela final.

## Falhas e recuperação

- perder qualquer batalha retorna ao último ponto de cura sem avançar o estágio;
- perder para Nilo não concede outro inicial nem bloqueia uma revanche;
- perder para o miniboss permite repetir a batalha e não repete a decisão;
- inventário cheio mantém itens opcionais disponíveis para nova tentativa;
- salvar e carregar preserva estágio, inicial, decisão, missão e treinadores;
- recusar uma escolha ou diálogo retorna o controle ao jogador;
- sair de um mapa nunca coloca o jogador diante de uma conexão inexistente;
- a tela final pode ser revista, mas não concede recompensas novamente.

## Localização

- português brasileiro permanece como texto autoral principal;
- inglês adapta tom e ritmo em vez de traduzir literalmente;
- símbolos de texto compartilham as mesmas chaves entre builds;
- nomes de personagens e iniciais devem funcionar nos dois idiomas;
- cada cena será testada nas caixas do GBA nas duas builds;
- a lógica não pode depender do tamanho de uma fala localizada.

## Ordem de implementação

1. Criar shells dos seis mapas, conexões e progressão básica.
2. Adicionar as três espécies provisórias e a escolha do inicial.
3. Implementar casa, vila, centro, tutorial e primeira batalha com Nilo.
4. Implementar a rota, encontros, treinadores e missão secundária.
5. Implementar a ruína e as três resoluções de Vínculo.
6. Implementar miniboss, manifestação do guardião e encerramento.
7. Executar regressão bilíngue, save/reload e jogo completo sem debug.

Cada passo deve gerar uma alteração testável e reversível. Arte final não pode
bloquear a validação da lógica.

## Checklist de saída do Marco 3

- [ ] save novo chega ao encerramento sem comando de debug;
- [ ] os seis mapas possuem entradas e saídas válidas;
- [ ] os três iniciais funcionam em batalha, resumo, cura e save;
- [ ] Nilo escolhe corretamente o inicial com vantagem;
- [ ] encontros e treinadores permitem progressão sem treino excessivo;
- [ ] a missão opcional não bloqueia a história;
- [ ] as três decisões de Vínculo convergem e deixam consequências distintas;
- [ ] vitória e derrota do miniboss preservam o estado correto;
- [ ] save/reload funciona em cada estágio obrigatório;
- [ ] português e inglês concluem o mesmo fluxo;
- [ ] nenhuma ROM, save ou asset sem origem é versionado;
- [ ] CI e testes automatizados permanecem verdes.

## Fora do escopo do greybox

- sprites finais e animações das três linhas evolutivas;
- mapas além da Vila, Rota da Neblina e Ruína do Primeiro Elo;
- Selo, ginásio, Liga ou segunda decisão de Vínculo;
- sistema de reputação ou painel de tendências;
- mecânica moderna exclusiva;
- seleção de idioma dentro da ROM;
- patch público.

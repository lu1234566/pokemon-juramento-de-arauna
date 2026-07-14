# Plano de testes

## Gates de integração

Uma mudança só pode chegar à `main` quando:

1. a verificação de arquivos proibidos passa;
2. o alvo Emerald compila;
3. os testes oficiais passam;
4. os testes manuais afetados estão registrados;
5. documentação e créditos foram atualizados quando necessário.

## Teste por alteração

- [ ] Build limpo.
- [ ] Nenhum warning novo relevante.
- [ ] Evento inicia, conclui e não repete indevidamente.
- [ ] Flags e variáveis permanecem corretas.
- [ ] Vitória e derrota não quebram a progressão.
- [ ] Save e carregamento funcionam.
- [ ] Debug temporário foi removido ou protegido por configuração.

## Teste bilíngue

- [ ] `pt-BR` e `en` vêm do mesmo commit.
- [ ] Conteúdo e correções são equivalentes.
- [ ] Textos cabem nas caixas.
- [ ] Nomes próprios seguem o glossário.
- [ ] Variáveis e pronomes funcionam.
- [ ] Nenhuma chave está ausente.

## Teste de mapa

- [ ] Entradas, saídas e posição após warp.
- [ ] Colisões e elevações.
- [ ] Conexões entre mapas.
- [ ] NPCs não bloqueiam passagens permanentemente.
- [ ] Áreas futuras não podem ser acessadas cedo.
- [ ] Encontros, música e clima corretos.
- [ ] Revisitar o local produz o estado esperado.

## Teste de inicial original

- [ ] Escolha e recebimento com equipe vazia e cheia.
- [ ] Sprite frontal, traseiro, ícone e paletas.
- [ ] Resumo, Pokédex e PC.
- [ ] Stats, habilidade, natureza e gênero.
- [ ] Learnset e TMs.
- [ ] Evolução e cancelamento.
- [ ] Shiny.
- [ ] Cry.
- [ ] Save e carregamento antes e depois da evolução.

## Regressão do vertical slice

- [ ] Save novo até o encerramento.
- [ ] Cada inicial.
- [ ] Cada escolha de Vínculo.
- [ ] Derrota em todas as batalhas obrigatórias.
- [ ] Equipe cheia ao receber recompensa.
- [ ] Inventário em condições limítrofes.
- [ ] Caminhos opcionais e retorno a mapas anteriores.
- [ ] Pelo menos duas execuções recentes do mGBA.
- [ ] Aplicação limpa dos patches nas bases corretas.

## Severidade

| Nível | Exemplo | Política |
|---|---|---|
| Bloqueador | Não compila ou não inicia | Impede integração |
| Crítico | Trava, corrompe save ou impede progressão | Impede lançamento |
| Alto | Evento ou mecânica central incorreta | Corrigir antes da versão |
| Médio | Problema perceptível com alternativa | Planejar correção |
| Baixo | Texto ou decoração pequena | Agrupar em revisão |

## Evidência de teste

Issues e PRs devem registrar:

- commit testado;
- emulador e versão;
- idioma;
- save novo ou migrado;
- passos executados;
- resultado;
- captura ou log quando útil.

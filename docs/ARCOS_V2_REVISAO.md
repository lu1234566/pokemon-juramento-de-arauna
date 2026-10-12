# Arcos V2 — implementação e limites de aceitação

Base: `eee381dcaf524ff98ccef100ab60f39fa00f356f`, de 12/10/2026.
Fontes: Roteiro Canônico v2.0, seções 20.1, 31 e 32; Bíblia Narrativa v1.3;
contrato da Casa do Uivo; implementação atual de `ARCOS_RASCUNHO.md`.

## Comportamento entregue

- Eremita: nove quadros próprios de 16 × 32, folha 144 × 32, paleta exclusiva.
- Filhote: nove quadros próprios de 32 × 32, folha 288 × 32, sem alterar a
  espécie selvagem ou o registro de Guaracim.
- Uivo: compromisso de acessibilidade com três escolhas, recusa sem perda de
  progresso e replay escrito após conclusão, sem recompensa duplicada.
- Fogueira: a roda de escuta permanece acessível mesmo depois da sétima
  insígnia e durante o arco. A volta com SACRED ASH exige Liga e Torre do Ruído.
- Torre do Ruído: cinco mapas novos, acessíveis por Ciro na Casa da Fogueira
  depois do Hall da Fama. As saídas retornam à entrada da Casa.
- Anahi: o Aurora Ticket exige conclusão da Torre e despertar de Arauá na
  roda. Saves antigos com o ticket/viagem já habilitados não perdem acesso.
- O validador antigo redireciona para a validação atual; o original permanece
  disponível para a entrega histórica V1.

## Torre: TR01–TR09

| Núcleo | Eventos | Implementação |
|---|---|---|
| Recepção | TR01 | Ciro abre acesso; evacuar ou explicar aos trabalhadores, com consentimento e estado persistente. |
| Essência | TR02–TR03 | Devolver três lotes em qualquer ordem; preservar o item 11.407 de Dona Zila por cópia protegida ou devolução assistida por Anahi. |
| Contratos | TR04 | Ciro publica sua assinatura e a autorização médica da mãe, mantendo decisões separadas. |
| Barragem | TR05 | Reunir gravação, desenho, relatório escolar e documento do teste da barragem em qualquer ordem. |
| Sifão | TR06–TR09 | O agente ajuda ou hesita conforme a abordagem aos trabalhadores; batalha própria com Meira, nv56–58; contenção e leitura dos documentos; escolha de custódia e rendição. |

Os andares reutilizam **layouts técnicos nativos de AraunaSerraTecnica**, já
presentes no repositório. Não foram tratados como nova adaptação final do
concept da Torre. Os eventos, objetos e warps são próprios; as salas
originais da Serra continuam intactas. O mapa da região não recebe uma
fachada nova nesta etapa: o acesso é uma viagem oferecida por Ciro.

Os casos do roteiro ainda não existentes no save têm resolução assistida por
Ciro e Anahi. Não são prometidos aqui o sistema completo de eixos, a variante
de batalha contra o Agente, visuais saturados de Essência, o montage dos vinte
Espíritos, os Testemunhos finais ou toda a contação combinatória do ato 32.
O rito cerimonial de Arauá continua no encontro existente de Birth Island.

## Alocações e saves

| Recurso | Alocação |
|---|---|
| Mapas | Cinco nomes no fim do último grupo; IDs anteriores não mudam. |
| Treinador | `TRAINER_ARAUNA_TOWER_MEIRA` 858; `TRAINERS_COUNT` 859, dentro do limite 864. |
| Variáveis | 0x40FB–0x40FE para Torre; 0x40FF para compromisso do Uivo. |
| Flags | 0x043–0x04C: conclusão, três lotes, quatro documentos, despertar de Arauá e visibilidade de Ciro. |
| Gráficos | IDs virtuais 0x1001/0x1002; canais E/F preparados na transição. |
| Paletas | Tags 0x1200/0x1201 na tabela; Eremita e filhote no slot especial exclusivo de suas salas separadas. |

Nenhuma estrutura persistente, limite de flags, slot de insígnia ou variável
de progressão de Emerald foi ampliado. Estado 4 da Fogueira em save antigo
não é rebaixado e SACRED ASH não é concedida novamente. O estado 3 antigo
passa a aguardar o novo fluxo. A Torre pode ser feita mesmo sem terminar Uivo
ou Primeiro Elo.

## Reprodução da validação

```sh
python3 tools/arauna_maps/validate_fogueira_arcos.py --output review/arcos_v2/validation.json
python3 tools/arauna/check_arcos_assets.py
python3 tools/arauna_maps/validate_fogueira_roda_v1.py
bash scripts/check_arauna_static.sh
bash scripts/build_arauna.sh -j2 all
```

O modelo percorre 2.240 cenários da roda, 30 de Fogueira, 1.728 jornadas da
Torre, sete casos do Uivo e 33 do Aurora Ticket. Confere saídas, interações acessíveis, formas de
recusa, perda e retomada da batalha, mochila cheia e idempotência. As linhas
medidas ficam dentro de 208 pixels, com reserva para nome de jogador de sete
caracteres. Essa contagem é de caminhos de eventos modelados, não de jornadas
executadas no emulador.

## Aceitação ainda necessária

1. Tradução qualificada para Libras e revisão surda sinalizante — ainda não
   realizadas. O modo escrito é o único ativado.
2. Revisão autoral das falas e das adaptações do rascunho.
3. Aceitação visual no emulador: sprites, paletas, chegada/saída das cinco
   salas, derrota/retorno reais, save/load e efeitos da Fogueira.

Compilação e CI devem ser reportadas com o commit efetivamente testado. Não
reutilizar o teste visual antigo como evidência desta versão.

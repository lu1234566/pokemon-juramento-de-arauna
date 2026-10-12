# Arcos em rascunho: Casa do Uivo, Primeira Câmara e Casa da Fogueira

> **Rascunho.** Estas cenas foram escritas a partir da sinopse, da Design Bible
> e do contrato da Casa do Uivo, para que os três lugares deixem de ser só
> visita e passem a ter história jogável. Não são o texto canônico do roteiro:
> a Bíblia lista as cenas (U03–U11, S09–S13) mas não o diálogo. Tudo aqui pode
> ser reescrito sem mexer em mapa, flag ou variável — os estados ficam, as
> falas trocam.

O Eremita da Casa do Uivo fala **por escrito**: cada fala dele é uma página do
caderno virada para a sala. Nenhuma fala é apresentada como Libras e nenhum
gesto foi inventado. A cena sinalizada (seção 20.1 do roteiro: tradução
qualificada, revisão por pessoa surda sinalizante, storyboard, legenda e
replay) continua pendente, como o `CASA_UIVO_V1_BLUEPRINT.md` exige.

## Casa do Uivo — U03 a U11

Serra do Uivo (slot de Rustboro). Abre depois da **segunda insígnia**, que é o
"Selo da Maré" da Bíblia; antes disso a visita continua igual.

| cena | onde | o que acontece | `VAR_ARAUNA_UIVO_STATE` |
|---|---|---|---:|
| U03 consentimento | Sala, Eremita | Ele pergunta se você quer ler a história da mãe com ele. "Não" é uma resposta completa e não muda nada. | 0 → 1 |
| U04 relato e interrupção | Sala | O relato escrito; um caminhante entra contando que o uivo voltou e que os mineiros querem espantar com lampião. O Eremita pede para pôr os cadernos da mãe em ordem. | → 2 |
| U05 os cadernos | Memórias, mesa | Escolher qual caderno vem primeiro e qual vem depois ("família ao entardecer", "filhote na neblina", "pano nas pedras"). Ordem errada: as páginas não fecham e recomeça. Certa: a história inteira, terminando em "Don't chase a howl. Answer it." | → 3 |
| U05 o pano | Memórias | Pegar o pano da mãe (sim/não). | → 4 |
| U06–U07 busca e batalha de acalmar | Refúgio | Ao entrar, ouve-se o uivo. Um GUARACIM (#052) filhote, apavorado, junto à cachoeira: batalha selvagem nv17. Se ele cai ou foge, o pano o acalma e um GUARÁ adulto responde do alto; ele volta para casa. Se for capturado, o pano vai com ele. Se você foge, ele continua lá. | → 5 |
| U08–U09 reconto | Sala | A serra reunida (o caminhante, uma tecelã, um mineiro). O Eremita conduz: mostra os cadernos à sala e escreve uma página nova. O texto muda se o filhote foi capturado. | → 6 |
| U10 compromisso | Sala | Assinar o registro com a serra (sim/não). "Não" não fecha nada: dá para voltar. | → 7 |
| U11 registro e selo | Sala | Um sino com um GUARÁ uivando no cabo: o **HOWL SEAL** (o Selo do Uivo) — no jogo é um SOOTHE BELL. | → 8 |

O Eremita e o filhote agora têm arte própria: nove quadros de caminhada,
PNG indexado de 4 bits e paleta exclusiva. Usam IDs virtuais nos canais de
gráfico E/F, definidos na transição dos respectivos mapas. A espécie selvagem
Guaracim e seu registro de overworld continuam intactos; o gancho
`AraunaStory_OnTransition` não sobrescreve mais o canal A para esta cena.

Depois do reconto, o compromisso registra intérprete comunitário, aulas
contínuas ou conselho bilíngue com liderança surda. Recusar todas as opções
mantém o estado 6. Depois de concluir o arco, o Eremita oferece replay do
relato e do reconto escritos, respeitando o ramo do filhote e sem repetir
missão ou recompensa. Isso não é Libras; a preparação linguística está em
`CASA_UIVO_LIBRAS_PRODUCAO.md`.

O Selo não trava o Pampa da Espera. A Bíblia liga o Selo à liberação narrativa
do Pampa; isso fica para quando a progressão da Bíblia for adotada no grafo.

## Primeira Câmara — o primeiro vínculo

Depois de ouvir o altar (o que já existia), ele oferece o rito: escolher na
equipe o companheiro em quem você mais confia. O altar lê o vínculo pela
amizade — fio fino, oscila, firme, sem tremer — e pergunta se é esse o
**primeiro vínculo**. Dá para trocar depois, voltando ao altar. A pedra de
AUGUSTO ganha uma linha depois do rito.

**Em batalha** (`src/arauna_bond.c`): o primeiro vínculo com amizade 220 ou mais
segura com 1 HP o primeiro golpe que o derrubaria, **uma vez por batalha**, com
a mensagem "X held on for JOGADOR!". Usa o lugar da Focus Band no cálculo de
dano; se a Focus Band já segurou, ou Endure, ou há substituto, o vínculo não
gasta. O rito em si soma 20 de amizade. Fica de fora em batalha link, gravada,
Frontier, Trainer Hill, base secreta e e-Reader, onde as regras são
compartilhadas com quem nunca foi ao altar.

O vínculo é guardado pela *personalidade* da criatura (duas variáveis), então
acompanha a criatura no PC, com apelido novo ou depois de evoluir.

## Casa da Fogueira — S09 a S13

Encruzilhada Central (Mauville), no salão da roda. A roda de escuta V1 continua
igual e funciona antes, durante e depois.

| cena | quando | o que acontece | `VAR_ARAUNA_FOGUEIRA_STATE` |
|---|---|---|---:|
| S09 Noite de História | 7ª insígnia, falando com o guardião | Contar uma história: o uivo, o laço partido ou o próprio caminho. As duas primeiras mudam se você viveu o arco do Uivo ou fez o rito da Câmara. | 0 → 1 |
| S10 HORIZON | logo em seguida | BRENO e dois agentes entram para gravar tudo o que se disse na fogueira e levar ao LIVING ARCHIVE. "Ninguém aqui concordou." | 1 |
| S11 defesa | logo em seguida | A roda se levanta; entre as batalhas os moradores bloqueiam a porta do memorial e as crianças cantarolam por cima dos gravadores. Duas batalhas com agentes (nv41–42) e BRENO (nv42–43). Perder não apaga nada: o HORIZON continua no salão e o guardião pergunta se você fica com a roda (por construção; a derrota não foi jogada no emulador). | 1 → 2 |
| S12 presságio | ao fim da defesa | O fogo sobe até as vigas; uma forma de asas de fagulha olha cada rosto. Ainda é um presságio. | → 3 |
| S13 volta depois da Torre do Ruído | Hall da Fama **e** `FLAG_ARAUNA_TOWER_COMPLETE` | O guardião recebe você, reconta blocos do save, presencia Arauá e entrega SACRED ASH. A mochila cheia mantém o estado 3; a recompensa não repete. | → 4 |

A **Torre Juramento** continua resolvendo a crise de M'Boi entre a sétima e a
oitava insígnias. Ela não é a **Torre do Ruído** do roteiro, que contém o
Arquivo de Essência, contratos e Sifão-Mestre. A Torre do Ruído tem agora
cinco salas próprias e só é acessível depois do Hall da Fama, por Ciro na
entrada da Casa da Fogueira. Os eventos TR01–TR09 usam estado próprio,
sem alterar as variáveis de Sky Pillar ou M'Boi. Ver `ARCOS_V2_REVISAO.md`.

O guardião oferece a roda de escuta em todos os estados. Escolher NO nessa
oferta abre a conversa sobre a Noite de História ou sobre o retorno do arco.
O Aurora Ticket de Anahi passa a exigir a conclusão da Torre e o despertar
na Fogueira; tickets e recompensas já obtidos em saves antigos são mantidos.

Os três treinadores do HORIZON são novos e foram acrescentados no fim
(`TRAINER_ARAUNA_FOGUEIRA_AGENT_1`, `_AGENT_2`, `_ADMIN`, ids 855–857). BRENO é
o administrador que já existia no Arquivo Central (slot de Matt).

## O que foi alocado

Tudo acrescentado no fim ou tirado de espaço que o vanilla nunca usou. Nenhum
id existente mudou e o tamanho do save é o mesmo.

| o quê | ids |
|---|---|
| flags | `FLAG_ARAUNA_FIRST_LINK_MADE` 0x034, `FLAG_ARAUNA_UIVO_PUP_CAUGHT` 0x035, `FLAG_ARAUNA_UIVO_HIDE_PUP` 0x036, `FLAG_ARAUNA_UIVO_HIDE_NEIGHBOR` 0x037, `FLAG_ARAUNA_UIVO_HIDE_CIRCLE` 0x038, `FLAG_ARAUNA_FOGUEIRA_HIDE_HORIZON` 0x039 |
| variáveis | `VAR_ARAUNA_UIVO_STATE` 0x40F7, `VAR_ARAUNA_FOGUEIRA_STATE` 0x40F8, `VAR_ARAUNA_FIRST_LINK_LO/HI` 0x40F9–0x40FA |
| treinadores | 855–857 (`TRAINERS_COUNT` 858; o limite de flags é 864) |
| menus | `MULTI_ARAUNA_NOTEBOOKS` 115, `MULTI_ARAUNA_STORY_NIGHT` 116 |
| texto de batalha | `STRINGID_ARAUNABONDHELD` 381 |
| specials | `AraunaBond_ReadSelected`, `AraunaBond_MakeFirstLink`, `AraunaBond_FindFirstLink` (no fim da tabela) |
| campo de batalha | `araunaBondUsed`, `araunaBondMessage` no fim do `BattleStruct`, que é zerado a cada batalha |

As flags de esconder são recalculadas pelo estado do arco toda vez que o mapa
carrega, então um save antigo nunca vê um NPC de cena fora de hora.

## Como foi conferido

No mGBA, com a ROM de teste (o harness fica fora do repositório):

- Casa do Uivo, do começo ao fim: consentimento, relato e interrupção (estado
  2); ordem errada recusada e ordem certa aceita (3); pano (4); o uivo ao
  entrar no Refúgio; batalha com o Guaracim nv17, o pano acalma, ele volta para
  casa (5); captura com MASTER BALL (5, flag de captura); reconto, assinatura,
  SOOTHE BELL (8).
- Primeira Câmara: menu da equipe, leitura do vínculo, confirmação, as duas
  variáveis gravadas; o altar reconhece o vínculo na volta; a linha nova na
  pedra de AUGUSTO.
- Vínculo em batalha: um nv5 com amizade 255 contra a Nara — o golpe crítico
  que o derrubaria deixa 1 HP e aparece "Pimpau held on for A!"; no turno
  seguinte ele cai, porque é uma vez por batalha.
- Casa da Fogueira: Noite de História, entrada do HORIZON, as três batalhas,
  saída, ARAUÁ (estado 3); volta com a oitava insígnia e SACRED ASH (4); antes
  da sétima insígnia a roda V1 responde igual a antes.
- Build oficial e todos os gates do projeto passando; largura de texto dentro
  dos 208 px.

O comando antigo `validate_fogueira_roda_v1.py` agora redireciona ao
validador atual `validate_fogueira_arcos.py`. O teste histórico foi preservado
em `validate_fogueira_roda_v1_snapshot.py` e pode ser chamado com
`--legacy-v1`, somente num checkout/pacote V1 exato.

O validador atual interpreta os comandos do fonte e confere geometria,
visibilidade por estado, consentimento, derrota modelada, retomada,
capacidade da mochila e recompensas únicas. Não executa o engine ARM nem
certifica arte/timing em emulador. Os testes antigos de emulador descritos
acima pertencem à versão anterior; a aceitação visual desta alteração deve
ser registrada separadamente.

## O que continua pendente

- A cena sinalizada do Uivo, com tradução e revisão qualificadas.
- Arte própria da criança e assets de sinalização aprovados. Eremita e
  filhote já têm sprites próprios de caminhada; não são sinais em Libras.
- O "sistema de pânico" que o contrato menciona para U06–U09: aqui a batalha
  de acalmar é uma batalha selvagem comum com o desfecho narrado.
- A liberação do Pampa pelo Selo. A ordem Liga → Torre do Ruído → Fogueira
  já tem um fluxo próprio; os detalhes integrais dos eixos de Vínculo e dos
  finais do roteiro ainda não são os deste rascunho.
- Revisão do texto pelo autor.


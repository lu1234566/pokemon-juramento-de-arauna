# Roteiro de teste — AraunaMapLab

Este roteiro valida o laboratório técnico de M2. O terreno de Littleroot, o
TREECKO e alguns recursos visuais ainda são placeholders; o objetivo desta
etapa é provar mapas, eventos, localização, inventário, batalha e persistência.

## Preparação

1. Compile a ROM em português a partir de um commit limpo.
2. Inicie um save novo e conclua a cena da mudança para Littleroot.
3. Saia da casa do protagonista e fale com o homem próximo ao centro da vila.
4. Aceite entrar no mapa experimental.

## Fluxo principal

- [ ] O warp coloca o jogador no mapa com neblina e sem travar controles.
- [ ] A pesquisadora apresenta a área em português.
- [ ] Se a equipe estiver vazia, ela entrega um TREECKO de nível 5.
- [ ] Uma segunda conversa oferece retorno a Littleroot.
- [ ] Recusar o retorno mantém o jogador no laboratório.
- [ ] Aceitar o retorno posiciona o jogador ao lado do ponto de acesso.

## Item e flag

- [ ] A Poké Bola entrega uma POTION quando existe espaço na mochila.
- [ ] A Poké Bola desaparece depois da coleta.
- [ ] Sair e voltar não recria o item.
- [ ] Com o bolso cheio, o item permanece disponível para nova tentativa.

## Treinador

- [ ] Nilo recusa a batalha quando a equipe está vazia.
- [ ] Com um Pokémon, a batalha começa contra um Poochyena de nível 4.
- [ ] A vitória mostra a fala de derrota e a fala pós-batalha.
- [ ] Falar novamente não reinicia a primeira batalha.
- [ ] Perder a batalha não corrompe o save nem bloqueia o acesso ao mapa.

## Persistência e idioma

- [ ] Salvar e recarregar preserva item coletado, conversa e treinador vencido.
- [ ] O mesmo roteiro funciona na build inglesa.
- [ ] Nenhuma fala autoral mistura os dois idiomas.
- [ ] Nenhuma linha transborda ou fica cortada.

Registre commit, idioma, versão do mGBA, save novo ou migrado e capturas de
qualquer falha na issue de M2.

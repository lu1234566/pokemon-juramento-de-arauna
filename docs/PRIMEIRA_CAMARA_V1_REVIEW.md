# Primeira Câmara V1

A Primeira Câmara foi acrescentada como um desvio opcional da Rota 101. São dois mapas próprios: **chegada de 30×26** e **interior de 22×24**. A referência é a prancha enviada `01_Primeira_Camara_Primeiro_Elo.png`, nos três painéis, e a página 42 da Master Map Design Bible.

A chegada tem vegetação escura, espelhos d’água, ponte/escadaria de pedra, cascatas, guardiões e uma fachada com núcleo ciano. O interior reúne antecâmara, inscrições, duas estátuas, altar com elo partido e luz persistente. As imagens são renders dos metatiles realmente gravados; a iluminação e os detalhes ilustrados do concept foram adaptados à escala e paleta do GBA.

## Alcance e roteiro

O mapa e uma Rota da Neblina formal não existiam no código. A nova Trilha da Neblina ocupa um ramal de 16 células no setor nordeste da Rota 101. Ela conserva as duas conexões, os oito objetos, os nove gatilhos do prólogo e a placa anterior. A clareira, seus trajetos e o script recebido permanecem intactos; a nova placa e seu texto são acrescentados ao fim dos eventos/scripts.

| Estado | Resultado |
| --- | --- |
| Primeira interação com a porta | Registra a visita e mantém a passagem fechada |
| Visita registrada, conquistas incompletas | Informa que a passagem está selada |
| Visita registrada e duas conquistas | Abre a porta; a abertura persiste ao retornar |
| Escolha de não escutar o altar | Nenhuma mudança de estado, inventário ou recompensa |
| Escolha de escutar | Ativa a luz do elo; o estado persiste ao retornar |
| Nova interação após escutar | Texto de retorno, sem repetir a ativação |

As conquistas da Terra e da Maré correspondem aqui a **BADGE01 e BADGE02**, já preservadas nas respectivas adaptações visuais com Dalva e Ademar. A Câmara somente consulta essas flags. Três bits anteriormente livres (0x3D–0x3F) guardam porta vista, porta aberta e altar escutado, sem renumerar flags ou mudar o formato do save. As inscrições incluem Augusto e o princípio "O que nos liga, permanece".

Este pacote implementa cenário, acesso, porta e interação do altar. Não implementa um Sistema de Vínculos completo, evoluções narrativas, mudanças de atributos, capturas ou novas insígnias. As versões PT-BR e EN dos 13 blocos novos foram verificadas; o renderer de inglês substitui somente esses textos, seguindo o fluxo de tradução já usado no projeto.

## Integração

São **40 arquivos do jogo**. Os dois mapas e layouts são acrescentados ao final dos registros; todos os IDs anteriores permanecem iguais. O tileset secundário `AraunaPrimeiraCamara` contém 111 metatiles e 233 tiles gráficos de 8×8, dentro do orçamento de VRAM estática. Árvores, água e pedras conservam os quadrantes nativos copiados e usam paletas locais; o banco primário não muda.

O banco compartilhado de Amanhecer recebe somente **um metatile ao final**, que reutiliza a imagem da estrada e acrescenta o comportamento nativo de saída a leste. Nenhuma imagem, paleta ou entrada anterior desse banco muda. Os sprites, a paleta, o retrato e os registros de Dalva permanecem intactos.

Base local de revisão: **90c1a1b**, após Casa da Terra V1. Os arquivos de integração e o patch são identificados em `review/camara_v1_integration.json` e `review/camara_v1_from_review_base.patch`.

```bash
python3 tools/apply_camara_v1.py --target /caminho/do/projeto --check
python3 tools/apply_camara_v1.py --target /caminho/do/projeto
```

O aplicador preserva registros externos e guarda os arquivos anteriores. Não copie todo o ZIP sobre seu projeto: as outras fontes são dependências de revisão. Uma divergência nos arquivos de entrada ou nos novos mapas/assets é recusada antes da escrita.

## Verificação

- Oito warps recíprocos, nove novas interações de cenário e todas as áreas caminháveis foram conferidos nos quatro estados visuais.
- As 16 combinações da porta e quatro situações do altar foram executadas em um interpretador restrito dos comandos reais dos scripts, incluindo repetição, recusa e recarga do mapa.
- As funções C nativas de flags foram compiladas e testadas nos oito conjuntos dos três bits novos, preservando o bit vizinho. O teste também executou três direções de chegada, a troca de metatile sem perda de elevação e quatro verificações de alcance usando a função de elevação do engine.
- Esses testes usam fixtures controladas de save/mapa e não executam o engine inteiro.
- O conversor nativo `mapjson` gerou 17 arquivos de mapas, grupos, layouts e constantes. Doze recortes 240×160 cobrem os dois mapas.
- O teste do pacote recompõe os 40 arquivos do jogo e todas as imagens após extração, recompila os eventos e verifica aplicação, idempotência e conflitos antes da escrita.

Reprodução requer Python 3, Pillow, DejaVu Sans, `cc`, `g++` e `make`.

```bash
python3 tools/build_camara_v1.py
python3 tools/validate_camara_v1.py
python3 tools/probe_camara_v1_native.py
python3 tools/build_camara_v1_review.py
python3 scripts/render_primeira_camara_en_checked.py --check
python3 tools/check_camara_v1_package.py --archive /caminho/do/pacote.zip
```

Build completo da ROM e emulador permanecem pendentes. Não houve push, merge ou GitHub Actions.

A pedido do usuário, a próxima etapa é **Vila Amanhecer completa: exterior, casas e laboratório**, antes de retomar a ordem restante da Bible.

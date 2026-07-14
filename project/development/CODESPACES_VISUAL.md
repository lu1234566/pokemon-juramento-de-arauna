# Ambiente visual no Codespaces

Este ambiente permite editar mapas no Porymap e testar a ROM no mGBA diretamente pelo navegador do Chromebook. O Codespace executa um desktop Linux leve; o navegador mostra esse desktop por uma conexão noVNC privada.

## O que é instalado

| Componente | Origem fixada | Finalidade |
| --- | --- | --- |
| Ubuntu | Dev Container `ubuntu-24.04` | Base reproduzível do Codespace |
| Desktop | `desktop-lite:1`, noVNC `1.2.0` | Interface gráfica pelo navegador |
| Porymap | tag `6.3.1` oficial | Edição de mapas, eventos e conexões |
| mGBA | pacote `mgba-qt` do Ubuntu 24.04 | Teste da ROM gerada localmente |
| ARM GCC | pacotes do Ubuntu 24.04 | Compilação do projeto |

O Porymap é compilado em `~/.local/share/arauna-tools`, fora do repositório. ROMs, saves e outros arquivos proprietários continuam proibidos no Git.

## Primeira ativação

Depois de esta configuração chegar à `main`, abra o Codespace e execute **Codespaces: Rebuild Container** pela paleta de comandos. Também é possível criar um Codespace novo.

O processo automático instala os pacotes e compila o Porymap. Na primeira execução isso pode levar vários minutos. Se ele for interrompido, repita:

```bash
bash .devcontainer/setup-visual-tools.sh
```

Quando o terminal mostrar `Ambiente visual pronto`, abra a aba **Ports** do Codespace:

1. Localize a porta `6080`, chamada **Arauna — ambiente visual**.
2. Confirme que a visibilidade está como **Private**. Se não estiver, altere para **Private** antes de abrir.
3. Selecione **Open in Browser**.
4. Na tela do noVNC, selecione **Connect** e use a senha `vscode`.

O acesso privado do Codespaces exige autenticação no GitHub. A senha do noVNC é apenas a segunda barreira do desktop e não substitui a privacidade da porta. Nunca torne as portas `6080` ou `5901` públicas.

## Compilar e abrir as ferramentas

No terminal do Codespace, atualize a branch e gere a ROM desejada:

```bash
git switch main
git pull
make ARAUNA_LANGUAGE=PORTUGUESE -j$(nproc)
```

Para abrir somente o Porymap:

```bash
bash scripts/open_visual_tools.sh porymap
```

Na primeira abertura, escolha a pasta atual do repositório como projeto. Em um Codespace ela normalmente fica em `/workspaces/pokemon-juramento-de-arauna`. O Porymap altera os arquivos-fonte de mapas que podem ser revisados normalmente com `git diff`.

Para testar o build português no mGBA:

```bash
bash scripts/open_visual_tools.sh mgba pokeemerald-ptbr.gba
```

Para abrir as duas ferramentas de uma vez:

```bash
bash scripts/open_visual_tools.sh all pokeemerald-ptbr.gba
```

O build inglês usa o mesmo fluxo com `ARAUNA_LANGUAGE=ENGLISH` e `pokeemerald-en.gba`.

## Fluxo seguro de trabalho

1. Edite e salve o mapa no Porymap.
2. Confira somente as mudanças esperadas com `git status --short` e `git diff`.
3. Compile nos dois idiomas e teste a área no mGBA.
4. Execute `bash scripts/check_no_proprietary_files.sh`.
5. Faça commit e push apenas de código, dados de mapa, scripts e documentação.

Arquivos `.gba`, `.sav`, `.state`, patches, configurações locais do Porymap e a cópia compilada das ferramentas estão ignorados ou bloqueados. Não force a inclusão deles no Git.

## Persistência, custo e encerramento

- Os arquivos em `/workspaces` permanecem enquanto o Codespace existir, mas um Codespace não substitui o Git: faça commit e push antes de encerrar um marco de trabalho.
- As ferramentas instaladas fora do repositório podem ser recriadas pelo script após um rebuild; não precisam ser copiadas para o projeto.
- Um Codespace ativo consome a cota da conta. Ao terminar, pare-o pela página de Codespaces ou pelo comando **Codespaces: Stop Current Codespace**.
- Excluir um Codespace remove mudanças que nunca foram enviadas ao GitHub.

## Solução de problemas

Se um programa não aparecer, mantenha a página da porta `6080` aberta e rode novamente seu comando de abertura. Os logs ficam em:

```text
~/.cache/arauna-visual/porymap.log
~/.cache/arauna-visual/mgba.log
```

Verificações úteis:

```bash
echo "$DISPLAY"
command -v porymap
command -v mgba-qt
command -v arm-none-eabi-gcc
```

Se faltar alguma ferramenta, execute novamente `bash .devcontainer/setup-visual-tools.sh`. Se a porta `6080` não existir, reconstrua o container para que o recurso `desktop-lite` seja aplicado.

## Referências oficiais

- [Desktop Lite — Dev Container Features](https://github.com/devcontainers/features/tree/main/src/desktop-lite)
- [Porymap 6.3.1](https://github.com/huderlem/porymap/releases/tag/6.3.1)
- [Encaminhamento e privacidade de portas no Codespaces](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace)
- [mGBA](https://github.com/mgba-emu/mgba)

# Mata da Espera V1 — origem dos elementos gráficos

Gerados com a ferramenta integrada `image_gen.imagegen`, em geração direta,
com fundo transparente e sem imagem de referência. A imagem fonte permanece
em `source.png`. O compilador separa os quatro componentes, reduz em nearest
neighbor, quantiza para quinze cores GBA mais transparência e monta os tiles.

## Prompt utilizado

Create a clean game sprite asset sheet for a Brazilian Atlantic rainforest dungeon in a 2004 Game Boy Advance top-down RPG, Pokemon Emerald aesthetic. Transparent background. Crisp deliberate low resolution pixel art, orthographic top-down view with short south-facing visible trunks, no perspective/isometric angle. Limited palette: deep blue-green outlines, bottle green shade, moss-green foliage, small muted ochre leaf highlights, warm dark-brown roots. Four separate non-overlapping assets with generous transparent gutters: upper left one ancient buttress-root tree with a broad dense irregular canopy (logical sprite about 80 pixels wide by 96 pixels high); upper right one mossy fallen trunk with sinuous branching roots, horizontal (logical sprite about 64 by 32 pixels); lower left one dense fern and bromeliad cluster (32 by 32 logical pixels); lower right one tangled exposed root on the forest floor, horizontal (48 by 16 logical pixels). All four assets in exactly the same native pixel scale, with readable silhouette and low-color clusters like real GBA overworld tiles. Fully solid opaque interior pixels, transparent surrounding silhouette. No ground rectangle, no scenery, no player, no shadows outside silhouette, no text, no labels, no grid. The massive tree is the landmark; vines and buttress roots are visible underneath its canopy. Final artwork arranged on a square canvas with the large tree occupying most of its upper-left quadrant; use nearest-neighbor type sharpness, never painterly, no gradients, no anti-aliasing.

# Route110 double-battle freeze: Tuim form-sheet overflow

The normal campaign reached Route110 after the museum delivery. Walking north
from `(8,77)` started the two-trainer battle at `(8,76)`. Both opponents could
send out Tuim (`SPECIES_CASTFORM`, slot 385). The original ROM
`0cc8a741b0c5af840c45e21d362eccd7577dcead6c52d2af876f15ceb48e4d23`
could hang during the intro or a replacement send-out, sometimes showing a
black screen. This was reproduced from native SAVE/CONTINUE without fixtures,
teleports, injected calls, game RAM/ROM writes or forced outcomes.

## Cause and change

`AllocateMonSpritesGfx` reserves `0x2000` bytes per battler. Castform's form
animations address four single `0x800`-byte frames. Its concatenated animated
sheet had two frames per form, decompressing to `0x4000` bytes. Loading that
sheet into the fourth battler's buffer overwrote the following heap headers.
Later allocations followed corrupted pointers and could also damage interrupt
state; that was a downstream symptom of the buffer overflow.

`gMonFrontPic_Castform` now uses the existing combined still-front sheet. This
contains the four frames the form animation expects and fits `0x2000` bytes.
For all four forms, the still image is byte-for-byte identical in indexed pixel
data to the first frame of its installed animated PNG. No art file, palette,
animation command, trainer roster, map, layout or audio is edited. Ciro's
installed art is unchanged.

## Regression coverage

`test_castform_graphics.py` is a native allocation/loading fixture, kept
separate from the campaign journey. It checks the compiled front/back sizes,
compares every loaded form frame with the existing still-front pixel data,
loads all four battle slots, checks the heap block list after every load and
exercises allocation/free afterward. It rejects the original compiled sheet
because its decompressed length is `0x4000` instead of `0x2000`.

The test runs in the full native-runtime workflow. That workflow also triggers
when `src/anim_mon_front_pics.c` changes. Private native campaign saves are not
committed or uploaded in the public evidence artifact.

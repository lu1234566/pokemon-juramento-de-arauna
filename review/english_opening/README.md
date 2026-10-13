# Native English opening

The supplied `gba_assets (1).zip` is the English source; its SHA-256 is
`f5259711dea2f14249d2a5a1ee95d6f0c58ff339bb443a3b8587b748c708ca83`.
The two numbered 720x480 MP4s are identical. The unnumbered ZIP contains
Portuguese captions and is not used. Uploads remain unchanged.

The 44-second cinematic uses all 660 supplied 240x160 frames at 15 fps and
its supplied 13,379 Hz, 8-bit mono audio. Frame 631 supplies the title with
`PRESS START`; the game's proper name remains `POKÉMON JURAMENTO DE ARAUNA`.
A/Start/B/Select skips the movie, and A/Start enters the menu from the title.
The title's existing save/RTC/berry shortcuts and idle replay are retained.

GBA conversion uses 48 RGB555 colors per frame and at most eight colors
per 8x8 tile. Weighted color reduction within tiles is needed to fit the
32 MiB cartridge and changes some color detail. Captions and composition
are preserved. The frame data occupies 9,835,244 bytes; audio and title
are additional. Mode 4 pages flip at VBlank. The existing MP2K player plays
the one-shot PCM; video time uses its sample clock.

The decoder uses a dedicated 280-byte IWRAM buffer and a 19,800-byte
allocation from the existing heap. It borrows no subsystem buffers. The
heap allocation is freed before the title/menu and when playback ends.
Linker assertions enforce the existing RAM budgets and decoder copy size.

Rebuild the authored assets with Pillow, NumPy and a host C compiler:

```sh
python3 tools/arauna/build_opening_assets.py '/path/to/gba_assets (1).zip'
python3 tools/arauna/check_opening_assets.py
bash scripts/build_arauna.sh -j2 all
```

The asset validator checks all decoded frame hashes, palette/index bounds,
chunk checksums, audio format/checksum, source identity and the title.
ROMs, saves, states and native test harnesses are excluded from Git.

#include "global.h"
#include "arauna_opening.h"
#include "main.h"
#include "title_screen.h"
#include "palette.h"
#include "scanline_effect.h"
#include "task.h"
#include "sprite.h"
#include "gpu_regs.h"
#include "malloc.h"
#include "m4a.h"
#include "decompress.h"
#include "link.h"

#include "data/arauna_opening_en.h"

#define OPENING_PIXELS (DISPLAY_WIDTH * DISPLAY_HEIGHT)
#define OPENING_SCRATCH_BYTES (30 * 20 * 33)
#define OPENING_PAGE_BYTES 0xA000
#define OPENING_PAGE_BIT 0x10
#define OPENING_RATE 13379
#define OPENING_FPS 15

// Only bookkeeping is permanent RAM. The 19.4 KiB decode area uses the existing
// heap while the cinematic is active and is freed before the title/menu.
static EWRAM_DATA u8 *sOpeningScratch = NULL;
static EWRAM_DATA volatile u32 sOpeningSamples = 0;
static EWRAM_DATA volatile u16 sOpeningFrame = 0;
static EWRAM_DATA volatile u16 sPreparedFrame = 0;
static EWRAM_DATA volatile bool8 sFrameReady = FALSE;
static EWRAM_DATA volatile bool8 sOpeningSkipRequested = FALSE;
static EWRAM_DATA volatile u8 sOpeningPage = 0;

static const u8 ALIGNED(4) sOpeningWave[] = INCBIN_U8("sound/direct_sound_samples/arauna_opening_en.bin");
static const struct ToneData sOpeningVoice = {8, 60, 0, 0, (struct WaveData *)sOpeningWave, 255, 0, 255, 0};
// MP2K opcodes from sound/MPlayDef.s: KEYSH, TEMPO, VOICE, VOL, PAN,
// TIE Cn3 v127, followed by waits longer than the one-shot PCM waveform.
static const u8 sOpeningPart[] = {
    0xBC, 0, 0xBB, 75, 0xBD, 0, 0xBE, 127, 0xBF, 64, 0xCF, 60, 127,
    [13 ... 52] = 0xB0,
    [53] = 0xB1,
};
static const struct SongHeader sOpeningSong = {1, 0, 0, 0, (struct ToneData *)&sOpeningVoice, { (u8 *)sOpeningPart }};

static void ResetBitmapDisplay(void)
{
    SetVBlankCallback(NULL);
    SetHBlankCallback(NULL);
    ScanlineEffect_Stop();
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_FORCED_BLANK);
    REG_DISPCNT = DISPCNT_FORCED_BLANK;
    DmaFill16(3, 0, (void *)PLTT, PLTT_SIZE);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    SetGpuReg(REG_OFFSET_WIN0H, 0);
    SetGpuReg(REG_OFFSET_WIN0V, 0);
    SetGpuReg(REG_OFFSET_WIN1H, 0);
    SetGpuReg(REG_OFFSET_WIN1V, 0);
    SetGpuReg(REG_OFFSET_WININ, 0);
    SetGpuReg(REG_OFFSET_WINOUT, 0);
    SetGpuReg(REG_OFFSET_BG2PA, 0x100);
    SetGpuReg(REG_OFFSET_BG2PB, 0);
    SetGpuReg(REG_OFFSET_BG2PC, 0);
    SetGpuReg(REG_OFFSET_BG2PD, 0x100);
    SetGpuReg(REG_OFFSET_BG2X_L, 0);
    SetGpuReg(REG_OFFSET_BG2X_H, 0);
    SetGpuReg(REG_OFFSET_BG2Y_L, 0);
    SetGpuReg(REG_OFFSET_BG2Y_H, 0);
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
}

static void FreeOpeningScratch(void)
{
    if (sOpeningScratch != NULL)
    {
        Free(sOpeningScratch);
        sOpeningScratch = NULL;
    }
}

// A relocatable leaf decoder runs from a dedicated 328-byte IWRAM buffer.
// This avoids ROM fetch waits without borrowing another subsystem's memory.
static COMMON_DATA u32 sOpeningDecoder[82] = {0};
extern const u32 AraunaOpening_DecodeTiles[];
extern const u32 AraunaOpening_DecodeTilesEnd[];

static void RenderFrame(u16 frame, u8 page)
{
    void (*volatile decode)(const u8 *, vu16 *) = (void (*)(const u8 *, vu16 *))sOpeningDecoder;
    LZ77UnCompWram((const u32 *)(sOpeningFrames[frame] + ARAUNA_OPENING_PALETTE_BYTES), sOpeningScratch);
    decode(sOpeningScratch, (vu16 *)(VRAM + page * OPENING_PAGE_BYTES));
}

static void VBlankOpening(void)
{
    sOpeningSamples += gSoundInfo.pcmSamplesPerVBlank;
    if ((~REG_KEYINPUT) & (A_BUTTON | START_BUTTON | B_BUTTON | SELECT_BUTTON))
        sOpeningSkipRequested = TRUE;
    if (sFrameReady && (sOpeningSamples * OPENING_FPS) / OPENING_RATE >= sPreparedFrame)
    {
        sOpeningPage ^= 1;
        DmaCopy16(3, sOpeningFrames[sPreparedFrame], (void *)PLTT, ARAUNA_OPENING_PALETTE_BYTES);
        REG_DISPCNT = DISPCNT_MODE_4 | DISPCNT_BG2_ON | (sOpeningPage ? OPENING_PAGE_BIT : 0);
        sOpeningFrame = sPreparedFrame;
        sFrameReady = FALSE;
    }
}

static void EndOpening(void)
{
    SetVBlankCallback(NULL);
    m4aMPlayStop(&gMPlayInfo_BGM);
    FreeOpeningScratch();
    sFrameReady = FALSE;
    SetMainCallback2(CB2_InitTitleScreen);
}

static void CB2_PlayAraunaOpening(void)
{
    if (sOpeningSkipRequested || JOY_NEW(A_BUTTON | START_BUTTON | B_BUTTON | SELECT_BUTTON))
    {
        EndOpening();
        return;
    }
    if (sOpeningSamples >= ARAUNA_OPENING_AUDIO_SAMPLES && sOpeningFrame == ARAUNA_OPENING_FRAMES - 1)
    {
        EndOpening();
        return;
    }
    if (!sFrameReady && sOpeningFrame + 1 < ARAUNA_OPENING_FRAMES)
    {
        u16 next = sOpeningFrame + 1;
        RenderFrame(next, sOpeningPage ^ 1);
        sPreparedFrame = next;
        sFrameReady = TRUE;
    }
}

void CB2_InitAraunaOpening(void)
{
    ResetBitmapDisplay();
    m4aMPlayAllStop();
    ResetSerial();
    FreeOpeningScratch();
    sOpeningScratch = Alloc(OPENING_SCRATCH_BYTES);
    if (sOpeningScratch == NULL)
    {
        SetMainCallback2(CB2_InitTitleScreen);
        return;
    }
    CpuCopy32(AraunaOpening_DecodeTiles, sOpeningDecoder, (u8 *)AraunaOpening_DecodeTilesEnd - (u8 *)AraunaOpening_DecodeTiles);
    sOpeningSamples = 0;
    sOpeningSkipRequested = FALSE;
    sOpeningFrame = sPreparedFrame = 0;
    sOpeningPage = 0;
    sFrameReady = FALSE;
    RenderFrame(0, 0);
    DmaCopy16(3, sOpeningFrames[0], (void *)PLTT, ARAUNA_OPENING_PALETTE_BYTES);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_4 | DISPCNT_BG2_ON);
    SetVBlankCallback(VBlankOpening);
    MPlayStart(&gMPlayInfo_BGM, (struct SongHeader *)&sOpeningSong);
    SetMainCallback2(CB2_PlayAraunaOpening);
}

void AraunaOpening_LoadTitleGraphics(void)
{
    FreeOpeningScratch();
    ResetBitmapDisplay();
    LZ77UnCompVram((const u32 *)(sOpeningTitle + ARAUNA_OPENING_PALETTE_BYTES), (void *)VRAM);
    LoadPalette(sOpeningTitle, 0, ARAUNA_OPENING_PALETTE_BYTES);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_4 | DISPCNT_BG2_ON);
}

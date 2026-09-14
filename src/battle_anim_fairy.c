#include "global.h"
#include "battle_anim.h"
#include "battle_anim_internal.h"
#include "trig.h"
#include "constants/battle_anim.h"

static void AnimFairySpark(struct Sprite *sprite);
static void AnimFairySparkStep(struct Sprite *sprite);
static void AnimFairyWave(struct Sprite *sprite);
static void AnimFairyWaveStep(struct Sprite *sprite);
static void AnimFairyCrescent(struct Sprite *sprite);
static void AnimFairyCrescentStep(struct Sprite *sprite);
static void AnimFairyOathAttacker(struct Sprite *sprite);
static void AnimFairyOathTarget(struct Sprite *sprite);
static void AnimFairyAuraStep(struct Sprite *sprite);
static void AnimFairyEclipse(struct Sprite *sprite);
static void AnimFairyEclipseStep(struct Sprite *sprite);

static const union AnimCmd sAnim_FairySpark[] =
{
    ANIMCMD_FRAME(0, 4),
    ANIMCMD_FRAME(4, 4),
    ANIMCMD_FRAME(8, 4),
    ANIMCMD_FRAME(12, 4),
    ANIMCMD_JUMP(0),
};

static const union AnimCmd *const sAnims_FairySpark[] =
{
    sAnim_FairySpark,
};

static const union AnimCmd sAnim_FairyWave[] =
{
    ANIMCMD_FRAME(0, 4),
    ANIMCMD_FRAME(16, 4),
    ANIMCMD_FRAME(32, 4),
    ANIMCMD_JUMP(0),
};

static const union AnimCmd *const sAnims_FairyWave[] =
{
    sAnim_FairyWave,
};

static const union AnimCmd sAnim_FairyTwoFrame[] =
{
    ANIMCMD_FRAME(0, 6),
    ANIMCMD_FRAME(16, 6),
    ANIMCMD_JUMP(0),
};

static const union AnimCmd *const sAnims_FairyTwoFrame[] =
{
    sAnim_FairyTwoFrame,
};

const struct SpriteTemplate gFairySparkSpriteTemplate =
{
    .tileTag = ANIM_TAG_FAIRY_SPARK,
    .paletteTag = ANIM_TAG_FAIRY_SPARK,
    .oam = &gOamData_AffineOff_ObjNormal_16x16,
    .anims = sAnims_FairySpark,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = AnimFairySpark,
};

const struct SpriteTemplate gFairyWaveSpriteTemplate =
{
    .tileTag = ANIM_TAG_FAIRY_WAVE,
    .paletteTag = ANIM_TAG_FAIRY_WAVE,
    .oam = &gOamData_AffineOff_ObjNormal_32x32,
    .anims = sAnims_FairyWave,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = AnimFairyWave,
};

const struct SpriteTemplate gFairyCrescentSpriteTemplate =
{
    .tileTag = ANIM_TAG_FAIRY_CRESCENT,
    .paletteTag = ANIM_TAG_FAIRY_CRESCENT,
    .oam = &gOamData_AffineOff_ObjNormal_32x32,
    .anims = sAnims_FairyTwoFrame,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = AnimFairyCrescent,
};

const struct SpriteTemplate gFairyOathAttackerSpriteTemplate =
{
    .tileTag = ANIM_TAG_FAIRY_OATH,
    .paletteTag = ANIM_TAG_FAIRY_OATH,
    .oam = &gOamData_AffineOff_ObjNormal_32x32,
    .anims = sAnims_FairyTwoFrame,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = AnimFairyOathAttacker,
};

const struct SpriteTemplate gFairyOathTargetSpriteTemplate =
{
    .tileTag = ANIM_TAG_FAIRY_OATH,
    .paletteTag = ANIM_TAG_FAIRY_OATH,
    .oam = &gOamData_AffineOff_ObjNormal_32x32,
    .anims = sAnims_FairyTwoFrame,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = AnimFairyOathTarget,
};

const struct SpriteTemplate gFairyEclipseSpriteTemplate =
{
    .tileTag = ANIM_TAG_FAIRY_ECLIPSE,
    .paletteTag = ANIM_TAG_FAIRY_ECLIPSE,
    .oam = &gOamData_AffineOff_ObjNormal_32x32,
    .anims = sAnims_FairyTwoFrame,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = AnimFairyEclipse,
};

// args: x offset, y offset, lifetime, drift amplitude
static void AnimFairySpark(struct Sprite *sprite)
{
    InitSpritePosToAnimTarget(sprite, TRUE);
    sprite->data[0] = gBattleAnimArgs[2] > 0 ? gBattleAnimArgs[2] : 28;
    sprite->data[1] = 0;
    sprite->data[2] = gBattleAnimArgs[3] != 0 ? gBattleAnimArgs[3] : 3;
    sprite->callback = AnimFairySparkStep;
}

static void AnimFairySparkStep(struct Sprite *sprite)
{
    sprite->data[1]++;
    sprite->x2 = Sin((sprite->data[1] * 10) & 0xFF, sprite->data[2]);
    sprite->y2 = -(sprite->data[1] / 2);
    if (--sprite->data[0] <= 0)
        DestroyAnimSprite(sprite);
}

// args: attacker x/y offset, duration, target x/y offset
static void AnimFairyWave(struct Sprite *sprite)
{
    InitSpritePosToAnimAttacker(sprite, TRUE);
    sprite->data[0] = gBattleAnimArgs[2] > 0 ? gBattleAnimArgs[2] : 24;
    sprite->data[1] = sprite->x;
    sprite->data[2] = GetBattlerSpriteCoord(gBattleAnimTarget, BATTLER_COORD_X_2) + gBattleAnimArgs[3];
    sprite->data[3] = sprite->y;
    sprite->data[4] = GetBattlerSpriteCoord(gBattleAnimTarget, BATTLER_COORD_Y_PIC_OFFSET) + gBattleAnimArgs[4];
    InitAnimLinearTranslation(sprite);
    sprite->callback = AnimFairyWaveStep;
}

static void AnimFairyWaveStep(struct Sprite *sprite)
{
    if (AnimTranslateLinear(sprite))
        DestroyAnimSprite(sprite);
}

// args: x/y offset, lifetime
static void AnimFairyCrescent(struct Sprite *sprite)
{
    InitSpritePosToAnimTarget(sprite, TRUE);
    sprite->data[0] = gBattleAnimArgs[2] > 0 ? gBattleAnimArgs[2] : 42;
    sprite->data[1] = 0;
    sprite->callback = AnimFairyCrescentStep;
}

static void AnimFairyCrescentStep(struct Sprite *sprite)
{
    sprite->data[1] = (sprite->data[1] + 5) & 0xFF;
    sprite->y2 = Sin(sprite->data[1], 3);
    if (--sprite->data[0] <= 0)
        DestroyAnimSprite(sprite);
}

// args: x/y offset, lifetime
static void AnimFairyOathAttacker(struct Sprite *sprite)
{
    InitSpritePosToAnimAttacker(sprite, TRUE);
    sprite->data[0] = gBattleAnimArgs[2] > 0 ? gBattleAnimArgs[2] : 36;
    sprite->data[1] = 0;
    sprite->callback = AnimFairyAuraStep;
}

static void AnimFairyOathTarget(struct Sprite *sprite)
{
    InitSpritePosToAnimTarget(sprite, TRUE);
    sprite->data[0] = gBattleAnimArgs[2] > 0 ? gBattleAnimArgs[2] : 36;
    sprite->data[1] = 0;
    sprite->callback = AnimFairyAuraStep;
}

static void AnimFairyAuraStep(struct Sprite *sprite)
{
    sprite->data[1] = (sprite->data[1] + 8) & 0xFF;
    sprite->x2 = Sin(sprite->data[1], 2);
    sprite->y2 = Sin((sprite->data[1] + 64) & 0xFF, 2);
    if (--sprite->data[0] <= 0)
        DestroyAnimSprite(sprite);
}

// args: x/y offset, lifetime
static void AnimFairyEclipse(struct Sprite *sprite)
{
    InitSpritePosToAnimTarget(sprite, TRUE);
    sprite->data[0] = gBattleAnimArgs[2] > 0 ? gBattleAnimArgs[2] : 52;
    sprite->data[1] = 0;
    sprite->callback = AnimFairyEclipseStep;
}

static void AnimFairyEclipseStep(struct Sprite *sprite)
{
    sprite->data[1] = (sprite->data[1] + 4) & 0xFF;
    sprite->y2 = Sin(sprite->data[1], 2);
    if (--sprite->data[0] <= 0)
        DestroyAnimSprite(sprite);
}

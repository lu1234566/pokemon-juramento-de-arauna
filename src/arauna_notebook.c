#include "global.h"
#include "event_data.h"
#include "item_menu.h"
#include "item_use.h"
#include "string_util.h"
#include "text.h"
#include "config/arauna.h"
#include "constants/flags.h"
#include "constants/vars.h"

// Bond axes are packed into a single var so the save layout never grows:
// bits 0-4 Courage, bits 5-9 Wisdom, bits 10-14 Compassion (0-31 each).
#define BOND_AXIS_WIDTH  5
#define BOND_AXIS_MASK   0x1F

// Canonical qualitative feedback. The game never shows numbers (canon 8.1).
static const u8 sBond_Courage[] = _(
    "THE NOTEBOOK\n"
    "You tend to arrive before\l"
    "certainty.");

static const u8 sBond_Wisdom[] = _(
    "THE NOTEBOOK\n"
    "You look for the thread before\l"
    "pulling the knot.");

static const u8 sBond_Compassion[] = _(
    "THE NOTEBOOK\n"
    "You listen to those left inside\l"
    "the problem.");

static const u8 sBond_Plural[] = _(
    "THE NOTEBOOK\n"
    "You learned that no oath holds\l"
    "up with a single voice.");

static const u8 sNotebook_ChoosePartner[] = _(
    "CURRENT OBJECTIVE\n"
    "Care for all three guests.\p"
    "FIELD NOTES\n"
    "No entries yet.");

static const u8 sNotebook_MeetCiro[] = _(
    "CURRENT OBJECTIVE\n"
    "Meet CIRO in the plaza.\p"
    "FIELD NOTES\n"
    "Partner registered.");

static const u8 sNotebook_ExploreMist[] = _(
    "CURRENT OBJECTIVE\n"
    "Explore the east mist path.\p"
    "FIELD NOTES\n"
    "Find a record worth keeping.");

static const u8 sNotebook_ReturnToCiro[] = _(
    "CURRENT OBJECTIVE\n"
    "Return to CIRO in the plaza.\p"
    "FIELD NOTES\n"
    "A gray trail crossed the mist.");

static const u8 sNotebook_TravelCoastRoad[] = _(
    "CURRENT OBJECTIVE\n"
    "Follow the coast road to PORTO.\p"
    "TRAVEL RULE\n"
    "Roads are crossed on foot.");

static const u8 sNotebook_PortoBegin[] = _(
    "PORTO DAS REDES\n"
    "Four traces remain.\p"
    "OBJECTIVE\n"
    "Ask CELINA where to begin.");

static const u8 sNotebook_PortoMemorial[] = _(
    "PORTO DAS REDES\n"
    "Memorial testimony recorded.\p"
    "OBJECTIVE\n"
    "Find the discharge permit.");

static const u8 sNotebook_PortoPermit[] = _(
    "PORTO DAS REDES\n"
    "Permit and memorial recorded.\p"
    "OBJECTIVE\n"
    "Listen along the old docks.");

static const u8 sNotebook_PortoDock[] = _(
    "PORTO DAS REDES\n"
    "The dockworker's verse remains.\p"
    "OBJECTIVE\n"
    "Inspect CELINA's unfinished net.");

static const u8 sNotebook_PortoReady[] = _(
    "PORTO DAS REDES\n"
    "All four traces are recorded.\p"
    "OBJECTIVE\n"
    "Confront the CONSORTIUM agent.");

static const u8 sNotebook_PortoAfterAgent[] = _(
    "PORTO DAS REDES\n"
    "The agent's story broke apart.\p"
    "OBJECTIVE\n"
    "Return to CELINA and the water.");

static const u8 sNotebook_PortoTestimony[] = _(
    "TESTIMONIES\n"
    "IARA-MAE: RECORDED.\p"
    "OBJECTIVE\n"
    "Complete the TIDE VIGIL.");

static const u8 sNotebook_CollectBoard[] = _(
    "MARE BADGE: RECORDED.\p"
    "CURRENT OBJECTIVE\n"
    "Collect the TIDE BOARD from\n"
    "PORTO's boatbuilder.");

static const u8 sNotebook_Serra[] = _(
    "MARE BADGE: RECORDED.\n"
    "TIDE BOARD: READY.\p"
    "CURRENT OBJECTIVE\n"
    "Take the inland road toward\n"
    "SERRA DO UIVO.");

static const u8 sNotebook_SerraComplete[] = _(
    "MARE BADGE: RECORDED.\n"
    "UIVO BADGE: RECORDED.\p"
    "Two stories now answer\n"
    "the Starless Night.");

static const u8 sBoardReady[] = _(
    "TIDE BOARD\n"
    "Ready for calm water.\p"
    "Face a calm channel and press A.\n"
    "Strong currents remain unsafe.");

static const u8 sBoardNotAuthorized[] = _(
    "The TIDE BOARD is not yet\n"
    "authorized for field travel.");

static const u8 *GetAraunaNotebookPage(void)
{
    u16 storyStage = VarGet(VAR_ARAUNA_STORY_STAGE);

    if (FlagGet(FLAG_ARAUNA_BADGE_UIVO))
        return sNotebook_SerraComplete;
    if (FlagGet(FLAG_ARAUNA_BADGE_MARE) && !FlagGet(FLAG_ARAUNA_BOARD_RECEIVED))
        return sNotebook_CollectBoard;
    if (FlagGet(FLAG_ARAUNA_BADGE_MARE))
        return sNotebook_Serra;
    if (FlagGet(FLAG_ARAUNA_TESTIMONY_IARA_MAE))
        return sNotebook_PortoTestimony;
    if (FlagGet(FLAG_ARAUNA_PORTO_AGENT_DEFEATED))
        return sNotebook_PortoAfterAgent;
    if (FlagGet(FLAG_ARAUNA_PORTO_NET_FOUND)
     && FlagGet(FLAG_ARAUNA_PORTO_DOCK_SONG_HEARD)
     && FlagGet(FLAG_ARAUNA_PORTO_PERMIT_FOUND)
     && FlagGet(FLAG_ARAUNA_PORTO_MEMORIAL_HEARD))
        return sNotebook_PortoReady;
    if (FlagGet(FLAG_ARAUNA_PORTO_DOCK_SONG_HEARD))
        return sNotebook_PortoDock;
    if (FlagGet(FLAG_ARAUNA_PORTO_PERMIT_FOUND))
        return sNotebook_PortoPermit;
    if (FlagGet(FLAG_ARAUNA_PORTO_MEMORIAL_HEARD))
        return sNotebook_PortoMemorial;
    if (FlagGet(FLAG_ARAUNA_PORTO_ARRIVED))
        return sNotebook_PortoBegin;
    if (storyStage >= 8)
        return sNotebook_TravelCoastRoad;
    if (storyStage >= 6)
        return sNotebook_ReturnToCiro;
    if (storyStage >= 3)
        return sNotebook_ExploreMist;
    if (storyStage >= 2)
        return sNotebook_MeetCiro;

    return sNotebook_ChoosePartner;
}

static u8 GetBondAxis(u8 axis)
{
    return (VarGet(VAR_ARAUNA_BOND_AXES) >> (axis * BOND_AXIS_WIDTH)) & BOND_AXIS_MASK;
}

// 0 = no reading yet or a plural bond, 1 = Courage, 2 = Wisdom, 3 = Compassion.
// A tie between the leading axes is a valid outcome and reads as the plural bond.
u16 GetAraunaDominantBond(void)
{
    u8 courage = GetBondAxis(ARAUNA_BOND_AXIS_COURAGE);
    u8 wisdom = GetBondAxis(ARAUNA_BOND_AXIS_WISDOM);
    u8 compassion = GetBondAxis(ARAUNA_BOND_AXIS_COMPASSION);

    if (courage == 0 && wisdom == 0 && compassion == 0)
        return 0;
    if (courage > wisdom && courage > compassion)
        return 1;
    if (wisdom > courage && wisdom > compassion)
        return 2;
    if (compassion > courage && compassion > wisdom)
        return 3;

    return 0;
}

static const u8 *GetAraunaBondLine(void)
{
    switch (GetAraunaDominantBond())
    {
    case 1:  return sBond_Courage;
    case 2:  return sBond_Wisdom;
    case 3:  return sBond_Compassion;
    default: return sBond_Plural;
    }
}

void ItemUseOutOfBattle_AraunaNotebook(u8 taskId)
{
    const u8 *page = GetAraunaNotebookPage();

    // Once any bond has been recorded, the notebook closes with its qualitative reading.
    if (VarGet(VAR_ARAUNA_BOND_AXES) != 0)
    {
        u8 *end = StringCopy(gStringVar4, page);

        *end++ = CHAR_PROMPT_CLEAR;
        StringCopy(end, GetAraunaBondLine());
        page = gStringVar4;
    }

    DisplayItemMessage(taskId, FONT_NORMAL, page, CloseItemMessage);
}

void ItemUseOutOfBattle_AraunaBoard(u8 taskId)
{
    const u8 *text = FlagGet(FLAG_ARAUNA_BOARD_FIELD_UNLOCKED)
                   ? sBoardReady
                   : sBoardNotAuthorized;

    DisplayItemMessage(taskId, FONT_NORMAL, text, CloseItemMessage);
}

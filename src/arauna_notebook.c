#include "global.h"
#include "event_data.h"
#include "item_menu.h"
#include "item_use.h"
#include "text.h"
#include "constants/flags.h"
#include "constants/vars.h"

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

static const u8 sNotebook_Serra[] = _(
    "MARE BADGE: RECORDED.\p"
    "CURRENT OBJECTIVE\n"
    "Take the inland road toward\n"
    "SERRA DO UIVO.");

static const u8 sNotebook_SerraComplete[] = _(
    "MARE BADGE: RECORDED.\n"
    "UIVO BADGE: RECORDED.\p"
    "Two stories now answer\n"
    "the Starless Night.");

static const u8 *GetAraunaNotebookPage(void)
{
    u16 storyStage = VarGet(VAR_ARAUNA_STORY_STAGE);

    if (FlagGet(FLAG_ARAUNA_BADGE_UIVO))
        return sNotebook_SerraComplete;
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

void ItemUseOutOfBattle_AraunaNotebook(u8 taskId)
{
    DisplayItemMessage(taskId, FONT_NORMAL, GetAraunaNotebookPage(), CloseItemMessage);
}

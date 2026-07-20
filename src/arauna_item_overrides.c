#include "global.h"
#include "item.h"
#include "item_use.h"
#include "constants/items.h"

#undef GetItemName
#undef GetItemDescription
#undef GetItemFieldFunc

extern const u8 *GetItemName(enum Item itemId);
extern const u8 *GetItemDescription(enum Item itemId);
extern ItemUseFunc GetItemFieldFunc(enum Item itemId);

static const u8 sZilasNotebookName[] = _("Zila's Notebook");
static const u8 sZilasNotebookDescription[] = _(
    "Field notes that\n"
    "track objectives,\n"
    "Bonds and stories.");

const u8 *AraunaGetItemName(enum Item itemId)
{
    if (itemId == ITEM_FAME_CHECKER)
        return sZilasNotebookName;

    return GetItemName(itemId);
}

const u8 *AraunaGetItemDescription(enum Item itemId)
{
    if (itemId == ITEM_FAME_CHECKER)
        return sZilasNotebookDescription;

    return GetItemDescription(itemId);
}

ItemUseFunc AraunaGetItemFieldFunc(enum Item itemId)
{
    if (itemId == ITEM_FAME_CHECKER)
        return ItemUseOutOfBattle_AraunaNotebook;

    return GetItemFieldFunc(itemId);
}

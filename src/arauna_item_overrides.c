#include "global.h"
#include "item.h"
#include "item_use.h"
#include "string_util.h"
#include "constants/items.h"

#undef CopyItemName
#undef CopyItemNameHandlePlural
#undef GetItemName
#undef GetItemDescription
#undef GetItemFieldFunc

extern u8 *CopyItemName(enum Item itemId, u8 *dst);
extern u8 *CopyItemNameHandlePlural(enum Item itemId, u8 *dst, u32 quantity);
extern const u8 *GetItemName(enum Item itemId);
extern const u8 *GetItemDescription(enum Item itemId);
extern ItemUseFunc GetItemFieldFunc(enum Item itemId);

static const u8 sZilasNotebookName[] = _("Zila's Notebook");
static const u8 sZilasNotebookDescription[] = _(
    "Field notes that\n"
    "track objectives,\n"
    "Bonds and stories.");

u8 *AraunaCopyItemName(enum Item itemId, u8 *dst)
{
    if (itemId == ITEM_FAME_CHECKER)
        return StringCopy(dst, sZilasNotebookName);

    return CopyItemName(itemId, dst);
}

u8 *AraunaCopyItemNameHandlePlural(enum Item itemId, u8 *dst, u32 quantity)
{
    if (itemId == ITEM_FAME_CHECKER)
        return StringCopy(dst, sZilasNotebookName);

    return CopyItemNameHandlePlural(itemId, dst, quantity);
}

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

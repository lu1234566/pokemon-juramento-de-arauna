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

static const u8 sTideBoardName[] = _("Tide Board");
static const u8 sTideBoardDescription[] = _(
    "A folding board for\n"
    "crossing calm water\n"
    "without a field move.");

static const u8 *GetAraunaItemName(enum Item itemId)
{
    switch (itemId)
    {
    case ITEM_FAME_CHECKER:
        return sZilasNotebookName;
    case ITEM_DEVON_SCOPE:
        return sTideBoardName;
    default:
        return NULL;
    }
}

u8 *AraunaCopyItemName(enum Item itemId, u8 *dst)
{
    const u8 *name = GetAraunaItemName(itemId);

    if (name != NULL)
        return StringCopy(dst, name);

    return CopyItemName(itemId, dst);
}

u8 *AraunaCopyItemNameHandlePlural(enum Item itemId, u8 *dst, u32 quantity)
{
    const u8 *name = GetAraunaItemName(itemId);

    if (name != NULL)
        return StringCopy(dst, name);

    return CopyItemNameHandlePlural(itemId, dst, quantity);
}

const u8 *AraunaGetItemName(enum Item itemId)
{
    const u8 *name = GetAraunaItemName(itemId);

    if (name != NULL)
        return name;

    return GetItemName(itemId);
}

const u8 *AraunaGetItemDescription(enum Item itemId)
{
    switch (itemId)
    {
    case ITEM_FAME_CHECKER:
        return sZilasNotebookDescription;
    case ITEM_DEVON_SCOPE:
        return sTideBoardDescription;
    default:
        return GetItemDescription(itemId);
    }
}

ItemUseFunc AraunaGetItemFieldFunc(enum Item itemId)
{
    switch (itemId)
    {
    case ITEM_FAME_CHECKER:
        return ItemUseOutOfBattle_AraunaNotebook;
    case ITEM_DEVON_SCOPE:
        return ItemUseOutOfBattle_AraunaBoard;
    default:
        return GetItemFieldFunc(itemId);
    }
}

"""Bounded, normal-menu preparation for the continuing campaign journey."""
from campaign_controller import *


def lead(slot):
    """Reorder through Pokemon > SWITCH, waiting for each real UI state."""
    wanted = party()[slot]['personality']
    start_action(1)
    for _ in range(30):
        if active_task('Task_HandleSelectionMenuInput') is not None:
            break
        choose_party(slot)
    else:
        raise RuntimeError('Party context menu did not open')
    internal = read('sPartyMenuInternal')
    actions = [read(internal + 15 + i, 1) for i in range(read(internal + 23, 1))]
    target = actions.index(1)  # MENU_SWITCH
    act(0, 1, 30)
    task = active_task('Task_HandleSelectionMenuInput')
    for _ in range(12):
        if read(SYMS['gTasks'] + 40 * task + 8, 2) == target:
            break
        act(128, 2, 25)
    act(1, 2, 35)
    for _ in range(30):
        if party()[0]['personality'] == wanted:
            break
        if active_task('Task_HandleChooseMonInput') is not None:
            # SWITCH moves slotId2; slotId stays on the source Pokemon.
            act(1 if read(SYMS['gPartyMenu'] + 10, 1) == 0 else 32, 2, 30)
        else:
            act(0, 1, 30)
    else:
        raise RuntimeError('Party SWITCH did not complete')
    act(0, 1, 120)
    for _ in range(20):
        if overworld() and not read('sLockFieldControls', 1):
            return
        act(2, 2, 40)
    raise RuntimeError('Party menu did not close')


def teach_lineage(slot, move, replace_slot):
    """Use ARAUNA > LINEAGE, including the real move-forgetting screen."""
    return _teach_from_menu(slot, move, replace_slot, 2)


def teach_remember(slot, move, replace_slot):
    """Use ARAUNA > REMEMBER for moves in the actual current learnset."""
    return _teach_from_menu(slot, move, replace_slot, 1)


def _teach_from_menu(slot, move, replace_slot, menu_choice):
    move = constant(move) if isinstance(move, str) else move
    assert move not in party()[slot]['moves']
    initial_moves = party()[slot]['moves']
    expected_slot = initial_moves.index(0) if 0 in initial_moves else replace_slot
    start_action(4)
    for _ in range(100):
        if active_task('Task_HandleMultichoiceInput') is not None:
            break
        act(1, 2, 25)
    else:
        raise RuntimeError('ARAUNA menu did not open')
    act(0, 1, 25)
    for _ in range(menu_choice):
        act(128, 2, 25)
    act(1, 2, 60)
    for _ in range(160):
        if active_task('Task_HandleChooseMonInput') is not None:
            choose_party(slot)
        elif read(SYMS['gMain'] + 4) == SYMS['CB2_MoveRelearnerMain'] | 1:
            if read(read('sMoveRelearnerStruct'), 1) in (4, 6):
                break
            act(1, 2, 25)
        else:
            act(1, 2, 25)
    else:
        raise RuntimeError('Move list did not open')
    # The actual C struct starts its aligned u16 array after 17 u8s.
    choices = [read(read('sMoveRelearnerStruct') + 18 + 2 * i, 2) for i in range(25)]
    assert move in choices, ('move not offered by menu', menu_choice, move, choices)
    for _ in range(choices.index(move)):
        act(128, 2, 25)
    act(1, 2, 25)
    replaced = False
    for _ in range(400):
        if active_task('Task_HandleReplaceMoveInput') is not None and not replaced:
            act(0, 1, 50)
            for _ in range(replace_slot):
                act(128, 2, 25)
            act(1, 2, 80)
            replaced = True
        elif move in party()[slot]['moves'] and active_task('Task_HandleChooseMonInput') is not None:
            break
        elif overworld() and not read('sLockFieldControls', 1):
            break
        else:
            act(1, 2, 25)
    else:
        raise RuntimeError('Move teaching did not finish')
    for _ in range(160):
        if overworld() and not read('sLockFieldControls', 1):
            assert party()[slot]['moves'][expected_slot] == move
            return
        act(2 if active_task('Task_HandleChooseMonInput') is not None or active_task('Task_HandleMultichoiceInput') is not None else 1, 2, 25)
    raise RuntimeError('Move menu did not return to the field')

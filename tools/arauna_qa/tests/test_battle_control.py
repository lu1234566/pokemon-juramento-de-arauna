import unittest
from dataclasses import replace

from arauna_qa.battle_control import (
    BattleInputController,
    BattlePromptState,
    CONTROLLER_CHOOSEACTION,
    CONTROLLER_CHOOSEMOVE,
)


def prompt(command=CONTROLLER_CHOOSEACTION, action=3, move=0, double=False):
    return BattlePromptState(
        battler=0,
        side="player",
        controller_active=True,
        command=command,
        action_cursor=action,
        move_cursor=move,
        is_double_prompt=double,
        no_pp_number=False,
        target_cursor=0xFF,
    )


class FakeMenu:
    def __init__(self, value):
        self.value = value

    def player_prompt(self):
        return self.value


class FakeBridge:
    def __init__(self, menu, submit=True):
        self.menu = menu
        self.inputs = []
        self.submit = submit

    def press(self, key, frames=1):
        self.inputs.append(key)
        p = self.menu.value
        if p is None:
            return
        if p.command == CONTROLLER_CHOOSEACTION:
            if key == "LEFT" and p.action_cursor & 1:
                self.menu.value = replace(p, action_cursor=p.action_cursor ^ 1)
            elif key == "UP" and p.action_cursor & 2:
                self.menu.value = replace(p, action_cursor=p.action_cursor ^ 2)
            elif key == "A" and p.action_cursor == 0:
                self.menu.value = replace(p, command=CONTROLLER_CHOOSEMOVE, is_double_prompt=False)
        elif p.command == CONTROLLER_CHOOSEMOVE:
            if key == "RIGHT" and not (p.move_cursor & 1):
                self.menu.value = replace(p, move_cursor=p.move_cursor ^ 1)
            elif key == "LEFT" and p.move_cursor & 1:
                self.menu.value = replace(p, move_cursor=p.move_cursor ^ 1)
            elif key == "DOWN" and not (p.move_cursor & 2):
                self.menu.value = replace(p, move_cursor=p.move_cursor ^ 2)
            elif key == "UP" and p.move_cursor & 2:
                self.menu.value = replace(p, move_cursor=p.move_cursor ^ 2)
            elif key == "A" and self.submit:
                self.menu.value = None


class BattleInputTests(unittest.TestCase):
    def test_verified_action_and_move_cursor_path_submits(self):
        menu = FakeMenu(prompt())
        bridge = FakeBridge(menu)
        controller = BattleInputController(bridge, menu, max_polls=2)
        result = controller.choose_move(3)
        self.assertTrue(result.success)
        self.assertEqual(result.reason, "move_submitted")
        self.assertEqual(bridge.inputs, ["LEFT", "UP", "A", "RIGHT", "DOWN", "A"])

    def test_rejects_double_battle_prompt(self):
        menu = FakeMenu(prompt(command=CONTROLLER_CHOOSEMOVE, action=0, move=0, double=True))
        bridge = FakeBridge(menu)
        result = BattleInputController(bridge, menu).choose_move(0)
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "double_battle_not_supported")
        self.assertEqual(bridge.inputs, [])

    def test_does_not_guess_target_when_submission_remains_active(self):
        menu = FakeMenu(prompt(command=CONTROLLER_CHOOSEMOVE, action=0, move=0))
        bridge = FakeBridge(menu, submit=False)
        result = BattleInputController(bridge, menu, max_polls=2).choose_move(0)
        self.assertFalse(result.success)
        self.assertEqual(result.reason, "target_selection_or_unconfirmed_submission")
        self.assertEqual(bridge.inputs, ["A"])


if __name__ == "__main__":
    unittest.main()

import unittest
import pygame as pg
pg.font.init()
from Monopoly.Board import Dice
from unittest.mock import patch, Mock

import unittest
from unittest.mock import patch, Mock
import importlib

dice_module = importlib.import_module("Monopoly.Board")

Dice = dice_module.Dice
class TestDice(unittest.TestCase):
    def test_roll_returns_expected_values(self):
        dummy_screen = pg.Surface((800, 600))
        dummy_event = Mock()
        dummy_event.type = 0

        with patch.object(dice_module.pg.mouse, "get_pos", return_value=(0, 0)), \
             patch.object(dice_module.pg.event, "get", return_value=[dummy_event]), \
             patch.object(dice_module.pg.display, "flip", return_value=None), \
             patch.object(dice_module.pg.display, "update", return_value=None), \
             patch.object(dice_module, "display_message", return_value=None), \
             patch.object(dice_module.random, "randint", side_effect=[6, 5]), \
             patch.object(dice_module.pg, "quit", return_value=None):
            
            dice = Dice()
            dice.button.is_clicked = lambda event: True

            result = dice.roll(dummy_screen)
            self.assertEqual(result, (6, 5), "Rolling wrong")


if __name__ == "__main__":
    unittest.main()
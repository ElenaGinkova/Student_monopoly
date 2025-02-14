from unittest.mock import patch, Mock, MagicMock
from Monopoly.Game import Game, get_textbox_info, active_box_i
import unittest
import pygame as pg
from Monopoly.Characters.Tutor import Tutor
from Monopoly.Board import Board, Dice

class TestTutorPower(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.game = Game()
        self.game.board = Board()
        self.game.dice = Dice()
        self.game.screen = pg.Surface((1500, 700))
        self.game.font = pg.font.Font(None, 32)
        self.tutor = Tutor("Tutor")
        self.dummy = Tutor("Dummy")
        self.game.players = [self.tutor, self.dummy]
        self.game.player = self.tutor

    @patch('Monopoly.Characters.Tutor.decision_menu', return_value="Екстра")
    def test_tutor_power(self, mock_decision_menu):
        self.dummy.change_life = MagicMock()
        self.tutor.power(self.game)
        self.dummy.change_life.assert_called_once_with(-5, self.game)
        self.tutor.use_power.assert_called_once()
        self.assertTrue(self.turor.used_power)
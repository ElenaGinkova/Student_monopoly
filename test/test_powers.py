from unittest.mock import patch, Mock, MagicMock
from Monopoly.Game import Game, get_textbox_info, active_box_i
import unittest
import pygame as pg
from Monopoly.Characters.Tutor import Tutor
from Monopoly.Board import Board, Dice, FIELD_COUNT
from Monopoly.Characters.TicketChecker import TicketChecker
from Monopoly.Characters.Librarian import Librarian
from Monopoly.Characters.Roommate import Roommate
from Monopoly.Characters.CleaningLady import CleaningLady


class TestTutorPower(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.game = Game()
        self.game.board = Board()
        self.game.dice = Dice()
        self.game.background = pg.Surface((1100, 600))
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
        self.assertTrue(self.tutor.used_power)


class TestTicketCheckerPower(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.game = Game()
        self.game.board = Board()
        self.game.dice = Dice()
        self.game.background = pg.Surface((1100, 600))
        self.game.screen = pg.Surface((1500, 700))
        self.game.font = pg.font.Font(None, 32)
        self.tc = TicketChecker("TicketChecker")
        self.dummy = TicketChecker("Dummy")
        self.game.players = [self.tc, self.dummy]
        self.game.player = self.tc

    @patch('Monopoly.Characters.TicketChecker.choose_between_players')
    def test_ticket_checker_power(self, mock_choose):
        mock_choose.return_value = self.dummy
        old_money = self.dummy.get_money()
        self.tc.power(self.game)
        self.assertEqual(old_money - 50, self.dummy.get_money())


class TestLibrarianPower(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.game = Game()
        self.game.board = Board()
        self.game.dice = Dice()
        self.game.background = pg.Surface((1100, 600))
        self.game.screen = pg.Surface((1500, 700))
        self.game.font = pg.font.Font(None, 32)
        self.libr = Librarian("Libr")
        self.dummy = Librarian("Dummy")
        self.game.players = [self.libr, self.dummy]
        self.game.player = self.libr

    @patch('Monopoly.Characters.Librarian.visualise')
    @patch('Monopoly.Characters.Librarian.display_message')
    @patch('Monopoly.Characters.Librarian.take_turn', return_value=6)
    def test_librarian_power_success(self, mock_take_turn, mock_display_message, mock_visualise):
        with patch('Monopoly.Characters.Librarian.choose_between_players', return_value=self.dummy) as mock_choose:
            self.libr.power(self.game)
            self.assertEqual(self.dummy.cooldown, 1)

    @patch('Monopoly.Characters.Librarian.visualise')
    @patch('Monopoly.Characters.Librarian.display_message')
    @patch('Monopoly.Characters.Librarian.take_turn', return_value=3)
    def test_librarian_power_failure(self, mock_take_turn, mock_display_message, mock_visualise):
        with patch('Monopoly.Characters.Librarian.choose_between_players', return_value=self.dummy) as mock_choose:
            self.dummy.cooldown = 0
            self.libr.power(self.game)
            self.assertEqual(self.dummy.cooldown, 0)



class TestRoommatePower(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.game = Game()
        self.game.board = Board()
        self.game.dice = Dice()
        self.game.background = pg.Surface((1100, 600))
        self.game.screen = pg.Surface((1500, 700))
        self.game.font = pg.font.Font(None, 32)
        self.room = Roommate("Room")
        self.dummy = Roommate("Dummy")
        self.game.players = [self.room, self.dummy]
        self.game.player = self.room

    @patch('Monopoly.Characters.Roommate.choose_between_players')
    def test_roommate_power(self, mock_choose):
        mock_choose.return_value = self.dummy
        old_room_pos = self.room.get_pos_indx()
        old_dumm_pos = self.dummy.get_pos_indx()
        self.room.power(self.game)
        self.assertEqual(old_room_pos, self.dummy.get_pos_indx())
        self.assertEqual(old_dumm_pos, self.room.get_pos_indx())


class TestCleaningLadyPower(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.game = Game()
        self.game.board = Board()
        self.game.dice = Dice()
        self.game.background = pg.Surface((1100, 600))
        self.game.screen = pg.Surface((1500, 700))
        self.game.font = pg.font.Font(None, 32)
        self.cleaning = CleaningLady("Cleaner")
        self.dummy = CleaningLady("Dummy")
        self.game.player = self.cleaning
        self.game.players = [self.cleaning, self.dummy]

    def test_cleaninglady_power_forward(self):
        old_pos = self.dummy.get_pos_indx()
        with patch('Monopoly.Characters.CleaningLady.decision_menu', return_value="Напред") as mock_decision, \
             patch('Monopoly.Characters.CleaningLady.choose_between_players', return_value=self.dummy) as mock_choose:
            self.cleaning.power(self.game)
        self.assertEqual((old_pos + 1) % FIELD_COUNT, self.dummy.get_pos_indx())

    def test_cleaninglady_power_backward(self):
        old_pos = self.dummy.get_pos_indx()
        with patch('Monopoly.Characters.CleaningLady.decision_menu', return_value="Назад") as mock_decision, \
             patch('Monopoly.Characters.CleaningLady.choose_between_players', return_value=self.dummy) as mock_choose:
            self.cleaning.power(self.game)
        new_pos = old_pos - 1
        if new_pos < 0:
            new_pos += FIELD_COUNT
        self.assertEqual(new_pos, self.dummy.get_pos_indx())

if __name__ == "__main__":
    unittest.main()
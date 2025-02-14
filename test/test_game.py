import os
import sys
import unittest
from collections import OrderedDict
from unittest.mock import patch, Mock, MagicMock
from Monopoly.Board import FIELD_COUNT
from Monopoly.Board import Dice, Board
from Monopoly.Characters.GirlsMagnet import GirlsMagnet
import pygame as pg
from Monopoly.Game import Game, get_textbox_info, active_box_i
from Monopoly.Players import Player


pg.font.init()


class TestPreGameMethods(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("Player1", "Monopoly/assets/character0.png")
        self.player2 = Player("Player2", "Monopoly/assets/character1.png")
        self.game = Game([self.player1, self.player2])
        self.game.player = self.player1
    
    def test_get_players(self):
        players = self.game.get_players()
        self.assertEqual(players, [self.player1, self.player2])
    
    def test_remove_player(self):
        self.game.remove_player(self.player1)
        self.assertNotIn(self.player1, self.game.get_players())
    
    def test_are_filled(self):
        box1 = [pg.Rect(0, 0, 100, 50), "Player1", False]
        box2 = [pg.Rect(0, 60, 100, 50), "Player2", False]
        input_boxes = [box1, box2]

        self.assertTrue(self.game.are_filled(input_boxes))

        box2[1] = ""
        self.assertFalse(self.game.are_filled(input_boxes))
    
    def test_is_valid_count(self):
        box = [pg.Rect(0, 0, 100, 50), "5", False]
        self.assertTrue(self.game.is_valid_count(box))

        box[1] = "10"
        self.assertFalse(self.game.is_valid_count(box))

        box[1] = "a"
        self.assertFalse(self.game.is_valid_count(box))
    
    def test_renumerate(self):
        selected = OrderedDict()
        selected[1] = 1
        selected[2] = 2
        self.game.renumerate(selected, 1)

        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[2], 1)
    
    def test_get_textbox_info(self):
        input_box = [pg.Rect(0, 0, 100, 50), "Test", False]

        event = pg.event.Event(pg.KEYDOWN, key = pg.K_a, unicode="A")
        get_textbox_info([input_box], event, 0)
        self.assertEqual(input_box[1], "TestA")

        event = pg.event.Event(pg.KEYDOWN, key = pg.K_BACKSPACE)
        get_textbox_info([input_box], event, 0)
        self.assertEqual(input_box[1], "Test")
    
    def test_active_box_i(self):
        rect1 = pg.Rect(10, 10, 100, 50)
        rect2 = pg.Rect(200, 10, 100, 50)
        input_boxes = [[rect1, "Box1", False], [rect2, "Box2", False]]
        event = pg.event.Event(pg.MOUSEBUTTONDOWN, pos = (210, 20)) # clicked inside the box
        index = active_box_i(event, input_boxes)
        self.assertEqual(index, 1)

        event = pg.event.Event(pg.MOUSEBUTTONDOWN, pos = (500, 500)) # clicked nowhere inside the boxes
        index = active_box_i(event, input_boxes)
        self.assertEqual(index, -1)

class TestGameTurn(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.screen = pg.Surface((1500, 700))
        self.game.background = pg.Surface((1100, 600))
        self.game.board.move = MagicMock()
        dummy_field = MagicMock()
        dummy_field.action = MagicMock()
        self.game.board.get_field_from_indx = MagicMock(return_value=dummy_field)

    @patch('Monopoly.Board.Dice.roll', return_value=(1, 2))
    @patch('Monopoly.Visualisations.decision_menu', return_value="Край на хода")
    def test_take_turn(self, mock_decision_menu, mock_dice_roll):
        player = Player("Player", "Monopoly/assets/character0.png")
        player.reset_power = MagicMock()
        player.get_power_name = MagicMock(return_value="Mocked Power")
        with patch.object(self.game, 'handle_menu', return_value = False) as mock_handle_menu:
            with patch('Monopoly.Board.Dice.roll', return_value=(1, 2)):
                self.game.take_turn(player)
              
                mock_handle_menu.assert_called()
                player.reset_power.assert_called()

class TestHandleMenuMysteryShot(unittest.TestCase):

    def setUp(self):
        pg.init()
        self.game = Game()
        self.game.screen = pg.Surface((1500, 700))
        self.game.background = pg.Surface((1100, 600))
        self.game.board = Board()
        self.game.font = pg.font.Font(None, 32)
        self.game.dice = Dice()
        self.game.player = GirlsMagnet("player1")
        self.game.players = [self.game.player, GirlsMagnet("player2")]

    @patch('Monopoly.Game.decision_menu', return_value="Край на хода")
    def test_handle_menu_end_turn(self,mocked):
        result = self.game.handle_menu()
        self.assertFalse(result)
    
    @patch('Monopoly.Game.decision_menu', side_effect=["Mystery shot", "player2", "Добре", "Край на хода"])
    def test_handle_menu_mystery_shot_with_shots_success(self, mock_decision_menu):
        prev_life = self.game.players[1].get_life()
        prev_mist_shots = self.game.players[0].mystery_shots
        result = self.game.handle_menu()
        self.assertFalse(result)
        self.assertEqual(prev_life - 10, self.game.players[1].get_life())
        self.assertEqual(self.game.players[0].mystery_shots, prev_mist_shots - 1)
        self.assertEqual(mock_decision_menu.call_count, 4)

class TestGameWin(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.screen = MagicMock()

    @patch('Monopoly.Game.Game.select_characters')
    @patch('Monopoly.Game.Game.get_names')
    @patch('Monopoly.Game.Game.choose_count')
    @patch('Monopoly.Game.decision_menu')
    def test_play_victory(self, mock_decision_menu, mock_choose_count, mock_get_names, mock_select_characters):
        mock_choose_count.return_value = 2
        mock_get_names.return_value = [("dummy", "player1", False), ("dummy", "player2", False)]
        
        def fake_select_characters(names):
            self.game.players = [GirlsMagnet("player1"), GirlsMagnet("player2")]
        mock_select_characters.side_effect = fake_select_characters

        mock_decision_menu.side_effect = ["Йее", "Не"]

        def fake_take_turn(player):
            if player.get_name() == "player1":
                for p in self.game.players:
                    if p.get_name() == "player2":
                        self.game.eliminate(p)
        self.game.take_turn = fake_take_turn

        with self.assertRaises(SystemExit):
            self.game.play()


class TestHandleMenuPower(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.game = Game()
        self.game.screen = pg.Surface((1500, 700))
        self.game.font = pg.font.Font(None, 32)
        self.game.board = Board()
        self.game.dice = Dice()
        self.game.background = pg.Surface((1100, 600))
        self.player1 = GirlsMagnet("player1")
        self.player2 = GirlsMagnet("player2")
        self.game.player = self.player1
        self.game.players = [self.player1, self.player2]

    @patch('Monopoly.Characters.GirlsMagnet.choose_between_players')
    @patch('Monopoly.Game.decision_menu', side_effect=["Разсеяй играч", "Край на хода"])
    def test_handle_menu_power_actual(self, mock_decision_menu, mock_choose_between_players):
        mock_choose_between_players.return_value = self.player2

        result = self.game.handle_menu()

        self.assertFalse(result)
        self.assertEqual(self.player2.cooldown, 1)
        self.assertEqual(mock_decision_menu.call_count, 2)





if __name__ == "__main__":
    unittest.main()
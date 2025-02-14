import sys
import os
import unittest
from unittest.mock import Mock
import pygame as pg
from Monopoly.Board import Board, FIELD_COUNT, GO_MONEY, JAIL_INDX
from Monopoly.Players import Player
from Monopoly.Game import Game
from Monopoly.Board import Dice
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

pg.font.init()


class TestBoardWithRealPlayerAndGame(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.screen = pg.display.set_mode((800, 600))
        pl1 = Player("Player1", "Monopoly/assets/character0.png")
        pl2 = Player("Player2", "Monopoly/assets/character1.png")
        self.game = Game([pl1, pl2])
        self.game.background = pg.Surface((1100, 600))
        self.game.dice = Dice()
        self.game.player = pl1

    def test_move_normal(self):
        pos_index = self.game.player.get_pos_indx()
        steps = 4
        expected_index = (pos_index + steps) % FIELD_COUNT
        
        self.board.move(self.game.player, steps, self.screen, self.game)
        
        self.assertEqual(self.game.player.get_pos_indx(), expected_index)

    def test_go_to_jail(self):
        self.board.go_to_jail(self.game.player, self.screen, self.game)
        self.assertEqual(self.game.player.get_pos_indx(), JAIL_INDX, "Not indicating in jail")
        self.assertTrue(self.game.player.is_in_jail, "Not indicating in jail")

    def test_move_reverse(self):
        self.game.player = Player("Player1", "Monopoly/assets/character0.png")
        pos_indx = 10
        self.board.move(self.game.player, pos_indx, self.screen, self.game)
        self.game.player.reverse_move()

        steps = 11
        new_index =  pos_indx - steps
        if new_index < 0:
            new_index += FIELD_COUNT
        old_money = self.game.get_player().get_money()
        self.board.move(self.game.player, steps, self.screen, self.game)
        self.assertFalse(self.game.player.reverse_moving)
        self.assertIs(self.game.player.get_pos_indx(), new_index)
        recieved_money = self.game.get_player().get_money() - old_money

        if new_index > pos_indx and new_index != 0:
            self.assertEqual(recieved_money, GO_MONEY)
        else:
            self.assertEqual(recieved_money, 0)
    
    def test_get_next_bus_field(self):
        # bus_indexes = [6, 13, 22, 32]
        field = self.board.get_next_bus_field(5)
        self.assertIs(field, self.board.fields[6])

        field = self.board.get_next_bus_field(6)
        self.assertIs(field, self.board.fields[13])

        field = self.board.get_next_bus_field(32)
        self.assertIs(field, self.board.fields[0])
        
        field = self.board.get_next_bus_field(33)
        self.assertIs(field, self.board.fields[0])

if __name__ == "__main__":
    unittest.main()

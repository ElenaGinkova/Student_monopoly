from FieldTypes.Fields import Field
from Button import decision_menu
import pygame as pg
import random


class Exe(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        mess = f"{self.name} - Замаяни сте от вечерта. Следващият ход е наобратно"
        decision_menu(game.screen, mess, [["Да видим", (300, 370), (150, 50)]], game)
        game.get_player().reverse_move()
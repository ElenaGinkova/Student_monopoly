from FieldTypes.Fields import Field
from Visualisations import decision_menu
import pygame as pg
import random


class December8(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        mess = f"{self.name} - Пиянска вечер. -10 живот. 2 дена почивка!"
        decision_menu(game.screen, mess, [["Супер", (300, 370), (150, 50)]], game)
        game.get_player().change_life(-10, game)
        game.get_player().cool_down()
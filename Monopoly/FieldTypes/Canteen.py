from FieldTypes.Fields import Field
from Visualisations import decision_menu
import pygame as pg
import random


class Canteen(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        mess = f"{self.name} - Дали днес ще имате късмет с храната?"
        decision_menu(game.screen, mess, [["Да видим", (300, 370), (150, 50)]], game)
        success = random.randint(0, 1)
        if success == 1:
            mess = f"{self.name} - Днес хапнахте безопасна храна!"
            decision_menu(game.screen, mess, [["Супер", (300, 370), (150, 50)]], game)
            game.get_player().change_life(10, game)
        else:
            mess = f"{self.name} - Днес хапнахте боб с наденица!"
            decision_menu(game.screen, mess, [["Ужас", (300, 370), (150, 50)]], game)
            game.get_player().change_life(-10, game)
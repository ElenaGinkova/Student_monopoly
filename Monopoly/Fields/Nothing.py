from Fields import Field
from Button import decision_menu
import pygame as pg


class Nothing(Field):
    def __init__(self, indx, name, position, action, text):
        super().__init__(indx, name, position, action)
        self.text = text

    def action(self, game):
        decision_menu(game.screen, self.text, [["Добре", (300, 370), (150, 50)]], game)

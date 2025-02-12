from FieldTypes.Fields import Field
from Visualisations import decision_menu
import pygame as pg


class Nothing(Field):
    def __init__(self, indx, name, position, text):
        super().__init__(indx, name, position)
        self.text = text

    def action(self, screen, game):
        decision_menu(game.screen, self.text, [["Добре", (300, 370), (150, 50)]], game)

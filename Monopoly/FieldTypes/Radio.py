from ..FieldTypes.Fields import Field
from ..Visualisations import decision_menu
import pygame as pg
import random


class Radio(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        mess = f"Избере новина за наем за разпространение!"
        dec = decision_menu(game.screen, mess, [["Двойни цени", (200, 370), (150, 50)], ["Половин цени", (400, 370), (150, 50)], ["Безплатно", (600, 370), (150, 50)]], game)
        game.effect = dec
        game.effect_turns_left = 5
from FieldTypes.Fields import Field
from Button import decision_menu
import pygame as pg


class UNSS(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        mess = f"{self.name} - Получавате диплома(ползва се за бонус ход)"
        game.get_player().recieve_diploma()
        decision_menu(game.screen, mess, [["Добре", (300, 370), (150, 50)]], game)
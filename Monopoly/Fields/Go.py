from Fields import Field
from Button import display_message
import pygame as pg


GO_MONEY = 200


class Go(Field):
    def __init__(self, indx, name, position, action):
        super().__init__(indx, name, position, action)

    def action(self, game):
        display_message(self.screen, self.font,500,50,"Стъпихте на \"Джобни от дома\"!")
        pg.display.update()
        pg.time.wait(2000)
        game.get_player().recieve_money(game.screen, game, GO_MONEY)

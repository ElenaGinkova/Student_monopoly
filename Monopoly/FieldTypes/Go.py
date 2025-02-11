from FieldTypes.Fields import Field
from Button import display_message, visualise
import pygame as pg


GO_MONEY = 200


class Go(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        visualise(screen, game)
        display_message(screen, game.font,500,50,"Стъпихте на \"Джобни от дома\"!")
        pg.display.update()
        pg.time.wait(2000)
        game.get_player().recieve_money(game.screen, game, GO_MONEY)

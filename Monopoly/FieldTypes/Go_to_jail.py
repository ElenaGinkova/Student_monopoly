from FieldTypes.Fields import Field
from Button import display_message
import pygame as pg


class Go_to_jail(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, game):
        display_message(self.screen, self.font,500,50,"Беше ви връчена жълта книжка!")
        pg.display.update()
        pg.time.wait(2000)
        game.go_to_jail()


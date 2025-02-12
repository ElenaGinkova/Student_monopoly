from FieldTypes.Fields import Field
from Visualisations import display_message, visualise
import pygame as pg


class GoToJail(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        visualise(screen, game)
        display_message(screen, game.font,500,50,"Беше ви връчена жълта книжка!")
        pg.display.update()
        pg.time.wait(2000)
        game.go_to_jail()


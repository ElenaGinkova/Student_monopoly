from ..Players import Player
from ..Visualisations import decision_menu, display_message
import pygame as pg


class Tutor(Player):
    def __init__(self, name):
        super().__init__(name, "Monopoly/assets/character2.png")
    
    def get_power_name(self):
        return "Депресирай играчи"

    def power(self, game):
        if self.has_power():
            decision_menu(game.screen, "Дай ново домашно и депресирай всички.", [["Екстра", (300, 300), (150, 50)]], game)
            self.depress(game)
            self.use_power()
        else:
            display_message(game.screen, game.font, 500, 50, f"Изхабилите сте силата си! Още {self.power_cooldown} хода")
            pg.display.flip()
            pg.time.wait(1000)
    
    def depress(self, game):
        players = game.get_players().copy()
        players.remove(self)
        for pl in players:
            pl.change_life(-5, game)